import numpy as np
import pandas as pd

from tradingbot.indicators import atr, bollinger_bands, ema, rsi


def _series(values):
    return pd.Series(values, index=pd.date_range("2024-01-01", periods=len(values), freq="1h", tz="UTC"))


def test_ema_converges_to_constant():
    s = _series([100.0] * 50)
    out = ema(s, 10)
    assert np.isclose(out.iloc[-1], 100.0)


def test_ema_reacts_faster_than_longer_period():
    s = _series(list(np.linspace(100, 200, 60)))
    fast = ema(s, 5)
    slow = ema(s, 30)
    assert fast.iloc[-1] > slow.iloc[-1]  # rising series: fast EMA leads


def test_rsi_bounds():
    rng = np.random.default_rng(0)
    s = _series(100 + np.cumsum(rng.standard_normal(200)))
    out = rsi(s, 14).dropna()
    assert (out >= 0).all() and (out <= 100).all()


def test_rsi_high_on_pure_uptrend():
    s = _series(list(np.linspace(100, 200, 40)))
    out = rsi(s, 14).dropna()
    assert out.iloc[-1] > 90


def test_bollinger_mid_equals_sma():
    s = _series(list(np.linspace(100, 150, 40)))
    bb = bollinger_bands(s, period=20, num_std=2)
    sma = s.rolling(20).mean()
    pd.testing.assert_series_equal(bb["bb_mid"], sma, check_names=False)
    assert (bb["bb_upper"].dropna() >= bb["bb_mid"].dropna()).all()
    assert (bb["bb_lower"].dropna() <= bb["bb_mid"].dropna()).all()


def test_atr_nonnegative():
    idx = pd.date_range("2024-01-01", periods=30, freq="1h", tz="UTC")
    rng = np.random.default_rng(1)
    close = 100 + np.cumsum(rng.standard_normal(30))
    high = close + np.abs(rng.standard_normal(30))
    low = close - np.abs(rng.standard_normal(30))
    df = pd.DataFrame({"open": close, "high": high, "low": low, "close": close}, index=idx)
    out = atr(df, 14).dropna()
    assert (out >= 0).all()
