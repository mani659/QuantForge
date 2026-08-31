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

## DISC-021 — Canonical event studies: XAGUSD asymmetry is statistically observable but economically non-viable

**Source files:** `output/event_study_v1/`, `output/event_study_v2/`, `output/event_study_v3/` (protocols, run scripts, event datasets, final reports); `output/xagusd_cost_viability_v1/` (protocol, `final_cost_viability_report.md`, `event_cost_matched.csv`); `data/tick/XAGUSD_mt5_ticks.csv`; `data/m1/XAGUSD_M1.csv`.

**Research question:** Does the extreme short-term displacement → recoil → persistence behavioral hypothesis, retained from the original corpus, constitute a deployable and economically viable mean-reversion edge?

**Finding:** The hypothesis is **statistically observable in a narrow, direction-specific sense** — XAGUSD downward displacement is followed by positive direction-adjusted return under pre-registered, dependence-aware definitions — but it is **economically non-viable**: observed tick-level bid/ask transaction costs consume essentially the entire gross effect, leaving no defensible margin for commission, slippage, or broker variation. Statistical detectability does not establish economic viability. The Mean-Reversion research line is formally **CLOSED for deployment promotion** under the current evidence.

**Classification: RESEARCH FINDING / ECONOMICALLY NON-VIABLE.** The XAGUSD effect is NOT retained as a validated trading strategy, a production detector, a production threshold, a BOE runtime semantic, or a deployable edge.

**Evidence (QuantForge-internal canonical studies, 2026-08, all pre-registered before outcome inspection):**

- **V1** (`output/event_study_v1/`, 27,297 events, 5 markets): the initial operationalization (rolling price z-score) found no robust out-of-sample cross-market reversion — only 2/30 partition-level cells distinguishable from chance; no stable threshold region; GATE 1 FAILED.
- **V2** (`output/event_study_v2/`, 83,307 events): alternative normalizations (N1 price-z, N2 ATR-relative, N3 return-based), regime/walk-forward, pre-registered persistence, Holm multiplicity control — one coherent lead emerged: XAGUSD (N1 pooled Holm survivor p_holm=0.0135; matched-quantile significant in both directions under N1/N2). Single-market; persistence effect later found mechanically confounded; GATE 1 PARTIALLY PASSED — NOT PROMOTABLE.
- **V3** (`output/event_study_v3/`, 34,348 events): adversarial confirmation of the XAGUSD lead only — F1 (N1 DOWN) +0.00109, p_holm=0.006, the single Holm survivor of a 12-test family with a clean EURUSD negative control; stable monotone threshold region 2.5–3.5 (not a spike); positive in all walk-forward folds and all chronological thirds; direction/magnitude consistent on the reused TEST holdout but narrow-CI insignificant (p=0.167; no fresh holdout exists); leakage-free entry-at-confirmation persistence added no discrimination; directionally asymmetric (UP only at matched rarity); single-market with no mechanistic justification. GATE 1 FAILED — EVIDENCE INSUFFICIENT. Break-even round-trip cost ≈ 10.9 bp was the decisive unknown.
- **Cost Viability V1** (`output/xagusd_cost_viability_v1/`): **data correction — the repository DOES contain observed XAGUSD bid/ask tick data covering the research period** (`data/tick/XAGUSD_mt5_ticks.csv`, 146.4M ticks, 2021-07-13 → 2026-07-12), overturning the earlier assumption that no observed spread data existed. Primary cell (N1 DOWN, VALIDATION): gross +10.66 bp/2h (full population +10.86 bp, matching V3); observed round-trip spread cost median 9.09 bp, mean 9.89 bp, P90 11.42 bp, P99 36.15 bp; net +0.77 bp with dependence-aware cluster-bootstrap 95% CI [−3.78, +5.40] spanning zero; net success rate 52.6%; conservative full-spread-per-side model net −9.1 bp; a minimal 2+2 bp unobserved commission/slippage band already flips even the median case negative. **NON-VIABLE** under the pre-registered decision rule (net CI spans zero at median cost; P90 cost exceeds break-even).

**Relationship:** Behavioral mean reversion; economic viability; execution costs; negative-result record.

**Confidence:** High that the negative economic conclusion is correct for this operationalization (observed costs, not assumptions); high that the XAGUSD DOWN asymmetry is statistically real in the narrow pre-registered sense. Cross-market portability is absent and the market-specificity mechanism is unresolved — both moot for promotion.

**Framework status:** Research finding only. The line did NOT establish production values for: detector trigger; production threshold; detector parameter schema; detector lifecycle; production recoil semantics; production persistence semantics. No V1/V2/V3 parameter is promoted into BOE configuration.

**Future importance:** Critical as a boundary-setting negative result. It prevents future sessions from reinterpreting the XAGUSD lead as an unresolved opportunity and restarting curve-fitting, documents the observed bid/ask dataset as a foundation asset, and establishes that future hypotheses must demonstrate margin against observed execution costs before promotion.

---

## DISC-022 — Fixed 12/1 TSMOM candidate fails cross-era incremental replication

**Source files:** `output/tsmom_v1/` (protocol v1.0.3, `run_tsmom_v1.py`, `results_TSMOM_V1.json`, `SCIENTIFIC_REPORT_TSMOM_V1.md`); `output/tsmom_v2/` (protocol v2.0.0, `run_tsmom_v2.py`, `experiment_metadata_TSMOM_V2.json`, `assessment_events_TSMOM_V2.csv`, `incremental_monthly_TSMOM_V2.csv`, `bootstrap_TSMOM_V2.csv`, `negative_controls_TSMOM_V2.csv`, `cost_analysis_TSMOM_V2.csv`, `results_TSMOM_V2.json`); historical panel acquisition/fingerprint records (`HPD_MANIFEST.csv`, `HPD_CONTRACT_HASHES.csv`, `FINAL_CLASSIFICATION.csv`, `PER_MARKET_VALIDATION.csv`); `data/m1/{XAUUSD,EURUSD,BTCUSD,XAGUSD,USATECHIDXUSD}_M1.csv`; `docs/SESSION_HANDOFF.md`.

**Research question (V2, drift-controlled):** Does the fixed 12-month-lookback / 1-month-skip / 1-month-hold TSMOM signal add incremental predictive value above a same-universe, same-weight all-long drift benchmark, across the validated historical and contemporary panels?

**Finding:** The historical panel shows a real **incremental** effect: F1 (TRAIN+VALIDATION, 148 months) `ΔΠ = Π_tsmom − Π_long` ≈ **+0.67% per month**, 95% CI lower bound positive, Holm-adjusted one-sided p ≈ **0.038** (family {F1, Layer-B}); the effect is broad (21/28 markets positive; all leave-one-market-out and leave-one-class-out values positive) and all three pre-registered negative controls (NC1 paired direction rotation, NC3 24-month long-lag shift, NC4 calendar-block null) are clean. **However, the contemporary replication (2021–2026, 5 markets, T = 54) contradicts the historical direction**: `ΔΠ` ≈ **−1.10% per month** (CI upper bound +0.09%), with the all-long benchmark strongly positive (≈ +3.02%/month, p ≈ 0.001) and TSMOM failing to beat it. The frozen promotion gate requires cross-era directional consistency (Condition 8); **Condition 8 FAILS**, so the candidate is **NOT PROMOTABLE / TSMOM REMAINS UNRESOLVED**. Scientific classification: **PARTIALLY REPRODUCED**. The line is formally **CLOSED** as a QuantForge-promotable candidate.

**Classification: RESEARCH FINDING / CLOSED — NOT PROMOTABLE.** This is a boundary-setting negative result for the *fixed 12/1 TSMOM operationalization within QuantForge*. It does NOT claim that trend following or momentum in general does not work; the external AQR/MOP and HOP literature remains historical context and is not disproven.

**Evidence (QuantForge-internal pre-registered studies, 2026-08):**

- **TSMOM V1** (`output/tsmom_v1/`, 5-market contemporary-only panel, 219 assessments): Scientific **INCONCLUSIVE** / Economic **NOT CONFIRMED**. F1 absolute-return mean ≈ +1.51%/month with 95% CI **[−2.53%, +4.54%]** including zero (p ≈ 0.2375); the formal NC2 (6-month time-shifted signal) produced a *stronger* association (mean ≈ +3.93%/month, CI excluding zero), showing the positive point estimates could not be separated from unconditional drift / long-biased composition; long-biased XAUUSD and USATECHIDXUSD dominated; only 21 pooled flips.
- **TSMOM V2 — historical Layer A** (`output/tsmom_v2/`, 28-market validated HPD panel, common window 1987-01-13 → 2002-08-30, 175 position months, 4,900 market-months, 552 pooled flips): F1 `ΔΠ` ≈ +0.67%/month, 95% CI ≈ [+0.03%, +1.54%], one-sided p ≈ 0.019, Holm ≈ 0.038; all-long drift book itself ≈ +0.71%/month (drift is a material component of absolute TSMOM ≈ +1.39%/month). Long exposure ≈ 53%; mean |cross-market corr| ≈ 0.07–0.11 (inference used month-vector calendar block bootstrap, not independent-row counts). NC1 fraction-null-≥-observed ≈ 0.0001; NC3 lagged-signal effect negative (no persistence beyond the construction horizon); NC4 ≈ 0.037.
- **TSMOM V2 — historical F2 (TEST, 27 months, consumed once):** `ΔΠ` ≈ +0.34%/month, positive direction, 95% CI includes zero, p ≈ 0.120 — corroborative only, never re-used.
- **TSMOM V2 — contemporary Layer B** (5 markets, T = 54): `ΔΠ` ≈ **−1.10%/month** (net-of-observed-MT5-cost ≈ −1.11%/month), one-sided p ≈ 0.971; all-long ≈ +3.02%/month with CI excluding zero — the drift benchmark dominates and the incremental signal is directionally **opposite** the historical panel.
- **Promotion gate (frozen, all 8 conditions):** conditions 1–7 pass (F1 mean > 0; F1 CI LB > 0; Holm-adjusted p < 0.05; positive vs all-long; not single-market; not single-class; clean negative controls). **Condition 8 (contemporary directional consistency) FAILS.** Final: NOT PROMOTABLE.

**Relationship:** Drift-controlled incremental identification; cross-era / cross-dataset transfer; dependence-aware inference; negative-result record. Extends the V1 identification-failure register (drift confounding) into a fully controlled historical + contemporary adjudication. Distinct from but complementary to DISC-021 (economic non-viability): here the decisive problem is **lack of stable incremental signal across eras**, not transaction costs.

**Confidence:** High that the historical incremental effect is real within its historical sample (dependence-aware CI, clean controls, broad market breadth). High that the contemporary result contradicts the required cross-era consistency (direction, not just noise; all-long strongly positive). High that the closure decision is correct for the tested candidate. The economics are NOT the reason for closure (historical costs unobserved by design; contemporary economics NOT CONFIRMED but secondary).

**Framework status:** Research finding only. No TSMOM detector, no runtime parameter, no BOE semantic, no Assembly/Deployment/StrategyManifest value, and no lookback/horizon/weighting/market-selection regime was ever promoted. TEST consumed exactly once. The research-to-runtime firewall held throughout V1 and V2.

**Future importance:** Decisive boundary-setting record. Prevents future sessions from restarting the *fixed 12/1* TSMOM candidate merely because the historical result was statistically positive. Any future trend/momentum work is a **new independent hypothesis** and must enter through Research Hypothesis Selection from zero — it cannot be a V3 of this line. Preserves the distinction between "this candidate did not establish a stable edge" and "trend following does not work."

---

## DISC-023 — H01 Equity V1: US-tech cross-era replication established; broad-US historical evidence gap remains

**Source files:** `output/research_discovery/H01_EQUITY_VOLATILITY_ASYMMETRY/` (protocol v1.1.0 `H01_EQUITY_VOLATILITY_ASYMMETRY_PROTOCOL_V1.md` SHA-256 `a97cd0e2…`; `run_h01_equity_v1.py`; `experiment_metadata_H01_EQ_V1.json`; `results_H01_EQ_V1.json`; `class_stats_H01_EQ_V1.csv`; `per_market_stats_H01_EQ_V1.csv`; `matched_pairs_H01_EQ_V1.csv`; `bootstrap_replicates_H01_EQ_V1.csv`; `daily_series/`; `SCIENTIFIC_REPORT_H01_EQ_V1.md`); `output/research_discovery/H01_EQUITY_V1_SCIENTIFIC_ADJUDICATION.md`; the Track-A chain (screening, scope decision, data-source audit, data-acquisition report, definition lock); H01 v1.2 protocol/report/adjudication; frozen HPD validation records (`FINAL_CLASSIFICATION.csv`, `PER_MARKET_VALIDATION.csv`, `HPD_MANIFEST.csv`).

**Research question:** Does the classic negative-shock volatility-response asymmetry (forward ΔlnRV response conditioned on pre-shock volatility state, magnitude-matched negative vs positive daily shocks) generalize beyond the two single-market equity observations seen in H01 v1.2 — across a validated multi-market US equity universe?

**Finding:** The US-anchored replication is **strongly supported within its registered scope**: 3 of 4 cells SUPPORT at the family-level significance floor (all p_raw = 0.00010 = 1/10001, count = 0/10,000 null draws ≥ |D_obs|; all p_Holm = 0.0004), 1 cell EVIDENCE-LIMITED, 0 CONTRADICTION, 0 INCONCLUSIVE. The **US-tech exposure (NASDAQ100 + NASDAQCOM) replicates across two eras** (historical 1986-2002 and contemporary 2016-2026, both two-market SUPPORT) — the registered strong cross-era replication condition is met. The **broad-US exposure** is SUPPORT contemporarily (SP500 + DJIA, D = +0.316) but EVIDENCE-LIMITED historically (`sp` only, D = +0.150 descriptive; the frozen ≥2-market rule withholds a primary verdict from a single-market cell). **Not established:** generalization across US equity-index markets broadly, and any international claim (outside the US-anchored scope by decision).

**Classification: SCIENTIFICALLY CONFIRMED / ECONOMIC TRANSLATION CLOSED — ECONOMIC FAILURE (DISC-023).** The experiment earned the claim that classic asymmetry is strongly supported in the tested US-tech exposure and replicates across eras. However, the registered Q1 / 11-day economic translation failed the mandatory dual-era gate. Economic failure does not invalidate the H01 scientific finding.

**Evidence (pre-registered, outcome-blind; executed exactly once):** 
- Scientific: EQBROAD_L1 D = +0.150 CI [0.079, 0.193]; EQBROAD_L2 D = +0.316 CI [0.234, 0.389]; EQTECH_L1 D = +0.208 CI [0.154, 0.264]; EQTECH_L2 D = +0.330 CI [0.236, 0.392]. 
- Economic: The registered Q1 / 11-day economic translation failed the mandatory dual-era gate. Historical: FAIL — Δ = -0.00143921, 95% CI entirely below zero. Contemporary: PASS — Δ = +0.00077702, 95% CI entirely above zero. Overall: ECONOMIC FAILURE. The historical/contemporary divergence must be preserved exactly as evidence.

**Relationship:** Volatility-response asymmetry (leverage-effect literature prior: Black 1976; GJR 1993; Engle–Ng 1993; Aït-Sahalia–Fan–Li 2013); asset-class-specific replication; cross-era replication discipline (mirrors the TSMOM Condition-8 standard); dependence-aware inference; negative economic translation record.

**Confidence:** High that the US-tech cross-era scientific replication is real within the registered design. High that the economic translation is an ECONOMIC FAILURE due to a clear fail on the historical leg under frozen execution (EXEC_04).

**Framework status:** Scientific finding only. No detector, no runtime parameter, no BOE semantic, no trading strategy, and no regime filter use is authorized. 

**Closure basis (2026-08-23):** The registered Q1/11-day economic translation yielded negative returns across all market segments in the Historical era (1982–2002) but yielded uniformly positive returns in the Contemporary era (2016–2026). It categorically failed the dual-era stability gate. **This closure does not falsify the H01 phenomenon.** The classic volatility-response asymmetry remains scientifically supported. The economic translation track is closed because the registered rule failed to produce a stable cross-era edge.

**Future importance:** Establishes the strongest equity-specific result in the H01 program and defines its exact boundary (US-anchored, two exposures, tech replicated) while serving as a boundary-setting negative economic result. Prevents future sessions from (a) overclaiming economic viability, (b) rescuing the translation via contemporary-only markets, parameter tuning, or post-hoc threshold searching, (c) reopening H01 Equity Track A without a new explicit research proposal, or (d) interpreting the economic failure as a scientific contradiction. The scientific and economic findings are frozen. H01 Equity Track A is CLOSED.

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

## DISC-024 - Session-Anchored Range Expansion (USATECHIDXUSD): Contradicted

**Relationship:** Behavioral edge screening candidate; independent test of volatility state transition.

**Candidate Name:** Session-Anchored Range Expansion

**Why screened:** To evaluate if extreme pre-session range compression (overnight/European session) reliably precedes increased cash-session range expansion.

**Execution Artifacts:**
- Definition Lock: `output/research_discovery/SESSION_RANGE_EXPANSION_DEFINITION_LOCK_V1.md`
- Protocol: `output/research_discovery/SESSION_RANGE_EXPANSION_EVENT_STUDY_PROTOCOL_V1.md`
- Execution: `output/research_discovery/SESSION_RANGE_EXPANSION/EXECUTION_REPORT_V1.md`
- Adjudication: `output/research_discovery/SESSION_RANGE_EXPANSION_SCIENTIFIC_ADJUDICATION_V1.md`

**Final Verdict:** CONTRADICTED. Extreme pre-session compression (<= trailing 63-day 25th percentile) was associated with significantly *lower* subsequent normalized cash-session range than the control group. 

**Exact Next Disposition:** CLOSED.
- The hypothesis is falsified for this asset and definition.
- **PROHIBITION:** Do not tune parameters, test K-means, or invent a replacement hypothesis to rescue this candidate.

---

## DISC-025 — Liquidity Sweep / Reversal: behavioral discovery supported, minimal executable translation economically non-viable, line CLOSED

**Source files:** `output/research_discovery/XAUUSD_LIQUIDITY_SWEEP_REVERSAL/` (v1.2.0 event study; event CSVs for XAUUSD/XAGUSD/USATECHIDXUSD/BTCUSD; `SCIENTIFIC_REPORT_V1.md`); `XAUUSD_LIQUIDITY_SWEEP_REVERSAL_EVENT_STUDY_PROTOCOL_V1.md` (v1.2.0, SHA-256 `c6b8fbd4…`); `XAUUSD_LIQUIDITY_SWEEP_REVERSAL_FINAL_CLEARANCE_AUDIT_V1.md`/`_V2.md`; `XAUUSD_LIQUIDITY_SWEEP_REVERSAL_SCIENTIFIC_ADJUDICATION_V1.md`; `LIQUIDITY_SWEEP_STRATEGY_ECONOMIC_TRANSLATION_V1.md`; `LIQUIDITY_SWEEP_POST_ECONOMIC_GOVERNANCE_ADJUDICATION_V1.md`; `LIQUIDITY_SWEEP_RESEARCH_LINE_CLOSURE_GOVERNANCE_RECORD_V1.md`; `data/m1/*_M1.csv`; observed MT5 bid/ask `data/tick/{XAUUSD,XAGUSD,USATECHIDXUSD,BTCUSD}_mt5_ticks.csv`; `output/xagusd_cost_viability_v1/xagusd_minute_aggregates.csv` (XAGUSD).

**Research question:** Does a deterministic sweep of a prior Asian-session extreme, followed by wick rejection and micro-structural reversal confirmation, produce a statistically larger subsequent 120-minute directional excursion than the registered rejected-sweep control group — and, if so, does the minimal executable translation survive the economics of actually trading it?

**Finding:** The behavioral phenomenon is **statistically supported in all four evaluable markets** — XAUUSD, XAGUSD, USATECHIDXUSD, BTCUSD (all Holm-adjusted p = 3.9996e-04 < 0.05, ΔM_obs > 0, CIs far from zero; event counts 984–1,960 treatment / 39–117 control; three economically distinct mechanisms: precious metals, equity-index CFD, crypto). EURUSD is **DATA-LIMITED / NOT ADJUDICATED** (16.96% invalid-day fraction > 10% gate, halt before inference). The minimal executable translation — **confirmation-close entry, reversal-direction trade, structural sweep-extreme stop, 120-minute-close exit, fixed notional** — is **ECONOMICALLY NON-VIABLE in all four markets and gross-negative BEFORE transaction costs** (median gross per trade: XAUUSD −5.3 bp, XAGUSD −11.6 bp, USATECHIDXUSD −5.0 bp, BTCUSD −11.8 bp; win rates 19–26%; stop-out rates 70–80%; negative in every year and both chronological halves of every market; observed MT5 spreads exact-minute ≥ 98.3%). Failure mechanism: **TRANSLATION FAILURE** (the validated excursion is anchored at the swept Asian level; the confirmation-close entry sits 4.7–13.2 bp beyond the level, the structural stop converts the intra-window reversion into losses, and the horizon-close exit misses the MFE extreme) — not a cost failure, and behavioral failure is not established.

**Classification: RESEARCH FINDING — BEHAVIORALLY SUPPORTED / ECONOMICALLY NON-VIABLE (registered minimal translation) / LINE CLOSED.** The behavioral discovery is preserved as real; the candidate is closed for trading purposes. Under the strict alternative-selection rule, no alternative translation (limit entry at the Asian level, next-bar-open entry, Asian opposite-boundary target, trailing exit) has a justification that predates the economic result and derives from the frozen behavioral object, so **no alternative economic protocol is authorized**.

**Evidence (pre-registered, outcome-blind; 2026-08):** behavioral ΔM_obs / 95% CI: XAUUSD 4.057 [3.477, 4.582]; XAGUSD 0.101 [0.086, 0.114]; USATECHIDXUSD 39.787 [32.805, 47.219]; BTCUSD 229.100 [188.699, 263.300]; all p_raw = 1/10001 (floor, count = 0 of 10,000 null draws), all p_Holm = 3.9996e-04; B = 10,000, L = 10, seed = 20260817; stationary day-cluster block bootstrap; null-imposing recentered construction ΔM*_null = ΔM* − ΔM_obs; percentile sampling CI separate from null p. Economic translation: baseline registered before computation, zero tuning, manually validated trade-by-trade; observed cost model RT(A) median 1.05–16.77 bp across markets; net A+0 median −7.2 to −27.5 bp; cumulative net (A+4) −5,929 to −39,553 bp; max drawdown ≈ full cumulative loss. Reproducibility caveats on record: the behavioral execution's bootstrap/null draw files, metadata JSON, and execution script were not persisted (observed statistics, counts, and input hashes verified from persisted artifacts; inference layer internally consistent but not recomputable from draws); the EURUSD halt's exact invalid-day operationalization (≈600-bar/day minimum coverage; 291/1,716 days) is not uniquely pinned by the registered §17 text.

**Relationship:** Behavioral edge screening candidate (auction-mechanics stop-run/reversal hypothesis); cross-market validation; economic viability; negative-result record. Distinct from but complementary to DISC-021 (economic non-viability under observed costs — here the failure is the entry/stop/exit mapping, gross before costs), DISC-022 (cross-era replication failure), DISC-023 (H01 Equity), and DISC-024 (session range, contradicted).

**Confidence:** High that the behavioral phenomenon is statistically real within the registered design (Holm-corrected, four markets, three mechanisms, directionally consistent). High that the minimal executable translation is economically non-viable (gross-negative before costs, uniform across markets/years/halves, observed-spread-confirmed). Not established: whether any other executable mapping could capture the excursion (untested; not authorized), and any FX statement (EURUSD data-limited).

**Framework status:** Research finding only. No detector, no runtime parameter, no BOE semantic, no Assembly/Deployment/StrategyManifest value, no trading signal, no EA. The behavioral protocol, event CSVs, adjudications, and economic artifacts are the permanent record; nothing crossed into runtime.

**Future importance:** Boundary-setting negative result. Prevents future sessions from (a) reviving the sweep/reversal candidate by retesting entry/exit/stop variants, (b) inverting or rescuing the hypothesis, (c) building an EA from the closed translation, or (d) reinterpreting the EURUSD data-limit as a hypothesis result. Preserves the distinction between "the behavior is real" and "the behavior is tradable."

---

## DISC-026 — Opening Range Breakout (ORD): Scientifically Supported / Economic Translation Closed

**Source files:** `output/research_discovery/ORD_OPENING_RANGE_DEFINITION_LOCK_V1.md`, `ORD_OPENING_RANGE_EVENT_STUDY_PROTOCOL_V1_AMENDED.md`, `ORD_V1_1_0_GOVERNANCE_APPROVAL_FREEZE.md`, `ORD_SCIENTIFIC_RESULTS_ADJUDICATION_V1.md`, `ORD_ECONOMIC_TRANSLATION_PROTOCOL_V2_1_AMENDED.md`, `ORD_ECONOMIC_EXECUTION_STAGING_DESIGN_V1.md`, `ORD_ECONOMIC_STAGE0_PREFLIGHT_20260822T113645Z.md`, `output/research_discovery/ORD_STAGE2_XAGUSD_EXEC_01`.

**Research question:** Does an Opening Range Breakout (ORD) strategy produce statistically significant scientific edge, and can it be translated into an economically viable staged execution model?

**Finding:** The scientific hypothesis is **SCIENTIFICALLY SUPPORTED**. The adjudication artifact confirms 3/3 evaluable registered markets (XAUUSD, XAGUSD, USATECHIDXUSD) passed the Holm-adjusted threshold. However, the exact **XAGUSD REGISTERED ECONOMIC TRANSLATION — ECONOMICALLY NON-VIABLE / CLOSED**.
Execution `ORD_STAGE2_XAGUSD_EXEC_01` (EXECUTION_20260824T130709Z_0c18d950-aa99-4e90-af55-6847f8134542) generated 2,176 trades across the exact frozen Stage-1 preparation (source SHA: `edccad88ed5b74caf16a14203f3cf743306c65f2ebc5004cf566ed61deeb6e17`). The result is strictly negative: median net -12.404 bp, mean net -9.064 bp, cumulative -19,723.0 bp, Win Rate 9.1%, PF 0.356, Dev median -14.162 bp, OOS median -10.355 bp. Protocol gates for economic viability uniformly failed. Yearly results were unequivocally negative from 2021-2025.

**Classification: RESEARCH FINDING — SCIENTIFICALLY SUPPORTED / ECONOMICALLY NON-VIABLE (registered XAGUSD object) / LINE CLOSED.**
The negative economic result applies to the registered XAGUSD economic object and does not invalidate the underlying scientific finding. This does not claim universal non-viability, that all markets fail, that ORD can never produce an economic edge, or that the scientific mechanism is false.

**Framework status:** Research finding only. The scientific finding is positive; the economic execution is uniformly negative. No runtime implementation is authorized.

**Future importance:** Prohibits reviving the XAGUSD ORD strategy without a fundamentally different execution model. Protects the scientific finding while cleanly closing the economic branch.

---

## DISC-027 — Research Factory V2 G1 Cycle (2026-08-25): Invalid / Non-Adjudicable

**Source files:** `RESEARCH_FACTORY_V2_G1_SCREEN_20260825.md`, `RESEARCH_FACTORY_V2_G1_INTEGRITY_AUDIT_20260825.md`, `RESEARCH_FACTORY_V2_G1_INVALIDITY_20260825.md`.

**Research question:** Do candidates CAND-G0-001 through CAND-G0-004 possess sufficient observed economic headroom to justify a G2 pilot?

**Finding:** **INVALID / NON-ADJUDICABLE**. The G1 implementation failed the integrity audit due to systematic calculation of Maximum Favorable Excursion (MFE) instead of deterministic executable exit, inclusion of pre-entry (breakout) excursion, silent parameter proxy substitution, and undocumented event downsampling. 

**Classification: RESEARCH-FACTORY GOVERNANCE FINDING / NON-ADJUDICABLE.** Do NOT give the four candidate mechanisms a negative scientific verdict. The execution itself was invalid.

**Program-level lesson:** G1 executable-capture contract strengthened after discovery of systematic MFE/pre-entry and definition-proxy errors. G1 cannot be outcome-driven or approximate; it must adhere exactly to the defined trigger, entry, and exit.

## Final summary
**Source events:** CAND-G0-010 event-state duplication failure (2026-08-25).

**Methodological finding:** Repeated event occurrence is not itself the edge. The research objective is to estimate conditional post-event behavior and determine whether that conditional distribution produces positive mathematical expectancy after executable costs. Event persistence must not be counted as repeated independent opportunities. Any state-based event machine must explicitly enforce Opportunity Integrity (event onset, completion, re-arm, duplicate suppression) before execution.

---

## METHODOLOGICAL LESSON: V5 G1 Screening and Conditional Edge

**Source events:** V5 G1 Screening Cycle (2026-08-25).

**Findings:**
- **CAND-012 (Trend-Pullback Re-Acceleration):** G1 ECONOMICALLY INSUFFICIENT / CLOSED.
- **CAND-013 (Macro-Shock Volatility Reset Continuation):** G1 ECONOMICALLY INSUFFICIENT / CLOSED.

**Methodological Lessons:**
1. **Opportunity Integrity Confirmed:** The V5 implementations correctly enforced event identity: duplicate 20-EMA touches and overlapping volatility resets were suppressed. This demonstrates that the Opportunity Integrity correction introduced after CAND-010 is functioning.
2. **Conditionalization Limits:** Conditionalization does not create an edge by itself. A candidate may define a plausible state variable, yet the conditional return distribution can remain economically negative. Therefore, Event → KPI state → conditional return must be evaluated empirically rather than assumed.
3. **Frequency Considerations:** A structurally interesting event is not necessarily a tradeable discovery object if its valid occurrence frequency is too low. Frequency must be judged relative to holding period, turnover, target deployment, and expected opportunity rate.

## DISC-027 — CAND-015: Nasdaq-Crypto Information Absorption Lag

**Classification: RESEARCH FINDING — SCIENTIFICALLY SUPPORTED / ECONOMICALLY VIABLE / G5 HISTORICAL REPLAY VALIDATED / G6 REPLAY HARNESS VALIDATED.**

CAND-015 = scientifically supported + economically viable + historical production-style replay validated + G6 replay harness validated.

True forward validation blocked by absent real-time/demo data feed.

No CAND-015 strategy changes occurred.
## DISC-028 — Governance: Parallel Forward Validation and Discovery

**Relationship:** Parallelization of forward validation and discovery research.

**Status:** The CAND-015 forward observation is a protected validation track. The running observation must remain untouched until its complete log is available. No scientific or economic conclusion may be drawn from the partial 7-day forward observation before the session is complete and independently audited.

**Parallel Track:** In parallel, the Research Factory V2 is ACTIVE at G0 — Candidate Generation. New research must not influence the CAND-015 forward observation, and partial CAND-015 forward results must not be used to select new candidates.

## DISC-029 — Research Factory V2 G0 Cycle (V7)

**Relationship:** Tradeable Edge Discovery Screening.

**Status:** The V7 G0 candidate generation cycle was completed, promoting candidates CAND-G0-018, CAND-G0-019, and CAND-G0-020 to G1. 

**Outcome:** Recorded as a research-screening milestone. Do NOT create a scientific finding from G0 alone. Do NOT claim economic support. Do NOT claim strategy viability.

## DISC-030 — Research Factory V2 G1 Cycle (V7)

**Relationship:** Tradeable Edge Discovery Screening.

**Status:** The V7 G1 Economic Plausibility Screen was completed for CAND-018, CAND-019, and CAND-020. The original CAND-018 result was INVALIDATED due to future-data leakage in the trend filter. A fresh, corrected G1 was executed for CAND-018.
- CAND-018 (Final Adjudication): RETURN TO G0 (Structurally negative expectancy due to left tail. Risk-controlled variant requires new G0 candidate).
- CAND-019: BLOCKED (Missing local data for Fixed Income benchmark).
- CAND-020: INSUFFICIENT (Killed).

**Outcome:** Recorded as a research-screening milestone. Do NOT call any candidate scientifically supported. Do NOT call any candidate economically viable.

## DISC-031 — Research Factory V2 G0 Cycle (V8)

**Relationship:** Tradeable Edge Discovery Screening.

**Status:** The V8 G0 candidate generation cycle was completed (post-CAND-018 lesson), explicitly incorporating pre-entry state conditioning. Promoted candidates: CAND-G0-021, CAND-G0-022, CAND-G0-023, CAND-G0-024.

**Outcome:** Recorded as a research-screening milestone. Do NOT create a scientific finding from G0 alone. Do NOT claim economic support. Do NOT claim strategy viability.

## DISC-032 — Research Factory V2 G1 Cycle (V8)

**Relationship:** Tradeable Edge Discovery Screening.

**Status:** The V8 G1 Economic Plausibility Screen was completed for candidates CAND-021, CAND-022, CAND-023, and CAND-024.
- CAND-021 (Final Adjudication): G2 READY.
- CAND-022: BLOCKED (Missing GBPUSD M1 data).
- CAND-023: INSUFFICIENT (Killed).
- CAND-024: INSUFFICIENT (Killed).

**Outcome:** Recorded as a research-screening milestone. Do NOT call any candidate scientifically supported. Do NOT call any candidate economically viable.

## DISC-033 — Research Factory V2 G2 Cycle (CAND-021)

**Relationship:** Tradeable Edge Discovery Screening.

**Status:** The G2 Cheap Empirical Pilot was completed for CAND-021. The chronological holdout reproduced the positive expected value and the effect survived 4.0-point friction stress. Final Adjudication: G3 READY (Scientific effect empirically validated, descriptive reproduction successful).

**Outcome:** The core phenomenon is empirically validated out-of-sample. Recorded as a milestone. Do NOT claim the overall strategy is viable without formal risk controls.

## DISC-034 — Research Factory V2 G3 Cycle (CAND-021)

**Relationship:** Tradeable Edge Discovery Screening.

**Status:** The G3 Scientific Validation was completed for CAND-021. The formal permutation test on the primary endpoint (Difference in mean net returns between FAVORABLE and ADVERSE states) yielded a negative difference (-2.09) with a p-value of 0.90. Scientific Classification: CONTRADICTED.

**Outcome:** The hypothesis that the pre-entry D1 volatility state isolates a more profitable regime is completely contradicted by statistical evidence. The descriptive reproduction in G2 was statistically identical to chance. The object is rejected and returned to G0.
G1/G2 showed positive descriptive economics in the registered FAVORABLE subset, but G3 demonstrated that the pre-entry D1 volatility-state label did not produce a statistically distinguishable conditional return difference. The apparent economic separation was not supported as a genuine conditional scientific effect.

## DISC-035 — Research Factory V2 G0 Cycle V9

**Relationship:** Tradeable Edge Discovery Screening.

**Status:** V9 G0 candidate generation completed. Designed to find independent mechanistic edges instead of adding arbitrary filters. Promoted Candidates:
- CAND-G0-025 (Macro Shock Liquidity Void Reversal - Family A)
- CAND-G0-026 (US Open Initial Balance Trap - Family C)
- CAND-G0-027 (Intraday Trend Inventory Unwind - Family D)

**Outcome:** Candidates promoted to G1 for Economic Plausibility Screening.

## DISC-036 — Research Factory V2 G1 Screen V9

**Relationship:** Tradeable Edge Discovery Screening.

**Status:** V9 G1 Economic Plausibility Screen completed.
- CAND-G0-025: PASS — MARGINAL.
- CAND-G0-026: INSUFFICIENT.
- CAND-G0-027: INSUFFICIENT.

**Outcome:** CAND-G0-025 was independently adjudicated. The underlying mechanism is observable without look-ahead, but the massive ~50-point standard deviation renders the +1.25 mean net too fragile for unhedged empirical piloting. Final Decision: HOLD. Line closed; returned to G0.

## DISC-037 — Research Factory V2 Governance Amendment (Artifact vs System)

**Relationship:** Tradeable Edge Discovery Screening.

**Status:** Formal distinction created between 'Research Artifacts' (individual scientific edge components) and 'Strategy Systems' (deployable trading architectures). 

**Outcome:** Candidates with strong per-event economics but low standalone frequency (such as CAND-024 and CAND-025) are no longer automatically killed. They are classified as COMPONENT-CANDIDATES and retained for future SYSTEM ASSEMBLY, where the union of multiple artifacts produces sufficient system-level frequency.

## DISC-038 — Historical Artifact Reintroduction Audit V1

**Relationship:** Tradeable Edge Discovery Screening.

**Status:** Retrospective audit of historical lines (DISC-021-026, CAND-018-027) completed under the Artifact vs System Governance V1.

**Outcome:** 
- CAND-024 is designated COMPONENT-ELIGIBLE / RETAINED FOR SYSTEM ASSEMBLY REVIEW (A).
- CAND-025 is designated COMPONENT-CANDIDATE (CONDITIONAL) / RETAINED FOR SYSTEM ASSEMBLY REVIEW (B).
- No failed artifacts were rescued. All contradicted or economically non-viable strategies (DISC-021, DISC-022, DISC-023, DISC-024, DISC-025, DISC-026, CAND-018, CAND-020, CAND-021, CAND-023, CAND-026, CAND-027) remain permanently closed (C/D/E).

## DISC-039 — System Assembly Candidate Register

**Relationship:** Tradeable Edge Discovery Screening.

**Status:** SYSTEM ASSEMBLY CANDIDATE REGISTER ESTABLISHED.

**Outcome:** 
- CAND-024 retained as a COMPONENT-CANDIDATE / EVENT OPPORTUNIST. Its standalone status remains CLOSED.
- CAND-025 retained but UNQUALIFIED. Its standalone status remains CLOSED.

## DISC-040 — Research Factory V2 G0 Cycle V10

**Relationship:** Tradeable Edge Discovery Screening.

**Status:** V10 G0 candidate generation cycle completed. Focused on component-oriented discovery (Event Opportunist, Session Component, Cross-Market, Diversifier).

**Outcome:** Promoted to G1: CAND-G0-028, CAND-G0-029, CAND-G0-030, CAND-G0-031.

## DISC-041 — Research Factory V2 G1 Screen V10

**Relationship:** Tradeable Edge Discovery Screening.

**Status:** V10 G1 Economic Plausibility Screen completed.

**Outcome:** All V10 candidates killed/blocked. 
- CAND-028: BLOCKED (Data Quality - True volume unavailable)
- CAND-029: BLOCKED (Data Availability - Missing USDJPY/TLT)
- CAND-030: INSUFFICIENT (Killed) - Evaluated EURUSD Asian Value Area Rejection. 374 events, +7.18 pip median gross, but severe left tail resulted in -1.25 pip negative mean expectancy.
- CAND-031: BLOCKED (Data Availability - Missing VIX)
- G2 NOT EXECUTED.

## DISC-042 — Research Factory V2 G1 Closure V10

**Relationship:** Tradeable Edge Discovery Screening.

**Status:** V10 G1 cycle formally closed.

**Outcome:** 
- No G2 candidates.
- CAND-030 permanently CLOSED due to negative expectancy (left tail) despite high win rate.
- CAND-028, CAND-029, CAND-031 permanently CLOSED due to data availability/quality blockers.
- Next G0 cycle must prioritize mechanisms with naturally asymmetric positive payoffs and positive expectancy, diversifying away from "high hit rate but negative expectancy" patterns.

## DISC-043 — Research Factory V2 G0 Cycle V11

**Relationship:** Tradeable Edge Discovery Screening.

**Status:** V11 G0 candidate generation cycle completed. Focused on positive-expectancy mechanism discovery (Breakout Continuation, Forced Flow, Cross-Market Repricing).

**Outcome:** Promoted to G1: CAND-G0-032 (Session Component), CAND-G0-033 (Session/Event Opportunist), CAND-G0-034 (Cross-Market/Event Opportunist).

## DISC-044 — Research Factory V2 G1 Screen V11

**Relationship:** Tradeable Edge Discovery Screening.

**Status:** V11 G1 Economic Plausibility Screen completed.

**Outcome:** 
- CAND-032: PASS — CLEAR. NY Open Structural Momentum Ignition (USATECHIDXUSD) demonstrated broad-based positive expectancy (+12.02 points mean net, N=257). Promoted to G2.
- CAND-033: INSUFFICIENT. WMR Pre-Fixing Flow Acceleration (EURUSD) captured the observable momentum but was mathematically insufficient to overcome friction.
- CAND-034: INSUFFICIENT. Metals Macro Confirmation Ignition (XAUUSD/XAGUSD) failed due to a severe unhedged left tail (positive median but negative mean).
- G2 NOT EXECUTED.

## DISC-045 — CAND-032 Final G1 Adjudication

**Relationship:** Tradeable Edge Discovery Screening.

**Status:** Final independent adjudication of CAND-032 G1 results completed.

**Outcome:** 
- G1 Verdict confirmed: G2 READY.
- The NY Open Structural Momentum mechanism (USATECHIDXUSD) was verified free of look-ahead bias with rigorous event integrity.
- Expected value (+12.02 points net) was determined to be broad-based, not reliant on a handful of extraordinary outliers, thus fulfilling the positive-expectancy mandate.

## DISC-046 — CAND-032 G2 Cheap Empirical Pilot

**Relationship:** Tradeable Edge Discovery Screening.

**Status:** G2 completed for CAND-G0-032 (NY Open Structural Momentum).

**Outcome:** 
- G2 Verdict: PROMOTE TO G3.
- The mechanism reproduced robustly outside the aggregate sample. The chronological holdout maintained strong positive expectancy (+10.61 points mean net, median +42.60) despite absorbing the worst outlier of the entire dataset (-1134 points).
- The mechanism proved highly resistant to friction stress (surviving 2x / 4.0 point round-trip assumptions) and maintained broad-based structural stability without reliance on tail winners.

## DISC-047 — CAND-032 G3 Scientific Validation

**Relationship:** Tradeable Edge Discovery Screening.

**Status:** G3 completed for CAND-G0-032 (NY Open Structural Momentum).

**Outcome:** 
- G3 Verdict: INCONCLUSIVE.
- Despite strong G1/G2 economics (+12.02 points mean net), the unhedged left-tail variance (worst trade -1134 points) paralyzed scientific inference.
- A direction-sign permutation placebo test yielded a null 95% CI of [-24.79, +20.94]. The observed +12.02 effect falls entirely within this noise band (p=0.1133), meaning the mechanism cannot be mathematically distinguished from a random coin flip on highly volatile days.
- G4 NOT EXECUTED. Pipeline blocked by scientific insufficiency.

## DISC-048 — CAND-032 G3 Closure

**Relationship:** Tradeable Edge Discovery Screening.

**Status:** Formal closure of the CAND-032 research line.

**Outcome:** 
- CAND-032 line is CLOSED (G3 INCONCLUSIVE).
- No G4 executed. No rescue authorized.
- Lesson recorded: A strong out-of-sample economic result (G2) can remain scientifically non-adjudicable (G3) if the registered mechanism cannot be distinguished from a suitable null due to severe unhedged variance.
- Next action: Return to G0 Candidate Generation.

## DISC-049 — V12 G0 Candidate Generation

**Relationship:** Tradeable Edge Discovery Screening.

**Status:** V12 G0 candidate generation completed.

**Outcome:** 
- Promoted CAND-G0-035 (Month-End Imbalance Acceleration).
- Promoted CAND-G0-036 (Structural PDH Pre-Market Acceptance).
- Promoted CAND-G0-037 (Cross-Index Tech Leadership Divergence).
- V12 strictly prioritizes mechanisms with pre-declared, falsifiable counterfactuals to ensure scientific adjudicability (solving the CAND-032 variance trap). G1 pending.

## DISC-050 — V12 G1 Economic Plausibility Screen

**Relationship:** Tradeable Edge Discovery Screening.

**Status:** V12 G1 screening completed.

**Outcome:** 
- CAND-035 (Month-End Imbalance): COMPONENT-CANDIDATE (Retain). Massive per-event economics (+62.36 mean net) and a flawless counterfactual validation, but low opportunity frequency (4 events/year).
- CAND-036 (Structural PDH Acceptance): INSUFFICIENT. The strictly verified acceptance produced negative expectancy (-16.15), fundamentally contradicted by the unverified gap-up counterfactual (+13.95).
- CAND-037 (Cross-Index Divergence): BLOCKED. Required missing USA500IDXUSD_M1.csv data.
- Zero standalone G2 promotions.

## DISC-051 — V13 G0 Candidate Generation

**Relationship:** Tradeable Edge Discovery Screening.

**Status:** V13 G0 candidate generation completed.

**Outcome:** 
- Promoted CAND-G0-038 (Mid-Day Counter-Trend Reload).
- Promoted CAND-G0-039 (Structural Gap-Fill Rejection).
- Promoted CAND-G0-040 (Volatility Compression Expansion).
- V13 prioritized finding specialized, low-frequency component artifacts with strong structural positive-expectancy hypotheses and strict falsifiable counterfactuals. G1 pending.

## DISC-052 — V13 G1 Economic Plausibility Screen

**Relationship:** Tradeable Edge Discovery Screening.

**Status:** V13 G1 screening completed.

**Outcome:** 
- CAND-038 (Mid-Day Reload): INSUFFICIENT. Validated counterfactual outperformance but the absolute net economics relied entirely on a single positive outlier, with a structurally negative median (-18.88).
- CAND-039 (Gap-Fill Rejection): INSUFFICIENT. The strictly bounded confirmation criteria (testing the YC precisely without exceeding it) yielded 0 historical events.
- CAND-040 (Volatility Expansion): INSUFFICIENT. The expansion from compression yielded negative expectancy (-18.99), completely contradicted by its counterfactual (which yielded +92.21).
- Zero standalone G2 promotions. Zero new Component-Candidates retained.

## DISC-053 — V13 G1 Closure

**Relationship:** Tradeable Edge Discovery Screening.

**Status:** Formal closure of the V13 G1 cycle.

**Outcome:** 
- V13 cycle CLOSED. No candidates produced a sustainable positive-expectancy profile.
- Lesson recorded: A positive mean created by a single extreme observation (CAND-038) does not establish an economically healthy artifact.
- Lesson recorded: Zero event frequency (CAND-039) is evidence of insufficient empirical opportunity, not necessarily evidence that the underlying mechanism is false.
- Lesson recorded: A proposed causal explanation (CAND-040 dealer gamma) cannot be claimed when required observational data is unavailable.
- Next action: Return to G0 Candidate Generation (V14).

## DISC-054 — V14 G0 Candidate Generation

**Relationship:** Tradeable Edge Discovery Screening.

**Status:** V14 G0 candidate generation completed.

**Outcome:** 
- Promoted CAND-G0-041 (Post-OPEX Unpinning Drift).
- Promoted CAND-G0-042 (Correlated Liquidity-Shock Reversion).
- Promoted CAND-G0-043 (European-Close Liquidity Vacuum).
- V14 shifted focus to Objective Economic Constraints, generating hypotheses derived from calendar mechanics (options expiration), structural parity breaks (margin/liquidity shocks), and institutional market structure (European session handoff). G1 pending.

## DISC-055 — V14 G1 Economic Plausibility Screen

**Relationship:** Tradeable Edge Discovery Screening.

**Status:** V14 G1 screening completed.

**Outcome:** 
- CAND-041 (Post-OPEX Drift): INSUFFICIENT. Post-OPEX gaps resisted mean-reversion better than generic Mondays, but the absolute median was negative (-10.06), driven entirely by a single outlier.
- CAND-042 (Correlated Shock Reversion): COMPONENT-CANDIDATE (Event Opportunist). Produced massive +63 mean / +228 median points. N=5 is too small for chronological G2 holdout testing, but the strong per-event structural dislocation earns it a place on the Component Register.
- CAND-043 (Liquidity Vacuum): INSUFFICIENT. Continuation after a dominant morning trend yielded worse performance (-3.80) than the vacuum after a flat morning, explicitly contradicting the hypothesis.
- Causal mechanisms (gamma pinning, forced liquidations, order book depth) were isolated from observed price behavior due to missing proxy data. Zero standalone G2 promotions.

## DISC-056 — V14 G1 Closure & Component Governance Update

**Relationship:** Tradeable Edge Discovery Screening.

**Status:** Formal closure of the V14 G1 cycle and update of Component Register governance.

**Outcome:** 
- V14 cycle CLOSED. No candidates produced high-frequency, robust economics suitable for standalone G2 promotion.
- Component Governance Updated: Delineated `COMPONENT-CANDIDATE` (retained for interesting descriptive economics, not scientifically validated) from `QUALIFIED SYSTEM COMPONENT` (passed independent rigorous scientific gating).
- Retained CAND-042 as COMPONENT-CANDIDATE — EVENT OPPORTUNIST, but explicitly NOT scientifically qualified.
- Lesson recorded: Component retention may occur before mechanism validation, but System Assembly qualification requires stronger independent evidence.
- Lesson recorded: A highly profitable event is not sufficient evidence for a proposed causal mechanism when the registered counterfactual is also highly profitable.
- Next action: Return to G0 Candidate Generation (V15) focusing on mechanisms with economically constrained counterfactuals.

## DISC-057 — V15 G0 Candidate Generation

**Relationship:** Tradeable Edge Discovery Screening.

**Status:** V15 G0 candidate generation completed.

**Outcome:** 
- Promoted CAND-G0-044 (Initial Balance Trap Liquidation).
- Promoted CAND-G0-045 (Safe-Haven Confirmed Risk-Off).
- Promoted CAND-G0-046 (Opening Print Capitulation Pivot).
- V15 shifted focus to counterfactual-discriminating mechanisms, generating hypotheses based on trapped institutional flow, cross-market structural confirmation, and cost-basis capitulation. G1 pending.

## DISC-058 — V15 G1 Economic Plausibility Screen

**Relationship:** Tradeable Edge Discovery Screening.

**Status:** V15 G1 screening completed.

**Outcome:** 
- CAND-044 (Initial Balance Trap Liquidation): INSUFFICIENT. Negative expectancy. Breaking a massive morning trend yielded worse results (-40.20 mean) than breaking a tight chop range (-7.68 mean), explicitly contradicting the forced liquidation hypothesis.
- CAND-045 (Safe-Haven Confirmed Risk-Off): INSUFFICIENT. High win rate but constrained upside. Crucially, the counterfactual (unconfirmed equity crashes) proved MORE profitable than the treatment (confirmed crashes), directly contradicting the thesis that safe-haven confirmation filters out mean-reversion.
- CAND-046 (Opening Print Capitulation Pivot): INSUFFICIENT. Negative expectancy. Crossing the Open after a massive excursion yielded negative returns, while the counterfactual chop crosses yielded positive returns.
- Lesson recorded: Hypotheses that sound mechanistically perfect often fail completely when confronted with empirical price action and explicit counterfactuals. Zero standalone G2 promotions.

## DISC-059 — V15 G1 Closure & Counterfactual Superiority Doctrine

**Relationship:** Tradeable Edge Discovery Screening.

**Status:** Formal closure of the V15 G1 cycle and update of G1 doctrine.

**Outcome:** 
- V15 cycle CLOSED. No candidates produced valid, counterfactual-discriminating economics.
- Doctrine Updated: Added the "Counterfactual Superiority Rule" to G1. A treatment that is profitable in absolute terms does NOT qualify as a mechanism artifact if its pre-registered counterfactual is materially more profitable.
- Lesson recorded: Event economics must be strictly separated from mechanism value. A condition must explicitly add information relative to its counterfactual; simply producing profitable events is insufficient if the base event without the condition is superior.
- Next action: Return to G0 Candidate Generation (V16) focusing on mechanisms where the condition is expected to actively add value relative to a very close counterfactual.

## DISC-060 — V16 G0 Candidate Generation

**Relationship:** Tradeable Edge Discovery Screening.

**Status:** V16 G0 candidate generation completed.

**Outcome:** 
- Promoted CAND-G0-047 (Fixing-Window Liquidity Transfer).
- Promoted CAND-G0-048 (Sequential Macro-Release Dislocation).
- Promoted CAND-G0-049 (Cross-Market Lead-Lag Asymmetry).
- V16 shifted focus to objective economic constraints where the condition explicitly adds value relative to a very close counterfactual. Mechanisms span Settlement/Reference Price Constraints (A), Information Arrival/Sequential Repricing (G), and Cross-Market Constraints (D). G1 NOT EXECUTED.

## DISC-061 — V16 G1 Economic Plausibility Screen

**Relationship:** Tradeable Edge Discovery Screening.

**Status:** V16 G1 screening completed.

**Outcome:** 
- CAND-047 (Fixing-Window Liquidity Transfer): INSUFFICIENT. The treatment produced negative expectancy (-43.62 bps mean net, 0% win rate) and was materially outperformed by the counterfactual (-7.04 bps mean net, 57% win rate), directly contradicting the value of the constraint.
- CAND-048 (Sequential Macro-Release Dislocation): INSUFFICIENT. The exact registered condition (a 1% move between 08:30 and 09:30, followed by an exact touch of the 08:30 level) yielded zero historical events.
- CAND-049 (Cross-Market Lead-Lag Asymmetry): INSUFFICIENT. The exact registered condition (a 1% Gold shock between 09:30 and 10:30 while Silver remained <0.2% flat) yielded zero historical events.
- Zero standalone G2 promotions.

## DISC-062 — V16 G1 Closure

**Relationship:** Tradeable Edge Discovery Screening.

**Status:** Formal closure of the V16 G1 cycle.

**Outcome:** 
- V16 cycle CLOSED. No candidates produced valid economics.
- Lesson recorded: Overly strict definitions designed to ensure structural purity (CAND-048, CAND-049) can completely extinguish opportunity frequency, rendering the artifact untestable.
- Lesson recorded: Price behaviors attributed to "institutional necessity" (CAND-047) are just as susceptible to negative expectancy as generic technical patterns when subjected to strict friction and counterfactual comparison.
- Next action: Return to G0 Candidate Generation (V17).

## DISC-083 — V23 G1 Economic Plausibility Screen

**Relationship:** Tradeable Edge Discovery Screening.

**Status:** V23 G1 screening completed.

**Outcome:** 
- CAND-068 (Post-Shock Absorption Reversal) [ALPHA]: INSUFFICIENT. Failed due to extreme evidence limitation (N=7). Fading the 7 recorded shock-absorption patterns performed worse than fading the shock immediately.
- CAND-069 (NY Mid-Session Reversal Anchor) [ALPHA]: INSUFFICIENT. Generated a virtually flat net expectancy (+0.75 bps), failing to clear the >5 bps friction hurdle, despite slightly outperforming morning anchors.
- CAND-070 (Sustained Momentum Micro-Structure Failure) [ALPHA]: INSUFFICIENT. Failed absolute expectancy and falsified its hypothesis: fading the first structure break in an overheated trend performs significantly worse than fading identical structure breaks in chop. The trend overwhelmingly resumes and stops out the mean-reversion trade.
- All candidates failed G1. Zero standalone G2 promotions. Zero components added. Next action: Return to G0 Candidate Generation.

## DISC-084 — V23 Closure & Component/State Qualification Readiness Review

**Relationship:** Governance Architecture.

**Status:** V23 formally closed. Repository review completed.

**Outcome:** 
- V23 closed.
- Conducted a repository-wide evidence audit to determine if QuantForge should return to G0 or begin formally qualifying existing components.
- Determined that CAND-024 and CAND-035 possess massive historical expectancy and have passed scientific counterfactual validation, failing G2 promotion exclusively on calendar frequency. 
- Defined the "Rare-Event Validation Doctrine" (event-counts vs calendar duration). 
- Decided to suspend G0 and G1 to pursue RARE-EVENT COMPONENT QUALIFICATION for CAND-024 and CAND-035.
- System Assembly (S0) remains NOT YET EXECUTABLE.

## DISC-085 — Rare-Event Component Forward Qualification Protocol

**Relationship:** Governance Architecture & Forward Validation.

**Status:** Protocol defined and authorized.

**Outcome:** 
- Formalized the event-count-based forward qualification protocol for CAND-024 (Friday De-Risking) and CAND-035 (Month-End Imbalance).
- Reconstructed their exact frozen historical identities to prevent semantic drift during forward observation.
- Established a minimum threshold of 3 independent forward events and a target of 5 forward events. 
- Defined strict paper execution metrics, identity matching rules, and failure conditions. 
- Verified that CAND-042, CAND-059, and System Assembly remain expressly excluded from this track. 
- Authorized the explicit launch of the qualification track, pending the provisioning of dedicated forward-runner infrastructure.

## DISC-086 — Rare-Event Forward Infrastructure Provisioning

**Relationship:** Governance Architecture & Forward Validation.

**Status:** Infrastructure Ready — Observation Not Launched.

**Outcome:** 
- Provisioned the dedicated, isolated forward-observation infrastructure for CAND-024 and CAND-035. 
- Enforced frozen contracts via deterministic hashing to prevent semantic drift. 
- Implemented strict event/outcome ledgers, a paper execution firewall, exponential backoff reconnect logic, and timezone-aware session mechanics. 
- Verified infrastructure readiness via pytest and a synthetic smoke test. 
- Observation launch is formally authorized but pending broker feed configuration.

## DISC-087 — Rare-Event Forward Qualification Launched

**Relationship:** Governance Architecture & Forward Validation.

**Status:** FORWARD OBSERVATION ACTIVE (CAND-024 / CAND-035).

**Outcome:** 
- Launched the background daemon tracking the event-count based forward qualification for CAND-024 and CAND-035.
- Event tracking is operating strictly under frozen contracts (no SMC POI filters, no trend filters).
- Confirmed strict paper-only execution wall with no live execution methods available.
- Track will remain active until minimum 3 (target 5) qualifying events are recorded per component, or the 18-month safety boundary is hit.

## DISC-088 — Rare-Event Forward Launch Integrity Audit

**Relationship:** Governance Architecture & Forward Validation.

**Status:** OPERATIONAL BUT NOT TRUE FORWARD VALIDATION (BLOCKED).

**Outcome:** 
- Audited the running forward qualification daemon for CAND-024 and CAND-035. 
- Confirmed rigorous isolation of the paper execution layer. 
- Discovered the runner is actively fed by a deterministic synthetic market price generator (`time.sleep(1)` loop with canned quotes) rather than a live broker feed adapter.
- Observation clock cannot officially start until a live market-data adapter replaces the placeholder synthetic feed.

## DISC-089 — Rare-Event Market Feed Remediation

**Relationship:** Governance Architecture & Forward Validation.

**Status:** REAL MARKET FEED NOT VERIFIED — QUALIFICATION BLOCKED.

**Outcome:** 
- Refactored the rare-event runner to consume a clean `MarketDataFeed` interface.
- Implemented a read-only MT5 adapter (`mt5_market_feed.py`).
- Enforced explicit `--mode forward` and blocked synthetic data from triggering forward mode.
- Tests verify strict isolation of `PaperExecutionFirewall` and proper handling of `DATA_STALE` states to avoid fabricating `NO_EVENT` records.
- The MT5 verification smoke test was executed but live ticks were unavailable for USATECHIDXUSD in the terminal.
- Observation is fully provisioned but awaits a live MT5 terminal environment to verify real market conditions.

## DISC-090 — Rare-Event MT5 Read-Only Market Data Environment Diagnostic

**Relationship:** Governance Architecture & Forward Validation.

**Status:** REAL MARKET FEED NOT VERIFIED — QUALIFICATION BLOCKED.

**Outcome:** 
- Diagnosed the root cause of the missing `USATECHIDXUSD` feed data. 
- Verified that MT5 and Python IPC are functioning correctly. 
- Confirmed the local MT5 terminal is connected to an Exness trial server that does not provide `USATECHIDXUSD`. 
- Discovered alias instruments (e.g., `USTECm`), but correctly prevented unauthorized symbol mapping to preserve frozen contract definitions.
- Established that the environment requires explicit architectural authorization to implement a symbol alias map or provision the correct broker environment before qualification can proceed.

## DISC-091 — Frozen Instrument Identity / MT5 Symbol Mapping Audit

**Relationship:** Governance Architecture & Forward Validation.

**Status:** MAPPING NOT SAFE — QUALIFICATION BLOCKED.

**Outcome:** 
- Conducted an evidence-based audit of candidate mapping aliases (`USTECm`, `USTEC_x100m`) for the missing `USATECHIDXUSD` symbol. 
- Determined that while price translation is deterministic, the exact Friday closing behavior and Month-End 16:00 ET closing imbalance mechanics of Exness CFDs cannot be guaranteed to perfectly match the frozen research dataset without historical verification. 
- Concluded that the integrity of CAND-024 and CAND-035 events prevents substitution. 
- The runner must be provisioned with an MT5 environment that natively offers the `USATECHIDXUSD` market object to maintain scientific continuity.

## DISC-092 — Explicit Frozen-Instrument Normalization Review

**Relationship:** Governance Architecture & Forward Validation.

**Status:** APPROVED WITH NORMALIZATION — READY FOR LAUNCH.

**Outcome:** 
- Conducted a formal governance review to re-evaluate the previous mapping rejection for `USTECm`. 
- Confirmed through direct MT5 M1 bar extraction that Exness `USTECm` provides dense, continuous quoting at the critical event thresholds (Fridays through 15:45 ET and month-ends through 16:00 ET). 
- Established that all CAND-024 and CAND-035 event logic is structurally invariant under deterministic 1:1 price scaling. 
- Explicit USTECm environment mapping approved for future CAND-024/CAND-035 forward qualification (Mapping ID: `MAPPING:USATECHIDXUSD->EXNESS:USTECM:1.0`). 
- Historical candidate identities and contract hashes remain frozen; `USTECm` is declared strictly as an authorized execution environment representation.

## DISC-093 — Rare-Event Forward Qualification Post-Launch Integrity Check

**Relationship:** Governance Architecture & Forward Validation.

**Status:** PASS — PROTECTED FORWARD OBSERVATION.

**Outcome:** 
- Following the explicit launch of the rare-event forward runner, conducted a read-only post-launch audit to ensure compliance.
- Verified EXACTLY ONE qualification daemon running actively under the approved `--mode forward`.
- Confirmed correct telemetry persistence in heartbeats (preserving `logical_symbol`, `broker_symbol`, and `mapping_id` independently).
- Verified `cand_024_engine.py` and `cand_035_engine.py` frozen semantics remained strictly unaltered by the mapping integration.
- Confirmed feed failure states (e.g. data stale/indeterminate) correctly bypass logic rather than registering as `NO_EVENT`.
- Qualification clock established, candidate parameters isolated, and track formally transitioned into protected operational freeze pending target event count capture.

## DISC-094 — Unified Forward Supervisor Implementation

**Relationship:** Systems Architecture & Runtime Persistence.

**Status:** UNIFIED FORWARD SUPERVISOR ACTIVE.

**Outcome:** 
- Deprecated the ad-hoc runner script in favor of a full unified supervisor runtime (`scripts/forward/quantforge_forward_supervisor.py`).
- Established robust `msvcrt` OS-level singleton locking to prevent execution races.
- Created `status_quantforge_forward.bat`, `stop_quantforge_forward.bat`, and `run_quantforge_forward.bat` as operational interfaces.
- Implemented a registry pattern to isolate independent module ledgers, executing candidates in parallel over ONE shared MT5 market data connection.
- Preserved exact qualification clock start (`2026-08-27T09:44:58Z`) by migrating legacy logs to `runtime/forward/history/` and logging explicit transition timestamps.
- Set up Windows Scheduled Task bindings for persistence across IDE/shell terminations. CAND-015 remains PROTECTED and strictly external.

## DISC-095 — Canonical Contract Ratification and Qualification Resume

**Relationship:** Governance Architecture & Forward Validation.

**Status:** CANONICAL RARE-EVENT QUALIFICATION RESUMED — PROTECTED.

**Outcome:** 
- Discovered phantom hash problem: CAND-024 (`c49c5bb0`) and CAND-035 (`a7c2132d`) were not reproducible from any stored definition.
- Discovered mixed-field hash problem: repair attempt produced hashes (`5638ffc1`, `3715d51a`) that included historical evidence fields not in the contract hash input.
- Established canonical architecture: `FrozenStrategyContract` (executable semantics only, hash input) / `HistoricalEvidence` (research results, NOT in hash) / `EnvironmentMapping` (broker/runtime, NOT in hash).
- Canonical hashes: CAND-024 = `925495a8`, CAND-035 = `ddc5d0e9`.
- 78/78 contract tests pass (identity, mutation, evidence exclusion, environment exclusion, field completeness, serialization, engine consistency, negative tests, phantom separation, content verification).
- Engine consistency verified: both engines import and use canonical contracts.
- Supervisor contract firewall verified: top-down import chain, no reconstruction.
- Pre-ratification period classified as INTEGRITY GAP (2026-08-27T09:44:58Z → 2026-08-27T10:10:08Z).
- Zero qualifying events accepted during pre-ratification period.
- Valid canonical qualification resume: 2026-08-27T12:05:15Z.
- Original intended start preserved: 2026-08-27T09:44:58Z.
- Task Scheduler requires Administrator to install (bat script ready).
- Forward qualification now collecting valid evidence on canonical contracts.
- CAND-015 remains PROTECTED / EXTERNAL / UNTOUCHED.
- System Assembly remains NOT EXECUTED.

## DISC-096 — Forward Runtime Simplified to One Manual Unified Launcher

**Relationship:** Systems Architecture & Runtime Persistence.

**Status:** FORWARD RUNTIME SIMPLIFIED — ONE BAT, ONE SUPERVISOR, ONE MT5 FEED.

**Outcome:** 
- Simplified the forward-observation architecture to one manual BAT launcher, one supervisor, one MT5 read-only connection, and all currently authorized forward modules.
- CAND-015 integration assessed: CANNOT be safely integrated without semantic changes. Different contract architecture (dictionary-based identity, dual-market data, pandas/ATR engine). Decision: EXTERNAL / PROTECTED.
- BAT launcher modified for detached process launch via `start /b`. Returns control to operator immediately.
- Singleton lock prevents duplicate supervisors.
- Task Scheduler declared NOT REQUIRED. Manual BAT is canonical operator entry point.
- Status display updated with canonical hashes, mapping, and CAND-015 explanation.
- 49/49 forward runtime tests pass (contracts, engines, registry, paper execution, module processing, supervisor, ledgers, market data, status, shutdown, BAT files, canonical identity, CAND-015 external).
- CAND-024 + CAND-035 under unified supervisor. CAND-015 remains PROTECTED / EXTERNAL.
- Operator workflow: `run_quantforge_forward.bat` → `status_quantforge_forward.bat` → `stop_quantforge_forward.bat`.
- After PC restart: operator manually runs `run_quantforge_forward.bat`. No automatic startup required.
- Qualification timeline preserved: original `2026-08-27T09:44:58Z`, valid resume `2026-08-27T12:05:15Z`.

## DISC-097 — CAND-015 Adapter-Based Integration into Unified Runner

**Relationship:** Systems Architecture & Runtime Persistence.

**Status:** CAND-015 INTEGRATED VIA ADAPTER — ONE RUNNER, THREE INDEPENDENT OBSERVERS.

**Outcome:**
- CAND-015 successfully integrated into unified forward runner via adapter pattern.
- Adapter (`cand015_adapter.py`) translates shared MT5 feed into CAND-015's `process_tick()` interface.
- Key finding: CAND-015 engine only uses USATECHIDXUSD M1 data (BTCUSD buffered but unused in signal evaluation).
- Adapter fetches latest completed M1 bar from MT5, maps USTECm → USATECHIDXUSD, feeds to engine.
- Engine's internal logic preserved: pandas resampling, Wilder's ATR, M5/D1 calculations unchanged.
- Cold start: engine accumulates M1 bars over time; no signals until 30 days of M5 bars available for ATR.
- Module registry updated: `get_registry()` now accepts optional `market_data` parameter for CAND-015.
- Status display updated: shows CAND-015 adapter status when available.
- 52/52 forward runtime tests pass (including 3 new CAND-015 adapter tests).
- Architecture: ONE BAT → ONE RUNNER → ONE MT5 FEED → THREE INDEPENDENT OBSERVERS.
- No signal combination. No portfolio logic. No inter-module state.

## DISC-098 — Project Cleanup and Obsolete Infrastructure Pruning

**Relationship:** Repository Maintenance & Project Hygiene.

**Status:** CLEANUP COMPLETED — OBSOLETE INFRASTRUCTURE PRUNED.

**Outcome:**
- Comprehensive cleanup of QuantForge repository before V24 research cycle.
- Removed: root scratch .py (4 files), root .txt dumps (3 files), diagnostic scripts (2), stale logs (2), research/scratch/ (11 files), empty directories (4), __pycache__ (50 dirs, ~4 MB), .pytest_cache (2 dirs).
- Removed superseded infrastructure: run_cand015_forward.bat, install_quantforge_forward_task.bat, rare_event_runner.py, run_long_observation.py.
- Task Scheduler removal deferred (requires Administrator). Task is Ready but never ran. Supervisor is manually started.
- ALL authoritative research preserved (271+ entries in output/research_discovery/).
- ALL active forward runtime preserved (supervisor, engines, ledgers, status).
- ALL governance preserved (SESSION_HANDOFF, discovery database, timeline).
- Tests: 130/130 pass (52 forward + 78 contract).
- Supervisor RUNNING (PID 6924) throughout cleanup. No interruption.
- V24 readiness: READY.

## DISC-101 — Operator Workflow Correction — Stale Status / Process Authority

**Relationship:** Runtime Architecture Correction.

**Status:** CORRECTION COMPLETE — PROCESS AUTHORITY ESTABLISHED.

**Incident:** After PC reboot on 2026-08-29, `status_quantforge_forward.bat` reported RUNNING for dead PID 5080. `tasklist /FI "PID eq 5080"` returned no tasks. `wmic process` showed no supervisor process. The persisted `status.json` was stale and was incorrectly treated as authoritative runtime state.

**Root Cause:** Status script and launcher used file existence (status.json, supervisor.lock) as proof of process liveness. Neither verified the actual Windows process.

**Correction:**
- Created `scripts/forward/process_validation.py` — robust PID/process verification via `wmic` command-line scanning.
- Fixed `status.py` — verifies actual process before reporting RUNNING; shows STALE warning when status.json is stale.
- Fixed `run_quantforge_forward.bat` — scans for real supervisor process (not just lock file); cleans stale locks.
- Fixed `stop_quantforge_forward.bat` — verifies process exists before sending shutdown request.
- Fixed `quantforge_forward_supervisor.py` — stale lock detection/cleanup on startup; proper LIVE banner with actual PID.
- Fixed `module_registry.py` — event console deduplication via (event_id, event_state) pairs.
- Created `scripts/forward/tests/test_process_validation.py` — 63 regression tests.
- Created `output/research_discovery/QUANTFORGE_OPERATOR_RUNTIME_CORRECTION_V1.md` — comprehensive artifact.

**Test Results:**
- 63 new tests: ALL PASS
- 54 existing forward runtime tests: ALL PASS
- Combined: 117/117 PASS

**Hard Rule Established:** A persisted status file is NOT proof that the process is alive. The actual Windows process is authoritative for RUNNING/NOT RUNNING.

**Operator Workflow:**
1. `run_quantforge_forward.bat` — starts experiment (one visible CMD window)
2. `status_quantforge_forward.bat` — shows real process state
3. `stop_quantforge_forward.bat` — stops the actual process
4. After PC restart: manually run BAT again. No Task Scheduler. No auto-start.

**Preserved:**
- CAND-015: ACTIVE / PROTECTED (adapter-based, semantic unchanged)
- CAND-024: ACTIVE — 0/3/5 (canonical: 925495a8)
- CAND-035: ACTIVE — 0/3/5 (canonical: ddc5d0e9)
- MT5: Exness-MT5Trial15 / USTECm (read-only)
- No live/demo/real orders (paper-only)
- No signal combination across candidates
- No Task Scheduler required

**Artifact:** `output/research_discovery/QUANTFORGE_OPERATOR_RUNTIME_CORRECTION_V1.md`

## DISC-102 — G1 Economic Qualification Framework V3 Ratification

**Relationship:** Governance Framework Ratification.

**Status:** RATIFIED — EFFECTIVE FOR FUTURE RESEARCH CYCLES ONLY (V25+).

**Context:** The original G1 framework applied a single-gate design (Mean Net > 5 bps + Counterfactual Treatment Superior) uniformly to all artifact classes. The V19-V24 meta-review revealed that this design is inappropriate for State/Condition artifacts (which don't generate standalone trades), rare-event Alpha (which can't accumulate N in standard G2 holdouts), and regime specialists (which intentionally suppress activity outside their regime).

**Framework Change:**
- Two-layer architecture: 9 hard validity gates + holistic economic evidence adjudication
- Four artifact-specific classes: Standalone Alpha, Rare-Event Alpha, State/Condition, Regime/Specialist
- Five-level evidence classification replacing binary PASS/FAIL
- Economic metrics treated as evidence inputs, not hard thresholds
- 5 bps and 20 bps downgraded to reference points
- N=3 and N=10 downgraded to evidence-quality markers
- 2 bps State delta removed as universal rule
- Median is evidence, not a gate
- G1 decision based on total evidence profile, not numeric score

**Hard Validity Gates (9):** Deterministic definition, executable entry, no hindsight contamination, correct cost normalization, data integrity, legitimate counterfactual, causal claims limited to observables, no future-bar dependency, reproducibility.

**Adjudication Classes:**
1. Economically Negative
2. Informationally Interesting
3. Economically Promising
4. Qualification-Worthy
5. Rare-Event Qualification-Worthy

**G1 Decisions:** CONTINUE TO G2 / HOLD / RARE-EVENT FORWARD QUALIFICATION / STATE INTERACTION ELIGIBLE / REJECT

**Rescue Firewall:** V19-V24 remain closed. Framework applies prospectively only. No historical reclassification without explicit owner authorization.

**Artifacts:**
- `output/research_discovery/QUANTFORGE_G1_ECONOMIC_QUALIFICATION_CRITERIA_AUDIT_V1.md`
- `output/research_discovery/QUANTFORGE_G1_ECONOMIC_QUALIFICATION_FRAMEWORK_V3_PROPOSAL.md`
- `output/research_discovery/QUANTFORGE_G1_HARD_GATES_VS_EVIDENCE_ADJUDICATION_V1.md`
- `output/research_discovery/QUANTFORGE_G1_ECONOMIC_QUALIFICATION_FRAMEWORK_V3_RATIFICATION_V1.md`

---

## V25 G0 — Economic Displacement Candidate Generation (2026-08-29)

Generated 3 V25 G0 candidates focused on economic displacement mechanisms (not price patterns):

- **CAND-074** (London Gold Fix Benchmark Execution Pressure) — Settlement/Benchmark family. Enter XAUUSD at London AM Fix in direction of pre-fix move. Exit 30 min later.
- **CAND-075** (US Equity Closing Auction Concentrated Order Flow) — Settlement/Benchmark family. Enter USATECHIDXUSD at 3:59 PM ET in direction of late-session move. Exit at close.
- **CAND-076** (Gold Overnight Repricing -> Tech Opening Direction) — Cross-Market Transmission family (EXTENSION of CAND-071). Enter USATECHIDXUSD at 9:30 AM ET in direction of overnight Gold move. Exit at 10:00 AM ET.

**Status:** V25 G0 COMPLETE. 3 candidates generated.

---

## V25 G1 — Economic Plausibility Screen (2026-08-29)

All three V25 candidates evaluated under G1 V3 evidence-based adjudication framework:

- **CAND-074:** N=1285, Mean Net=-1.72 bps, Median Net=-2.32 bps, Counterfactual Superior. Fix window adds no directional value. **ECONOMICALLY NEGATIVE.**
- **CAND-075:** N=623, Mean Net=-2.15 bps, Median Net=-2.28 bps, Counterfactual Superior. Closing auction adds no directional value. **ECONOMICALLY NEGATIVE.**
- **CAND-076:** N=466, Mean Net=-2.14 bps, Median Net=-2.83 bps, Counterfactual Superior (+2.20 bps). Gold direction inversely related to Tech. **ECONOMICALLY NEGATIVE.**

All three candidates pass all 9 hard validity gates. Economic failure is not validity failure. No conditional information value observed — all counterfactuals are superior.

**Status:** V25 G1 COMPLETE. NO G2 PROMOTIONS.

---

## V25 Closure (2026-08-29)

V25 closed with no G2 candidate. Settlement/benchmark mechanism families (CAND-074, CAND-075) failed alongside cross-market transmission (CAND-076). The V19-V25 total is now 21 candidates, 0 G2 promotions.

**Status:** V25 CLOSED.

---

## V26 G0 — Dynamic State Transition Discovery (2026-08-29)

Generated 3 V26 G0 candidates focused on dynamic state transitions (not static conditions):

- **CAND-077** (Volatility Compression-to-Expansion Transition Event) — Volatility Development family. Trade breakout direction when ATR percentile transitions from compressed (<25th) to expanding (>50th). Counterfactual: same breakout in already-expanded state.
- **CAND-078** (Trend Exhaustion Transition -> Mean-Reversion Event) — Trend Exhaustion family. Fade trend direction when 8+ consecutive same-direction closes are followed by a reversal bar. Counterfactual: same counter-trend signal after only 2-4 consecutive closes.
- **CAND-079** (Cross-Market Gold Volatility Regime Transition -> Tech Direction) — Cross-Market State Transition family. Trade Tech direction when Gold ATR percentile transitions rapidly from compressed to expanded. Counterfactual: same Tech window during already-expanded Gold volatility.

External custom-bot statistical findings used only as provisional research priors (not imported thresholds). First cycle to explicitly require state-transition mechanisms.

**Status:** V26 G0 COMPLETE. 3 candidates generated.

---

## V26 G1 — Economic Plausibility Screen (2026-08-30)

All three V26 candidates evaluated under G1 V3 evidence-based adjudication:

- **CAND-077:** N=2084, Net=-0.85 bps, CF delta=+1.67 bps TREATMENT SUPERIOR. **INFORMATIONALLY INTERESTING** — largest informational signal in Research Factory history. Compression-to-expansion transition adds real value but absolute economics remain negative.
- **CAND-078:** N=2946, Net=-2.21 bps, CF delta=-0.25 bps COUNTERFACTUAL SUPERIOR. **ECONOMICALLY NEGATIVE** — exhaustion transition adds no value.
- **CAND-079:** N=35920, Net=-1.79 bps, CF delta=+0.78 bps TREATMENT SUPERIOR. **INFORMATIONALLY INTERESTING** — Gold volatility transition adds weak value.

All three have negative absolute economics. Volume data unavailable (all zeros) for both instruments — noted as data limitation. Dynamic state-transition approach shows more promise than static conditions.

**Status:** V26 G1 COMPLETE. NO G2 PROMOTIONS.

---

## V26 Closure + Dynamic-State Knowledge (2026-08-30)

V26 formally closed. CAND-077 classified as STATE REVIEW ELIGIBLE — OWNER REVIEW REQUIRED (+1.67 bps conditional delta, largest in RF history). CAND-078 closed as ECONOMICALLY NEGATIVE. CAND-079 classified as STATE OBSERVATION (+0.78 bps delta, weak). Dynamic state-transition approach shows more conditional information than static conditions. CAND-077 requires owner review before any State interaction study.

**Status:** V26 CLOSED. STATE GOVERNANCE REVIEW REQUIRED.

---

## CAND-077 State Governance Review (2026-08-30)

Formal governance review of CAND-077 post-closure exploratory filter findings. Original CAND-077: N=2084, Net=-0.85 bps, CF delta=+1.67 bps (TREATMENT SUPERIOR), all 9 validity gates pass. Post-closure exploratory analysis found monotonic breakout-magnitude relationship: >15 bps breakout = 64.8% WR, +8.41 bps mean, +6.97 bps median, ~77/year.

**Decision:** STATE REVIEW ELIGIBLE preserved. Classification: supporting evidence for state review, NOT validated strategy. No numerical threshold ratified. The breakout-size observation strengthens the case for formal State hypothesis registration but does NOT validate any specific filter.

**State concept:** Expansion magnitude after compression contains incremental information about downstream outcome distribution.

**Future path:** Formal State hypothesis → qualified downstream Alpha required → interaction study → State qualification.

**V27 readiness:** READY. CAND-077 state review does not block V27 G0.

Artifact: `output/research_discovery/QUANTFORGE_CAND077_STATE_GOVERNANCE_REVIEW_V1.md`

**Status:** CAND-077 STATE GOVERNANCE REVIEW COMPLETE. STATE REVIEW ELIGIBLE PRESERVED. V27 G0 READY.

---

## V27 G0 Dynamic State Transition Discovery (2026-08-30)

Generated 3 V27 G0 candidates focused on genuinely distinct dynamic state transitions:

- **CAND-080** (Volatility Regime Quality Transition) — Smooth-to-choppy character change. Fade-the-trend entry after regime quality deterioration. Mechanism: Volatility Development — Regime Character Transition.
- **CAND-081** (Structural Level Failure Trap) — Breakout failure trapping participants. Counter-breakout fade after failed breakout. Mechanism: Post-Event State Transition — Failed Breakout Trap.
- **CAND-082** (Post-Expansion Retracement Quality State) — Retracement quality as State/Condition. Continuation entry after quality retracement. Mechanism: State Transition + Event Interaction — Volatility Development Quality.

All three are NEW (no overlap with V19-V26 or historical candidates). All three use USATECHIDXUSD M1 data. No volume required. CAND-077 remains STATE REVIEW ELIGIBLE — not reopened.

Artifact: `output/research_discovery/TRADEABLE_EDGE_DISCOVERY_SCREENING_V27.md`

**Status:** V27 G0 COMPLETE. 3 CANDIDATES GENERATED. G1 PENDING.

---

## V27 G1 Economic Plausibility Screen (2026-08-30)

All three V27 candidates evaluated under G1 V3 evidence-based adjudication:

- **CAND-080** (Vol Regime Quality Transition): N=3893, Net=-1.75 bps. Counterfactual FAILED (zero events for already-choppy condition). **INSUFFICIENT** — closed.
- **CAND-081** (Structural Level Failure Trap): N=3887, Net=-0.78 bps, CF delta=+1.23 bps TREATMENT SUPERIOR (second-strongest conditional delta in RF history). All 9 validity gates PASS. **INFORMATIONALLY INTERESTING** — STATE REVIEW ELIGIBLE.
- **CAND-082** (Post-Expansion Retracement Quality): N=97, Net=-0.33 bps, CF delta=+0.96 bps mean / -1.63 bps median (MIXED, outlier-dependent). State hypothesis contradicted (quality retracements worse than poor on median). **INFORMATIONALLY INTERESTING** — closed.

No G2 promotions. CAND-081 added to State Library as STATE REVIEW ELIGIBLE.

Artifact: `output/research_discovery/RESEARCH_FACTORY_V2_G1_SCREEN_20260830_V27.md`

**Status:** V27 G1 COMPLETE. NO G2 PROMOTIONS. CAND-081 STATE REVIEW ELIGIBLE.

---

## CAND-077 + CAND-081 State Governance Review (2026-08-30)

Formal State Governance Review of both State Review Eligible objects following V27 G1.

**CAND-077:** STATE REVIEW ELIGIBLE — PRESERVED. Volatility character transition is a genuine State concept. +1.67 bps conditional delta established. Post-closure filter observations remain EXPLORATORY EVIDENCE ONLY — no threshold ratified.

**CAND-081:** STATE REVIEW ELIGIBLE — PRESERVED. Structural level failure trap is a genuine State concept distinct from CAND-077. +1.23 bps conditional delta established. Absolute economics negative (-0.78 bps).

**Independence:** The two mechanisms are genuinely independent (different observables, different participant populations, different timeframes). They can coexist.

**V28 readiness:** READY.

Artifact: `output/research_discovery/QUANTFORGE_CAND077_CAND081_STATE_GOVERNANCE_REVIEW_V1.md`

**Status:** STATE GOVERNANCE REVIEW COMPLETE. V28 G0 READY.

---

## V28 G0 New Discovery (2026-08-30)

Generated 3 V28 G0 candidates spanning three distinct economic mechanism families:

- **CAND-083** (Cumulative Rejection Pressure Sweep) — Rejection cascade after multiple failed breakouts. Fade entry after breakout failure with 3+ prior rejections. Mechanism: Failed Information / Expectation Reset — Rejection Cascade.
- **CAND-084** (Intraday Range Compression → Expansion Asymmetry) — Range dynamics and trapped participants. Continuation entry after compression → expansion. Mechanism: Market Microstructure / Execution Condition — Range Dynamics.
- **CAND-085** (Approach Velocity → Breakout Continuation) — How price reaches a level determines post-breakout dynamics. Continuation entry after high-velocity approach breakout. Mechanism: Event Sequence / Path Dependence — Approach Dynamics.

All three are NEW (no overlap with V19-V27 or historical candidates). All three use USATECHIDXUSD M1 data. No volume required.

Artifact: `output/research_discovery/TRADEABLE_EDGE_DISCOVERY_SCREENING_V28.md`

**Status:** V28 G0 COMPLETE. 3 CANDIDATES GENERATED. G1 PENDING.

---

## V28 G1 Economic Plausibility Screen (2026-08-30)

All three V28 candidates evaluated under G1 V3:

- **CAND-083** (Cumulative Rejection Pressure): N=2318, Net=-2.33 bps, CF delta=+4.60 bps TREATMENT SUPERIOR (largest conditional delta in RF history). All 9 gates PASS. **INFORMATIONALLY INTERESTING** — STATE REVIEW ELIGIBLE.
- **CAND-084** (Range Compression -> Expansion): N=1910, Net=-1.42 bps, CF delta=+0.14 bps (negligible). Mechanism IDENTICAL to CAND-077. **INFORMATIONALLY INTERESTING** — EXTENSION / REDUNDANT.
- **CAND-085** (Approach Velocity): N=8201, Net=-2.13 bps, CF INVALID (zero low-velocity events). **INSUFFICIENT**.

No G2 promotions. CAND-083 added to State Library as STATE REVIEW ELIGIBLE. CAND-084 classified as extension of CAND-077.

Artifact: `output/research_discovery/RESEARCH_FACTORY_V2_G1_SCREEN_20260830_V28.md`

**Status:** V28 G1 COMPLETE. NO G2 PROMOTIONS. CAND-083 STATE REVIEW ELIGIBLE.

---

## DISC-035 — CAND-083 State Governance Review Complete (2026-08-30)

- **CAND-083** (Cumulative Rejection Pressure Sweep) — Formal governance review following V28 G1. Decision: STATE REVIEW ELIGIBLE — PRESERVED. Distinct State concept from CAND-077 and CAND-081. Mechanism: accumulated rejection pressure at structural level creates distinct market condition. G1 evidence: N=2318, Net=-2.33 bps, CF delta=+4.60 bps (TREATMENT SUPERIOR). All 9 gates PASS. Counterfactual valid (N=316). Independence audit: CAND-083 INDEPENDENT from CAND-077 (different observables) and INDEPENDENT but POTENTIALLY RELATED to CAND-081 (pre-failure vs post-failure). No numerical threshold ratified. Absolute economics negative — NOT standalone Alpha.

Artifact: `output/research_discovery/QUANTFORGE_CAND083_STATE_GOVERNANCE_REVIEW_V1.md`

**Status:** CAND-083 STATE GOVERNANCE REVIEW COMPLETE. STATE REVIEW ELIGIBLE PRESERVED. V29 G0 READY.

---

## DISC-036 — V29 G0 New Discovery Complete (2026-08-30)

- **CAND-086** (Information Absorption Failure Cascade): Repeated failed directional moves (>1.5× ATR that reverse >50% within 5 bars) create trapped-participant state. When count ≥3 in 20-bar lookback, next sustained directional move has larger continuation. Mechanism: Information Absorption / Failure family. Artifact class: Alpha/Event (provisional). Prior-art: NEW.
- **CAND-087** (Recovery Quality Differential): Post-disturbance recovery quality (>2× ATR move, recovery measured over 10 bars) reveals participant constraint. Weak recovery (<25% recovered) indicates trapped participants remain; strong recovery (>75%) indicates resolution. Mechanism: Recovery / Failure of Recovery family. Artifact class: Alpha/Event (provisional). Prior-art: NEW.
- **CAND-088** (Session Sequence Asymmetry): Opening directional bias (first 30 bars) followed by opposite-direction structural break (20-bar rolling high/low) traps opening-bias participants. Path-dependent mechanism. Mechanism: Path Dependence / Event Sequence family. Artifact class: Alpha/Event (provisional). Prior-art: NEW.

All three genuinely distinct from V19-V28 and from each other. CAND-077/CAND-081/CAND-083 preserved and untouched.

Artifact: `output/research_discovery/TRADEABLE_EDGE_DISCOVERY_SCREENING_V29.md`

**Status:** V29 G0 COMPLETE. 3 CANDIDATES GENERATED. G1 PENDING.

---

## DISC-037 — V29 G1 Economic Plausibility Screen Complete (2026-08-30)

- **CAND-086** (Information Absorption Failure Cascade): N=10198, Net=-2.06 bps, CF delta=+0.07 bps mean / -0.03 bps median (MIXED, negligible). ECONOMICALLY NEGATIVE — CLOSED. All 9 gates PASS. Conditional delta negligible.
- **CAND-087** (Recovery Quality Differential): N=9930, Net=-1.91 bps, CF delta=+0.23 bps mean / -0.03 bps median (MIXED, weak). INFORMATIONALLY INTERESTING — CLOSED. All 9 gates PASS. Too weak for State classification.
- **CAND-088** (Session Sequence Asymmetry): N=222, Net=-15.51 bps, CF delta=-19.59 bps (COUNTERFACTUAL SUPERIOR). ECONOMICALLY NEGATIVE — CLOSED. All 9 gates PASS. Hypothesis contradicted: aligned breaks outperform opposite breaks.

Notable: Aligned-direction structural breaks (CF) produce +4.07 bps net mean, 58.3% WR. Genuine positive finding not part of hypothesis.

No G2 promotions. No State Review Eligible. All three CLOSED.

Artifact: `output/research_discovery/RESEARCH_FACTORY_V2_G1_SCREEN_20260830_V29.md`

**Status:** V29 G1 COMPLETE. NO G2 PROMOTIONS. ALL CANDIDATES CLOSED. V30 G0 READY.

---

## DISC-038 — Relational Research Framework Governance Established (2026-08-30)

- Relational research governance framework established for QuantForge. Defines admission rules (STATE REVIEW ELIGIBLE, STATE OBSERVATION, STATE-ARTIFACT admissible; closed candidates NOT admissible as positive inputs; protected forward candidates permanently excluded), hypothesis schema, counterfactual framework, incremental information framework, multiple testing controls, discovery/confirmation separation, relational lifecycle, promotion rules, State relationship governance, unexpected observation governance (CAND-088 aligned-break classified as EXPLORATORY OBSERVATION requiring new G0), closed-line firewall, forward runtime firewall. Framework GOVERNED but not yet EXECUTING. V30 G0 is next milestone.

Artifact: `output/research_discovery/QUANTFORGE_RELATIONAL_RESEARCH_FRAMEWORK_GOVERNANCE_V1.md`

**Status:** RELATIONAL RESEARCH FRAMEWORK ESTABLISHED. V30 G0 READY.

---

## DISC-039 — Unified Research Knowledge Ledger V1 Established (2026-08-30)

- Comprehensive unified knowledge ledger covering V19-V29 constructed and reconciled. 33 candidates (CAND-056 through CAND-088) documented with full provenance. 6 behavioural knowledge records created. 7 State objects registered. 26 closed candidates preserved as negative knowledge. 4 exploratory observations documented. 3 untested relational hypothesis seeds recorded. Completeness audit passed: all candidates accounted for, all economic numbers sourced, no thresholds ratified, no closed candidates promoted, no relational experiments performed, no new Alphas created.

Artifact: `output/research_discovery/QUANTFORGE_UNIFIED_RESEARCH_KNOWLEDGE_LEDGER_V1.md`

**Status:** UNIFIED KNOWLEDGE LEDGER V1 RECONCILED. V30 G0 READY.

---

## DISC-040 — Unified Research History CSV Ledger V1 Established (2026-08-31)

- Machine-readable structured CSV ledger constructed covering the FULL QuantForge research history (Pre-Research Factory through V29). Reconstructed 73 candidates, 12 behavioural knowledge records, 21 structured evidence measurements, 7 State objects, 5 exploratory observations, 69 negative knowledge records, 10 conceptual relationships (ALL UNTESTED). Expanded scope from V19-V29 (covered by the Markdown ledger) to the complete available history. 8 reconciliation exceptions documented. Serves as durable structured research memory for future relational research and meta-analysis.

Artifacts:
- `research/knowledge/unified_ledger/` (7 CSV files + data dictionary + reconciliation exceptions)
- `output/research_discovery/QUANTFORGE_UNIFIED_RESEARCH_HISTORY_CSV_LEDGER_V1.md`

**Status:** UNIFIED RESEARCH HISTORY CSV LEDGER V1 ESTABLISHED. V30 G0 READY.