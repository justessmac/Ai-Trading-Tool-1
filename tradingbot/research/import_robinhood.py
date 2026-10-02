"""Merge Robinhood MCP historicals (saved JSON tool results) into data_cache/.

The Robinhood connector is only callable from a Claude session, not from
plain Python. Large `get_equity_historicals` / `get_index_historicals`
results get saved to JSON files; this script parses those files and merges
the bars into `data_cache/<SYMBOL>.csv`, the cache `data.load_daily` reads.

Robinhood daily bars are split-adjusted but NOT dividend-adjusted, so they
are written to both the adjusted and the `_raw` cache files. (For ETFs this
slightly understates mean-reversion returns across ex-dividend dates.)

Usage:
  python -m tradingbot.research.import_robinhood FILE [FILE ...] [--alias UUID=^VIX] [--repair]

Run the full import (all files) with --repair once: repair must see the
whole history, and re-running it on already repaired data is a no-op.
"""
from __future__ import annotations

import argparse
import json

import numpy as np
import pandas as pd

from tradingbot.research.data import CACHE_DIR


def parse_file(path: str, aliases: dict[str, str]) -> dict[str, pd.DataFrame]:
    with open(path) as fh:
        payload = json.load(fh)
    out = {}
    for res in payload["data"]["results"]:
        sym = res.get("symbol") or res.get("instrument_id") or res.get("id")
        sym = aliases.get(sym, sym)
        if "instrument_id" in res and not sym.startswith("^"):
            sym = "^" + sym  # index, e.g. VIX -> ^VIX (the name data.load_daily uses)
        bars = [b for b in res.get("bars", []) if not b.get("interpolated")]
        if not bars:
            continue
        # Equity bars use *_price keys; index bars (e.g. VIX) use *_value.
        key = "price" if "close_price" in bars[0] else "value"
        df = pd.DataFrame(
            {
                "open": [float(b[f"open_{key}"]) for b in bars],
                "high": [float(b[f"high_{key}"]) for b in bars],
                "low": [float(b[f"low_{key}"]) for b in bars],
                "close": [float(b[f"close_{key}"]) for b in bars],
                "volume": [b.get("volume", 0) for b in bars],
            },
            index=pd.to_datetime([b["begins_at"][:10] for b in bars]),
        )
        df.index.name = "date"
        out[sym] = df
    return out


_SPLIT_RATIOS = sorted({n / m for n in range(1, 6) for m in range(1, 6) if n != m})


def _snap_to_split_ratio(factor: float, tol: float = 0.05) -> float:
    """Use the exact split ratio (e.g. 0.25 for a 1:4 reverse split) when the
    observed jump is within `tol` (log) of one, so the genuine market move on
    the jump day is preserved instead of being zeroed out."""
    best = min(_SPLIT_RATIOS, key=lambda r: abs(np.log(factor / r)))
    return best if abs(np.log(factor / best)) < tol else factor


def repair_price_jumps(df: pd.DataFrame, threshold: float = 0.3, window: int = 10) -> tuple[pd.DataFrame, list[str]]:
    """Fix split artefacts in Robinhood daily bars (ETFs only, never VIX).

    Robinhood's history contains (a) splits that were never back-adjusted
    (a permanent level shift, e.g. EWJ's 1:4 reverse split in Nov 2016) and
    (b) short runs of bars quoted at 2x/4x/0.5x the true price that snap
    back within days. A close-to-close move with |log return| > `threshold`
    (~35%, larger than any genuine one-day move in these ETFs, incl. 2008 and
    2020) that is reversed almost exactly within `window` bars is (b): the
    run is rescaled. One that persists is (a): all EARLIER bars are rescaled
    so returns stay correct.
    """
    df = df.copy()
    cols = ["open", "high", "low", "close"]
    log = []
    i = 1
    while i < len(df):
        jump = np.log(df["close"].iat[i] / df["close"].iat[i - 1])
        if abs(jump) <= threshold:
            i += 1
            continue
        back = None
        for k in range(i + 1, min(i + 1 + window, len(df))):
            rev = np.log(df["close"].iat[k] / df["close"].iat[k - 1])
            if abs(rev + jump) < 0.05:
                back = k
                break
        factor = _snap_to_split_ratio(float(np.exp(-jump)))
        if back is not None:
            df.iloc[i:back, df.columns.get_indexer(cols)] *= factor
            log.append(f"{df.index[i].date()}..{df.index[back - 1].date()} bad run x{factor:.3f}")
            i = back
        else:
            df.iloc[:i, df.columns.get_indexer(cols)] /= factor
            log.append(f"{df.index[i].date()} unadjusted split, earlier bars x{1 / factor:.3f}")
            i += 1
    return df, log


def repair_index_spikes(df: pd.DataFrame, threshold: float = 0.5, tol: float = 0.15) -> tuple[pd.DataFrame, list[str]]:
    """Fix single bad bars in index levels such as VIX.

    VIX genuinely jumps (+115% on 2018-02-05), so split logic cannot be used.
    A bar is bad only if its close moved more than `threshold` in log terms
    AND the next close returns to within `tol` of the previous one (e.g.
    Robinhood shows VIX 77.27 on 2023-01-09 between 21.97 and 20.58). Real
    spikes decay over days, so they do not match. Bad bars are replaced with
    the average of their neighbours."""
    df = df.copy()
    c = df["close"].to_numpy(dtype=float, copy=True)
    log = []
    for i in range(1, len(df) - 1):
        jump = np.log(c[i] / c[i - 1])
        if abs(jump) > threshold and abs(np.log(c[i + 1] / c[i - 1])) < tol:
            fill = (c[i - 1] + c[i + 1]) / 2
            log.append(f"{df.index[i].date()} bad bar {c[i]:.2f} -> {fill:.2f}")
            df.iloc[i, df.columns.get_indexer(["open", "high", "low", "close"])] = fill
            c[i] = fill
    return df, log


def repair_cache(symbols: list[str]) -> None:
    for sym in symbols:
        # Index levels (VIX, cached as _VIX) legitimately jump: only fix single bad bars.
        fixer = repair_index_spikes if sym.startswith(("^", "_")) else repair_price_jumps
        for suffix in ("", "_raw"):
            path = CACHE_DIR / f"{sym}{suffix}.csv"
            if not path.exists():
                continue
            df, log = fixer(pd.read_csv(path, index_col="date", parse_dates=["date"]))
            df.to_csv(path)
            if log and suffix == "":
                print(f"[repair] {sym}: " + "; ".join(log))


def merge_into_cache(frames: dict[str, pd.DataFrame]) -> None:
    CACHE_DIR.mkdir(exist_ok=True)
    for sym, df in frames.items():
        for suffix in ("", "_raw"):
            path = CACHE_DIR / f"{sym.replace('^', '_')}{suffix}.csv"
            if path.exists():
                old = pd.read_csv(path, index_col="date", parse_dates=["date"])
                df_all = pd.concat([old, df])
            else:
                df_all = df
            df_all = df_all[~df_all.index.duplicated(keep="last")].sort_index()
            df_all.to_csv(path)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--alias", action="append", default=[], help="ID=SYMBOL mapping, e.g. an index UUID to ^VIX")
    ap.add_argument("--repair", action="store_true", help="after merging, fix split artefacts in all cached ETFs")
    args = ap.parse_args()
    aliases = dict(a.split("=", 1) for a in args.alias)
    for f in args.files:
        frames = parse_file(f, aliases)
        merge_into_cache(frames)
        print(f, "->", ", ".join(f"{s}:{len(d)}" for s, d in frames.items()))
    if args.repair:
        repair_cache(sorted(p.stem for p in CACHE_DIR.glob("*.csv") if not p.stem.endswith("_raw")))


if __name__ == "__main__":
    main()
