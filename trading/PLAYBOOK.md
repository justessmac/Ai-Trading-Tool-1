# Live playbook: Agentic account (••••0819)

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
Core trend positions are never averaged down (no adding to losers outside
these rules).

## Hard rules
- Never deposit to or withdraw from this account, or move money in or out
  of it in any way (user's standing instruction, 2026-09-27).
- No options, no margin, no leverage, no shorting, no symbols other than SPY and IBIT, no
  discretionary trades. Changing these requires the user's say-so.
- Any rule change must first pass a backtest on data it was not tuned on and
  be written here with the evidence.
- If an order fails or anything looks wrong, do nothing and tell the user.

## Improvement process (goal: maximise long-run growth without risk of ruin)
Daily research (weekdays after the close) + monthly deep review (1st of each month):
0. Daily: check today's fills vs expected prices (slippage), data sanity, and any
   rule-following mistakes; then test ONE item from trading/research_backlog.md
   (or a new idea added there) and log the result. At most ONE rule change per
   calendar week, so each change's effect can be measured.
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
