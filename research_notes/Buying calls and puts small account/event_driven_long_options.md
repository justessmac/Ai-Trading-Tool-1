# Event-Driven Long Options: Empirical Evidence for Buying Calls, Puts, Straddles and Strangles Around Events

Research note compiled late September 2026. Method caveat: most primary PDFs (SSRN, NBER, Rice, MDPI, BSIC, AlphaArchitect, CXO, Quantpedia) were blocked by the network proxy, so several numbers below come from search-result abstracts and summaries rather than full-text reads. Where a number could only be seen in a summary, that is noted. Baseline fact to keep in mind: straddles on individual stocks lose money on average outside events (about -0.19% per day and -2.09% per week holding-period return, per the Gao/Xing/Zhang summary), because of the variance risk premium.

## 1. Earnings: pre-earnings long straddles/strangles (IV run-up) vs. holding through the announcement (IV crush)

### Takeaway
The best academic evidence (Gao/Xing/Zhang, JFQA 2018; Chung and Louis, JEF 2017) finds positive average ATM straddle returns when you buy a few days before earnings, but the edge is concentrated in small, illiquid, high-volatility names where spreads are widest, and transaction costs "drastically" reduce it. Buying a straddle the day before and holding through the announcement loses on average for liquid large caps according to practitioner backtests (Option Alpha: AAPL won 41% of the time with an average of -1.31%). Options on average price earnings moves about right or slightly rich. The only claim of large profits after costs comes from a weak student SSRN paper that ignored costs.

### Cited Findings
**Gao, Xing and Zhang, "Anticipating Uncertainty: Straddles around Earnings Announcements," JFQA 53(6), Dec 2018, pp. 2587-2617**
- Average ATM straddles held from 3 days before an earnings announcement (EA) to the announcement date earn a highly significant +3.34% return. In the same data, straddles on individual stocks in general earn significantly negative returns — [IDEAS/RePEc abstract](https://ideas.repec.org/a/cup/jfinqa/v53y2018i06p2587-2617_00.html); [Semantic Scholar](https://www.semanticscholar.org/paper/Anticipating-Uncertainty:-Straddles-around-Earnings-Gao-Xing/22fbdc3dd06be4045903ec8ca38386c1b2b7876b)
- Sample period: January 1996 to December 2010. A second window, from 1 day before the EA to the EA date, yields about +2.3%. Non-event straddle returns are -0.19% per day and -2.09% per week — (search-result summaries of [CXO Advisory](https://www.cxoadvisory.com/volatility-effects/option-straddles-around-earnings-announcements/) and the [working paper](https://www.ruf.rice.edu/~yxing/straddle_201305_03.pdf); full text blocked, so not verified line by line)
- The positive returns are larger for smaller firms and for firms with higher volatility, higher kurtosis, more volatile past earnings surprises, and lower trading volume / higher transaction costs. Straddle returns are significantly higher when the historical EA move is large relative to the option-implied EA move — [ResearchGate](https://www.researchgate.net/publication/327632662_Anticipating_Uncertainty_Straddles_around_Earnings_Announcements); [working paper](https://www.ruf.rice.edu/~yxing/straddle_201305_03.pdf)
- Transaction costs "drastically decrease the straddles performance." A Quantpedia-style summary reports that delta-neutral straddles with 4–10 days to expiration, paying half the bid-ask spread, net about 1.64% on average over the 3-day window (the summary called this a "daily" return, which is ambiguous; 1996–2010) — (search-result summary of [Quantpedia PDF](https://quantpedia.com/www/Anticipating_Uncertainty-Straddles_Around_Earnings_Announcements.pdf) / [PapersWithBacktest](https://paperswithbacktest.com/strategies/anticipating-uncertainty-straddles-around-earnings-announcements); not verified in full text)
- The authors argue that negatively priced volatility and jump risk factors cannot explain the returns, so the market underestimates EA uncertainty — [working paper](https://www.ruf.rice.edu/~yxing/straddle_201305_03.pdf)

**Chung and Louis, "Earnings Announcements and Option Returns," Journal of Empirical Finance, 2017**
- A BEFORE_EA straddle portfolio (straddles bought before earnings) earns an average of +5.1% over a one-month holding period. An AFTER_EA portfolio earns a negative return. Going long BEFORE_EA and short AFTER_EA earns 14.4% per month — [search summary of SSRN 2886040](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2886040); [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0927539816300743)
- Their explanation: option traders underestimate future volatility before EAs, especially after a period of low volatility, and overestimate it after EAs, especially after a period of high volatility. Buying before is best when pre-formation volatility is low — [ResearchGate](https://www.researchgate.net/publication/305385282_Earnings_announcements_and_option_returns)
- Implication: implied volatility after earnings is too high, so buying options immediately after earnings (for example to trade drift) starts with a structural headwind.

**Later / practitioner evidence (with vendor-bias flags)**
- Khan and Khan (SSRN 4832160, May 2024, NYU/UIC students, not peer reviewed), a 17-year S&P 500 backtest:
  - ATM straddles bought 30 trading days before earnings lose value up to the day before the EA, because theta outweighs the IV run-up.
  - Buying 1 day before and selling 1 day after reports a 108% CAGR and a Sharpe of 2.2 over 13,120 trades, with single-week losses up to 83.8%.
  - Commissions, slippage and taxes were explicitly not accounted for — [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4832160)
  - Treat as low reliability: the headline numbers are compounded, mid-price based and conflict with the other evidence below.
- Option Alpha, a vendor that promotes premium selling:
  - AAPL ATM straddle bought the day before earnings and sold the day after, 2007 onward: won 41.38% of the time, average return -1.31%. The straddle averaged about $15 before and $7.95 after.
  - FB (now META): won 27% of the time.
  - Short straddles won ≥60% of the time — [Option Alpha](https://optionalpha.com/podcast/long-straddle-earnings-option-strategy)
  - Covers only single stocks, so the sample is small.
- tastytrade, also a premium-selling vendor:
  - Bought straddles 2 weeks before earnings and closed just before the report, and concluded that buying premium before earnings does not work ("nail in the coffin").
  - SteadyOptions, which sells pre-earnings straddle trades as a service, says the design (14 days out, near-expiry options with high theta) guaranteed losses about 90% of the time and that 5–7 days is the better entry — [SteadyOptions](https://steadyoptions.com/articles/buying-premium-prior-to-earnings-does-it-work-r89/)
  - Both sides have commercial bias.
- SteadyOptions (subscription service; self-reported, not audited). Its pre-earnings straddles and calendars are closed before the announcement, bundled with other strategies:
  - 2017: 113/138 winners, +169.1% (10% allocation per trade)
  - 2022: 147/215 (68.4%), +90.5%
  - 2024: 136/187 (72.7%), +116.7%
  - 2025: 83/136 (61.0%), only +6.5% compounded
  - Pre-earnings calendars in 2017: +13.8% average, 84% winners
  - Sources: [2017](https://steadyoptions.com/articles/steadyoptions-2017-year-in-review-r306/); [2022](https://steadyoptions.com/articles/steadyoptions-2022-year-in-review-r728/); [2024](https://steadyoptions.com/articles/steadyoptions-2024-year-in-review-r813/); [2025](https://steadyoptions.com/articles/steadyoptions-2025-year-in-review-r822/)
- Lipkin, Tatevossian and K M (SSRN 4701633, Jan 2024; Journal of Risk): options "in most cases do a good job of predicting" the size of earnings moves, but with significant outliers. Earnings moves are fat-tailed and symmetric up/down — [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4701633); [Risk.net](https://www.risk.net/journal-of-risk/7960706/earnings-moves-and-pre-earnings-implied-volatility)
- Practitioner claims:
  - Stocks stay inside the option-implied earnings move about 70–75% of the time, versus 68% for a 1-SD normal — (search summary of [Maverick Trading](https://www.mavericktrading.com/free-trading-videos/articles/implied-vs-actual-earnings-moves-is-the-market-overpricing-volatility); vendor, method unknown)
  - A search summary said the implied move overestimates the actual move by about 10–15%. I could not trace this to a primary source, so it is unverified.
- A 2023 study of weekly options (JRFM 16(5):270) finds weekly straddle prices around EAs "not optimally efficient" — [MDPI](https://www.mdpi.com/1911-8074/16/5/270) (full text blocked; direction and size of the mispricing not verified)

### Inferences
- The documented edge is a pre-announcement IV run-up that is too small: implied volatility underestimates the coming event. It is:
  - largest in small, volatile, illiquid names, exactly where retail bid-ask spreads are widest (often 5–15%+ of the straddle price)
  - statistically real in 1996–2010 data before costs, and much smaller after paying half the spread
  - a gross average of about +3% per 3-day trade, easily eaten by a round-trip spread in thin names
- For a Robinhood account (no commissions, but you pay the spread and fills can be poor), the realistic version is:
  - Trade liquid, penny-increment names.
  - Buy about 3–7 trading days before the EA, using an expiry just after the EA so the event variance is in the price.
  - Prefer stocks whose historical EA moves exceed the implied move.
  - Exit before the announcement (the Chung/Louis and GXZ windows end at or before the reaction), or accept a coin-flip-or-worse through-event bet.
  - Expect small average edges and many small losers, with no strong post-2010 peer-reviewed confirmation.
- Holding through the event in large caps has negative or near-zero expectancy in the vendor backtests. That is consistent with Chung/Louis showing IV overshooting after EAs.
- Ambiguity to flag: GXZ's window ends "at the announcement date." For before-open reporters, the day-0 close already includes the reaction. So the +3.34% may partly include the announcement move itself rather than only the IV run-up.

### Gaps
- No peer-reviewed study found that uses post-2015 data (the era of weekly options and 0DTE, when retail option buying around earnings grew heavily) to test whether the GXZ/Chung-Louis pre-EA premium survives net of full bid-ask spreads.
- Win rates and return distributions for the GXZ strategy were not retrievable, because the full text was blocked.
- No independent audited track record exists for pre-earnings straddle services.

## 2. Post-earnings announcement drift (PEAD) via options

### Takeaway
There is no good evidence that buying directional options to ride PEAD is profitable today. Classic PEAD returns have decayed toward zero in recent years, option traders already price earnings surprises, and post-EA implied volatility is too high (Chung/Louis), which penalizes option buyers.

### Cited Findings
- Typical PEAD strategy returns have gradually decreased to about 0 in recent years — (search summary of [Caltech/Katz "Anomalous Anomaly"](https://jkatz.caltech.edu/documents/28622/peads.pdf) and [review in ScienceDirect](https://www.sciencedirect.com/science/article/pii/S2214635020303750))
- PEAD strategies are less profitable once trading frictions are included — [ScienceDirect 2024](https://www.sciencedirect.com/science/article/pii/S0148619524000584)
- Firms with listed options attract arbitrageurs who overcorrect: in optioned firms, the highest-surprise decile can underperform the lowest — [Quantpedia, reversal in PEAD](https://quantpedia.com/strategies/reversal-in-post-earnings-announcement-drift)
- Straddles on extreme earnings surprises are not more profitable than those on mild surprises, which suggests option traders already price prior surprises — ["The Post Earnings Announcement Drift and Option Traders"](https://www.researchgate.net/publication/256034131_The_Post_Earnings_Announcement_Drift_and_Option_Traders)
- A Penn State honors thesis (student work) found that 62.5% of individual straddles and 70.8% of strangles were profitable at their peak (mean peak returns of 27.1% and 29.9%). Neither was profitable as a portfolio over a 90-day hold. The peak-return figures are look-ahead and not tradeable — [PSU](https://honors.libraries.psu.edu/catalog/21244)
- After EAs, IV tends to be overestimated, so straddles bought after the announcement earn negative returns (Chung and Louis) — [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0927539816300743)

### Inferences
- A PEAD trade with long calls or puts relies on stock drift that has largely disappeared in optioned, liquid names, while paying IV that is still elevated after the event. The expected value is likely negative after spreads.

### Gaps
- No peer-reviewed paper found that tests a directional long-call/long-put PEAD strategy, net of costs, on recent (post-2015) data.

## 3. Biotech / FDA catalysts (PDUFA, advisory committees, trial readouts)

### Takeaway
The only rigorous evidence concerns informed trading. Unusual call buying and implied-volatility spreads before FDA events predict the direction of the stock's move, and a call strategy earns about 15%. That profit reflects information leakage or asymmetry, not a mispriced straddle. I found no peer-reviewed evidence that blind long straddles into PDUFA dates or trial readouts are profitable. Practitioners widely say IV on binary biotech events is priced very high.

### Cited Findings
- Bohmann and Patel, "Informed options trading prior to FDA announcements," Journal of Business Finance & Accounting 49(7-8), 2022, pp. 1211-1236:
  - Implied-volatility spreads, call volume and call order imbalance rise significantly in the 5 days before FDA announcements, and they predict announcement-day stock returns.
  - Average abnormal announcement-day return is about 1%.
  - Buying calls 5 days before and closing the day after the news earns about 15%.
  - Effects are stronger where information asymmetry is high and governance is weak — [Wiley](https://onlinelibrary.wiley.com/doi/10.1111/jbfa.12600); [IDEAS](https://ideas.repec.org/a/bla/jbfnac/v49y2022i7-8p1211-1236.html); [UTS OPUS](https://opus.lib.uts.edu.au/handle/10453/160828)
  - The summary does not make clear whether the ~15% is unconditional or depends on the IV-spread signal. Transaction costs are not stated in the snippets.
- FDA advisory-committee study (Journal of Empirical Finance / Journal of Corporate Finance, 2023):
  - About 32% of advisory meetings show significant abnormal option volume before the meeting, mostly short-dated OTM options.
  - Informed traders tend to sell before the meeting to also capture the IV crush — [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S092911992300144X); [ResearchGate](https://www.researchgate.net/publication/375718777_Informed_options_trading_before_FDA_drug_advisory_meetings)
- Vendor tools (Market Chameleon biotech catalyst report) compare the straddle implied move with historical moves. This is marketing and tooling, not performance evidence — [Market Chameleon](https://marketchameleon.com/reports/biotech-stock-catalysts)

### Inferences
- The FDA call-option result reads as "follow the unusual flow," not "options are cheap." Retail traders cannot see order imbalance in real time the way the study measured it, and much of the profit may come from illegal leakage.
- Biotech binary events are often priced with huge implied moves. Without evidence that realized moves exceed implied ones, long straddles are a pure gamble with a probable negative expected value after wide spreads in small-cap biotech options.

### Gaps
- No systematic study found of realized vs. implied moves for PDUFA dates or trial readouts (straddle P&L across many events).
- Sample sizes and periods for Bohmann and Patel were not visible in accessible snippets.

## 4. Other events: IPO lockup expirations, index inclusion, stock splits, macro (FOMC, CPI, NFP)

### Takeaway
- Lockups: stock-level evidence of negative returns is solid, but I found no study testing put buying net of costs.
- Index inclusion and splits: evidence concerns option-implied information (skew, informed trading), not profitable option buying.
- FOMC and macro: the variance risk premium is large and positive on event days, so buying index straddles into FOMC is, on the balance of evidence, negative expected value. One study reports +2.6%, but the peer-reviewed work shows the opposite.

### Cited Findings
**IPO lockups**
- IPOs show significant negative abnormal returns around lockup expiration (1988–2012). The highest idiosyncratic-volatility quintile falls 2–12% more than the lowest. Effects are larger among stocks with newly listed options (1996–2012) — [ScienceDirect (JEF 2014)](https://www.sciencedirect.com/science/article/abs/pii/S0927539814000589)
- Negative lockup returns are larger for firms with higher implied-volatility uncertainty — [Sunder et al. working paper](https://d30i16bbj53pdg.cloudfront.net/sites/default/files/documents/school-of-accounting/sunder_paper.pdf)

**Index inclusion**
- IV skew of S&P 500 additions (1996–2019) steepens by 0.92 points (3.66% to 4.58%) over the 5 months after inclusion, meaning option traders expect a reversal of the price pressure — [EFMA 2022 paper](http://www.efmaefm.org/0EFMAMEETINGS/EFMA%20ANNUAL%20MEETINGS/2022-Rome/papers/EFMA%202022_stage-3032_question-Full%20Paper_id-329.pdf)

**Stock splits**
- Split-announcement abnormal returns are significantly smaller for optioned stocks, so options markets already embed the information — [ScienceDirect (JBF 2008)](https://www.sciencedirect.com/science/article/abs/pii/S0378426607002804)
- Informed option trading precedes split announcements (Gharghori, Maberly and Nguyen, JFQA 52(2), 2017) — [JSTOR](https://www.jstor.org/stable/26164614)

**FOMC and macro**
- Wright, "Event-Day Options" (NBER w28306; Journal of Time Series Analysis 2025):
  - Uses Wednesday/Friday-expiring Treasury and equity futures options.
  - Variance risk premia are "large and significantly positive, especially for FOMC days" (also for employment-report days).
  - Option buyers overpay for event variance on average — [NBER](https://www.nber.org/papers/w28306); [Wiley](https://onlinelibrary.wiley.com/doi/10.1111/jtsa.12819)
- Recovering the FOMC risk premium (JFE 2022, S&P 500 options expiring just after meetings): the premium ranges from 1 to 326 bp and averages 45 bp over 1996–2019 — [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0304405X22000927)
- Conflicting evidence:
  - DeSimone (2017) reports significant +2.6% returns for straddles held over Fed meetings.
  - A Lund thesis finds negative straddle returns across all windows for all macro announcements, with no evidence that buying ahead is profitable — [Lund thesis](https://lup.lub.lu.se/student-papers/record/9197108/file/9197117.pdf)
- Nasdaq-100 1-day straddles: over the most recent 12 FOMC meetings in that article, the average move was ±0.75%, and ATM straddles were overpriced in 10 of 12 — [Nasdaq](https://www.nasdaq.com/articles/fomc-volatility-premium-evidence-1-day-nasdaq-100-straddles) (article date not visible; small sample)

### Inferences
- A lockup put buy is plausible in theory (a predictable negative drift). However, the date is public, borrow and put IV likely price it in, and no net-of-cost option study exists. Treat it as unproven.
- Index-inclusion and split "plays" with options are marketing or anecdote. The academic work shows options already anticipate these events.
- Macro events are the clearest case against buying: straddle sellers collect a documented event-day premium.

### Gaps
- No option-return study found for lockup puts, split-announcement calls or index-inclusion trades.
- No CPI-specific straddle-return study found. Wright covers FOMC and NFP.
- DeSimone (2017) sample details could not be verified.

## 5. Well documented vs. anecdotal: overall evidence scorecard

### Takeaway
Only one long-option event setup has peer-reviewed support for positive average returns: buying straddles a few days before earnings and exiting at or around the announcement. It is gross of most costs, uses 1996–2010 data, and is concentrated in hard-to-trade names. Everything else either has negative documented expected value for buyers (FOMC and macro, post-earnings, holding through earnings in large caps), relies on informed flow (FDA calls), or has no option-return evidence (lockups, splits, index inclusion, PDUFA straddles).

### Cited Findings
- **Well documented, positive gross:**
  - Pre-EA straddles, GXZ 2018: +3.34% over 3 days, 1996–2010 — [IDEAS](https://ideas.repec.org/a/cup/jfinqa/v53y2018i06p2587-2617_00.html)
  - Pre-EA straddles, Chung and Louis 2017: +5.1% per month — [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0927539816300743)
- **Documented, conditional on informed-flow signals:** FDA calls, about +15% — [Wiley](https://onlinelibrary.wiley.com/doi/10.1111/jbfa.12600)
- **Documented negative for buyers:**
  - Straddles bought after earnings (Chung and Louis) — [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0927539816300743)
  - FOMC and NFP event-day variance premium (Wright) — [NBER](https://www.nber.org/papers/w28306)
  - Generic stock straddles: -2.09% per week — [working paper](https://www.ruf.rice.edu/~yxing/straddle_201305_03.pdf)
- **Vendor or low-quality, mixed:**
  - Option Alpha AAPL/FB through-earnings losses — [Option Alpha](https://optionalpha.com/podcast/long-straddle-earnings-option-strategy)
  - Khan and Khan's 108% CAGR with no costs — [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4832160)
  - SteadyOptions self-reported results — [SteadyOptions](https://steadyoptions.com/articles/steadyoptions-2025-year-in-review-r822/)
  - The tastytrade "nail in coffin" study — [SteadyOptions critique](https://steadyoptions.com/articles/buying-premium-prior-to-earnings-does-it-work-r89/)

### Inferences
- For a small Robinhood account, the defensible approach is:
  - Small, liquid pre-earnings straddles or strangles bought about 3–7 days before and closed before the release, sized to survive long losing streaks.
  - Filtered for names whose historical EA moves exceed the current implied move, and for low recent realized volatility (the Chung/Louis condition).
  - Tracked against realized fills, because the academic edge (about 3% per trade) is the same size as a typical round-trip spread cost.
- Holding long premium through earnings, FOMC or CPI, or into post-earnings drift, should be treated as negative expected value unless the trader has a specific, testable edge.
- The SteadyOptions 2025 result (+6.5% vs. triple digits in earlier years) hints that the pre-earnings edge may be compressing. That is one self-reported data point.

### Gaps
- No post-2018 peer-reviewed replication of the pre-EA straddle premium net of realistic retail fills.
- No evidence found on how the 2022+ explosion in short-dated and 0DTE retail option buying changed event IV pricing.
