# QuantForge Research Gaps

Scope is limited to the permitted `yuvi` root and `Research` folder, excluding QuantForge and raw/M1/tick/OHLC datasets.

## Critical gaps before treating historical evidence as live-ready

1. **Live forward validation is absent.** Stress and Monte Carlo studies are favorable but do not measure live fills, rejection behavior, actual latency, or broker-specific slippage.
2. **Virtual signal, recoil and persistence need fixed, versioned definitions.** The conceptual framework is strong, but the retained outputs do not establish final portable thresholds.
3. **Tail-risk evidence from basket/grid clustering needs a safety decision.** `trade_clusters.csv` shows a strongly positive median but a minimum cluster PnL of -5,234.54 and maximum lot 10.24. This cannot be treated as an ordinary trade-level risk profile.
4. **Cross-market claims require reproducible result tables.** The journal reports strong EURUSD/BTC figures, but full supporting tables are not retained in the audit scope.
5. **MAE/MFE definition mismatch must be resolved.** The two exported trade files have materially different row counts, PnL distributions and adverse-excursion sign conventions.

## Partially validated ideas worth revisiting

- **Regime classification:** HIGH_VOL_TREND outperforms NEUTRAL in the small retained matrix, but subgroup counts of 0–15 cannot establish a robust regime rule.
- **Session timing:** Journals report timing concentration, and `analyze_time_pattern.py` exists, but its result file is absent.
- **Simple indicator replication:** stochastic, momentum, candle and SMA models were tested in `entry_replication_test.py`; no archived overlap results survive.
- **Probe-confirm-scale / controlled recovery:** named in the consolidated journal, but a fully traceable numerical comparison is not available in scope.
- **NASDAQ transfer:** reported PF about 2.37 on 14 trades; explicitly insufficient for inference.

## Contradictions and caveats to retain

- The journal says yearly stability/no catastrophic breakdown, but `yearly_robustness_results.csv` has negative 2021 and 2024 rows, zero trades in 2022, and one trade in 2023. The reasonable conclusion is that early coverage is inadequate, not that all years validate the edge.
- High PF values with 0.0 PF in some rows reflect no recorded gross loss, not infinite or inherently superior performance. Small samples should not be ranked by that field.
- Monte Carlo distributions validate sensitivity to permutation and modeled friction only; they cannot eliminate source-trade selection bias.
- The master 72-trade log is favorable (87.5% win rate, PF 7.22), but it is a selected strategy log, not an all-signal population.

## Ideas apparently abandoned or not supported enough to promote

- **Trailing stops / long runner extraction:** journals state trailing logic degraded performance and quick snap exits were preferred.
- **Generic, indicator-only reconstruction:** investigated but no evidence survives that a stochastic/SMA-style model reproduces the behavioral entry logic.
- **Unconditional grid recovery:** cluster-tail data makes an unrestricted recovery approach a risk concern, not a validated edge.

## Recommended research sequence

1. Freeze a canonical event dataset with explicit signal, virtual-signal, recoil, persistence, exit and MAE/MFE definitions.
2. Reproduce walk-forward and cross-market tables from that dataset with sample sizes and confidence intervals.
3. Test a strict no-grid/no-scaling baseline separately from any basket recovery logic.
4. Run controlled forward/paper observation that records intended price, received price, spread, latency and rejection reason; do not infer this from Monte Carlo.
5. Re-test regime/session filters only after minimum sample rules are defined.
6. Evaluate portfolio correlation and simultaneous-signal exposure across Gold, EURUSD, BTC, Silver and NASDAQ.

## What should not be lost

- The behavioral thesis is not “buy oversold.” It is extreme displacement followed by observable recoil and stabilization.
- Confirmation rejects many candidates; lower trade count is a deliberate feature, not a failure.
- Quick exits are an empirical design choice tied to snap behavior.
- Robustness testing was unusually broad for the retained corpus: expansion, delays, spread, slippage, yearly slices, walk forward and two Monte Carlo variants.
- The gap is evidence preservation and independent reproduction—not a need to invent a new strategy.
