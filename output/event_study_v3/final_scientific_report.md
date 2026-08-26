# QuantForge — Canonical Mean-Reversion Event Study V3 — Final Scientific Report

**Protocol:** V3.0.0 (pre-registered, `EVENT_STUDY_PROTOCOL_V3.md`) · **Date:** 2026-08-12 · **Area:** `output/event_study_v3/`
**Design posture:** adversarial confirmation / falsification of the V2 XAGUSD lead.

---

## 1. Executive Verdict

**GATE 1 FAILED — EVIDENCE INSUFFICIENT.**

The XAGUSD down-displacement reversion effect is **real and reproducible in a narrow, direction-specific sense** — it survives dependence-aware cluster-bootstrap inference (F1: N1 DOWN, +0.00109, p_holm = 0.006, the single Holm survivor of a 12-test family with a clean negative control), it is a **monotone stable threshold region** (not a spike), it is **positive in every walk-forward fold and every chronological third**, and it holds direction and magnitude on the holdout (+0.00101 vs +0.00109 on VALIDATION). But it **fails the promotion gates that matter for a scientific specification**: it is economically marginal-to-non-viable under realistic transaction costs (gross ≈ 10.9 bp over 2 h; break-even round-trip ≈ 10 bp; dies at 20–30 bp; the N2 variant dies at 5 bp), it is **directionally asymmetric** (DOWN robust at ±3.0, UP present only at extreme matched rarity), it is **normalization-partial** (only N1 of the two primary normalizations survives Holm), it loses **narrow-CI holdout significance**, it is single-market with **no mechanistic justification**, and the multiplicity record is 1/12. Entry-at-confirmation persistence is now cleanly designed and shows **no discrimination value** — confirming that the V2 persistence result was mechanical.

The effect cannot justify a Scientific Specification Readiness Review. This is a valid scientific result: the lead is genuine but economically insufficient and semantically incomplete.

## 2. V1 → V2 → V3 Reasoning

- **V1:** single operationalization failed GATE 1 (2/30 cells, no OOS reversion, no threshold region, no portability).
- **V2:** alternative normalizations, regime/walk-forward, persistence — XAGUSD DOWN emerged as the one coherent lead (Holm survivor, matched-quantile both directions, walk-forward/regime/chrono stable). Persistence found mechanically confounded.
- **V3:** adversarial confirmation of the XAGUSD lead only: dependence-aware inference, leakage-free entry-at-confirmation persistence, cost bands, holdout, threshold/normalization/negative-control robustness.

## 3. Pre-Registered Protocol

`EVENT_STUDY_PROTOCOL_V3.md` (frozen before any confirmatory outcome inspection): XAGUSD-only (EURUSD as single negative control); N1/N2 at primary threshold ±3.0; entry-at-confirmation K=60 with direction-specific reversion-side retention ≥ 0.6; cluster bootstrap (overlapping-window clusters over ALL events) with null-centered p-values; 12-test Holm family (F1–F8 lead + C1–C4 control); threshold neighborhood {2.5, 3.0, 3.5} evaluated confirmatorily; matched-rarity (0.5% quantiles) normalization comparison incl. N3 sensitivity; walk-forward folds A–D and chronological thirds; TEST as secondary layer with explicit reuse caveat (no fresh holdout exists); cost band {0, 5, 10, 20, 30} bp round trip as labelled assumptions; stopping rules; reproducibility requirements.

## 4. Event Definition

Carried forward unchanged from V2: N1 `(close−SMA₁₂₀)/σ₁₂₀`; N2 `(close−SMA₁₂₀)/ATR₁₂₀`; ±3.0; S=240 same-direction separation; H=120 outcomes; direction-adjusted returns with fixed hypothesized signs. No thresholds or definitions were changed after outcomes.

## 5. Dependence-Aware Inference

- Cluster bootstrap over connected components of the window-overlap graph (|Δt| < 120) built across BOTH directions; statistics pool the direction-selected events within resampled clusters (preserves cross-direction dependence). Null-centered bootstrap p-values, B=2000, seeded.
- **Within-VALIDATION dependence is mild:** XAGUSD N1: 686 clusters / 770 events, 84 direction-mixing pairs, max cluster size 2, mean size seen 1.18–1.27; N2: 1,048 clusters / 1,532 events, 484 mixing pairs, max 2. Event-return serial correlation |r| ≤ 0.15.
- The cluster bootstrap widened F1's CI only marginally ([0.00063, 0.00156] vs event-level [0.00063, 0.00154]) — **dependence does not explain the effect.** Effective independence unit = cluster (~686 for N1 VALIDATION), not raw bars.
- Note: the earlier large V2 overlap counts arose from pooling across partitions; per-partition analysis (events ≥ H from boundaries) is substantially cleaner.

## 6. Persistence / Entry-at-Confirmation

Leakage-free design (confirmation uses t+1..t+60 only; entry and outcome begin at t+60; outcome window does not overlap the confirmation window). **All four tests are null**:
- Confirmed-entry outcome vs baseline: F5 N1 +0.00025 (p=0.27), F7 N2 +0.00007 (p=0.63).
- Confirmed vs unconfirmed discrimination: F6 N1 +0.00025 (p=0.48), F8 N2 −0.00032 (p=0.17).

**The confirmation filter adds no discrimination value.** The V2 persistence effect is confirmed to be mechanical first-hour drift, not a usable event-definition component.

## 7. Holdout Confirmation

**No fresh untouched holdout exists** (data ends at the V1/V2 TEST boundary; TEST was reported in V1 and V2). TEST [0.85, 1.0) was re-run as a secondary layer with the reuse caveat:

| Test | Effect | CI | p |
|---|---|---|---|
| H1 N1 DOWN | +0.00101 | [−0.00040, 0.00237] | 0.167 |
| H2 N1 UP | −0.00093 | [−0.00273, 0.00151] | 0.400 |
| H3 N2 DOWN | +0.00015 | [−0.00089, 0.00115] | 0.771 |
| H4 N2 UP | −0.00018 | [−0.00130, 0.00101] | 0.739 |

**Direction and magnitude are consistent with VALIDATION (H1 +0.00101 vs F1 +0.00109); narrow-CI significance is not achieved** (p=0.167, n=484). Holdout support: partial.

## 8. Cost-Aware Analysis

Gross effects (bp over 2 h), N1/N2 × DOWN/UP, VALIDATION + TEST:

| Cell | Gross | −5 bp | −10 bp | −20 bp | −30 bp | Break-even |
|---|---|---|---|---|---|---|
| N1 DOWN VAL | 10.86 | 5.86 | 0.86 | −9.14 | −19.14 | 10.86 |
| N1 DOWN TEST | 10.07 | 5.07 | 0.07 | −9.93 | −19.93 | 10.07 |
| N2 DOWN VAL | 4.41 | −0.59 | −5.59 | −15.59 | −25.59 | 4.41 |
| N2 DOWN TEST | 1.53 | −3.47 | −8.47 | −18.47 | −28.47 | 1.53 |
| N1/N2 UP | ≤ 0 | ≤ 0 | ≤ 0 | ≤ 0 | ≤ 0 | ≤ 0 |

**Classification: economically non-viable under realistic costs.** The cost band is a labelled assumption (no spread data in the repository; volume unusable). The effect survives only at the very bottom of a plausible XAGUSD M1 band (~5 bp round trip) for N1, and dies at 10+ bp; N2 dies at 5 bp. Break-even round-trip ≈ 10 bp (N1). This fails the "economically meaningful after costs" gate.

## 9. Normalization Robustness

- **Primary threshold ±3.0:** N1 DOWN Holm-significant (F1); N2 DOWN same sign but p_holm=0.121 (fails). N3 at ±3.0: 9–18 events only.
- **Matched rarity (0.5% quantiles):** N1 DOWN +0.00131 (p=0.0005) and N1 UP −0.00101 (p=0.027); N2 DOWN +0.00242 (p=0.0005) and N2 UP −0.00282 (p=0.004); N3 DOWN +0.00100 (p=0.082, marginal), N3 UP −0.00082 (p=0.174). **At equal rarity the effect is symmetric in both directions under N1 and N2** and directionally consistent (not significant) under N3.
- Conclusion: robust to N1/N2 (both directions at matched rarity), N3 directionally consistent but not significant. Normalization robustness: PARTIAL (one primary Holm survivor; N3 weak).

## 10. Threshold Robustness

**Stable monotone region, not a spike** (VALIDATION, DOWN):
- N1: +0.00064 (2.5) → +0.00109 (3.0) → +0.00155 (3.5); all CIs exclude 0; p ≤ 0.001.
- N2: +0.00038 (2.5) → +0.00044 (3.0) → +0.00065 (3.5); all CIs exclude 0; p ≤ 0.018.
- The effect strengthens with extremity — a robust region, the correct signature for a genuine effect.

## 11. Walk-Forward / Temporal Stability

- **N1 DOWN: positive in all 4 folds** (+0.00033, +0.00072, +0.00028, +0.00109); fold D (=VALIDATION) significant; A/B/C CIs wide.
- **N2 DOWN: positive in all 4 folds** (+0.00012, +0.00028, +0.00020, +0.00044); D significant.
- **Chronological thirds (N1 DOWN): +0.00031 / +0.00063 / +0.00089 — monotonically increasing, positive in all three calendar periods** (N2 likewise positive in all three). The effect is **persistent and strengthening, not decaying or episodic.**

## 12. Directionality

**Directionally asymmetric at the primary threshold** (DOWN robust: F1 significant; UP null: F2 p=0.68, F4 p=0.88) and **symmetric only at extreme matched rarity** (both directions significant for N1/N2). Per the protocol's classification rule: this must NOT be called generic "mean reversion" — it is a **directional asymmetry** (XAGUSD downward displacement followed by upward reversion) whose UP-side dependence on rarity is unexplained. Separate scientific interpretation would be required before any use.

## 13. Multiple Comparison Control

12 pre-registered tests, Holm α=0.05: **1/12 Holm survivors (F1, p_holm=0.006)**. Negative control (C1–C4, EURUSD) entirely null (best p=0.297) — the inference machinery does not manufacture false positives. Holdout layer (4 tests, Holm within layer): none significant (best p=0.167).

## 14. Negative Findings / Falsification

The experiment actively sought falsification and found it in material form:
1. **Economic non-viability** — the effect dies under realistic costs (break-even ≈ 10 bp; N2 at 5 bp). FAIL.
2. **Normalization partiality** — only 1 of 2 primary normalizations survives Holm; N3 not significant. PARTIAL FAIL.
3. **Holdout narrow-CI failure** — direction/magnitude hold, significance does not (p=0.167). PARTIAL FAIL.
4. **Directional asymmetry** — UP-side only at extreme rarity; not symmetric at operating thresholds. UNRESOLVED.
5. **Persistence adds nothing** — entry-at-confirmation discrimination null; V2's persistence effect was mechanical. CONFIRMED NEGATIVE.
6. **Market-specificity mechanism** — no mechanistic justification; single-market empirical effect only. UNRESOLVED.
7. **Multiplicity** — 1/12. WEAK.
8. Dependence, threshold-region, walk-forward, chrono, negative-control, and matched-rarity normalization checks all PASS — the effect is not an artifact of those.

## 15. Scientific Specification Matrix

| Semantic | V2 | V3 Result | Production Ready? |
|---|---|---|---|
| Event definition | PARTIAL (XAGUSD) | CONFIRMED (XAGUSD DOWN) | NO |
| Trigger | UNESTABLISHED | PARTIAL (monotone region; DOWN) | NO |
| Normalization | PARTIAL (N1/N2) | PARTIAL (N1 Holm; N2 marginal; N3 ns) | NO |
| Threshold | UNESTABLISHED | PARTIAL (stable region 2.5–3.5, DOWN) | NO |
| Direction | PARTIAL (asym) | ASYMMETRIC (DOWN robust; UP matched-only) | NO |
| Recoil | UNESTABLISHED | UNESTABLISHED | NO |
| Persistence | CONTRADICTED (confounded) | **CONFIRMED NULL** (no discrimination) | NO |
| MAE/MFE | ESTABLISHED | ESTABLISHED (research-local) | n/a |
| Event boundaries | PARTIAL | PARTIAL | NO |
| Regime dependence | PARTIAL | CONFIRMED STABLE (all folds/thirds) | n/a |
| Cross-market | CONTRADICTED | CONTRADICTED (single-market) | NO |
| Cost viability | n/a | **CONTRADICTED** (non-viable at realistic costs) | NO |
| Parameter schema | UNESTABLISHED | UNESTABLISHED | NO |

## 16. Economic / Statistical Conclusion

Statistically: a real, reproducible, dependence-aware, threshold-stable, temporally persistent directional asymmetry in XAGUSD (1/12 Holm, clean control). Economically: **not viable** — gross 10.9 bp over 2 h, break-even ≈ 10 bp round trip, dying at 20–30 bp, N2 variant dead at 5 bp. A tiny effect that vanishes after plausible costs is not an implementable edge. The verdict separates cleanly: statistical significance ≠ behavior proven ≠ economic edge.

## 17. Remaining Critical Gaps

1. **Actual XAGUSD M1 transaction-cost data** (spread/slippage) — the decisive unknown; the effect's fate rests on whether real round-trip costs are < 10 bp.
2. **Market-specificity mechanism** for XAGUSD (silver microstructure) — or explicit acceptance of an empirical-only boundary.
3. **Directional asymmetry semantics** — why DOWN is robust at ±3.0 while UP appears only at matched rarity.
4. **N3 robustness** — directionally consistent but not significant.
5. **Fresh holdout** — none exists in the repository data.

## 18. Promotion Decision

**GATE 1 FAILED — EVIDENCE INSUFFICIENT.** Not because the effect is absent (it is real in a narrow sense) but because the evidence cannot support a Scientific Specification Readiness Review: the economics fail decisively, normalization and holdout support are partial, the directionality is asymmetric/unresolved, and the market-specificity mechanism is unestablished. The correct scientific conclusion: the XAGUSD lead is a genuine but economically non-viable directional asymmetry under the assumptions available; engineering remains DESIGN BLOCKED and must NOT begin.

## 19. Exact Next Research / Engineering Task

**No engineering task.** The only legitimate next research step is a **cost-viability assessment using external, observed XAGUSD M1 transaction-cost data** (the effect's fate is decided by whether real round-trip costs are below ~10 bp). If external cost data is unavailable or shows costs ≥ 10 bp, the lead should be **closed as economically non-viable** and recorded in `research/knowledge/RESEARCH_DISCOVERY_DATABASE.md` as a DISC-style negative/conditional finding. The detector milestone remains DESIGN BLOCKED; no scientific specification exists to implement.

---

*Research artifact. V1 and V2 remain valid, unmodified scientific results. All artifacts and hashes are in `output/event_study_v3/`; full parameter/seed/fingerprint records in `experiment_metadata_V3.json`.*
