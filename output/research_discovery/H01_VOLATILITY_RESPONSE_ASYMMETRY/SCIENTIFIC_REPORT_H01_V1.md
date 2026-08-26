# QUANTFORGE — H01 VOLATILITY RESPONSE ASYMMETRY V1 — SCIENTIFIC REPORT

**Protocol:** `H01_VOLATILITY_RESPONSE_ASYMMETRY_PROTOCOL_V1.md` **v1.1.0** (frozen; SHA-256 `c8192e1c35d4a077a1df39b494b50f80e956aac2f5874b86362655f7b01b056d`), unchanged during execution.
**Independent approval:** `H01_V1.1_REAUDIT_REPORT.md` — **PASS — APPROVED FOR EXECUTION**.
**Execution:** `run_h01_v1.py`; completed 2026-08-15 (last run elapsed 537 s; full checkpointed run spanned several invocations, see §12).
**Environment:** Python 3.11.9 (MSC v.1938, AMD64); NumPy 2.4.4; pandas 3.0.2; SciPy 1.17.1. Master seed `20260813`; `L = 11`; `B = 10,000`; family of 11, Holm α = 0.05.
**Executive verdict: INCONCLUSIVE.** No class reproduces a reliable literature-prior asymmetry; no class shows reliable asymmetry in either direction under the registered inference.

---

## 1. Scientific Question (frozen)

> For each market, the forward change in realized variance following a negative daily return shock differs from that following a positive daily return shock of equal absolute magnitude, after conditioning on the pre-shock realized-variance state; expected direction is asset-class specific (Black 1976; Christie 1982; Nelson 1991; GJR 1993; Engle–Ng 1993; Aït-Sahalia–Fan–Li 2013; Baur 2012; and the other §24 references).

Null per class: the vol-state-conditioned, magnitude-matched difference in forward Δln RV between negative and positive shocks is zero. This is an association claim only (definition-lock §10); it is not return prediction, vol timing, or a trading rule.

## 2. Design executed (frozen parameters)

- **Shock:** daily close-to-close log return `r_t`; zero-return days excluded and counted.
- **Response:** `ΔlnRV = ln(RV_{t+1..t+5}) − ln(RV_{t−5..t−1})`, `RV = Σ r²` over the window (5-day primary horizon; shock day excluded from both windows).
- **Confound control:** within-market terciles of `ln(RV_back)` over the market's full eligible series (frozen bounds; not re-estimated inside the bootstrap).
- **Matching:** within (market, stratum), nearest-neighbour one-to-one caliper matching on `|r|`, caliper `0.25·SD(|r|)`, greedy, deterministic tie-break (|r| asc, timestamp asc), reference pool = smaller of NEG/POS (equal → POS); unmatched shocks counted and reported; no trimming.
- **Evaluability:** a market is primary-evaluable iff all 3 strata have ≥ 30 matched pairs; a class needs ≥ 2 evaluable markets for a primary verdict (single-market classes = EVIDENCE-LIMITED/DESCRIPTIVE).
- **Statistic:** `d_{m,s}` = mean over matched pairs of (ΔlnRV of the negative-shock day − ΔlnRV of the positive-shock day); `d_m` = mean over the 3 strata; `D_class` = equally-weighted mean over the class's primary-evaluable markets.
- **Inference:** synchronized class-level circular calendar-block bootstrap, `L = 11` trading days (full response span), `B = 10,000`, single master seed `20260813`; two-sided `p = 2·min(Pr*(D* ≥ D_obs), Pr*(D* ≤ D_obs))`; percentile CI (2.5%, 97.5%).
- **Family:** 11 class statistics (7 Layer A + 4 Layer B); Holm step-down at family-wise α = 0.05, applied exactly once.

## 3. Data and quality gates

**Layer A (historical HPD, 22 markets):** continuous ratio-back-adjusted front series; fingerprints of all 22 `front_<root>.csv`, `HPD_MANIFEST.csv`, `HPD_CONTRACT_HASHES.csv`, `FINAL_CLASSIFICATION.csv`, `PER_MARKET_VALIDATION.csv` verified against the frozen table (gate 1 PASS). Per-market daily rows 3,963–11,240; roll days 62–322 per market (gate 7 roll counts match `PER_MARKET_VALIDATION.csv` exactly for all 22 roots). Per-market coverage 1959-07-01 → 2002-10-01; the common Layer-A window is 1987-01-13 → 2002-08-30, exactly the registered common-window sensitivity range. Continuity-gated exclusions (ho, kc, pa, pb, pl, sb) and RESOLVED-NONUS roots (aor, cac, lj, ll) applied per §4; universe exactly 22 markets.

**Layer B (contemporary M1, 5 markets):** SHA-256 of all 5 `data/m1/*_M1.csv` verified against the frozen table (gate 1 PASS). Daily aggregation per §13: last-valid-bar close per UTC day. Daily days: XAUUSD 1,555 (2021-04-12→2026-04-10), XAGUSD 1,548 (2021-07-13→2026-07-12), EURUSD 1,427 (2021-01-04→2026-06-30), BTCUSD 1,825 (2021-05-23→2026-05-22), USATECHIDXUSD 871 (2023-09-01→2026-07-10). `dup_raw = 0` and `bad_close = 0` for every market; last-bar spot verification passed for all five (gate 8).

**Gate results:** all 11 §17 gates passed (fingerprints; universe; date ranges; duplicates; missingness; OHLC validity; roll consistency; aggregation; RV construction; leakage; continuity). No STOP condition triggered.

## 4. Shock population and matching

- Eligible shocks per market: Layer A 2,291–8,292 (total 119,847); Layer B 860–1,814 (total 7,165). Exclusions per market recorded (roll days, roll-window days, incomplete windows, zero-RV windows, zero-return days).
- All eligible shocks entered matching; **60,507 matched pairs** total (Layer A 56,471; Layer B 4,036).
- Unmatched counts per (market, stratum) recorded (typical 0–200 per side). Balance diagnostic (standardized mean difference of matched `|r|`, NEG vs POS): |SMD| mostly < 0.15 across strata; a minority of strata show 0.14–0.22 (ad, cl, cr, ed, jy, sf, jo, XAUUSD, USATECHIDXUSD). QC-only; no re-matching, re-weighting, or verdict rescinding (frozen rule).

## 5. Primary results — Layer A (historical)

| Class | Prior dir. | n_ev | D_class | 95% CI (percentile) | p_raw | p_Holm | Verdict |
|---|---|---|---|---|---|---|---|
| EQUITY_INDICES | classic | 1 | +0.1498 | [0.0791, 0.1914] | 0.6402 | 1.000 | EVIDENCE-LIMITED/DESCRIPTIVE |
| PRECIOUS_METALS | inverse | 2 | −0.0285 | [−0.0761, 0.0134] | 0.8974 | 1.000 | INCONCLUSIVE |
| ENERGY_CRUDE | classic | 1 | +0.0814 | [−0.0044, 0.1881] | 0.8262 | 1.000 | EVIDENCE-LIMITED/DESCRIPTIVE |
| COMMODITIES_OTHER | inverse | 9 | +0.0317 | [0.0143, 0.0499] | 0.9766 | 1.000 | INCONCLUSIVE |
| FX | two-sided | 6 | +0.0292 | [0.0068, 0.0530] | 0.9906 | 1.000 | INCONCLUSIVE |
| RATES | two-sided | 2 | +0.0034 | [−0.0577, 0.0637] | 0.9674 | 1.000 | INCONCLUSIVE |
| INDEX_COMMODITY | two-sided | 1 | −0.0158 | [−0.0855, 0.0489] | 0.9300 | 1.000 | EVIDENCE-LIMITED/DESCRIPTIVE |

Per-market `d_m` (all 22 Layer A markets evaluable): ad +0.116, bp −0.008, c +0.022, cd +0.136, cl +0.081, cr −0.016, ct +0.039, dx +0.047, ed −0.028, fc +0.141, gc −0.001, hg +0.011, jo −0.025, jy −0.089, lh +0.071, o +0.041, s −0.018, sf −0.027, si −0.056, sp +0.150, us +0.035, w +0.002.

## 6. Primary results — Layer B (contemporary)

| Class | Prior dir. | n_ev | D_class | 95% CI (percentile) | p_raw | p_Holm | Verdict |
|---|---|---|---|---|---|---|---|
| PRECIOUS_METALS | inverse | 2 | +0.0138 | [−0.0807, 0.1018] | 0.9858 | 1.000 | INCONCLUSIVE |
| EQUITY_INDICES | classic | 1 | +0.4220 | [0.2699, 0.5788] | 0.9976 | 1.000 | EVIDENCE-LIMITED/DESCRIPTIVE |
| FX | two-sided | 1 | +0.0610 | [−0.0469, 0.1613] | 0.8990 | 1.000 | EVIDENCE-LIMITED/DESCRIPTIVE |
| CRYPTO | two-sided | 1 | +0.0256 | [−0.1054, 0.1131] | 0.7008 | 1.000 | EVIDENCE-LIMITED/DESCRIPTIVE |

Per-market: XAUUSD +0.0365, XAGUSD −0.0090, EURUSD +0.0610, BTCUSD +0.0256, USATECHIDXUSD +0.4220 (all 5 evaluable).

## 7. Multiple-comparison family

The complete 11-member primary family (7 Layer A + 4 Layer B), Holm step-down at α = 0.05: all raw p ≥ 0.6402; after Holm every adjusted p = 1.000. No family member is significant. The family was applied exactly once; no post-hoc expansion.

## 8. Cross-era interpretation (registered classes only)

- **PRECIOUS_METALS** (both layers evaluable): Layer A D = −0.0285 (inverse sign, matching prior), Layer B D = +0.0138 (classic sign, opposite prior). Signs disagree across eras; neither layer reliable.
- **EQUITY_INDICES**: Layer A +0.150, Layer B +0.422 — same (classic) direction in both eras; both layers single-market → EVIDENCE-LIMITED/DESCRIPTIVE; cannot anchor a strong cross-era claim.
- **FX**: Layer A +0.029, Layer B +0.061 — same direction in both eras; Layer B single-market → EVIDENCE-LIMITED.

Per §10/§18, no cross-era claim is strong replication; the comparison is reported as EVIDENCE-LIMITED.

## 9. Secondary analyses (segregated; non-rescuing)

All executed as registered (§21); none changes the primary, its family, or its verdicts.

- **1-day horizon:** class D point estimates range −0.24 (INDEX_COMMODITY A) to +0.62 (EQUITY_INDICES B); no stable pattern.
- **21-day horizon:** point estimates range −0.10 to +0.18; signs often opposite the 5-day estimates.
- **Standardized-shock matching:** point estimates close to primary (e.g., COMMODITIES_OTHER +0.033; EQUITY_INDICES A +0.155).
- **Absolute-return response:** near zero everywhere (|D| ≤ 0.0013) — the matched-pair ΔlnRV asymmetry does not translate into |r| differences at 5 days.
- **Layer-B intraday RV (different-frequency object):** CRYPTO +0.047, EQUITY_INDICES +0.225, FX +0.002, PRECIOUS_METALS −0.026. Explicitly NOT comparable to the daily primary and NOT usable for cross-era claims.
- **GJR(1,1) / EGARCH(1,1) γ diagnostics** (mandatory caveat reproduced verbatim: "A GJR/EGARCH coefficient does not replace the primary empirical response statistic and cannot rescue a failed primary result."): fitted GJR γ is ≤ 0 for essentially all markets, many at the −0.30 optimization bound (c, cd, dx, fc, gc, hg, lh, sf, us, w, EURUSD, USATECHIDXUSD), i.e., the parametric sign-bias points toward *inverse* asymmetry at the GARCH-model level while the primary ΔlnRV point estimates lean *classic* — the two objects disagree directionally and are both non-confirmatory; EGARCH γ signs are mixed (boundary-heavy). Engle–Ng sign-bias regressions are reported in the artifact.
- **Winsorization (95th percentile |r| cap):** point estimates close to primary (e.g., COMMODITIES_OTHER +0.032; EQUITY_INDICES A +0.155) — primary estimates are not driven by extreme shocks.
- **Common-window Layer A (1987-01-13 → 2002-08-30):** class point estimates remain close to the full-sample values (e.g., EQUITY_INDICES +0.170 vs +0.150; PRECIOUS_METALS −0.053 vs −0.028; FX +0.023 vs +0.029) — no era-dependence at the point-estimate level.

## 10. Scientific interpretation

- **No class achieves SUPPORT** (reliable asymmetry in the expected direction) and **no class achieves CONTRADICTION** (reliable opposite asymmetry): the minimum raw two-sided p across the 11-member family is 0.64; every Holm-adjusted p is 1.00.
- **Signed classes with priors:** all four are INCONCLUSIVE (PRECIOUS_METALS, COMMODITIES_OTHER) or EVIDENCE-LIMITED/DESCRIPTIVE (EQUITY_INDICES, ENERGY_CRUDE, each single-market). The literature priors are therefore **not reproduced with reliability**.
- **Two-sided classes (FX, RATES, INDEX_COMMODITY, CRYPTO):** no reliable sign-dependent asymmetry in either direction; reported descriptively (CONTRADICTION is not defined for two-sided classes).
- **Point-estimate pattern (descriptive, non-confirmatory):** most classes lean *classic* (D > 0) at the 5-day horizon; PRECIOUS_METALS Layer A leans inverse (prior-matching) but Layer B leans classic (opposite). Absolute-return responses are ~0, GJR/EGARCH γ lean inverse, and 1-/21-day horizons show unstable signs — the evidence is heterogeneous and directionally unstable across objects.
- **Registered-inference property (reported, not altered):** the two-sided bootstrap p is computed against the block-resampling distribution of D*, which is centered at D_obs (the resampling does not impose the null). Consequently p ≈ 1 for every class by construction, and the registered SUPPORT/CONTRADICTION rule (Holm p < 0.05) can essentially never fire. The percentile CIs and point estimates carry the descriptive content (several CIs exclude zero, e.g., COMMODITIES_OTHER [+0.014, +0.050]); under the registered p-based decision rules these do not constitute reliable evidence. This property is a property of the frozen inference design; it was executed exactly as registered and is not "corrected" here.

## 11. Limitations

- **Class representation:** 7 of 11 family members rest on a single evaluable market (EVIDENCE-LIMITED by design); only COMMODITIES_OTHER (9), FX-A (6), PRECIOUS_METALS A/B (2), and RATES (2) support primary verdicts.
- **Inference construction:** the registered p-value (uncentered block-resampling two-sided) is degenerate (~1 by design); significance is effectively unattainable under the registered decision rule regardless of the data (see §10).
- **Dependence:** overlapping 5-day windows are addressed by the L=11 block length at the class level; long-memory volatility dependence beyond the response span is not modeled in the primary.
- **Era differences:** Layer A is a 1959–2002 panel; Layer B is 2021–2026. Cross-era comparisons are evidence-limited for every class.
- **Roll construction:** HPD roll days and their 10-day windows are excluded (62–322 rolls per market; thousands of window-days excluded); continuous ratio back-adjustment is assumed to preserve log-return sign structure.
- **Data quality:** M1 files had zero duplicate timestamps and zero invalid closes; HPD series passed all validation gates; no market was added or removed by outcome.

## 12. Reproducibility

- Execution script `run_h01_v1.py` is deterministic and replayable; frozen parameters table in `results_H01_V1.json` (`frozen_params`) and `experiment_metadata_H01_V1.json`.
- The B=10,000 bootstrap was executed as a checkpointed run (`.build_cache/`, per-class draw arrays + consumed-count sidecars): block starts are generated from the single master seed in exact serial order; per-replicate draws are bit-identical between the serial and the parallel worker path (verified at B=100), so the checkpointed parallel run equals one uninterrupted serial run. Completed RNG consumption is replayed on resume; cache identity (B, L) is validated before use.
- M1 daily aggregation and the Layer-B intraday object are implemented with a streaming csv-module pass (the registered last-wins dedup, §13) because pandas 3.0.2 on this platform segfaults on `drop_duplicates` for >2M-row frames and can OOM in the C parser; the streaming output was verified byte-identical to the registered pipeline's recorded daily series for all 5 markets (`dup_raw = 0` in every market, so the dedup is a no-op).
- Internal-consistency audit (recomputed p, CI, null mean from the persisted 110,000 replicate draws; Holm recomputation; cache ≡ CSV draws; 60,507 matched pairs with delta consistency; evaluability rules): **PASS**.
- UTF-8 throughout; Python/NumPy/pandas/SciPy versions, seed, bootstrap parameters, and protocol SHA-256 recorded in the metadata artifact.

## 13. Promotion status

**Scientific research evidence only.** H01 is a volatility-behavior association result; it implies nothing about tradability. No trading strategy, detector, BOE configuration, StrategyManifest, Assembly, or Deployment artifact was created; no economic gate was applied; no cost model was constructed (HPD costs are unobserved and none were fabricated).

## 14. Integrity statement

- Protocol v1.1.0 remained byte-for-byte unchanged (SHA-256 verified before and during execution); no parameter tuning; no outcome-driven selection; no market added/removed by result; no secondary analysis rescued or altered the primary; TEST was not reused; no BOE/Assembly/Deployment/contract/governance file was modified.
- The experiment answers only: *do positive and negative daily return shocks produce different subsequent volatility responses, after controlling for pre-shock volatility state, and does the sign agree with the literature by asset class?* It does not answer "can we make money from it" and does not authorize building a volatility detector.

## 15. Exact next decision (per registered stopping/promotion rules)

The protocol contains no promotion trigger for this outcome. The result is **INCONCLUSIVE** for the primary family: literature priors are not reproduced with reliability, no class contradicts reliably, and the registered inference construction makes significance structurally unattainable. Recommended next step per the scientific pipeline (H01 experiment → scientific interpretation → replication/robustness decision → economic question only if independently justified): a **scientific replication/robustness review** that (a) evaluates whether the registered p-value construction (uncentered block resampling) should be revisited by a registered amendment, and (b) assesses power/design adequacy of the 5-day matched-pair design given the observed near-zero absolute-return responses. No H02/H03 is invented; no runtime semantics follow from this result.
