"""Whole-account simulation of the adopted rules, and a deposit projection to $50k.

Sleeves (daily, decisions at the close, next-day returns):
- Core 50%: SPY/QQQ rotation (Strategy 1b at full size, the November target); out -> T-bills (BIL).
- Bitcoin trend 25%: spot BTC (weekdays), SMA100 +/-5%, exposure min(1, 0.40/vol20).
- Bitcoin swing 25%: RSI(2)<10 and > SMA100, exit RSI(2)>70 or 10 days.
- Idle cash (unused parts of the two Bitcoin quarters): the dip sleeve (lowest RSI(2) of
  SPY/QQQ/IWM) or the turn-of-month SPY trade use up to 20% of the account; the rest earns
  BIL (T-bills).
Costs: 0.03%/side for ETFs, 0.1%/side for Bitcoin. Period 2018-2026 (spot BTC; IBIT only
exists from 2024). The core and dip rules were chosen on 2000-2014 data and the Bitcoin
rules on 2018-2021, so 2018-2021 is partly in-sample for Bitcoin.

Projection: block bootstrap (21-day blocks) of the simulated daily returns, 5,000 paths,
starting $500 plus a monthly deposit; reports months to reach $50k.

Usage: python -m tradingbot.research.portfolio_sim
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from tradingbot.indicators import rsi
from tradingbot.research import core_rotation as cr
from tradingbot.research.data import load_daily
from tradingbot.research.dip_candidates import frame as dip_frame
from tradingbot.research.eth_trend import trend_returns


def daily_returns() -> pd.DataFrame:
    px = pd.concat({s: load_daily(s)["close"] for s in ("SPY", "QQQ", "IWM", "BIL")}, axis=1, sort=True).dropna()
    idx = px.index[px.index >= "2017-06-01"]
    btc = load_daily("BTC-USD")["close"]
    btc = btc[btc.index.dayofweek < 5].reindex(idx).ffill()
    bil = px.BIL.pct_change().reindex(idx).fillna(0)

    # core: rotation, out -> BIL
    hold = cr.strategies(px[["SPY", "QQQ"]])["rotate_126_abs"].reindex(idx)
    nxt = px.pct_change().shift(-1).reindex(idx)
    core = pd.Series(np.where(hold == "SPY", nxt.SPY, np.where(hold == "QQQ", nxt.QQQ, nxt.BIL)), index=idx)
    switch = (hold != hold.shift()).astype(float) * 2 * cr.COST
    core = (core - switch).shift(1).fillna(0)

    # bitcoin trend weight (0..1 of its quarter)
    sma = btc.rolling(100).mean()
    st, on = False, []
    for x, s in zip(btc.values, sma.values):
        if not np.isnan(s):
            st = True if x > s * 1.05 else False if x < s * 0.95 else st
        on.append(st)
    vol = btc.pct_change().rolling(20).std() * np.sqrt(252)
    w_tr = (pd.Series(on, index=idx, dtype=float) * np.minimum(1, 0.40 / vol)).fillna(0)
    r_btc = btc.pct_change().fillna(0)
    tr = w_tr.shift() * r_btc - (w_tr - w_tr.shift()).abs() * 0.001

    # bitcoin swing in/out (0/1 of its quarter)
    r2 = rsi(btc, 2)
    w_sw, pos, age = [], False, 0
    for i in range(len(idx)):
        if pos:
            age += 1
            if r2.iloc[i] > 70 or age >= 10:
                pos = False
        elif r2.iloc[i] < 10 and btc.iloc[i] > sma.iloc[i]:
            pos, age = True, 0
        w_sw.append(1.0 if pos else 0.0)
    w_sw = pd.Series(w_sw, index=idx)
    sw = w_sw.shift() * r_btc - (w_sw - w_sw.shift()).abs() * 0.001

    # idle cash: dip (priority) or TOM, capped 20% of account
    idle = 0.25 * (1 - w_tr) + 0.25 * (1 - w_sw)
    dd = dip_frame()
    dip_on = pd.Series(0.0, index=idx)
    dip_ret = pd.Series(0.0, index=idx)
    pos = None
    for i, d in enumerate(idx[:-1]):
        if pos is not None:
            f, age = pos
            dip_on.iloc[i] = 1
            dip_ret.iloc[i + 1] = dd[f].c.loc[idx[i + 1]] / dd[f].c.loc[d] - 1
            age += 1
            if dd[f].rsi.loc[d] > 70 or age >= 10:
                pos, dip_on.iloc[i] = None, 0
            else:
                pos = (f, age)
            continue
        c = [f for f in ("SPY", "QQQ", "IWM") if dd[f].rsi.loc[d] < 10 and dd[f].c.loc[d] > dd[f].sma.loc[d]]
        if c:
            f = min(c, key=lambda x: dd[x].rsi.loc[d])
            pos, dip_on.iloc[i] = (f, 0), 1
            dip_ret.iloc[i + 1] = dd[f].c.loc[idx[i + 1]] / dd[f].c.loc[d] - 1
    month = pd.Series(idx.to_period("M"), index=idx)
    pos_end = month.groupby(month).cumcount(ascending=False)
    pos_start = month.groupby(month).cumcount()
    tom_on = pd.Series(0.0, index=idx)
    i = 0
    while i < len(idx):
        if pos_end.iloc[i] == 4:
            j = i
            while j < len(idx) and not (pos_start.iloc[j] == 0 and j > i):
                j += 1
            tom_on.iloc[i:j] = 1  # held after the close of days i..j-1, sold at close of day j (1st day)
            i = j + 1
        else:
            i += 1
    spy_next = px.SPY.pct_change().reindex(idx).fillna(0)
    sat_w = np.minimum(0.20, idle)
    sat_ret = np.where(dip_on.shift() > 0, dip_ret, np.where(tom_on.shift() > 0, spy_next, np.nan))
    sat = pd.Series(np.where(np.isnan(sat_ret), 0, sat_w.shift() * (pd.Series(sat_ret, index=idx).fillna(0) - bil)), index=idx)
    turnover = ((dip_on.diff().abs() + tom_on.diff().abs()) * sat_w * 0.0003).fillna(0)
    total = 0.5 * core + 0.25 * tr + 0.25 * sw + idle.shift().fillna(0.5) * bil + sat - turnover
    return pd.DataFrame({"total": total, "core": core, "btc_trend": tr, "btc_swing": sw}).loc["2018-01-01":]


def project(r: pd.Series, deposit: float, start: float = 500.0, target: float = 50_000, paths: int = 5000,
            months: int = 240) -> np.ndarray:
    rng = np.random.default_rng(7)
    vals = r.values
    n_blocks = len(vals) // 21
    blocks = vals[: n_blocks * 21].reshape(n_blocks, 21)
    hit = np.full(paths, np.inf)
    for p in range(paths):
        eq = start
        for m in range(months):
            eq = eq * np.prod(1 + blocks[rng.integers(n_blocks)]) + deposit
            if eq >= target:
                hit[p] = m + 1
                break
    return hit


def run() -> None:
    df = daily_returns()
    out = ["# Whole-account simulation of the adopted rules (2018-2026) and a path to $50k\n\n",
           "| Part | CAGR | max DD | Sharpe |\n|---|---|---|---|\n"]
    for col in df.columns:
        eq = (1 + df[col]).cumprod()
        yrs = (eq.index[-1] - eq.index[0]).days / 365.25
        out.append(f"| {col} (as part of the account)" if col != "total" else "| **whole account**")
        out.append(f" | {eq.iloc[-1] ** (1 / yrs) - 1:+.1%} | {(eq / eq.cummax() - 1).min():.0%} | "
                   f"{df[col].mean() / df[col].std() * np.sqrt(252):.2f} |\n")
    yr = df.total.groupby(df.index.year).apply(lambda x: (1 + x).prod() - 1)
    out.append("\n| Year | Whole account |\n|---|---|\n" + "".join(f"| {y} | {v:+.1%} |\n" for y, v in yr.items()))
    out.append("\n## Months to reach $50,000 from $500 (bootstrap of the 2018-2026 daily returns)\n\n"
               "| Monthly deposit | 10% of paths (lucky) | median | 90% of paths (unlucky) | deposits alone, no growth |\n|---|---|---|---|---|\n")
    for dep in (0, 100, 250, 500, 1000):
        h = project(df.total, dep)
        q = np.percentile(h, [10, 50, 90])
        plain = (50_000 - 500) / dep if dep else np.inf
        f = lambda m: "never (20y)" if not np.isfinite(m) else f"{m:.0f} mo ({m / 12:.1f} y)"
        out.append(f"| ${dep} | {f(q[0])} | {f(q[1])} | {f(q[2])} | {f(plain)} |\n")
    open("reports/portfolio_sim.md", "w").write("".join(out))
    print("".join(out))


if __name__ == "__main__":
    run()
