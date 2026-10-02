"""Daily OHLCV loading for the strategy research harness.

Sources, tried in order, with an on-disk CSV cache under `data_cache/`:
  - Yahoo Finance chart API (split- and dividend-adjusted via adjclose)
  - Stooq CSV download (adjusted)

Both need outbound network access to the respective host. If neither is
reachable you can drop a CSV with columns date,open,high,low,close,volume
into `data_cache/<SYMBOL>.csv` (e.g. exported from another source) and it
will be used as-is.
"""
from __future__ import annotations

import io
import json
import time
import urllib.request
from pathlib import Path

import pandas as pd

CACHE_DIR = Path(__file__).resolve().parents[2] / "data_cache"

STOOQ_ALIASES = {"^VIX": "^vix", "^IRX": "^irx", "BTC-USD": "btcusd", "ETH-USD": "ethusd"}


def _http_get(url: str, timeout: float = 30.0) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def _fetch_yahoo(symbol: str, adjusted: bool = True) -> pd.DataFrame:
    url = (
        f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.request.quote(symbol)}"
        "?period1=0&period2=9999999999&interval=1d&events=div,splits&includeAdjustedClose=true"
    )
    payload = json.loads(_http_get(url))
    result = payload["chart"]["result"][0]
    quote = result["indicators"]["quote"][0]
    df = pd.DataFrame(
        {
            "open": quote["open"],
            "high": quote["high"],
            "low": quote["low"],
            "close": quote["close"],
            "volume": quote["volume"],
        },
        index=pd.to_datetime(result["timestamp"], unit="s").normalize(),
    )
    adj = result["indicators"].get("adjclose")
    if adj and adjusted:
        factor = pd.Series(adj[0]["adjclose"], index=df.index) / df["close"]
        for col in ("open", "high", "low", "close"):
            df[col] = df[col] * factor
    return df


def _fetch_stooq(symbol: str) -> pd.DataFrame:
    code = STOOQ_ALIASES.get(symbol, symbol.lower() + ".us")
    raw = _http_get(f"https://stooq.com/q/d/l/?s={code}&i=d")
    df = pd.read_csv(io.BytesIO(raw))
    df.columns = [c.lower() for c in df.columns]
    df["date"] = pd.to_datetime(df["date"])
    return df.set_index("date")[["open", "high", "low", "close"] + (["volume"] if "volume" in df else [])]


def _clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df[~df.index.duplicated(keep="last")].sort_index()
    df = df.dropna(subset=["open", "high", "low", "close"])
    df = df[(df["close"] > 0) & (df["open"] > 0)]
    df.index.name = "date"
    return df


def load_daily(symbol: str, *, refresh: bool = False, adjusted: bool = True) -> pd.DataFrame:
    """Return daily OHLCV for `symbol`, indexed by date. `adjusted=False`
    returns raw traded prices (needed to place option strikes); only the
    Yahoo source can provide those."""
    CACHE_DIR.mkdir(exist_ok=True)
    suffix = "" if adjusted else "_raw"
    path = CACHE_DIR / f"{symbol.replace('^', '_')}{suffix}.csv"
    if path.exists() and not refresh:
        return _clean(pd.read_csv(path, index_col="date", parse_dates=["date"]))

    errors = []
    sources = [lambda s: _fetch_yahoo(s, adjusted)] + ([_fetch_stooq] if adjusted else [])
    for fetch in sources:
        for attempt in range(3):
            try:
                df = _clean(fetch(symbol))
                if len(df) < 50:
                    raise ValueError(f"only {len(df)} rows")
                df.to_csv(path)
                return df
            except Exception as exc:  # network/parse errors: try next source
                errors.append(f"{getattr(fetch, '__name__', 'yahoo')}: {exc}")
                time.sleep(2**attempt)
    raise RuntimeError(f"Could not load {symbol}: " + "; ".join(errors[-2:]))


def load_many(symbols: list[str], *, refresh: bool = False) -> dict[str, pd.DataFrame]:
    out = {}
    for sym in symbols:
        try:
            out[sym] = load_daily(sym, refresh=refresh)
        except RuntimeError as exc:
            print(f"[data] skipping {sym}: {exc}")
    return out
