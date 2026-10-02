# NY-open reversal backtest (5-minute bars)

Data: Robinhood 5-minute regular-hours bars for 20 symbols (AAPL, AMD, AMZN, AVGO, DIA, GLD, GOOGL, IWM, JPM, META, MSFT, NVDA, QQQ, SMH, SPY, TLT, TSLA, XLE, XLF, XLK), 2026-02-23 to 2026-09-25. Robinhood serves no older intraday history, so this is ~7 months only.

In-sample (used to pick configs): before 2026-07-01. Out-of-sample: from 2026-07-01. Costs 0.03% per side. Returns are % of position per trade.

'long' = long-only trades (Robinhood does not allow shorting stocks).

| Config | Side | IS trades | IS win | IS exp | IS t | OOS trades | OOS win | OOS exp | OOS t |
|---|---|---|---|---|---|---|---|---|---|
| `gap_fade(g=0.003, exit=10:30)` | both | 1201 | 37% | -0.049% | -2.80 | 809 | 36% | -0.051% | -2.42 |
| `gap_fade(g=0.003, exit=10:30)` | long | 567 | 40% | -0.019% | -0.73 | 352 | 37% | -0.029% | -0.92 |
| `gap_fade(g=0.003, exit=12:00)` | both | 1201 | 34% | -0.062% | -3.25 | 809 | 34% | -0.050% | -2.17 |
| `gap_fade(g=0.003, exit=12:00)` | long | 567 | 38% | -0.006% | -0.22 | 352 | 34% | -0.017% | -0.47 |
| `gap_fade(g=0.003, exit=15:55)` | both | 1201 | 33% | -0.065% | -3.23 | 809 | 34% | -0.052% | -2.17 |
| `gap_fade(g=0.003, exit=15:55)` | long | 567 | 36% | -0.021% | -0.70 | 352 | 34% | -0.025% | -0.66 |
| `gap_fade(g=0.005, exit=10:30)` | both | 998 | 37% | -0.051% | -2.50 | 650 | 35% | -0.045% | -1.79 |
| `gap_fade(g=0.005, exit=10:30)` | long | 461 | 40% | -0.011% | -0.36 | 279 | 38% | -0.010% | -0.27 |
| `gap_fade(g=0.005, exit=12:00)` | both | 998 | 33% | -0.066% | -2.96 | 650 | 34% | -0.042% | -1.50 |
| `gap_fade(g=0.005, exit=12:00)` | long | 461 | 39% | +0.005% | 0.13 | 279 | 35% | +0.011% | 0.26 |
| `gap_fade(g=0.005, exit=15:55)` | both | 998 | 32% | -0.068% | -2.89 | 650 | 33% | -0.045% | -1.55 |
| `gap_fade(g=0.005, exit=15:55)` | long | 461 | 36% | -0.011% | -0.31 | 279 | 35% | +0.002% | 0.04 |
| `gap_fade(g=0.01, exit=10:30)` | both | 557 | 37% | -0.043% | -1.33 | 373 | 32% | -0.037% | -0.93 |
| `gap_fade(g=0.01, exit=10:30)` | long | 257 | 42% | +0.026% | 0.53 | 167 | 35% | +0.016% | 0.27 |
| `gap_fade(g=0.01, exit=12:00)` | both | 557 | 32% | -0.061% | -1.72 | 373 | 30% | -0.041% | -0.93 |
| `gap_fade(g=0.01, exit=12:00)` | long | 257 | 40% | +0.045% | 0.83 | 167 | 32% | +0.042% | 0.63 |
| `gap_fade(g=0.01, exit=15:55)` | both | 557 | 31% | -0.072% | -1.91 | 373 | 29% | -0.031% | -0.67 |
| `gap_fade(g=0.01, exit=15:55)` | long | 257 | 36% | +0.015% | 0.26 | 167 | 33% | +0.042% | 0.59 |
| `false_break(target=mid, exit=12:00)` | both | 1337 | 41% | -0.057% | -5.23 | 877 | 40% | -0.062% | -4.94 |
| `false_break(target=mid, exit=12:00)` | long | 641 | 43% | -0.059% | -3.44 | 446 | 38% | -0.074% | -4.22 |
| `false_break(target=mid, exit=15:55)` | both | 1337 | 42% | -0.051% | -4.48 | 877 | 41% | -0.060% | -4.58 |
| `false_break(target=mid, exit=15:55)` | long | 641 | 43% | -0.048% | -2.72 | 446 | 38% | -0.071% | -3.97 |
| `false_break(target=other, exit=12:00)` | both | 1399 | 36% | -0.035% | -2.35 | 917 | 30% | -0.074% | -4.50 |
| `false_break(target=other, exit=12:00)` | long | 670 | 37% | -0.031% | -1.36 | 457 | 30% | -0.063% | -2.72 |
| `false_break(target=other, exit=15:55)` | both | 1399 | 34% | -0.032% | -1.94 | 917 | 29% | -0.078% | -4.45 |
| `false_break(target=other, exit=15:55)` | long | 670 | 35% | -0.019% | -0.76 | 457 | 28% | -0.068% | -2.71 |
| `fade30(k=1.0, exit=12:00)` | both | 661 | 33% | -0.005% | -0.19 | 478 | 26% | -0.085% | -3.25 |
| `fade30(k=1.0, exit=12:00)` | long | 322 | 34% | +0.037% | 0.93 | 235 | 25% | -0.088% | -2.27 |
| `fade30(k=1.0, exit=15:55)` | both | 661 | 24% | -0.046% | -1.61 | 478 | 22% | -0.122% | -4.48 |
| `fade30(k=1.0, exit=15:55)` | long | 322 | 25% | -0.023% | -0.56 | 235 | 23% | -0.119% | -2.91 |
| `fade30(k=1.5, exit=12:00)` | both | 359 | 33% | +0.010% | 0.28 | 255 | 25% | -0.089% | -2.70 |
| `fade30(k=1.5, exit=12:00)` | long | 183 | 34% | +0.061% | 1.06 | 138 | 25% | -0.088% | -1.78 |
| `fade30(k=1.5, exit=15:55)` | both | 359 | 25% | -0.005% | -0.11 | 255 | 22% | -0.115% | -3.03 |
| `fade30(k=1.5, exit=15:55)` | long | 183 | 25% | +0.031% | 0.50 | 138 | 23% | -0.097% | -1.73 |
| `fade30(k=2.0, exit=12:00)` | both | 197 | 29% | +0.016% | 0.30 | 121 | 20% | -0.131% | -2.74 |
| `fade30(k=2.0, exit=12:00)` | long | 105 | 34% | +0.077% | 0.99 | 64 | 20% | -0.132% | -1.91 |
| `fade30(k=2.0, exit=15:55)` | both | 197 | 24% | +0.009% | 0.16 | 121 | 17% | -0.172% | -4.24 |
| `fade30(k=2.0, exit=15:55)` | long | 105 | 28% | +0.057% | 0.70 | 64 | 20% | -0.170% | -3.43 |

## Selected on in-sample only (long-only, best IS t per family, >= 30 IS trades)

| Family | Config | IS t | OOS trades | OOS win | OOS exp | OOS t |
|---|---|---|---|---|---|---|
| gap_fade | `gap_fade(g=0.01, exit=12:00)` | 0.83 | 167 | 32% | +0.042% | 0.63 |
| false_break | `false_break(target=other, exit=15:55)` | -0.76 | 457 | 28% | -0.068% | -2.71 |
| fade30 | `fade30(k=1.5, exit=12:00)` | 1.06 | 138 | 25% | -0.088% | -1.78 |

19 configurations were tried; with this many tries on 7 months of data, an in-sample t of ~2 is expected by chance alone.
