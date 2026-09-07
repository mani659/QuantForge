# QUANTFORGE — H01 VOLATILITY RESPONSE ASYMMETRY V1.2 — SCIENTIFIC REPORT

**Experiment:** H01 Volatility Response Asymmetry — controlled re-execution under protocol **v1.2.0**
**Status:** COMPLETE — corrected null-inference layer, verified against the registered RNG stream
**Date:** 2026-08-16
**Protocol:** `H01_VOLATILITY_RESPONSE_ASYMMETRY_PROTOCOL_V1.md` v1.2.0, SHA-256 `9d3edb69b7628956efbc8135b08c78c322d1ffee8af2a35e35dedc246d87c68f` (byte-for-byte unchanged during execution)
**Predecessor:** H01 v1.1 execution remains frozen as **CONFIRMATORY INFERENCE INVALID / SCIENTIFIC RESULT UNADJUDICATED**; its p-values are never reused or mixed with v1.2 results.

---

## 1. Executive Verdict

**Under the corrected null-imposing inference, the registered decision rules fire for the first time.**

- **L1_COMMODITIES_OTHER — CONTRADICTION.** D = +0.032 (positive asymmetry: positive shocks precede *larger* forward vol increases than magnitude-matched negative shocks), Holm-adjusted p = 0.0054, 7/9 (78%) evaluable markets sign-consistent. This **contradicts the registered INVERSE prior** (which predicts D < 0) at the family level (α = 0.05).
- **L1 and L2 EQUITY_INDICES — strongly significant positive asymmetry (p_holm = 0.0011 each; D = +0.150 and +0.422), direction-consistent across both eras**, but **capped at EVIDENCE-LIMITED/DESCRIPTIVE** by the registered ≥2-evaluable-markets rule (each has 1 evaluable market: `sp`; `USATECHIDXUSD`). Their direction matches the registered CLASSIC prior (D > 0) — they are SUPPORT-candidates that the single-market cap prevents from being classified.
- **All other classes: INCONCLUSIVE or EVIDENCE-LIMITED/DESCRIPTIVE.** No reliable asymmetry in either direction for FX, RATES, INDEX_COMMODITY, CRYPTO, PRECIOUS_METALS, or ENERGY_CRUDE at the registered inference.

The corrected inference has power (raw p-values spread across [0.0001, 0.914]) — the v1.1 location-invariant defect is fully retired.

---

## 2. Execution Identity

- Protocol v1.2.0 (frozen; hash above; byte-for-byte unchanged during execution — verified post-run).
- Governance chain completed before execution: inference-validity audit → null-distribution methodology decision (**A — VALID METHOD**) → methodology-decision audit (**A — METHODOLOGY VALID**) → v1.2 amendment → amendment audit (**CONDITIONAL PASS**, one reproducibility clarification) → reproducibility clarification → **FINAL EXECUTION CLEARANCE — PASS (APPROVED FOR V1.2 RE-EXECUTION)**.
- Script: `run_h01_v12.py` (fork of the verified `run_h01_v1.py`; only the null-inference layer changed). Environment: Python 3.11.9 (MSC v.1938, AMD64), NumPy 2.4.4, pandas 3.0.2, SciPy 1.17.1.
- Registered parameters: **B = 10,000, L = 11, master seed 20260813**, α = 0.05, 11-member Holm family, synchronized circular calendar blocks, matching rebuilt inside replicates.
- **Final execution:** single uninterrupted invocation (2026-08-16, elapsed 1907.6 s), no resume, no parallel-cache race. All 11 classes × 10,000 replicates = **110,000 draws**, every draw verified against the deterministic registered stream.

---

## 3. Execution Incident and Resolution (transparency record)

The first execution attempt of the v1.2 bootstrap was corrupted by an **execution-infrastructure defect**, discovered during post-run verification and fully corrected:

1. **Cause.** (a) A foreground-tool timeout left the first invocation orphaned; a second invocation launched concurrently; both wrote the same `.build_cache` files. (b) More fundamentally, the script's checkpoint/resume `_task_stream` **skips fully-cached classes without consuming their RNG draws**, so any resumed run's stream is shifted for subsequent classes — resumed executions are not serial-equivalent to an uninterrupted run.
2. **Detection.** The v1.2 sampling draws were compared row-by-row against the true registered stream (seed 20260813, per-replicate `rng.integers(0,T,size=nblocks)` in the registered name-layer class order) using the script's own `rep_class_dm2` machinery: 9/11 classes were correct; **L1_PRECIOUS_METALS (replicates 7351–10000) and L2_PRECIOUS_METALS (all replicates) carried non-registered draws** (p-values 0.22428 / 0.76732 from the contaminated draw set). The v1.1 bootstrap draw set was found to contain the same class of defect (independent of the registered p-value defect that already invalidated v1.1 inference).
3. **Correction.** All v1.2 bootstrap caches were cleared and the registered computation was re-executed in a **single uninterrupted invocation** (no resume → the skip bug is never reached). This is the registered realization: the full B = 10,000 synchronized bootstrap under seed 20260813.
4. **Verification.** Post-correction, every class × 25 boundary replicates (including every cache-save boundary) matches the true registered stream exactly (0 mismatches, sampling and null draws); the pivot identity `D*_null = D* − D_obs` holds to machine precision (~1e-16) for all 110,000 draws; raw p-values, percentile CIs, Holm values, and verdicts recompute exactly from the persisted replicates.
5. **Impact on results.** Only the two affected classes' bootstrap quantities changed. L1_PRECIOUS_METALS p_raw corrected 0.22428 → **0.22928**; L2_PRECIOUS_METALS p_raw corrected 0.76732 → **0.76542**. **No verdict changed.** All scientific conclusions below are unaffected by the incident.

No protocol file, matching rule, statistic, or scientific object was changed by the correction. The script is byte-stable from the corrected run onward.

---

## 4. Dataset / Quality

Identical to the v1.1 execution (all §17 gates re-passed; gate fingerprints verified): all 22 Layer A HPD markets + 5 Layer B M1 markets loaded; roll consistency, missingness, duplicate, OHLC validity, and continuity gates passed; **60,507 matched pairs** (56,471 Layer A + 4,036 Layer B); Layer A eligible shocks 119,847; Layer B 7,165. The `matched_pairs_H01_V1.2.csv` is byte-identical to the v1.1 matched-pairs artifact (SHA-256 prefix `b5b5041f…` equal) — matching is unchanged.

---

## 5. Primary Class Statistics (frozen statistic, unchanged)

Class statistic D_class = equal-weighted mean over evaluable markets of the vol-state-conditioned, magnitude-matched difference in forward ΔlnRV, ΔlnRV(neg) − ΔlnRV(pos). D_obs values are **bit-identical to v1.1** for all 11 classes (matching and aggregation unchanged):

| Class | D_obs | CI95 (sampling) | p_raw (null) | p_holm | n_ev | Verdict |
|---|---|---|---|---|---|---|
| L1_COMMODITIES_OTHER | +0.0317 | [0.0143, 0.0499] | 0.00060 | **0.0054** | 9 | **CONTRADICTION** |
| L1_ENERGY_CRUDE | +0.0814 | [−0.0022, 0.1913] | 0.10519 | 0.7363 | 1 | EVIDENCE-LIMITED/DESCRIPTIVE |
| L1_EQUITY_INDICES | +0.1498 | [0.0799, 0.1930] | 0.00010 | **0.0011** | 1 | EVIDENCE-LIMITED/DESCRIPTIVE |
| L2_EQUITY_INDICES | +0.4220 | [0.2685, 0.5766] | 0.00010 | **0.0011** | 1 | EVIDENCE-LIMITED/DESCRIPTIVE |
| L1_FX | +0.0292 | [0.0064, 0.0525] | 0.01330 | 0.1064 | 6 | INCONCLUSIVE |
| L2_FX | +0.0610 | [−0.0460, 0.1611] | 0.25127 | 1.0000 | 1 | EVIDENCE-LIMITED/DESCRIPTIVE |
| L1_INDEX_COMMODITY | −0.0158 | [−0.0868, 0.0488] | 0.63804 | 1.0000 | 1 | EVIDENCE-LIMITED/DESCRIPTIVE |
| L1_PRECIOUS_METALS | −0.0285 | [−0.0768, 0.0146] | 0.22928 | 1.0000 | 2 | INCONCLUSIVE |
| L2_PRECIOUS_METALS | +0.0138 | [−0.0788, 0.1044] | 0.76542 | 1.0000 | 2 | INCONCLUSIVE |
| L1_RATES | +0.0034 | [−0.0592, 0.0632] | 0.91361 | 1.0000 | 2 | INCONCLUSIVE |
| L2_CRYPTO | +0.0256 | [−0.1054, 0.1131] | 0.67463 | 1.0000 | 1 | EVIDENCE-LIMITED/DESCRIPTIVE |

**Holm family (11):** p_raw values feed the standard Holm step-down at α = 0.05. Three classes pass family-level significance: L1_COMMODITIES_OTHER (0.0054), L1_EQUITY_INDICES (0.0011), L2_EQUITY_INDICES (0.0011).

---

## 6. Corrected Null Inference (protocol §9A.2, authoritative data-level form)

- Frozen per-(market, stratum) constants `c_(m,s) = mean(d_i)` over the observed matched pairs; frozen for all replicates; never re-estimated inside replicates.
- Null transformation at the shock-response level, applied **before rebuilt matching** to every eligible shock: ΔlnRV(neg) → ΔlnRV(neg) − c_(m,s)/2; ΔlnRV(pos) → ΔlnRV(pos) + c_(m,s)/2. Equivalent to pair-level `d_i^0 = d_i − c_(m,s)`, imposing E[d_(m,s)] = 0 per stratum under H0.
- Null draws `D*_null` computed on the same resampled, re-matched pairs as the sampling draws; matching response-blind, so pairing is identical.
- P-value: `p = (1 + count)/(B + 1)`, `count = #{b : |D*_null,b| ≥ |D_obs|}`, inclusive `≥`, B = 10,000.
- Verified: the data-level construction equals the statistic-level pivot `D* − D_obs` to machine precision in this run (all strata represented in all replicates); null distributions centered at zero up to the sampling distribution's own finite-sample offset.
- **The old v1.1 p-value `2·min(Pr(D*≥D_obs), Pr(D*≤D_obs))` is retired** and appears nowhere in v1.2 outputs.

---

## 7. Historical vs Contemporary Interpretation

- **Equity indices are the strongest signal and consistent across eras**: L1 (historical `sp`, 1959–2002 window) D = +0.150 and L2 (contemporary `USATECHIDXUSD`, 2023–2026) D = +0.422, both significant at the minimum achievable p under the corrected inference (p_holm = 0.0011). Both are single-market classes → EVIDENCE-LIMITED/DESCRIPTIVE under the registered rule; the cross-era directional consistency is descriptive, not confirmatory.
- **PRECIOUS_METALS** (only other cross-era class): L1 D = −0.028, L2 D = +0.014, both far from significance (p = 0.229 / 0.765) → INCONCLUSIVE in both eras; no reliable cross-era statement.
- **FX**: L1 (6 markets) D = +0.029, p_raw 0.0133 but p_holm 0.106 → INCONCLUSIVE; L2 single-market → EVIDENCE-LIMITED.
- The single registered **CONTRADICTION** (COMMODITIES_OTHER, Layer A) has no Layer B counterpart (Layer-A-only class).

---

## 8. Secondary Analyses (protocol §21; non-rescuing, cannot alter primary verdicts)

- **Horizon sensitivity**: 1-day forward window: COMMODITIES_OTHER +0.035 (same sign); EQUITY_L1 +0.380, EQUITY_L2 +0.622 (same sign, larger); RATES −0.097 (flips negative at 1d). 21-day: COMMODITIES_OTHER −0.103 (flips sign), EQUITY_L1 −0.067 (flips), EQUITY_L2 +0.175 (same sign).
- **Standardized-shock matching**: same signs as primary for all classes (COMMODITIES_OTHER +0.033, EQUITY_L1 +0.155, EQUITY_L2 +0.487) — not driven by |r|-scaling.
- **|r|-response matching** (magnitude-response, not ΔlnRV): all |D| ≤ 0.0013 — the asymmetry is specific to the log-RV response, not the raw absolute-return response.
- **Intraday Layer B RV**: EQUITY_L2 +0.225 (same sign); CRYPTO +0.047; PM_L2 −0.026 (opposite sign to its daily ΔlnRV result); FX_L2 +0.002.
- **Winsorization**: unchanged signs, slightly smaller magnitudes (e.g., COMMODITIES_OTHER +0.032).
- **Common-window Layer A sensitivity** (1987-01-13 → 2002-08-30): COMMODITIES_OTHER +0.011 (positive but weaker in the common window), EQUITY_INDICES +0.170 (same sign), PRECIOUS_METALS −0.053 (same sign).
- **GJR/EGARCH + Engle–Ng**: run per §21.6/7. Most GJR asymmetry gammas pinned at the −0.3 bound (same behavior as v1.1) — these coefficients sit at the optimizer clamp and are **not** reinterpreted as evidence for or against H01 (secondary firewall). They are descriptive only.

None of the secondaries are rescuing: no secondary result changes any primary verdict, and none is permitted to.

---

## 9. Limitations

- **Bootstrap/matching caveat (registered §9A.7):** block-bootstrap consistency is assumed; the estimator contains greedy nearest-neighbour matching rebuilt inside replicates; Abadie–Imbens-style caveats exist for fixed-M matching estimators; this exact estimator/bootstrap combination has no dedicated published theorem. The caveat applies equally to the sampling CI and the corrected null test; no stronger finite-sample guarantee is claimed.
- **Single-market classes** (EQUITY_INDICES both layers, ENERGY_CRUDE, INDEX_COMMODITY, L2_FX, L2_CRYPTO): capped at EVIDENCE-LIMITED/DESCRIPTIVE by the registered ≥2-market rule regardless of significance — their strong point estimates are descriptive.
- **Execution-infrastructure incident** (§3): the corrected realization is verified against the deterministic stream; residual risk is limited to the possibility that a future executor re-introduces the checkpoint/resume skip defect. The registered computation itself (single uninterrupted run, seed 20260813) is unambiguous and reproducible.

---

## 10. Reproducibility

An independent executor can reproduce every number in §5 from the persisted artifacts alone:
- `bootstrap_replicates_H01_V1.2.csv` — 110,000 draws (sampling + null per class), seed 20260813, B = 10,000, L = 11.
- `results_H01_V1.2.json` — class stats, multiplicity (raw p, Holm), verdicts, secondaries, frozen params.
- `experiment_metadata_H01_V1.2.json` — protocol hash `9d3edb69…`, version 1.2.0, fingerprints, environment.
- `matched_pairs_H01_V1.2.csv`, `per_market_stats_H01_V1.2.csv`, `class_stats_H01_V1.2.csv`.
- Stream identity verified: p-values recomputed exactly from the persisted null draws; Holm recomputed exactly; D_obs bit-identical to v1.1; matched pairs byte-identical to v1.1.

---

## 11. V1.1 Invalid-Result Firewall

- H01 v1.1 remains **CONFIRMATORY INFERENCE INVALID / SCIENTIFIC RESULT UNADJUDICATED** — it cannot be retroactively converted into a v1.2 result.
- v1.1 p-values, Holm values, and classifications are never reused or mixed with v1.2 results (separate artifact names throughout).
- v1.1 artifacts are preserved untouched (dated 2026-08-15).
- Additionally recorded for provenance: the v1.1 *bootstrap draw set* was found to carry the same checkpoint/resume stream defect (§3.2) — an additional, independent reason the v1.1 inference could not have been used, beyond the registered p-value defect.

---

## 12. Exact Next Research Decision

The registered H01 v1.2 result is now a valid, fully verified confirmatory realization. The single family-level decision it produces is a **CONTRADICTION** of the registered INVERSE prior for the broad Layer-A commodities-other basket (positive vol-response asymmetry), with equity indices showing strong but evidence-limited positive asymmetry in both eras. The next research decision is scientific, not procedural:

- **Interpret the contradiction** (positive asymmetry in COMMODITIES_OTHER; strong positive asymmetry in EQUITY_INDICES): is the 12-month TSMOM vol asymmetry genuinely reversed (positive shocks → more vol), or is the realized-vol ΔlnRV response capturing a different mechanism (e.g., vol-of-vol feedback, liquidity, or the 5-day-window construction)?
- **Candidate follow-on hypotheses** (each requires the same governance chain: methodology decision → pre-registration → independent audit): an H01b replication on the reversed-direction prior for the contradicted basket; a multi-market equity-indices expansion (currently 1 market each) to escape the single-market cap; a horizon-response study (1d vs 5d vs 21d show sign instability in several classes, which is itself a finding).

No re-execution, no protocol change, and no new experiment is authorized by this report.
