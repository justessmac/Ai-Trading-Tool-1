"""Daily-bar mean-reversion strategies (Connors/Alvarez style) and a
trade-by-trade simulator.

Execution model (no lookahead):
  - Signals are computed on the close of day t.
  - Entries and signal exits fill at the OPEN of day t+1.
  - An optional stop-loss is checked against each held day's low; it fills
    at the stop price, or at the open if the day gapped through it.
  - Costs are charged per side as a fraction of price (slippage + fees).
"""
from __future__ import annotations

import itertools
from dataclasses import dataclass, field

import numpy as np
import pandas as pd

from tradingbot.indicators import bollinger_bands, rsi, sma


def prepare(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    c = out["close"]
    out["sma5"] = sma(c, 5)
    out["sma200"] = sma(c, 200)
    out["rsi2"] = rsi(c, 2)
    out["crsi2"] = out["rsi2"] + out["rsi2"].shift(1)
    rng = (out["high"] - out["low"]).replace(0, np.nan)
    out["ibs"] = ((c - out["low"]) / rng).fillna(0.5)
    for n in (5, 7, 10):
        out[f"low{n}"] = c.rolling(n).min()
        out[f"high{n}"] = c.rolling(n).max()
    down = (c < c.shift(1)).astype(int)
    out["down_streak"] = down.groupby((down == 0).cumsum()).cumsum()
    lh = (out["high"] < out["high"].shift(1)) & (out["low"] < out["low"].shift(1))
    out["hl3"] = lh & lh.shift(1, fill_value=False) & lh.shift(2, fill_value=False)
    for k in (1.5, 2.0, 2.5):
        out[f"bbl{k}"] = bollinger_bands(c, 20, k)["bb_lower"]
    out["bbmid"] = sma(c, 20)
    out["prev_high"] = out["high"].shift(1)
    # Turn of month: trading-day position within month, from start and end.
    month = out.index.to_period("M")
    out["tdom"] = out.groupby(month).cumcount() + 1
    out["tdom_rev"] = out.groupby(month).cumcount(ascending=False) + 1
    return out


@dataclass(frozen=True)
class Config:
    family: str
    params: tuple = field(default_factory=tuple)

    @property
    def p(self) -> dict:
        return dict(self.params)

    def label(self) -> str:
        return self.family + "(" + ", ".join(f"{k}={v}" for k, v in self.params) + ")"


def signals(d: pd.DataFrame, cfg: Config) -> tuple[pd.Series, pd.Series]:
    """Return (entry, exit) boolean series evaluated at each day's close."""
    p = cfg.p
    c = d["close"]
    trend = c > d["sma200"] if p.get("trend", True) else pd.Series(True, index=d.index)
    f = cfg.family
    if f == "rsi2":
        entry = d["rsi2"] < p["th"]
    elif f == "crsi2":
        entry = d["crsi2"] < p["th"]
    elif f == "double7":
        entry = c <= d[f"low{p['n']}"]
    elif f == "ibs":
        entry = d["ibs"] < p["th"]
    elif f == "down_days":
        entry = d["down_streak"] >= p["k"]
    elif f == "hl3":
        entry = d["hl3"].astype(bool)
    elif f == "bb":
        entry = c < d[f"bbl{p['k']}"]
    elif f == "tom":
        entry = d["tdom_rev"] == p["enter_rev"]
    else:
        raise ValueError(f)
    entry = entry & trend

    x = p.get("exit", "sma5")
    if f == "tom":
        exit_ = d["tdom"] == p["exit_day"]
    elif f == "double7":
        exit_ = c >= d[f"high{p['n']}"]
    elif x == "sma5":
        exit_ = c > d["sma5"]
    elif x == "prev_high":
        exit_ = c > d["prev_high"]
    elif x == "bbmid":
        exit_ = c > d["bbmid"]
    elif x.startswith("rsi"):
        exit_ = d["rsi2"] > float(x[3:])
    else:
        raise ValueError(x)
    return entry.fillna(False), exit_.fillna(False)


def simulate(d: pd.DataFrame, cfg: Config, cost: float, symbol: str = "") -> list[dict]:
    entry, exit_ = signals(d, cfg)
    p = cfg.p
    stop = p.get("stop")
    max_hold = p.get("max_hold", 20)
    o, h, l, c = (d[k].to_numpy() for k in ("open", "high", "low", "close"))
    ent, ext = entry.to_numpy(), exit_.to_numpy()
    idx = d.index
    trades = []
    n = len(d)
    entry_days = np.flatnonzero(ent[: n - 1])
    last_exit = 0
    for i in entry_days:
        if i < last_exit:
            continue  # still in the previous position
        j = i + 1  # fill at next open
        px_in = o[j]
        stop_px = px_in * (1 - stop) if stop else None
        k = j
        px_out = None
        while k < n:
            if stop_px is not None and l[k] <= stop_px:
                px_out = min(o[k], stop_px) if k > j else stop_px
                break
            if (ext[k] or k - j + 1 >= max_hold) and k + 1 < n:
                k += 1
                px_out = o[k]
                break
            k += 1
        if px_out is None:  # still open at end of data: mark at last close
            k, px_out = n - 1, c[n - 1]
        ret = px_out * (1 - cost) / (px_in * (1 + cost)) - 1
        trades.append(
            {"symbol": symbol, "entry_date": idx[j], "exit_date": idx[k], "ret": ret, "days": k - j}
        )
        last_exit = k
    return trades


def grid() -> list[Config]:
    cfgs: list[Config] = []

    def add(family, **space):
        keys = list(space)
        for vals in itertools.product(*(space[k] for k in keys)):
            cfgs.append(Config(family, tuple(zip(keys, vals))))

    common = dict(trend=[True, False], stop=[None, 0.10], max_hold=[10, 20])
    add("rsi2", th=[5, 10, 15, 25], exit=["sma5", "rsi70", "prev_high"], **common)
    add("crsi2", th=[10, 20, 35, 50], exit=["sma5", "rsi65"], **common)
    add("double7", n=[5, 7, 10], **common)
    add("ibs", th=[0.1, 0.2, 0.3], exit=["sma5", "prev_high"], **common)
    add("down_days", k=[2, 3, 4], exit=["sma5", "prev_high"], **common)
    add("hl3", exit=["sma5", "prev_high"], **common)
    add("bb", k=[1.5, 2.0, 2.5], exit=["sma5", "bbmid"], **common)
    add("tom", enter_rev=[2, 4, 6], exit_day=[1, 3, 5], trend=[True, False], stop=[None], max_hold=[15])
    return cfgs
