"""ETH trend sleeve next to the Bitcoin trend sleeve (backlog item 4).

Same rule as the live IBIT trend half: hold when price > SMA100 x 1.05, exit
when < SMA100 x 0.95 (hysteresis); exposure = min(1, 0.40 / vol20). Spot
BTC-USD and ETH-USD daily closes, weekdays only (the ETFs IBIT/ETHA trade on
weekdays), 0.1% cost per unit of exposure traded. Selection 2018-2021,
confirmation 2022-2026 (same split as the Bitcoin sleeve).
Compared: BTC trend only vs a 50/50 BTC/ETH split of the same sleeve, and ETH alone.

Usage: python -m tradingbot.research.eth_trend
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from tradingbot.research.data import load_daily

COST = 0.001


def trend_returns(c: pd.Series, band: float = 0.05, n: int = 100, vol_target: float | None = 0.40) -> pd.Series:
    sma = c.rolling(n).mean()
    state, on = False, []
    for x, s in zip(c.values, sma.values):
        if not np.isnan(s):
            state = True if x > s * (1 + band) else False if x < s * (1 - band) else state
        on.append(state)
    on = pd.Series(on, index=c.index, dtype=float)
    r = c.pct_change()
    vol = r.rolling(20).std() * np.sqrt(252)
    w = on * (np.minimum(1, vol_target / vol) if vol_target else 1)
    w = w.fillna(0)
    return (w.shift() * r - (w - w.shift()).abs() * COST).fillna(0)


def metrics(r: pd.Series) -> tuple[float, float, float]:
    eq = (1 + r).cumprod()
    yrs = (r.index[-1] - r.index[0]).days / 365.25
    return eq.iloc[-1] ** (1 / yrs) - 1, float((eq / eq.cummax() - 1).min()), r.mean() / r.std() * np.sqrt(252)


def run() -> None:
    px = pd.concat({s: load_daily(s)["close"] for s in ("BTC-USD", "ETH-USD")}, axis=1, sort=True).dropna()
    px = px[px.index.dayofweek < 5]
    rb, re = trend_returns(px["BTC-USD"]), trend_returns(px["ETH-USD"])
    variants = {"BTC trend (live)": rb, "ETH trend": re, "50/50 BTC+ETH trend": 0.5 * rb + 0.5 * re,
                "BTC buy & hold": px["BTC-USD"].pct_change().fillna(0), "ETH buy & hold": px["ETH-USD"].pct_change().fillna(0)}
    corr = px.pct_change().corr().iloc[0, 1]
    out = ["# ETH trend sleeve next to Bitcoin\n\n",
           f"Spot daily closes (weekdays) {px.index[0].date()} to {px.index[-1].date()}; SMA100 with 5% band, exposure min(1, 0.40/vol20), "
           f"0.1% cost per unit traded. Daily return correlation BTC/ETH: {corr:.2f}.\n\n",
           "| Sleeve | 2018-2021 CAGR | max DD | Sharpe | 2022-2026 CAGR | max DD | Sharpe |\n|---|---|---|---|---|---|---|\n"]
    for name, r in variants.items():
        a, b = metrics(r.loc["2018":"2021"]), metrics(r.loc["2022":])
        out.append(f"| {name} | {a[0]:+.1%} | {a[1]:.0%} | {a[2]:.2f} | {b[0]:+.1%} | {b[1]:.0%} | {b[2]:.2f} |\n")
    open("reports/eth_trend_backtest.md", "w").write("".join(out))
    print("".join(out))


if __name__ == "__main__":
    run()
