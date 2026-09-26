"""Backtest the SPY put-spread candidate on REAL historical option prices.

Robinhood's connector exposes daily bars for expired SPY options back to
late 2017. Contracts are looked up and their bars fetched from a Claude
session (MCP tools cannot be called from plain Python); the saved JSON
tool results are parsed here, keyed by OCC symbol.

Workflow:
  plan.csv    trade plan: the model's entry days and strikes (see
              `run_real_backtest`), with the real Friday expiration
              nearest to 45 DTE.
  `chunk N`   prints the contract lookups needed for trades in chunk N,
              grouped by strike, skipping contracts already fetched.
  `status`    shows how many planned contracts have price data.
  `run`       prices every trade from real closes and writes the report.

Pricing: entry at each leg's daily close (Robinhood's closes behave like
marks: open == close); settlement at intrinsic value from SPY's close on
expiry day. Costs use the same per-leg model as the simulator, so model
and real results differ only in the option prices.
"""
from __future__ import annotations

import glob
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from tradingbot.research.data import CACHE_DIR, load_daily
from tradingbot.research.options_sim import DIV_YIELD, approx_rates, bs_price, implied_vol
from tradingbot.research.stats import trade_stats

OPT_DIR = CACHE_DIR / "options"
PLAN = OPT_DIR / "plan.csv"
TOOL_RESULTS = Path("/root/.claude/projects/-home-user-Ai-Trading-Tool-1")
CHUNK = 20


def _parse_occ(occ: str) -> tuple[str, float, str]:
    """'SPY   200320P00300000' -> ('2020-03-20', 300.0, 'put')."""
    code = occ.replace(" ", "")[-15:]
    expiry = f"20{code[0:2]}-{code[2:4]}-{code[4:6]}"
    kind = "put" if code[6] == "P" else "call"
    return expiry, int(code[7:]) / 1000.0, kind


def load_option_bars() -> dict[tuple[str, float], pd.Series]:
    """All saved get_option_historicals results -> {(expiry, strike): close series}."""
    out: dict[tuple[str, float], pd.Series] = {}
    files = glob.glob(str(TOOL_RESULTS / "**" / "mcp-Robinhood_Trading-get_option_historicals-*.txt"), recursive=True)
    files += glob.glob(str(OPT_DIR / "bars_*.json"))
    for f in files:
        try:
            payload = json.load(open(f))
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue
        for res in payload.get("data", {}).get("results", []):
            if not res.get("occ_symbol") or not res.get("bars"):
                continue
            expiry, strike, kind = _parse_occ(res["occ_symbol"])
            if kind != "put":
                continue
            bars = [b for b in res["bars"] if not b.get("interpolated")]
            s = pd.Series(
                [float(b["close_price"]) for b in bars],
                index=pd.to_datetime([b["begins_at"][:10] for b in bars]),
            )
            key = (expiry, strike)
            out[key] = pd.concat([out[key], s]).groupby(level=0).last() if key in out else s
    return out


def _third_friday(year: int, month: int) -> pd.Timestamp:
    first = pd.Timestamp(year=year, month=month, day=1)
    return first + pd.Timedelta(days=(4 - first.dayofweek) % 7 + 14)


def make_plan() -> pd.DataFrame:
    """Entry days = the simulator's trades for the selected config (weekly,
    SPY > 200d SMA). Expiry = the standard monthly (3rd Friday; Thursday if
    that Friday is a holiday) closest to 45 DTE: Robinhood only has history
    for weekly expirations from ~3-4 weeks before expiry, and monthlies are
    the liquid, commonly traded ~45 DTE contracts. Strikes = ~30 and ~5
    delta (same model as the simulator) for that actual time to expiry."""
    from tradingbot.research import options_sim as opt

    spy = load_daily("SPY", adjusted=False)
    vix = load_daily("^VIX")["close"]
    spy = spy.loc[vix.index.min():]
    vix = vix.reindex(spy.index).ffill()
    rates = approx_rates(spy.index)
    cfg = opt.OptConfig("put_spread", 0.3, 0.05, 45, None, None, 0, "trend")
    model = pd.DataFrame(opt.simulate(spy, vix, rates, cfg))
    model = model[model.entry_date >= "2017-11-01"]
    trading_days = spy.index
    rows = []
    for m in model.itertuples():
        d = m.entry_date
        cands = []
        for k in range(0, 4):
            y, mo = (d + pd.DateOffset(months=k)).year, (d + pd.DateOffset(months=k)).month
            f = _third_friday(y, mo)
            f = trading_days[trading_days <= f][-1] if f <= trading_days[-1] else f
            cands.append(f)
        expiry = min(cands, key=lambda f: abs((f - d).days - 45))
        if expiry > trading_days[-1]:
            continue
        T = (expiry - d).days / 365.0
        S, v, r = float(spy["close"][d]), float(vix[d]), float(rates[d])
        ks = opt.strike_for_delta(S, T, r, v, 0.30, "put")
        kl = min(opt.strike_for_delta(S, T, r, v, 0.05, "put"), ks - 1)
        rows.append({"entry_date": d.date(), "expiry_real": expiry.date(), "dte": (expiry - d).days,
                     "K_short": ks, "K_long": kl, "model_ret": m.ret})
    plan = pd.DataFrame(rows)
    plan.insert(0, "trade_id", range(len(plan)))
    OPT_DIR.mkdir(parents=True, exist_ok=True)
    plan.to_csv(PLAN, index=False)
    return plan


def _needed(plan: pd.DataFrame) -> pd.DataFrame:
    need = pd.concat(
        [
            plan[["trade_id", "expiry_real", "K_short"]].rename(columns={"K_short": "K"}),
            plan[["trade_id", "expiry_real", "K_long"]].rename(columns={"K_long": "K"}),
        ]
    )
    return need


def chunk(n: int) -> None:
    plan = pd.read_csv(PLAN)
    part = plan.iloc[n * CHUNK : (n + 1) * CHUNK]
    have = load_option_bars()
    need = _needed(part)
    need = need[[(e, k) not in have for e, k in zip(need.expiry_real, need.K)]].drop_duplicates(["expiry_real", "K"])
    for k, g in need.groupby("K"):
        print(f"strike {k:.4f}  expiries {','.join(sorted(g.expiry_real))}")
    print(f"# trades {part.trade_id.min()}-{part.trade_id.max()}: entries {part.entry_date.min()}..{part.entry_date.max()}, "
          f"latest expiry {part.expiry_real.max()}, {len(need)} contracts missing")


def pending(include_partial: bool = False) -> None:
    """Contracts with a looked-up ID (ids.csv: expiry,strike,id) but no bars
    yet, in batches of 10 with a date range covering their entries.

    Results under ~85k characters come back inline instead of being saved
    to a file, so only full batches are listed (unless `include_partial`)
    and each range spans at least 130 days."""
    ids = pd.read_csv(OPT_DIR / "ids.csv", names=["expiry", "strike", "id"])
    have = load_option_bars()
    plan = pd.read_csv(PLAN)
    todo = ids[[(e, float(k)) not in have for e, k in zip(ids.expiry, ids.strike)]].drop_duplicates("id")
    todo = todo.sort_values(["expiry", "strike"])
    for i in range(0, len(todo), 10):
        b = todo.iloc[i : i + 10]
        if len(b) < 10 and not include_partial:
            print(f"# {len(b)} left for the next batch")
            break
        first = pd.Timestamp(plan[plan.expiry_real.isin(b.expiry)].entry_date.min()) - pd.Timedelta(days=3)
        end = pd.Timestamp(b.expiry.max()) + pd.Timedelta(days=1)
        first = min(first, end - pd.Timedelta(days=130))
        print(f"{first:%Y-%m-%dT00:00:00Z} {end:%Y-%m-%dT00:00:00Z} " + ",".join(b.id))
    print(f"# {len(todo)} contracts pending")


def status() -> None:
    plan = pd.read_csv(PLAN)
    have = load_option_bars()
    need = _needed(plan).drop_duplicates(["expiry_real", "K"])
    got = [(e, k) in have for e, k in zip(need.expiry_real, need.K)]
    print(f"{sum(got)}/{len(need)} contracts have bars")
    miss = need[[not g for g in got]]
    if len(miss):
        first = plan.set_index("trade_id").loc[miss.trade_id.min()]
        print(f"first missing: trade {miss.trade_id.min()} ({first.entry_date}), chunk {miss.trade_id.min() // CHUNK}")


def _slip(legs, S, T, r, vix, prices, slip_mult):
    """Same per-leg cost as options_sim._slip, but on the real leg prices."""
    return sum((0.01 + 0.02 * px) * slip_mult + 0.0004 for px in prices)


def run(out_path: str = "reports/real_options_backtest.md") -> None:
    plan = pd.read_csv(PLAN, parse_dates=["entry_date", "expiry_real"])
    bars = load_option_bars()
    spy = load_daily("SPY", adjusted=False)["close"]
    rows = []
    for t in plan.itertuples():
        e = t.expiry_real.strftime("%Y-%m-%d")
        ks, kl = bars.get((e, t.K_short)), bars.get((e, t.K_long))
        if ks is None or kl is None or t.entry_date not in ks.index or t.entry_date not in kl.index:
            rows.append({"trade_id": t.trade_id, "entry_date": t.entry_date, "status": "no data"})
            continue
        ps, pl = float(ks[t.entry_date]), float(kl[t.entry_date])
        settle_day = spy.index[spy.index <= t.expiry_real][-1]
        S_T = float(spy[settle_day])
        width = t.K_short - t.K_long
        row = {"trade_id": t.trade_id, "entry_date": t.entry_date, "exit_date": settle_day, "status": "ok",
               "short_px": ps, "long_px": pl, "model_ret": t.model_ret}
        for label, mult in (("", 1.0), ("_2x", 2.0), ("_mid", 0.0)):
            credit = ps - pl - _slip(None, None, None, None, None, (ps, pl), mult)
            intrinsic = max(0.0, t.K_short - S_T) - max(0.0, t.K_long - S_T)
            exit_cost = _slip(None, None, None, None, None, (max(0.0, t.K_short - S_T), max(0.0, t.K_long - S_T)), mult) if intrinsic > 0 else 0.0
            risk = width - credit
            row["credit" + label] = credit
            row["ret" + label] = (credit - intrinsic - exit_cost) / risk if risk > 0 else np.nan
        rows.append(row)
    df = pd.DataFrame(rows)
    ok = df[df.status == "ok"].copy()
    ok.to_csv(OPT_DIR / "real_trades.csv", index=False)
    years = (ok.exit_date.max() - ok.entry_date.min()).days / 365.25 if len(ok) else 0
    stats = {
        "Real prices, base costs": trade_stats(ok.assign(ret=ok["ret"], weight=0.05), years),
        "Real prices, 2x costs": trade_stats(ok.assign(ret=ok["ret_2x"], weight=0.05), years),
        "Real prices, mid (no costs)": trade_stats(ok.assign(ret=ok["ret_mid"], weight=0.05), years),
        "Model prices, same trades": trade_stats(ok.assign(ret=ok["model_ret"], weight=0.05), years),
    }
    lines = [
        "# SPY put spread on real option prices\n",
        "Strategy (selected in-sample on modelled prices, unchanged here): sell ~30-delta put, buy ~5-delta put, "
        "standard monthly expiry nearest 45 DTE, enter weekly only when SPY > 200-day SMA, hold to expiry.\n",
        f"Data: Robinhood daily closes for expired SPY options; {len(ok)} of {len(df)} planned trades priced "
        f"({ok.entry_date.min().date() if len(ok) else '-'} to {ok.exit_date.max().date() if len(ok) else '-'}).\n",
        "\n| Pricing | Trades | Win rate (95% low) | Avg win / loss | Expectancy | PF | t | Worst | Max DD (5% risk/trade) |\n|---|---|---|---|---|---|---|---|---|\n",
    ]
    for k, s in stats.items():
        lines.append(
            f"| {k} | {s.n} | {s.win_rate:.1%} (≥{s.win_rate_lo95:.1%}) | {s.avg_win:+.1%} / {s.avg_loss:+.1%} | "
            f"{s.expectancy:+.2%} | {s.profit_factor:.2f} | {s.t_stat:.2f} | {s.worst_trade:+.0%} | {s.max_drawdown:.1%} |\n"
        )
    if len(ok):
        ok["year"] = ok.entry_date.dt.year
        yr = ok.groupby("year").agg(trades=("ret", "size"), win=("ret", lambda s: (s > 0).mean()), mean_ret=("ret", "mean"),
                                    model_mean=("model_ret", "mean"))
        lines.append("\n## By entry year (base costs)\n\n| Year | Trades | Win rate | Mean return on risk | Model mean |\n|---|---|---|---|---|\n")
        for y, r in yr.iterrows():
            lines.append(f"| {y} | {r.trades} | {r.win:.0%} | {r.mean_ret:+.1%} | {r.model_mean:+.1%} |\n")
    Path(out_path).write_text("".join(lines))
    print("".join(lines))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    if cmd == "plan":
        p = make_plan()
        print(len(p), "trades;", p.dte.describe()[["min", "mean", "max"]].round(1).to_dict())
    elif cmd == "pending":
        pending(include_partial="--all" in sys.argv)
    elif cmd == "chunk":
        chunk(int(sys.argv[2]))
    elif cmd == "run":
        run()
    else:
        status()
