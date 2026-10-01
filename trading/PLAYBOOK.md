# Live playbook: Agentic account (••••0819)


## >>> USER OVERRIDE 2026-10-01: ALL-IN OPTIONS MODE (supersedes Strategies 1-4 and the options limits) <<<
The user chose this explicitly on 2026-10-01 after being shown that it will very likely lose most or
all of the money (choice recorded in the session: "All-in options, as asked"). While this section
is active:
- Sell all stocks/ETFs and crypto in the account (at/after the 2026-10-01 open) and use the full
  buying power (keep ~$2 cash) to BUY option contracts, maximising the number of contracts within
  the liquidity filters below. Strategies 1-4 (SPY/QQQ/IBIT/dip/TOM/SGOV) are suspended; their
  daily-check routine is disabled.
- Long options only (calls/puts bought to open). Never sell naked options, never use margin to
  buy, no spreads that need collateral beyond the cash.
- Each new trade still needs its own research note in trading/research_notes/ (thesis, catalyst,
  why this strike/expiry, what kills it). Social media stays leads only.
- Contract filters (to avoid paying away the money in spreads): expiry 5-45 days; open interest
  >= 500 and volume today >= 100; bid-ask spread <= 15% of the mid; enter with a limit order at
  or near the mid. Among contracts passing these, prefer the setup with the best evidence, then
  the most contracts for the money.
- Exits: sell half when a position is +100%, let the rest run with a stop at breakeven on the
  remainder; sell everything 2 trading days before expiry if not already closed (avoid the last
  days of decay and exercise risk); no stop-loss on the way down unless the thesis breaks (a
  premium-based stop just locks in losses on noisy options).
- When flat, the next trade follows the same process with whatever cash is left.
- New deposits are NOT automatically put into options: they wait as cash until the user says what
  to do with them.
- GOAL AND TIME BOX (user, 2026-10-01): make as much money as possible with high-risk,
  high-reward option trades for 2 weeks, i.e. through the close of Thursday 2026-10-15, or until
  the account reaches a decent size, whichever comes first. "Decent size" = $10,000 account value
  (user, 2026-10-01; was $1,000).
- When the time box ends or the target is hit: close all option positions and tell the user.
  Then rewrite the daily-check routine from this playbook (all adopted strategies incl. 1b, 1c,
  3 change, 4) and resume Strategies 1-4, unless the user says otherwise.
- MEME-TRADE RESEARCH (user, 2026-10-01): scan for meme setups several times a day (WSB hot/new,
  StockTwits trending, Robinhood scanner for relative volume >= 3 and big % moves, short-interest
  and options-volume spikes, news via WebSearch). Social posts are still leads only: each meme
  trade needs our own check (real catalyst or squeeze mechanics, rising volume, options liquid
  enough to pass the filters) and a research note. A meme setup may replace an open position only
  if that position's thesis is broken or it is at the +100% half-sale point.
- EXIT TIMING (user, 2026-10-01: "time the market as best as possible for your exits"). Open
  positions are checked at every routine run (9:47, 10:47, 12:47, 14:47 meme scans and the 15:32
  check), using the underlying's 5-minute bars, VWAP and volume, on top of the fixed rules above:
  * Lock in gains with a trailing rule: once a position is up >= +50%, sell if it gives back
    more than a third of its peak gain (e.g. peak +90% -> sell below +60%).
  * Sell into strength: if the underlying spikes far above VWAP on climax volume (a parabolic
    5-minute run that starts printing lower highs, volume fading), take profit rather than wait.
  * Sell weakness early: if the underlying loses VWAP and the day's opening-range low (calls) or
    high (puts) on rising volume, and the thesis depended on momentum, exit rather than hope.
  * Events: if the thesis is a catalyst (earnings etc.), decide BEFORE the event whether to hold
    through it; the options' implied volatility usually collapses right after, so a call can lose
    even on good news. If the move already happened before the event, sell before it.
  * Avoid the first 5-10 minutes after the open and the last 5 minutes before the close for
    entries/exits unless a stop or event forces it (widest spreads).
  These are judgment aids, not a tested edge; every exit and its reason is logged.
- APPROVAL (user, 2026-10-01): all trades in this mode are made without asking first; the user is
  told after each trade (phone alert + summary).
- The user can end this mode early by saying so.

Goal: compound the account without risking ruin until it is large enough for
the SPY put-spread strategy (~$47k+). Deposits, not trading, will do most of
that; the job here is to never blow up and to capture market growth.

## Strategy: SPY 200-day trend filter (2% band)
Published rule (Faber 2007), not fitted here. 2000–2026 check on this repo's
data: CAGR +8.2%, max drawdown −19% (buy & hold: +8.0%, −55%), ~2 switches/yr.

- Signal checked each weekday at ~15:48 ET using the live SPY price vs the
  200-day SMA of daily closes (unadjusted).
- If SPY > SMA × 1.02 → SPY sleeve (50% of the account, see Strategy 2) in
  SPY (fractional, dollar-based market buys; keep ~$2 cash buffer).
- If SPY < SMA × 0.98 → sell all SPY, SPY sleeve holds cash.
- Between the bands → do nothing (keeps the current state).
- Cash the user adds themselves: all targets are % of total account value,
  so new money is deployed by the next daily check wherever signals are in
  (cash otherwise). Log each detected deposit in trading/deposits.csv so
  performance is measured separately from contributions.

## Strategy 1b: SPY/QQQ momentum rotation for the core (adopted 2026-10-01, phased in)
The 50% SPY sleeve is split in two halves, tracked in trading/state.json as "core_rotation":
- SPY trend half (25% of account): the Strategy 1 rule above, unchanged.
- Rotation half (25% of account): at the first check of each month, pick
  whichever of SPY/QQQ has the higher 126-trading-day return (daily closes).
  Hold the pick (checked daily) only while it is above its own 200-day SMA
  (2% band, same hysteresis as Strategy 1) AND its 126-day return is > 0;
  otherwise this half holds cash. A pick change mid-month waits for the next
  month's first check, unless the filter forces cash.
- Step 2: from the first check of November 2026, if the October phase-in had
  no execution problems, the whole 50% core sleeve follows the rotation rule
  and the SPY trend half is retired. Log the switch and alert the user.
Backtest (adjusted closes, 0.03%/side, next-day returns): chosen on 2000–2014
out of 6 rotation variants (+7.3%/yr, max DD −23.5% vs the SPY rule's +5.0%,
−21.7%); confirmed 2015–2026 (+10.6%/yr, −24.5% vs +8.0%, −20.9%); ~5
switches/yr. Drawdown is close to the −25% limit and the gain leans on QQQ's
tech run after 2015. Report: reports/core_rotation_backtest.md.

## Strategy 1c: core "out" cash in T-bills (approved 2026-10-01, effective 2026-10-05)
When the SPY trend half or the rotation half is out (holding cash), that cash
sits in SGOV instead of plain cash (only if $20 or more; sell SGOV first when
the half re-enters). Backtest (SHY as the 2003-2014 proxy): +9.9% vs +9.4%/yr
(DD −21% vs −24%) in 2003–2014; +10.7% vs +10.6% in 2015–2026. Long bonds (TLT,
IEF) and gold failed (TLT −42% DD in 2022). Report: reports/risk_off_asset_backtest.md.

## Strategy 2: Bitcoin trend sleeve via IBIT (adopted 2026-09-27, user asked for crypto)
Traded through IBIT (iShares spot Bitcoin ETF) as a regular fractional stock
order: same hours and tools as SPY, and Robinhood has daily history for it.
Backtest (GBTC 2017–2023 chained to IBIT 2024+, 0.1% cost per switch):
100-day SMA with a 5% band. Chosen on 2018–2021 (CAGR +59%, max DD −50% vs
buy & hold +37%, −77%); confirmed on 2022–2026 unseen data (CAGR +41%,
max DD −26% vs buy & hold +14%, −77%). ~3 switches/yr.
- Target split (updated 2026-09-27, user asked for swing trading): 50% SPY
  sleeve / 50% Bitcoin sleeve. The Bitcoin sleeve is split in two halves,
  both traded in IBIT and tracked separately in trading/state.json:
  * IBIT trend half (25% of account): when the IBIT trend signal is in,
    hold 25% of account × min(1, 0.40 / vol20) in IBIT (vol20 = annualised
    stdev of IBIT's last 20 daily returns); out → 0.
  * IBIT swing half (25% of account): BUY 25% of account in IBIT when
    RSI(2) of IBIT daily closes < 10 AND IBIT > its 100-day SMA; SELL that
    swing position when RSI(2) > 70 or after 10 trading days, whichever
    first. Otherwise this half holds cash.
  Swing rule chosen on 2018–2021 (17 trades, 82% win, +4.2%/trade, t=3.0),
  confirmed on 2022–2026 (20 trades, 70% win, +2.5%/trade, t=2.0; avg hold
  ~7 days; in the market ~8% of the time). Bitcoin-sleeve backtest (IS | OOS):
  trend only CAGR +28%/DD −29% | +30%/−25%; swing only +25%/−15% | +14%/−12%;
  50/50 hybrid +28%/−14% | +23%/−14%. The hybrid gives up some upside for
  roughly half the drawdown. Only ~37 swing trades in total: thin evidence,
  re-check in monthly reviews.
- Adjust the IBIT position only when its target differs from the current
  position by more than 5 points of the account (limits churn); full exits
  on the trend signal always execute.
- Rejected for crash protection (failed on 2022–2026 unseen data): trailing
  stops of 15/20/25% and a fast exit below the 20-day SMA.
- IBIT trades only on weekdays; Bitcoin moves 24/7, so weekend crashes show
  up as a Monday gap that no rule here can avoid.
- Each sleeve follows only its own signal; a sleeve that is "out" holds cash.
- Rebalance the SPY sleeve to 50% (of total account value) at the first check of each
  month, and only if a sleeve is off target by more than 5 points of the
  account.
- Caveats: only ~8 years of Bitcoin history (a strong era for crypto); GBTC's
  premium/discount adds noise before 2024.

## Strategy 3: SPY dip-buy swing (adopted 2026-09-29, user asked for buy-red/sell-green)
Uses idle cash only (cash not needed by the targets above), capped at 20% of
the account, tracked in trading/state.json as "spy_dip".
- BUY when SPY's RSI(2) (Wilder, daily closes incl. today's live price) < 10
  AND SPY > its 200-day SMA; size = min(20% of account, idle cash − $2).
- SELL that dip position when RSI(2) > 70 or after 10 trading days.
- If the Bitcoin swing signal fires while cash is tied up here, the Bitcoin
  swing uses what cash is left (it does not force a sale here).
Backtest (SPY, 0.03% cost/side, next-day fills): chosen on 2001–2014 (81
trades, 79% win, +0.55%/trade, t 2.5); confirmed 2015–2026 (98 trades, 68%
win, +0.36%/trade, t 2.2, ~6-day holds, ~9 trades/yr). Small edge per trade:
expected to add roughly +0.5–1%/yr to the account at 20% size.
- CHANGE EFFECTIVE 2026-10-05 (approved 2026-10-01; waits a week per the
  one-change-per-strategy-per-week rule): the dip candidates become SPY, QQQ
  and IWM. Each day with no dip position open, compute RSI(2) and the 200-day
  SMA for all three. If one or more has RSI(2) < 10 and is above its SMA200,
  buy the one with the LOWEST RSI(2) (same size rule); exit that fund on its
  own RSI(2) > 70 or after 10 trading days. One dip position at a time.
  Backtest (fills at the signal close, 0.03%/side): 2001–2014 sleeve +5.2%/yr
  (t 2.6) vs SPY-only +1.3%; 2015–2026 +6.6%/yr, 75% win, t 3.0, DD −15% vs
  +4.7%, −12%; ~12 trades/yr. Report: reports/dip_candidates_backtest.md.
Core trend positions are never averaged down (no adding to losers outside
these rules).

## Strategy 4: turn-of-month (TOM) + T-bill yield on idle cash (adopted 2026-10-01)
Idle cash = cash not needed by the targets above and not used by the IBIT
swing or SPY dip sleeves (those two have priority). Tracked in
trading/state.json as "tom".
- TOM: at the 15:48 check on the trading day when exactly 4 trading days of
  the month remain after today, BUY SPY with min(20% of account, idle cash −
  $2). SELL it at the 15:48 check on the 1st trading day of the next month.
  No trend filter. If the IBIT swing or SPY dip signal fires while TOM holds
  cash, they use what is left (no forced sale), like Strategy 3.
- T-bills: idle cash of $20 or more that TOM and the other sleeves are not
  using sits in SGOV (0-3 month T-bill ETF). Sell SGOV first whenever any
  sleeve needs cash. Don't trade SGOV for amounts under $20 (not worth the
  rounding).
Backtest (SPY, adjusted closes, 0.03%/side): chosen on 2001–2014 out of 40
settings (168 trades, 62% win, +0.53%/trade, t 2.7); confirmed 2015–2026
(140 trades, 59% win, +0.39%/trade, t 2.5); works on QQQ/IWM too. Edge over a
random 5-day hold is only ~+0.14%/trade; mostly cheap market exposure on ~24%
of days. Idle-cash sleeve 2015–2026: BIL+TOM +5.3%/yr (max DD −10%) vs BIL
+2.0%, cash 0%. Report: reports/turn_of_month_backtest.md.

## Hard rules
- Never deposit to or withdraw from this account, or move money in or out
  of it in any way (user's standing instruction, 2026-09-27).
- No margin, no leverage, no shorting stock, no discretionary trades.
  Changing these requires the user's say-so.
- Options: ALLOWED by the user on 2026-09-29, only as follows:
  - only a setup that has passed the adoption test on REAL historical option
    prices (Robinhood option historicals), after costs;
  - defined risk only: bought calls/puts or debit/credit spreads with a
    known max loss; never naked short options;
  - max loss per options trade ≤ 20% of the account; total options risk
    open ≤ 30% of the account;
  - every options order is recorded like any other trade and alerted.
- Symbols: SPY and IBIT for the core strategies; other US stocks/ETFs only
  through a strategy that passed the adoption test (e.g. a stocks-in-play
  day-trading rule), with the per-trade risk limits that strategy defines.
- Never copy trades. A ticker being hyped on Reddit/X/StockTwits, or someone
  else's trade, is only a lead. Before ANY trade in a non-core name the bot
  must (a) have a signal from an adopted, backtested strategy, and (b) write
  its own research note to trading/research_notes/YYYY-MM-DD_<TICKER>.md
  covering: the catalyst verified from a primary source (SEC filing, company
  press release, earnings report) or reputable news, not social posts;
  liquidity (volume, bid-ask spread, float); recent price/volume behaviour;
  red flags (dilution/offerings, reverse splits, pump patterns, halts,
  going-concern notes); planned entry, stop, exit and max loss. No note, no
  trade.
- Moving focus to a new strategy: if a newly adopted strategy (e.g. stocks-in-
  play day trading) beats the existing strategies on risk-adjusted return in
  its backtest AND over at least 30 live trades, the monthly review may shift
  more of the account to it, in steps of at most 25% of the account per
  month, keeping the drawdown limits. It never takes the whole account at
  once.
- Any rule change must first pass a backtest on data it was not tuned on and
  be written here with the evidence.
- If an order fails or anything looks wrong, do nothing and tell the user.

## Improvement process (goal: maximise long-run growth without risk of ruin)
Daily research (weekdays after the close) + monthly deep review (1st of each month):
0. Daily: check today's fills vs expected prices (slippage), data sanity, and any
   rule-following mistakes; then test ONE item from trading/research_backlog.md
   (or a new idea added there) and log the result. Multiple rule changes per
   week are allowed (user, 2026-09-29): every change must pass the adoption
   test on its own, gets its own dated log entry and phone alert, and each
   strategy's trades are tagged by sleeve so its live effect can be measured
   separately. Don't change the same strategy twice in one week.
1. Compare live results with what the backtest predicted; log the gap and why.
2. Research and backtest ONE candidate improvement (e.g. QQQ vs SPY
   momentum rotation, dual momentum, volatility-scaled exposure, adding
   cash yield via SGOV when out of the market).
3. Adopt it only if ALL hold: tested on 2000–2014, confirmed on 2015+ data it
   was not tuned on; higher CAGR on both; max drawdown no worse than −25%;
   no leverage, options, margin or shorting; fewer than ~12 trades a year.
4. Write the result here (adopted or rejected, with numbers) and in
   `trading/research_log.md`; tell the user and send a phone alert if the
   rules change.
Losses from following the rules are expected and are not a reason to change
them; only evidence from step 3 is.

## Journal
See `trading/journal.md` (one line per check that trades or changes state).
