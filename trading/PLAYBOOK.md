# Live playbook: Agentic account (••••0819)

Goal: compound the account without risking ruin until it is large enough for
the SPY put-spread strategy (~$47k+). Deposits, not trading, will do most of
that; the job here is to never blow up and to capture market growth.

## Strategy: SPY 200-day trend filter (2% band)
Published rule (Faber 2007), not fitted here. 2000–2026 check on this repo's
data: CAGR +8.2%, max drawdown −19% (buy & hold: +8.0%, −55%), ~2 switches/yr.

- Signal checked each weekday at ~15:48 ET using the live SPY price vs the
  200-day SMA of daily closes (unadjusted).
- If SPY > SMA × 1.02 → be fully in SPY (fractional, dollar-based market buy
  of available buying power minus $2).
- If SPY < SMA × 0.98 → sell all SPY, hold cash.
- Between the bands → do nothing (keeps the current state).
- New deposits: invest them only while the signal is "in".

## Hard rules
- No options, no margin, no leverage, no shorting, no other symbols, no
  discretionary trades. Changing these requires the user's say-so.
- Any rule change must first pass a backtest on data it was not tuned on and
  be written here with the evidence.
- If an order fails or anything looks wrong, do nothing and tell the user.

## Journal
See `trading/journal.md` (one line per check that trades or changes state).
