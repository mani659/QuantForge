# QUANTFORGE — H01 EQUITY VOLATILITY-ASYMMETRY V1 SCIENTIFIC REPORT

**Protocol:** `H01_EQUITY_VOLATILITY_ASYMMETRY_PROTOCOL_V1.md` v1.1.0 (FROZEN)
**Protocol SHA-256:** `a97cd0e27394cb83cce1a37e5369a182aad407a11e450b9385d30f9390f0d6ab`
**Clearance:** PASS — APPROVED FOR EXECUTION (final independent H01 Equity V1.1 execution-clearance audit)
**Execution:** single invocation, serial (1 worker), below-normal OS priority; seed `20260816`; B = 10,000; L = 11; no checkpoint/resume; no concurrent runs.
**Duration:** 1,296.7 s; peak RSS 78.2 MB; no resource-pressure events.
**Artifact set:** this report, `experiment_metadata_H01_EQ_V1.json`, `results_H01_EQ_V1.json`, `class_stats_H01_EQ_V1.csv`, `per_market_stats_H01_EQ_V1.csv`, `matched_pairs_H01_EQ_V1.csv`, `bootstrap_replicates_H01_EQ_V1.csv` (40,000 draws = 4 cells × 10,000 × 2), `daily_series/`, `run_h01_equity_v1.py`, `run_h01_equity_v1.log`.

---

## 1. Execution Identity

- Experiment: **H01 EQUITY VOLATILITY-ASYMMETRY V1** (Track A, US-anchored multi-market equity replication of the classic volatility-response asymmetry).
- Protocol version 1.1.0; frozen scientific object, universe, matching, strata, bootstrap, null-inference, Holm family, and decision rules per the definition lock and pre-registration.
- Inputs: the **frozen 2026-08-16 snapshot** — HPD `front_sp.csv` + four FRED fredgraph files — every SHA-256 verified against protocol §7 before computation (GATE 1 PASS).
- All data-quality gates passed (fingerprints; universe; date-range; duplicate/validity; missingness; `sp` roll consistency = 82 vs `PER_MARKET_VALIDATION.csv`; RV construction; leakage-free windows; determinism; licensing record carried into metadata).

## 2. Dataset Integrity

| Market | Era | Window | Daily rows | Eligible shocks | Matched pairs (3 strata) | Evaluable |
|---|---|---|---|---|---|---|
| `sp` (S&P 500 futures, HPD) | HISTORICAL | 1982-04-21 → 2002-10-01 | 5,163 | 4,894 | 651/642/663 (1,956) | yes |
| SP500 (FRED cash) | CONTEMPORARY | 2016-08-15 → 2026-08-14 | 2,610 | 2,482 | 359/356/365 (1,080) | yes |
| DJIA (FRED cash) | CONTEMPORARY | 2016-08-15 → 2026-08-14 | 2,610 | 2,474 | 374/370/351 (1,095) | yes |
| NASDAQ100 (FRED cash) | HISTORICAL | 1986-01-02 → 2002-10-01 | 4,221 | 3,976 | 631/599/615 (1,845) | yes |
| NASDAQCOM (FRED cash) | HISTORICAL | 1982-04-21 → 2002-10-01 | 5,147 | 4,898 | 726/697/740 (2,163) | yes |
| NASDAQ100 (FRED cash) | CONTEMPORARY | 2016-08-15 → 2026-08-14 | 2,593 | 2,463 | 347/341/356 (1,044) | yes |
| NASDAQCOM (FRED cash) | CONTEMPORARY | 2016-08-15 → 2026-08-14 | 2,604 | 2,465 | 336/338/367 (1,041) | yes |

- FRED holiday placeholders in the frozen snapshot are empty value fields; counts (96/96/362/487) match the registered protocol §8.1 numbers exactly; dropped as missing days, never imputed.
- Every market is primary-evaluable (≥ 30 matched pairs in all three strata). All markets' terciles/calipers/`c_(m,s)` are frozen constants computed once on the original data.
- **Machinery identity cross-check:** `sp` d_m = +0.14978 reproduces the frozen H01 v1.2 `sp` value (+0.150) and the §21.9 MT5 reference USATECHIDXUSD d_m = +0.42196 reproduces the frozen v1.2 +0.422 — the shared statistical machinery is byte-consistent with the validated H01 v1.2 pipeline.

## 3. Primary Class Statistics (observed results)

`D_cell = ΔlnRV(negative shock) − ΔlnRV(positive shock)`, magnitude-matched, vol-state-conditioned, equal market weights.

| Cell | Exposure | Era | Evaluable markets | D_cell | d_m by market |
|---|---|---|---|---|---|
| EQBROAD_L1 | Broad US | HISTORICAL | `sp` (1) | **+0.1498** | sp +0.1498 |
| EQBROAD_L2 | Broad US | CONTEMPORARY | SP500, DJIA (2) | **+0.3160** | SP500 +0.3647, DJIA +0.2672 |
| EQTECH_L1 | US tech | HISTORICAL | NDX, NCOMP (2) | **+0.2083** | NDX +0.1840, NCOMP +0.2325 |
| EQTECH_L2 | US tech | CONTEMPORARY | NDX, NCOMP (2) | **+0.3297** | NDX +0.3519, NCOMP +0.3074 |

All 7 primary market-level statistics are positive (classic direction). Directional consistency within every cell = 1.0 (all evaluable markets agree with the cell sign).

## 4. Sampling CIs (percentile, ordinary sampling draws)

| Cell | CI 95% |
|---|---|
| EQBROAD_L1 | [0.0787, 0.1929] |
| EQBROAD_L2 | [0.2340, 0.3889] |
| EQTECH_L1 | [0.1541, 0.2643] |
| EQTECH_L2 | [0.2359, 0.3922] |

All four CIs lie entirely above zero.

## 5. Null-Test p-values (corrected null construction, `(1+count)/(B+1)`, inclusive `≥`)

All 10,000 null draws per cell were finite; **count = 0 in every cell** (no null draw reached |D_obs|).

| Cell | count | p_raw | p_Holm (4-cell family) |
|---|---|---|---|
| EQBROAD_L1 | 0 / 10,000 | 0.000100 (= 1/10001) | 0.000400 |
| EQBROAD_L2 | 0 / 10,000 | 0.000100 | 0.000400 |
| EQTECH_L1 | 0 / 10,000 | 0.000100 | 0.000400 |
| EQTECH_L2 | 0 / 10,000 | 0.000100 | 0.000400 |

Independent post-execution recomputation of p-values, CIs, Holm, and D_obs from the persisted draws and tables reproduces every value exactly. The retired v1.1 D_obs-centered p-value is not used anywhere.

## 6. Holm-Adjusted Results

Family-wise α = 0.05, two-sided, Holm step-down over exactly the four registered cells. Every cell p_Holm = 0.0004 < 0.05 → family-level significant in the classic direction.

## 7. Historical vs Contemporary Interpretation

- **EQTECH (US-tech exposure):** SUPPORT in both eras (L1 D=+0.2083, L2 D=+0.3297, both p_Holm=0.0004, both markets agreeing in each era) → the registered **strong cross-era replication** condition is met (EQTECH strong replication = **TRUE**). The same exposure, same index family, two independent eras ~30 years apart, replicate the classic asymmetry at family-level significance.
- **EQBROAD (broad-US exposure):** the contemporary layer (SP500, DJIA) is **SUPPORT**. The historical layer (EQBROAD_L1) contains a single market (`sp`), so by the registered ≥2-evaluable-market rule it is **EVIDENCE-LIMITED/DESCRIPTIVE** — it reports D=+0.1498 with p_Holm=0.0004 and a CI above zero, but receives **no primary verdict** and cannot anchor a strong cross-era claim. The cross-era EQBROAD comparison is descriptive only (registered §20), never "strong replication." Historical broad-US generalization therefore rests on the descriptive `sp` observation plus the contemporary two-market SUPPORT.

## 8. Scientific Classification (registered rules, protocol §23)

| Cell | Verdict |
|---|---|
| EQBROAD_L1 | **EVIDENCE-LIMITED/DESCRIPTIVE** (single evaluable market, by construction) |
| EQBROAD_L2 | **SUPPORT** |
| EQTECH_L1 | **SUPPORT** |
| EQTECH_L2 | **SUPPORT** |

- No cell produced a CONTRADICTION or INCONCLUSIVE primary verdict.
- **Strong replication:** EQTECH across eras — YES. EQBROAD across eras — not claimable (historical leg evidence-limited).
- **Scope boundary:** this establishes that the classic asymmetry **generalizes across US equity-index markets** (two distinct exposures — broad large-cap and Nasdaq family — and two eras for the tech exposure), **not** "equity markets generally" and **not** an international claim. The universal/broad H01 formulation remains closed and is not revived by this result.
- Generalization claim rests on exposure-level evidence (2 exposures, up to 2 eras, 7 market-level observations all classic-direction), not on market count.

## 9. Secondary Analyses (pre-declared; NON-RESCUING; cannot alter any primary verdict)

- **21.1 1-day horizon** (cell D): EQBROAD_L1 +0.380, EQBROAD_L2 +0.349, EQTECH_L1 +0.334, EQTECH_L2 +0.389 — classic direction at the 1-day horizon, stronger than 5-day.
- **21.2 21-day horizon**: EQBROAD_L1 **−0.067** (descriptive negative), EQBROAD_L2 +0.155, EQTECH_L1 +0.117, EQTECH_L2 +0.101 — the effect is not monotone across horizons; historical `sp` shows a negative 21-day descriptive value. Sensitivity only.
- **21.3 standardized-shock matching**: all cells positive (+0.155 / +0.310 / +0.235 / +0.303).
- **21.4 absolute-return response**: all cells positive but tiny (+0.0007 … +0.0013).
- **21.5 winsorization sensitivity** (95th-pct cap): all cells positive (+0.155 / +0.318 / +0.209 / +0.331), essentially unchanged from the primary.
- **21.6/21.7 GJR(1,1)/EGARCH(1,1) γ diagnostics**: GJR γ slightly negative for the long-history series and at the −0.30 bound for the short contemporary series; EGARCH γ at the +0.30 bound for most series. Per the protocol's mandatory statement, *"A GJR/EGARCH coefficient does not replace the primary empirical response statistic and cannot rescue a failed primary result"* — known boundary/clamp behavior in this environment means GJR/EGARCH output is **non-confirmatory** and its signs are **not scientific evidence**. Engle–Ng sign/size-bias t-statistics are recorded in `results_H01_EQ_V1.json`.
- **21.8 common-window sensitivity** (1986-01-02 → 2002-10-01): EQBROAD_L1 +0.177, EQTECH_L1 +0.213 (sp +0.177, NDX +0.184, NCOMP +0.243) — the historical layer result is robust to the common exposure window.
- **21.9 MT5 cross-provider reference**: USATECHIDXUSD d_m = +0.422 (reproduces the frozen v1.2 observation). Descriptive cross-provider, different-instrument reference only; never a primary market.
- **21.10 cross-source futures/cash context**: documentary (acquisition report §6/§10: futures/cash corr ≈ 0.95, median ≈ 16 bp, 1987/1982 genuine divergences) — interpretation context for EQBROAD_L1 only; not recomputed in-experiment from restricted sources.

## 10. Limitations

1. **Futures vs cash (registered Option A):** historical broad-US is measured on S&P 500 futures; contemporary on cash indices — a registered source-type difference, an interpretation limitation, never adjusted away.
2. **Exposure structure:** NASDAQ100 ⊂ NASDAQCOM is one tech exposure; SP500/DJIA is one broad-US exposure. Exposure count (2), not market count (7), is the carrier of the generalization claim.
3. **EQBROAD_L1 evidence-limited:** the historical broad-US leg is a single market; it can describe but not confirm.
4. **US-anchored scope:** no international generalization is claimed; the scope decision explicitly withholds international breadth.
5. **Era gap 2002–2016** is structurally excluded (no validated broad-US cash series); the two eras do not form a continuous record.
6. **Inference caveats (registered):** block-bootstrap consistency assumed; greedy nearest-neighbour caliper matching rebuilt in replicates carries Abadie–Imbens-style caveats; the estimator/bootstrap combination has no dedicated published theorem.
7. **Licensing:** HPD PENDING; FRED platform CLEAR with attribution, underlying index archival rights PENDING; permission requests PREPARED, NOT SENT — carried into execution metadata; a governance constraint, not a scientific one.
8. **Secondary 21.2:** the 21-day historical `sp` value is descriptively negative; this is a non-rescuing sensitivity and does not alter the frozen 5-day primary.

## 11. Reproducibility

- Protocol SHA-256, all input fingerprints, Python/NumPy/SciPy versions, seed, B, L, era windows, worker count, resource mode, timestamps, duration, and peak memory recorded in `experiment_metadata_H01_EQ_V1.json`.
- Post-execution verification: p-values, percentile CIs, Holm adjustment, D_obs, and verdict labels recomputed independently from the persisted CSV artifacts — all exact matches (0 differences to 1e-12).
- Stream integrity: single serial invocation; fixed cell order (EQBROAD_L1, EQBROAD_L2, EQTECH_L1, EQTECH_L2) × replicate index; 10,000 replicates per cell with no duplicate IDs; sampling and null draws generated from the same master stream; results cannot depend on worker completion order (no workers).
- Re-execution of the frozen snapshot with the same seed reproduces the identical stream by construction.

## 12. V1.1 Invalid-Result Firewall

> **H01 v1.1 remains CONFIRMATORY INFERENCE INVALID / SCIENTIFIC RESULT UNADJUDICATED.**

No v1.1 p-value is used or mixed with this result set. This H01 Equity V1 result is a new, independently pre-registered and audited experiment on a separate universe; it does not rescue, revise, or merge with the H01 v1.1/v1.2 commodity/currency class results.

## 13. Exact Next Research Decision

The US-anchored generalization question is answered in the affirmative under the registered rules:

> The classic negative-shock volatility-response asymmetry **generalizes across US equity-index markets** — two distinct exposures, with the tech exposure replicated across two eras at family-level significance, and the broad-US exposure supported contemporarily with a descriptive historical confirmation. International generalization and the broad universal claim are **not** established and remain closed by scope.

Next legitimate step (governance gate, not executed here): an **H01 Equity V1 adjudication/interpretation task** — independent, read-only review of this result set and its classification — before any further Track-A scientific decision (e.g., whether the evidence-limit on EQBROAD_L1 justifies a data-acquisition path for a second historical broad-US series). No runtime, strategy, BOE, or Assembly connection is implied or authorized by this result.

## 14. Integrity

The experiment was executed exactly once under protocol v1.1.0 with the registered frozen snapshot, seed 20260816, B = 10,000, L = 11, single invocation, serial resource-conservative execution (below-normal priority, peak RSS 78 MB, no resource-pressure events). All registered gates passed; no parameter, universe, matching, strata, bootstrap, null, family, or decision rule was changed; no secondary analysis altered any primary verdict; no result was inspected and rerun; BOE/Assembly/Deployment and all governance records were untouched. This report distinguishes observed results from statistical inference and from registered classification; it neither strengthens nor weakens the numbers.
