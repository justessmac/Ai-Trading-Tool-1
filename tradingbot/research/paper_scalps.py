"""Score the morning 'stocks in play' paper trades from 5-minute bars.

Rules (fixed in the daily research routine, not tuned):
- opening range (OR) = the 9:30-9:35 ET bar;
- entry = first bar starting 9:35 or later that trades through the OR level in
  the setup direction, filled at that level plus 0.05% slippage (at the bar's
  open if it gaps through);
- stop = the other side of the OR, checked from the bar after entry (the order
  of high and low inside the entry bar is unknown);
- exit = the 15:55 bar's open; costs 0.1% round trip.
Shorts are paper only (Robinhood cannot short).

Usage: python -m tradingbot.research.paper_scalps YYYY-MM-DD
reads trading/scans/morning/<date>.csv and data_cache/intraday/5min_<date>.json
(a saved get_equity_historicals result), appends to trading/paper/stocks_in_play.csv
and rewrites the summary in trading/paper/README.md.
"""
from __future__ import annotations

import csv
import json
import math
import sys
from pathlib import Path

import pandas as pd

SLIP = 0.0005
COST = 0.001
LOG = Path("trading/paper/stocks_in_play.csv")
README = Path("trading/paper/README.md")
FIELDS = ["date", "ticker", "direction", "entered", "entry_time_et", "entry", "stop", "exit",
          "r_multiple", "pct_return", "reason"]


def _bars(raw: dict, symbol: str) -> pd.DataFrame:
    res = next(r for r in raw["data"]["results"] if r["symbol"] == symbol)
    df = pd.DataFrame(res["bars"])
    df["t"] = pd.to_datetime(df.begins_at).dt.tz_convert("America/New_York")
    for c in ("open", "high", "low", "close"):
        df[c] = df[c + "_price"].astype(float)
    if "interpolated" in df:
        df = df[df.interpolated != True]  # noqa: E712  gap-fill bars carry no trades
    return df.set_index("t")[["open", "high", "low", "close"]]


def score(row: dict, bars: pd.DataFrame, date: str) -> dict:
    short = row["direction"].lower().startswith("short")
    hi, lo = float(row["or_high"]), float(row["or_low"])
    level, stop = (lo, hi) if short else (hi, lo)
    out = {"date": date, "ticker": row["ticker"], "direction": "short" if short else "long",
           "entered": "no", "stop": stop}
    day = pd.Timestamp(date, tz="America/New_York")
    after = bars[bars.index >= day + pd.Timedelta(hours=9, minutes=35)]
    exit_bar = bars[bars.index <= day + pd.Timedelta(hours=15, minutes=55)]
    hit = (after.low < level) if short else (after.high > level)
    if not hit.any():
        out["reason"] = "never broke the OR level"
        return out
    t = after.index[hit.values][0]
    before = after[after.index < t]
    opp = (before.high > hi) if short else (before.low < lo)
    notes = [f"OR {'high' if short else 'low'} broken first at {before.index[opp.values][0]:%H:%M}"] if opp.any() else []
    o = after.loc[t, "open"]
    fill = min(o, level) if short else max(o, level)
    entry = fill * (1 - SLIP) if short else fill * (1 + SLIP)
    later = after[after.index > t]
    stopped = (later.high >= stop) if short else (later.low <= stop)
    if stopped.any():
        ts = later.index[stopped.values][0]
        px = max(later.loc[ts, "open"], stop) if short else min(later.loc[ts, "open"], stop)
        why = f"stopped {ts:%H:%M}"
    else:
        last = exit_bar.index[-1]
        at_close = last.strftime("%H:%M") == "15:55"
        px = float(exit_bar.iloc[-1].open if at_close else exit_bar.iloc[-1].close)
        why = "exit 15:55 open" if at_close else f"no trades at 15:55; exit at the {last:%H:%M} bar's close"
    gross = (entry - px) / entry if short else (px - entry) / entry
    net = gross - COST
    risk = abs(stop - entry) / entry
    out.update(entered="yes", entry_time_et=f"{t:%H:%M}", entry=round(entry, 4), exit=round(px, 4),
               r_multiple=round(net / risk, 2), pct_return=round(100 * net, 2),
               reason="; ".join([why] + notes))
    return out


def summary(df: pd.DataFrame) -> str:
    lines = ["| Side | Paper trades | Win rate | Avg R | Total R | t-stat |\n|---|---|---|---|---|---|\n"]
    for side, sub in (("long", df[df.direction == "long"]), ("short", df[df.direction == "short"]), ("all", df)):
        r = sub.r_multiple.astype(float)
        n = len(r)
        t = r.mean() / (r.std(ddof=1) / math.sqrt(n)) if n > 1 and r.std(ddof=1) > 0 else float("nan")
        lines.append(f"| {side} | {n} | {(r > 0).mean():.0%} | {r.mean():+.2f} | {r.sum():+.2f} | {t:.2f} |\n"
                     if n else f"| {side} | 0 | - | - | - | - |\n")
    return "".join(lines)


def run(date: str) -> pd.DataFrame:
    raw = json.load(open(f"data_cache/intraday/5min_{date}.json"))
    rows = list(csv.DictReader(open(f"trading/scans/morning/{date}.csv")))
    new = [score(r, _bars(raw, r["ticker"]), date) for r in rows]
    LOG.parent.mkdir(parents=True, exist_ok=True)
    old = pd.read_csv(LOG) if LOG.exists() else pd.DataFrame(columns=FIELDS)
    old = old[old.date != date]
    df = pd.concat([old, pd.DataFrame(new, columns=FIELDS)], ignore_index=True)
    df.to_csv(LOG, index=False)
    taken = df[df.entered == "yes"]
    body = README.read_text().split("<!-- end summary -->", 1)[-1] if README.exists() else ""
    README.write_text(
        "# Paper trades: stocks in play (opening-range breaks)\n\n"
        f"Running summary, updated {date}. R = net return / risk to the stop. Costs 0.1% round trip.\n\n"
        + summary(taken) + f"\nSetups scanned: {len(df)}; entered: {len(taken)}.\n<!-- end summary -->" + body)
    print(pd.DataFrame(new).to_string(index=False))
    print(summary(taken))
    return df


if __name__ == "__main__":
    run(sys.argv[1])
