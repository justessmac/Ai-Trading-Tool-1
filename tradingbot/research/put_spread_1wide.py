"""SPY $1-wide put credit spread on REAL option prices (small-account version).

Same entries as the tested 30/5-delta put spread (reports/real_options_backtest.md):
weekly, only when SPY > 200-day SMA, standard monthly expiry nearest 45 DTE,
short put ~30 delta. The only change is the long leg: $1 below the short
strike instead of ~5 delta, so max risk per spread is ~$70-90 instead of
thousands. Nothing was tuned here; the rule is the one chosen in-sample on
modelled 2000-2014 prices.

Pricing: each leg's Robinhood daily close (a mark) on the entry day; held to
expiry and settled at intrinsic value from SPY's close on expiry day. Costs:
a flat slippage per leg per side from the mark ($0.02 base, $0.04 stress, 0 at
"mid") plus $0.04 per contract per side in fees. The percentage model used for
the wide spread (0.01 + 2% of each leg's price) is also shown: on a $1-wide
spread whose legs cost ~$5-15 each it charges $0.20-0.60 per side, more than
the whole ~$0.20 credit, so it is far harsher than real SPY spread fills.

Account simulation: start $750 (the account after the user's $500 deposit),
1 spread per weekly signal while the open max-loss total stays <= 30% of
equity and one spread's max loss <= 20% of equity (playbook options limits).
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from tradingbot.research import real_options as ro
from tradingbot.research.data import load_daily
from tradingbot.research.stats import trade_stats

OOS_START = pd.Timestamp("2022-01-01")
START_EQUITY = 750.0
FEE = 0.0004  # $0.04 per contract per side, per share


def _flat(slip: float):
    return lambda legs: sum(slip + FEE for _ in legs)


COSTS = {
    "": _flat(0.02),
    "_2x": _flat(0.04),
    "_mid": _flat(0.0),
    "_pct": lambda legs: ro._slip(None, None, None, None, None, legs, 1.0),
}
NAMES = (("base ($0.02/leg)", ""), ("2x ($0.04/leg)", "_2x"), ("mid (fees only)", "_mid"), ("% model", "_pct"))


def trades() -> pd.DataFrame:
    plan = pd.read_csv(ro.PLAN, parse_dates=["entry_date", "expiry_real"])
    bars = ro.load_option_bars()
    spy = load_daily("SPY", adjusted=False)["close"]
    rows = []
    for t in plan.itertuples():
        e = t.expiry_real.strftime("%Y-%m-%d")
        ks = ro._nearest(bars, e, t.K_short, t.entry_date)
        if ks is None or (e, ks - 1) not in bars or t.entry_date not in bars[(e, ks - 1)].index:
            rows.append({"entry_date": t.entry_date, "status": "no data"})
            continue
        ps, pl = float(bars[(e, ks)][t.entry_date]), float(bars[(e, ks - 1)][t.entry_date])
        settle = spy.index[spy.index <= t.expiry_real][-1]
        S_T = float(spy[settle])
        row = {"entry_date": t.entry_date, "exit_date": settle, "status": "ok", "short_k": ks,
               "long_k": ks - 1, "short_px": ps, "long_px": pl, "spy_entry": float(spy[t.entry_date]),
               "spy_expiry": S_T}
        intrinsic = max(0.0, ks - S_T) - max(0.0, ks - 1 - S_T)
        legs_itm = (max(0.0, ks - S_T), max(0.0, ks - 1 - S_T))
        for label, cost in COSTS.items():
            credit = ps - pl - cost((ps, pl))
            exit_cost = cost(legs_itm) if intrinsic > 0 else 0.0
            risk = 1.0 - credit
            row["credit" + label] = credit
            row["risk" + label] = risk
            row["pnl" + label] = credit - intrinsic - exit_cost  # per share; x100 per spread
            row["ret" + label] = row["pnl" + label] / risk if risk > 0 else np.nan
        rows.append(row)
    return pd.DataFrame(rows)


def account_sim(ok: pd.DataFrame, col: str = "") -> dict:
    """Dollar P&L of 1-lot spreads on a $750 account under the playbook limits."""
    eq, open_pos, curve, taken = START_EQUITY, [], [], 0
    for t in ok.sort_values("entry_date").itertuples():
        for p in [p for p in open_pos if p[0] <= t.entry_date]:
            eq += p[1]
            open_pos.remove(p)
        risk = 100 * getattr(t, "risk" + col)
        open_risk = sum(p[2] for p in open_pos)
        if risk <= 0.20 * eq and open_risk + risk <= 0.30 * eq:
            open_pos.append((t.exit_date, 100 * getattr(t, "pnl" + col), risk))
            taken += 1
        curve.append((t.entry_date, eq))
    for p in sorted(open_pos):
        eq += p[1]
        curve.append((p[0], eq))
    s = pd.Series(dict(curve)).sort_index()
    years = (s.index[-1] - s.index[0]).days / 365.25
    return {"trades": taken, "end": eq, "cagr": (eq / START_EQUITY) ** (1 / years) - 1,
            "max_dd": float((s / s.cummax() - 1).min())}


def run(out_path: str = "reports/put_spread_1wide_backtest.md") -> pd.DataFrame:
    df = trades()
    ok = df[df.status == "ok"].copy()
    ok.to_csv("reports/put_spread_1wide_trades.csv", index=False)
    lines = ["# SPY $1-wide put credit spread on real option prices\n\n",
             f"{len(ok)} of {len(df)} planned weekly trades priced ({ok.entry_date.min().date()} to "
             f"{ok.exit_date.max().date()}). Returns are per dollar of max risk (width - credit).\n\n",
             "| Period | Costs | Trades | Win rate | Avg credit | Avg win / loss | Expectancy | t | Worst |\n"
             "|---|---|---|---|---|---|---|---|---|\n"]
    for pname, sub in (("2017-2021 (IS)", ok[ok.entry_date < OOS_START]), ("2022-2026 (OOS)", ok[ok.entry_date >= OOS_START]),
                       ("All", ok)):
        for cname, col in NAMES:
            s = trade_stats(sub.assign(ret=sub["ret" + col], weight=0.05), None)
            lines.append(f"| {pname} | {cname} | {s.n} | {s.win_rate:.1%} | ${100 * sub['credit' + col].mean():.0f} | "
                         f"{s.avg_win:+.1%} / {s.avg_loss:+.1%} | {s.expectancy:+.2%} | {s.t_stat:.2f} | {s.worst_trade:+.0%} |\n")
    lines.append("\n## $750 account, 1-lot spreads within the playbook limits (max loss/trade <= 20%, total <= 30%)\n\n"
                 "| Costs | Spreads taken | End equity | CAGR | Max drawdown |\n|---|---|---|---|---|\n")
    for cname, col in NAMES:
        a = account_sim(ok, col)
        lines.append(f"| {cname} | {a['trades']} | ${a['end']:,.0f} | {a['cagr']:+.1%} | {a['max_dd']:.1%} |\n")
    ok["year"] = ok.entry_date.dt.year
    yr = ok.groupby("year").agg(n=("ret", "size"), win=("ret", lambda s: (s > 0).mean()), mean=("ret", "mean"),
                                pnl=("pnl", lambda s: 100 * s.sum()))
    lines.append("\n## By entry year (base costs, 1 spread per week, no sizing limits)\n\n"
                 "| Year | Trades | Win rate | Mean return on risk | Sum P&L per 1-lot ($) |\n|---|---|---|---|---|\n")
    for y, r in yr.iterrows():
        lines.append(f"| {y} | {int(r.n)} | {r.win:.0%} | {r['mean']:+.1%} | {r.pnl:+,.0f} |\n")
    open(out_path, "w").write("".join(lines))
    print("".join(lines))
    return ok


if __name__ == "__main__":
    run()
