"""NY-open reversal strategies on 5-minute bars (Robinhood data, Feb 2026+).

Robinhood's connector only serves 5-minute equity bars from 2026-02-23, so
this is a ~7-month test across 20 liquid ETFs and large stocks. Bars come
from saved get_equity_historicals tool results (`import`), cached per symbol
in data_cache/intraday/<SYM>.csv with New York timestamps.

Families tested (all enter after the 9:30 open, exit by 15:55 at the latest):
  gap_fade   open gaps >= g vs the prior close; enter at the 9:35 bar's open
             against the gap; target = prior close; stop = the first 5-minute
             bar's extreme on the gap side (+ a small buffer).
  false_break  "Judas swing": price breaks the first-15-minute opening range,
             then a bar closes back inside it before 11:00; enter at the next
             bar's open toward the other side of the range; stop = the
             breakout extreme; target = the opposite side of the range.
  fade30     fade the first 30 minutes' move when it exceeds k x the symbol's
             average absolute 30-minute opening move; stop = the 9:30-10:00
             extreme; hold to the exit time.

Fills: next-bar open; if a bar touches both stop and target the stop is
assumed first. Costs: 0.03% per side. Returns are % of the position.
In-sample (selection): 2026-02-23..2026-06-30. Out-of-sample: 2026-07-01+.
Robinhood does not allow short selling, so long-only results are reported
separately: they are what this account could actually trade.
"""
from __future__ import annotations

import glob
import itertools
import json
import sys
from dataclasses import dataclass

import numpy as np
import pandas as pd

from tradingbot.research.data import CACHE_DIR
from tradingbot.research.real_options import TOOL_RESULTS
from tradingbot.research.stats import trade_stats

INTRA_DIR = CACHE_DIR / "intraday"
COST = 0.0003  # per side
OOS_START = pd.Timestamp("2026-07-01")
TZ = "America/New_York"


def import_results() -> None:
    frames: dict[str, list[pd.DataFrame]] = {}
    for f in glob.glob(str(TOOL_RESULTS / "**" / "mcp-Robinhood_Trading-get_equity_historicals-*.txt"), recursive=True):
        try:
            payload = json.load(open(f))
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue
        for res in payload.get("data", {}).get("results", []):
            if res.get("interval") != "5minute":
                continue
            bars = [b for b in res["bars"] if not b.get("interpolated") and b.get("session", "reg") == "reg"]
            if not bars:
                continue
            df = pd.DataFrame(
                {
                    "open": [float(b["open_price"]) for b in bars],
                    "high": [float(b["high_price"]) for b in bars],
                    "low": [float(b["low_price"]) for b in bars],
                    "close": [float(b["close_price"]) for b in bars],
                    "volume": [int(b["volume"]) for b in bars],
                },
                index=pd.to_datetime([b["begins_at"] for b in bars], utc=True).tz_convert(TZ).tz_localize(None),
            )
            frames.setdefault(res["symbol"], []).append(df)
    INTRA_DIR.mkdir(parents=True, exist_ok=True)
    for sym, parts in frames.items():
        old = INTRA_DIR / f"{sym}.csv"
        if old.exists():  # merge with earlier fetches instead of overwriting them
            parts = [pd.read_csv(old, index_col="time", parse_dates=True)] + parts
        df = pd.concat(parts).sort_index()
        df = df[~df.index.duplicated(keep="last")]
        df.to_csv(INTRA_DIR / f"{sym}.csv", index_label="time")
        print(sym, len(df), df.index.min(), df.index.max())


def load(sym: str) -> pd.DataFrame:
    return pd.read_csv(INTRA_DIR / f"{sym}.csv", index_col="time", parse_dates=True)


def symbols() -> list[str]:
    return sorted(p.stem for p in INTRA_DIR.glob("*.csv"))


@dataclass(frozen=True)
class Cfg:
    family: str
    params: tuple

    def label(self) -> str:
        return f"{self.family}(" + ", ".join(f"{k}={v}" for k, v in self.params) + ")"

    def p(self, key):
        return dict(self.params)[key]


def _walk(day: pd.DataFrame, start_i: int, side: int, entry: float, stop: float, target: float | None, exit_time: str):
    """Walk bars from start_i; return (exit_price, reason)."""
    t_exit = pd.Timestamp(exit_time).time()
    for i in range(start_i, len(day)):
        bar = day.iloc[i]
        if day.index[i].time() >= t_exit:
            return bar.open, "time"
        hit_stop = bar.low <= stop if side > 0 else bar.high >= stop
        if hit_stop:
            gap_through = bar.open <= stop if side > 0 else bar.open >= stop
            return (bar.open if gap_through else stop), "stop"
        if target is not None and (bar.high >= target if side > 0 else bar.low <= target):
            return target, "target"
    return day.iloc[-1].close, "close"


def _trade(sym, day, side, entry_i, stop, target, exit_time):
    entry = day.iloc[entry_i].open
    if (side > 0 and stop >= entry) or (side < 0 and stop <= entry):
        return None
    if target is not None and ((side > 0 and target <= entry) or (side < 0 and target >= entry)):
        return None
    px, why = _walk(day, entry_i, side, entry, stop, target, exit_time)
    gross = side * (px / entry - 1)
    return {"symbol": sym, "entry_date": day.index[entry_i], "exit_date": day.index[entry_i].normalize(),
            "side": side, "ret": gross - 2 * COST, "reason": why}


def simulate(sym: str, df: pd.DataFrame, cfg: Cfg) -> list[dict]:
    out = []
    days = [g for _, g in df.groupby(df.index.date)]
    avg30 = []
    for k, day in enumerate(days):
        day = day.between_time("09:30", "15:55")
        if len(day) < 70 or day.index[0].time() != pd.Timestamp("09:30").time():
            continue
        prev = days[k - 1] if k > 0 else None
        if cfg.family == "gap_fade" and prev is not None:
            pc = prev.close.iloc[-1]
            gap = day.open.iloc[0] / pc - 1
            if abs(gap) < cfg.p("g"):
                continue
            side = -1 if gap > 0 else 1
            first = day.iloc[0]
            buf = 0.001 * pc
            stop = first.high + buf if side < 0 else first.low - buf
            tr = _trade(sym, day, side, 1, stop, pc, cfg.p("exit"))
        elif cfg.family == "false_break":
            orng = day.iloc[:3]
            hi, lo = orng.high.max(), orng.low.min()
            tr, broke, ext = None, 0, None
            for i in range(3, len(day) - 1):
                if day.index[i].time() >= pd.Timestamp("11:00").time():
                    break
                b = day.iloc[i]
                if broke == 0:
                    if b.high > hi:
                        broke, ext = 1, b.high
                    elif b.low < lo:
                        broke, ext = -1, b.low
                    else:
                        continue
                ext = max(ext, b.high) if broke > 0 else min(ext, b.low)
                back_inside = b.close < hi if broke > 0 else b.close > lo
                if back_inside:
                    side = -broke
                    tgt = lo if side < 0 else hi
                    if cfg.p("target") == "mid":
                        tgt = (hi + lo) / 2
                    tr = _trade(sym, day, side, i + 1, ext, tgt, cfg.p("exit"))
                    break
        elif cfg.family == "fade30":
            first30 = day.between_time("09:30", "09:55")
            move = first30.close.iloc[-1] / first30.open.iloc[0] - 1
            hist = avg30[-20:]
            avg30.append(abs(move))
            if len(hist) < 10 or abs(move) < cfg.p("k") * np.mean(hist):
                continue
            side = -1 if move > 0 else 1
            stop = first30.high.max() if side < 0 else first30.low.min()
            stop = stop * (1 + 0.001 * -side)
            tr = _trade(sym, day, side, 6, stop, None, cfg.p("exit"))
        else:
            continue
        if tr:
            out.append(tr)
    return out


def grid() -> list[Cfg]:
    g = []
    for gap, ex in itertools.product([0.003, 0.005, 0.01], ["10:30", "12:00", "15:55"]):
        g.append(Cfg("gap_fade", (("g", gap), ("exit", ex))))
    for tgt, ex in itertools.product(["mid", "other"], ["12:00", "15:55"]):
        g.append(Cfg("false_break", (("target", tgt), ("exit", ex))))
    for k, ex in itertools.product([1.0, 1.5, 2.0], ["12:00", "15:55"]):
        g.append(Cfg("fade30", (("k", k), ("exit", ex))))
    return g


def _stats(t: pd.DataFrame):
    if len(t) == 0:
        return None
    s = trade_stats(t.assign(weight=0.1), years=None)
    return s


def run(out_path: str = "reports/open_reversal_backtest.md") -> None:
    data = {s: load(s) for s in symbols()}
    rows, best = [], {}
    all_trades = {}
    for cfg in grid():
        t = pd.DataFrame([tr for s, df in data.items() for tr in simulate(s, df, cfg)])
        if t.empty:
            continue
        t = t.sort_values("entry_date")
        all_trades[cfg.label()] = t
        for side_name, sub in (("both", t), ("long", t[t.side > 0])):
            is_, oos = sub[sub.entry_date < OOS_START], sub[sub.entry_date >= OOS_START]
            si, so = _stats(is_), _stats(oos)
            rows.append((cfg, side_name, si, so, oos))
    lines = [
        "# NY-open reversal backtest (5-minute bars)\n\n",
        f"Data: Robinhood 5-minute regular-hours bars for {len(data)} symbols ({', '.join(data)}), "
        f"{min(d.index.min() for d in data.values()).date()} to {max(d.index.max() for d in data.values()).date()}. "
        "Robinhood serves no older intraday history, so this is ~7 months only.\n\n",
        f"In-sample (used to pick configs): before {OOS_START.date()}. Out-of-sample: from {OOS_START.date()}. "
        f"Costs {COST:.2%} per side. Returns are % of position per trade.\n\n",
        "'long' = long-only trades (Robinhood does not allow shorting stocks).\n\n",
        "| Config | Side | IS trades | IS win | IS exp | IS t | OOS trades | OOS win | OOS exp | OOS t |\n|---|---|---|---|---|---|---|---|---|---|\n",
    ]
    for cfg, side_name, si, so, _ in rows:
        f = lambda s, a: "-" if s is None else a(s)
        lines.append(
            f"| `{cfg.label()}` | {side_name} | {f(si, lambda s: s.n)} | {f(si, lambda s: f'{s.win_rate:.0%}')} | "
            f"{f(si, lambda s: f'{s.expectancy:+.3%}')} | {f(si, lambda s: f'{s.t_stat:.2f}')} | "
            f"{f(so, lambda s: s.n)} | {f(so, lambda s: f'{s.win_rate:.0%}')} | "
            f"{f(so, lambda s: f'{s.expectancy:+.3%}')} | {f(so, lambda s: f'{s.t_stat:.2f}')} |\n"
        )
    # Selection: best in-sample t-stat per family among long-only configs with >= 30 IS trades.
    lines.append("\n## Selected on in-sample only (long-only, best IS t per family, >= 30 IS trades)\n\n"
                 "| Family | Config | IS t | OOS trades | OOS win | OOS exp | OOS t |\n|---|---|---|---|---|---|---|\n")
    for fam in ("gap_fade", "false_break", "fade30"):
        cands = [r for r in rows if r[0].family == fam and r[1] == "long" and r[2] is not None and r[2].n >= 30]
        if not cands:
            continue
        cfg, _, si, so, _ = max(cands, key=lambda r: r[2].t_stat)
        lines.append(
            f"| {fam} | `{cfg.label()}` | {si.t_stat:.2f} | {so.n if so else 0} | "
            f"{f'{so.win_rate:.0%}' if so else '-'} | {f'{so.expectancy:+.3%}' if so else '-'} | "
            f"{f'{so.t_stat:.2f}' if so else '-'} |\n"
        )
    lines.append(f"\n{len(rows) // 2} configurations were tried; with this many tries on 7 months of data, "
                 "an in-sample t of ~2 is expected by chance alone.\n")
    open(out_path, "w").write("".join(lines))
    print("".join(lines))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "run"
    if cmd == "import":
        import_results()
    else:
        run()
