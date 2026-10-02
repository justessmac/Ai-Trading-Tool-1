"""Trade-level statistics and the pass/fail acceptance test.

A strategy "passes" only if, on data it was NOT tuned on (out-of-sample):
  - it produced enough trades,
  - its win rate is >= the target,
  - it is net profitable after costs with statistical support
    (mean trade t-stat >= min_t and profit factor > 1), and
  - it stays profitable when costs are doubled.
"""
from __future__ import annotations

import math
from dataclasses import asdict, dataclass

import numpy as np
import pandas as pd


def wilson_interval(wins: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return (0.0, 0.0)
    p = wins / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return (centre - half, centre + half)


def max_drawdown(equity: pd.Series) -> float:
    if equity.empty:
        return 0.0
    peak = equity.cummax()
    return float(((equity - peak) / peak).min())


@dataclass
class TradeStats:
    n: int
    win_rate: float
    win_rate_lo95: float
    avg_win: float
    avg_loss: float
    payoff_ratio: float
    expectancy: float
    profit_factor: float
    t_stat: float
    worst_trade: float
    total_return: float
    max_drawdown: float
    cagr: float

    def as_dict(self) -> dict:
        return asdict(self)


def trade_stats(trades: pd.DataFrame, years: float | None = None) -> TradeStats:
    """`trades` needs columns `ret` (net fractional return on capital at risk)
    and `exit_date`. Portfolio curve assumes each trade is sized at `weight`
    (column, default 1) of equity, compounding in exit-date order."""
    if trades.empty:
        return TradeStats(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    r = trades["ret"].to_numpy(dtype=float)
    n = len(r)
    wins = r[r > 0]
    losses = r[r <= 0]
    lo, _ = wilson_interval(len(wins), n)
    avg_win = float(wins.mean()) if len(wins) else 0.0
    avg_loss = float(losses.mean()) if len(losses) else 0.0
    gross_loss = -losses.sum()
    pf = float(wins.sum() / gross_loss) if gross_loss > 0 else float("inf")
    sd = r.std(ddof=1) if n > 1 else 0.0
    t = float(r.mean() / (sd / math.sqrt(n))) if sd > 0 else 0.0

    w = trades["weight"].to_numpy(dtype=float) if "weight" in trades else np.ones(n)
    order = np.argsort(trades["exit_date"].to_numpy())
    equity = pd.Series(np.cumprod(1 + (r * w)[order]))
    total = float(equity.iloc[-1] - 1)
    cagr = float(equity.iloc[-1] ** (1 / years) - 1) if years and years > 0 and equity.iloc[-1] > 0 else 0.0
    return TradeStats(
        n=n,
        win_rate=len(wins) / n,
        win_rate_lo95=lo,
        avg_win=avg_win,
        avg_loss=avg_loss,
        payoff_ratio=abs(avg_win / avg_loss) if avg_loss else float("inf"),
        expectancy=float(r.mean()),
        profit_factor=pf,
        t_stat=t,
        worst_trade=float(r.min()),
        total_return=total,
        max_drawdown=max_drawdown(pd.concat([pd.Series([1.0]), equity])),
        cagr=cagr,
    )


@dataclass
class Criteria:
    min_trades_total: int = 1000
    min_trades_oos: int = 250
    min_win_rate: float = 0.85
    min_t: float = 2.0


def passes(is_stats: TradeStats, oos_stats: TradeStats, oos_stress: TradeStats, c: Criteria) -> tuple[bool, str]:
    reasons = []
    if is_stats.n + oos_stats.n < c.min_trades_total:
        reasons.append(f"trades {is_stats.n + oos_stats.n}<{c.min_trades_total}")
    if oos_stats.n < c.min_trades_oos:
        reasons.append(f"OOS trades {oos_stats.n}<{c.min_trades_oos}")
    for label, s in (("IS", is_stats), ("OOS", oos_stats)):
        if s.win_rate < c.min_win_rate:
            reasons.append(f"{label} win {s.win_rate:.1%}")
        if s.t_stat < c.min_t or s.profit_factor <= 1:
            reasons.append(f"{label} t={s.t_stat:.2f} PF={s.profit_factor:.2f}")
    if oos_stress.expectancy <= 0:
        reasons.append("OOS unprofitable at 2x costs")
    return (not reasons, "; ".join(reasons) or "PASS")
