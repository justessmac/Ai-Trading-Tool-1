# Trade records: Agentic account (••••0819)

Every order the bot places is recorded here and pushed to GitHub
(branch `claude/serene-newton-kcj7hk`) in the same run, so records
survive the cloud session ending.

- `trades.csv`: one row per order, including rejected or failed ones.
  - `sleeve`: `spy`, `ibit_trend` or `ibit_swing`
  - `reason`: the playbook rule that fired, e.g. "SPY > SMA200×1.02"
  - `signal_values`: the numbers behind it, e.g. "SPY 771.30 / SMA200 718.45"
  - `state`: `filled`, `partially_filled`, `rejected`, `failed` or `cancelled`
- `YYYY/YYYY-MM-DD_<symbol>_<side>.json`: the raw order details returned by
  Robinhood for each trade, including order id, fills and fees.

Robinhood also keeps its own permanent order history; the order id links
the two.
