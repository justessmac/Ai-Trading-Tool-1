"""Re-check the live Bitcoin rules on spot BTC-USD, including 2014-2017 (never used to pick them).

The live rules were chosen on GBTC 2018-2021. Spot BTC-USD (weekdays only, like IBIT) adds
an independent period, 2014-09 to 2017-12, and more trades for the swing rule.
- Trend half: SMA100 with 5% band, exposure min(1, 0.40/vol20); 0.1% per unit traded.
- Swing half: buy at the close when RSI(2) < th and close > SMA100; sell at the close when
  RSI(2) > x or after 10 days; 0.1% per side. Live: th 10, x 70. Neighbours shown for robustness.

Usage: python -m tradingbot.research.btc_recheck
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from tradingbot.indicators import rsi
from tradingbot.research.data import load_daily
from tradingbot.research.eth_trend import metrics, trend_returns

COST = 0.001
PERIODS = (("2014-09-17", "2017-12-31", "2014-2017 (new)"), ("2018-01-01", "2021-12-31", "2018-2021 (chosen)"),
           ("2022-01-01", "2026-12-31", "2022-2026 (confirm)"))


def swing(c: pd.Series, th: float, x: float, max_hold: int = 10) -> pd.DataFrame:
    r2, sma = rsi(c, 2), c.rolling(100).mean()
    trades, i = [], 100
    while i < len(c) - 1:
        if r2.iloc[i] < th and c.iloc[i] > sma.iloc[i]:
            j = i + 1
            while j < len(c) - 1 and not (r2.iloc[j] > x or j - i >= max_hold):
                j += 1
            trades.append({"entry": c.index[i], "ret": c.iloc[j] / c.iloc[i] - 1 - 2 * COST, "days": j - i})
            i = j + 1
        else:
            i += 1
    return pd.DataFrame(trades)


def run() -> None:
    c = load_daily("BTC-USD")["close"]
    c = c[c.index.dayofweek < 5]
    out = ["# Bitcoin rules re-check on spot BTC (weekdays), incl. unseen 2014-2017\n\n",
           "## Trend half (live: SMA100, 5% band, vol target 40%)\n\n| Period | CAGR | max DD | Sharpe | BTC buy & hold CAGR | B&H DD |\n|---|---|---|---|---|---|\n"]
    tr, bh = trend_returns(c), c.pct_change().fillna(0)
    for a, b, lab in PERIODS:
        m, n = metrics(tr.loc[a:b]), metrics(bh.loc[a:b])
        out.append(f"| {lab} | {m[0]:+.1%} | {m[1]:.0%} | {m[2]:.2f} | {n[0]:+.1%} | {n[1]:.0%} |\n")
    out.append("\n## Swing half (RSI(2) entry threshold / exit level)\n\n| Rule | Period | Trades | Win | Avg | t |\n|---|---|---|---|---|---|\n")
    for th, x in ((10, 70), (5, 70), (15, 70), (10, 60), (10, 80)):
        t = swing(c, th, x)
        for a, b, lab in PERIODS:
            s = t[(t.entry >= a) & (t.entry <= b)]
            ts = s.ret.mean() / (s.ret.std(ddof=1) / np.sqrt(len(s))) if len(s) > 1 else np.nan
            out.append(f"| {'**live** ' if (th, x) == (10, 70) else ''}<{th} / >{x} | {lab} | {len(s)} | {(s.ret > 0).mean():.0%} | "
                       f"{s.ret.mean():+.2%} | {ts:.2f} |\n")
    open("reports/btc_recheck.md", "w").write("".join(out))
    print("".join(out))


if __name__ == "__main__":
    run()
