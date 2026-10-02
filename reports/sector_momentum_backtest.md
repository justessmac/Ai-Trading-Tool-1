# Sector momentum vs the SPY/QQQ rotation core

**Verdict (2026-10-01): rejected.** All nine sector-momentum settings lost to the plain SPY trend rule in both periods. The best in-sample (top 4 by 252 days) made +3.9%/yr vs +5.0% in 2000-2014, and +5.1% vs +8.0% in 2015-2026. Mega-cap tech dominance and fast sector reversals since 2000 hurt it; the SPY/QQQ rotation stays the core.

Data 2000-01-03 to 2026-09-25.

| Strategy | 2000-2014 CAGR | max DD | Sharpe | 2015-2026 CAGR | max DD | Sharpe |
|---|---|---|---|---|---|---|
| SPY trend (live) | +5.0% | -22% | 0.56 | +8.0% | -21% | 0.72 |
| rotate_126_abs | +7.3% | -24% | 0.62 | +10.6% | -25% | 0.73 |
| sectors top 2 by 63d | +1.8% | -36% | 0.20 | +6.3% | -23% | 0.48 |
| sectors top 3 by 63d | +1.7% | -30% | 0.20 | +4.3% | -21% | 0.39 |
| sectors top 4 by 63d | +2.0% | -30% | 0.24 | +3.6% | -20% | 0.36 |
| sectors top 2 by 126d | +3.1% | -34% | 0.28 | +2.8% | -29% | 0.25 |
| sectors top 3 by 126d | +2.0% | -30% | 0.22 | +3.4% | -24% | 0.31 |
| sectors top 4 by 126d | +3.0% | -28% | 0.31 | +3.8% | -21% | 0.36 |
| sectors top 2 by 252d | +3.5% | -31% | 0.31 | +3.7% | -33% | 0.31 |
| sectors top 3 by 252d | +3.7% | -25% | 0.35 | +5.8% | -23% | 0.48 |
| sectors top 4 by 252d | +3.9% | -22% | 0.39 | +5.1% | -19% | 0.47 |
