"""Overnight vs intraday returns (close-to-open vs open-to-close) on SPY, QQQ, IWM.

Overnight strategy: buy at the close, sell at the next open, every day. Costs per side:
0.002% (a 1-cent spread on SPY, commission-free) and 0.01% (stress). Adjusted OHLC (the
same adjustment factor applies to open and close within a day). Selection 2001-2014,
confirmation 2015-2026. Note: this needs a market-on-open sell and a market-on-close buy
every day; the bot can't place orders at the open reliably today (one 15:48 check per day).

Usage: python -m tradingbot.research.overnight
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from tradingbot.research.data import load_daily
from tradingbot.research.eth_trend import metrics


def run() -> None:
    out = ["# Overnight vs intraday returns\n\n",
           "| Fund | Leg | Cost/side | 2001-2014 CAGR | max DD | 2015-2026 CAGR | max DD |\n|---|---|---|---|---|---|---|\n"]
    for sym in ("SPY", "QQQ", "IWM"):
        d = load_daily(sym)
        on = d.open / d.close.shift() - 1
        intra = d.close / d.open - 1
        bh = d.close.pct_change()
        rows = [("buy & hold", bh, 0.0), ("intraday (open->close)", intra, 0.0),
                ("overnight (close->open)", on, 0.0), ("overnight", on, 0.00002), ("overnight", on, 0.0001)]
        for name, r, c in rows:
            rr = (r - (2 * c if name.startswith("overnight") else 0)).fillna(0)
            a, b = metrics(rr.loc["2001":"2014"]), metrics(rr.loc["2015":])
            out.append(f"| {sym} | {name} | {c:.3%} | {a[0]:+.1%} | {a[1]:.0%} | {b[0]:+.1%} | {b[1]:.0%} |\n")
    open("reports/overnight_backtest.md", "w").write("".join(out))
    print("".join(out))


if __name__ == "__main__":
    run()
