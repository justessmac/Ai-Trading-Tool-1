"""Core sleeve: SPY vs QQQ momentum rotation, on top of the 200-day trend filter.

Baseline (live Strategy 1): hold SPY when SPY > SMA200 x 1.02, cash when
< SMA200 x 0.98, otherwise keep the current state. Checked daily.

Candidates:
  qqq_trend      the same rule on QQQ instead of SPY.
  rotate_L       on the first trading day of each month pick whichever of
                 SPY/QQQ has the higher L-day return (L = 63, 126, 252); hold
                 it while the picked fund passes its own 2%-band SMA200 filter
                 (checked daily), cash otherwise.
  rotate_L_abs   as rotate_L, but cash also when the picked fund's L-day
                 return is <= 0 (dual momentum, Antonacci).

Signals use the day's close; the position earns the next day's return (live
orders go in at 15:48, so this is slightly conservative). Costs 0.03% per side
on every switch. Adjusted closes (dividends included). Cash earns 0.
Selection 2000-2014 (includes the QQQ -83% dot-com crash), confirmation 2015-2026.
Adoption needs higher CAGR in both periods and max drawdown no worse than -25%.

Usage: python -m tradingbot.research.core_rotation
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from tradingbot.research.data import load_daily

COST = 0.0003
IS_END = "2014-12-31"


def band_state(close: pd.Series, band: float = 0.02) -> pd.Series:
    sma = close.rolling(200).mean()
    state, out = False, []
    for c, s in zip(close.values, sma.values):
        if not np.isnan(s):
            if c > s * (1 + band):
                state = True
            elif c < s * (1 - band):
                state = False
        out.append(state)
    return pd.Series(out, index=close.index)


def simulate(px: pd.DataFrame, holding: pd.Series) -> pd.Series:
    """holding: per day, the fund held after the close ('' = cash). Returns daily strategy returns."""
    rets = px.pct_change().shift(-1)  # return earned the next day
    r = pd.Series(0.0, index=px.index)
    for col in px.columns:
        r[holding == col] = rets[col][holding == col]
    changes = (holding != holding.shift()).astype(float)
    legs = changes * ((holding != "").astype(int) + (holding.shift().fillna("") != "").astype(int))
    return (r - legs * COST).shift(1).fillna(0)  # align: return realised on the following day


def strategies(px: pd.DataFrame) -> dict[str, pd.Series]:
    on = {c: band_state(px[c]) for c in px.columns}
    out = {"SPY buy & hold": pd.Series("SPY", index=px.index),
           "SPY trend (live)": pd.Series(np.where(on["SPY"], "SPY", ""), index=px.index),
           "QQQ trend": pd.Series(np.where(on["QQQ"], "QQQ", ""), index=px.index)}
    month = pd.Series(px.index.to_period("M"), index=px.index)
    month_start = month.ne(month.shift())
    for L in (63, 126, 252):
        mom = px / px.shift(L) - 1
        pick = mom.dropna().idxmax(axis=1).reindex(px.index).where(month_start).ffill()
        for absolute in (False, True):
            hold = []
            for d, p in pick.items():
                if not isinstance(p, str) or np.isnan(mom.loc[d, p]):
                    hold.append("")
                    continue
                ok = on[p].loc[d] and (not absolute or mom.loc[d, p] > 0)
                hold.append(p if ok else "")
            out[f"rotate_{L}{'_abs' if absolute else ''}"] = pd.Series(hold, index=px.index)
    return out


def metrics(r: pd.Series) -> tuple[float, float, float]:
    eq = (1 + r).cumprod()
    yrs = (r.index[-1] - r.index[0]).days / 365.25
    cagr = eq.iloc[-1] ** (1 / yrs) - 1
    dd = float((eq / eq.cummax() - 1).min())
    sharpe = r.mean() / r.std() * np.sqrt(252) if r.std() > 0 else np.nan
    return cagr, dd, sharpe


def run() -> None:
    px = pd.concat({s: load_daily(s)["close"] for s in ("SPY", "QQQ")}, axis=1).dropna().loc["1999-03-10":]
    strats = strategies(px)
    out = ["# Core sleeve: SPY vs QQQ momentum rotation\n\n",
           f"Daily adjusted closes {px.index[0].date()} to {px.index[-1].date()} (first 200+ days are warm-up). "
           "Costs 0.03%/side per switch; cash earns 0. Selection 2000-2014, confirmation 2015-2026.\n\n",
           "| Strategy | 2000-2014 CAGR | max DD | Sharpe | 2015-2026 CAGR | max DD | Sharpe | switches/yr |\n"
           "|---|---|---|---|---|---|---|---|\n"]
    for name, hold in strats.items():
        r = simulate(px, hold)
        a, b = r.loc["2000-01-01":IS_END], r.loc["2015-01-01":]
        ma, mb = metrics(a), metrics(b)
        h = hold.loc["2000-01-01":]
        sw = (h != h.shift()).sum() / ((h.index[-1] - h.index[0]).days / 365.25)
        out.append(f"| {name} | {ma[0]:+.1%} | {ma[1]:.0%} | {ma[2]:.2f} | {mb[0]:+.1%} | {mb[1]:.0%} | {mb[2]:.2f} | {sw:.1f} |\n")
    open("reports/core_rotation_backtest.md", "w").write("".join(out))
    print("".join(out))


if __name__ == "__main__":
    run()
