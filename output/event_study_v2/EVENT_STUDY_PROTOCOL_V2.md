# QuantForge — Canonical Mean-Reversion Event Study Protocol V2 (Pre-Registered)

**Status:** PRE-REGISTERED (defined before any outcome inspection)
**Date:** 2026-08-12
**Version:** V2.0.0
**Area:** `output/event_study_v2/` (research artifact; not production code)
**Relation to V1:** V2 is a controlled follow-up to Event Study V1 (`output/event_study_v1/`). V1 results are NOT erased or re-interpreted. V2 changes ONLY what is explicitly pre-registered below; everything else is carried over unchanged from V1.

## 1. Purpose

V1's single operationalization (rolling close-price z-score, Z=3.0, W=120, H=120) failed GATE 1: no OOS reversion, no stable threshold region, no cross-market portability.

V2 answers one narrow question:

> Is the V1 negative result specific to the V1 operationalization (rolling price z-score), or does the underlying behavioral hypothesis fail under a small, pre-registered set of scientifically justified alternative operationalizations?

V2 tests exactly three unresolved issues: (A) alternative normalization, (B) regime-resolved and walk-forward behavior, (C) persistence-conditioned outcomes. V2 does NOT change the research hypothesis: extreme short-term displacement → adverse/panic momentum → recoil → persistence → measurable outcome.

## 2. Governing rules (pre-registered)

1. **No outcome inspection before this protocol is frozen.**
2. **No look-ahead.** Detection inputs use data up to and including bar `t`'s close. Outcomes use bars `t+1…t+H` only. Regime measures use data up to `t` only.
3. **No selected-trade bias.** The event dataset contains the whole eligible population per the rules below.
4. **No threshold mining.** A single primary threshold per normalization is pre-registered; the sensitivity grid is TRAIN-only and exploratory; a matched-quantile check is exploratory. No value is selected by outcome.
5. **No post-hoc redefinition.** Any definition change requires a new protocol version.
6. **No tuning on VALIDATION or TEST.** VALIDATION evaluates the pre-registered definitions once (confirmatory). TEST is a single final hold-out pass (pre-authorized) interpreted ONLY as follow-up confirmation of effects that survived Holm correction on VALIDATION; otherwise TEST results are descriptive.
7. **No iteration.** One confirmatory pass. Further analysis requires a new protocol version.
8. **Negative results are valid.** "GATE 1 FAILED" is an acceptable conclusion.

## 3. Data

- Sources: `data/m1/{XAUUSD,EURUSD,BTCUSD,XAGUSD,USATECHIDXUSD}_M1.csv` (identical to V1).
- Format: `timestamp,open,high,low,close,volume`; M1 bars; naive MT5 server time; ordering only.
- Data-quality manifest recomputed (rows, ranges, duplicates, gaps, missing OHLCV, volume coverage) and SHA-256 fingerprints recorded.
- **Volume is unusable for 4 of 5 markets (100% zero rows, confirmed in V1); NO V2 methodology uses volume.**
- Usable period per market: bars with `W` warm-up and `H` forward bars within the partition.

## 4. Normalization study (Issue A)

Three pre-registered displacement normalizations, all computed at bar `t` from information up to and including `t`:

| ID | Name | Formula | Units | Warm-up |
|----|------|---------|-------|---------|
| N1 | Rolling price z-score (V1, unchanged) | `n1_t = (close_t − SMA_W(close)) / σ_W(close)` | standard deviations | W |
| N2 | ATR-relative displacement | `n2_t = (close_t − SMA_W(close)) / ATR_W` where `TR_t = max(high−low, |high−close_{t−1}|, |low−close_{t−1}|)`, `ATR_W = mean(TR over W)` | multiples of ATR | W |
| N3 | Return-based standardized displacement | `n3_t = (close_t/close_{t−W} − 1) / (σ_W(1-bar returns) · √W)` | standard deviations (t-statistic form) | W |

- `W = 120` (≈ 2 h on M1) for all three; `σ_W` = rolling std over the window with `min_periods=W` (same call as V1).
- N1 is carried over verbatim from V1 for direct comparison; N2 and N3 are the two pre-registered alternatives. Justification: ATR-normalization is the standard volatility-scaled displacement measure in market-microstructure work; the return-based form is the standard standardized-cumulative-return statistic. No other indicators are tested.
- **Primary threshold: ±3.0 for all three normalizations** (central value of the corpus-documented −2.8…−3.8 range; same justification as V1; for N2 the unit is "3×ATR displacement from the rolling mean", for N3 "3σ-equivalent 2-hour return").
- **Sensitivity grid (TRAIN-only, exploratory):** thresholds `±{2.5, 3.0, 3.5}` per normalization.
- **Matched-quantile comparability check (exploratory):** per market, TRAIN-based 0.5% and 99.5% quantiles of each normalization's distribution; VALIDATION events at those thresholds; reported as a count/mean comparison so the three normalizations are compared at equal rarity. Explicitly NOT used for selection.

## 5. Candidate event definition

- DOWN event at `t` iff `norm_t ≤ −3.0`; UP event at `t` iff `norm_t ≥ +3.0` (per normalization).
- Same-direction minimum separation `S = 240` bars (keep first qualifying bar; suppress subsequent same-direction bars until 240 bars elapsed) — identical to V1.
- Cross-direction overlap is allowed; its frequency is reported as a dependence caveat.
- Direction populations analyzed separately and pooled direction-adjusted. Direction is research metadata; no contract change.
- Hypothesized reversion signs are FIXED: DOWN displacement → positive direction-adjusted return; UP displacement → negative raw return (i.e., positive direction-adjusted). Signs are never flipped after results.

## 6. Outcome measures (identical to V1, pre-registered)

Primary horizon `H = 120` bars; outcomes use bars `t+1…t+H`.

For DOWN events:
- `event_return_H = close[t+H]/close[t] − 1`
- `adverse (MAE) = (close[t] − min(low[t+1..t+H]))/close[t]`
- `favorable (MFE) = (max(high[t+1..t+H]) − close[t])/close[t]`
- `recovery_ratio = favorable/(favorable+adverse)`
- `recovery_time` = first bar index `i∈[1..H]` with `close[t+i] > close[t]`; `H+1` if never
- `retention = mean(close[t+i] > close[t] for i ∈ 1..H)`

For UP events: mirror definitions. `direction_adjusted_return = +event_return` for DOWN, `−event_return` for UP. Positive direction-adjusted return = reversion in the hypothesized direction.

## 7. Persistence study (Issue C) — pre-registered criterion

- **Persistence PASS (P-pass):** `retention_60 ≥ 0.6`, i.e., price is above (below, for UP events) the event close for at least 60% of the first 60 bars (`PERSIST_H = 60`, `PERSIST_Q = 0.6`). Rationale: a neutral "majority-hold" criterion; NOT selected from outcomes.
- Persistence is a **pre-registered part of the event definition test**: P-pass vs P-fail subpopulations are compared for discrimination (mean direction-adjusted return), stability across periods and markets, and OOS behavior.
- Confirmatory test: P-pass vs P-fail difference of mean direction-adjusted return on VALIDATION, per normalization (pooled directions), permutation p-value.
- No persistence threshold is selected by outcome.

## 8. Regime analysis (Issue B)

Two deterministic, look-ahead-free regime dimensions:

1. **Volatility regime:** `vol_t` = rolling std of 1-bar returns over W ending at `t`. Tercile boundaries (33.3/66.7 percentiles) computed on TRAIN per market. Classes: LOW / MID / HIGH. Applied to VALIDATION and TEST.
2. **Chronological regime:** each market's full span split into three equal chronological thirds. Stability across calendar periods.

No regime classifier is designed to explain the V1 result; dimensions are minimal and reproducible.

## 9. Walk-forward analysis (Issue B)

Four chronological folds with growing training and fixed evaluation windows (per market, fractions of the full span):

| Fold | Training | Evaluation |
|------|----------|------------|
| A | [0, 0.40) | [0.40, 0.50) |
| B | [0, 0.50) | [0.50, 0.60) |
| C | [0, 0.60) | [0.60, 0.70) |
| D | [0, 0.70) | [0.70, 0.85) (= V1 VALIDATION window) |

- All rules are pre-registered; **no parameter is selected within a fold**, so the walk-forward is an evaluation of rule stability, not a selection mechanism.
- Per fold (normalization, direction, fold): event count, mean direction-adjusted return, bootstrap CI.
- Fold D doubles as the V1-VALIDATION comparison point.

## 10. Partitions (identical to V1)

- TRAIN = [start, 0.70), VALIDATION = [0.70, 0.85), TEST = [0.85, end), chronological per market.
- Events within `H` bars of a partition boundary are excluded from that partition's outcome statistics (retained in dataset, flagged).

## 11. Statistical method and multiple-comparison control

- Bootstrap 95% CIs: B=2000 resamples, seeded (`seed=20260813`).
- Effect tests use a two-sided **permutation p-value** (B=2000, seeded) of the difference of means (events vs equal-size direction-adjusted partition baseline; P-pass vs P-fail for the persistence test).
- **Confirmatory family (all on VALIDATION; 27 tests, pre-registered):**
  1. Pooled direction-adjusted effect vs baseline per normalization: N1, N2, N3 → 3
  2. Direction-resolved effect per normalization: 3 × 2 → 6
  3. Persistence (P-pass vs P-fail, pooled): 3
  4. Per-market pooled effect per normalization: 3 × 5 → 15
- **Multiplicity control: Holm correction** at family-wise α = 0.05 across all 27 tests. Rationale: the family is small and pre-defined; Holm controls FWER without an independence assumption and is more powerful than Bonferroni; under unknown positive dependence it is conservative, which is appropriate here. The method is chosen a priori for its properties, not for its result.
- TEST is interpreted only as follow-up confirmation of effects that survived Holm on VALIDATION; otherwise TEST is descriptive (avoids a second unconstrained multiplicity layer).

## 12. Dependence handling

- Same-direction separation `S=240 ≥ H=120` ⇒ **no overlapping same-direction outcome horizons**.
- Cross-direction overlap is permitted; its frequency per normalization is reported. Bootstrap/permutation resample at the event level; under cross-direction dependence the intervals may mildly understate uncertainty — recorded as a documented limitation (same as V1).
- Event counts and effective-sample caveats are reported per cell; small cells are flagged, never treated as validation.

## 13. Economic vs statistical significance

- Statistical significance alone is insufficient. Reported per effect: mean/median magnitude (in basis points over 2 h), CI, stability.
- Interpretive judgment (stated as interpretation, not a pre-registered gate): effects smaller than ≈ 5–10 bp over a 2-hour horizon are economically negligible relative to realistic transaction costs. The final report labels each surviving effect with this assessment.

## 14. Stopping rules

1. If **no** confirmatory test survives Holm correction at α=0.05 with a positive direction-adjusted sign and economically non-negligible magnitude → **GATE 1 FAILED**; V2 stops; no further iteration within V2.
2. If some effects survive Holm but lack direction consistency, walk-forward stability, or cross-market support → **GATE 1 PARTIALLY PASSED** at most; not promotable.
3. Any further analysis = new protocol version (V3), not an edit of V2.

## 15. Reproducibility

Recorded with outputs: protocol V2.0.0, seeds, all parameters above, dataset SHA-256 fingerprints, pandas/numpy versions, script identity, event-dataset row count and SHA-256, partition definitions, exact normalization formulas, bootstrap/permutation settings, Holm procedure.

## 16. Promotion gate

**GATE 1 PASSED** requires: directional consistency; OOS (VALIDATION, Holm-corrected) survival; walk-forward stability; cross-market stability **or** a clearly justified market-specific boundary; threshold/normalization stability; statistical significance after multiplicity control; practical economic significance; reproducibility. Anything less → GATE 1 PARTIALLY PASSED or GATE 1 FAILED. Even a GATE 1 PASSED result does NOT authorize implementation — a separate Scientific Specification Readiness Review is required first.

## 17. Output artifacts

`EVENT_STUDY_PROTOCOL_V2.md`, `run_event_study_v2.py`, `event_dataset_V2.csv`, `experiment_metadata_V2.json`, `data_manifest_V2.csv`, `results_confirmatory_V2.csv`, `results_normalization_V2.csv`, `results_crossmarket_V2.csv`, `results_walkforward_V2.csv`, `results_regime_V2.csv`, `results_persistence_V2.csv`, `results_threshold_V2.csv`, `SCIENTIFIC_REPORT_V2.md`. All under `output/event_study_v2/`. V1 artifacts are untouched.

---

*Pre-registered 2026-08-12 before any outcome analysis. No threshold, window, regime, or persistence definition in this document was chosen after inspecting outcomes.*
