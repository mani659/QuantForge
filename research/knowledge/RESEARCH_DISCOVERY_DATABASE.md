# QuantForge Research Discovery Database

Scope: `C:\Users\User10\Documents\MRV\yuvi` and `C:\Users\User10\Documents\MRV\yuvi\Research` only. The `QuantForge` directory and raw/M1/tick/OHLC datasets were excluded. This record is evidence-led: a claim is marked limited where samples are small or only a script (not its output) survives.

## Evidence map

- Consolidated journals: `Research.docx`, `Universal_Mean_Reversion_Research_Journal_v1.0.0.docx`.
- Strategy/result outputs: `recoil_profile_analysis.csv`, `robustness_expansion_results.csv`, `randomized_stress_test_results.csv`, `walk_forward_results.csv`, `yearly_robustness_results.csv`, `meta_regime_results.csv`, `real_trade_monte_carlo.csv`, `monte_carlo_distribution.csv`, `yuvi_master_trade_log.csv`.
- Forensic/EA research: `entry_forensics.py`, `tick_entry_forensics.py`, `entry_replication_test.py`, `MAE_MFE.py`, `deep_analysis.py`, `cluster.py`, `synthetic_clone.py`, `test-14.py`, `mr_buy_subregimes.py`, `regime_classifier.py`, `regime_edge_matrix.py`, `yuvi_eur.py`, `yuvi_x_v01.py`, `extract_mt5_ea_data.py`, `market.py`, `analyze_time_pattern.py`, `analyze_basket_depth.py`, `analyze_grid_spacing.py`.

---

## DISC-001 — Extreme displacement is the candidate trigger

**Source files:** both research journals; `entry_forensics.py`; `recoil_profile_analysis.csv`; `yuvi_master_trade_log.csv`.

**Research question:** Does extreme short-term overextension identify a mean-reversion opportunity?

**Finding:** The retained research consistently frames the edge as deep z-score displacement plus adverse/panic momentum, rather than generic mean reversion. The 44-event recoil profile contains z-scores from -2.80 to -3.80 (mean about -3.0).

**Evidence:** Journal reports deeper/“very deep” conditions outperform moderate ones. The master log’s 72 selected trades has mean z-score -2.86 and mean momentum -15.01.

**Relationship:** Behavioral mean reversion; virtual signal.

**Confidence:** Medium-high. Selection criteria are clear, but the archived output is not a full unfiltered comparison.

**Framework status:** Partially implemented.

**Future importance:** Critical.

---

## DISC-002 — Volatility expansion conditions the edge

**Source files:** both journals; `entry_forensics.py`; `meta_regime_results.csv`; `recoil_profile_analysis.csv`.

**Research question:** Is displacement sufficient without a volatility context?

**Finding:** The journals report high-volatility conditions as materially stronger and low-volatility conditions as weaker. This supports treating volatility as a condition of behavioral dislocation, not merely a sizing input.

**Evidence:** In `meta_regime_results.csv`, HIGH_VOL_TREND has 15 trades, PF 1.93 and expectancy 0.2938; NEUTRAL has 11 trades, PF 1.19 and expectancy 0.0537. HIGH_VOL_MR and LOW_VOL_MR contain only 2 and 1 trades respectively, so they do not independently validate the comparison.

**Relationship:** Regime classification; behavioral mean reversion.

**Confidence:** Medium.

**Framework status:** Partially implemented.

**Future importance:** High.

---

## DISC-003 — Panic momentum contributes confluence

**Source files:** `Research.docx`; `entry_forensics.py`; `recoil_profile_analysis.csv`.

**Research question:** Does rapid adverse momentum distinguish emotional displacement from ordinary movement?

**Finding:** The retained journal records panic momentum clusters as the strongest outcome class. The selected recoil sample has consistently negative momentum at entry (mean -15.01).

**Evidence:** Journal conclusion: “PANIC” materially outperformed lighter momentum states. The archive lacks the complete factor table, so the exact incremental effect cannot be re-estimated.

**Relationship:** Behavioral mean reversion; confluence.

**Confidence:** Medium.

**Framework status:** Partially implemented.

**Future importance:** High.

---

## DISC-004 — Recoil is a measurable confirmation, not an entry thesis alone

**Source files:** `recoil_profile_analysis.csv`; `Research.docx`; `mr_buy_subregimes.py`.

**Research question:** What differentiates strong recovery from failed/weak recovery after a panic signal?

**Finding:** Strong winners show materially positive near-term recoil; scratch outcomes do not.

**Evidence:** Of 44 profiled events: 26 STRONG_WINNER, 9 WEAK_WINNER, 9 SCRATCH. Mean recoil at 3/5/10 bars is 7.72/7.65/10.72 for strong winners versus -1.19/-1.62/-4.15 for scratches. Mean final move is 14.87 for strong winners versus -9.37 for scratches.

**Relationship:** Recoil; virtual signal.

**Confidence:** High for the selected sample; external generalization remains unproven.

**Framework status:** Partially implemented.

**Future importance:** Critical.

---

## DISC-005 — Persistence after recoil is a second gate

**Source files:** `Research.docx`; `robustness_expansion_results.csv`; `mr_buy_subregimes.py`.

**Research question:** Is a first recoil sufficient to make a real entry?

**Finding:** No. The research narrative states that price must hold after recoil. Expansion results explicitly track both `RecoilFails` and `PersistenceFails`, preserving the two-stage hypothesis.

**Evidence:** FULL_EXPANSION reports 132 recoil failures and 122 persistence failures before 81 confirmations; SESSION_EXPANSION reports 56 and 65 failures before 28 confirmations. These are counts, not a causal estimate, but demonstrate that confirmation rejects many candidate events.

**Relationship:** Persistence; virtual signal; recoil.

**Confidence:** High conceptually, medium quantitatively.

**Framework status:** Partially implemented.

**Future importance:** Critical.

---

## DISC-006 — Confluence trades quantity for quality

**Source files:** `Research.docx`; `robustness_expansion_results.csv`.

**Research question:** Does combining displacement, momentum, volatility and timing improve the candidate set?

**Finding:** The journals report higher PF/expectancy and fewer trades under full confluence. The later expansion exercise shows high reported PF persists when rules are loosened, though trade counts remain modest.

**Evidence:** BASELINE: 12 trades, 91.67% win rate, PF 6.02. FULL_EXPANSION: 81 trades, 86.42%, PF 7.46, expectancy 1.1559, maximum drawdown -3.0. SESSION_EXPANSION: 28 trades, PF 11.10.

**Relationship:** Confluence; robustness expansion.

**Confidence:** Medium-high; all figures require independent reproduction from untouched data.

**Framework status:** Partially implemented.

**Future importance:** Critical.

---

## DISC-007 — Fast snap exits outperform runner extraction

**Source files:** both research journals; `yuvi_eur.py`; `yuvi_x_v01.py`.

**Research question:** What exit shape fits the observed behavioral move?

**Finding:** The journals consistently report that quick snap/adaptive exits outperform extended runners; trailing logic degraded performance in the archived experiments.

**Evidence:** The source journals explicitly identify quick snap behavior as dominant and extended runner extraction as limited. In the 72-trade master log, outcomes are 42 TP, 28 TIME, 2 SL, consistent with a short-horizon exit design.

**Relationship:** Exit optimization; recoil.

**Confidence:** Medium-high.

**Framework status:** Partially implemented.

**Future importance:** High.

---

## DISC-008 — Virtual signals filter early failure

**Source files:** `Research.docx`; `synthetic_clone.py`; `entry_replication_test.py`.

**Research question:** Should every panic observation become an executable signal?

**Finding:** The research moved to a virtual-signal stage followed by real-entry confirmation. The stated benefit was rejecting trades that fail before confirmation.

**Evidence:** The journal reports major PF improvement, large drawdown reduction and improved win rate, but does not retain the underlying before/after table in the permitted files.

**Relationship:** Virtual signal; recoil; persistence.

**Confidence:** Medium.

**Framework status:** Implemented conceptually / partially implemented operationally.

**Future importance:** Critical.

---

## DISC-009 — The edge survived deliberate execution degradation

**Source files:** `randomized_stress_test_results.csv`; `Research.docx`.

**Research question:** Does spread, slippage and delay erase the reported edge?

**Finding:** Every archived stress scenario remains positive with PF above 6.3 and expectancy above 1.11.

**Evidence:** BASELINE: 81 trades, PF 7.46, expectancy 1.1559, max DD -3.0. HEAVY_SLIPPAGE: 41 trades, PF 6.31, expectancy 1.1431, max DD -3.25. WIDER_SPREAD: 63 trades, PF 6.68. ENTRY_DELAY_2 has the worst listed drawdown, -4.57, but remains PF 7.20.

**Relationship:** Execution robustness.

**Confidence:** High for the simulated scenarios; not a substitute for live fills.

**Framework status:** Partially implemented.

**Future importance:** Critical.

---

## DISC-010 — Yearly walk-forward results were positive in the retained out-of-sample slices

**Source files:** `walk_forward_results.csv`; `Research.docx`.

**Research question:** Does the confirmation framework persist outside its development period?

**Finding:** 2024–2026 retained walk-forward rows are positive, with 2025 and 2026 providing most of the evidence.

**Evidence:** 2024: 4 trades, expectancy 0.8898; 2025: 30 trades, 80% win rate, PF 3.99, max DD -3.0; 2026: 32 trades, 93.75%, PF 13.10, max DD -3.0. The 2024 sample is too small for inference.

**Relationship:** Walk forward; temporal stability.

**Confidence:** Medium-high.

**Framework status:** Partially implemented.

**Future importance:** Critical.

---

## DISC-011 — Earlier yearly evidence is mixed and sample-limited

**Source files:** `yearly_robustness_results.csv`.

**Research question:** Is the edge stable across the full retained annual record?

**Finding:** The record contradicts a blanket “all years robust” conclusion. 2021 and 2024 are negative, 2022 has no trades, and 2023 has one trade. Stronger 2025–2026 results drive the positive conclusion.

**Evidence:** 2021: 2 trades, PnL -0.50, PF 0.67; 2024: 4 trades, PnL -1.30, PF 0.26; 2025: 17 trades, PF 3.88; 2026: 20 trades, PF 2.15.

**Relationship:** Temporal robustness; contradiction record.

**Confidence:** High that early evidence is insufficient; no conclusion beyond that is justified.

**Framework status:** Unknown.

**Future importance:** Critical.

---

## DISC-012 — Monte Carlo results are favorable, conditional on the selected trade stream

**Source files:** `real_trade_monte_carlo.csv`; `monte_carlo_distribution.csv`; `yuvi_x_v01.py`; `Research.docx`.

**Research question:** Is performance dominated by order sequence or modest adverse execution perturbation?

**Finding:** Both archived distributions show positive terminal balances and bounded drawdowns under resampling/perturbation, but they inherit selection bias from the source trade series.

**Evidence:** Real-trade Monte Carlo (10,000 runs): mean final balance 10,072.02; 1st percentile 10,061.37; mean max DD -3.89; worst -10.36; mean PF 6.46. Synthetic distribution (5,000 runs): mean final balance 10,081.91; 1st percentile 10,070.67; mean max DD -3.19. No ruin metric is stored in the output, though the journal reports zero ruin probability.

**Relationship:** Monte Carlo; execution robustness.

**Confidence:** Medium-high for sequence robustness, medium for live survivability.

**Framework status:** Partially implemented.

**Future importance:** High.

---

## DISC-013 — Cross-market transfer is the central universality claim

**Source files:** `Universal_Mean_Reversion_Research_Journal_v1.0.0.docx`; `yuvi_eur.py`; `test-14.py`.

**Research question:** Is the pattern instrument-specific?

**Finding:** The consolidated journal reports Gold as robust, EURUSD at 329 trades/PF about 4.5, BTC at 2,665 trades/PF about 6.0, and preliminary NASDAQ at 14 trades/PF 2.37.

**Evidence:** The journal explicitly cautions that NASDAQ coverage is limited (2021-05 to 2023-09) and 14 trades are insufficient. The underlying full cross-market output tables are not in this scope.

**Relationship:** Universality; cross-market validation.

**Confidence:** Medium-high for EURUSD/BTC as journalled; low for NASDAQ.

**Framework status:** Partially implemented.

**Future importance:** Critical.

---

## DISC-014 — Regime effects are plausible but not yet statistically established

**Source files:** `regime_classifier.py`; `regime_edge_matrix.py`; `meta_regime_results.csv`.

**Research question:** Can market regime explain where the edge strengthens or degrades?

**Finding:** The retained matrix indicates better performance in high-volatility trend conditions than neutral conditions, but subgroup samples are small and several cells are empty.

**Evidence:** HIGH_VOL_TREND: 15 trades, PF 1.93. NEUTRAL: 11 trades, PF 1.19. LOW_VOL_TREND: zero trades. HIGH_VOL_MR: 2 trades; LOW_VOL_MR: 1 trade.

**Relationship:** Regime classification.

**Confidence:** Low-medium.

**Framework status:** Partially implemented.

**Future importance:** High.

---

## DISC-015 — Grid/basket mechanics introduce concentrated tail risk

**Source files:** `MAE_MFE.py`; `deep_analysis.py`; `cluster.py`; `trade_clusters.csv`; `analyze_basket_depth.py`; `analyze_grid_spacing.py`.

**Research question:** What does recovery/grid clustering contribute to performance and failure?

**Finding:** Most clusters are profitable, but losses are highly concentrated in a small tail. This is a risk-architecture discovery, not proof that grid recovery should remain part of the strategy.

**Evidence:** 7,525 clusters; 99.39% marked win clusters. Median cluster PnL 38.64, but minimum -5,234.54. Median trade count is 8; 99th percentile trade count 35, maximum 63. Maximum lot reaches 10.24 versus median 0.08.

**Relationship:** Execution robustness; risk; exit optimization.

**Confidence:** High for tail concentration.

**Framework status:** Not implemented as a safe portfolio/risk control.

**Future importance:** Critical.

---

## DISC-016 — MAE/MFE files document asymmetric excursion risk

**Source files:** `MAE_MFE.py`; `trades_mae_mfe.csv`; `trades_with_mae_mfe.csv`.

**Research question:** How adverse and favorable excursions relate to trade outcomes and sizing?

**Finding:** The two exports are not interchangeable: one is 64,246 rows with mean PnL 0.93 and max loss -69.4; the other is 72,966 rows with mean PnL 8.85 and max loss -2,201.6. This signals distinct extraction/definition pipelines and prevents unqualified merging of their conclusions.

**Evidence:** `trades_with_mae_mfe.csv` has MAE minimum -4,556.8 and MFE minimum -2,524.16; `trades_mae_mfe.csv` records MAE as mostly positive values with a different convention. Both contain extreme lot-size tails up to 10.24.

**Relationship:** MAE/MFE; risk; exit optimization.

**Confidence:** High for data-definition inconsistency; no direct performance conclusion should be combined.

**Framework status:** Not implemented.

**Future importance:** High.

---

## DISC-017 — Entry replication investigated simple indicator explanations

**Source files:** `entry_replication_test.py`; `synthetic_clone.py`.

**Research question:** Can historical EA entries be reconstructed by stochastic-only, stochastic-cross, momentum, candle-count, or SMA rules?

**Finding:** The script tests these competing simple models against logged entry timestamps, preserving the conclusion-seeking method. No archived output is present, so no winner should be claimed.

**Evidence:** Models include stochastic threshold/cross, momentum, three-candle, and SMA filters; overlap with actual entries is the metric.

**Relationship:** Virtual signal; model identifiability.

**Confidence:** Unknown.

**Framework status:** Not implemented.

**Future importance:** Medium.

---

## DISC-018 — Time, basket depth and grid spacing were investigated as EA behavior forensics

**Source files:** `analyze_time_pattern.py`; `analyze_basket_depth.py`; `analyze_grid_spacing.py`; `extract_mt5_ea_data.py`; `market.py`.

**Research question:** What mechanical structure can be recovered from MT5 EA logs?

**Finding:** The scripts quantify second-of-minute timing, same-timestamp basket depth, sell-entry price spacing, order fields, and basket TP events. Their outputs are absent, so these are preserved as documented research questions, not findings.

**Evidence:** Methodology survives in code; no corresponding summary files remain in the permitted scope.

**Relationship:** Execution forensics; grid/basket behavior.

**Confidence:** Unknown.

**Framework status:** Unknown.

**Future importance:** Medium.

---

## DISC-019 — Time-to-reversion and hold duration are part of the behavioral signature

**Source files:** `Research.docx`; `yuvi_master_trade_log.csv`; `recoil_profile_analysis.csv`.

**Research question:** Does a profitable response occur quickly enough to be an operational filter?

**Finding:** The journals characterize fast recoil as the distinguishing behavior. The master trade log’s mean holding period is 11.6 bars (median 11.5), while recoil profile records early bars 3/5/10.

**Evidence:** Strong winners have positive early recoil at all three horizons; scratches are negative on average at all three.

**Relationship:** Recoil; exit optimization; persistence.

**Confidence:** High for the selected profile, medium for universal thresholds.

**Framework status:** Partially implemented.

**Future importance:** High.

---

## DISC-020 — Live validation remains the decisive unresolved scientific test

**Source files:** both journals; `real_trade_monte_carlo.csv`; `extract_mt5_ea_data.py`.

**Research question:** Do historical and simulated results survive actual broker execution?

**Finding:** No permitted artifact demonstrates forward live validation, real fills, or live slippage beyond simulation. The journals themselves list this limitation.

**Evidence:** The stress and Monte Carlo tests are favorable, but no live result dataset or audited forward period is present.

**Relationship:** Execution robustness; live validation.

**Confidence:** High that this is a gap.

**Framework status:** Not implemented.

**Future importance:** Critical.

---

## File-level coverage and duplicate grouping

| Research group | Supporting files | Preserved conclusion/status |
|---|---|---|
| Behavioral signal and confluence | `yuvi_eur.py`, `yuvi_x_v01.py`, `test-14.py`, both journals | DISC-001/002/003/006/013; implemented/partial. |
| Virtual entry/recoil/persistence | `entry_forensics.py`, `tick_entry_forensics.py`, `entry_replication_test.py`, `synthetic_clone.py`, `mr_buy_subregimes.py`, `recoil_profile_analysis.csv` | DISC-004/005/008/017; partial. |
| Exit and excursion analysis | `MAE_MFE.py`, `deep_analysis.py`, `trades_mae_mfe.csv`, `trades_with_mae_mfe.csv`, `yuvi_master_trade_log.csv` | DISC-007/016/019; partial. |
| Grid/basket/EA forensics | `cluster.py`, `trade_clusters.csv`, `analyze_*`, `extract_mt5_ea_data.py`, `market.py`, `reconstructed_trades.csv` | DISC-015/018; not implemented/unknown. |
| Regime research | `regime_classifier.py`, `regime_edge_matrix.py`, `meta_regime_results.csv` | DISC-002/014; partial and sample-limited. |
| Robustness and validation | `robustness_expansion_results.csv`, `randomized_stress_test_results.csv`, `walk_forward_results.csv`, `yearly_robustness_results.csv`, `real_trade_monte_carlo.csv`, `monte_carlo_distribution.csv` | DISC-009/010/011/012; partial. |

## Final summary

### Top 20 permanent discoveries

DISC-001 through DISC-020 are the permanent discoveries, including negative and contradictory evidence rather than only positive claims.

### Ten discoveries already embedded in QuantForge (conceptual/partial)

1. Validated-data-before-analysis discipline.
2. Market DNA / volatility and structure measurement.
3. Adaptive strategy selection.
4. Signal confidence gating.
5. Behavioral mean-reversion orientation.
6. Recoil-aware signal logic.
7. Persistence/confirmation concept.
8. Risk gating and trade-plan separation.
9. Execution-layer separation from intelligence.
10. Deterministic research recording/validation intent.

### Ten discoveries still missing or only partially represented

1. Explicit virtual-signal → real-entry lifecycle.
2. Quantified recoil horizon thresholds.
3. Quantified persistence-hold thresholds.
4. Regime classifier with adequately powered validation.
5. Session/clock filters backed by retained output.
6. Live forward validation and fill-quality archive.
7. Portfolio/cross-instrument correlation controls.
8. Tail-risk controls for grid/basket concentration.
9. Harmonized MAE/MFE definitions and reporting.
10. Reproduction of the cross-market performance tables from source datasets.

### Research confidence assessment

**Overall: medium-high for a behavioral hypothesis; medium for deployable performance claims.** Recoil/persistence, stress, and later walk-forward evidence are internally consistent. Confidence is reduced by selected-sample reporting, sparse early years, small regime/NASDAQ cells, differing MAE/MFE conventions, and absence of live forward evidence.

### Architecture fidelity

The current architecture remains faithful to the research at a high level: validation → market characterization → adaptive decision → signal → risk → execution. It does not yet fully embody the research’s virtual-signal, quantified recoil/persistence, regime, and live-validation knowledge. Those omissions are implementation gaps, not evidence that the architecture contradicts the research.
