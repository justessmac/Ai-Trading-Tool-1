# Weekly reviews

## Week ending 2026-10-03 (first week)
**Account:** $301.63, all cash. No equity, crypto or option positions. Contributed $250.00 (deposits.csv); pending deposits $0.
**Trading return (time-weighted, deposits excluded):** week +20.7%, since inception +20.7% ($250.00 -> $301.63, +$51.63).
- Benchmarks, Fri 9/25 close -> Fri 10/2 close: SPY -0.2%, IBIT +0.3%.
- P&L by trade: NKE Oct 9 $33 puts +$51.68 (bought 4 @ $0.56, sold @ $0.69). SPY round trip -$0.33 (765.21 -> 763.19). IBIT +$0.32 (47.14 -> 47.41). BTC $1 test about -$0.04.

**Mode:** user override on 10/01 put the account in all-in long-options mode through 10/15 (target $10,000). The stock/crypto strategies are suspended, so the signals below are for reference only.

| Signal | Value | State |
|---|---|---|
| SPY vs 200-day SMA | $769.64 vs $720.47 | +6.8%, above the band (in) |
| IBIT vs 100-day SMA | $47.73 vs $39.96 | +19.4% (trend in) |
| IBIT vol20 | 47.5% annualised | |
| IBIT RSI(2) | 55.5 | no swing; none open |

**Rule check:**
- 9/28 SPY/IBIT buys and 10/01 sales: followed the playbook and the user's override. Recorded in trades.csv; fills match the broker.
- NKE: research note present.
  - Entry: the $0.53 limit sat unfilled for 24 minutes; re-bought at the $0.56 ask, about $12 extra. The new buy-at-the-ask rule fixes this.
  - Exit at $0.69 (+23%), while the opening bid was $1.21 (+135%). About $208 lost to a rule conflict ("no trades in the first minutes" vs "sell the peak"). Fixed by the user-approved SELL AT THE OPEN rule for earnings plays, which the 9:31 routine now runs first.
- Process gaps found and fixed:
  - The daily-check routine lacked the strategies adopted 10/01. It is disabled now and must be rewritten from the playbook when options mode ends.
  - Scanners searched stock volume instead of option liquidity. The meme scan now filters on option volume, price $3-80.
  - The earnings shortlist lived only in notes. New routine trig_01NWVU5i7zXvppgBQFpLnK43 runs at 14:12 ET.
  - Peak-watch one-offs fired after the exit. The meme scan now disables leftovers.
- Open item for the user: the $250 deposit that showed as pending earlier in the week no longer appears in pending_deposits and has not landed. The user was asked to check the Robinhood app.
- No rule changes in this review (all changes above were made earlier in the week with user approval or as process fixes).
