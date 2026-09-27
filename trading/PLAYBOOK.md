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
- Cash the user adds themselves: invest it only while the signal is "in".

## Strategy 2: Bitcoin trend sleeve via IBIT (adopted 2026-09-27, user asked for crypto)
Traded through IBIT (iShares spot Bitcoin ETF) as a regular fractional stock
order: same hours and tools as SPY, and Robinhood has daily history for it.
Backtest (GBTC 2017–2023 chained to IBIT 2024+, 0.1% cost per switch):
100-day SMA with a 5% band. Chosen on 2018–2021 (CAGR +59%, max DD −50% vs
buy & hold +37%, −77%); confirmed on 2022–2026 unseen data (CAGR +41%,
max DD −26% vs buy & hold +14%, −77%). ~3 switches/yr.
- Target split (updated 2026-09-27 for crash protection): 50% SPY sleeve /
  50% IBIT sleeve, with the IBIT sleeve volatility-scaled:
  IBIT exposure = 50% of account × min(1, 0.40 / vol20), where vol20 is the
  annualised standard deviation of IBIT's last 20 daily returns. When
  Bitcoin gets violent, exposure shrinks automatically; the rest is cash.
  Backtest 2018-04..2026-09 (monthly rebalance): CAGR +21.3%, max DD −20.4%,
  worst week −11.7%; 2022+ unseen: CAGR +20.3%, DD −13.6%. (Previous 70/30
  without scaling: CAGR +24.0%, max DD −23.9%, worst week −14.2%; 2022+
  CAGR +19.1%, DD −13.1%.)
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

## Hard rules
- Never deposit to or withdraw from this account, or move money in or out
  of it in any way (user's standing instruction, 2026-09-27).
- No options, no margin, no leverage, no shorting, no symbols other than SPY and IBIT, no
  discretionary trades. Changing these requires the user's say-so.
- Any rule change must first pass a backtest on data it was not tuned on and
  be written here with the evidence.
- If an order fails or anything looks wrong, do nothing and tell the user.

## Improvement process (goal: maximise long-run growth without risk of ruin)
Monthly review (1st of each month):
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
