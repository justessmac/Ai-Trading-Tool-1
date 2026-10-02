# Core sleeve: SPY vs QQQ momentum rotation

**Verdict (2026-10-01): adopted as a change to Strategy 1, phased in (rotate_126_abs).** The new rule: each month hold whichever of SPY/QQQ has the higher 6-month (126-day) return. Hold it only while that fund is above its 200-day SMA (2% band) and its 6-month return is positive; otherwise cash.
- In-sample pick (best Sharpe and CAGR, 2000-2014): +7.3%/yr, max DD -23.5%, vs the live SPY trend rule's +5.0%, -21.7%.
- Confirmed 2015-2026: +10.6%/yr, max DD -24.5%, vs +8.0%, -20.9%. Sharpe 0.73 vs 0.72. Switches 4.7/yr.
- Passes the playbook test (higher CAGR in both periods, DD within -25%, < 12 trades/yr), but only just on drawdown, and it is worse on drawdown than the live rule by ~2-4 points.
- Robustness is mixed: every rotation variant beat the live rule on 2015-2026, but on 2000-2014 the 63- and 252-day versions lost to it. QQQ trend alone was best on 2015-2026 (+13.6%) but fails on 2000-2014 drawdown (-29%).
- Main risk: most of the gain comes from QQQ's mega-cap tech run after 2015. The absolute-momentum and trend exits are what protected it in 2000-2002 and 2022.
- Phase-in (playbook: shift <= 25% of the account per month): from Oct 1, half the core sleeve (25% of the account) follows the rotation. If nothing breaks, the whole sleeve follows from the first check of November.

Daily adjusted closes 2000-01-03 to 2026-09-25 (first 200+ days are warm-up). Costs 0.03%/side per switch; cash earns 0. Selection 2000-2014, confirmation 2015-2026.

| Strategy | 2000-2014 CAGR | max DD | Sharpe | 2015-2026 CAGR | max DD | Sharpe | switches/yr |
|---|---|---|---|---|---|---|---|
| SPY buy & hold | +2.4% | -56% | 0.22 | +11.8% | -34% | 0.73 | 0.0 |
| SPY trend (live) | +5.0% | -22% | 0.56 | +8.0% | -21% | 0.72 | 1.7 |
| QQQ trend | +5.3% | -29% | 0.45 | +13.6% | -25% | 0.87 | 2.2 |
| rotate_63 | +5.1% | -29% | 0.45 | +11.6% | -25% | 0.78 | 3.8 |
| rotate_63_abs | +3.2% | -24% | 0.33 | +9.1% | -22% | 0.67 | 8.8 |
| rotate_126 | +6.1% | -29% | 0.52 | +11.5% | -25% | 0.77 | 3.1 |
| rotate_126_abs | +7.3% | -24% | 0.62 | +10.6% | -25% | 0.73 | 4.7 |
| rotate_252 | +4.8% | -29% | 0.43 | +12.0% | -25% | 0.79 | 3.1 |
| rotate_252_abs | +3.6% | -27% | 0.35 | +11.7% | -25% | 0.78 | 3.5 |
