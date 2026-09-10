import pandas as pd

from tradingbot.backtest import run_backtest
from tradingbot.config import StrategyConfig


def _bar(o, h, l, c):
    return {"open": o, "high": h, "low": l, "close": c}


def test_long_trade_hits_target():
    # Bar 0: warmup, no candidate. Bar 1: candidate flagged at close.
    # Bar 2: entry at open, then rallies to hit target.
    idx = pd.date_range("2024-01-01", periods=4, freq="1h", tz="UTC")
    rows = [
        {**_bar(100, 101, 99, 100), "long_candidate": False, "short_candidate": False,
         "stop_distance": 2.0, "target_distance": 3.0},
        {**_bar(100, 101, 99, 100), "long_candidate": True, "short_candidate": False,
         "stop_distance": 2.0, "target_distance": 3.0},
        {**_bar(100, 104, 99.5, 103), "long_candidate": False, "short_candidate": False,
         "stop_distance": 2.0, "target_distance": 3.0},
        {**_bar(103, 105, 102, 104), "long_candidate": False, "short_candidate": False,
         "stop_distance": 2.0, "target_distance": 3.0},
    ]
    df = pd.DataFrame(rows, index=idx)
    config = StrategyConfig(fee_bps=0, slippage_bps=0, risk_per_trade_pct=0.01, max_holding_bars=100)

    trades, curve = run_backtest(df, config, "TEST/USDT")

    assert len(trades) == 1
    t = trades[0]
    assert t.direction == "long"
    assert t.exit_reason == "target"
    assert t.pnl > 0
    assert curve.iloc[-1] > config.initial_equity


def test_long_trade_hits_stop():
    idx = pd.date_range("2024-01-01", periods=4, freq="1h", tz="UTC")
    rows = [
        {**_bar(100, 101, 99, 100), "long_candidate": False, "short_candidate": False,
         "stop_distance": 2.0, "target_distance": 3.0},
        {**_bar(100, 101, 99, 100), "long_candidate": True, "short_candidate": False,
         "stop_distance": 2.0, "target_distance": 3.0},
        {**_bar(100, 100.5, 97, 98), "long_candidate": False, "short_candidate": False,
         "stop_distance": 2.0, "target_distance": 3.0},
        {**_bar(98, 99, 97, 98), "long_candidate": False, "short_candidate": False,
         "stop_distance": 2.0, "target_distance": 3.0},
    ]
    df = pd.DataFrame(rows, index=idx)
    config = StrategyConfig(fee_bps=0, slippage_bps=0, risk_per_trade_pct=0.01, max_holding_bars=100)

    trades, curve = run_backtest(df, config, "TEST/USDT")

    assert len(trades) == 1
    t = trades[0]
    assert t.exit_reason == "stop"
    assert t.pnl < 0
    assert curve.iloc[-1] < config.initial_equity


def test_risk_per_trade_bounds_loss():
    idx = pd.date_range("2024-01-01", periods=4, freq="1h", tz="UTC")
    rows = [
        {**_bar(100, 101, 99, 100), "long_candidate": False, "short_candidate": False,
         "stop_distance": 2.0, "target_distance": 3.0},
        {**_bar(100, 101, 99, 100), "long_candidate": True, "short_candidate": False,
         "stop_distance": 2.0, "target_distance": 3.0},
        {**_bar(100, 100.5, 97, 98), "long_candidate": False, "short_candidate": False,
         "stop_distance": 2.0, "target_distance": 3.0},
        {**_bar(98, 99, 97, 98), "long_candidate": False, "short_candidate": False,
         "stop_distance": 2.0, "target_distance": 3.0},
    ]
    df = pd.DataFrame(rows, index=idx)
    risk_pct = 0.01
    config = StrategyConfig(fee_bps=0, slippage_bps=0, risk_per_trade_pct=risk_pct, max_holding_bars=100)

    trades, curve = run_backtest(df, config, "TEST/USDT")

    loss_pct = abs(trades[0].pnl) / config.initial_equity
    assert loss_pct <= risk_pct * 1.01  # small tolerance for stop != exact fill in degenerate case


def test_no_candidates_means_no_trades():
    idx = pd.date_range("2024-01-01", periods=10, freq="1h", tz="UTC")
    rows = [
        {**_bar(100, 101, 99, 100), "long_candidate": False, "short_candidate": False,
         "stop_distance": 2.0, "target_distance": 3.0}
        for _ in range(10)
    ]
    df = pd.DataFrame(rows, index=idx)
    config = StrategyConfig()

    trades, curve = run_backtest(df, config, "TEST/USDT")

    assert trades == []
    assert (curve == config.initial_equity).all()
