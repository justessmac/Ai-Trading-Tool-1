"""Volatility-scaled core (backlog item 8) on top of the SPY/QQQ rotation (Strategy 1b).

Exposure = min(1, target / realised vol), realised vol = annualised stdev of
the held fund's last N daily returns (N = 20 or 60), target = 12/15/20%.
Cash otherwise (earns 0). Turnover costs 0.03% per unit traded; weights only
move when they change by more than 5 points (like the live rebalance rule).
Selection 2000-2014, confirmation 2015-2026.

Usage: python -m tradingbot.research.vol_scaled_core
"""
from __future__ import annotations

import itertools

import numpy as np
import pandas as pd

from tradingbot.research import core_rotation as cr
from tradingbot.research.data import load_daily


def run() -> None:
    px = pd.concat({s: load_daily(s)["close"] for s in ("SPY", "QQQ")}, axis=1, sort=True).dropna().loc["1999-03-10":]
    hold = cr.strategies(px)["rotate_126_abs"]
    rets = px.pct_change()
    nxt = pd.Series(0.0, index=px.index)  # next day's return of the fund held after today's close
    for c in px.columns:
        nxt[hold == c] = rets[c].shift(-1)[hold == c]
    out = ["# Volatility-scaled core (on the SPY/QQQ rotation)\n\n",
           "| Variant | 2000-2014 CAGR | max DD | Sharpe | 2015-2026 CAGR | max DD | Sharpe | avg exposure when in |\n"
           "|---|---|---|---|---|---|---|---|\n"]
    base = cr.simulate(px, hold)
    a, b = cr.metrics(base.loc["2000":"2014"]), cr.metrics(base.loc["2015":])
    out.append(f"| rotation, unscaled (Strategy 1b) | {a[0]:+.1%} | {a[1]:.0%} | {a[2]:.2f} | {b[0]:+.1%} | {b[1]:.0%} | {b[2]:.2f} | 100% |\n")
    for n, target in itertools.product((20, 60), (0.12, 0.15, 0.20)):
        vols = {c: rets[c].rolling(n).std() * np.sqrt(252) for c in px.columns}
        raw = pd.Series(0.0, index=px.index)
        for c in px.columns:
            m = hold == c
            raw[m] = np.minimum(1, target / vols[c][m])
        raw = raw.fillna(0)
        w, cur = [], 0.0
        for x in raw.values:
            if x == 0 or abs(x - cur) > 0.05:
                cur = x
            w.append(cur)
        w = pd.Series(w, index=px.index)
        # w decided at today's close, earns tomorrow's return of the held fund
        r = (w * nxt - (w - w.shift()).abs() * cr.COST).shift(1).fillna(0)
        a, b = cr.metrics(r.loc["2000":"2014"]), cr.metrics(r.loc["2015":])
        out.append(f"| vol{n}, target {target:.0%} | {a[0]:+.1%} | {a[1]:.0%} | {a[2]:.2f} | {b[0]:+.1%} | {b[1]:.0%} | {b[2]:.2f} | "
                   f"{w[w > 0].mean():.0%} |\n")
    open("reports/vol_scaled_core_backtest.md", "w").write("".join(out))
    print("".join(out))


if __name__ == "__main__":
    run()
