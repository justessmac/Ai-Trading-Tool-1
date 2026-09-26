# High-Win-Rate Short-Term Mean-Reversion and Swing Strategies (Equities, ETFs, Crypto)

> **Method note (read first):** The network egress proxy blocked full-page fetches of every primary vendor and blog domain tried (quantifiedstrategies.com, alvarezquanttrading.com, quantpedia.com, turingtrader.com, quantitativo.com, coinquant.ai, and a gurufinanceinsights substack). So the figures below come from **search-result snippets and summaries of those pages**, not from pages read in full. Treat each number as "reported by source X, as shown in a search snippet". Check it against the page, or better, re-run the backtest before relying on it. Most numbers are **vendor or blog backtests** (QuantifiedStrategies sells strategies; Connors Research sells books and strategy guides). Few are independent, peer-reviewed or out-of-sample. Almost no source states its commission or slippage assumptions in the snippets.

## 1. Connors / Alvarez strategies: rules, published stats, post-publication decay

### Takeaway
The Connors/Alvarez family (RSI(2), Double 7s, Cumulative RSI, 3-day high/low, TPS, ConnorsRSI) reliably shows **~70-83% win rates on SPY/index ETFs** in backtests. Samples are small, however (about 150-600 trades on a single ETF). Losers are typically **larger than winners** (payoff ratio below 1). Raw returns usually **trail buy-and-hold**, because time in the market is low. The 90%+ win-rate claims (TPS "93.98%") come from Connors' own marketing. The one quantified decay study found (Concretum, on ConnorsRSI) shows the edge shrinking about 5x from the 1990s to 2015-2025.

### Cited Findings
**RSI(2), basic (Connors):**
- Canonical rules: SPY above its 200-day SMA; buy when RSI(2) drops below 5 (or 10); exit when the close is above the 5-day SMA (a variant exits when RSI(2) rises above 70). Connors' research reportedly found that stops *reduced* performance for this system — [StockCharts ChartSchool RSI(2)](https://chartschool.stockcharts.com/table-of-contents/trading-strategies-and-models/trading-strategies/rsi-2); [FMZQuant/Medium summary](https://medium.com/@FMZQuant/larry-connors-rsi2-mean-reversion-strategy-861f5a3579e3)
- QuantifiedStrategies' RSI(2) on SPY: **75% win rate, 0.57% average gain per trade, 23% max drawdown**. Period and trade count were not in the snippet. (Vendor.) — [QuantifiedStrategies: RSI2 on SPY](https://www.quantifiedstrategies.com/rsi2-on-spy/)
- An independent blogger ran classic RSI(2) on SPY from **Oct 2000 to recent**: **181 trades, 82% win rate**. It **loses to buy-and-hold on raw return** once costs are included. (Independent but unaudited; the full article could not be fetched.) — [Guru Finance Insights substack](https://gurufinanceinsights.substack.com/p/i-backtested-the-classic-rsi2-mean)
- A separate write-up of an "82% win rate SPY system" reports that the **average loss is roughly 2x the average win** — [backtest.substack: "The 82% Win Rate SPY System and the Metrics That Actually Matter"](https://backtest.substack.com/p/the-82-win-rate-spy-system-and-the)
- QuantifiedStrategies also markets a "Triple RSI" SPY pullback strategy with a **90% win rate** and an "RSI trading strategy (91% win rate)". (Vendor headline claims; rules and trade counts were not in the snippets.) — [QS Triple RSI](https://quantifiedstrategies.substack.com/p/triple-rsi-quantified-strategy-90); [QS RSI 91%](https://www.quantifiedstrategies.com/rsi-trading-strategy/)
- One search summary claimed "out-of-sample validation 2015-2025 shows slight performance decay from HFT competition." The claim traces to QuantifiedStrategies' RSI-2 guide; the underlying numbers were not visible. Treat it as an unverified vendor assertion — [QS RSI 2 guide](https://www.quantifiedstrategies.com/rsi-2-strategy/)

**Double 7s** (*Short Term Trading Strategies That Work*, Connors & Alvarez 2008):
- Rules: SPY above its 200-day SMA; buy at the next open after a **7-day closing low**; exit on a **7-day closing high**. There is no stop — [Easycators](https://easycators.com/thinkscript/connors-alvarez-double-7s-trading-strategy-for-thinkorswim-from-short-term-trading-strategies-that-work/); [QuantifiedStrategies Double Seven](https://www.quantifiedstrategies.com/larry-connors-double-seven-strategy-does-it-still-work/)
- SPY from 1993: **154 trades, 82.5% win rate, 1.18% average gain**. The **average loser (2.99%) is larger than the average winner (2.06%)**. Profit factor 2.58, Sharpe 1.4. QQQ 79.4%, FXI 76.9%, EWZ 81%. (Vendor re-test, done after publication, so partly out-of-sample for 2008 onward.) — [QuantifiedStrategies Double Seven](https://www.quantifiedstrategies.com/larry-connors-double-seven-strategy-does-it-still-work/)
- Journeyman Investor also reports about a 75% win rate — [Journeyman Investor](https://www.journeymaninvestor.com/double-7s-strategy-75-win-rate-stock-secrets/)

**Cumulative RSI** (same book):
- Book claim (p.104): **79.49% accurate on SPY**, 779.51 S&P points, average hold under 5 days. Rules as commonly summarized: SPY above its 200-day SMA; the 2-day sum of RSI(2) below 35 triggers entry (QS's snippet mentions a "3-day sum below 20" variant); exit when RSI(2) rises above 65 — [QuantifiedStrategies Cumulative RSI (83% headline)](https://www.quantifiedstrategies.com/cumulative-rsi-indicator/); [thinkorswim.net Cumulative RSI-3](https://thinkorswim.net/thinkscript/cumulative-rsi-3-trading-strategy/)
- A later variant (3-day sum below 20) shows a **68% win rate** in a re-test — [StratBase.ai RSI(2) article](https://stratbase.ai/en/blog/rsi-2-strategy-larry-connors). Conflict: the QS headline says 83%. The two figures differ by variant and period.

**3-Day High/Low** (*High Probability ETF Trading*, Connors):
- Rules: buy an ETF above its 200-day SMA after 3 consecutive lower highs and lower lows (plus a 5-day SMA condition) — [QuantifiedStrategies 3-day H/L](https://www.quantifiedstrategies.com/larry-connors-3-day-high-low-method/)
- QS re-test on SPY: **1,616 trades, 2000 to Nov 2020, 0.38% average gain per trade, CAGR 5.74%**. The win rate was not in the snippet. (This is one of the few single-ETF tests with more than 1,000 trades.) — [QuantifiedStrategies 3-day H/L](https://www.quantifiedstrategies.com/larry-connors-3-day-high-low-method/)

**TPS (Time, Price, Scale-in):**
- Connors marketing: "accuracy rate of **93.98%**", and "20+ variations ... over **92.8%** winning trades" in backtests (**vendor claims**) — [TradingStrategyGuides](https://tradingstrategyguides.com/tps-trading-strategy/); [Connors Research store](https://store6372061.ecwid.com/Connors-Research-Trading-Strategy-Series-ETF-Scale-In-Trading-p46730736); [TradingMarkets](https://tradingmarkets.com/recent/learn_how_to_trade_etf_funds_successfully_tps_and_the_science_of_scaling-in-677936)
- Rules as commonly summarized: ETF above its 200-day SMA and RSI(2) below 25 on 2 consecutive days → buy 10%. Add 20%, 30% and 40% at each lower close. Exit when RSI(2) rises above 70 — [Easycators TPS](https://easycators.com/thinkscript/tps-trading-strategy-connors/)
- An independent re-test (as summarized in search) found about **81 trades/year, a 77% win rate, +1.05% expected return per trade, and a 0.85 payoff ratio**. That is materially below the 93.98% claim. The attribution within the Quantitativo, TuringTrader and QS group of results is uncertain — [Quantitativo](https://www.quantitativo.com/p/trading-etfs-while-fear-and-greed); [TuringTrader Connors TPS](https://www.turingtrader.com/portfolios/connors-tps/)

**ConnorsRSI (2012-2014):**
- Out-of-sample decay study: stocks with **CRSI below 5 averaged +1.5% next-week return in 1990-2000**, versus **only +0.3% in 2015-2025**. (Concretum Research is independent of Connors.) — [Concretum Research on X](https://x.com/ConcretumR/status/1879572346362593308)
- QS headline: "75% win rate" for ConnorsRSI — [QuantifiedStrategies ConnorsRSI](https://www.quantifiedstrategies.com/connors-rsi/)

**General post-publication decay:**
- Across 72 published strategies, the **Sharpe ratio falls by about half after publication**. Causes are arbitrage or overfitting — [Falck, Rej & Thesmar, "Why and how systematic strategies decay" (arXiv 2105.01380)](https://arxiv.org/pdf/2105.01380)

### Inferences
- The typical Connors-type profile is: win rate 75-83%, average win about 0.8-2%, average loss 1.5-3%, profit factor 2-3, about 5-15% time in market, and ~150-600 SPY trades over 25-30 years. A 75-85% hit rate is therefore attainable. But the net edge per trade (about 0.4-1.2%) is thin relative to the tail loss.
- Claims above 90% (TPS, Triple RSI, "91%") come from vendors. The one independent-looking TPS re-test found 77%.
- ConnorsRSI decaying from 1.5% to 0.3% per week, together with the ~50% Sharpe haircut after publication, suggests using a **haircut of 50-80% on in-sample per-trade edge** when projecting forward.

### Gaps
- Could not retrieve the original book tables (Connors & Alvarez 2008/2009) with exact trade counts and periods, except the Cumulative RSI p.104 figure.
- No verified year-by-year RSI(2) results for 2008, 2020 or 2022 were found. The search summary asserting RSI(2) "diminished in 2022" had no visible supporting data.
- Cost assumptions were not visible in any of the vendor snippets.

## 2. IBS, turn-of-the-month, Bollinger pullbacks, "buy after N down days"

### Takeaway
IBS on SPY/QQQ shows some of the best per-trade stats among simple single-ETF rules: ~74-78% win rates and 0.8-1.3% average per trade. Turn-of-the-month gives ~78% wins on 198 trades at low exposure. A plain "3 down days" rule is weak (65% wins, 0.13% per trade) and easily consumed by costs.

### Cited Findings
- **IBS** = (Close − Low)/(High − Low). The simple rule is to buy when IBS is low (e.g. below 0.2) and exit when IBS is high or on a later close. Reported results: **SPY 0.8% average per trade, 78% win rate; QQQ 1.33% average, 75% win rate** (vendor) — [QuantifiedStrategies IBS](https://www.quantifiedstrategies.com/internal-bar-strength-ibs-indicator-strategy/)
- IBS + RSI on the S&P 500 (QS): **583 trades, average hold 5.8 days, 74% win rate, average win 1.67% vs average loss 1.75%, max drawdown 22%, profit factor 2.73, Sharpe 1.7**. Adding a VIX filter improved the win rate and per-trade return — [QuantifiedStrategies IBS strategies](https://www.quantifiedstrategies.com/ibs-internal-bar-strength-indicator-strategies/); [QS S&P 500 IBS+RSI](https://www.quantifiedstrategies.com/sp-500-mean-reversion-using-ibs-and-rsi/)
- Alvarez has a dedicated IBS mean-reversion study (the page could not be fetched) — [Alvarez Quant Trading IBS](https://alvarezquanttrading.com/blog/internal-bar-strength-for-mean-reversion/). An open-source Python IBS backtester for SPY (1993-present) exists for replication — [GitHub toniker10/SPY-IBS-Mean-Reversion-Strategy](https://github.com/toniker10/SPY-IBS-Mean-Reversion-Strategy)
- **Turn of the month** (SPY): **198 trades, 78% win rate, 0.68% per trade, 4.3% annual, invested 7% of the time**. A tighter variant produced **58 trades, 1.12% average**, 2% annual, invested 2% of the time. The window is typically the last 4 trading days plus the first 3 trading days of the month — [QuantifiedStrategies TOM substack](https://quantifiedstrategies.substack.com/p/the-turn-of-the-month-effect-with); [QuantSeeker "Do they still work?"](https://www.quantseeker.com/p/turn-of-the-month-strategies-do-they)
- **Buy after 3 down days (SPY, 1993-present):** **661 trades, 65% win rate, +0.13% per trade** with a next-open exit. A close exit gives +0.24% and 61% wins — [QuantifiedStrategies/tradinginvestingstrategies substack](https://tradinginvestingstrategies.substack.com/p/the-famous-3-down-days-trading-strategy-backtest)
- Bollinger-band pullbacks in an uptrend: **no specific trade counts or win rates were retrieved** (see Gaps).

### Inferences
- Stacking filters (IBS below 0.2, RSI(2) below 10, above the 200-day SMA, VIX elevated) raises the win rate but lowers trade count. On one ETF, reaching 1,000 or more trades requires a basket or looser rules.
- TOM is structurally different (calendar, not price-based) and weakly correlated with oversold signals. It is a candidate diversifier.

### Gaps
- No Bollinger-band pullback backtest with exact stats was retrieved.
- No independent (non-vendor) out-of-sample IBS results after 2015 were found.

## 3. Applying to baskets of stocks (1,000+ trades) and survivorship bias

### Takeaway
Running the rules across S&P 500 or Russell 1000 members easily yields thousands of trades. Using today's constituents (survivorship plus pre-inclusion bias) can badly inflate results. **Point-in-time constituents including delisted stocks (e.g. Norgate) are required.**

### Cited Findings
- One example of a mean-reversion system on S&P 500 stocks: **22.48% CAGR with biased (current-constituent) data vs 14.51% with unbiased data** — [hmaquant substack "Survivorship Bias and Other Data Landmines"](https://hmaquant.substack.com/p/survivorship-bias-and-other-data)
- Survivorship plus pre-inclusion bias **shifted S&P 500 constituent returns by about 7% per year over 10 years** — [Price Action Lab substack](https://priceactionlab.substack.com/p/survivorship-bias-in-backtesting)
- Conflicting evidence: Alvarez found that **adding delisted stocks *improved* a mean-reversion system**, with a "huge improvement" without the 200-day MA filter, while trend-following results worsened. So the direction of the bias depends on the strategy — [Alvarez: survivorship-free data](https://alvarezquanttrading.com/blog/how-much-does-hot-having-survivorship-free-data-changes-test-results/)
- Norgate Platinum supplies historical index constituents and delisted stocks. Unadjusted price data affects RSI and MA filters — [Alvarez Norgate review](https://alvarezquanttrading.com/blog/norgate-data-review/); [QuantRocket primer](https://www.quantrocket.com/blog/survivorship-bias/)

### Inferences
- For a 1,000-trade sample: about 500 S&P 500 names × an RSI(2)- or IBS-style rule produces thousands of trades per decade. But the trades cluster on the same selloff days, so the *effective* number of independent samples is much smaller than the trade count.
- The direction of survivorship bias for mean reversion is ambiguous. Survivor-only data drops the bankruptcies (flattering the strategy) but also drops the sharp rebounds in distressed names (penalizing it). Test both ways.

### Gaps
- No published Connors/Alvarez stock-basket stats (win rate, trade count) with point-in-time constituents were retrieved in full.

## 4. Crypto mean reversion (BTC/ETH) and fee sensitivity

### Takeaway
The evidence is mixed and mostly non-academic. Large, liquid coins (BTC/ETH) show **daily momentum more than reversal** in academic work. Retail RSI(2)-style dip-buying on BTC is marginal after fees. At a Robinhood-like round-trip cost (about 0.7-2%), a typical per-trade edge of about 0.5-1% is largely eliminated.

### Cited Findings
- Academic (3,600+ coins, daily): low prior-day return predicts outperformance (**reversal**), but this is driven by illiquid coins. **The handful of largest, most liquid coins show daily momentum instead** — [Dobrynskaya et al., "Up or down? Short-term reversal, momentum, and liquidity effects in cryptocurrency markets," Int'l Review of Financial Analysis 2021](https://www.sciencedirect.com/science/article/pii/S1057521921002349)
- Intraday BTC (Mar 2013 to May 2020) shows both intraday momentum and reversal. The pattern depends on jumps, FOMC days and liquidity — [Wen, Bouri, Xu, Zhao (SSRN 4080253)](https://www.sciencedirect.com/science/article/abs/pii/S1062940822000833)
- Padysak & Vojtko (2022), using hourly BTC data (Oct 2015 to Feb 2022), found that combining trend-following with mean reversion delivered **about 2x buy-and-hold risk-adjusted returns** — [Quantpedia](https://quantpedia.com/revisiting-trend-following-and-mean-reversion-strategies-in-bitcoin/)
- QuantifiedStrategies concludes that "traditional buy-the-dip / sell-strength mean reversion **doesn't work** on Bitcoin and cryptos". RSI works better as momentum on BTC — [QS Bitcoin RSI](https://www.quantifiedstrategies.com/bitcoin-rsi-trading-strategy/)
- Coinquant (vendor blog) reports a BTC daily mean-reversion variant at **+84.5% total, 74.1% win rate, 2018-2026**. It also found that **RSI(2) + 200 MA on BTC was marginal, with commissions "nearly wiping the edge"**, and that the low profit factor stems from oversized losers in real breakdowns — [Coinquant 78 backtests](https://www.coinquant.ai/blog/building-a-mean-reversion-strategy-in-cryptocurrency-markets-evidence-from-78-backtests); [Coinquant extreme-fear RSI](https://www.coinquant.ai/blog/trading-the-fear-what-backtesting-an-rsi-mean-reversion-strategy-through-extreme-fear-reveals-btc-2026)
- A Pine Script RSI strategy lost money on all 5 assets tested — [Betashorts, Medium](https://medium.com/@betashorts1998/i-backtested-the-same-pine-script-rsi-strategy-on-5-different-assets-every-single-one-lost-money-431dc2b9d13e)
- **Robinhood crypto cost:** default market-maker routing costs **close to 2% round trip on BTC**, and Robinhood receives $0.95 per $100 routed. "Smart Exchange Routing" carries a disclosed 0-0.95% fee that falls with volume — [BeInCrypto](https://beincrypto.com/robinhood-bitcoin-spread-agentic-trading/); [Yahoo Finance](https://finance.yahoo.com/markets/crypto/articles/trading-bitcoin-robinhood-why-2-220000888.html). A 2026 guide instead cites typical BTC/ETH spreads of **0.35-0.85%** per side — [Bitget Academy](https://www.bitget.com/academy/robinhood-crypto-trading-spreads-explained-2026-america-beginners-guide-costs-features-new-tools). (These figures conflict and vary by time and route.)

### Inferences
- If the gross per-trade edge is about 0.5-1% (typical for equity-style RSI dip-buys) and the round trip costs 0.7-2%, the net edge is about zero or negative. Crypto mean reversion on Robinhood therefore needs either much larger per-trade targets (about 3% or more) or a lower-cost venue.
- A high crypto win rate without a stop is especially dangerous: 50-80% drawdowns (2018, 2022) turn "dips" into regime breaks.

### Gaps
- No peer-reviewed BTC/ETH RSI(2) or Bollinger backtest with exact trade counts and fee sensitivity tables was retrieved.

## 5. No stop-loss, high win rates, and tail risk

### Takeaway
Connors and Alvarez explicitly found that **stops, even very wide ones (up to 50%), reduced performance** of their mean-reversion systems. That choice is a key reason win rates reach 75-85%. The trade-off is that the average loser is larger than the average winner, and the strategy carries a tail-loss profile concentrated in crashes.

### Cited Findings
- "In every single case, the use of stops lowered the performance. Even the 50% stop had lower performance than no stop" (Connors) — [TradingMarkets "Stops Hurt!"](https://tradingmarkets.com/trading-tip/stops-hurt-1597528); [Best of the Battle Plan: Stops Hurt](https://tradingmarkets.com/recent/best_of_the_battle_plan_stops_hurt-951402)
- Alvarez tested maximum-loss stops and scaling out on mean reversion — [Alvarez: Maximum loss stops](https://alvarezquanttrading.com/blog/maximum-loss-stops-do-you-really-need-them/); [Alvarez: Adding stops and scaling out](https://alvarezquanttrading.com/blog/adding-stops-and-scaling-out-to-a-mean-reversion-strategy/) (contents not retrieved)
- Payoff asymmetry evidence: Double 7s average loss 2.99% vs win 2.06% — [QS](https://www.quantifiedstrategies.com/larry-connors-double-seven-strategy-does-it-still-work/). "82% win" SPY system with losses about 2x wins — [backtest.substack](https://backtest.substack.com/p/the-82-win-rate-spy-system-and-the). Crypto: a low profit factor despite a high win rate, because losers are oversized in breakdowns — [Coinquant](https://www.coinquant.ai/blog/trading-the-fear-what-backtesting-an-rsi-mean-reversion-strategy-through-extreme-fear-reveals-btc-2026)
- Example March/April 2020: SPY RSI(2) at about 2.1 triggered an entry, and the trade gained **+4.4% in 2 days**. This is a search summary, so treat it as anecdotal — [Guru Finance Insights](https://gurufinanceinsights.substack.com/p/i-backtested-the-classic-rsi2-mean)
- Max drawdowns of **22-23%** for SPY RSI(2) and IBS systems, versus ~55% for SPY buy-and-hold in 2008 — [QS RSI2](https://www.quantifiedstrategies.com/rsi2-on-spy/); [QS IBS](https://www.quantifiedstrategies.com/ibs-internal-bar-strength-indicator-strategies/)

### Inferences
- The 200-day SMA filter blocks most entries during prolonged bear markets such as 2008 and 2022. It does not protect trades opened just before a crash begins (e.g. Feb 2020, Oct 2008 entries made while still above the 200-day SMA). A time stop (e.g. exit after 10 days) or a catastrophic stop is a sensible compromise even if it lowers backtest CAGR.

### Gaps
- No year-by-year verified returns for 2008, 2020 and 2022 were retrieved for any of these systems.

## 6. Evidence of weakening edges and where they still work

### Takeaway
The academic short-term reversal premium is real but time-varying: it is strongest when the VIX is high, and it is heavily eroded by costs. Practitioner evidence (Alvarez, Concretum) shows weaker stock mean reversion in low-volatility regimes and a much smaller per-trade edge since 2015. The edge is not gone, but it is smaller and depends on volatility.

### Cited Findings
- Nagel (2012), *Review of Financial Studies* 25(7):2005-2039: short-term reversal returns proxy the returns to liquidity provision. They are **strongly time-varying and predictable with the VIX**, and the conditional Sharpe "increases enormously" in turmoil such as 2007-09 — [RFS abstract](https://academic.oup.com/rfs/article-abstract/25/7/2005/1602153); [NBER w17653](https://www.nber.org/papers/w17653)
- Collin-Dufresne & Daniel link reversals to liquidity — [Kent Daniel working paper](https://www.kentdaniel.net/papers/unpublished/str2.pdf)
- Alvarez: mean reversion was "faltering" versus 2010-2015, especially in 2018, and "mean reversion likes volatility". Opportunities are fewer, but per-trade profit on Russell 1000 stocks since 1995 has not collapsed (the regression slope is only slightly down) — [Alvarez: Is mean reversion dead?](https://alvarezquanttrading.com/blog/is-mean-reversion-dead/); [Alvarez: Health of stock mean reversion](https://alvarezquanttrading.com/blog/the-health-of-stock-mean-reversion-dead-dying-or-doing-just-fine/). Note: the search snippets gave inconsistent dates (2013/2015/2018) for these posts.
- ConnorsRSI next-week edge fell from 1.5% (1990-2000) to 0.3% (2015-2025) — [Concretum](https://x.com/ConcretumR/status/1879572346362593308)
- The Sharpe ratio of published strategies falls by about 50% after publication — [arXiv 2105.01380](https://arxiv.org/pdf/2105.01380)

### Inferences
- The edge is most likely to persist in index ETFs (SPY/QQQ), large caps during high-VIX regimes, and a VIX-filtered IBS/RSI(2) combination. It is least likely in large-cap crypto on a retail spread venue.
- A realistic forward expectation for SPY RSI(2)/IBS systems is a win rate of about 70-80% with a per-trade edge of about 0.3-0.6% net, while holding at most the historical 20-25% max drawdown.

### Gaps
- Jegadeesh (1990) and Lehmann (1990), the original weekly/monthly reversal papers, were not retrieved or verified in this session. Their magnitudes should be sourced separately.
- The Quantpedia short-term reversal page (returns, Sharpe, cost notes) was blocked — [Quantpedia STR](https://quantpedia.com/strategies/short-term-reversal-in-stocks)
- No independent post-2015 RSI(2) SPY out-of-sample study with exact numbers was found beyond the Concretum ConnorsRSI result.
