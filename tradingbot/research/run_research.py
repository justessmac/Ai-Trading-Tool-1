"""Search high-win-rate strategies with an honest in-sample / out-of-sample split.

Protocol (fixed before looking at any results):
  1. Every config in each family's grid is run on the IN-SAMPLE period only.
  2. Per family, the config with the best IS t-stat among those meeting the
     IS win-rate target is selected (if none meet it, the highest-IS-win-rate
     config with IS t >= 2 is selected so the report still shows how close
     the family got).
  3. Only the selected config is run on the OUT-OF-SAMPLE period, once at
     base costs and once at 2x costs. OOS results never feed back into
     selection.
  4. `stats.passes` decides PASS/FAIL. The number of configs tried is
     reported so readers can judge multiple-testing risk.

Usage:
  python -m tradingbot.research.run_research [--split 2015-01-01] [--out reports/backtest_results.md]
"""
from __future__ import annotations

import argparse
import multiprocessing as mp
from collections import defaultdict
from pathlib import Path

import pandas as pd

from tradingbot.research import mean_reversion as mr
from tradingbot.research import options_sim as opt
from tradingbot.research.data import load_daily, load_many
from tradingbot.research.stats import Criteria, TradeStats, passes, trade_stats

ETF_UNIVERSE = [
    "SPY", "QQQ", "IWM", "DIA", "MDY",
    "XLB", "XLE", "XLF", "XLI", "XLK", "XLP", "XLU", "XLV", "XLY",
    "EFA", "EWJ", "EWG", "EWU", "EWC", "EWA",
]
CRYPTO_UNIVERSE = ["BTC-USD", "ETH-USD"]
ETF_COST = 0.0005  # 5 bps per side
CRYPTO_COST = 0.005  # 0.5% per side (~1% round trip, Robinhood-style spread)
START = "2000-01-01"


def _split(trades: pd.DataFrame, split: pd.Timestamp):
    return trades[trades["entry_date"] < split], trades[trades["entry_date"] >= split]


def _years(trades: pd.DataFrame) -> float:
    if trades.empty:
        return 0.0
    return (trades["exit_date"].max() - trades["entry_date"].min()).days / 365.25


def run_mean_reversion(data, cost, split, weight):
    prepared = {s: mr.prepare(d.loc[START:]) for s, d in data.items()}
    results = []
    by_family = defaultdict(list)
    for cfg in mr.grid():
        by_family[cfg.family].append(cfg)

    for family, cfgs in by_family.items():
        scored = []
        for cfg in cfgs:
            trades = []
            for sym, d in prepared.items():
                trades += mr.simulate(d, cfg, cost, sym)
            t = pd.DataFrame(trades)
            if t.empty:
                continue
            is_t, _ = _split(t, split)
            scored.append((cfg, trade_stats(is_t, _years(is_t))))
        yield from _select_and_test(
            family, scored, len(cfgs), split, weight,
            run=lambda cfg, c: pd.DataFrame(
                [tr for sym, d in prepared.items() for tr in mr.simulate(d, cfg, c, sym)]
            ),
            cost=cost,
        )


_OPT_ARGS: tuple = ()


def _init_opt(*args):
    global _OPT_ARGS
    _OPT_ARGS = args


def _score_opt(cfg):
    spy_raw, vix, rates, split, weight = _OPT_ARGS
    t = pd.DataFrame(opt.simulate(spy_raw, vix, rates, cfg))
    if t.empty:
        return None
    is_t, _ = _split(t, split)
    return cfg, trade_stats(is_t.assign(weight=weight), _years(is_t))


def run_options(spy_raw, vix, rates, split, weight):
    by_family = defaultdict(list)
    for cfg in opt.grid():
        by_family[cfg.structure].append(cfg)
    with mp.Pool(initializer=_init_opt, initargs=(spy_raw, vix, rates, split, weight)) as pool:
        all_scored = [s for s in pool.map(_score_opt, opt.grid(), chunksize=4) if s is not None]
    for family, cfgs in by_family.items():
        scored = [(c, s) for c, s in all_scored if c.structure == family]
        yield from _select_and_test(
            family, scored, len(cfgs), split, weight,
            run=lambda cfg, m: pd.DataFrame(opt.simulate(spy_raw, vix, rates, cfg, slip_mult=m)),
            cost=1.0,
        )


def _select_and_test(family, scored, n_tried, split, weight, run, cost):
    crit = Criteria()
    ok = [(c, s) for c, s in scored if s.win_rate >= crit.min_win_rate and s.t_stat >= crit.min_t and s.n > 0]
    if ok:
        cfg, _ = max(ok, key=lambda cs: cs[1].t_stat)
    else:
        profitable = [(c, s) for c, s in scored if s.t_stat >= crit.min_t]
        pool = profitable or scored
        if not pool:
            return
        cfg, _ = max(pool, key=lambda cs: (cs[1].win_rate, cs[1].t_stat))
    base = run(cfg, cost).assign(weight=weight)
    stress = run(cfg, cost * 2).assign(weight=weight)
    is_t, oos_t = _split(base, split)
    _, oos_s = _split(stress, split)
    is_st = trade_stats(is_t, _years(is_t))
    oos_st = trade_stats(oos_t, _years(oos_t))
    oos_stress = trade_stats(oos_s, _years(oos_s))
    ok_flag, why = passes(is_st, oos_st, oos_stress, crit)
    yield {
        "family": family,
        "config": cfg.label(),
        "configs_tried": n_tried,
        "is_hit_target": bool(ok),
        "IS": is_st,
        "OOS": oos_st,
        "OOS_2x_cost": oos_stress,
        "pass": ok_flag,
        "why": why,
        "oos_trades": oos_t,
    }


def _fmt(s: TradeStats) -> str:
    return (
        f"{s.n} | {s.win_rate:.1%} (≥{s.win_rate_lo95:.1%}) | {s.avg_win:+.2%} / {s.avg_loss:+.2%} | "
        f"{s.expectancy:+.3%} | {s.profit_factor:.2f} | {s.t_stat:.2f} | {s.worst_trade:+.1%} | "
        f"{s.cagr:+.1%} | {s.max_drawdown:.1%}"
    )


def render(rows, split, notes) -> str:
    hdr = (
        "| Strategy | Period | Trades | Win rate (95% low) | Avg win / loss | Expectancy | PF | t | Worst | CAGR | Max DD |\n"
        "|---|---|---|---|---|---|---|---|---|---|---|\n"
    )
    out = [
        "# Backtest results: high win-rate strategy search\n",
        f"In-sample: {START} to {split.date()} (used for tuning). Out-of-sample: {split.date()} onward (never used for tuning).\n",
        "Pass = ≥1000 total trades, ≥250 OOS trades, win rate ≥85% in BOTH periods, mean-trade t ≥ 2 and PF > 1 in both, "
        "and still profitable out-of-sample at 2x costs.\n",
        *notes,
        "\n## Summary\n",
        "| Strategy family | Selected config (chosen on IS only) | Configs tried | OOS trades | OOS win | OOS expectancy | Result |\n|---|---|---|---|---|---|---|\n",
    ]
    for r in rows:
        o = r["OOS"]
        out.append(
            f"| {r['family']} | `{r['config']}` | {r['configs_tried']} | {o.n} | {o.win_rate:.1%} | "
            f"{o.expectancy:+.3%} | {'**PASS**' if r['pass'] else 'fail: ' + r['why']} |\n"
        )
    out.append("\n## Detail\n\n" + hdr)
    for r in rows:
        for period in ("IS", "OOS", "OOS_2x_cost"):
            out.append(f"| {r['family']} | {period} | {_fmt(r[period])} |\n")
    return "".join(out)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", default="2015-01-01")
    ap.add_argument("--out", default="reports/backtest_results.md")
    ap.add_argument("--skip-options", action="store_true")
    ap.add_argument("--skip-crypto", action="store_true")
    args = ap.parse_args()
    split = pd.Timestamp(args.split)

    rows, notes = [], [
        "\nData: Robinhood daily bars via the Robinhood MCP connector (split-adjusted, NOT dividend-adjusted; "
        "split artefacts repaired by `import_robinhood.repair_price_jumps`). Missing dividends bias ETF "
        "mean-reversion returns slightly downward.\n"
    ]
    etfs = load_many(ETF_UNIVERSE)
    notes.append(f"\nETF universe loaded: {', '.join(etfs)} (cost {ETF_COST:.2%}/side, 10% of equity per trade).\n")
    rows += [dict(r, family="etf_" + r["family"]) for r in run_mean_reversion(etfs, ETF_COST, split, 0.10)]

    if not args.skip_crypto:
        crypto = load_many(CRYPTO_UNIVERSE)
        if crypto:
            csplit = pd.Timestamp("2021-01-01")
            notes.append(
                f"\nCrypto: {', '.join(crypto)} (cost {CRYPTO_COST:.1%}/side). Crypto history is short, so its split is {csplit.date()}.\n"
            )
            rows += [dict(r, family="crypto_" + r["family"]) for r in run_mean_reversion(crypto, CRYPTO_COST, csplit, 0.25)]

    if not args.skip_options:
        spy_raw = load_daily("SPY", adjusted=False)
        vix = load_daily("^VIX")["close"]
        spy_raw = spy_raw.loc[vix.index.min():]
        vix = vix.reindex(spy_raw.index).ffill()
        try:
            rates = load_daily("^IRX")["close"] / 100.0
            rates = rates.reindex(spy_raw.index).ffill().fillna(0.02)
        except RuntimeError:
            rates = opt.approx_rates(spy_raw.index)
            notes.append("\nRisk-free rate: approximate annual T-bill averages (no daily ^IRX series available).\n")
        notes.append(
            "\nOptions: SPY, weekly entries, Black-Scholes with VIX-based vol + put skew (NOT real option quotes); "
            "returns are per dollar of max risk (strike cash for CSPs); portfolio curves put 5% of equity at risk per trade.\n"
        )
        rows += [dict(r, family="spy_" + r["family"]) for r in run_options(spy_raw, vix, rates, split, 0.05)]

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render(rows, split, notes))
    for r in rows:
        print(f"{r['family']:<24} {'PASS' if r['pass'] else 'fail'}  {r['config']}  -> {r['why']}")
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
