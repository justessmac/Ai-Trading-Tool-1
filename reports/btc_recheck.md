# Bitcoin rules re-check on spot BTC (weekdays), incl. unseen 2014-2017

**Verdict (2026-10-01):**
- **Trend half: confirmed.** On 2014-2017 spot data, which was never used to pick the rule: +120%/yr, max DD -28%, Sharpe 2.1, vs buy & hold +188%, -61%. It lags in raging bull markets but roughly halves the drawdown in all three periods.
- **Swing half: weaker than believed. Kept for now, flagged for the 2026-10-03 weekly review.**
  - On spot BTC the live rule made +0.07%/trade in 2018-2021, the period it was chosen on. On GBTC it showed +4.2%/trade there, so GBTC's premium/discount swings likely inflated the original result.
  - On the new 2014-2017 data it made +4.9%/trade (t 2.6); in 2022-2026 +1.2%/trade (t 1.2).
  - Pooled on spot: 63 trades, about +1.9%/trade, still positive but not significant within any single period.
  - RSI(2)<5 was positive in all three periods but has only 8-11 trades each. No change on this evidence; switching to <5 would be fitting noise.

## Trend half (live: SMA100, 5% band, vol target 40%)

| Period | CAGR | max DD | Sharpe | BTC buy & hold CAGR | B&H DD |
|---|---|---|---|---|---|
| 2014-2017 (new) | +120.1% | -28% | 2.14 | +187.5% | -61% |
| 2018-2021 (chosen) | +36.2% | -33% | 1.04 | +33.3% | -81% |
| 2022-2026 (confirm) | +25.4% | -25% | 0.92 | +13.2% | -67% |

## Swing half (RSI(2) entry threshold / exit level)

| Rule | Period | Trades | Win | Avg | t |
|---|---|---|---|---|---|
| **live** <10 / >70 | 2014-2017 (new) | 18 | 78% | +4.91% | 2.63 |
| **live** <10 / >70 | 2018-2021 (chosen) | 20 | 65% | +0.07% | 0.04 |
| **live** <10 / >70 | 2022-2026 (confirm) | 25 | 72% | +1.24% | 1.20 |
| <5 / >70 | 2014-2017 (new) | 11 | 82% | +5.98% | 1.71 |
| <5 / >70 | 2018-2021 (chosen) | 9 | 78% | +4.08% | 2.48 |
| <5 / >70 | 2022-2026 (confirm) | 8 | 75% | +3.28% | 1.58 |
| <15 / >70 | 2014-2017 (new) | 26 | 69% | +2.20% | 1.91 |
| <15 / >70 | 2018-2021 (chosen) | 29 | 72% | +1.13% | 0.73 |
| <15 / >70 | 2022-2026 (confirm) | 31 | 71% | +0.85% | 0.96 |
| <10 / >60 | 2014-2017 (new) | 18 | 72% | +3.43% | 1.96 |
| <10 / >60 | 2018-2021 (chosen) | 22 | 64% | +0.13% | 0.08 |
| <10 / >60 | 2022-2026 (confirm) | 26 | 77% | +1.32% | 1.41 |
| <10 / >80 | 2014-2017 (new) | 16 | 75% | +3.45% | 1.54 |
| <10 / >80 | 2018-2021 (chosen) | 20 | 65% | -0.02% | -0.01 |
| <10 / >80 | 2022-2026 (confirm) | 24 | 67% | +1.89% | 1.56 |
