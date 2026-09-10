"""Bar-by-bar backtest engine, operating on the exec_tf bars produced by
`strategy.generate_signals`.

Execution model:
  - A candidate flagged as of bar t's close is only actionable at bar
    t+1's open (one-bar delay -- no lookahead).
  - Stops/targets are checked against each bar's high/low; if both would
    have been hit in the same bar, the stop is assumed to fill first
    (conservative).
  - Fees (`fee_bps`) are charged on both entry and exit notional.
    Slippage (`slippage_bps`) worsens every fill price.
  - Only one position per symbol at a time.
"""
from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from tradingbot.config import StrategyConfig
from tradingbot.risk import position_size


@dataclass
class Trade:
    symbol: str
    direction: str  # "long" or "short"
    entry_time: pd.Timestamp
    entry_price: float
    qty: float
    stop: float
    target: float
    risk_amount: float
    exit_time: pd.Timestamp | None = None
    exit_price: float | None = None
    exit_reason: str | None = None
    pnl: float | None = None
    r_multiple: float | None = None


def _slippage_adjust(price: float, is_buy: bool, slippage_bps: float) -> float:
    factor = slippage_bps / 10_000
    return price * (1 + factor) if is_buy else price * (1 - factor)


def run_backtest(exec_df: pd.DataFrame, config: StrategyConfig, symbol: str):
    equity = config.initial_equity
    position: Trade | None = None
    holding_bars = 0
    trades: list[Trade] = []
    equity_curve = []

    fee_rate = config.fee_bps / 10_000

    for i in range(1, len(exec_df)):
        row = exec_df.iloc[i]
        prev = exec_df.iloc[i - 1]
        ts = exec_df.index[i]

        if position is not None:
            holding_bars += 1
            is_long = position.direction == "long"
            hit_stop = row["low"] <= position.stop if is_long else row["high"] >= position.stop
            hit_target = row["high"] >= position.target if is_long else row["low"] <= position.target
            timed_out = holding_bars >= config.max_holding_bars

            exit_price = None
            reason = None
            if hit_stop:
                exit_price, reason = position.stop, "stop"
            elif hit_target:
                exit_price, reason = position.target, "target"
            elif timed_out:
                exit_price, reason = row["close"], "timeout"

            if exit_price is not None:
                exit_price = _slippage_adjust(exit_price, is_buy=not is_long, slippage_bps=config.slippage_bps)
                fee = exit_price * position.qty * fee_rate
                sign = 1 if is_long else -1
                pnl = (exit_price - position.entry_price) * position.qty * sign - fee
                equity += pnl
                position.exit_time = ts
                position.exit_price = exit_price
                position.exit_reason = reason
                position.pnl = pnl
                position.r_multiple = pnl / position.risk_amount if position.risk_amount else 0.0
                trades.append(position)
                position = None
                holding_bars = 0

        if position is None:
            if prev.get("long_candidate", False):
                entry_price = _slippage_adjust(row["open"], is_buy=True, slippage_bps=config.slippage_bps)
                stop = entry_price - prev["stop_distance"]
                target = entry_price + prev["target_distance"]
                qty = position_size(equity, config.risk_per_trade_pct, entry_price, stop)
                if qty > 0 and stop > 0:
                    fee = entry_price * qty * fee_rate
                    equity -= fee
                    position = Trade(
                        symbol=symbol,
                        direction="long",
                        entry_time=ts,
                        entry_price=entry_price,
                        qty=qty,
                        stop=stop,
                        target=target,
                        risk_amount=abs(entry_price - stop) * qty,
                    )
                    holding_bars = 0
            elif prev.get("short_candidate", False):
                entry_price = _slippage_adjust(row["open"], is_buy=False, slippage_bps=config.slippage_bps)
                stop = entry_price + prev["stop_distance"]
                target = entry_price - prev["target_distance"]
                qty = position_size(equity, config.risk_per_trade_pct, entry_price, stop)
                if qty > 0 and target > 0:
                    fee = entry_price * qty * fee_rate
                    equity -= fee
                    position = Trade(
                        symbol=symbol,
                        direction="short",
                        entry_time=ts,
                        entry_price=entry_price,
                        qty=qty,
                        stop=stop,
                        target=target,
                        risk_amount=abs(entry_price - stop) * qty,
                    )
                    holding_bars = 0

        if position is not None:
            sign = 1 if position.direction == "long" else -1
            unrealized = (row["close"] - position.entry_price) * position.qty * sign
            equity_curve.append((ts, equity + unrealized))
        else:
            equity_curve.append((ts, equity))

    # Force-close any position still open at the end of the data
    if position is not None:
        last_row = exec_df.iloc[-1]
        is_long = position.direction == "long"
        exit_price = _slippage_adjust(last_row["close"], is_buy=not is_long, slippage_bps=config.slippage_bps)
        fee = exit_price * position.qty * fee_rate
        sign = 1 if is_long else -1
        pnl = (exit_price - position.entry_price) * position.qty * sign - fee
        equity += pnl
        position.exit_time = exec_df.index[-1]
        position.exit_price = exit_price
        position.exit_reason = "end_of_data"
        position.pnl = pnl
        position.r_multiple = pnl / position.risk_amount if position.risk_amount else 0.0
        trades.append(position)
        if equity_curve:
            equity_curve[-1] = (equity_curve[-1][0], equity)

    curve = pd.Series(
        [v for _, v in equity_curve], index=[t for t, _ in equity_curve], name="equity"
    )
    return trades, curve
