"""Stocks-in-play opening-range breakout (Zarattini, Barbon & Aziz 2024) on Robinhood 5-minute bars.

Paper rules: each day rank stocks (price > $5, 14-day average volume >= 1M,
14-day ATR > $0.50) by relative volume = first-5-minute volume / its 14-day
average; trade the top N with relative volume >= 1. Direction = colour of the
first 5-minute bar (no trade on a doji). Stop order at the opening-range high
(long) or low (short), placed for the 9:35 bar onward; stop loss 10% of the
14-day ATR from entry; exit at the 15:55 bar's open. Size = equal risk.

Variants tested (chosen on the in-sample period only):
  stop  "atr10" (paper) or "or" (other side of the opening range, our paper-trade rule)
  top_n 3 / 5 / 10, min relative volume 1 or 2.

Data: Robinhood serves 5-minute bars only from 2026-02-23, so this is ~7 months
on the stocks in data_cache/intraday (popular Robinhood names; that list is
from today, a mild look-ahead bias). In-sample 2026-02-23..06-30, out-of-sample
07-01 onward. Costs 0.05% per side (fills at the trigger price plus that).
Robinhood cannot short, so long-only results are what the account could trade.
"""
from __future__ import annotations

import itertools

import numpy as np
import pandas as pd

from tradingbot.research.open_reversal import INTRA_DIR, OOS_START, load
from tradingbot.research.stats import trade_stats

ETFS = {"SPY", "QQQ", "IWM", "DIA", "XLF", "XLE", "XLK", "SMH", "TLT", "GLD"}
COST = 0.0005  # per side
LOOKBACK = 14


def stocks() -> list[str]:
    return sorted(p.stem for p in INTRA_DIR.glob("*.csv") if p.stem not in ETFS and not p.stem.startswith("5min"))


def day_table(sym: str) -> pd.DataFrame:
    """One row per day: opening bar, prior-14-day stats, and the day's bars for the walk."""
    df = load(sym)
    df["date"] = df.index.normalize()
    g = df.groupby("date")
    daily = pd.DataFrame({"high": g.high.max(), "low": g.low.min(), "close": g.close.last(), "volume": g.volume.sum()})
    first = df[df.index.time == pd.Timestamp("09:30").time()].set_index("date")
    daily = daily.join(first[["open", "high", "low", "close", "volume"]].add_prefix("or_"), how="inner")
    prev_close = daily.close.shift()
    tr = pd.concat([daily.high - daily.low, (daily.high - prev_close).abs(), (daily.low - prev_close).abs()], axis=1).max(axis=1)
    daily["atr"] = tr.rolling(LOOKBACK).mean().shift()
    daily["avg_vol"] = daily.volume.rolling(LOOKBACK).mean().shift()
    daily["rel_vol"] = daily.or_volume / daily.or_volume.rolling(LOOKBACK).mean().shift()
    daily["prev_close"] = prev_close
    daily["sym"] = sym
    return daily.dropna(subset=["atr", "rel_vol"])


def trade(day: pd.DataFrame, side: int, level: float, stop_dist: float) -> tuple[float, float, str] | None:
    """Walk 9:35..15:50 bars; return (entry, exit, reason) or None if never triggered."""
    bars = day[(day.index.time >= pd.Timestamp("09:35").time())]
    entry = None
    for t, b in bars.iterrows():
        if t.time() >= pd.Timestamp("15:55").time():
            return (entry, b.open, "close") if entry is not None else None
        if entry is None:
            if (side > 0 and b.high > level) or (side < 0 and b.low < level):
                fill = max(b.open, level) if side > 0 else min(b.open, level)
                entry, stop = fill, fill - side * stop_dist
                # the stop can be hit later in the entry bar; order unknown, so check the bar's far side
                if (side > 0 and b.low <= stop and b.close < entry) or (side < 0 and b.high >= stop and b.close > entry):
                    return entry, stop, "stop (entry bar)"
            continue
        if (side > 0 and b.low <= stop) or (side < 0 and b.high >= stop):
            gap = (b.open <= stop) if side > 0 else (b.open >= stop)
            return entry, (b.open if gap else stop), "stop"
    return (entry, bars.iloc[-1].close, "last bar") if entry is not None else None


def candidates() -> tuple[pd.DataFrame, dict[str, pd.DataFrame]]:
    tables, bars = [], {}
    for s in stocks():
        bars[s] = load(s)
        tables.append(day_table(s))
    t = pd.concat(tables).reset_index().rename(columns={"index": "date"})
    t = t[(t.prev_close > 5) & (t.avg_vol >= 1e6 / 1) & (t.atr > 0.5)]
    t = t[t.or_close != t.or_open]
    t["side"] = np.where(t.or_close > t.or_open, 1, -1)
    return t, bars


def run_cfg(cands: pd.DataFrame, bars: dict, stop: str, top_n: int, min_rv: float, cache: dict) -> pd.DataFrame:
    rows = []
    c = cands[cands.rel_vol >= min_rv]
    for d, grp in c.groupby("date"):
        for r in grp.nlargest(top_n, "rel_vol").itertuples():
            key = (r.sym, d, stop)
            if key not in cache:
                day = bars[r.sym][bars[r.sym].index.normalize() == d]
                level = r.or_high if r.side > 0 else r.or_low
                dist = 0.10 * r.atr if stop == "atr10" else (r.or_high - r.or_low)
                cache[key] = (trade(day, r.side, level, dist), dist)
            res, dist = cache[key]
            if res is None:
                continue
            entry, exit_, why = res
            ret = r.side * (exit_ - entry) / entry - 2 * COST
            rows.append({"date": d, "sym": r.sym, "side": r.side, "rel_vol": r.rel_vol, "entry": entry, "exit": exit_,
                         "reason": why, "ret": ret, "R": ret / (dist / entry)})
    return pd.DataFrame(rows)


def _line(name: str, sub: pd.DataFrame) -> str:
    if len(sub) < 2:
        return f"| {name} | {len(sub)} | - | - | - | - |\n"
    t = sub.R.mean() / (sub.R.std(ddof=1) / np.sqrt(len(sub)))
    return (f"| {name} | {len(sub)} | {(sub.R > 0).mean():.0%} | {sub.R.mean():+.3f} | {sub.ret.mean():+.3%} | {t:.2f} |\n")


def run() -> None:
    cands, bars = candidates()
    cache: dict = {}
    grid = list(itertools.product(("atr10", "or"), (3, 5, 10), (1.0, 2.0)))
    out = ["# Stocks in play: 5-minute opening-range breakout (Zarattini, Barbon & Aziz 2024)\n\n",
           f"{len(stocks())} popular Robinhood stocks, 5-minute bars {cands.date.min().date()} to {cands.date.max().date()}. "
           "In-sample to 2026-06-30, out-of-sample from 2026-07-01. Costs 0.05% per side. R = net return / stop distance.\n\n",
           "## All configurations, in-sample (selection) and out-of-sample\n\n",
           "| Config | Side | IS trades | IS avg R | IS t | OOS trades | OOS avg R | OOS t |\n|---|---|---|---|---|---|---|---|\n"]
    best, best_t = None, -np.inf
    results = {}
    for stop, n, rv in grid:
        df = run_cfg(cands, bars, stop, n, rv, cache)
        results[(stop, n, rv)] = df
        for side_name, sub in (("both", df), ("long", df[df.side > 0])):
            is_, oos = sub[sub.date < OOS_START], sub[sub.date >= OOS_START]
            ti = is_.R.mean() / (is_.R.std(ddof=1) / np.sqrt(len(is_))) if len(is_) > 1 else np.nan
            to = oos.R.mean() / (oos.R.std(ddof=1) / np.sqrt(len(oos))) if len(oos) > 1 else np.nan
            out.append(f"| stop={stop}, top {n}, RV>={rv:g} | {side_name} | {len(is_)} | {is_.R.mean():+.3f} | {ti:.2f} | "
                       f"{len(oos)} | {oos.R.mean():+.3f} | {to:.2f} |\n")
            if side_name == "long" and ti > best_t:
                best, best_t = (stop, n, rv), ti
    df = results[best]
    out.append(f"\n## Best long-only config in-sample: stop={best[0]}, top {best[1]}, RV>={best[2]:g}\n\n"
               "| Sample | Trades | Win rate | Avg R | Avg return | t |\n|---|---|---|---|---|---|\n")
    for side_name, sub in (("long", df[df.side > 0]), ("short (paper only)", df[df.side < 0])):
        out.append(_line(f"{side_name} IS", sub[sub.date < OOS_START]))
        out.append(_line(f"{side_name} OOS", sub[sub.date >= OOS_START]))
    paper = results[("atr10", 10, 1.0)]
    out.append("\n## Paper's own settings (stop 10% ATR, top 10, RV>=1), full period\n\n"
               "| Sample | Trades | Win rate | Avg R | Avg return | t |\n|---|---|---|---|---|---|\n")
    out += [_line("long", paper[paper.side > 0]), _line("short", paper[paper.side < 0]), _line("both", paper)]
    open("reports/stocks_in_play_backtest.md", "w").write("".join(out))
    df.to_csv("reports/stocks_in_play_trades.csv", index=False)
    print("".join(out))


if __name__ == "__main__":
    run()
