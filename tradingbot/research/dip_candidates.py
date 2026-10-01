"""SPY dip-buy sleeve (Strategy 3) with QQQ and IWM as extra candidates.

Live rule: buy at the close when RSI(2) < 10 and close > 200-day SMA; sell at
the close when RSI(2) > 70 or after 10 trading days. Costs 0.03%/side;
adjusted closes. One position at a time in the sleeve. Variants for the
multi-fund sleeve, when several signal on the same day: priority SPY > QQQ >
IWM, or the lowest RSI(2). Selection 2001-2014, confirmation 2015-2026.

Usage: python -m tradingbot.research.dip_candidates
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from tradingbot.indicators import rsi, sma
from tradingbot.research.data import load_daily

COST = 0.0003
FUNDS = ("SPY", "QQQ", "IWM")


def frame() -> dict[str, pd.DataFrame]:
    out = {}
    for f in FUNDS:
        c = load_daily(f)["close"]
        out[f] = pd.DataFrame({"c": c, "rsi": rsi(c, 2), "sma": sma(c, 200)})
    idx = out["SPY"].index
    for f in FUNDS:
        out[f] = out[f].reindex(idx)
    return out


def sleeve(data: dict, funds: tuple, pick: str = "priority") -> tuple[pd.DataFrame, pd.Series]:
    idx = data["SPY"].index
    daily = pd.Series(0.0, index=idx)
    trades, pos = [], None
    for i in range(201, len(idx) - 1):
        d = idx[i]
        if pos is not None:
            f, ei, ep = pos
            daily.iloc[i] = data[f].c.iloc[i] / data[f].c.iloc[i - 1] - 1
            if data[f].rsi.iloc[i] > 70 or i - ei >= 10:
                r = data[f].c.iloc[i] / ep - 1 - 2 * COST
                daily.iloc[i] -= 2 * COST
                trades.append({"fund": f, "entry": idx[ei], "exit": d, "ret": r})
                pos = None
            continue
        cands = [f for f in funds if data[f].rsi.iloc[i] < 10 and data[f].c.iloc[i] > data[f].sma.iloc[i]]
        if cands:
            f = cands[0] if pick == "priority" else min(cands, key=lambda x: data[x].rsi.iloc[i])
            pos = (f, i, data[f].c.iloc[i])
    return pd.DataFrame(trades), daily


def run() -> None:
    data = frame()
    out = ["# Dip-buy sleeve: SPY plus QQQ/IWM candidates\n\n",
           "RSI(2)<10 above the 200-day SMA, exit RSI(2)>70 or 10 days; one position at a time; 0.03%/side.\n\n",
           "| Variant | IS trades/yr | IS avg | IS win | IS t | IS sleeve CAGR | OOS trades/yr | OOS avg | OOS win | OOS t | OOS sleeve CAGR | OOS DD |\n"
           "|---|---|---|---|---|---|---|---|---|---|---|---|\n"]
    variants = [("SPY only (live)", ("SPY",), "priority"), ("QQQ only", ("QQQ",), "priority"), ("IWM only", ("IWM",), "priority"),
                ("SPY>QQQ>IWM priority", FUNDS, "priority"), ("lowest RSI of 3", FUNDS, "lowest"),
                ("SPY>QQQ", ("SPY", "QQQ"), "priority")]
    for name, funds, pick in variants:
        t, daily = sleeve(data, funds, pick)
        cells = []
        for a, b in (("2001", "2014"), ("2015", "2026")):
            tt = t[(t.entry >= a) & (t.entry <= f"{b}-12-31")]
            dd = daily.loc[a:b]
            yrs = (dd.index[-1] - dd.index[0]).days / 365.25
            eq = (1 + dd).cumprod()
            tstat = tt.ret.mean() / (tt.ret.std(ddof=1) / np.sqrt(len(tt)))
            cells += [f"{len(tt) / yrs:.1f}", f"{tt.ret.mean():+.2%}", f"{(tt.ret > 0).mean():.0%}", f"{tstat:.2f}",
                      f"{eq.iloc[-1] ** (1 / yrs) - 1:+.1%}"]
            last_dd = f"{(eq / eq.cummax() - 1).min():.0%}"
        out.append(f"| {name} | " + " | ".join(cells) + f" | {last_dd} |\n")
    open("reports/dip_candidates_backtest.md", "w").write("".join(out))
    print("".join(out))


if __name__ == "__main__":
    run()
