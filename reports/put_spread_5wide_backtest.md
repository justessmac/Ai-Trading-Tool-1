# SPY $5-wide put credit spread on real option prices

Date: 2026-09-30. Verdict: **rejected for now** (edge per trade, but not reliable out-of-sample and
the account-level result is worse than holding SPY at every account size up to $10k).

Rule (unchanged from the tested wide put spread, nothing tuned): each week, only when SPY > 200-day SMA,
sell the ~30-delta put in the standard monthly expiry nearest 45 DTE and buy the put $5 lower; hold to expiry.
Max loss ~$380-410 per spread. Prices: Robinhood daily marks for the exact contracts (350 of 352 weekly
trades priced). Costs: flat slippage from the mark per leg per side plus $0.04/contract/side fees.

## Verdict
- Per trade it is better than the $1 version: 86% win rate, ~$91 credit vs ~$400 risk, +6.0% per dollar
  risked after costs over all 350 trades (t 2.7), and still positive at double costs (+4.8%, t 2.2).
- But the edge is concentrated in 2017-2021 (+7.6%/trade, t 2.8). On the unseen 2022-2026 data it is
  +4.2%/trade with t 1.2: not statistically reliable.
- At the account level it fails. With the playbook limits (one spread's max loss <= 20% of the account,
  all spreads <= 30%), losses cluster in sell-offs (2018, early 2022, 2023):

  | Account | 2017-2021 CAGR / max DD | 2022-2026 CAGR / max DD | SPY same periods |
  |---|---|---|---|
  | $2,000 | +3.2% / -27% | -3.5% / -19% (only 2 trades possible) | +12.9% / -34%, +10.9% / -24% |
  | $5,000 | +5.4% / -36% | -3.6% / -46% | |
  | $10,000 | +10.7% / -20% | +2.9% / -36% | |

- Sizing is the core problem: a $5-wide spread's ~$400 max loss is 20% of a $2,000 account, so one
  loss knocks the account below the size where the rule allows the next trade, and at $3-5k two or three
  losses in a row cost 25-45%. Selling puts only works with many small positions relative to the account.
- Re-test at >= $25k (each spread <= ~2% of the account, many open at once), and alongside the full
  30/5-delta version that already passed on real prices (+3.4%/trade) at ~$47k.

350 of 352 planned weekly trades priced (2017-11-02 to 2026-09-18). Returns are per dollar of max risk (width - credit).

| Period | Costs | Trades | Win rate | Avg credit | Avg win / loss | Expectancy | t | Worst |
|---|---|---|---|---|---|---|---|---|
| 2017-2021 (IS) | base ($0.02/leg) | 182 | 87.9% | $86 | +21.0% / -89.2% | +7.64% | 2.76 | -101% |
| 2017-2021 (IS) | 2x ($0.04/leg) | 182 | 87.9% | $82 | +19.8% / -90.3% | +6.48% | 2.34 | -102% |
| 2017-2021 (IS) | mid (fees only) | 182 | 87.9% | $90 | +22.2% / -88.2% | +8.83% | 3.18 | -100% |
| 2017-2021 (IS) | % model | 182 | 87.9% | $73 | +17.1% / -112.9% | +1.35% | 0.40 | -192% |
| 2022-2026 (OOS) | base ($0.02/leg) | 168 | 84.5% | $96 | +23.5% / -101.0% | +4.20% | 1.21 | -101% |
| 2022-2026 (OOS) | 2x ($0.04/leg) | 168 | 84.5% | $92 | +22.3% / -102.0% | +3.03% | 0.87 | -102% |
| 2022-2026 (OOS) | mid (fees only) | 168 | 84.5% | $100 | +24.7% / -100.0% | +5.41% | 1.55 | -100% |
| 2022-2026 (OOS) | % model | 168 | 83.9% | $75 | +17.6% / -114.9% | -3.71% | -0.96 | -164% |
| All | base ($0.02/leg) | 350 | 86.3% | $91 | +22.1% / -95.6% | +5.99% | 2.71 | -101% |
| All | 2x ($0.04/leg) | 350 | 86.3% | $87 | +20.9% / -96.6% | +4.82% | 2.19 | -102% |
| All | mid (fees only) | 350 | 86.3% | $95 | +23.4% / -94.6% | +7.19% | 3.25 | -100% |
| All | % model | 350 | 86.0% | $74 | +17.3% / -114.0% | -1.08% | -0.42 | -192% |

## $2,000 account, 1-lot spreads within the playbook limits (max loss/trade <= 20%, total <= 30%)

Same period, SPY buy and hold (with dividends): CAGR +13.0%, max drawdown -34.1%.

| Costs | Spreads taken | End equity | CAGR | Max drawdown |
|---|---|---|---|---|
| base ($0.02/leg) | 23 | $1,602 | -2.5% | -48.8% |
| 2x ($0.04/leg) | 18 | $1,568 | -2.7% | -42.1% |
| mid (fees only) | 2 | $1,684 | -1.9% | -19.9% |
| % model | 12 | $1,618 | -2.4% | -38.8% |

## By entry year (base costs, 1 spread per week, no sizing limits)

| Year | Trades | Win rate | Mean return on risk | Sum P&L per 1-lot ($) |
|---|---|---|---|---|
| 2017 | 8 | 100% | +14.8% | +515 |
| 2018 | 42 | 76% | -6.0% | -1,068 |
| 2019 | 44 | 95% | +18.2% | +3,232 |
| 2020 | 37 | 86% | +8.0% | +1,101 |
| 2021 | 51 | 90% | +8.4% | +1,775 |
| 2022 | 5 | 20% | -75.4% | -1,528 |
| 2023 | 43 | 79% | -1.7% | -240 |
| 2024 | 50 | 94% | +15.5% | +3,153 |
| 2025 | 41 | 85% | +4.7% | +785 |
| 2026 | 29 | 86% | +6.6% | +757 |
