# Research backlog (daily research picks the top untested item)

Status: todo / testing / adopted / rejected (see research_log.md for results)

| # | Idea | Why it might help | Status |
|---|---|---|---|
| 0b | Options (Setup A in reports/Buying calls and puts small account.md; also B–D there queued after): SPY $1-wide call debit spread (~30 DTE) on the SPY dip-buy signal instead of shares; test on REAL SPY call prices | leverages a tested edge with defined max loss (~$40–60) | REJECTED 2026-09-29: 74 trades, after costs −7.6%/trade (t −2.1); positive only at mid prices (+4.6%, t 1.2). See reports/options_setup_a_backtest.md. Next: Setup B (pre-earnings straddle) |
| 0a | Stocks-in-play day trading (Zarattini, Barbon & Aziz 2024): each morning pick stocks with the highest relative volume (incl. lower-priced names gaining attention via Robinhood scans), trade the 5-minute opening-range breakout, stop at the range, exit by close. Test on Robinhood 5-min bars (Feb 2026+) for a broad universe, with spread costs | published evidence for a daily intraday edge on 'stocks in play' | todo |
| 1 | Cash yield: hold idle cash in SGOV (T-bill ETF) instead of cash | ~4% on idle cash, near-zero risk | todo |
| 2 | QQQ vs SPY: 3–6-month momentum picks which one the core holds | Nasdaq led most of 2010–2026 | todo |
| 3 | SPY dip-buy: add IWM/QQQ as extra dip candidates | more dip trades per year | todo |
| 4 | ETH trend sleeve (ETHA/ETHE) alongside Bitcoin | second crypto trend, diversification | todo |
| 5 | Turn-of-month effect: hold SPY dip sleeve last 1 + first 3 days of month | strong OOS result earlier (+0.4%/trade, t 6.9) | todo |
| 6 | Bitcoin swing: RSI(2) thresholds re-check with more IBIT data | only 37 trades so far | todo |
| 7 | Post-IPO lockup rebound on 100+ IPOs | +3.5% (t 1.8) on 38 IPOs | todo |
| 8 | Volatility-scale SPY core too (target 15%) | smaller crashes | todo |
| 9 | Weekend Bitcoin gap: does Monday IBIT gap predict the week? | IBIT misses weekends | todo |
| 10 | Execution: trade at 3:48 vs close — measure slippage from live fills | real costs vs assumed | todo |
| 11 | Option SELLING, unlocked by account size: ≥$500–1,000 → SPY/QQQ $1-wide put credit spreads (retest on real prices, 30/5-delta rules scaled down); ≥$5,000 → covered calls on IBIT/ETFs; ≥$47,000 → full SPY 30/5-delta put spread (86% win, +3.4%/trade on real prices). Monthly review checks account size and runs the adoption test when a threshold is crossed | harvests the volatility risk premium (Cboe BXM/PUT: equity-like returns, lower volatility) | NEXT (user depositing $500 on 2026-09-29 → ~$750): run the ≥$500 test first — SPY $1-wide put credit spread on real option prices, max loss per spread ≤ 20% of account |
