# Robust Backtesting Methodology for High-Win-Rate (>=85%) Strategies

Research-process note: WebFetch was blocked by the egress proxy for every domain tried (ssrn/davidhbailey.com, wikipedia, robinhood cdn, metricgate), so findings below come from search-result summaries of primary sources (SSRN/journal abstracts, CBOE, broker disclosures). Items marked "(derived)" are standard algebra or computations I ran myself (Python, stdlib) and are listed under Inferences, not Cited Findings.

## 1. Math of win rate vs payoff ratio (expectancy, profit factor, skew, Kelly, ruin)

### Takeaway
A win rate is meaningless without the payoff ratio: at 85% hit rate the average loss can be at most ~5.67x the average win (payoff >= 0.1765) before costs. Strategies that achieve 85%+ hit rates are almost always structurally short volatility / negatively skewed (e.g., put writing, tight take-profit with wide or no stop), so their risk lives in rare tail losses that a 1000-trade sample may under-represent.

### Cited Findings
- Selling ATM S&P 500 puts monthly earned an average premium of 1.65% of notional per month (~19.8%/yr); the CBOE PUT index had a higher Sharpe/Sortino and *more negative skewness* than the S&P 500 — [Neuberger Berman / Bondarenko via NB](https://www.nb.com/documents/public/en-us/uncovering_the_equity_index_putwrite_strategy_ria.pdf); [Bondarenko 2019, CBOE](https://cdn.cboe.com/resources/education/research_publications/PutWriteCBOE19_v14_by_Prof_Oleg_Bondarenko_as_of_June_14.pdf)
- Over 32+ years, PUT compounded 9.54%/yr vs S&P 500 9.80% with volatility 9.95% vs 14.93%; average implied vol 19.3% vs realized 15.1% (1990–2018) — the volatility risk premium that funds high hit rates — [Bondarenko 2019, CBOE](https://cdn.cboe.com/resources/education/research_publications/PutWriteCBOE19_v14_by_Prof_Oleg_Bondarenko_as_of_June_14.pdf)
- PUT averaged +2.11% vs +4.14% for S&P in large up months and −2.93% vs −5.38% in large down months (capped upside, retained downside = negative skew profile) — [Bondarenko 2019, CBOE](https://cdn.cboe.com/resources/education/research_publications/PutWriteCBOE19_v14_by_Prof_Oleg_Bondarenko_as_of_June_14.pdf)
- Minimum track record length explicitly penalizes negative skew and positive excess kurtosis — i.e., a negatively skewed high-win-rate strategy needs a *longer* record to prove the same Sharpe — [Bailey & López de Prado, "The Sharpe Ratio Efficient Frontier" (SSRN)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1821643); [PerformanceAnalytics MinTrackRecord](https://rdrr.io/cran/PerformanceAnalytics/man/MinTrackRecord.html)

### Inferences
- (derived) Definitions for a trade list with win rate p, average win W>0, average loss L>0 (absolute), payoff ratio R = W/L:
  - Expectancy per trade E = p*W − (1−p)*L = L*(p*R − (1−p)).
  - Breakeven win rate p* = 1/(1+R); breakeven payoff R* = (1−p)/p.
  - Profit factor PF = sum(wins)/|sum(losses)| = p*W / ((1−p)*L) = p*R/(1−p). Profitable iff PF > 1.
  - Computed breakeven payoff: p=0.85 → R*=0.1765 (avg loss may be up to 5.67x avg win); p=0.90 → 0.1111 (9x); p=0.95 → 0.0526 (19x). Costs raise these thresholds: add per-trade cost c to L and subtract from W.
- (derived) Why high hit rates imply negative skew: hitting 85% requires placing the profit target much closer than the effective stop (or using no stop, or selling options). Mechanically, a random-walk trade with target +a and stop −b hits the target with probability ≈ b/(a+b) before costs, so 85% "win rate" with zero edge is trivially obtainable with b ≈ 5.67a. A high hit rate is therefore NOT evidence of edge; only positive net expectancy is.
- (derived) Kelly: for a binary bet, f* = p − (1−p)/R = (p*R − (1−p))/R. Example p=0.85, R=0.25: f* = 0.85 − 0.15/0.25 = 0.25. But Kelly assumes the loss size is known; for short-vol strategies the true worst loss is fat-tailed (gap/crash), so use fractional Kelly (e.g., ¼–½) sized off a *stressed* loss (e.g., the worst historical loss ×2 or a scenario like the 1987/2008/2020 gap), not the average loss.
- (derived) Risk-of-ruin check to implement: Monte Carlo resample the trade P&L list (with block bootstrap to keep clustering), apply the sizing rule, and report P(drawdown > X%) and P(equity < ruin threshold) over the planned horizon; for negatively skewed strategies also inject synthetic tail events (e.g., a −10x-average-loss trade at rate 1/1000) to see sensitivity.
- A report for any >=85% claim should always show: p with CI, R, E (net of costs) with CI, PF, skewness/kurtosis of trade returns, max single loss as multiple of avg win, and max drawdown.

### Gaps
- Could not fetch a primary source for formal risk-of-ruin formulas under fat tails (e.g., Vince, Thorp); the Kelly/ruin items above are standard derivations, not cited.

## 2. Data snooping and multiple testing (PBO, DSR, Reality Check, SPA, t>3, "iterate until target")

### Takeaway
Every configuration tried must be counted. Selecting the best of N variants inflates the in-sample metric by roughly the expected maximum of N noise draws (≈2.5σ for N=100, ≈3.3σ for N=1000). Iterating parameters "until" win rate >=85% and PF>1 is precisely the procedure these tests were built to penalize; the reported metric must be deflated (DSR), the selection process evaluated (PBO via CSCV), or the family tested jointly (Reality Check/SPA), and the final claim confirmed on untouched data.

### Cited Findings
- PBO (Bailey, Borwein, López de Prado, Zhu) estimates the probability that the in-sample-best configuration underperforms the median out-of-sample, via combinatorially symmetric cross-validation (CSCV); standard hold-out is described as unreliable for investment backtests — [SSRN 2326253](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253); [Semantic Scholar](https://www.semanticscholar.org/paper/The-Probability-of-Backtest-Overfitting-Bailey-Borwein/b1233b4f5384f003e85c2e0eec1a2dfc08f624c5)
- Deflated Sharpe Ratio (Bailey & López de Prado, 2014) corrects for selection bias under multiple testing and non-normal returns; it is the Probabilistic Sharpe Ratio with the benchmark replaced by a "deflated" benchmark (the expected max Sharpe across trials) — [SSRN 2460551](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2460551); [Balaena Quant / Medium](https://medium.com/balaena-quant-insights/deflated-sharpe-ratio-dsr-33412c7dd464)
- MinBTL: approximate upper bound MinBTL < 2·ln(N) / E[max_N]² (years); with only 5 years of data, no more than ~45 independent configurations should be tried or one almost surely finds an IS annualized Sharpe of 1 with OOS expected Sharpe 0 — [Bailey et al., "Pseudo-Mathematics and Financial Charlatanism", Notices of the AMS 2014](https://www.ams.org/notices/201405/rnoti-p458.pdf); [SSRN 2308659](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2308659). (Note: the search summary rendered the bound without the square on E[max_N]; from my recollection of the AMS paper the bound is 2·ln N / E[max_N]², but I could not open the PDF to confirm. With E[max_N]=1 both forms give the same number: for N=45 the bound is 2·ln45 ≈ 7.6 years, and the exact (non-approximate) expression in the paper gives about 5 years, which matches the 5-year/45-trial example.)
- Harvey, Liu & Zhu (RFS 2016): given hundreds of tested factors, a new factor should clear t > 3.0 rather than 2.0; "most claimed research findings in financial economics are likely false" — [RFS](https://academic.oup.com/rfs/article/29/1/5/1843824); [NBER w20592](https://www.nber.org/papers/w20592)
- Harvey & Liu "Backtesting" (JPM 2015): industry routinely applies an ad-hoc 50% Sharpe haircut; they show the correct haircut is non-linear (larger for marginal Sharpe ratios) and provide a profit hurdle adjusted for number of tests (Bonferroni, Holm, BHY); code is published — [SSRN 2345489](https://papers.ssrn.com/abstract=2345489); [Duke programs](https://people.duke.edu/~charvey/backtesting/); [quantstrat SharpeRatio.haircut](https://rdrr.io/github/braverock/quantstrat/man/SharpeRatio.haircut.html)
- White's Reality Check (2000) and Hansen's SPA (2005) test whether the *best* of many rules beats a benchmark, using a stationary bootstrap over the whole model universe; SPA studentizes and drops very poor models, making it less conservative/more powerful than RC — [Hansen, "A Test for Superior Predictive Ability"](https://cdr.lib.unc.edu/downloads/zp38wf793); [Hsu & Kuan, RC and SPA on technical analysis](https://homepage.ntu.edu.tw/~ckuan/pdf/snoop01.pdf); [Hsu, Hsu & Kuan Step-SPA](https://homepage.ntu.edu.tw/~ckuan/pdf/Step-SPA-20090720.pdf)
- Aronson's Evidence-Based Technical Analysis frames data-mining bias from testing many rules on the same history and uses Monte Carlo permutation (Masters) and bootstrap to build a no-skill null distribution; detrending the market data is shown equivalent to benchmarking against position bias — [Wiley](https://onlinelibrary.wiley.com/doi/book/10.1002/9781118268315); [ResearchGate](https://www.researchgate.net/publication/286014244_Evidence-Based_Technical_Analysis_Applying_the_Scientific_Method_and_Statistical_Inference_to_Trading_Signals)
- MinTRL formula: MinTRL = 1 + [1 − γ3·SR + ((γ4 − 1)/4)·SR²]·(Φ⁻¹(1−α)/SR)², SR per-period, γ3 skew, γ4 raw kurtosis — [PerformanceAnalytics](https://rdrr.io/cran/PerformanceAnalytics/man/MinTrackRecord.html); [Bailey & López de Prado SSRN 1821643](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1821643)

### Inferences
- (derived, implementable) PSR and DSR in Python:
  - σ(SR̂) = sqrt( (1 − γ3·SR̂ + ((γ4−1)/4)·SR̂²) / (T−1) ), T = number of returns (trades or periods).
  - PSR(SR*) = Φ( (SR̂ − SR*) / σ(SR̂) ).
  - Expected max Sharpe across N trials: SR0 = sqrt(Var[{SR_n}]) · [ (1−γ)·Φ⁻¹(1 − 1/N) + γ·Φ⁻¹(1 − 1/(N·e)) ], γ = 0.5772 (Euler–Mascheroni). DSR = PSR(SR0). Accept if DSR > 0.95.
  - Computed multiplier (1−γ)Φ⁻¹(1−1/N)+γΦ⁻¹(1−1/(Ne)): N=10 → 1.575; N=100 → 2.531; N=1000 → 3.255. I.e., with 1000 tried variants, the best one's Sharpe t-stat ≈3.3 purely by chance — matching the Harvey-Liu-Zhu t>3 hurdle intuitively.
- (derived) CSCV/PBO algorithm to implement: build matrix M (T periods × N configurations of per-period P&L); split rows into S even blocks (e.g., S=16 → C(16,8)=12,870 combos); for each combo, IS = S/2 blocks, OOS = complement; pick best config IS by chosen metric; compute its relative rank ω̄ in OOS; λ = ln(ω̄/(1−ω̄)); PBO = fraction of combos with λ ≤ 0. Target PBO < 0.05–0.10; PBO ≳ 0.5 means selection is no better than random.
- "Iterate until target" protocol that remains valid: (a) log every variant tested (N) including abandoned ones; (b) lock the final hold-out before any iteration and touch it once; (c) report DSR using the logged N and the variance of trial Sharpes; (d) run SPA/RC or a permutation test over the full family; (e) if the hold-out fails, it is burned — any further iteration needs new data (paper trading / forward test).
- For a win-rate target specifically, the same logic applies to the proportion: the best of N rules' hit rate is biased upward; Bonferroni-adjust (α/N) or use a bootstrap max-statistic null.

### Gaps
- Exact published DSR/PBO numeric thresholds could not be verified from the full papers (fetch blocked); 0.95 DSR and PBO<0.1 are common practitioner conventions, not confirmed from the source text.
- No primary source fetched for how to count "effective independent trials" when variants are correlated (López de Prado suggests clustering trials; not verified here).

## 3. Walk-forward, splits, CPCV, Monte Carlo reshuffling, bootstrap / Wilson CI at n=1000

### Takeaway
Use an untouched final hold-out plus either rolling walk-forward (Pardo: IS window 4–6x the OOS window; walk-forward efficiency >= 0.5) or combinatorial purged CV with embargo to get a distribution rather than a single OOS path. At n=1000 trades, an observed 85% hit rate has a 95% Wilson CI of roughly 82.7%–87.1%, so to *confirm* p >= 0.85 you need an observed hit rate of about 87%+ over 1000 trades.

### Cited Findings
- Pardo recommends rolling walk-forward with in-sample window 4–6x the out-of-sample window (e.g., daily data with 1-year OOS → 4–6 years IS) — [Quanthop summary of Pardo 2008](https://quanthop.com/learn/backtesting-optimization/parameter-optimization); [Better System Trader interview with Pardo](https://bettersystemtrader.com/060-strategy-optimization-with-robert-pardo/)
- Walk-forward efficiency WFE = annualized OOS performance / annualized IS performance; >=50% considered successful, >70% strong, <30% suggests overfit — [TradeStation WFO help](https://help.tradestation.com/09_01/tswfo/topics/walk-forward_summary_out-of-sample.htm); [Quanthop](https://quanthop.com/learn/backtesting-optimization/parameter-optimization) (secondary sources; thresholds are practitioner rules of thumb)
- Purging removes training observations whose labels overlap the test period; an embargo additionally drops training observations just after the test set; CPCV generates multiple backtest paths from combinations of train/test groups — [Purged cross-validation (Wikipedia via search)](https://en.wikipedia.org/wiki/Purged_cross-validation); [QuantInsti](https://blog.quantinsti.com/cross-validation-embargo-purging-combinatorial/); [skfolio CombinatorialPurgedCV](https://skfolio.org/generated/skfolio.model_selection.CombinatorialPurgedCV.html)
- Wilson score interval: (p̂ + z²/2n ± z·sqrt(p̂(1−p̂)/n + z²/4n²)) / (1 + z²/n); recommended over Wald as a default — [Binomial proportion CI](https://en.wikipedia.org/wiki/Binomial_proportion_confidence_interval); [AFIT recommended intervals](https://www.afit.edu/STAT/statcoe_files/12_Binomial%20proportion%20intervals%20DRAFT%20-%20PA%20copy(1).pdf)
- PBO paper argues plain hold-out is unreliable for backtests (single path, wasteful, and researchers peek) — [SSRN 2326253](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253)

### Inferences
- (computed, 95% Wilson) n=1000: p̂=0.85 → [0.8265, 0.8708]; p̂=0.87 → [0.8477, 0.8894]; p̂=0.90 → [0.8798, 0.9171]. n=500: p̂=0.85 → [0.816, 0.879]. So "≥85% confirmed" at 95% one-sided needs roughly p̂ ≥ 0.869 at n=1000 (one-sided z=1.645 lowers this slightly, to ~0.868). Python: `statsmodels.stats.proportion.proportion_confint(k, n, method='wilson')`.
- Independence caveat: Wilson assumes i.i.d. trades. Overlapping or same-day trades across correlated tickers are clustered; use block bootstrap (by day/week) or compute an effective n (e.g., n_eff = number of distinct non-overlapping trade days) and recompute the CI.
- Recommended split for a 1000+ trade study: chronological 60% development (with internal walk-forward or CPCV), 20% validation (model/parameter selection lock), 20% final test touched once; require ≥1000 trades in the *combined OOS* (walk-forward stitched OOS + final test), not in-sample.
- Monte Carlo trade reshuffling: permuting trade order does NOT change win rate, mean, or total P&L — it only produces a distribution of drawdown/path statistics (report 95th-percentile max drawdown and longest losing streak). To test edge, use (a) bootstrap of trade returns for CI on mean/PF, (b) permutation/randomized-entry null (random entries with the same exit rules and holding times) — critical for high-win-rate strategies because asymmetric target/stop alone produces high hit rates.
- Randomized-entry null specifically: generate ≥1000 random-entry strategies with identical TP/SL/holding rules on the same instruments/dates; the real strategy's net expectancy must beat the 95th (or Bonferroni-adjusted) percentile of that null; its hit rate should also exceed the null's hit rate distribution.
- Stability checks: parameter plateau (performance should degrade smoothly for ±10–20% parameter perturbations), subperiod consistency (bull/bear/high-VIX regimes), and cross-instrument consistency.

### Gaps
- Could not access Pardo's book directly; thresholds are via secondary summaries.
- No authoritative source found for a recommended number of CPCV groups; skfolio docs expose n_folds/n_test_folds but defaults were not verified.

## 4. Realistic cost modeling and biases (slippage, spread, Robinhood fees, fills, lookahead, survivorship)

### Takeaway
High-win-rate strategies have small average wins, so costs consume a large fraction of edge: a 0.2% round-trip cost on a strategy whose average win is 0.5% removes 40% of every win. Model fills at the next bar's open (or worse), charge half-spread + slippage each side, include Robinhood's regulatory fees on sells and crypto spread markups, and use survivorship-free, point-in-time data.

### Cited Findings
- Robinhood (per search summary of its fee schedule): FINRA TAF from 1 Jan 2026 is $0.000195/share on equity sells and $0.00329/contract on option sells, max $9.79/trade, not passed through for sales of 50 shares or less; SEC Section 31 fee rate set to $0 as of 14 May 2025 for the remainder of that fiscal year (rate resets periodically); Options Regulatory Fee (ORF) is passed through as a blended rate that varies by exchange — [Robinhood Financial Fee Schedule](https://cdn.robinhood.com/assets/robinhood/legal/RHF+Fee+Schedule.pdf) (PDF itself not fetchable here; values from search summary — verify before use)
- Robinhood crypto: zero commission, but cost is embedded in the spread; as of 15 June 2026 Robinhood Crypto receives $0.95 per $100 notional (0.95%) from its market maker on market-maker-routed orders; secondary sources report ~0.35–0.85% markups on major coins and reports of ~2% effective BTC spread on the default route — [Robinhood Crypto fee schedule PDF](https://cdn.robinhood.com/assets/robinhood/legal/rhc-fee-schedule.pdf); [Robinhood crypto order routing](https://robinhood.com/us/en/support/articles/crypto-order-routing/); [Yahoo Finance on 2% spread](https://finance.yahoo.com/markets/crypto/articles/trading-bitcoin-robinhood-why-2-220000888.html); [Bitget academy](https://www.bitget.com/academy/robinhood-crypto-fee) (figures conflict across sources and dates — treat 0.5–1% per side as a planning range and verify with live quotes)
- Survivorship: delisted tickers often vanish from Yahoo/Stooq, so backtests on today's tickers silently drop losers and inflate returns — [ASSIP data card on free equity APIs](https://edwardlg.github.io/assip-2026-empirical-finance/textbook/data-cards/free-equity-apis.html)
- yfinance `auto_adjust=True` back-adjusts prices for splits/dividends, so historical prices change after each dividend and two pulls can disagree — [ASSIP data card](https://edwardlg.github.io/assip-2026-empirical-finance/textbook/data-cards/free-equity-apis.html)
- Purging/embargo exist because labels depending on future events leak into training (a form of lookahead) — [QuantInsti](https://blog.quantinsti.com/cross-validation-embargo-purging-combinatorial/)

### Inferences
- (derived) Cost model to implement per side: cost = half_spread + slippage + fees. Suggested conservative defaults for backtests (assumptions, not sourced): liquid large-cap US equities/ETFs 2–5 bps per side; small caps 10–30 bps; options: fill at mid ± 25–50% of quoted spread (options spreads are often 1–10% of premium, which dominates small-premium short-option wins); crypto via Robinhood: ~0.5–1.0% per side from the markup above. Stress test with 2x costs — a strategy that fails at 2x costs is fragile.
- Fill rules: signal computed on bar t close → execute at bar t+1 open (plus slippage). Intrabar TP/SL on daily bars: if both TP and SL could be hit in the same bar, assume the stop hit first (pessimistic); this matters enormously for high-win-rate TP/SL designs where optimistic ordering inflates hit rate.
- Gaps: stop orders on daily data should fill at min(stop, open) for longs when the open gaps through — gaps are where negatively skewed strategies lose; ignoring them understates tail losses.
- Lookahead checklist: no use of same-bar close for same-bar entry; adjusted-price data not used to compute signals that assume raw price levels (e.g., round-number or $-based filters); indicators computed with only past data (check `shift(1)`); universe membership point-in-time; fundamentals by release date not period end.
- Robinhood-specific: TAF/SEC are negligible for most retail sizes (e.g., selling 500 shares → ~$0.10 TAF); the material Robinhood costs are spread/PFOF execution quality and crypto markups.

### Gaps
- Could not verify the current (FY2026) SEC Section 31 rate or Robinhood's current ORF blended rate; primary PDFs were blocked.
- No authoritative source found for typical Robinhood equity price improvement/slippage in bps.

## 5. Free data sources (daily/intraday prices, VIX, options)

### Takeaway
For daily equities/ETFs: yfinance (convenient but unofficial and survivorship-biased), Stooq (no key), Tiingo (free key, cleaner EOD), Alpha Vantage (25 calls/day free). For crypto intraday: Binance bulk files at data.binance.vision (with checksums) and exchange REST klines. VIX: free CSV from CBOE since 1990. Historical option chains are the hard part — free samples exist (OptionsDX, DoltHub, Kaggle), otherwise paid (CBOE DataShop).

### Cited Findings
- Alpha Vantage free tier: 25 requests/day, 5/min — [Alpha Vantage support](https://www.alphavantage.co/support/); [DEV Community comparison](https://dev.to/pickuma/alpha-vantage-vs-yahoo-finance-api-free-market-data-for-side-projects-an-honest-comparison-411o)
- yfinance is unofficial, scrapes an endpoint Yahoo may change; Stooq is free, no key, reachable via pandas-datareader; Tiingo has a free keyed tier with cleaner documented EOD data; all suffer survivorship bias — [ASSIP data card](https://edwardlg.github.io/assip-2026-empirical-finance/textbook/data-cards/free-equity-apis.html)
- Binance publishes daily and monthly zipped kline/trade/aggTrade files at data.binance.vision (URL pattern `https://data.binance.vision/data/spot/monthly/klines/<SYMBOL>/<interval>/<SYMBOL>-<interval>-YYYY-MM.zip`), each with a .CHECKSUM (sha256); fields: open_time, OHLC, volume, close_time, quote volume, num_trades — [binance-public-data GitHub](https://github.com/binance/binance-public-data); [Binance data portal](https://data.binance.vision/?prefix=data%2Fspot%2Fmonthly%2Fklines)
- CBOE VIX daily history 1990–present free at `https://cdn.cboe.com/api/global/us_indices/daily_prices/VIX_History.csv` (DATE, OPEN, HIGH, LOW, CLOSE) — [Macroption](https://www.macroption.com/vix-historical-data/); [CBOE VIX historical data](https://www.cboe.com/tradable-products/vix/vix-historical-data)
- VIX options history is not free (CBOE DataShop) — [Macroption](https://www.macroption.com/vix-options-historical-data/); [Cboe DataShop](https://datashop.cboe.com/)
- Free option-chain sources: DoltHub, Cboe, Kaggle, OptionsDX; OptionsDX offers free chains for SPY, SPX, VIX, QQQ, TSLA, AAPL, NVDA, UVXY, SLV and Deribit BTC for 2010–2023 at EOD to minute frequency — [David Arias, CFA](https://davidariasfinance.com/scripts/free-options-data/)
- CBOE PUT index (put-write benchmark) dashboard for benchmarking short-put strategies — [CBOE PUT dashboard](https://www.cboe.com/us/indices/dashboard/put/)

### Inferences
- For survivorship-free equity universes on free data, restrict tests to ETFs/indices or to a fixed historical list; otherwise note that single-stock results are upward biased.
- Coinbase public candles API is another crypto source (not verified in this session).
- For backtesting short-option high-win-rate strategies without paid chains, one can approximate with Black-Scholes using VIX as IV proxy for SPX, but this ignores skew and spreads — treat as indicative only; validate on OptionsDX sample chains.
- The Robinhood MCP (get_equity_historicals / get_option_historicals) may be usable for recent data but likely has limited lookback (not verified; the connector failed to connect in this session).

### Gaps
- Tiingo free-tier exact limits and Coinbase candle limits not verified.
- Binance REST klines per-request limit (commonly 1000 candles) was not confirmed by the retrieved sources.

## 6. Statistical tests for "confirmed profitability" (t-test, bootstrap, MinTRL)

### Takeaway
"Confirmed" should mean: on out-of-sample trades net of costs, (1) mean trade return > 0 with t >= 3 (multiple-testing-aware hurdle), (2) bootstrap 95% lower bound on mean and on profit factor above 0 / 1, (3) Wilson lower bound on hit rate >= 0.85, (4) DSR > 0.95 given the logged number of trials, and (5) record length >= MinTRL given skew/kurtosis — plus beating a randomized-entry null.

### Cited Findings
- t > 3.0 hurdle for new findings under multiple testing — [Harvey, Liu & Zhu, RFS 2016](https://academic.oup.com/rfs/article/29/1/5/1843824)
- Harvey & Liu provide multiple-testing-adjusted profit hurdles and haircut Sharpe (Bonferroni/Holm/BHY) with code — [Duke programs](https://people.duke.edu/~charvey/backtesting/); [Practical Applications summary](https://people.duke.edu/~charvey/Media/2016/Practical_applications_backtesting.pdf)
- MinTRL formula and its penalty on negative skew/fat tails — [PerformanceAnalytics MinTrackRecord](https://rdrr.io/cran/PerformanceAnalytics/man/MinTrackRecord.html); [Portfolio Optimizer blog on PSR/MinTRL](https://portfoliooptimizer.io/blog/the-probabilistic-sharpe-ratio-hypothesis-testing-and-minimum-track-record-length-for-the-difference-of-sharpe-ratios/); Python impl: [jsharpe](https://github.com/tschm/jsharpe)
- Stationary bootstrap is the resampling basis of Reality Check/SPA — [Hansen SPA](https://cdr.lib.unc.edu/downloads/zp38wf793)

### Inferences
- (derived) Trade-level t-stat: t = mean(r) / (std(r)/sqrt(n)) = SR_trade·sqrt(n). For n=1000 and t=3, the needed per-trade Sharpe is 3/sqrt(1000) ≈ 0.095. Example: p=0.85, win +1%, loss −4.5% → mean = 0.85 − 0.675 = 0.175%; std ≈ sqrt(0.85·1² + 0.15·4.5² − 0.175²) ≈ sqrt(0.85+3.0375−0.0306) ≈ 1.964% → SR_trade ≈ 0.089 → t ≈ 2.82 at n=1000: *not* confirmed at t>3 despite 85% wins and positive expectancy. Shows how thin high-win-rate edges are statistically.
- With negative skew, the t-test's normal approximation is optimistic; prefer bootstrap (≥10,000 resamples; block bootstrap if trades cluster) percentile or BCa CIs for mean return and PF (`scipy.stats.bootstrap`). Also check MinTRL with the observed γ3 (negative) and γ4 (high) — it will exceed n computed from the naive t-test.
- Minimal Python acceptance pipeline:
  1. `trades` = OOS net-of-cost returns (after next-open fills, pessimistic intrabar ordering).
  2. Hit rate Wilson lower bound (one-sided 95%) >= 0.85.
  3. `scipy.stats.ttest_1samp(r, 0, alternative='greater')` → t >= 3 (or p < 0.05/N_trials).
  4. Bootstrap lower 95% bound of mean > 0 and of PF > 1.
  5. DSR > 0.95 using N = number of logged variants, SR variance across variants, γ3, γ4.
  6. PBO < 0.1 from CSCV over the tried configuration grid.
  7. Randomized-entry null: real expectancy > 95th percentile of null.
  8. Robustness: 2x cost stress still PF > 1; subperiod/regime split all positive or explained; ±20% parameter perturbation keeps PF > 1.
  9. Tail: max single loss and 99th-percentile Monte Carlo drawdown within risk budget; fractional-Kelly sizing on stressed loss.

### Gaps
- No primary source verified for recommended bootstrap resample counts or block lengths (Politis–White automatic block-length selection exists in the `arch` package, not verified in this session).
