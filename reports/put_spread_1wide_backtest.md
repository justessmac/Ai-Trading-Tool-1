# SPY $1-wide put credit spread on real option prices

Date: 2026-09-30. Verdict: **rejected** (fails the adoption test after costs).

Rule (unchanged from the tested wide put spread, nothing tuned): each week, only when SPY > 200-day SMA,
sell the ~30-delta put in the standard monthly expiry nearest 45 DTE and buy the put $1 lower; hold to expiry.
Max loss per spread ~$80, so it fits a $750 account (limit: 20% per trade, 30% total).
Prices: Robinhood daily marks for the exact contracts (654 SPY puts). Costs: flat slippage from the mark
per leg per side plus $0.04/contract/side fees; the % model row is the old wide-spread model (too harsh here).

## Verdict
- Win rate is high (86%) as expected, but the average credit is only ~$17-21 against ~$80 of risk:
  one loss wipes out ~5 wins.
- At realistic costs ($0.02/leg) the edge is +6.1%/trade in 2017-2021 but only +1.8% (t 0.5) in 2022-2026;
  at $0.04/leg it is negative. Only the no-slippage "mid" case is clearly positive (+7.8%, t 2.1 OOS).
- On a $750 account within the playbook limits: +4.5%/yr with a -40% drawdown (base costs), worse than
  just holding SPY, and the drawdown breaks the -25% limit.
- Same lesson as the call-spread test: on $1-wide spreads the bid-ask costs eat most of the premium.
  The wide version (30/5 delta, +3.4%/trade on real prices) still works, but it needs ~$47k.
- Next: re-test with $5-wide spreads (credit ~5x larger vs the same per-leg cost) once the account can
  hold a ~$400 max loss within the 20% rule (~$2,000 account).

318 of 352 planned weekly trades priced (2017-11-02 to 2026-09-18). Returns are per dollar of max risk (width - credit).

| Period | Costs | Trades | Win rate | Avg credit | Avg win / loss | Expectancy | t | Worst |
|---|---|---|---|---|---|---|---|---|
| 2017-2021 (IS) | base ($0.02/leg) | 164 | 87.8% | $16 | +19.7% / -91.8% | +6.08% | 2.03 | -105% |
| 2017-2021 (IS) | 2x ($0.04/leg) | 164 | 86.6% | $12 | +14.4% / -88.1% | +0.68% | 0.23 | -110% |
| 2017-2021 (IS) | mid (fees only) | 164 | 88.4% | $20 | +25.6% / -91.3% | +12.03% | 3.97 | -100% |
| 2017-2021 (IS) | % model | 164 | 52.4% | $2 | +7.3% / -55.0% | -22.33% | -3.30 | -529% |
| 2022-2026 (OOS) | base ($0.02/leg) | 154 | 84.4% | $18 | +21.4% / -104.2% | +1.83% | 0.50 | -105% |
| 2022-2026 (OOS) | 2x ($0.04/leg) | 154 | 84.4% | $14 | +15.8% / -108.6% | -3.62% | -0.99 | -110% |
| 2022-2026 (OOS) | mid (fees only) | 154 | 84.4% | $22 | +27.6% / -99.2% | +7.83% | 2.10 | -100% |
| 2022-2026 (OOS) | % model | 154 | 28.6% | $-4 | +4.1% / -46.3% | -31.91% | -5.59 | -361% |
| All | base ($0.02/leg) | 318 | 86.2% | $17 | +20.5% / -98.6% | +4.02% | 1.70 | -105% |
| All | 2x ($0.04/leg) | 318 | 85.5% | $13 | +15.1% / -98.8% | -1.40% | -0.60 | -110% |
| All | mid (fees only) | 318 | 86.5% | $21 | +26.5% / -95.7% | +10.00% | 4.19 | -100% |
| All | % model | 318 | 40.9% | $-1 | +6.2% / -49.9% | -26.97% | -6.05 | -529% |

## $750 account, 1-lot spreads within the playbook limits (max loss/trade <= 20%, total <= 30%)

| Costs | Spreads taken | End equity | CAGR | Max drawdown |
|---|---|---|---|---|
| base ($0.02/leg) | 119 | $1,108 | +4.5% | -40.2% |
| 2x ($0.04/leg) | 57 | $400 | -6.9% | -50.3% |
| mid (fees only) | 141 | $1,610 | +9.0% | -34.2% |
| % model | 23 | $31 | -30.4% | -96.0% |

## By entry year (base costs, 1 spread per week, no sizing limits)

| Year | Trades | Win rate | Mean return on risk | Sum P&L per 1-lot ($) |
|---|---|---|---|---|
| 2017 | 8 | 100% | +15.7% | +108 |
| 2018 | 42 | 71% | -13.1% | -462 |
| 2019 | 44 | 93% | +15.2% | +542 |
| 2020 | 37 | 86% | +4.3% | +122 |
| 2021 | 33 | 100% | +17.9% | +498 |
| 2022 | 2 | 0% | -104.9% | -173 |
| 2023 | 42 | 79% | -4.4% | -141 |
| 2024 | 48 | 94% | +14.1% | +560 |
| 2025 | 35 | 83% | -1.5% | -46 |
| 2026 | 27 | 85% | +2.0% | +43 |
