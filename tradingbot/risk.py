"""Position sizing."""
from __future__ import annotations


def position_size(equity: float, risk_pct: float, entry_price: float, stop_price: float) -> float:
    """Fixed-fractional sizing: risk `risk_pct` of equity on the stop distance.

    Returns a quantity (units of the asset), clamped so the position's
    notional value never exceeds available equity (no leverage assumed).
    """
    per_unit_risk = abs(entry_price - stop_price)
    if per_unit_risk <= 0 or equity <= 0:
        return 0.0
    risk_amount = equity * risk_pct
    qty = risk_amount / per_unit_risk
    max_qty_by_equity = equity / entry_price
    return max(0.0, min(qty, max_qty_by_equity))
