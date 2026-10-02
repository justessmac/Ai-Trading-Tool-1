# Stocks in play: 5-minute opening-range breakout (Zarattini, Barbon & Aziz 2024)

**Verdict (2026-10-01): rejected for real money on this universe; keep paper-testing small caps.**
- The config chosen in-sample (long, OR stop, top 5, RV>=1: +0.16R, t 1.7 on 150 trades) failed out-of-sample (-0.12R, t -1.5 on 144 trades).
- No configuration reaches t 2 in either period. With the paper's own settings (10% ATR stop, top 10) only 19% of trades win and the average is about 0R.
- The one hint: a relative-volume filter of 2 or more was positive in both halves for every setting (e.g. long, OR stop, top 3: +0.35R IS, +0.09R OOS). But the samples are small (38-62 trades) and t is below 1.6.
- Limits of this test: 40 popular large/mid caps over 7 months, while the paper's edge comes from a whole-market scan where true stocks in play are often small caps with news. That universe can't be rebuilt historically here, so the forward paper test (morning scan, relative volume >= 2) is the real test.

40 popular Robinhood stocks, 5-minute bars 2026-03-13 to 2026-09-30. In-sample to 2026-06-30, out-of-sample from 2026-07-01. Costs 0.05% per side. R = net return / stop distance.

## All configurations, in-sample (selection) and out-of-sample

| Config | Side | IS trades | IS avg R | IS t | OOS trades | OOS avg R | OOS t |
|---|---|---|---|---|---|---|---|
| stop=atr10, top 3, RV>=1 | both | 185 | +0.136 | 0.49 | 159 | -0.142 | -0.58 |
| stop=atr10, top 3, RV>=1 | long | 86 | +0.249 | 0.48 | 88 | -0.102 | -0.28 |
| stop=atr10, top 3, RV>=2 | both | 88 | +0.738 | 1.41 | 83 | +0.220 | 0.53 |
| stop=atr10, top 3, RV>=2 | long | 38 | +1.432 | 1.33 | 44 | +0.228 | 0.35 |
| stop=atr10, top 5, RV>=1 | both | 305 | +0.244 | 1.17 | 261 | -0.247 | -1.37 |
| stop=atr10, top 5, RV>=1 | long | 150 | +0.476 | 1.33 | 144 | -0.216 | -0.82 |
| stop=atr10, top 5, RV>=2 | both | 106 | +0.652 | 1.44 | 100 | +0.265 | 0.69 |
| stop=atr10, top 5, RV>=2 | long | 45 | +1.173 | 1.27 | 54 | +0.261 | 0.45 |
| stop=atr10, top 10, RV>=1 | both | 520 | +0.116 | 0.78 | 426 | -0.179 | -1.20 |
| stop=atr10, top 10, RV>=1 | long | 254 | +0.273 | 1.12 | 231 | -0.048 | -0.21 |
| stop=atr10, top 10, RV>=2 | both | 122 | +0.641 | 1.56 | 115 | +0.258 | 0.68 |
| stop=atr10, top 10, RV>=2 | long | 51 | +0.885 | 1.08 | 62 | +0.416 | 0.68 |
| stop=or, top 3, RV>=1 | both | 185 | +0.098 | 1.16 | 159 | -0.011 | -0.14 |
| stop=or, top 3, RV>=1 | long | 86 | +0.137 | 1.05 | 88 | -0.017 | -0.17 |
| stop=or, top 3, RV>=2 | both | 88 | +0.175 | 1.42 | 83 | +0.096 | 0.95 |
| stop=or, top 3, RV>=2 | long | 38 | +0.351 | 1.60 | 44 | +0.085 | 0.60 |
| stop=or, top 5, RV>=1 | both | 305 | +0.108 | 1.64 | 261 | -0.057 | -0.86 |
| stop=or, top 5, RV>=1 | long | 150 | +0.163 | 1.68 | 144 | -0.117 | -1.45 |
| stop=or, top 5, RV>=2 | both | 106 | +0.103 | 0.93 | 100 | +0.062 | 0.66 |
| stop=or, top 5, RV>=2 | long | 45 | +0.246 | 1.25 | 54 | +0.066 | 0.48 |
| stop=or, top 10, RV>=1 | both | 520 | +0.020 | 0.39 | 426 | -0.023 | -0.41 |
| stop=or, top 10, RV>=1 | long | 254 | +0.079 | 1.00 | 231 | +0.008 | 0.10 |
| stop=or, top 10, RV>=2 | both | 122 | +0.104 | 0.99 | 115 | -0.014 | -0.16 |
| stop=or, top 10, RV>=2 | long | 51 | +0.201 | 1.10 | 62 | +0.016 | 0.12 |

## Best long-only config in-sample: stop=or, top 5, RV>=1

| Sample | Trades | Win rate | Avg R | Avg return | t |
|---|---|---|---|---|---|
| long IS | 150 | 53% | +0.163 | +0.256% | 1.68 |
| long OOS | 144 | 44% | -0.117 | +0.005% | -1.45 |
| short (paper only) IS | 155 | 50% | +0.056 | +0.169% | 0.62 |
| short (paper only) OOS | 117 | 43% | +0.017 | +0.096% | 0.16 |

## Paper's own settings (stop 10% ATR, top 10, RV>=1), full period

| Sample | Trades | Win rate | Avg R | Avg return | t |
|---|---|---|---|---|---|
| long | 485 | 19% | +0.120 | +0.116% | 0.72 |
| short | 461 | 20% | -0.161 | -0.004% | -1.29 |
| both | 946 | 19% | -0.017 | +0.057% | -0.16 |
