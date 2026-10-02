"""What should the core hold when the SPY/QQQ rotation (Strategy 1b) is out? (cash vs bonds/gold)

When the rotation's state is cash, hold instead: SHY (1-3y Treasuries), IEF (7-10y), TLT
(20y+), GLD, or the defensive fund with the best 126-day return among SHY/IEF/GLD (monthly
pick, like the equity side). Costs 0.03%/side per switch. Data from 2002-07 (bond ETFs),
GLD from 2004-11 (before that the GLD variants hold cash). Selection 2003-2014,
confirmation 2015-2026.

Usage: python -m tradingbot.research.risk_off_asset
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from tradingbot.research import core_rotation as cr
from tradingbot.research.data import load_daily

DEF = ("SHY", "IEF", "TLT", "GLD")


def run() -> None:
    px = pd.concat({s: load_daily(s)["close"] for s in ("SPY", "QQQ") + DEF}, axis=1, sort=True).loc["1999-03-10":]
    px = px.dropna(subset=["SPY", "QQQ"])
    hold = cr.strategies(px[["SPY", "QQQ"]])["rotate_126_abs"]
    month = pd.Series(px.index.to_period("M"), index=px.index)
    ms = month.ne(month.shift())
    mom = px / px.shift(126) - 1
    variants = {"cash (live)": hold}
    for d in DEF:
        variants[f"{d} when out"] = hold.where(hold != "", np.where(px[d].notna(), d, ""))
    cand = ["SHY", "IEF", "GLD"]
    best = mom[cand].apply(lambda r: r.dropna().idxmax() if r.notna().any() else "", axis=1).where(ms).ffill().fillna("")
    best_pos = pd.Series([b if b and mom.loc[d, b] > 0 else "" for d, b in best.items()], index=px.index)
    variants["best of SHY/IEF/GLD (126d>0) when out"] = hold.where(hold != "", best_pos)
    out = ["# Core risk-off asset: cash vs bonds/gold when the rotation is out\n\n",
           "| When out, hold | 2003-2014 CAGR | max DD | Sharpe | 2015-2026 CAGR | max DD | Sharpe |\n|---|---|---|---|---|---|---|\n"]
    sub = px.ffill().fillna(0)
    for name, h in variants.items():
        r = cr.simulate(sub, h)
        a, b = cr.metrics(r.loc["2003":"2014"]), cr.metrics(r.loc["2015":])
        out.append(f"| {name} | {a[0]:+.1%} | {a[1]:.0%} | {a[2]:.2f} | {b[0]:+.1%} | {b[1]:.0%} | {b[2]:.2f} |\n")
    open("reports/risk_off_asset_backtest.md", "w").write("".join(out))
    print("".join(out))


if __name__ == "__main__":
    run()
