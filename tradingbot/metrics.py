"""Performance metrics computed from an equity curve and trade log."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


def max_drawdown(equity_curve: pd.Series) -> float:
    running_max = equity_curve.cummax()
    drawdown = (equity_curve - running_max) / running_max
    return float(drawdown.min()) if len(drawdown) else 0.0


def sharpe_ratio(returns: pd.Series, periods_per_year: float) -> float:
    if returns.std(ddof=0) == 0 or len(returns) < 2:
        return 0.0
    return float(returns.mean() / returns.std(ddof=0) * np.sqrt(periods_per_year))


def sortino_ratio(returns: pd.Series, periods_per_year: float) -> float:
    downside = returns[returns < 0]
    if downside.std(ddof=0) == 0 or len(returns) < 2:
        return 0.0
    return float(returns.mean() / downside.std(ddof=0) * np.sqrt(periods_per_year))


@dataclass
class BacktestMetrics:
    total_return_pct: float
    cagr_pct: float
    max_drawdown_pct: float
    sharpe: float
    sortino: float
    num_trades: int
    win_rate_pct: float
    profit_factor: float
    avg_r_multiple: float

    def as_dict(self) -> dict:
        return self.__dict__


def compute_metrics(
    equity_curve: pd.Series, trades: list, periods_per_year: float
) -> BacktestMetrics:
    if len(equity_curve) < 2:
        return BacktestMetrics(0, 0, 0, 0, 0, 0, 0, 0, 0)

    returns = equity_curve.pct_change().dropna()
    total_return_pct = (equity_curve.iloc[-1] / equity_curve.iloc[0] - 1) * 100

    n_periods = len(equity_curve)
    years = n_periods / periods_per_year if periods_per_year else np.nan
    cagr_pct = (
        ((equity_curve.iloc[-1] / equity_curve.iloc[0]) ** (1 / years) - 1) * 100
        if years and years > 0 and equity_curve.iloc[0] > 0
        else 0.0
    )

    closed = [t for t in trades if t.exit_price is not None]
    wins = [t for t in closed if t.pnl is not None and t.pnl > 0]
    losses = [t for t in closed if t.pnl is not None and t.pnl <= 0]
    win_rate_pct = (len(wins) / len(closed) * 100) if closed else 0.0
    gross_profit = sum(t.pnl for t in wins)
    gross_loss = abs(sum(t.pnl for t in losses))
    profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else float("inf") if gross_profit > 0 else 0.0
    r_multiples = [t.r_multiple for t in closed if t.r_multiple is not None]
    avg_r_multiple = float(np.mean(r_multiples)) if r_multiples else 0.0

    return BacktestMetrics(
        total_return_pct=float(total_return_pct),
        cagr_pct=float(cagr_pct),
        max_drawdown_pct=float(max_drawdown(equity_curve) * 100),
        sharpe=sharpe_ratio(returns, periods_per_year),
        sortino=sortino_ratio(returns, periods_per_year),
        num_trades=len(closed),
        win_rate_pct=float(win_rate_pct),
        profit_factor=float(profit_factor),
        avg_r_multiple=avg_r_multiple,
    )
