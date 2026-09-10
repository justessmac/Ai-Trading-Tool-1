"""Pluggable OHLCV data loading.

`load_symbol_data` is the one function the rest of the bot calls. It
returns (signal_tf_df, exec_tf_df) for a symbol. The `source` argument
selects where the underlying 1-minute (or native) data comes from:

  - "synthetic": generated locally, no network required. Used for
    development/testing inside network-restricted environments. See
    `data/synthetic.py` for caveats -- this is NOT real market data.

  - "ccxt": pulls real historical OHLCV from an exchange via the `ccxt`
    library. Requires outbound network access to the exchange's public
    REST API, which this sandbox's network policy blocks -- run this
    path locally or in an environment with exchange access. Install with
    `pip install ccxt` (not in requirements.txt by default).

  - "trader_dev": placeholder for the trader-dev MCP server. Important:
    an MCP tool can only be called by the Claude agent turn itself, not
    from inside a plain Python process at runtime. To use trader-dev data
    here, fetch/export OHLCV via the MCP tool from a Claude session and
    save it as CSV (see `load_from_csv`), or have trader-dev expose a
    plain REST endpoint you can call from `fetch_ccxt_ohlcv`-style code.
"""
from __future__ import annotations

import pandas as pd

from tradingbot.data.synthetic import generate_minute_bars, resample_ohlcv


def load_symbol_data(
    symbol: str,
    signal_tf: str,
    exec_tf: str,
    *,
    source: str = "synthetic",
    periods_minutes: int = 60 * 24 * 120,  # 120 days of 1m bars
    seed: int | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    if source == "synthetic":
        base = generate_minute_bars(symbol, periods_minutes, seed=seed)
        signal_df = resample_ohlcv(base, signal_tf)
        exec_df = resample_ohlcv(base, exec_tf)
        return signal_df, exec_df
    if source == "ccxt":
        return fetch_ccxt_ohlcv(symbol, signal_tf, exec_tf)
    if source == "trader_dev":
        raise NotImplementedError(
            "trader-dev data must be fetched via the MCP tool from a Claude "
            "session (or a REST wrapper) and loaded with load_from_csv(); "
            "see the module docstring."
        )
    raise ValueError(f"Unknown data source: {source!r}")


def fetch_ccxt_ohlcv(
    symbol: str, signal_tf: str, exec_tf: str, *, exchange_id: str = "binance", limit: int = 1000
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Fetch real OHLCV via ccxt. Requires `pip install ccxt` and network access."""
    import ccxt  # local import: optional dependency

    exchange = getattr(ccxt, exchange_id)()

    def _fetch(tf: str) -> pd.DataFrame:
        raw = exchange.fetch_ohlcv(symbol, timeframe=tf, limit=limit)
        df = pd.DataFrame(raw, columns=["timestamp", "open", "high", "low", "close", "volume"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms", utc=True)
        return df.set_index("timestamp")

    return _fetch(signal_tf), _fetch(exec_tf)


def load_from_csv(path: str) -> pd.DataFrame:
    """Load OHLCV from a CSV with columns: timestamp,open,high,low,close,volume."""
    df = pd.read_csv(path, parse_dates=["timestamp"])
    return df.set_index("timestamp").sort_index()
