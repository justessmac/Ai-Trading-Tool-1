import numpy as np
import pandas as pd

from tradingbot.research import mean_reversion as mr
from tradingbot.research import options_sim as opt
from tradingbot.research.stats import Criteria, passes, trade_stats, wilson_interval


def _daily(n=1500, seed=0, drift=0.0003, vol=0.012):
    rng = np.random.default_rng(seed)
    close = 100 * np.exp(np.cumsum(drift + vol * rng.standard_normal(n)))
    open_ = close * np.exp(0.003 * rng.standard_normal(n))
    high = np.maximum(open_, close) * (1 + np.abs(0.004 * rng.standard_normal(n)))
    low = np.minimum(open_, close) * (1 - np.abs(0.004 * rng.standard_normal(n)))
    idx = pd.bdate_range("2005-01-03", periods=n)
    return pd.DataFrame({"open": open_, "high": high, "low": low, "close": close}, index=idx)


def test_wilson_interval_matches_known_value():
    lo, hi = wilson_interval(850, 1000)
    assert abs(lo - 0.8265) < 1e-3 and abs(hi - 0.8708) < 1e-3


def test_trade_stats_basic():
    t = pd.DataFrame({"ret": [0.01] * 9 + [-0.05], "exit_date": pd.bdate_range("2020-01-01", periods=10)})
    s = trade_stats(t)
    assert s.n == 10 and abs(s.win_rate - 0.9) < 1e-12
    assert abs(s.expectancy - 0.004) < 1e-12
    assert abs(s.profit_factor - 0.09 / 0.05) < 1e-12


def test_passes_rejects_low_trade_count():
    t = pd.DataFrame({"ret": [0.01] * 95 + [-0.02] * 5, "exit_date": pd.bdate_range("2020-01-01", periods=100)})
    s = trade_stats(t)
    ok, why = passes(s, s, s, Criteria())
    assert not ok and "trades" in why


def test_mean_reversion_trades_enter_after_signal_day():
    d = mr.prepare(_daily())
    cfg = mr.Config("rsi2", (("th", 10), ("exit", "sma5"), ("trend", False), ("stop", None), ("max_hold", 10)))
    entry, _ = mr.signals(d, cfg)
    trades = mr.simulate(d, cfg, 0.0005, "X")
    assert trades
    signal_days = set(d.index[entry.to_numpy()])
    for tr in trades:
        prev_day = d.index[d.index.get_loc(tr["entry_date"]) - 1]
        assert prev_day in signal_days  # filled on the bar AFTER the signal
        assert tr["exit_date"] > tr["entry_date"]


def test_stop_loss_caps_loss_absent_gaps():
    d = mr.prepare(_daily(seed=3, vol=0.02))
    cfg = mr.Config("rsi2", (("th", 25), ("exit", "sma5"), ("trend", False), ("stop", 0.03), ("max_hold", 20)))
    trades = pd.DataFrame(mr.simulate(d, cfg, 0.0, "X"))
    # Only a gap through the stop can lose more than the stop.
    assert trades["ret"].min() > -0.10


def test_mr_grid_labels_unique():
    labels = [c.label() for c in mr.grid()]
    assert len(labels) == len(set(labels))


def test_bs_put_call_parity():
    S, K, T, r, q, v = 100.0, 95.0, 0.25, 0.03, 0.015, 0.2
    c = opt.bs_price(S, K, T, r, q, v, "call")
    p = opt.bs_price(S, K, T, r, q, v, "put")
    assert abs((c - p) - (S * np.exp(-q * T) - K * np.exp(-r * T))) < 1e-9


def test_strike_for_delta_is_otm_and_ordered():
    k16 = opt.strike_for_delta(400, 45 / 365, 0.03, 18, 0.16, "put")
    k05 = opt.strike_for_delta(400, 45 / 365, 0.03, 18, 0.05, "put")
    assert k05 < k16 < 400


def test_options_simulation_runs_on_synthetic_data():
    spy = _daily(n=800)
    vix = pd.Series(18.0, index=spy.index)
    rates = pd.Series(0.02, index=spy.index)
    cfg = opt.OptConfig("put_spread", 0.16, 0.05, 45, 0.5, 2.0, 21, "none")
    trades = pd.DataFrame(opt.simulate(spy, vix, rates, cfg))
    assert len(trades) > 50
    # A defined-risk spread can never lose more than its max risk (plus exit costs).
    assert trades["ret"].min() > -1.1


def test_repair_fixes_bad_run_and_unadjusted_split_but_keeps_real_crash():
    from tradingbot.research.import_robinhood import repair_price_jumps

    d = _daily(n=300, seed=5)
    truth = d.copy()
    d.iloc[100:102, :4] *= 2.0  # bad run quoted at 2x, snaps back
    d.iloc[:200, :4] *= 4.0  # unadjusted 1:4 reverse split on bar 200 (4x before)
    d.iloc[250:, :4] *= 0.8  # genuine -20% crash that persists: must be kept
    truth.iloc[250:, :4] *= 0.8
    fixed, log = repair_price_jumps(d)
    assert len(log) == 2
    ratio = (fixed["close"] / truth["close"]).round(6)
    assert ratio.nunique() == 1  # returns identical to the truth everywhere


def test_index_spike_repair_fixes_bad_bar_but_keeps_real_spike():
    from tradingbot.research.import_robinhood import repair_index_spikes

    idx = pd.bdate_range("2020-01-01", periods=8)
    close = [15.0, 15.5, 60.0, 15.2, 15.0, 37.0, 30.0, 25.0]  # bad bar, then a real decaying spike
    df = pd.DataFrame({"open": close, "high": close, "low": close, "close": close}, index=idx)
    fixed, log = repair_index_spikes(df)
    assert len(log) == 1
    assert abs(fixed["close"].iat[2] - 15.35) < 1e-9
    assert fixed["close"].iat[5] == 37.0
