# QuantForge — Canonical Mean-Reversion Event Study Protocol V3 (Pre-Registered)

**Status:** PRE-REGISTERED (defined before any confirmatory outcome inspection)
**Date:** 2026-08-12
**Version:** V3.0.0
**Area:** `output/event_study_v3/` (research artifact; not production code)
**Design posture:** adversarial confirmation / falsification of the V2 XAGUSD lead. The experiment is designed to FAIL the XAGUSD hypothesis if the evidence does not support it. No threshold search, no feature expansion, no optimization, no iteration.

## 1. Purpose and scope

V2 produced one coherent lead: **XAGUSD down-displacement reversion** (present under N1 and N2; TRAIN/VALIDATION/TEST sign-consistent; positive across walk-forward folds, chronological thirds, and volatility regimes; one Holm survivor in 27 tests; matched-quantile significant in both directions). V3 asks whether that lead survives:

1. dependence-aware (cluster/block) inference;
2. entry-at-confirmation persistence (leakage-free);
3. realistic transaction-cost assumptions;
4. chronological holdout confirmation (with the explicit caveat that no *fresh* holdout exists);
5. pre-registered robustness checks (threshold neighborhood, normalization, temporal stability, negative control).

**Scope restriction:** primary analysis is **XAGUSD only**. EURUSD is admitted as a single **pre-registered negative control** (the canonical null market in V1/V2) to validate the inference machinery. No other markets, indicators, features, or regime classifiers are added.

## 2. Governing rules

1. No confirmatory outcome inspection before this protocol is frozen.
2. No look-ahead. Detection inputs ≤ `t`. Confirmation inputs ≤ `t+K`. Outcome inputs start at `t+K`.
3. No threshold optimization: primary thresholds carried forward from V2 (±3.0 for N1/N2); a small pre-registered neighborhood {2.5, 3.0, 3.5} is evaluated **confirmatorily** (reported as a region vs spike), never selected by outcome.
4. No redefinition after outcomes; changes require a new protocol version.
5. No tuning on the holdout: TEST [0.85, 1.0) was partially observed in V1/V2; **V3 states explicitly that no fresh untouched holdout exists in the repository data**. TEST is re-used only as a pre-registered confirmatory layer and interpreted conservatively; primary inferential claims rest on VALIDATION and walk-forward stability.
6. Negative results and falsification are the intended outcomes if the evidence so dictates.
7. One confirmatory pass. No iteration.

## 3. Data

- `data/m1/XAGUSD_M1.csv` (lead) and `data/m1/EURUSD_M1.csv` (negative control). Same format as V1/V2; SHA-256 fingerprints recorded.
- No volume used (100% zero rows in XAGUSD; verified V1/V2).

## 4. Event definitions (carried forward from V2, unchanged)

- **N1** rolling price z-score: `(close − SMA₁₂₀)/σ₁₂₀(close)`.
- **N2** ATR-relative displacement: `(close − SMA₁₂₀)/ATR₁₂₀` (mean true range over 120).
- **Primary threshold: ±3.0** for both normalizations (V2 value, pre-registered).
- DOWN event at `t` iff `norm ≤ −3.0`; UP iff `norm ≥ +3.0`. Same-direction minimum separation `S=240` bars (unchanged from V1/V2). Warm-up `W=120`; outcome horizon `H=120` (bars `t+1..t+H`).
- Direction-adjusted return: DOWN `+ret`, UP `−ret`; hypothesized signs FIXED (DOWN → positive, UP → negative); never flipped.

## 5. Primary confirmatory family (XAGUSD, VALIDATION [0.70, 0.85), primary threshold ±3.0)

Four tests with **cluster bootstrap** inference (below):

| ID | Test | Expected sign |
|----|------|---------------|
| F1 | N1 DOWN, mean dir-adj return vs 0 | + |
| F2 | N1 UP, mean dir-adj return vs 0 | + |
| F3 | N2 DOWN, mean dir-adj return vs 0 | + |
| F4 | N2 UP, mean dir-adj return vs 0 | + |

Baseline: the pooled direction-adjusted H-bar partition baseline is ≈0 by construction; the test is mean(event dir-adj return) ≠ 0. The partition-baseline mean is reported alongside.

## 6. Entry-at-confirmation persistence (fixes the V2 confound)

- Confirmation point **K = 60 bars** after the event.
- Confirmation uses **only bars t+1..t+K**. No price information after `t+K` influences the decision.
- Confirmation condition (reversion-side, direction-specific):
  - DOWN event confirmed iff fraction of bars `t+1..t+60` with `close > close[t]` ≥ **0.6** (recovery holding above entry).
  - UP event confirmed iff fraction of bars `t+1..t+60` with `close < close[t]` ≥ **0.6** (price holding below entry).
- Entry at `t+K`. Outcome measured from `t+K`: `ret_K = close[t+K+H]/close[t+K] − 1`; direction-adjusted (`−ret_K` for UP). **The outcome window [t+K, t+K+H] does not overlap the confirmation window [t+1, t+K].**
- Events analyzed for confirmation require `t + K + H ≤ partition_end`.
- Secondary confirmatory tests (XAGUSD, VALIDATION):

| ID | Test |
|----|------|
| F5 | N1 confirmed-entry mean dir-adj outcome (vs t+K baseline, ≈0) |
| F6 | N2 confirmed-entry mean dir-adj outcome |
| F7 | N1 confirmed vs unconfirmed post-confirmation outcome difference |
| F8 | N2 confirmed vs unconfirmed post-confirmation outcome difference |

F7/F8 test whether the confirmation filter adds discrimination beyond the mechanical first-hour continuation; both groups are measured from `t+K`.

## 7. Negative control (EURUSD, VALIDATION, primary threshold)

Four tests with identical machinery, expected null:

| ID | Test |
|----|------|
| C1 | N1 DOWN mean dir-adj |
| C2 | N1 UP mean dir-adj |
| C3 | N2 DOWN mean dir-adj |
| C4 | N2 UP mean dir-adj |

A significant C-test signals machinery failure or a false positive and must be reported prominently.

## 8. Dependence-aware inference (cluster bootstrap)

- **Dependence structure:** event outcome windows `[t+1, t+H]` overlap iff `|t_i − t_j| < H`. Clusters = connected components of the overlap graph over ALL events (both directions) in the analysis window.
- **Cluster bootstrap:** resample clusters with replacement (B=2000, seeded); pool events within resampled clusters (cluster-size weighting is natural); compute the statistic per resample. Cluster-resampled mean, 95% CI, and **bootstrap p-value**: null-centered distribution `(T* − T_obs)`; two-sided `p = (1 + #{|T*−T_obs| ≥ |T_obs|})/(1+B)`.
- For confirmed-vs-unconfirmed (F7/F8): the same cluster resampling; the difference of group means within resampled clusters; resamples lacking one group are skipped and B_eff reported.
- Reported per analysis cell: raw event count, cluster count (effective independent episodes), mean/max cluster size, first-order serial correlation of event returns, and an explicit statement that clusters — not bars or raw events — are the independence unit.
- **Cluster size for post-confirmation outcomes:** `|t_i − t_j| < H` on `[t+K, t+K+H]` windows (same rule).

## 9. Multiplicity control

- **Pre-registered family: 12 tests** (F1–F8 + C1–C4), Holm-corrected at family-wise α = 0.05. Family is fixed before results.
- TEST holdout results are reported as a **separate secondary layer** (4 XAGUSD tests at primary threshold, Holm within that layer) and interpreted only as follow-up of the primary results — never as fresh confirmation.

## 10. Holdout

- **No fresh untouched holdout exists** (data ends at the V1/V2 TEST boundary; TEST was reported in V1 and V2). Explicitly stated per §2.5.
- TEST [0.85, 1.0) re-run with cluster-bootstrap inference as the secondary layer; results labeled with the reuse caveat.

## 11. Threshold robustness (confirmatory, not optimization)

- VALIDATION, N1 and N2, DOWN and UP, thresholds **{2.5, 3.0, 3.5}**: event count, cluster-bootstrap mean + CI.
- Interpretation: a **stable region** (adjacent thresholds positive, CIs overlapping) vs a **sharp spike** (isolated significance) vs flat/no-effect. A spike is evidence of instability.

## 12. Normalization robustness

- N1 vs N2 at primary threshold (the family above) and at **matched rarity** (TRAIN-based 0.5% / 99.5% quantiles per normalization, VALIDATION) with cluster-bootstrap CIs. N3 is retained as a pre-registered secondary sensitivity row at matched rarity only (V2 showed ±3.0 gives it too few events).

## 13. Temporal stability

- Walk-forward folds (fractions of the full span): A [0.40,0.50), B [0.50,0.60), C [0.60,0.70), D [0.70,0.85) — same as V2, cluster-bootstrap CIs.
- Chronological thirds (primary event definition per third) — cluster-bootstrap CIs.
- Interpretation: persistent / decaying / episodic / regime-specific.

## 14. Cost-aware economic analysis (assumption, clearly labelled)

- No spread/bid-ask data exists in the repository (volume unusable). A **pre-registered sensitivity band** of round-trip costs is applied: **{0, 5, 10, 20, 30} bp**. These are assumptions representing plausible XAGUSD M1 spread + slippage (statement: "cost band is an assumption; no observed spread data is available").
- Reported per strategy cell (N1/N2 × DOWN/UP, VALIDATION + TEST): gross mean effect (bp over 2 h), cost-adjusted means per band, **break-even round-trip cost** (bp), and viability classification: viable only if the effect exceeds a plausible cost band with CI support.

## 15. Outcome measures

Identical to V1/V2 for the t-referenced analysis (MAE/MFE/recovery/retention recorded in the event dataset). Post-confirmation outcome: `close[t+K+H]/close[t+K] − 1`, direction-adjusted.

## 16. Stopping rules

1. If the primary family (F1–F8) has **no** Holm survivor with the expected sign → **GATE 1 FAILED — HYPOTHESIS NOT CONFIRMED**; stop.
2. If the lead survives the primary family but fails holdout, walk-forward stability, normalization robustness, or cost viability → **GATE 1 FAILED — EVIDENCE INSUFFICIENT** (or PARTIALLY PASSED, per the evidence).
3. If a C-test (negative control) is significant → machinery/false-positive alert; report prominently and treat all positive claims with extra skepticism.
4. No iteration within V3.

## 17. Promotion gate

V3 recommends **SCIENTIFIC SPECIFICATION READINESS REVIEW** only if ALL of: directional coherence; dependence-aware significance (Holm family F1–F8); holdout support; walk-forward stability; threshold-region stability; normalization robustness (N1 AND N2); economically meaningful after plausible costs; reproducibility; non-confounded event/persistence definitions; no remaining critical semantic gaps. Anything less → **GATE 1 FAILED / DESIGN BLOCKED** and V3 must state what remains.

## 18. Reproducibility

Recorded with outputs: protocol V3.0.0, seeds (20260814), all parameters, source SHA-256 fingerprints, pandas/numpy versions, script identity, event-dataset row count + SHA-256, cluster-bootstrap settings, cost assumptions, output artifact hashes.

## 19. Outputs (all under `output/event_study_v3/`)

`EVENT_STUDY_PROTOCOL_V3.md`, `run_event_study_v3.py`, `event_dataset_V3.csv`, `dependence_analysis.csv`, `cost_sensitivity.csv`, `threshold_robustness.csv`, `normalization_comparison.csv`, `walk_forward.csv`, `holdout_results.csv`, `confirmatory_results.csv`, `experiment_metadata_V3.json`, `final_scientific_report.md`. V1 and V2 outputs are untouched.

---

*Pre-registered 2026-08-12 before any confirmatory outcome inspection. No threshold, confirmation rule, cost band, or family member was chosen after inspecting outcomes.*
