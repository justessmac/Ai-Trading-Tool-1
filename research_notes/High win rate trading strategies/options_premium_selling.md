# Options Premium-Selling Strategies with >=85% Win Rates (Robinhood Level 3 compatible)

> Research method note: WebFetch to nearly all primary domains (cdn.cboe.com, spintwig.com, projectfinance.com, optionalpha.com, aqr.com, cxoadvisory.com, steadyoptions.com, quantifiedstrategies.com, mdpi.com, wikipedia.org) was blocked by the network egress proxy during this session. All figures below come from search-engine result excerpts of the cited pages, not from full-text reads. Numbers are reported as surfaced; the report writer should treat any figure marked "(snippet)" as needing verification against the primary PDF before it is used for sizing or backtest calibration. Where a number could not be surfaced it is listed under Gaps rather than filled in from memory.

---

## 1. Cash-secured puts / put-write (CBOE PUT, WPUT, PUTY)

### Takeaway
Systematic cash-secured put writing on the S&P 500 is the best-documented premium-selling strategy: over 1986-2018 the ATM monthly PUT index roughly matched S&P 500 returns with ~2/3 of the volatility and a much smaller max drawdown (-32.7% vs -50.9% over 2006-2018), but it still lost -26.8% in 2008, and independent work finds the edge has shrunk or vanished since ~2010-2012. Note the index writes ATM puts (win rate far below 85%); >=85% win rates require OTM strikes (~16-delta or lower), which trade premium for lower win-size.

### Cited Findings
**Methodology**
- PUT (Cboe S&P 500 PutWrite, launched 2007) and WPUT (One-Week PutWrite, launched 2015) track gross performance of selling at-the-money SPX puts fully collateralized by US Treasury bills; PUT rolls monthly, WPUT weekly. — [Bondarenko 2019, SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3393940); [Cboe PutWrite Indices Methodology](https://cdn.cboe.com/api/global/us_indices/governance/Cboe_PutWrite_Indices_Methodology.pdf)
- PUTY (Cboe S&P 500 2% OTM PutWrite) writes a 2% out-of-the-money SPX put monthly and holds one-month T-bills to cover the liability. — [Cboe PutWrite Indices Methodology (via search excerpt)](https://cdn.cboe.com/api/global/us_indices/governance/Cboe_PutWrite_Indices_Methodology.pdf)
- Cboe benchmark option indexes (BXM family) price the newly written option using the VWAP between 11:30 a.m. and 1:30 p.m. ET on roll day (third Friday) — the same convention is used for PUT per the Cboe methodology family. — [Cboe BuyWrite Methodology / search excerpt](https://cdn.cboe.com/api/global/us_indices/governance/Cboe_BuyWrite_Indices_Methodology.pdf) (PUT applying the same VWAP convention is my reading of the shared methodology family; verify.)

**Long-run performance**
- Over 32+ years (June 1986 - Dec 2018), PUT had an annual compound return comparable to the S&P 500 with substantially lower standard deviation; annualized Sharpe 0.65 (PUT) vs 0.49 (S&P 500). — [Wilshire Analytics for Cboe, 2019 (snippet)](https://cdn.cboe.com/resources/spx/wilshire-options-based-benchmark-indexes-2019.pdf); [Cboe press/MarketScreener](https://www.marketscreener.com/quote/stock/CBOE-GLOBAL-MARKETS-6306029/news/CBOE-New-Wilshire-Analytics-Study-Finds-Options-Indexes-Offered-Noteworthy-Returns-Over-30-Years-23092094/)
- PUT, BXM and CMBO (all ATM writers) were the least volatile of the equity-based indexes studied, "and even with their relatively low volatilities... delivered strong returns" over the 32-year period. — [Wilshire 2019 (snippet)](https://cdn.cboe.com/resources/spx/wilshire-options-based-benchmark-indexes-2019.pdf)
- 2006-2018 (13 years): std. dev. 10.69% (PUT), 9.48% (WPUT), 14.32% (S&P 500). Max drawdown -32.7% (PUT), -24.2% (WPUT), -50.9% (S&P 500). — [Bondarenko 2019, Cboe-commissioned (snippet)](https://cdn.cboe.com/resources/education/research_publications/PutWriteCBOE19_v14_by_Prof_Oleg_Bondarenko_as_of_June_14.pdf)
- Average annual gross premium collected 2006-2018: 22.1% (PUT, monthly) vs 37.1% (WPUT, weekly). — [Bondarenko 2019 (snippet)](https://cdn.cboe.com/resources/education/research_publications/PutWriteCBOE19_v14_by_Prof_Oleg_Bondarenko_as_of_June_14.pdf)
- Longest drawdown-and-recovery: 30 months (PUT) vs 66 months (S&P 500). — [Bondarenko 2019 via search summary](https://papers.ssrn.com/sol3/Delivery.cfm/SSRN_ID3393940_code246693.pdf?abstractid=3393940&mirid=1)
- 2008 calendar-year returns: PUT -26.8%, BXM -28.7%, S&P 500 -37.0%. — [Wilshire 2019 (snippet)](https://cdn.cboe.com/resources/spx/wilshire-options-based-benchmark-indexes-2019.pdf)

**Source-independence flag**
- The Wilshire and Bondarenko studies were commissioned/published by Cboe, which earns fees from SPX options volume and licenses these indexes; they are academic-quality but not disinterested. — [Cboe IR release on Bondarenko study](https://ir.cboe.com/news/news-details/2016/New-Study-On-Weekly-Monthly-SP-500-PutWrite-Indexes-Released-01-27-2016/default.aspx)
- Independent re-examination (Kumiega, Sterijevski & Wills, Int. J. Financial Studies, Nov 2024) using actual options data 2012-2023 found that none of the simple passive option strategies (incl. BXM/PUT-type) outperformed the S&P 500; only a protective-put (PPUT) variant beat buy-and-hold on a risk-adjusted basis, and VIX worked as a regime filter. — [MDPI / Semantic Scholar summary](https://www.mdpi.com/2227-7072/12/4/114)

**Win rates for OTM cash-secured puts (delta / DTE variants)**
- Claim that SPY 45-DTE 16-delta puts expired OTM ~95% of the time (2005-2020) and 30-delta puts finished ITM ~11% (≈89% win), attributed to tastytrade backtests. — [ThetaLoop delta cheat sheet (vendor/app marketing, secondary)](https://thetaloop.app/learn/delta-guide). VENDOR SOURCE; primary tastylive segment not located.
- projectfinance, 16-delta SPY short puts, 30-60 DTE, 41,600 trades, Jan 2007 - May 2017: holding to expiration produced the highest average P/L per trade; taking profits at 25% of max produced a 98% success rate but required a 95.8% success rate just to break even because wins are so small relative to losses. — [projectfinance Short Put Management study (snippet)](https://www.projectfinance.com/short-put-management/) (educational site run by an options educator; independent of brokers but not peer reviewed)
- Spintwig SPY 45-DTE cash-secured short puts: 75% take-profit and hold-to-expiry both showed high win rates; hold-to-expiry had roughly the best Sharpe, with 50% and 75% take-profit close behind. — [Spintwig via 7 Circles summary](https://the7circles.uk/options-11-spintwig-efficiency/) (Spintwig is an independent hobbyist/analyst backtester using historical chains with commissions and fills modeled)

### Inferences
- A >=85% win-rate CSP rule set that is well supported in the literature: SPY/SPX, sell ~16-30 delta put, 30-60 DTE, hold to expiration or take profit at 50-75%. Expect win rate ~85-95% but average loss several times the average win; the breakeven win rate is the binding test, not the raw win rate.
- The ATM PUT index's advantage came mainly from lower volatility, not higher return; after costs and in post-2012 data the return edge over SPX appears small to zero.

### Gaps
- Could not read the Bondarenko/Wilshire PDFs; exact annualized returns (PUT vs SPX 1986-2018), % of positive months, and skewness numbers not captured.
- PUTY long-run return/drawdown not surfaced.
- No primary tastylive study document located; the 95%/89% OTM-expiry figures come from a secondary app vendor page.
- PUT/WPUT drawdowns for Feb 2018, Mar 2020, Aug 2024 not found in any accessible source.

---

## 2. Covered calls / buy-write (BXM, BXMD, BXY)

### Takeaway
BXM (long SPX + sell 1-month ATM call) delivered S&P-like returns at lower volatility over 1986-2018, but it is equity beta plus a small volatility premium; AQR shows most risk/return is plain equity exposure and the VRP component is ~10% of risk. 30-delta BXMD keeps more upside. Win rate is not a meaningful metric for buy-writes because losses come from the stock leg.

### Cited Findings
- BXM: hypothetical portfolio long SPX, selling a succession of one-month ATM SPX calls on the 3rd Friday; call premium set at the 11:30-13:30 ET VWAP. — [Cboe BuyWrite Methodology (snippet)](https://cdn.cboe.com/api/global/us_indices/governance/Cboe_BuyWrite_Indices_Methodology.pdf); [Wharton course notes](http://www-stat.wharton.upenn.edu/~steele/Courses/956/BuyWrite/BuyWrite.html)
- BXMD: long SPX and writes a monthly OTM SPX call with delta closest to 0.30. — [Cboe BuyWrite Methodology (snippet)](https://cdn.cboe.com/api/global/us_indices/governance/Cboe_BuyWrite_Indices_Methodology.pdf)
- Feldman & Roy (Ibbotson, 2004/2005) found BXM returns comparable to the S&P 500 with higher risk-adjusted return, 1988-2004 (Cboe-commissioned). — [ResearchGate: Passive options-based strategies - BXM](https://www.researchgate.net/publication/247907242_Passive_options-based_investment_strategies_The_case_of_the_CBOE_SP_500_BuyWrite_Index)
- BXM returned -28.7% in 2008 vs -37.0% for S&P 500. — [Wilshire 2019 (snippet)](https://cdn.cboe.com/resources/spx/wilshire-options-based-benchmark-indexes-2019.pdf)
- Israelov & Nielsen, "Covered Calls Uncovered" (FAJ 2015): covered calls = equity risk premium + volatility risk premium + an uncompensated naive equity-reversal exposure. Equity exposure contributed most risk and return; the short-vol component realized Sharpe near 1.0 but only ~10% of risk; the equity-reversal exposure contributed ~25% of risk with little return. A delta-managed covered call improves Sharpe. — [SSRN](https://papers.ssrn.com/sol3/Papers.cfm?abstract_id=2444999); [QuantPedia summary](https://quantpedia.com/covered-calls-uncovered/) (AQR sells alternative/vol products — mild interest, but peer reviewed)
- Kumiega et al. (2024): with real 2012-2023 options data, simple buy-write strategies did not beat SPX. — [MDPI](https://www.mdpi.com/2227-7072/12/4/114)

### Inferences
- Covered calls are a poor fit for a ">=85% win-rate" objective: return is dominated by the stock leg, and in strong bull markets (most of 2010-2024) ATM call writing caps upside and lags.
- BXY (2% OTM buy-write) data could not be retrieved; directionally, further-OTM writes should track SPX more closely with less premium.

### Gaps
- No BXY/BXMD long-run return or drawdown figures surfaced.

---

## 3. Bull put spreads and iron condors (SPX/SPY/QQQ/IWM, CNDR)

### Takeaway
Defined-risk spreads at 16-30 delta short strike produce raw win rates in the 68-90% range, but independent backtests show the call side of index iron condors has had negative expected value, the CNDR index has been roughly flat since 2010, and results swing from large gains to total loss depending on the stop-loss rule. Put-only credit spreads on SPX are the best-supported variant.

### Cited Findings
**CNDR**
- CNDR sells a monthly ~0.20-delta SPX put and ~0.20-delta SPX call and buys ~0.05-delta wings; no adjustments, held to expiration, mechanical monthly roll. — [Cboe CNDR Methodology](https://cdn.cboe.com/api/global/us_indices/governance/CNDR_Methodology.pdf); [Cboe insights: BFLY and CNDR](https://www.cboe.com/insights/posts/benchmark-indices-series-volatility-management-with-cboes-bfly-and-cndr-indices/)
- CNDR compound growth ~+9.11%/yr Jan 1987 - Jan 2010, then went from ~770 to ~784 between Jan 2010 and 2024 — essentially flat for 14 years. — [Options Jive blog (snippet; secondary, retail educator)](https://optionsjive.com/blog/iron-condor-options-strategy/); consistent with [Ben Kizemchuk post "RIP Captain Condor"](https://x.com/BenKizemchuk/status/2035447405026632099). Verify against [Cboe/Yahoo ^CNDR data](https://finance.yahoo.com/quote/%5ECNDR/).
- CNDR drawdowns are driven by realized volatility exceeding implied. — [Options Jive (snippet)](https://optionsjive.com/blog/iron-condor-options-strategy/)

**Spintwig (independent backtester)**
- Short SPX vertical put 45-DTE study: 18 backtests, >52,400 trades. Opening only on days a filter ("s1 signal") is TRUE and holding to expiration beat opening every day on total return, risk-adjusted return, max drawdown and drawdown duration. — [Spintwig (snippet)](https://spintwig.com/short-spx-vertical-put-45-dte-s1-signal-options-backtest/)
- 45-DTE short SPX puts / put verticals have generally had positive expected value while 45-DTE short SPX calls have had negative expected value; since the call side of an SPX iron condor is systematically unprofitable, selling the put side only is preferred. — [Spintwig iron condor 45-DTE (snippet)](https://spintwig.com/short-spx-iron-condor-45-dte-s1-signal-options-backtest/)

**projectfinance (independent educator)**
- SPY iron condors with 16-delta short strikes: 71,417 trades; ~68% probability of expiring worthless; put side carries more risk because skew makes the put spread wider. — [projectfinance Iron Condor Management (snippet)](https://www.projectfinance.com/iron-condor-management/)
- Short strangles (11-year SPY study): the best management combination was 50% profit target + 100% stop-loss (strangles are naked, not Level-3 eligible, but the management finding transfers directionally). — [projectfinance Short Strangle Management (snippet)](https://www.projectfinance.com/short-strangle-management/)

**OptionAlpha / FlashAlpha / others (vendors)**
- OptionAlpha SPY put credit spread study: short 0.30 delta / long 0.10 delta, tested profit-target, stop and roll combinations; 10% portfolio allocation produced "remarkably better" results than 5%. One configuration had a 52% win rate and lost $8,592.85 (avg -$171.86/trade). — [OptionAlpha blog (snippet; VENDOR — sells automation platform)](https://optionalpha.com/blog/spy-put-credit-spread-backtest)
- FlashAlpha: 96 SPY put-credit-spread parameter cells, 7 years of 1-minute chains, 16,024 trades with market-maker-style fills; the same cell returned +5,400% with a stop-loss and -100% without; raising short delta 10->30->45 raised CAGR and max drawdown about proportionally (Calmar flat); realistic fills were 4-7 cents/contract worse than mid with only ~20-25% of posted orders filled after ~12 minutes. Author withholds the best parameters. — [FlashAlpha (VENDOR — sells data API)](https://flashalpha.com/articles/spy-put-credit-spread-active-backtest-mm-fills-vrp-signal-drawdown-breaker)
- "91% win rate" SPY put credit spread rules claimed by Options Cafe. — [Options Cafe (VENDOR/marketing)](https://options.cafe/blog/spy-put-credit-spreads-strategy/)
- tastytrade house rule set: sell 16-delta call and put at ~45 DTE (prefer IV Rank 50-100), close winners at 50% of credit, exit at 21 DTE, stop if the credit doubles. — [Zerodha "In the Money" backtest of the 45-DTE strategy (secondary)](https://inthemoneybyzerodha.substack.com/p/we-backtested-the-famous-45-dte-strategy); [SJ Options critique](https://www.sjoptions.com/does-tastytrade-work/)
- An 11-year SPX backtest found the 16-delta tastytrade strangle underperformed the market; moving 30->16 delta roughly halved premium and nearly tripled stop-losses hit. — [SJ Options (independent critic, snippet)](https://www.sjoptions.com/does-tastytrade-work/); see also [Sweet Volatility practitioner experience](https://sweetvolatility.com/tasty-trade-experiments/)

### Inferences
- A defensible Level-3 rule set to backtest: SPX (or SPY) bull put spread, 45 DTE, short ~16-20 delta, long 5-10 delta (or fixed width, e.g., 25-50 SPX points), close at 50% of credit or 21 DTE, optional stop at 2x credit; optional regime filter (e.g., VIX term structure/contango or price > 200-day MA, akin to Spintwig's "s1").
- Iron condors add call-side trades that historical data says are negative EV on indices; they raise win-rate optics but likely lower net expectancy.
- Win rate is highly parameter-sensitive; the stop-loss rule dominates outcome at short DTE (FlashAlpha).

### Gaps
- Exact Spintwig tables (win rate, avg win/loss, CAGR, max DD per variant) and projectfinance IC tables could not be read.
- No independent data found for QQQ/IWM credit spreads beyond Spintwig titles (e.g., short IWM put 45-DTE s4, short NDX put s5) — results not surfaced.
- tastylive primary research segments (win rate, P/L per day for 50% management) not located in accessible form.

---

## 4. The Wheel

### Takeaway
The best available independent backtest (Spintwig, SPY, 45 DTE) finds no Wheel variant beat buy-and-hold SPY on total return; >94-99% of Wheel return came from the long-stock leg, and 4 of 10 variants had negative total return.

### Cited Findings
- SPY Wheel 45-DTE: not a single one of 10 configurations outperformed buy-and-hold on total return; four went negative. 5-delta hold-to-expiration was best, with >99% of its return attributable to the long SPY position; 50-delta early-management was worst (>94% of return from long SPY). — [Spintwig SPY Wheel 45-DTE (snippet)](https://spintwig.com/spy-wheel-45-dte-options-backtest/); [7 Circles summary](https://the7circles.uk/options-11-spintwig-efficiency/)

### Inferences
- The Wheel's high "win rate" per option cycle hides that assignment converts losses into long-stock positions; it should be benchmarked against buy-and-hold, not by win rate.

### Gaps
- No independent Wheel study on single stocks with survivorship-bias-free universe found.

---

## 5. Management rules: win rate vs total return

### Takeaway
Early profit-taking raises win rate but shrinks average win, raising the breakeven win rate; hold-to-expiry often maximizes P/L per trade, while 50% profit-taking tends to improve P/L per day and smooth risk. Stops can dominate outcomes.

### Cited Findings
- 16-delta SPY short puts 2007-2017: 25% profit target -> 98% success rate but 95.8% breakeven win rate; hold-to-expiration had the highest average P/L per trade. — [projectfinance (snippet)](https://www.projectfinance.com/short-put-management/)
- Strangles: 50% profit + 100% stop was the best combination in projectfinance's 11-year SPY test. — [projectfinance (snippet)](https://www.projectfinance.com/short-strangle-management/)
- SPY CSPs: hold-to-expiry had roughly the best Sharpe; 50%/75% take-profit close behind. — [7 Circles on Spintwig](https://the7circles.uk/options-11-spintwig-efficiency/)
- Same put-credit-spread cell: +5,400% with stop vs -100% without. — [FlashAlpha (vendor)](https://flashalpha.com/articles/spy-put-credit-spread-active-backtest-mm-fills-vrp-signal-drawdown-breaker)
- tastytrade's platform default "close at % of max profit" is 50%, reflecting its house methodology. — [tastytrade Help Center](https://support.tastytrade.com/support/s/solutions/articles/43000435423)
- SteadyOptions article tests whether "managing winners" adds value to short strangles. — [SteadyOptions](https://steadyoptions.com/articles/does-%E2%80%9Cmanaging-winners%E2%80%9D-add-value-to-short-strangles-r618/) (content not retrievable)

### Inferences
- For the >=85% objective, 50% profit-taking reliably lifts win rate into the 85-95% band for 16-30 delta shorts, but the backtest must report expectancy (avg win x p - avg loss x (1-p)) after costs, and compare to the breakeven win rate.
- Early exits also increase trade count, multiplying per-contract fees and spread costs (see Section 7).

### Gaps
- No primary quantitative source retrieved for "roll at 21 DTE" vs hold, beyond tastytrade rule descriptions.

---

## 6. Tail events and the volatility risk premium

### Takeaway
The VRP is well documented (implied variance on average exceeds realized), which is why put-selling wins often; but payoffs are negatively skewed, losses cluster in crashes (2008, Feb 2018, Mar 2020, Aug 2024), and recent evidence (Dew-Becker & Giglio 2025) finds index option alphas have been statistically indistinguishable from zero for ~15 years.

### Cited Findings
- Carr & Wu (RFS 2009): model-free variance risk premium (realized variance minus variance-swap rate) is on average negative across stock indexes -> variance risk is priced. — [Carr & Wu 2009 (NYU)](https://engineering.nyu.edu/sites/default/files/2019-01/CarrReviewofFinStudiesMarch2009-a.pdf); [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=577222)
- Bakshi & Kapadia (2003): delta-hedged long option positions earn negative average returns, evidence of a negative volatility risk premium. — [as summarized in Carr & Wu JFE 2016](https://engineering.nyu.edu/sites/default/files/2018-09/CarrJournalofFinEconomics2016.pdf)
- Dew-Becker & Giglio (Chicago Fed WP 2025-17, Sept 2025): equity index options historically had sharply negative returns/CAPM alphas, but over the past ~15 years option alphas have become indistinguishable from zero; they attribute the decline to falling trading frictions (intermediary model). — [Chicago Fed](https://www.chicagofed.org/publications/working-papers/2025/2025-17); [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5525882)
- AQR "Understanding the Volatility Risk Premium" (Israelov et al., May 2018) and "Pathetic Protection" (JAI 2019) — relevant AQR literature on VRP harvesting and put-writing vs protective puts. — [AQR whitepaper](https://www.aqr.com/-/media/AQR/Documents/Whitepapers/Understanding-the-Volatility-Risk-Premium.pdf); [Pathetic Protection](https://images.aqr.com/-/media/AQR/Documents/Journal-Articles/Pathetic-Protection-JAI-Wint19.pdf) (full text not retrieved)
- 2008: PUT -26.8%, BXM -28.7%, SPX -37.0%. — [Wilshire 2019](https://cdn.cboe.com/resources/spx/wilshire-options-based-benchmark-indexes-2019.pdf)
- Feb 2018 ("Volmageddon," Feb 5, 2018) and Feb 2020 volatility shocks each sent the S&P 500 down >10% in two weeks. — [Roundhill blog (snippet)](https://blog.roundhillinvestments.com/historical-corrections-last-week)
- Aug 5, 2024: VIX had its largest single-day spike on record (~+180% to 65+ intraday, closing ~39), triggered by the BoJ hike and yen-carry unwind; Nikkei -12.4%; market makers widened spreads asymmetrically, especially in OTM puts; some funds reportedly lost up to 40% in a day. — [Substack analysis (secondary, unverified)](https://navnoorbawa.substack.com/p/volatility-arbitrage-how-funds-profited); [Avantis on Aug 2024](https://www.avantisinvestors.com/avantis-insights/lessons-from-market-panic-2024/)

### Inferences
- Put-selling is a short-crash-insurance business: high win rate is structural, and a single month like Oct 2008 or Mar 2020 can erase 1-3 years of premium. Defined-risk spreads cap the loss per trade (width minus credit) but at 16-delta that loss is typically 3-6x the credit.
- Aug 2024 illustrates gap/spread risk: stops placed on option marks can be triggered at extreme prices when spreads blow out intraday.

### Gaps
- No accessible source quantified PUT/WPUT/CNDR returns for Feb 2018, Mar 2020, or Aug 2024 specifically.
- Ilmanen's VRP evidence (Expected Returns) not retrieved.

---

## 7. Transaction costs at Robinhood and edge erosion

### Takeaway
Robinhood charges no commission on options but passes through ~$0.04/contract in regulatory/clearing fees plus the TAF on sells; the dominant cost is the bid-ask spread, and realistic fills are several cents worse than mid, which for a $0.50-$1.00 credit spread can consume a large fraction of the edge.

### Cited Findings
- Robinhood collects a combined ~$0.04 per options contract to cover ORF and OCC fees; OCC clearing fee rose to $0.025/contract in Jan 2025; FINRA TAF from Jan 1, 2026 is $0.00329 per option contract sold. — [Robinhood Fee Schedule](https://cdn.robinhood.com/assets/robinhood/legal/RHF+Fee+Schedule.pdf); [Robinhood support: trading fees](https://robinhood.com/us/en/support/articles/trading-fees-on-robinhood)
- OCC implemented a clearing-fee holiday Dec 1-31, 2025. — [Federal Register](https://www.federalregister.gov/documents/2025/12/03/2025-21775/self-regulatory-organizations-the-options-clearing-corporation-notice-of-filing-and-immediate)
- Muravyev & Pearson (RFS 2020): quoted spreads on liquid equity options average ~8.1 cents/share; effective spreads ~2.2% of option value after accounting for execution timing; traders who time executions pay <40% of conventionally measured spreads. — [Muravyev & Pearson paper](https://www.cicfconf.org/sites/default/files/paper_745.pdf); [RFS](https://academic.oup.com/rfs/article-abstract/33/11/4973/5732665)
- FlashAlpha's SPY study: fills 4-7 cents/contract worse than mid; only ~20-25% of posted orders filled. — [FlashAlpha (vendor)](https://flashalpha.com/articles/spy-put-credit-spread-active-backtest-mm-fills-vrp-signal-drawdown-breaker)
- Dew-Becker & Giglio attribute the disappearance of option alpha to lower trading frictions — i.e., cheaper hedging by intermediaries compressed the premium sellers earn. — [Chicago Fed](https://www.chicagofed.org/publications/working-papers/2025/2025-17)

### Inferences
- Example: a 4-leg SPY iron condor opened and closed = 8 contract-legs x ~$0.04 ≈ $0.32 fees plus ~$0.02-0.07/share x 100 x legs slippage; on a $1.00 ($100) credit this can exceed 10-30% of gross premium. SPX (cash-settled, European, 1256 tax treatment) has larger notional per contract, so fixed per-contract fees matter less, but Robinhood account size must support ~$500k-notional SPX spreads (defined-risk width controls margin).
- Backtests should assume fills at mid minus 25-50% of the half-spread (or natural price for exits under stress) and model at least $0.04-0.05/contract/leg.

### Gaps
- Robinhood's PFOF-based execution quality on multi-leg options vs mid not independently quantified in retrieved sources.

---

## 8. Data needed for an honest backtest; Black-Scholes + VIX approximation

### Takeaway
Honest backtests need point-in-time option chains with bid/ask (not just mid or IV-derived prices); free EOD SPX/SPY data exists (OptionsDX), paid sources (Cboe DataShop, ORATS) are more complete. A Black-Scholes model driven by VIX can approximate ATM SPX options but mis-prices OTM puts due to skew and omits spreads, so it will overstate or misstate win rates and P/L for 16-delta strategies.

### Cited Findings
- OptionsDX offers free historical EOD/intraday quotes for SPX, SPY, VIX etc. with precomputed greeks, IV and underlying price. — [OptionsDX](https://www.optionsdx.com/)
- Cboe DataShop sells option EOD summaries, trades and quote data; SPX index-level bid/ask requires a Cboe Global Indices license (from ~$1k/month); legacy "Optsum" EOD for SPX/OEX/VIX covers 2005 - 9/30/2019. — [Cboe DataShop](https://datashop.cboe.com/option-eod-summary); [Data Products](https://datashop.cboe.com/data-products)
- Cboe Hanweck historical data: full OPRA quotes/trades, end-of-day and windowed snaps. — [Cboe Hanweck](https://cboe.com/services/analytics/hanweck/historical_data/)
- FlashAlpha's own guide stresses point-in-time chains and realistic fills; its 96-cell study used 1-minute SPY chains. — [FlashAlpha guide](https://flashalpha.com/articles/complete-guide-quant-options-backtesting)
- Kumiega et al. (2024) found real options data 2012-2023 overturned earlier model-based passive-option outperformance. — [MDPI](https://www.mdpi.com/2227-7072/12/4/114)
- CNDR losses arise when realized vol exceeds implied priced into the 20-delta shorts. — [Options Jive](https://optionsjive.com/blog/iron-condor-options-strategy/)

### Inferences
- VIX is a 30-day, strike-weighted variance measure; a 16-delta SPX put typically trades at an IV several vol points above VIX-implied ATM vol due to skew, and the 5-delta wing even higher. Using VIX as flat IV would under-price OTM puts (understating credits) and mis-state the strike location for a given delta; a skew adjustment (e.g., from Cboe SKEW or a fitted smile) is needed. It also can't capture bid-ask blowouts (Aug 2024) or early-exit fill quality. Use BS+VIX only for rough prototyping; confirm with OptionsDX SPX/SPY chains.
- Required fields: date/time, underlying price, expiry, strike, type, bid, ask, (last/volume/OI), IV, delta; plus dividends/rates for SPY, and settlement rules (SPX AM vs PM settlement).
- Avoid look-ahead: select strikes using only data available at entry time; use EOD or fixed-time snapshots consistently.

### Gaps
- ORATS pricing and coverage not surfaced in searches.
- No published study quantifying BS-with-VIX backtest error vs real chains was found.
