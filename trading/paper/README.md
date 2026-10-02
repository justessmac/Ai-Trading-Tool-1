# Paper trades: stocks in play (opening-range breaks)

Running summary, updated 2026-10-02. R = net return / risk to the stop. Costs 0.1% round trip.

| Side | Paper trades | Win rate | Avg R | Total R | t-stat |
|---|---|---|---|---|---|
| long | 4 | 50% | +0.03 | +0.10 | 0.03 |
| short | 8 | 50% | +0.21 | +1.65 | 0.50 |
| all | 12 | 50% | +0.15 | +1.75 | 0.42 |

Setups scanned: 14; entered: 12.
<!-- end summary -->

## What this is

Every morning scan (trading/scans/morning/) picks up to three "stocks in play" and writes an opening-range
setup for each. Nothing is traded; the daily research routine scores each setup from that day's 5-minute bars
with `python -m tradingbot.research.paper_scalps YYYY-MM-DD` (bars saved to data_cache/intraday/). The rules
are fixed in the routine and in the script's docstring. Do not tune them after seeing results.

- Short setups are paper only: Robinhood cannot short stock.
- Long setups count toward adoption. Real money needs 30+ long paper trades plus the playbook adoption
  test (IS/OOS backtest after costs) and a research note per trade.
- Win rate and t-stat on a handful of trades mean nothing. Microcap moves are fat-tailed and one day's
  sell-off can make every short look good.

## Log

- 2026-09-30: 3 short setups (LGHL, VBIO, BIYA), all entered, all held to the close: +1.02R, +1.62R, +1.76R.
  BIYA broke its OR high (to 3.17) before breaking down, so a trader using the usual "first side broken"
  rule would have skipped it. The routine's rule has no such filter, so it counts, but it is flagged in
  the log. LGHL had no trades in the 15:55 bar, so it exits at the last trade (4.95).
