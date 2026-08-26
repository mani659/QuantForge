# QuantForge — Canonical Mean-Reversion Event Study V2 — Scientific Report

**Protocol:** V2.0.0 (pre-registered, `EVENT_STUDY_PROTOCOL_V2.md`) · **Date:** 2026-08-12 · **Area:** `output/event_study_v2/`
**Data:** `data/m1/` (5 markets, M1) · **Event dataset:** `event_dataset_V2.csv` (83,307 rows; SHA-256 in `experiment_metadata_V2.json`)

---

## 1. Executive Verdict

**GATE 1 PARTIALLY PASSED — NOT PROMOTABLE.**

V2 answers its narrow question precisely: the V1 negative result was **not** purely an artifact of the V1 operationalization. For four of five markets (XAUUSD, EURUSD, BTCUSD, USATECHIDXUSD) the negative is **robust across all three pre-registered normalizations** — no normalization produces a reversion effect. For **XAGUSD**, a coherent signal survives: the down-displacement reversion effect appears under N1 and N2, is positive in TRAIN / VALIDATION / TEST, in all four walk-forward folds, all three chronological thirds, all three volatility regimes, and is the single test in the 27-member confirmatory family that survives Holm correction (N1_XAGUSD, p_holm = 0.0135). At equal rarity (matched quantiles), XAGUSD is significant in **both** directions under N1 and N2.

But the effect is **not a specification**: it is single-market with no mechanistic justification established, economically marginal (≈ 4–11 bp over 2 h), weak on multiplicity (1/27), dependent on normalization (N3 shows it only marginally at matched quantiles), loses narrow-CI significance on the TEST hold-out, and the bootstrap/permutation intervals are compromised by pervasive cross-direction overlap (up to 5.7M overlapping event pairs per market). The persistence study (Issue C) is **mechanically confounded by design** and must be re-designed (entry-at-confirmation) before it can answer anything.

Per the pre-registered stopping rules: not FAILED (real, reproducible candidate evidence exists for XAGUSD), not PASSED (multiplicity, market-specificity, economic magnitude, and design defects all stand). **GATE 1 remains not promotable; no engineering may begin.**

---

## 2. V1 → V2 Rationale

V1 (single operationalization: rolling price z-score, Z=3.0, W=120, H=120) failed GATE 1: 2/30 cells distinguishable, no OOS reversion, no stable threshold region, no cross-market portability. V2 tested whether that failure was operationalization-specific by adding two alternative normalizations (ATR-relative, return-based standardized), regime-resolved and walk-forward analysis, a pre-registered persistence criterion, and Holm multiple-comparison control over a 27-test confirmatory family.

**Result:** the V1 failure was *partly* operationalization-specific — but only for XAGUSD, and the XAGUSD signal was already visible in V1 (XAGUSD DOWN VALIDATION was one of V1's two distinguishable cells). For the other four markets, the negative is operationalization-robust.

## 3. Pre-Registered V2 Protocol

Fully specified in `EVENT_STUDY_PROTOCOL_V2.md` before any outcome inspection: three normalizations with formulas; primary threshold ±3.0 for all; TRAIN-only sensitivity grid {2.5, 3.0, 3.5}; matched-quantile (0.5%) comparability check; S=240 separation; H=120; partitions 0.70/0.85; persistence criterion retention_60 ≥ 0.6; volatility terciles from TRAIN; chronological thirds; four walk-forward folds (D = V1 VALIDATION window); permutation p-values (B=2000, seeded); Holm at α=0.05 over 27 pre-registered confirmatory tests; stopping rules; TEST as single pre-authorized hold-out interpreted only as follow-up of Holm survivors.

## 4. Dataset / Data Quality

Identical to V1 (fingerprints re-recorded): 5 markets, M1, 0 duplicate timestamps, 0 missing OHLCV, gaps up to ~4 days, **volume unusable in 4/5 markets (100% zero rows)** — no V2 methodology uses volume. Row counts 906,815–2,539,807. Manifest: `data_manifest_V2.csv`.

## 5. Normalization Comparison

At the pre-registered primary threshold ±3.0 (VALIDATION, direction-adjusted pooled):

| Normalization | Events (5 mkt) | Pooled effect | Holm survival |
|---|---|---|---|
| N1 (rolling z) | 3,901 | +0.00014 (p=0.38) | none pooled; **N1_XAGUSD survives** (+0.00059, p_holm=0.0135) |
| N2 (ATR-relative) | 8,231 | −0.00001 (p=0.31) | none (N2_XAGUSD p=0.063 — fails) |
| N3 (return-based) | 131 | −0.00045 (p=0.19) | none — too few events at ±3.0 |

**Critical comparability caveat:** at the equal raw threshold ±3.0, N3 produces ~30× fewer events than N1/N2 (a standardized 120-bar *cumulative* return of 3σ is far rarer than a 3σ deviation from the rolling mean). The raw-threshold comparison is therefore not rarity-matched; the matched-quantile comparison is the valid equal-rarity view:

**Matched quantiles (0.5% tails, TRAIN-derived thresholds, VALIDATION)** — cells with CI excluding zero:

| Cell | Effect | CI |
|---|---|---|
| N1 XAGUSD DOWN | +0.00131 | [0.00077, 0.00185] |
| N1 XAGUSD UP | −0.00101 | [−0.00191, −0.00021] |
| N2 XAGUSD DOWN | +0.00242 | [0.00144, 0.00345] |
| N2 XAGUSD UP | −0.00282 | [−0.00467, −0.00113] |
| N3 XAGUSD DOWN | +0.00100 | [−0.00004, 0.00207] (marginal) |

**XAGUSD is significant in BOTH directions under N1 and N2 at equal rarity — the strongest evidence in the study.** No other market has any cell with CI excluding zero.

**Conclusion (A):** normalization does not rescue four markets; XAGUSD's signal is present under all three normalizations at equal rarity (strongest N1/N2).

## 6. Regime Analysis

**XAGUSD N1 (VALIDATION) by volatility regime:** HIGH +0.00035, MID +0.00068, LOW +0.00038 — positive in all three. **N2:** +0.00029 / +0.00024 / +0.00015 — positive in all three. Other markets show no consistent regime structure (BTCUSD HIGH negative, MID positive — non-monotone; XAUUSD flat).

## 7. Walk-Forward Analysis

**XAGUSD N1 pooled dir-adj per fold:** A +0.00010, B +0.00053, C +0.00045, D(=V1 VALIDATION) +0.00048 — positive in all 4 folds, strengthening over time. **N2:** +0.00018 / +0.00012 / +0.00030 / +0.00020 — positive in all 4. BTCUSD N1: +0.00042 / +0.00041 / −0.00014 / +0.00004 — fades; XAUUSD mixed; EURUSD ~0. XAGUSD is the only market positive in every fold under both N1 and N2.

**Chronological thirds (XAGUSD N1):** +0.00022 / +0.00042 / +0.00023 — positive in all three calendar periods (N2 likewise). Stability is not a single-period artifact.

## 8. Persistence Analysis

**UNRESOLVED — the pre-registered design is mechanically confounded.**

The criterion `retention_60 ≥ 0.6` uses bars **t+1..t+60** — inside the measured outcome window **t+1..t+120**. P-pass vs P-fail therefore splits events on first-hour behavior, and the differences are the persistence of that first-hour drift, not an event-time discrimination signal. Decisive diagnostics:

1. Mirror-image P-pass/P-fail differences appear in **every** market with comparable magnitude (EURUSD +0.00130, XAUUSD +0.00288, BTCUSD +0.00754, XAGUSD +0.00587, USATECH +0.00324) — including EURUSD/XAUUSD with ~zero overall reversion effect. A genuine persistence criterion tied to the reversion phenomenon would not behave identically in markets with no reversion.
2. The share of P-pass events with positive 120-bar outcome is uniformly 74–77% in every market.

Pooled confirmatory persistence tests fail Holm anyway: N1 p=0.169, N2 p=0.015 → p_holm=0.39, N3 p=0.189. A usable persistence criterion must be tested with an **entry-at-confirmation** design: the filter decided at t+60 using only t+1..t+60, and the outcome measured from t+60 onward. This is the required V3 design change.

## 9. Directionality

Hypothesized signs fixed (DOWN → positive dir-adj, UP → negative dir-adj; never flipped). **XAGUSD is directionally consistent in the hypothesized direction**: DOWN positive (TRAIN/VALIDATION/TEST) and UP negative at matched quantiles. Every other market shows either flat (EURUSD, USATECH), inconsistent (BTCUSD), or single-cell anti-reversion anomalies (XAUUSD UP TEST raw +0.00064 — the same cell V1 flagged, i.e., upward displacement followed by continued upward movement). Directional symmetry is not established anywhere; XAGUSD asymmetry is the only stable pattern.

## 10. Cross-Market Portability

**Not portable.** XAGUSD is the sole market with any Holm-surviving or matched-quantile-significant cell. The protocol permits "a clearly justified market-specific boundary" in lieu of portability — V2 provides the *empirical* case (silver-specific) but **no mechanistic justification** (volume/spread proxies unavailable in the data; 100% zero-volume rows). The boundary claim requires V3 evidence; it is not established by this study.

## 11. Statistical / Multiplicity Control

- Confirmatory family: 27 pre-registered tests, Holm-corrected at α=0.05. **1/27 survives (N1_XAGUSD, p_holm=0.0135).**
- TEST hold-out (pre-authorized, interpreted only as follow-up): XAGUSD N1 DOWN +0.00101 (n=484, CI [−0.00043, 0.00240] — sign consistent with TRAIN/VALIDATION, interval wide); N2 DOWN +0.00015 (CI includes 0). **Direction holds; narrow-CI significance does not.**
- **Dependence limitation (pre-registered, now quantified):** cross-direction overlap is pervasive — 0.6M–5.7M event pairs within 2 h per market-normalization; every event effectively has cross-direction neighbors. Event-level bootstrap/permutation intervals may understate uncertainty; the intervals reported here should be read as optimistic.

## 12. Economic Significance

XAGUSD mean direction-adjusted effects: N1 DOWN ≈ +4 bp (TRAIN) to +11 bp (VALIDATION); matched-quantile ≈ +10 to +24 bp (N2). Against the stated interpretation threshold (≈5–10 bp over 2 h, negligible relative to realistic costs), the effect is **marginal at best** and does not meet a practical-economic bar even where statistically distinguishable. No cost model was applied (no spread data available).

## 13. Negative Findings

1. Four of five markets: **no reversion effect under any of three normalizations** — V1's negative is robust.
2. N3 at primary threshold: too few events (131) for inference; only the matched-quantile view is informative.
3. No cross-market portability; no mechanistic market-specificity evidence.
4. Persistence criterion: confounded by design; no usable event-time discrimination established.
5. XAGUSD TEST hold-out: direction holds, narrow-CI significance does not.
6. Economic magnitudes marginal everywhere.

## 14. Reproducibility

`experiment_metadata_V2.json`: protocol V2.0.0, normalization formulas, seeds (20260813), all parameters (W=120, thresholds, S=240, H=120, PERSIST_H/Q, partitions, folds), source SHA-256 fingerprints, pandas 3.0.2 / numpy 2.4.4, event-dataset rows 83,307 and SHA-256. Scripts: `run_event_study_v2.py`. Deterministic. No hidden filtering.

## 15. Scientific Specification Matrix

| Semantic | V1 Status | V2 Result | Evidence Strength | Production Ready? |
|---|---|---|---|---|
| Event definition | UNESTABLISHED | PARTIALLY ESTABLISHED (XAGUSD only) | reproducible, market-specific | NO |
| Trigger | UNESTABLISHED | UNESTABLISHED | no robust region | NO |
| Normalization | (single: N1) | PARTIALLY ESTABLISHED (N1/N2 agree; N3 weak) | moderate | NO |
| Threshold | UNESTABLISHED | UNESTABLISHED | monotone XAGUSD N1 (2.5→3.5), flat N2; no plateau | NO |
| Direction | UNESTABLISHED | PARTIALLY ESTABLISHED (XAGUSD asym.) | moderate | NO |
| Recoil | UNESTABLISHED | UNESTABLISHED (not re-tested in V2) | — | NO |
| Persistence | PARTIALLY ESTABLISHED (descriptive) | **CONTRADICTED as usable criterion** (confounded design) | mechanical | NO |
| MAE / MFE | ESTABLISHED (research-local) | ESTABLISHED (unchanged) | strong | n/a (research defs) |
| Event boundaries | PARTIALLY ESTABLISHED | PARTIALLY ESTABLISHED | moderate | NO |
| Regime dependence | UNESTABLISHED | PARTIALLY ESTABLISHED (XAGUSD regime-stable) | moderate | NO |
| Cross-market portability | UNESTABLISHED | **CONTRADICTED** (absent) | — | NO |
| Parameter schema | UNESTABLISHED | UNESTABLISHED | — | NO |

## 16. Exact Remaining Scientific Gaps

1. XAGUSD market-specificity: mechanistic justification or rejection (spread/session/microstructure proxies; the data lacks volume for 4/5 markets).
2. Cross-direction-dependence-aware inference (paired/block bootstrap or non-overlapping-episode restriction) — current intervals are optimistic.
3. Persistence as a usable criterion via entry-at-confirmation design (outcome from t+60).
4. Economic viability: cost-aware magnitude assessment for XAGUSD M1.
5. Threshold-region confirmation for XAGUSD N1/N2 on a V3 pre-registered confirmatory pass (family restricted to XAGUSD to control multiplicity).
6. TEST significance: the current hold-out is directionally consistent but not narrow-CI significant.

## 17. Promotion Decision

**GATE 1 PARTIALLY PASSED — NOT PROMOTABLE. Engineering must not begin.** The XAGUSD signal is a legitimate, reproducible research lead — the strongest evidence the project has produced — but it does not meet the pre-registered GATE 1 bar (multiplicity, market-specificity justification, economic magnitude, persistence design, TEST confirmation all fail or remain open). The state remains DESIGN BLOCKED at the specification level.

## 18. Exact Next Research Task

**Pre-registered Event Study V3 — XAGUSD confirmatory focus** (research only, no implementation):
1. Restrict the family to XAGUSD (N1, N2, matched quantiles, both directions) with Holm control; add TEST as a second pre-registered confirmatory layer.
2. Cross-direction-aware inference (block bootstrap by non-overlapping episode; report effective independent events).
3. Entry-at-confirmation persistence design (filter at t+60, outcome t+60→t+120).
4. Cost-aware economic assessment using an estimated XAGUSD M1 spread band.
5. Mechanistic hypothesis tests for market-specificity (session structure, volatility clustering, ATR-scaled magnitude) — or explicit acceptance of an empirical-only market-specific boundary.

---

*Research artifact. No production semantics are established by this document. V1 remains a valid, unmodified scientific result (`output/event_study_v1/`).*
