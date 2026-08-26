# QUANTFORGE — TSMOM V2 DRIFT-CONTROLLED EXPERIMENT — SCIENTIFIC REPORT

**Protocol:** EVENT_STUDY_PROTOCOL_TSMOM_V2_DRIFT_CONTROL.md v2.0.0 (frozen) — executed 2026-08-13T11:20:19.638090Z
**Elapsed:** 45.9 s
**Protocol SHA-256:** `e9aa9465e3ede5ab8b75c0fae7005fda6d312d97b6a6c7ab563f85b60e3c493d` (unchanged during execution)
**Source / inverse fingerprints:** recorded in `experiment_metadata_TSMOM_V2.json` and `results_TSMOM_V2.json`

> **Reconstruction notice:** This report was NOT produced at execution time — the terminal print stage crashed (console encoding) after all computational artifacts were written. It was reconstructed after execution and after the read-only adjudication audit, using ONLY numbers persisted in `results_TSMOM_V2.json`, `experiment_metadata_TSMOM_V2.json`, and the result CSVs. No recomputation, no new inference.

## 1. Scientific Classification
**PARTIALLY REPRODUCED** (historical positive incremental; contemporary direction opposite)

## 2. Economic Classification
- Historical Layer A: **UNRESOLVED by design** (HPD transaction costs unobserved; assumption bands only)
- Contemporary Layer B: **NOT CONFIRMED**

## 3. Research Question
Does the fixed 12-month-lookback / 1-month-skip / 1-month-hold TSMOM signal add incremental predictive value **above a same-universe, same-weight all-long drift benchmark**?

**Scientific object:** `ΔΠ(m) = Π_tsmom(m) − Π_long(m)`, where Π is the monthly portfolio return of the indicated book. Absolute TSMOM return is NOT the tested object.

## 4. Design

| Component | Description |
|---|---|
| Historical Layer A | 28-market validated HPD panel, common window 1987-01-13 → 2002-08-30, 175 position months, 4,900 market-months, 552 pooled flips |
| F1 | TRAIN + VALIDATION, T = 148, L = 12, B = 10,000, seed 20260813 |
| F2 | Historical TEST, T = 27, seed = F1 seed, single authorized use |
| Contemporary Layer B | 5 markets (XAUUSD, EURUSD, BTCUSD, XAGUSD, USATECHIDXUSD), 2021–2026, T = 54, 219 assessments, seed 20260814 |
| Partitions | TRAIN = 122, VALIDATION = 26, TEST = 27 (Layer A). F1 uses TRAIN+VALIDATION; F2 uses TEST the first and only time |
| Inference | Month-vector calendar block bootstrap (dependence-aware; mean cross-market abs correlation ≈ 0.07 tsmom / 0.11 long-running) |

## 5. Primary F1 Result — Incremental ΔΠ (TRAIN+VALIDATION, T = 148)

| Series | Mean/month | 95% CI | one-sided p |
|---|---|---|---|
| ΔΠ = Π_tsmom − Π_long | **+0.006726** (+0.67%) | [+0.000313, +0.015374] (+0.03%, +1.54%) | 0.0191 |
| Π_tsmom (absolute) | +0.013859 (+1.39%) | — | — |
| Π_long (drift benchmark) | +0.007133 (+0.71%) | — | — |

- Long exposure (F1): ≈ **53.0%** — drift is a material component of absolute TSMOM return.
- Hit rate (ΔΠ bootstrap): 55.4%.
- **Holm-adjusted p ≈ 0.038** (family {F1, Layer B}, α = 0.05) → F1 passes the multiple-comparison gate.

### Breadth
- 21/28 markets positive by mean incremental return (F1 months).
- All 28 leave-one-market-out values positive.
- All 9 leave-one-class-out values positive (FX 0.0040, Metals 0.0064, Grains 0.0071, Softs 0.0076, Livestock 0.0061, Energy 0.0068, Rates 0.0084, Equity index 0.0072, Index 0.0064).
- Only class means negative: Rates (−0.0145), Equity index (−0.0073).

## 6. Protected F2 Result — Historical TEST (T = 27, single use)

- ΔΠ mean ≈ **+0.003376** (+0.34%/month), positive direction, 95% CI [−0.005228, +0.019409] (includes zero), one-sided p ≈ 0.1203.
- Hit rate 48.1%.
- **Corroborative only.** Consumed exactly once; never re-used; no methodology changed after results.

## 7. Contemporary Layer B — Incremental ΔΠ (T = 54, 2021–2026)

| Series | Mean/month | 95% CI | one-sided p |
|---|---|---|---|
| ΔΠ = Π_tsmom − Π_long | **−0.011035** (−1.10%) | [−0.057016, +0.000893] (−5.70%, +0.09%) | 0.9709 |
| ΔΠ net of observed MT5 costs | −0.011140 (−1.11%) | [−0.057225, +0.000848] | 0.9716 |
| Π_tsmom (absolute) | +0.019167 (+1.92%) | [−0.019192, +0.052186] | 0.1512 |
| Π_long (drift benchmark) | +0.030202 (+3.02%) | [+0.018735, +0.062203] | 0.0012 |

- 219 assessments, 43 blocks, pooled flips = 19 (5-market pool).
- **Direction is OPPOSITE the historical Layer A.** The all-long drift book has a strongly positive, CI-excluding-zero mean (+3.02%/month); TSMOM fails to beat it and the incremental signal is negative.

## 8. Negative Controls (all clean)

| Control | B | Null mean | fraction-null-≥-observed |
|---|---|---|---|
| NC1 — paired direction rotation | 10,000 | −0.004772 | **0.0001** |
| NC3 — 24-month lag shift (T=151) | 10,000 | −0.006650 (median) | p ≈ 0.9462, effect negative |
| NC4 — calendar-block null | 10,000 | −0.003387 | **0.0373** |

None of the negative controls reproduces the F1 positive incremental result, consistent with signal-specificity of the historical effect near its construction horizon.

## 9. Promotion Gate (frozen §19, all 8 conditions)

| # | Condition | Result |
|---|---|---|
| 1 | F1 mean ΔΠ > 0 | PASS (+0.67%) |
| 2 | F1 95% CI lower bound > 0 | PASS (+0.03%) |
| 3 | Holm-adjusted p < 0.05 (family {F1, Layer B}) | PASS (0.038) |
| 4 | Positive vs all-long benchmark | PASS |
| 5 | Not single-market driven | PASS (21/28) |
| 6 | Not single-class driven | PASS (all LOCO positive) |
| 7 | Survives negative controls | PASS (NC1/NC3/NC4 clean) |
| 8 | **Contemporary directional consistency** | **FAIL** (historical +0.67% vs contemporary −1.10%) |

**Decision: NOT PROMOTABLE — RESEARCH REMAINS UNRESOLVED. Scientific classification: PARTIALLY REPRODUCED. Line CLOSED (DISC-022).**

## 10. Economics

- **Historical Layer A:** HPD transaction costs are **UNOBSERVED**; no fabricated spreads. Sensitivity bands {0, 5, 10, 20, 50} bp labelled **ASSUMPTION**; F1 net ΔΠ stays positive at 50 bp (persisted value ≈ +0.00111/month, F1 unit). Historical economics **UNRESOLVED by design**.
- **Contemporary Layer B:** Observed MT5 half-spreads (Option-A accounting); EURUSD assumed-cost sensitivity ≈ −0.0177/month across {0.1, 0.5, 1.0, 2.0} bp bands (persisted `cost_analysis_TSMOM_V2.csv`); net-layer CI lower bound < 0 → **NOT CONFIRMED**.
- **Economics are NOT the primary closure reason.** The decisive problem is the **absence of a stable incremental signal across eras** (Condition 8).

## 11. Relationship to TSMOM V1 (5-market contemporary panel)

V1 (2026-08-12, 219 contemporary assessments) was Scientific **INCONCLUSIVE** / Economic **NOT CONFIRMED**: F1 absolute-return CI included zero and the formal NC2 (time-shifted signal) produced a *stronger* association (mean ≈ +3.93%/month, CI excluding zero), so the positive point estimates could not be separated from unconditional drift. V2 replaced the contaminated control with a same-universe all-long drift benchmark and three clean pre-registered negative controls, resolving the V1 attribution problem. **V1 remains a historical record (INCONCLUSIVE); V2 supersedes its inference.**

## 12. Scope / Boundary

- This closes the **fixed 12/1 TSMOM operationalization within QuantForge** only. It does NOT claim that trend following or momentum in general does not work; the external AQR/MOP and HOP literature remains historical context (see DISC-022 §future-importance).
- No TSMOM V3, no lookback/horizon/weighting/market-selection search, no regime filtering, no TEST reuse, no detector, no runtime promotion. TEST consumed exactly once.

## 13. Artifacts

Source inventory (all under `output/tsmom_v2/`): `EVENT_STUDY_PROTOCOL_TSMOM_V2_DRIFT_CONTROL.md`, `run_tsmom_v2.py`, `experiment_metadata_TSMOM_V2.json`, `assessment_events_TSMOM_V2.csv` (5,119 rows), `incremental_monthly_TSMOM_V2.csv` (229 rows), `bootstrap_TSMOM_V2.csv` (60,000 rows), `negative_controls_TSMOM_V2.csv`, `cost_analysis_TSMOM_V2.csv`, `results_TSMOM_V2.json`, `.build_cache/`. Historical corpus files (`HPD_MANIFEST.csv`, `HPD_CONTRACT_HASHES.csv`, `FINAL_CLASSIFICATION.csv`, `PER_MARKET_VALIDATION.csv`) are referenced under `data/`.

## 14. Integrity

- Protocol SHA-256 unchanged during execution (`e9aa9465…c493d`).
- Monthly accounting identity `ΔΠ ≡ Π_tsmom − Π_long` verified to 1e-9 on all 229 rows by the read-only audit.
- Bootstrap/events/controls CSVs cross-verified against `results_TSMOM_V2.json`.
- TEST consumed exactly once; no rerun; no methodology changed after results.
- Computation state complete; reporting state reconstructed after the audit from persisted numbers.