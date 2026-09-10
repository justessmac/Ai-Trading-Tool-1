"""Central configuration for the multi-timeframe mean-reversion bot.

All tunable parameters live here so a run can be reproduced from one file.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class StrategyConfig:
    # Universe
    symbols: list[str] = field(default_factory=lambda: ["BTC/USDT", "ETH/USDT", "SOL/USDT"])

    # Timeframes: signals are detected on `signal_tf`, trend is judged and
    # orders are actually opened/managed on `exec_tf` (bar-close execution).
    signal_tf: str = "5m"
    exec_tf: str = "1h"

    # Trend filter (computed on exec_tf)
    ema_fast: int = 20
    ema_slow: int = 50

    # Pullback trigger (computed on signal_tf)
    rsi_period: int = 14
    rsi_oversold: float = 30.0
    rsi_overbought: float = 70.0
    bb_period: int = 20
    bb_std: float = 2.0

    # Volatility / risk (ATR computed on exec_tf)
    atr_period: int = 14
    atr_stop_multiple: float = 2.0
    reward_risk_ratio: float = 1.5  # target distance = reward_risk_ratio * stop distance
    max_holding_bars: int = 48  # exec_tf bars (48 * 1h = 2 days) before a forced timeout exit

    # Position sizing
    risk_per_trade_pct: float = 0.01  # fraction of equity risked per trade
    allow_short: bool = False  # spot-only by default; set True for perps

    # Costs (round-trip approximations, applied per fill)
    fee_bps: float = 4.0       # taker fee, basis points per fill
    slippage_bps: float = 2.0  # extra basis points per fill

    # Backtest
    initial_equity: float = 10_000.0
