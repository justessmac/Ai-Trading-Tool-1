"""Multi-timeframe mean-reversion pullback strategy.

Signal detection happens on the lower timeframe (`signal_tf`): RSI dipping
into oversold/overbought territory together with a touch of the Bollinger
Band extreme. Trend context and trade execution happen on the higher
timeframe (`exec_tf`): an EMA fast/slow filter defines the prevailing
trend, and a pullback signal is only actionable if at least one qualifying
lower-timeframe pullback occurred during the most recently *completed*
higher-timeframe bar and that bar confirms the trend.

This module is pure/vectorized: it returns one row per `exec_tf` bar with
the trend state, ATR, and boolean entry candidates. It does not decide
whether to actually open a trade -- that depends on portfolio state
(already in a position, available equity, etc.) and is handled by
`backtest.py`, which also applies the one-bar execution delay to avoid
lookahead (a candidate flagged as of bar t's close is only actionable at
bar t+1's open).
"""
from __future__ import annotations

import pandas as pd

from tradingbot.config import StrategyConfig
from tradingbot.indicators import atr as atr_indicator
from tradingbot.indicators import bollinger_bands, ema, rsi


def _resample_any(signal_bool: pd.Series, exec_index: pd.DatetimeIndex) -> pd.Series:
    """Roll up a boolean signal-timeframe series to the exec-timeframe buckets."""
    if len(exec_index) < 2:
        return pd.Series(False, index=exec_index)
    freq = exec_index[1] - exec_index[0]
    rolled = signal_bool.resample(freq, label="right", closed="right").max().fillna(False)
    return rolled.reindex(exec_index, fill_value=False).astype(bool)


def generate_signals(
    signal_df: pd.DataFrame, exec_df: pd.DataFrame, config: StrategyConfig
) -> pd.DataFrame:
    exec_df = exec_df.copy()
    exec_df["ema_fast"] = ema(exec_df["close"], config.ema_fast)
    exec_df["ema_slow"] = ema(exec_df["close"], config.ema_slow)
    exec_df["atr"] = atr_indicator(exec_df, config.atr_period)

    uptrend = (exec_df["close"] > exec_df["ema_slow"]) & (exec_df["ema_fast"] > exec_df["ema_slow"])
    downtrend = (exec_df["close"] < exec_df["ema_slow"]) & (exec_df["ema_fast"] < exec_df["ema_slow"])
    exec_df["trend"] = "flat"
    exec_df.loc[uptrend, "trend"] = "up"
    exec_df.loc[downtrend, "trend"] = "down"

    sig = signal_df.copy()
    sig["rsi"] = rsi(sig["close"], config.rsi_period)
    bb = bollinger_bands(sig["close"], config.bb_period, config.bb_std)
    sig = sig.join(bb)

    pullback_long = (sig["rsi"] < config.rsi_oversold) & (sig["close"] <= sig["bb_lower"])
    pullback_short = (sig["rsi"] > config.rsi_overbought) & (sig["close"] >= sig["bb_upper"])

    exec_df["pullback_long"] = _resample_any(pullback_long, exec_df.index)
    exec_df["pullback_short"] = _resample_any(pullback_short, exec_df.index)

    exec_df["long_candidate"] = (exec_df["trend"] == "up") & exec_df["pullback_long"]
    exec_df["short_candidate"] = (
        config.allow_short & (exec_df["trend"] == "down") & exec_df["pullback_short"]
    )

    exec_df["stop_distance"] = exec_df["atr"] * config.atr_stop_multiple
    exec_df["target_distance"] = exec_df["stop_distance"] * config.reward_risk_ratio

    warmup = max(config.ema_slow, config.atr_period)
    exec_df.iloc[:warmup, exec_df.columns.get_indexer(["long_candidate", "short_candidate"])] = False

    return exec_df
