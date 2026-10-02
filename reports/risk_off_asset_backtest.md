# Core risk-off asset: cash vs bonds/gold when the rotation is out

**Verdict (2026-10-01): T-bills/short Treasuries adopted for the core's "out" cash, effective 2026-10-05; bonds and gold rejected.**
- SHY when out: +9.9% vs +9.4%/yr (2003-2014, DD -21% vs -24%) and +10.7% vs +10.6% (2015-2026, same DD). A small, consistent gain with no extra risk. Live implementation: SGOV (0-3 month T-bills), already used for idle cash in Strategy 4.
- TLT failed: in-sample DD -26%, and in 2022 it fell with stocks (OOS DD -42%, CAGR below cash). IEF passed CAGR in both periods but breached the drawdown limit OOS (-30%).
- GLD only helped after 2015 (+14.2%) and hurt before (+9.1%, DD -33%): regime-dependent, rejected. Same for the best-of-three momentum pick (in-sample +8.5% < cash).
- Lesson: since 2022 stocks and bonds can fall together, so "bonds as the safe asset" is not reliable. Short T-bills are.
- Strategy 1/1b already changed this week (rotation adopted 2026-10-01), so this starts 2026-10-05.

| When out, hold | 2003-2014 CAGR | max DD | Sharpe | 2015-2026 CAGR | max DD | Sharpe |
|---|---|---|---|---|---|---|
| cash (live) | +9.4% | -24% | 0.71 | +10.6% | -25% | 0.73 |
| SHY when out | +9.9% | -21% | 0.74 | +10.7% | -25% | 0.74 |
| IEF when out | +10.8% | -21% | 0.77 | +10.9% | -30% | 0.73 |
| TLT when out | +11.3% | -26% | 0.74 | +9.9% | -42% | 0.62 |
| GLD when out | +9.1% | -33% | 0.56 | +14.2% | -34% | 0.85 |
| best of SHY/IEF/GLD (126d>0) when out | +8.5% | -29% | 0.57 | +12.1% | -28% | 0.77 |
