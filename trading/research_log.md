# Research log

| Date | Idea | IS (2000–2014) | OOS (2015+) | Decision |
|---|---|---|---|---|
| 2026-09-27 | SPY 200d filter, 2% band (baseline) | full 2000–2026: CAGR +8.2%, max DD −19% | — | adopted as baseline |
| 2026-09-27 | NY-open reversal (gap fade, false break, 30-min fade) | no edge | no edge | rejected (see reports/open_reversal_backtest.md) |
| 2026-09-27 | SPY 30/5-delta put spread | 88% win (model) | 86% win, +3.4%/trade on real prices | needs ~$47k+; parked |
| 2026-09-27 | Bitcoin trend via GBTC→IBIT: SMA 50/100/200 × band 0/5% (6 configs) | SMA100 5%: CAGR +59%, DD −50% (B&H +37%, −77%) | CAGR +41%, DD −26% (B&H +14%, −77%) | adopted as 30% sleeve (combined 70/30: CAGR +24%, DD −24%) |
| 2026-09-27 | Bitcoin crash protection: trailing stop 15/20/25%, vol target 40/60/80%, fast SMA20 exit | stops & fast exit best IS | stops & fast exit worse OOS; vol target 40% cuts worst week −24%→−13% | adopted 50/50 split with vol target 40% (CAGR +21%, DD −20%, 2022+ CAGR +20%); weight chosen after seeing 2022+ data (mild selection bias) |
