# Overnight vs intraday returns

**Verdict (2026-10-01): rejected (can't be run under the playbook), but noted.**
- The pattern is real in this data: nearly all of the market's gain came overnight. Intraday-only lost money on QQQ (2001-2014) and IWM (both periods). IWM overnight-only made +11.3%/yr in 2015-2026 after a 1-cent spread, vs +7.5% buy & hold.
- Why not: it needs a buy at the close and a sell at the open every day, ~250 round trips a year (playbook limit ~12). Drawdowns were -29% to -35% (limit -25%). At 0.01%/side it mostly disappears. The bot only acts once a day at 15:48 and can't reliably sell at the open.
- Caution: some published work finds the small-cap overnight gap partly reflects stale opening prints, so real fills would be worse.
- Useful takeaway for live rules: decide and trade near the close (as we do). Market moves happen mostly while we hold overnight, which is fine for multi-day positions.

| Fund | Leg | Cost/side | 2001-2014 CAGR | max DD | 2015-2026 CAGR | max DD |
|---|---|---|---|---|---|---|
| SPY | buy & hold | 0.000% | +3.3% | -56% | +11.8% | -34% |
| SPY | intraday (open->close) | 0.000% | +0.7% | -48% | +4.6% | -25% |
| SPY | overnight (close->open) | 0.000% | +2.6% | -34% | +6.9% | -29% |
| SPY | overnight | 0.002% | +1.6% | -35% | +5.8% | -29% |
| SPY | overnight | 0.010% | -2.4% | -45% | +1.6% | -30% |
| QQQ | buy & hold | 0.000% | +4.2% | -70% | +18.2% | -36% |
| QQQ | intraday (open->close) | 0.000% | -3.9% | -77% | +6.2% | -25% |
| QQQ | overnight (close->open) | 0.000% | +8.4% | -28% | +11.3% | -28% |
| QQQ | overnight | 0.002% | +7.4% | -29% | +10.2% | -29% |
| QQQ | overnight | 0.010% | +3.1% | -34% | +5.9% | -32% |
| IWM | buy & hold | 0.000% | +6.8% | -59% | +7.5% | -42% |
| IWM | intraday (open->close) | 0.000% | -1.0% | -55% | -4.4% | -61% |
| IWM | overnight (close->open) | 0.000% | +7.9% | -30% | +12.4% | -29% |
| IWM | overnight | 0.002% | +6.8% | -30% | +11.3% | -29% |
| IWM | overnight | 0.010% | +2.6% | -32% | +6.9% | -30% |
