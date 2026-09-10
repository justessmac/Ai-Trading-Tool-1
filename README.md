# Multi-Timeframe Crypto Trading Bot (Research/Backtest Stage)

A backtestable, multi-timeframe crypto trading system: pullback signals are
detected on a **lower timeframe** (5m), trend context and trade execution
happen on a **higher timeframe** (1h). This repo is currently at the
**research/backtest stage only** — there is no live order execution wired
up yet, by design (see "Roadmap" below).

## Important: read this before trusting any numbers

No trading system "compounds wealth to the highest extreme" or guarantees
profit — any strategy claiming that is either untested or about to blow up
an account. What this repo gives you is a disciplined, honestly-evaluated
pipeline: strategy logic, realistic backtest mechanics (fees, slippage,
one-bar execution delay to avoid lookahead), and clear metrics. Treat
positive backtest results as a hypothesis to keep testing, not a result to
trade on.

The default data source is **synthetic** (`tradingbot/data/synthetic.py`)
— a locally-generated random walk with regime-switching drift, used only
to validate the pipeline runs correctly end-to-end. **Do not** interpret
synthetic-data backtest results as evidence of real-world edge. Before
trusting any performance numbers, swap in real historical data (see
"Using real data" below) and expect to iterate on strategy parameters.

## Strategy logic

1. **Trend filter (1h, `exec_tf`)** — EMA(20) vs EMA(50): price above a
   rising EMA(50) with EMA(20) > EMA(50) = uptrend; symmetric for
   downtrend. Flat/no-trend otherwise.
2. **Pullback trigger (5m, `signal_tf`)** — RSI(14) < 30 together with
   price touching the lower Bollinger Band(20, 2) = an oversold pullback.
3. **Entry** — if any qualifying 5m pullback occurred during the most
   recently *completed* 1h bar, and that 1h bar confirms an uptrend, a
   long is opened at the next 1h bar's open. (Shorts are symmetric and
   controlled by `config.allow_short`, off by default since the current
   universe defaults to spot.)
4. **Stops/targets** — stop-loss is `atr_stop_multiple x ATR(14, 1h)`
   below entry; target is `reward_risk_ratio x stop distance` above entry.
   A `max_holding_bars` timeout forces an exit if neither is hit.
5. **Position sizing** — fixed-fractional: risk `risk_per_trade_pct` of
   current equity on the stop distance (`tradingbot/risk.py`).

All parameters live in `tradingbot/config.py`.

## Running it

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

python -m pytest tradingbot/tests            # unit tests
python -m tradingbot.run_backtest             # synthetic-data backtest
```

Output (per-symbol trade logs, equity curves, and a combined portfolio
equity plot) is written to `output/`.

## Using real data

This bot's data layer (`tradingbot/data/loader.py`) is pluggable via a
`source` argument:

- `source="synthetic"` (default) — no network needed, pipeline validation only.
- `source="ccxt"` — real historical OHLCV via the [ccxt](https://github.com/ccxt/ccxt)
  library (`pip install ccxt`). Requires outbound network access to the
  exchange's public REST API. **This sandbox's network policy blocks
  direct calls to exchange APIs**, so run this path locally or in an
  environment with exchange access:
  ```bash
  python -m tradingbot.run_backtest --source ccxt
  ```
- `source="trader_dev"` — placeholder for the `trader-dev` MCP server you
  configured. Important: an MCP tool can only be invoked by a Claude
  agent turn, not from inside a plain Python process at runtime. To
  backtest on trader-dev data, either (a) have a Claude session pull data
  via the MCP tool and export it to CSV, then load it with
  `tradingbot.data.loader.load_from_csv`, or (b) if trader-dev exposes a
  plain REST endpoint, add a fetch function alongside `fetch_ccxt_ohlcv`
  in `loader.py`. You'll also need to finish authorizing `trader-dev`
  (`claude mcp` / `/mcp` in an interactive session) before its tools are
  usable at all.

## Roadmap to a live bot (do this in order — do not skip steps)

1. **Backtest on real historical data** across multiple market regimes
   (bull, bear, chop) and multiple assets — not just the synthetic path.
2. **Walk-forward validate**: fit parameters on one period, test
   out-of-sample on the next, roll forward. A strategy that only works on
   the period it was tuned on is overfit, not profitable.
3. **Paper trade** against live market data with simulated fills for at
   least several weeks, comparing realized slippage/fees to your backtest
   assumptions.
4. **Live trading with real capital** — start with a small amount you can
   afford to lose entirely, with hard daily-loss and max-drawdown kill
   switches, before scaling up.

This repo currently covers step 1's tooling. Steps 2-4 are meaningful
additional work (a walk-forward harness, a paper-trading executor against
a live feed, and a live order-execution layer with kill switches) — happy
to build any of those next once you've told me which real data source and
exchange/broker you want them wired to.

## Layout

```
tradingbot/
  config.py       # all tunable parameters
  indicators.py   # EMA, RSI, Bollinger Bands, ATR
  data/
    synthetic.py  # local synthetic OHLCV generator (dev/test only)
    loader.py     # pluggable data source: synthetic / ccxt / trader_dev
  strategy.py     # multi-timeframe signal generation
  risk.py         # fixed-fractional position sizing
  backtest.py     # bar-by-bar backtest engine (fees, slippage, no lookahead)
  metrics.py      # Sharpe, Sortino, max drawdown, win rate, profit factor
  run_backtest.py # CLI entry point
  tests/          # pytest unit tests
```
