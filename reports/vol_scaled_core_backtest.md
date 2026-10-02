# Volatility-scaled core (on the SPY/QQQ rotation)

**Verdict (2026-10-01): rejected.**
- Scaling the rotation to a volatility target lowers drawdown (e.g. vol20 at 15%: DD -18%/-19% vs -24%/-25%), but lowers CAGR in both periods for every setting except a +0.1-point in-sample tie (vol60 at 20%). That one loses out-of-sample (+9.1% vs +10.6%).
- Sharpe barely changes, so it only trades return for smaller drops, which the playbook's growth goal doesn't want while drawdowns stay within -25%.
- Process note: a first run showed a large gain (+14.4%/yr OOS). That was a look-ahead bug: it used the next day's fund choice. The fixed run is above. core_rotation.simulate was checked and does not have the bug.

| Variant | 2000-2014 CAGR | max DD | Sharpe | 2015-2026 CAGR | max DD | Sharpe | avg exposure when in |
|---|---|---|---|---|---|---|---|
| rotation, unscaled (Strategy 1b) | +7.3% | -24% | 0.62 | +10.6% | -25% | 0.73 | 100% |
| vol20, target 12% | +5.5% | -14% | 0.61 | +7.7% | -18% | 0.73 | 80% |
| vol20, target 15% | +6.3% | -18% | 0.63 | +9.2% | -19% | 0.77 | 89% |
| vol20, target 20% | +7.1% | -23% | 0.64 | +10.3% | -22% | 0.77 | 96% |
| vol60, target 12% | +5.4% | -14% | 0.60 | +7.0% | -17% | 0.67 | 78% |
| vol60, target 15% | +6.4% | -16% | 0.64 | +8.4% | -19% | 0.70 | 88% |
| vol60, target 20% | +7.4% | -19% | 0.66 | +9.1% | -23% | 0.69 | 95% |
