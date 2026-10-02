"""IPO event study on Robinhood daily bars: lockup expiry and post-IPO drift.

IPO date = first non-interpolated daily bar. Lockup date = IPO + 180 calendar
days (the standard term; some firms had staged or early releases, which adds
noise). Returns are abnormal vs SPY (stock return minus SPY return).
"""
import glob
import json

import numpy as np
import pandas as pd

from tradingbot.research.data import load_daily
from tradingbot.research.real_options import TOOL_RESULTS

DIRECT_LISTINGS = {"PLTR", "ASAN", "COIN", "RBLX", "SPOT", "WORK"}


def load():
    out = {}
    for f in glob.glob(str(TOOL_RESULTS / "**" / "mcp-Robinhood_Trading-get_equity_historicals-*.txt"), recursive=True):
        try:
            p = json.load(open(f))
        except Exception:
            continue
        for r in p.get("data", {}).get("results", []):
            if r.get("interval") != "day":
                continue
            b = [x for x in r["bars"] if not x.get("interpolated")]
            if len(b) < 250:
                continue
            s = pd.Series([float(x["close_price"]) for x in b], index=pd.to_datetime([x["begins_at"][:10] for x in b]))
            out[r["symbol"]] = s
    return out


def window(s, spy, center, a, b):
    i = s.index.searchsorted(center)
    if i + b >= len(s) or i + a < 0:
        return None
    d0, d1 = s.index[i + a], s.index[i + b]
    if d0 not in spy.index or d1 not in spy.index:
        return None
    return (s[d1] / s[d0] - 1) - (spy[d1] / spy[d0] - 1)


if __name__ == "__main__":
    spy = load_daily("SPY", adjusted=False).close
    ipos = {k: v for k, v in load().items() if k not in DIRECT_LISTINGS and k not in
            {"SPY", "QQQ", "IWM", "DIA", "XLF", "XLE", "XLK", "SMH", "TLT", "GLD", "AAPL", "MSFT", "NVDA", "AMZN",
             "META", "TSLA", "GOOGL", "AMD", "AVGO", "JPM", "GBTC", "IBIT", "BITO", "ETHE", "ETHA"}}
    rows = []
    for sym, s in sorted(ipos.items()):
        ipo = s.index[0]
        if ipo < pd.Timestamp("2019-03-02"):
            continue
        lock = ipo + pd.Timedelta(days=180)
        rows.append(dict(sym=sym, ipo=ipo.date(),
                         lock_m10_m1=window(s, spy, lock, -10, -1),   # run-up into lockup (short before)
                         lock_m5_p5=window(s, spy, lock, -5, 5),
                         lock_0_p10=window(s, spy, lock, 0, 10),
                         d3_d30=window(s, spy, ipo, 3, 30),          # after options list
                         d3_d250=window(s, spy, ipo, 3, 250)))       # first year
    df = pd.DataFrame(rows)
    pd.set_option("display.width", 200)
    print(df.round(3).to_string(index=False))
    print("\nWindow (abnormal vs SPY)      n   mean    median  % negative  t")
    for c in ["lock_m10_m1", "lock_m5_p5", "lock_0_p10", "d3_d30", "d3_d250"]:
        x = df[c].dropna()
        print(f"{c:28s} {len(x):3d} {x.mean():+7.1%} {x.median():+7.1%} {(x<0).mean():8.0%} {x.mean()/x.std()*np.sqrt(len(x)):6.2f}")
