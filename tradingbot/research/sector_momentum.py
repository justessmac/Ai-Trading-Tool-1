"""Sector momentum (Moskowitz-Grinblatt style) vs the SPY/QQQ rotation core.

Universe: the 9 original SPDR sector ETFs (XLB XLE XLF XLI XLK XLP XLU XLV XLY, since 1998-12).
On the first trading day of each month rank by L-day return (L = 63/126/252), hold the top K
(K = 2/3/4) equally, each only while it is above its 2%-band SMA200 and its L-day return > 0
(otherwise that slot is cash). Monthly rebalance; 0.03%/side on turnover. Adjusted closes.
Selection 2000-2014, confirmation 2015-2026. Benchmarks: SPY trend, rotate_126_abs (Strategy 1b).

Usage: python -m tradingbot.research.sector_momentum
"""
from __future__ import annotations

import itertools

import numpy as np
import pandas as pd

from tradingbot.research import core_rotation as cr
from tradingbot.research.data import load_daily

SECTORS = ("XLB", "XLE", "XLF", "XLI", "XLK", "XLP", "XLU", "XLV", "XLY")


def weights(px: pd.DataFrame, L: int, K: int) -> pd.DataFrame:
    on = pd.concat({c: cr.band_state(px[c]) for c in px.columns}, axis=1)
    mom = px / px.shift(L) - 1
    month = pd.Series(px.index.to_period("M"), index=px.index)
    ms = month.ne(month.shift())
    w = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    picks: list[str] = []
    for d in px.index:
        if ms[d] and mom.loc[d].notna().all():
            picks = list(mom.loc[d].nlargest(K).index)
        for p in picks:
            if on.loc[d, p] and mom.loc[d, p] > 0:
                w.loc[d, p] = 1.0 / K
    return w


def returns(px: pd.DataFrame, w: pd.DataFrame) -> pd.Series:
    nxt = px.pct_change().shift(-1)
    r = (w * nxt).sum(axis=1) - w.diff().abs().sum(axis=1) * cr.COST
    return r.shift(1).fillna(0)


def run() -> None:
    px = pd.concat({s: load_daily(s)["close"] for s in SECTORS + ("SPY", "QQQ")}, axis=1, sort=True).dropna()
    sec = px[list(SECTORS)]
    out = ["# Sector momentum vs the SPY/QQQ rotation core\n\n",
           f"Data {px.index[0].date()} to {px.index[-1].date()}.\n\n",
           "| Strategy | 2000-2014 CAGR | max DD | Sharpe | 2015-2026 CAGR | max DD | Sharpe |\n|---|---|---|---|---|---|---|\n"]
    strats = cr.strategies(px[["SPY", "QQQ"]])
    for name in ("SPY trend (live)", "rotate_126_abs"):
        r = cr.simulate(px[["SPY", "QQQ"]], strats[name])
        a, b = cr.metrics(r.loc["2000":"2014"]), cr.metrics(r.loc["2015":])
        out.append(f"| {name} | {a[0]:+.1%} | {a[1]:.0%} | {a[2]:.2f} | {b[0]:+.1%} | {b[1]:.0%} | {b[2]:.2f} |\n")
    for L, K in itertools.product((63, 126, 252), (2, 3, 4)):
        r = returns(sec, weights(sec, L, K))
        a, b = cr.metrics(r.loc["2000":"2014"]), cr.metrics(r.loc["2015":])
        out.append(f"| sectors top {K} by {L}d | {a[0]:+.1%} | {a[1]:.0%} | {a[2]:.2f} | {b[0]:+.1%} | {b[1]:.0%} | {b[2]:.2f} |\n")
    open("reports/sector_momentum_backtest.md", "w").write("".join(out))
    print("".join(out))


if __name__ == "__main__":
    run()
