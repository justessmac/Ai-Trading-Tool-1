"""Turn-of-month (TOM) effect for idle cash, plus T-bill ETF yield on idle cash.

TOM rule: buy SPY at the close N trading days before month end (so the
position holds over the last N days), sell at the close of the M-th trading
day of the new month. Optional filter: only when SPY closes above its 200-day
SMA on the entry day. Costs 0.03% per side; returns use dividend-adjusted closes.

Grid (N in 1..4, M in 1..5, filter on/off) chosen on 2001-2014, confirmed on
2015-2026; QQQ and IWM are checked with the same pick as a robustness test.
Cash yield: BIL (1-3 month T-bills, 2007+) as the SGOV proxy before SGOV existed.

Usage: python -m tradingbot.research.turn_of_month
"""
from __future__ import annotations

import itertools

import numpy as np
import pandas as pd

from tradingbot.research.data import load_daily

COST = 0.0003
IS_END = pd.Timestamp("2014-12-31")


def tom_trades(close: pd.Series, n: int, m: int, trend: bool) -> pd.DataFrame:
    idx = close.index
    sma = close.rolling(200).mean()
    month = pd.Series(idx.to_period("M"), index=idx)
    pos_end = month.groupby(month).cumcount(ascending=False)  # 0 = last day of month
    rows = []
    entries = np.where(pos_end.values == n)[0]
    for i in entries:
        # exit: the m-th trading day of the next month = index of next month's first day + m - 1
        j = i + n + m
        if j >= len(idx):
            continue
        if trend and not close.iloc[i] > sma.iloc[i]:
            continue
        ret = close.iloc[j] / close.iloc[i] - 1 - 2 * COST
        rows.append({"entry": idx[i], "exit": idx[j], "ret": ret, "days": j - i})
    return pd.DataFrame(rows)


def _stats(df: pd.DataFrame) -> tuple[int, float, float, float]:
    if len(df) < 2:
        return len(df), np.nan, np.nan, np.nan
    r = df.ret
    return len(r), (r > 0).mean(), r.mean(), r.mean() / (r.std(ddof=1) / np.sqrt(len(r)))


def baseline(close: pd.Series, days: int, start, end) -> float:
    """Average return of holding SPY for `days` days from any day (the bar to beat per trade)."""
    c = close.loc[start:end]
    return float((c.shift(-days) / c - 1).mean())


def run() -> None:
    spy = load_daily("SPY")["close"].loc["2000-01-01":]
    out = ["# Turn-of-month effect and T-bill yield for idle cash\n\n",
           f"SPY daily (dividend-adjusted) {spy.index[0].date()} to {spy.index[-1].date()}. Costs 0.03%/side. "
           "Selection on 2001-2014, confirmation on 2015-2026.\n\n",
           "## Grid (sorted by in-sample t)\n\n",
           "| Hold last N / first M days | SMA200 filter | IS trades | IS win | IS avg | IS t | OOS trades | OOS win | OOS avg | OOS t |\n"
           "|---|---|---|---|---|---|---|---|---|---|\n"]
    res = []
    for n, m, trend in itertools.product(range(1, 5), range(1, 6), (False, True)):
        df = tom_trades(spy, n, m, trend)
        df = df[df.entry >= "2001-01-01"]
        is_, oos = df[df.entry <= IS_END], df[df.entry > IS_END]
        res.append(((n, m, trend), _stats(is_), _stats(oos), df))
    res.sort(key=lambda x: -x[1][3])
    for (n, m, trend), si, so, _ in res:
        out.append(f"| {n} / {m} | {'yes' if trend else 'no'} | {si[0]} | {si[1]:.0%} | {si[2]:+.2%} | {si[3]:.2f} | "
                   f"{so[0]} | {so[1]:.0%} | {so[2]:+.2%} | {so[3]:.2f} |\n")
    (n, m, trend), si, so, best = res[0]
    days = n + m
    out.append(f"\n## In-sample pick: hold the last {n} and first {m} trading days, SMA200 filter {'on' if trend else 'off'}\n\n")
    b_is = baseline(spy, days, "2001-01-01", IS_END)
    b_oos = baseline(spy, days, IS_END, None)
    out.append(f"Average {days}-day SPY return from any day: {b_is:+.2%} (2001-2014), {b_oos:+.2%} (2015-2026). "
               f"TOM trades: {si[2]:+.2%} and {so[2]:+.2%}.\n\n")
    out.append("| Market | Trades | Win | Avg | t (same rule, 2001-2026) |\n|---|---|---|---|---|\n")
    for sym in ("SPY", "QQQ", "IWM"):
        c = load_daily(sym)["close"]
        df = tom_trades(c, n, m, trend)
        s = _stats(df[df.entry >= "2001-01-01"])
        out.append(f"| {sym} | {s[0]} | {s[1]:.0%} | {s[2]:+.2%} | {s[3]:.2f} |\n")
    oos = best[best.entry > IS_END]
    out.append("\n## Out-of-sample by year\n\n| Year | Trades | Sum of returns |\n|---|---|---|\n")
    for y, g in oos.groupby(oos.entry.dt.year):
        out.append(f"| {y} | {len(g)} | {g.ret.sum():+.1%} |\n")

    # idle-cash sleeve: cash vs T-bills vs T-bills + TOM, as a fraction of the sleeve
    bil = load_daily("BIL")["close"]
    sgov = load_daily("SGOV")["close"]
    out.append("\n## Idle cash: T-bill ETF yield\n\n| Fund | Period | Annual return | Worst drawdown |\n|---|---|---|---|\n")
    for name, c in (("BIL", bil.loc["2015-01-01":]), ("SGOV", sgov)):
        yrs = (c.index[-1] - c.index[0]).days / 365.25
        out.append(f"| {name} | {c.index[0].date()} to {c.index[-1].date()} | {(c.iloc[-1] / c.iloc[0]) ** (1 / yrs) - 1:+.2%} | "
                   f"{(c / c.cummax() - 1).min():.2%} |\n")
    c = bil.loc["2025-09-30":]
    out.append(f"| BIL | last 12 months | {c.iloc[-1] / c.iloc[0] - 1:+.2%} | |\n")

    # sleeve simulation 2015+: always in BIL, switch to SPY during TOM windows
    days_idx = spy.loc["2015-01-01":].index.intersection(bil.index)
    in_tom = pd.Series(False, index=days_idx)
    for t in oos.itertuples():
        in_tom.loc[(in_tom.index > t.entry) & (in_tom.index <= t.exit)] = True
    r_spy, r_bil = spy.pct_change().reindex(days_idx), bil.pct_change().reindex(days_idx)
    switch = (in_tom != in_tom.shift()).astype(float) * COST * 2  # sell one, buy the other
    sleeves = {"cash": pd.Series(0.0, index=days_idx), "BIL only": r_bil,
               "BIL + TOM in SPY": np.where(in_tom, r_spy, r_bil) - switch, "SPY always": r_spy}
    out.append("\n## Idle-cash sleeve, 2015-2026 (returns of the sleeve itself)\n\n"
               "| Sleeve | Annual return | Max drawdown | Days in SPY |\n|---|---|---|---|\n")
    for name, r in sleeves.items():
        eq = (1 + pd.Series(r, index=days_idx).fillna(0)).cumprod()
        yrs = (eq.index[-1] - eq.index[0]).days / 365.25
        frac = in_tom.mean() if "TOM" in name else (1.0 if name == "SPY always" else 0.0)
        out.append(f"| {name} | {eq.iloc[-1] ** (1 / yrs) - 1:+.2%} | {(eq / eq.cummax() - 1).min():.1%} | {frac:.0%} |\n")
    open("reports/turn_of_month_backtest.md", "w").write("".join(out))
    print("".join(out))


if __name__ == "__main__":
    run()
