"""Synthetic OHLCV generator.

This is NOT real market data. It exists so the strategy/backtest pipeline
can be exercised and unit-tested end-to-end inside a sandbox with no
outbound network access. It generates a 1-minute base series with
regime-switching drift (alternating trend/chop segments) plus a small
mean-reverting overlay, so pullback-style signals have something realistic
to trigger on. Resample it to any timeframe with `resample_ohlcv`.

Do not use results derived from this data as evidence a strategy is
profitable on real markets -- swap in `data/loader.py`'s real-data path
before drawing any conclusions.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

TIMEFRAME_RULES = {
    "1m": "1min",
    "5m": "5min",
    "15m": "15min",
    "1h": "1h",
    "4h": "4h",
    "1d": "1D",
}


def generate_minute_bars(
    symbol: str,
    periods_minutes: int,
    *,
    start: str = "2023-01-01",
    base_price: float = 100.0,
    annual_vol: float = 0.6,
    regime_length_minutes: int = 4 * 60,
    mean_reversion_strength: float = 0.02,
    seed: int | None = None,
) -> pd.DataFrame:
    """Generate `periods_minutes` of synthetic 1-minute OHLCV bars.

    Uses a log-price random walk with a drift that switches sign every
    `regime_length_minutes` bars (so higher-timeframe trends exist) plus an
    Ornstein-Uhlenbeck-style pull back toward a slow moving average (so
    lower-timeframe pullbacks exist within each trend).
    """
    rng = np.random.default_rng(seed if seed is not None else abs(hash(symbol)) % (2**32))

    dt = 1.0 / (365 * 24 * 60)  # one minute, in years
    sigma = annual_vol * np.sqrt(dt)

    n = periods_minutes
    # Regime drift: alternates sign, magnitude randomized a bit per regime
    n_regimes = n // regime_length_minutes + 2
    regime_signs = rng.choice([-1.0, 1.0], size=n_regimes)
    regime_mag = rng.uniform(0.15, 0.45, size=n_regimes) * annual_vol
    drift_per_regime = regime_signs * regime_mag
    drift = np.repeat(drift_per_regime, regime_length_minutes)[:n] * dt

    log_price = np.empty(n)
    log_price[0] = np.log(base_price)
    slow_ma = log_price[0]
    shocks = rng.standard_normal(n)
    for i in range(1, n):
        slow_ma = 0.999 * slow_ma + 0.001 * log_price[i - 1]
        reversion = mean_reversion_strength * (slow_ma - log_price[i - 1]) * dt * 1000
        log_price[i] = log_price[i - 1] + drift[i] + reversion + sigma * shocks[i]

    close = np.exp(log_price)
    open_ = np.empty(n)
    open_[0] = close[0]
    open_[1:] = close[:-1]

    intrabar_noise = np.abs(rng.standard_normal(n)) * sigma * close
    high = np.maximum(open_, close) + intrabar_noise
    low = np.minimum(open_, close) - intrabar_noise
    low = np.minimum(low, np.minimum(open_, close) * 0.9999)  # guard against inversion
    volume = rng.lognormal(mean=6.0, sigma=0.5, size=n)

    idx = pd.date_range(start=start, periods=n, freq="1min", tz="UTC")
    df = pd.DataFrame(
        {"open": open_, "high": high, "low": low, "close": close, "volume": volume},
        index=idx,
    )
    df.index.name = "timestamp"
    return df


def resample_ohlcv(df_1m: pd.DataFrame, timeframe: str) -> pd.DataFrame:
    rule = TIMEFRAME_RULES[timeframe]
    out = df_1m.resample(rule, label="right", closed="right").agg(
        {"open": "first", "high": "max", "low": "min", "close": "last", "volume": "sum"}
    )
    return out.dropna(subset=["open", "high", "low", "close"])
