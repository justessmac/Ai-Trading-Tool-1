# SPY put spread on real option prices
Strategy (selected in-sample on modelled prices, unchanged here): sell ~30-delta put, buy ~5-delta put, standard monthly expiry nearest 45 DTE, enter weekly only when SPY > 200-day SMA, hold to expiry.
Data: Robinhood daily closes for expired SPY options; 352 of 352 planned trades priced (2017-11-02 to 2026-09-18).
Returns are per dollar of max risk; the equity columns put 5% of equity at risk per trade.

| Pricing | Trades | Win rate (95% low) | Avg win / loss | Expectancy | PF | t | Worst | CAGR | Max DD |
|---|---|---|---|---|---|---|---|---|---|
| Real prices, base costs | 352 | 86.4% (≥82.4%) | +12.1% / -51.9% | +3.39% | 1.48 | 2.47 | -122% | +6.6% | -25.6% |
| Real prices, 2x costs | 352 | 86.1% (≥82.1%) | +11.5% / -53.8% | +2.45% | 1.33 | 1.70 | -143% | +4.6% | -28.5% |
| Real prices, mid (no costs) | 352 | 86.6% (≥82.7%) | +12.7% / -49.9% | +4.33% | 1.65 | 3.33 | -100% | +8.6% | -22.7% |
| Model prices, same trades | 352 | 87.8% (≥83.9%) | +14.5% / -53.5% | +6.18% | 1.95 | 4.40 | -118% | +12.6% | -28.9% |

## Pass test (all real-price trades are out-of-sample)

| Requirement | Result | Value |
|---|---|---|
| ≥1000 trades | FAIL | 352 |
| win rate ≥85% | pass | 86.4% (95% low 82.4%) |
| mean-trade t ≥2 and PF > 1 | pass | t=2.47, PF=1.48 |
| profitable at 2x costs | pass | +2.45% per trade (t=1.70) |

**Overall: FAIL**

## By entry year (base costs)

| Year | Trades | Win rate | Mean return on risk | Model mean |
|---|---|---|---|---|
| 2017 | 8 | 100% | +10.1% | +14.0% |
| 2018 | 42 | 79% | -2.1% | -1.7% |
| 2019 | 44 | 95% | +12.2% | +11.4% |
| 2020 | 37 | 86% | -3.5% | -4.6% |
| 2021 | 51 | 90% | +6.5% | +11.4% |
| 2022 | 5 | 20% | -55.8% | -50.9% |
| 2023 | 44 | 77% | +2.7% | +8.8% |
| 2024 | 50 | 94% | +9.6% | +13.6% |
| 2025 | 42 | 86% | +0.8% | +3.3% |
| 2026 | 29 | 86% | +3.8% | +9.6% |

## Caveats

- Option prices are Robinhood's daily closing marks, not executable bid/ask quotes; the cost model (0.01 + 2% of price per leg per side, doubled in the stress row) stands in for the spread.
- Robinhood's option history starts in late 2017, so this covers ~9 years and one sample only. Losses cluster at a few sell-offs (expiries in Q4 2018, Mar 2020, Jan-May 2022, Oct 2023, Mar-Apr 2025, Mar 2026) and give back about two-thirds of the gross winnings.
- Expiry is the standard monthly nearest 45 DTE (the model used an exact-45-day expiry), so a few trades settle on different dates than in the model; this explains most model/real sign flips.
- 53 legs used the nearest listed strike (within $3) because the planned $1 strike was not yet listed on the entry day.
- Held to expiry and settled at intrinsic value from SPY's close; early assignment and pin risk are not modelled.
