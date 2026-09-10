"""CLI entry point: run the multi-timeframe mean-reversion backtest.

Usage:
    python -m tradingbot.run_backtest [--source synthetic] [--out-dir output]

By default this uses the synthetic data generator (see data/synthetic.py)
since this environment has no outbound network access to real exchanges.
Results on synthetic data are a pipeline smoke test only -- NOT evidence
of real-world profitability. Swap `--source ccxt` (after `pip install
ccxt`, run somewhere with exchange network access) to backtest on real
historical data before trusting any numbers.
"""
from __future__ import annotations

import argparse
import os

import pandas as pd

from tradingbot.backtest import run_backtest
from tradingbot.config import StrategyConfig
from tradingbot.data.loader import load_symbol_data
from tradingbot.metrics import compute_metrics
from tradingbot.strategy import generate_signals

PERIODS_PER_YEAR = {
    "1m": 365 * 24 * 60,
    "5m": 365 * 24 * 12,
    "15m": 365 * 24 * 4,
    "1h": 365 * 24,
    "4h": 365 * 6,
    "1d": 365,
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", default="synthetic", choices=["synthetic", "ccxt"])
    parser.add_argument("--out-dir", default="output")
    parser.add_argument("--days", type=int, default=120, help="History length in days")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    config = StrategyConfig()
    os.makedirs(args.out_dir, exist_ok=True)

    all_curves = {}
    all_trades = []
    summary_rows = []

    for i, symbol in enumerate(config.symbols):
        signal_df, exec_df = load_symbol_data(
            symbol,
            config.signal_tf,
            config.exec_tf,
            source=args.source,
            periods_minutes=args.days * 24 * 60,
            # Distinct seed per symbol -- otherwise every symbol would
            # replay the exact same synthetic price path.
            seed=args.seed + i,
        )
        signals = generate_signals(signal_df, exec_df, config)
        trades, curve = run_backtest(signals, config, symbol)
        metrics = compute_metrics(curve, trades, PERIODS_PER_YEAR[config.exec_tf])

        all_curves[symbol] = curve
        all_trades.extend(trades)
        summary_rows.append({"symbol": symbol, **metrics.as_dict()})

        trades_df = pd.DataFrame([t.__dict__ for t in trades])
        trades_path = os.path.join(args.out_dir, f"trades_{symbol.replace('/', '-')}.csv")
        trades_df.to_csv(trades_path, index=False)
        curve.to_csv(os.path.join(args.out_dir, f"equity_{symbol.replace('/', '-')}.csv"))

    summary = pd.DataFrame(summary_rows).set_index("symbol")
    pd.set_option("display.width", 120)
    print("\n=== Per-symbol backtest summary (synthetic data, research only) ===")
    print(summary.round(2).to_string())

    if all_curves:
        combined = pd.concat(all_curves.values(), axis=1)
        combined.columns = list(all_curves.keys())
        combined = combined.ffill().dropna()
        portfolio_equity = combined.sum(axis=1)
        portfolio_metrics = compute_metrics(portfolio_equity, all_trades, PERIODS_PER_YEAR[config.exec_tf])
        print("\n=== Combined portfolio (sum of independently-sized per-symbol equity) ===")
        print(pd.Series(portfolio_metrics.as_dict()).round(2).to_string())
        portfolio_equity.to_csv(os.path.join(args.out_dir, "equity_portfolio.csv"))

        try:
            import matplotlib.pyplot as plt

            fig, ax = plt.subplots(figsize=(10, 5))
            for sym, curve in all_curves.items():
                ax.plot(curve.index, curve.values, label=sym)
            ax.plot(portfolio_equity.index, portfolio_equity.values, label="portfolio", linewidth=2, color="black")
            ax.set_title("Equity curves (synthetic data)")
            ax.legend()
            fig.tight_layout()
            fig.savefig(os.path.join(args.out_dir, "equity_curves.png"))
        except ImportError:
            pass

    print(f"\nDetailed trades/equity CSVs written to: {os.path.abspath(args.out_dir)}")


if __name__ == "__main__":
    main()
