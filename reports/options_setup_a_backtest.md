# Options Setup A: SPY dip call debit spread (real option prices)

Date: 2026-09-29. Verdict: **rejected** (fails after costs).

## Rule tested
- Signal: the adopted SPY dip-buy rule (RSI(2) < 10 and SPY > 200-day SMA;
  exit when RSI(2) > 70 or after 10 trading days). Entry and exit at the
  signal-day close.
- Instead of shares: buy 1 SPY call at K1 = SPY rounded to the nearest $1,
  sell 1 call at K1 + 1, standard monthly expiry nearest 30 DTE with at
  least 21 DTE (actual 21–52, mean 35).
- Prices: Robinhood daily option marks for the exact contracts (148
  contracts, all 74 trades priced, none dropped). Listing-day 0.01
  placeholders removed.
- Costs: "base" = $0.02 per leg per side slippage from the mark plus
  $0.04/contract/side fees (≈ $0.04 + $0.0016 per share each way); "2x" doubles
  the slippage; "mid" = no slippage (fees only), an unreachable best case.
- Return = exit value / entry cost − 1 (max loss = 100% of the debit).

## Results (74 trades, 2017-11 to 2026-09)

| Period | Trades | Cost case | Win rate | Avg/trade | Median | Worst | t |
|---|---|---|---|---|---|---|---|
| 2017–2021 (IS) | 33 | mid | 67% | +1.6% | +11.9% | −67% | 0.28 |
| | | base | 45% | −10.5% | −0.3% | −74% | −1.95 |
| | | 2x | 12% | −21.3% | −12.2% | −81% | −4.20 |
| 2022–2026 (OOS) | 41 | mid | 73% | +7.0% | +13.6% | −79% | 1.36 |
| | | base | 54% | −5.3% | +1.2% | −86% | −1.10 |
| | | 2x | 24% | −16.2% | −10.2% | −92% | −3.56 |
| All | 74 | base | 50% | −7.6% | +0.5% | −86% | −2.13 |

Average debit $0.64 (= $64 per spread). The same trades in SPY shares averaged
+0.58% each.

## Why it fails
- A 1-point-wide spread is cheap in dollars but expensive in percent: about
  $0.04/share of round-trip slippage is ~6% of the debit each way, ~12% per
  trade, more than the whole edge (+5–7% per trade at mid).
- The spread gives up upside beyond K1+1 and loses time value while SPY
  goes nowhere; the dip edge (+0.6% on SPY in ~6 days) is too small to pay
  for that.
- Even at mid prices the result is not statistically significant (t 1.2).

## What this means for the account
- Adoption test failed on both periods after costs → no options sleeve yet.
- The ~$70 idle cash keeps serving the SPY dip (Strategy 3) and IBIT swing.
- Next options candidates (see reports/Buying calls and puts small account.md):
  Setup B, a pre-earnings long straddle closed before the announcement, which
  trades implied-volatility run-up rather than direction; and wider/cheaper
  structures only once the account can absorb them.

Data: reports/options_setup_a_trades.csv (trade-level marks and returns;
contract list cached locally in data_cache/options/).
