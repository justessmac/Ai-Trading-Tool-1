# SPY $1-wide put credit spread on real option prices

Date: 2026-09-30 (re-run with 21 contracts that were missing from the first run). Verdict: **rejected**.

Rule (unchanged from the tested wide put spread, nothing tuned): each week, only when SPY > 200-day SMA,
sell the ~30-delta put in the standard monthly expiry nearest 45 DTE and buy the put $1 lower; hold to expiry.
Max loss ~$80 per spread. Prices: Robinhood daily marks for the exact contracts. Costs: flat slippage from the
mark per leg per side plus $0.04/contract/side fees; the % model row is the old wide-spread model (too harsh here).

## Verdict
- 85% win rate, but the average credit is only ~$17 against ~$80 of risk: one loss wipes out ~5 wins.
- After $0.02/leg costs: +4.0%/trade in 2017-2021 (t 1.3) and +0.6%/trade in 2022-2026 (t 0.2); negative at
  $0.04/leg. Only the no-slippage "mid" case is clearly positive.
- The bid-ask cost per leg is about the same for $1 and $5 spreads, so on $1 spreads it eats most of the
  premium. See reports/put_spread_5wide_backtest.md for the $5 version.

339 of 352 planned weekly trades priced (2017-11-02 to 2026-09-18). Returns are per dollar of max risk (width - credit).

| Period | Costs | Trades | Win rate | Avg credit | Avg win / loss | Expectancy | t | Worst |
|---|---|---|---|---|---|---|---|---|
| 2017-2021 (IS) | base ($0.02/leg) | 182 | 86.3% | $16 | +19.7% / -94.4% | +4.03% | 1.32 | -105% |
| 2017-2021 (IS) | 2x ($0.04/leg) | 182 | 85.2% | $12 | +14.4% / -92.0% | -1.36% | -0.45 | -110% |
| 2017-2021 (IS) | mid (fees only) | 182 | 86.8% | $20 | +25.6% / -93.1% | +9.96% | 3.23 | -100% |
| 2017-2021 (IS) | % model | 182 | 48.4% | $2 | +7.5% / -55.0% | -24.80% | -3.89 | -529% |
| 2022-2026 (OOS) | base ($0.02/leg) | 157 | 83.4% | $18 | +21.4% / -104.2% | +0.60% | 0.16 | -105% |
| 2022-2026 (OOS) | 2x ($0.04/leg) | 157 | 83.4% | $14 | +15.8% / -108.7% | -4.83% | -1.30 | -110% |
| 2022-2026 (OOS) | mid (fees only) | 157 | 83.4% | $22 | +27.6% / -99.3% | +6.59% | 1.74 | -100% |
| 2022-2026 (OOS) | % model | 157 | 28.0% | $-4 | +4.1% / -48.2% | -33.51% | -5.84 | -361% |
| All | base ($0.02/leg) | 339 | 85.0% | $17 | +20.5% / -99.4% | +2.44% | 1.03 | -105% |
| All | 2x ($0.04/leg) | 339 | 84.4% | $13 | +15.0% / -100.2% | -2.96% | -1.26 | -110% |
| All | mid (fees only) | 339 | 85.3% | $21 | +26.5% / -96.3% | +8.40% | 3.49 | -100% |
| All | % model | 339 | 38.9% | $-1 | +6.3% / -51.3% | -28.84% | -6.66 | -529% |

## $750 account, 1-lot spreads within the playbook limits (max loss/trade <= 20%, total <= 30%)

Same period, SPY buy and hold (with dividends): CAGR +13.0%, max drawdown -34.1%.

| Costs | Spreads taken | End equity | CAGR | Max drawdown |
|---|---|---|---|---|
| base ($0.02/leg) | 125 | $1,007 | +3.4% | -51.9% |
| 2x ($0.04/leg) | 57 | $370 | -7.8% | -55.4% |
| mid (fees only) | 140 | $1,392 | +7.2% | -46.8% |
| % model | 23 | $31 | -30.4% | -96.0% |

## By entry year (base costs, 1 spread per week, no sizing limits)

| Year | Trades | Win rate | Mean return on risk | Sum P&L per 1-lot ($) |
|---|---|---|---|---|
| 2017 | 8 | 100% | +15.7% | +108 |
| 2018 | 42 | 71% | -13.1% | -462 |
| 2019 | 44 | 93% | +15.2% | +542 |
| 2020 | 37 | 86% | +4.3% | +122 |
| 2021 | 51 | 90% | +6.4% | +259 |
| 2022 | 5 | 20% | -79.3% | -329 |
| 2023 | 42 | 79% | -4.4% | -141 |
| 2024 | 48 | 94% | +14.1% | +560 |
| 2025 | 35 | 83% | -1.5% | -46 |
| 2026 | 27 | 85% | +2.0% | +43 |
