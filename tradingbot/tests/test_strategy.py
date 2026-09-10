import numpy as np
import pandas as pd

from tradingbot.config import StrategyConfig
from tradingbot.strategy import generate_signals


def _make_exec_df(n=120, start_price=100.0, trend=0.5, seed=0):
    rng = np.random.default_rng(seed)
    idx = pd.date_range("2024-01-01", periods=n, freq="1h", tz="UTC")
    close = start_price + np.cumsum(np.full(n, trend)) + rng.standard_normal(n) * 0.1
    high = close + 0.2
    low = close - 0.2
    open_ = np.concatenate([[close[0]], close[:-1]])
    return pd.DataFrame({"open": open_, "high": high, "low": low, "close": close}, index=idx)


def _make_signal_df(exec_df, seed=0):
    # 5-minute bars nested inside each 1h exec bar
    idx = pd.date_range(exec_df.index[0] - pd.Timedelta(hours=1), exec_df.index[-1], freq="5min", tz="UTC")
    rng = np.random.default_rng(seed)
    close = np.interp(
        np.arange(len(idx)),
        np.linspace(0, len(idx) - 1, len(exec_df)),
        exec_df["close"].values,
    ) + rng.standard_normal(len(idx)) * 0.05
    high = close + 0.05
    low = close - 0.05
    open_ = np.concatenate([[close[0]], close[:-1]])
    return pd.DataFrame({"open": open_, "high": high, "low": low, "close": close}, index=idx)


def test_uptrend_is_detected():
    exec_df = _make_exec_df(trend=0.5)
    signal_df = _make_signal_df(exec_df)
    config = StrategyConfig(ema_fast=5, ema_slow=15, atr_period=10)
    out = generate_signals(signal_df, exec_df, config)
    assert (out["trend"].iloc[40:] == "up").mean() > 0.8


def test_downtrend_is_detected():
    exec_df = _make_exec_df(trend=-0.5)
    signal_df = _make_signal_df(exec_df)
    config = StrategyConfig(ema_fast=5, ema_slow=15, atr_period=10)
    out = generate_signals(signal_df, exec_df, config)
    assert (out["trend"].iloc[40:] == "down").mean() > 0.8


def test_no_short_candidates_when_shorting_disabled():
    exec_df = _make_exec_df(trend=-0.5)
    signal_df = _make_signal_df(exec_df)
    config = StrategyConfig(ema_fast=5, ema_slow=15, atr_period=10, allow_short=False)
    out = generate_signals(signal_df, exec_df, config)
    assert not out["short_candidate"].any()


def test_warmup_period_has_no_candidates():
    exec_df = _make_exec_df(trend=0.5)
    signal_df = _make_signal_df(exec_df)
    config = StrategyConfig(ema_fast=5, ema_slow=15, atr_period=10)
    out = generate_signals(signal_df, exec_df, config)
    warmup = max(config.ema_slow, config.atr_period)
    assert not out["long_candidate"].iloc[:warmup].any()
    assert not out["short_candidate"].iloc[:warmup].any()


def test_long_candidate_requires_pullback_and_uptrend():
    exec_df = _make_exec_df(trend=0.5)
    signal_df = _make_signal_df(exec_df)
    config = StrategyConfig(ema_fast=5, ema_slow=15, atr_period=10)
    out = generate_signals(signal_df, exec_df, config)
    candidates = out[out["long_candidate"]]
    assert (candidates["trend"] == "up").all()
    assert (candidates["pullback_long"]).all()
