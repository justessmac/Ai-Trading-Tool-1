# Dip-buy sleeve: SPY plus QQQ/IWM candidates

**Verdict (2026-10-01): adopted for Strategy 3, effective 2026-10-05.** The playbook bars changing a strategy twice in one week, and Strategy 3 was adopted on 2026-09-29.
- Hypothesis: add QQQ/IWM as extra dip candidates. Within the multi-fund variants, the in-sample pick is "lowest RSI(2) of SPY/QQQ/IWM" (2001-2014 sleeve +5.2%/yr, t 2.6, vs the live SPY-only +1.3%).
- Confirmed 2015-2026: +6.6%/yr, 75% win, +0.55%/trade, t 3.0, max DD -15%, vs SPY-only +4.7%, -12%. About 12 trades/yr, at the playbook's ~12 limit.
- Caveats: QQQ alone was the single best fund in-sample but not better than SPY OOS. IWM alone was weak OOS (t 1.2, DD -32%). The gain comes from more opportunities, not a better signal.
- Note: this test fills at the signal-day close (the live 15:48 order); the playbook's original SPY numbers used next-day fills, so the two tables are not directly comparable.

RSI(2)<10 above the 200-day SMA, exit RSI(2)>70 or 10 days; one position at a time; 0.03%/side.

| Variant | IS trades/yr | IS avg | IS win | IS t | IS sleeve CAGR | OOS trades/yr | OOS avg | OOS win | OOS t | OOS sleeve CAGR | OOS DD |
|---|---|---|---|---|---|---|---|---|---|---|---|
| SPY only (live) | 5.8 | +0.25% | 69% | 1.03 | +1.3% | 8.4 | +0.57% | 82% | 3.63 | +4.7% | -12% |
| QQQ only | 7.4 | +0.74% | 72% | 3.56 | +5.4% | 8.5 | +0.56% | 75% | 2.52 | +4.6% | -14% |
| IWM only | 7.1 | +0.56% | 74% | 2.13 | +3.8% | 6.7 | +0.42% | 73% | 1.15 | +2.5% | -32% |
| SPY>QQQ>IWM priority | 10.1 | +0.46% | 72% | 2.50 | +4.5% | 11.9 | +0.46% | 75% | 2.59 | +5.4% | -16% |
| lowest RSI of 3 | 10.2 | +0.53% | 73% | 2.56 | +5.2% | 12.1 | +0.55% | 75% | 3.01 | +6.6% | -15% |
| SPY>QQQ | 8.4 | +0.48% | 73% | 2.29 | +3.9% | 10.2 | +0.51% | 78% | 2.98 | +5.1% | -16% |
