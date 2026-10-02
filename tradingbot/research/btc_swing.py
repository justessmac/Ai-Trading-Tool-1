"""Swing-trading rules for the Bitcoin sleeve (GBTC 2017-2023 chained to IBIT).

Daily closes only (Robinhood equity history). Signal at close t, filled at
close t+1 (conservative vs the ~15:48 live check). Cost 0.1% per side.
In-sample 2018-04..2021-12, out-of-sample 2022-01..2026-09.
"""
import itertools
import numpy as np
import pandas as pd

from tradingbot.research.options_sim import approx_rates

COST = 0.001


def series():
    g = pd.read_csv("data_cache/crypto_GBTC.csv", index_col=0, parse_dates=True).close
    i = pd.read_csv("data_cache/crypto_IBIT.csv", index_col=0, parse_dates=True).close
    r = pd.concat([g.pct_change()[g.index < "2024-01-12"], i.pct_change()[i.index >= "2024-01-12"]]).dropna()
    return (1 + r).cumprod(), r


def rsi(px, n):
    d = px.diff()
    up = d.clip(lower=0).ewm(alpha=1 / n, adjust=False).mean()
    dn = (-d.clip(upper=0)).ewm(alpha=1 / n, adjust=False).mean()
    return 100 - 100 / (1 + up / dn)


def backtest(px, r, entry, exit_fn, max_hold):
    """entry/exit_fn: boolean arrays evaluated at close t. Returns daily rets, trades."""
    p = px.to_numpy(); n = len(p); pos = np.zeros(n); trades = []; held = 0; ent_px = None
    for t in range(200, n - 1):
        if pos[t] == 0:
            if entry[t]:
                pos[t + 1] = 1; held = 0; ent_px = p[t + 1]; ent_i = t + 1
        else:
            held += 1
            if exit_fn[t] or held >= max_hold:
                pos[t + 1] = 0
                trades.append((px.index[ent_i], px.index[t + 1], p[t + 1] / ent_px - 1 - 2 * COST))
            else:
                pos[t + 1] = 1
    cash = (approx_rates(px.index) / 252).to_numpy()
    ret = pos * r.to_numpy() + (1 - pos) * cash - np.abs(np.diff(pos, prepend=0)) * COST
    return pd.Series(ret, index=px.index), pd.DataFrame(trades, columns=["entry", "exit", "ret"])


def rules(px):
    sma = {k: px.rolling(k).mean() for k in (20, 50, 100, 200)}
    out = {}
    r2 = rsi(px, 2)
    for th, trend in itertools.product((10, 20), (50, 100)):
        e = (r2 < th) & (px > sma[trend])
        out[f"RSI2<{th} & >SMA{trend}, exit RSI2>70/10d"] = (e.to_numpy(), (r2 > 70).to_numpy(), 10)
    for hi, lo in ((20, 10), (10, 5)):
        e = px >= px.rolling(hi).max()
        x = px <= px.rolling(lo).min()
        out[f"Breakout {hi}d high, exit {lo}d low"] = (e.to_numpy(), x.to_numpy(), 60)
    down3 = (px.diff() < 0).rolling(3).sum() == 3
    for trend in (50, 100):
        e = down3 & (px > sma[trend])
        out[f"3 down days & >SMA{trend}, exit up close/5d"] = (e.to_numpy(), (px.diff() > 0).to_numpy(), 5)
    return out


def stats(ret, trades, a, b):
    x = ret[(ret.index >= a) & (ret.index < b)]; eq = (1 + x).cumprod(); y = (x.index[-1] - x.index[0]).days / 365.25
    t = trades[(trades.entry >= a) & (trades.entry < b)]
    return dict(cagr=eq.iloc[-1] ** (1 / y) - 1, dd=(eq / eq.cummax() - 1).min(), n=len(t),
                win=(t.ret > 0).mean() if len(t) else np.nan, exp=t.ret.mean() if len(t) else np.nan,
                tstat=t.ret.mean() / t.ret.std() * np.sqrt(len(t)) if len(t) > 2 else np.nan,
                hold=(t.exit - t.entry).dt.days.mean() if len(t) else np.nan)


if __name__ == "__main__":
    px, r = series()
    P = [("2018-04-01", "2022-01-01", "IS"), ("2022-01-01", "2026-09-26", "OOS")]
    print(f"{'rule':44s} | " + " | ".join(f"{l}: CAGR  DD    trades win  exp/trade t  hold" for _, _, l in P))
    bh = pd.Series(r.to_numpy(), index=r.index)
    for name, (e, x, mh) in rules(px).items():
        ret, tr = backtest(px, r, e, x, mh)
        row = []
        for a, b, l in P:
            s = stats(ret, tr, a, b)
            row.append(f"{s['cagr']:+5.0%} {s['dd']:4.0%} {s['n']:5d} {s['win']:4.0%} {s['exp']:+6.2%} {s['tstat']:4.1f} {s['hold']:4.1f}d")
        print(f"{name:44s} | " + " | ".join(row))
