# Whole-account simulation of the adopted rules (2018-2026) and a path to $50k

| Part | CAGR | max DD | Sharpe |
|---|---|---|---|
| **whole account** | +16.6% | -20% | 1.09 |
| core (as part of the account) | +12.5% | -25% | 0.80 |
| btc_trend (as part of the account) | +26.2% | -33% | 0.92 |
| btc_swing (as part of the account) | -0.6% | -42% | 0.07 |

| Year | Whole account |
|---|---|
| 2018 | -5.4% |
| 2019 | +19.1% |
| 2020 | +47.2% |
| 2021 | +15.8% |
| 2022 | -8.0% |
| 2023 | +32.2% |
| 2024 | +37.2% |
| 2025 | +8.7% |
| 2026 | +9.7% |

## Months to reach $50,000 from $500 (bootstrap of the 2018-2026 daily returns)

| Monthly deposit | 10% of paths (lucky) | median | 90% of paths (unlucky) | deposits alone, no growth |
|---|---|---|---|---|
| $0 | never (20y) | never (20y) | never (20y) | never (20y) |
| $100 | 121 mo (10.1 y) | 150 mo (12.5 y) | 189 mo (15.8 y) | 495 mo (41.2 y) |
| $250 | 78 mo (6.5 y) | 97 mo (8.1 y) | 121 mo (10.1 y) | 198 mo (16.5 y) |
| $500 | 52 mo (4.3 y) | 63 mo (5.2 y) | 77 mo (6.4 y) | 99 mo (8.2 y) |
| $1000 | 33 mo (2.8 y) | 39 mo (3.2 y) | 46 mo (3.8 y) | 50 mo (4.1 y) |

## Findings (2026-10-01)
- **Whole account, all adopted rules (core at full rotation):** +16.6%/yr, worst drop -20%, Sharpe 1.09 over 2018-2026, vs SPY buy & hold ~+13%/yr with -34%. Losing years: 2018 -5%, 2022 -8%.
- **Deposits dominate:** $500/month reaches $50k in ~5 years (median; 4.3-6.4 y range), vs 8.2 years with no growth. $250/month: ~8 years. $1,000/month: ~3 years. Without deposits, $500 doesn't reach $50k within 20 years.
- **Bitcoin swing quarter is dead weight:** -0.6%/yr on spot BTC, max DD -42% within that quarter. Alternatives for that 25% (approximate, same simulation):

| Swing quarter replaced by | 2018-2021 CAGR / DD | 2022-2026 CAGR / DD |
|---|---|---|
| live (swing) | +17.7% / -20% | +15.7% / -12% |
| more core (75% core) | +23.1% / -23% | +17.2% / -14% |
| more Bitcoin trend (50% trend) | +27.1% / -23% | +21.1% / -16% |

- **Proposal for the Oct 3 weekly review (not adopted yet, because the user asked for swing trading on 2026-09-27):** retire the IBIT swing half and give its 25% to the IBIT trend rule, or split it between trend and core. The Bitcoin trend rule was confirmed on unseen 2014-2017 and 2022-2026 data. The cost is more crypto exposure: 50% of the account in Bitcoin when trending, vol-scaled to 40%.
- Caveats: Bitcoin rules were chosen on 2018-2021 (in-sample here); the bootstrap assumes the future looks like 2018-2026, an unusually strong period for both QQQ and Bitcoin. Treat the projections as optimistic.
