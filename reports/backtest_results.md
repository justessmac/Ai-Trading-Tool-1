# Backtest results: high win-rate strategy search
In-sample: 2000-01-01 to 2015-01-01 (used for tuning). Out-of-sample: 2015-01-01 onward (never used for tuning).
Pass = ≥1000 total trades, ≥250 OOS trades, win rate ≥85% in BOTH periods, mean-trade t ≥ 2 and PF > 1 in both, and still profitable out-of-sample at 2x costs.

Data: Robinhood daily bars via the Robinhood MCP connector (split-adjusted, NOT dividend-adjusted; split artefacts repaired by `import_robinhood.repair_price_jumps`). Missing dividends bias ETF mean-reversion returns slightly downward.

ETF universe loaded: SPY, QQQ, IWM, DIA, MDY, XLB, XLE, XLF, XLI, XLK, XLP, XLU, XLV, XLY, EFA, EWJ, EWG, EWU, EWC, EWA (cost 0.05%/side, 10% of equity per trade).

Risk-free rate: approximate annual T-bill averages (no daily ^IRX series available).

Options: SPY, weekly entries, Black-Scholes with VIX-based vol + put skew (NOT real option quotes); returns are per dollar of max risk (strike cash for CSPs); portfolio curves put 5% of equity at risk per trade.

## Summary
| Strategy family | Selected config (chosen on IS only) | Configs tried | OOS trades | OOS win | OOS expectancy | Result |
|---|---|---|---|---|---|---|
| etf_rsi2 | `rsi2(th=5, exit=rsi70, trend=True, stop=None, max_hold=20)` | 96 | 893 | 70.3% | +0.321% | fail: IS win 70.9%; OOS win 70.3% |
| etf_crsi2 | `crsi2(th=10, exit=rsi65, trend=True, stop=None, max_hold=20)` | 64 | 457 | 68.1% | +0.286% | fail: trades 966<1000; IS win 71.1%; OOS win 68.1% |
| etf_double7 | `double7(n=10, trend=True, stop=None, max_hold=20)` | 24 | 1553 | 69.6% | +0.312% | fail: IS win 71.0%; OOS win 69.6% |
| etf_ibs | `ibs(th=0.1, exit=prev_high, trend=True, stop=0.1, max_hold=20)` | 48 | 2884 | 64.0% | +0.156% | fail: IS win 65.4%; OOS win 64.0% |
| etf_down_days | `down_days(k=3, exit=prev_high, trend=True, stop=None, max_hold=20)` | 48 | 1803 | 63.9% | +0.145% | fail: IS win 66.6%; OOS win 63.9% |
| etf_hl3 | `hl3(exit=sma5, trend=True, stop=0.1, max_hold=10)` | 16 | 1228 | 62.6% | +0.081% | fail: IS win 65.2%; OOS win 62.6%; OOS t=1.29 PF=1.12; OOS unprofitable at 2x costs |
| etf_bb | `bb(k=2.5, exit=bbmid, trend=True, stop=None, max_hold=20)` | 48 | 355 | 78.0% | +1.179% | fail: trades 675<1000; IS win 74.1%; OOS win 78.0% |
| etf_tom | `tom(enter_rev=6, exit_day=3, trend=False, stop=None, max_hold=15)` | 18 | 2820 | 58.2% | +0.401% | fail: IS win 60.5%; OOS win 58.2% |
| spy_csp | `csp(sd=0.1, ld=None, dte=45, tp=None, stop=None, exit_dte=0, filt=trend)` | 192 | 473 | 95.3% | +0.007% | fail: trades 926<1000; OOS t=0.08 PF=1.02; OOS unprofitable at 2x costs |
| spy_put_spread | `put_spread(sd=0.3, ld=0.05, dte=45, tp=None, stop=None, exit_dte=0, filt=trend)` | 336 | 473 | 89.0% | +6.476% | fail: trades 926<1000 |
| spy_iron_condor | `iron_condor(sd=0.16, ld=0.05, dte=45, tp=None, stop=None, exit_dte=0, filt=trend)` | 336 | 473 | 84.1% | +6.815% | fail: trades 926<1000; OOS win 84.1% |

## Detail

| Strategy | Period | Trades | Win rate (95% low) | Avg win / loss | Expectancy | PF | t | Worst | CAGR | Max DD |
|---|---|---|---|---|---|---|---|---|---|---|
| etf_rsi2 | IS | 950 | 70.9% (≥68.0%) | +1.63% / -2.01% | +0.573% | 1.98 | 7.54 | -12.9% | +3.9% | -11.9% |
| etf_rsi2 | OOS | 893 | 70.3% (≥67.2%) | +1.48% / -2.42% | +0.321% | 1.45 | 3.18 | -37.2% | +2.4% | -15.8% |
| etf_rsi2 | OOS_2x_cost | 893 | 68.0% (≥64.8%) | +1.42% / -2.33% | +0.221% | 1.30 | 2.19 | -37.3% | +1.7% | -15.9% |
| etf_crsi2 | IS | 509 | 71.1% (≥67.0%) | +1.47% / -1.86% | +0.507% | 1.94 | 5.18 | -13.4% | +1.8% | -10.5% |
| etf_crsi2 | OOS | 457 | 68.1% (≥63.6%) | +1.35% / -1.97% | +0.286% | 1.45 | 2.48 | -30.5% | +1.1% | -6.0% |
| etf_crsi2 | OOS_2x_cost | 457 | 64.3% (≥59.8%) | +1.32% / -1.86% | +0.186% | 1.28 | 1.61 | -30.6% | +0.7% | -6.5% |
| etf_double7 | IS | 1706 | 71.0% (≥68.8%) | +2.13% / -3.39% | +0.530% | 1.54 | 6.64 | -18.6% | +6.5% | -19.2% |
| etf_double7 | OOS | 1553 | 69.6% (≥67.3%) | +2.12% / -3.83% | +0.312% | 1.27 | 2.83 | -38.2% | +4.1% | -40.2% |
| etf_double7 | OOS_2x_cost | 1553 | 68.2% (≥65.8%) | +2.06% / -3.76% | +0.212% | 1.18 | 1.92 | -38.2% | +2.7% | -41.1% |
| etf_ibs | IS | 3126 | 65.4% (≥63.7%) | +1.24% / -1.96% | +0.131% | 1.19 | 3.31 | -15.3% | +2.9% | -23.9% |
| etf_ibs | OOS | 2884 | 64.0% (≥62.2%) | +1.20% / -1.71% | +0.156% | 1.25 | 4.15 | -10.8% | +3.9% | -14.8% |
| etf_ibs | OOS_2x_cost | 2884 | 60.9% (≥59.1%) | +1.16% / -1.67% | +0.056% | 1.09 | 1.49 | -10.9% | +1.3% | -19.5% |
| etf_down_days | IS | 1974 | 66.6% (≥64.5%) | +1.23% / -1.56% | +0.296% | 1.57 | 6.93 | -13.2% | +4.2% | -12.8% |
| etf_down_days | OOS | 1803 | 63.9% (≥61.7%) | +1.12% / -1.59% | +0.145% | 1.25 | 3.27 | -16.0% | +2.2% | -10.5% |
| etf_down_days | OOS_2x_cost | 1803 | 60.5% (≥58.2%) | +1.09% / -1.55% | +0.045% | 1.07 | 1.01 | -16.1% | +0.7% | -13.0% |
| etf_hl3 | IS | 1284 | 65.2% (≥62.5%) | +1.15% / -1.68% | +0.163% | 1.28 | 2.82 | -12.6% | +1.5% | -17.9% |
| etf_hl3 | OOS | 1228 | 62.6% (≥59.9%) | +1.17% / -1.74% | +0.081% | 1.12 | 1.29 | -12.5% | +0.8% | -13.2% |
| etf_hl3 | OOS_2x_cost | 1228 | 59.1% (≥56.3%) | +1.14% / -1.69% | -0.019% | 0.97 | -0.31 | -12.6% | -0.2% | -15.0% |
| etf_bb | IS | 320 | 74.1% (≥69.0%) | +2.05% / -4.01% | +0.478% | 1.46 | 2.37 | -21.5% | +1.1% | -8.0% |
| etf_bb | OOS | 355 | 78.0% (≥73.4%) | +2.52% / -3.59% | +1.179% | 2.50 | 5.57 | -30.5% | +3.6% | -11.3% |
| etf_bb | OOS_2x_cost | 355 | 76.9% (≥72.2%) | +2.45% / -3.50% | +1.078% | 2.33 | 5.10 | -30.6% | +3.3% | -11.4% |
| etf_tom | IS | 3576 | 60.5% (≥58.9%) | +2.83% / -2.75% | +0.626% | 1.58 | 9.73 | -20.3% | +15.9% | -43.7% |
| etf_tom | OOS | 2820 | 58.2% (≥56.4%) | +2.33% / -2.28% | +0.401% | 1.42 | 6.86 | -14.4% | +10.1% | -21.0% |
| etf_tom | OOS_2x_cost | 2820 | 56.6% (≥54.7%) | +2.29% / -2.29% | +0.301% | 1.30 | 5.15 | -14.5% | +7.4% | -24.1% |
| spy_csp | IS | 453 | 96.5% (≥94.3%) | +0.31% / -2.12% | +0.223% | 3.97 | 8.63 | -6.4% | +0.4% | -0.5% |
| spy_csp | OOS | 473 | 95.3% (≥93.1%) | +0.31% / -6.25% | +0.007% | 1.02 | 0.08 | -26.4% | +0.0% | -4.2% |
| spy_csp | OOS_2x_cost | 473 | 95.3% (≥93.1%) | +0.30% / -6.39% | -0.009% | 0.97 | -0.09 | -27.0% | -0.0% | -4.3% |
| spy_put_spread | IS | 453 | 87.6% (≥84.3%) | +14.25% / -44.19% | +7.026% | 2.29 | 6.64 | -104.3% | +14.1% | -23.2% |
| spy_put_spread | OOS | 473 | 89.0% (≥85.9%) | +14.41% / -57.75% | +6.476% | 2.02 | 5.43 | -117.6% | +13.5% | -28.9% |
| spy_put_spread | OOS_2x_cost | 473 | 88.8% (≥85.6%) | +13.87% / -59.53% | +5.644% | 1.85 | 4.55 | -135.1% | +11.6% | -31.7% |
| spy_iron_condor | IS | 453 | 87.9% (≥84.5%) | +15.77% / -38.45% | +9.183% | 2.97 | 9.15 | -105.8% | +19.0% | -18.6% |
| spy_iron_condor | OOS | 473 | 84.1% (≥80.6%) | +16.76% / -45.98% | +6.815% | 1.93 | 5.37 | -129.1% | +14.3% | -30.2% |
| spy_iron_condor | OOS_2x_cost | 473 | 83.7% (≥80.1%) | +15.70% / -48.44% | +5.261% | 1.67 | 3.93 | -157.6% | +10.7% | -33.9% |
