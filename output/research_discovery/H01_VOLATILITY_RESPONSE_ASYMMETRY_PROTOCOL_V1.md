# QUANTFORGE — PRE-REGISTRATION — H01 VOLATILITY RESPONSE ASYMMETRY V1

**Protocol version:** 1.2.0 (v1.0.0 initial pre-registration + v1.1.0 outcome-blind audit-correction amendment + v1.2.0 outcome-blind null-inference amendment — see Amendment Record below)
**Status:** FROZEN PRE-REGISTRATION — created before any H01 outcome inspection; v1.1.0 amendment written outcome-blind; v1.2.0 null-inference amendment written outcome-blind (see Amendment Record — v1.2.0).
**Date of freeze:** 2026-08-13 (v1.0.0); v1.1.0 amendment written 2026-08-13, outcome-blind; v1.2.0 amendment written 2026-08-16, outcome-blind
**Project state:** QuantForge Engine COMPLETE/FROZEN; Strategy Assembly V1 FROZEN; Mean-Reversion CLOSED (DISC-021); Fixed 12/1 TSMOM CLOSED (DISC-022); H01 upstream records: NEW_HYPOTHESIS_SCREENING_V1 (H01 40/45, Level-1), H01_READINESS_AUDIT_V1 (decision B — PROMISING BUT NOT READY, 32/45), H01_DEFINITION_LOCK_V1 (decision A — H01 LEVEL 2 / RESEARCH-READY).
**Authorized action:** design and freeze this protocol ONLY. No experiment is executed by this artifact. No effect is computed, no GARCH/EGARCH/GJR model is fitted, no outcome is inspected, no clustering is performed, no script, dataset, cache, or result file exists at pre-registration time.
**Planned experiment output root (future, at execution):** `output/research_discovery/H01_VOLATILITY_RESPONSE_ASYMMETRY/`
**Integrity rule:** until this protocol passes an independent read-only audit, no outcome data, event dataset, result table, or analysis script may exist anywhere in QuantForge.

Every scientific choice below was fixed before outcomes. Where the upstream records left a procedural instrument unfixed (matching procedure, contemporary RV construction, control form, inference form, family boundary), this protocol resolves it as a pre-registration decision now, not at execution.

## Amendment Record — v1.1.0 (outcome-blind audit correction)

The independent read-only audit of the v1.0.0 protocol returned **FAIL — REVISE BEFORE EXECUTION** with 12 findings. This amendment implements the required corrections. **No H01 outcome was inspected at any point; this amendment was written entirely outcome-blind.** The frozen scientific question (§1), response definition (§3 + mandatory GJR/EGARCH caveat), horizon (§5), normalization (§6), vol-state stratification (§7), sign convention (§11), primary family + Holm correction (§15), data-quality gates (§17), economic firewall (§20), and prohibited-methods scope (§22) are **unchanged**. Sections modified: §2, §4, §6, §8, §9, §10, §11, §12, §13, §16, §18, §22, §23, §24. Original v1.0.0 language is preserved wherever unaffected; nothing is deleted from the scientific record.

**Corrections (audit findings 1–12):**
1. **Matching (§2):** rank-only `|r|` matching replaced by **nearest-neighbour caliper matching on `|r|`** (Option B; Austin 2011 matching-caliper methodology), caliper `0.25·SD(|r|)` within (market, stratum), greedy one-to-one, no reuse, unmatched counted, balance diagnostic (confirmatory/QC only).
2. **Ties (§2):** deterministic stable sort key `(|r| ascending, timestamp ascending)`; zero-return days (`r_t = 0`) excluded and counted.
3. **Excess/tail (§2, §8):** all eligible shocks enter matching; only matched pairs enter the primary statistic; unmatched counts reported — no adaptive trimming, no threshold.
4. **Zero-RV (§2, §12, §13):** a shock is ineligible if either window's `RV = 0`; counted and reported; no arbitrary epsilon.
5. **Minimum pair / missing stratum (§11):** a market is primary-evaluable only if all 3 strata have **≥ 30 matched pairs** (structural CLT-based floor, frozen pre-outcome, not derived from QuantForge data); failing markets retained in diagnostics.
6. **Minimum market (§11, §18):** ≥ 2 evaluable markets required for a primary class verdict; single-market classes = **EVIDENCE-LIMITED/DESCRIPTIVE**; the ≥2/3 consistency rule is never vacuous for a single evaluable market.
7. **Provenance (§4):** `continuity_ok` exclusions stated as pre-H01 frozen-pipeline facts, not outcome-derived; `hg` wording aligned to definition-lock §3 industrial-metals grouping.
8. **Bootstrap block length (§9, §16):** `L = 5` → **`L = 11` trading days** = full response span t−5..t+5, justified from the response DGP.
9. **Cross-market dependence (§9, §16):** independent per-market bootstrap + averaging replaced by **synchronized class-level calendar-block resampling** (union calendar, circular blocks).
10. **Bootstrap mechanics (§16):** circular blocks, wrap-around, replicate construction, pairing preservation within replicates, missing-market behavior, two-sided p-value formula, percentile CI, single master seed, `B = 10,000` fully specified.
11. **Two-sided classes (§18):** the ±0.2σ symmetry bound is **removed**; null = zero asymmetry; SUPPORT = reliable asymmetry in either direction; INCONCLUSIVE = failure to distinguish from zero; no replacement margin invented.
12. **Layer B missing-day rule (§13):** explicit daily-presence rule (≥ 1 valid M1 bar), incomplete-window dropping, weekend/closure/zero-RV handling, coverage-edge days — mirrors §12.

## Amendment Record — v1.2.0 (outcome-blind null-inference correction)

The post-execution **H01 INFERENCE VALIDITY AUDIT** established a structural defect in the v1.1.0 registered inference: §9.6/§16 registered `p = 2 × min(Pr*(D* ≥ D_obs), Pr*(D* ≤ D_obs))`, which computes the tail of the block-resampling **sampling** distribution at the observed statistic `D_obs`. Because the bootstrap draws `D*` are centered at (approximately) `D_obs`, this quantity is ≈ 1 regardless of whether the null holds; it is invariant to shifting the whole distribution by a constant and has no power against `H0: D_class = 0`. It is a sampling-distribution diagnostic, not a hypothesis test. The v1.1 execution was faithful to the registered protocol; the defect is in the registered inference design itself.

Governance chain (each step outcome-blind with respect to the corrected inference):
1. **H01 POST-EXECUTION INFERENCE VALIDITY AUDIT** — independently re-derived the registered p-value mathematics from the protocol and the persisted artifacts (all 110,000 replicate draws), confirmed the "p ≈ 1 by construction" diagnosis, and classified the v1.1 confirmatory result **CONFIRMATORY INFERENCE INVALID / SCIENTIFIC RESULT UNADJUDICATED** (governance classification C).
2. **H01 NULL-DISTRIBUTION METHODOLOGY DECISION V1** — outcome-blind methodology study concluding **A — VALID NULL-IMPOSING METHOD IDENTIFIED**: the null-centered synchronized circular calendar-block bootstrap (recentered pivot form), defined conceptually.
3. **H01 NULL-DISTRIBUTION METHODOLOGY DECISION AUDIT** — independent read-only audit of that decision concluding **A — METHODOLOGY VALID**, with three precision requirements carried into this amendment: (i) register the data-level form as the authoritative implementation; (ii) freeze the Monte-Carlo convention; (iii) disclose the bootstrap/matching-consistency limitations.

This amendment implements those three requirements. **No new method was selected from the observed H01 results:** no H01 effect magnitude, class ranking, CI, p-value, or observed significance was inspected or used to choose the corrected construction. The scientific object is unchanged. The amendment changes ONLY the null-testing/p-value layer of the primary inference. The v1.0.0 and v1.1.0 history above is preserved verbatim and remains part of the scientific record.

**Sections modified:** header (version/status/date), this record, §9 item 6, new §9A (operative null-inference specification), §16 (version line, bootstrap-mechanics p-value, FROZEN_PARAMS), §18 (p reference), §24 (integrity + next action). All other sections unchanged. Original v1.1.0 language is preserved wherever unaffected; nothing is deleted from the scientific record.

**1. Primary null (restated).** `H0: D_class = 0` for each primary class — the mean/class-location null: the vol-state-conditioned, magnitude-matched difference in forward `ΔlnRV` between negative and positive shocks is zero. It is NOT expanded into equality of full conditional response distributions, sign exchangeability of the pair-difference process, causal equality, or any GARCH-coefficient null.

**2. Primary null-imposing construction (data-level form — AUTHORITATIVE).** For each (market `m`, stratum `s`):
1. Retain the frozen matched-pair dataset exactly as defined by v1.1 (§2, §7, §11).
2. Compute the observed stratum mean `c_(m,s) = mean(d_i)` over the matched pairs in (m, s), where `d_i = ΔlnRV(negative-shock day) − ΔlnRV(positive-shock day)`. `c_(m,s)` is a **frozen full-sample constant** — computed once on the original matched data, never re-estimated inside any replicate (the same treatment as the frozen calipers and tercile bounds).
3. Construct the null response process at the **shock-response level (registered implementation)**: for each (market `m`, stratum `s`), subtract `c_(m,s)/2` from the `ΔlnRV` response of every eligible negative-shock day in (m, s) and add `c_(m,s)/2` to the `ΔlnRV` response of every eligible positive-shock day in (m, s) — applied to **every eligible shock**, including shocks unmatched in the original sample that may become matched after bootstrap resampling. The pair-level form `d_i^0 = d_i − c_(m,s)` is the equivalent statement for every matched pair; any deterministic sign-split that produces pair difference `d_i − c_(m,s)` is mathematically equivalent, and the ±`c_(m,s)/2` representation is the registered implementation.
4. Apply the EXISTING registered bootstrap/block-resampling/matching machinery (§9.1–§9.5, §16) to the null-transformed response process: same union calendar per class, same `L = 11` blocks, same `B = 10,000`, same master seed `20260813`, matching recomputed inside replicates exactly as registered (matching is response-blind — it depends only on `|r|`, stratum, and dates — so recentering does not change pairing). The transformation is applied before rebuilt matching in each replicate; matching and eligibility are unchanged.
5. Compute the frozen market and class statistics exactly as v1.1 specifies (§11), including the registered empty-stratum handling (§9.3).

The purpose is to impose `E[d_(m,s)] = 0` at the conditioning level of the registered H01 null. `c_(m,s)` is computed once from the frozen observed matched data, is frozen for all bootstrap replicates, and is never recomputed inside replicates. **Unchanged:** shock matching, pair assignment, calipers, strata, eligibility, market membership, and the primary statistic `d_{m,s}`/`d_m`/`D_class` and its construction.

**3. Statistic-level pivot form.** `D*_null = D* − D_obs` is registered as the equivalent statistic-level representation, with this precise status:
- the **data-level form (item 2) is authoritative**;
- the statistic-level form is **exactly equivalent** when all required strata are represented in the replicate for every evaluable market (the equal 1/3 stratum weights and the fixed equal market weights make the recentering constant exactly `D_obs`);
- when the registered empty-stratum aggregation rule (§9.3) creates a difference, **the data-level form controls**;
- the protocol **never silently substitutes** the statistic-level shortcut where it is not exact.

This is the critical clarification from the methodology audit: the audit documented that the persisted v1.1 replicates show material deviations of the replicate mean from `D_obs` in some classes, attributable precisely to the empty-stratum aggregation rule. The v1.2 execution therefore implements the data-level form.

**4. Bootstrap machinery (preserved unchanged).** Synchronized circular calendar blocks; `L = 11` trading days; `B = 10,000`; master seed `20260813`; synchronized cross-market resampling; matching reconstruction inside replicates; fixed evaluable-market membership; frozen calipers; frozen volatility strata. The amendment changes only which response values enter the null resampling. No new bootstrap family is introduced.

**5. Corrected p-value.** The v1.1 formula `2 × min(Pr*(D* ≥ D_obs), Pr*(D* ≤ D_obs))` is **retired** and plays no role in the primary inference. The frozen null-test is:

`p_two = Pr*( |D*_null| ≥ |D_obs| )`

- the observed statistic is compared with the null distribution centered at zero;
- this is a hypothesis test of `H0: D_class = 0`;
- this is NOT the former D_obs-centered sampling-distribution diagnostic.

**6. Monte-Carlo convention (frozen).** `p = (1 + count)/(B + 1)`, with `count = #{b : |D*_null,b| ≥ |D_obs|}`. This is the standard conservative finite-B convention: it never yields a zero p-value at finite B, is uniform to O(1/B) under the null for continuous draws, and is chosen from statistical first principles (finite-B exactness), not from any H01 result. No RNG changes are required; the existing master seed drives the identical resampling streams.

**7. Confidence interval (retained).** The registered percentile bootstrap CI `(2.5%, 97.5%)` remains the reported interval — a **sampling interval** for `D_class`, computed from the ordinary sampling draws `D*` (the block-resampling distribution centered at `D_obs`). Explicitly distinguished: the sampling CI is a coverage statement about the parameter; the hypothesis-test p-value is the tail probability of the null-imposed draws `D*_null`. The CI is not replaced by the null distribution, and the old CI is never reinterpreted as a p-value.

**8. Holm family (unchanged).** Preserved exactly: 11 primary class tests (7 Layer A + 4 Layer B), Holm step-down, family-wise `α = 0.05`. The corrected v1.2 p-values — not the retired v1.1 p-values — feed Holm. No family member is added or removed.

**9. Scientific decision rules (unchanged; p now the v1.2 null-test p).** §18 applies verbatim with "family-adjusted two-sided bootstrap p-value" read as the corrected v1.2 null-test p (§9A.4): SUPPORT (signed classes) = valid Holm-adjusted p < 0.05, direction matches the registered prior, ≥ 2/3 evaluable-market sign consistency, cross-era requirement where registered; CONTRADICTION = valid Holm-adjusted p < 0.05 in the registered opposite direction (or other registered contradiction condition); INCONCLUSIVE = otherwise. Two-sided classes: significant nonzero asymmetry → SUPPORT; failure to distinguish from zero → INCONCLUSIVE; no equivalence bound is invented. Single-market classes remain EVIDENCE-LIMITED/DESCRIPTIVE. No other decision rule is introduced.

**10. Bootstrap/matching limitations disclosure.** Block-bootstrap consistency is assumed for the registered dependence structure; the estimator contains greedy nearest-neighbour caliper matching; the protocol uses a nonparametric bootstrap with matching rebuilt in each replicate; Abadie–Imbens-style nearest-neighbour bootstrap caveats exist for fixed-M matching estimators; the exact construction here is not claimed to have a dedicated published theorem; this caveat applies to the sampling CI and the corrected hypothesis test alike; the correction does not claim stronger finite-sample guarantees than the methodology supports. This is a limitations disclosure, not a claim of invalidity.

**11. Outcome-blind statement.** The v1.2 inference method was selected from statistical principles and methodological literature after identifying a structural defect in v1.1. No H01 effect magnitude, class ranking, CI, p-value, or observed significance was used to select the method.

**12. Status of the v1.1 execution.** The v1.1 execution remains frozen and is classified **CONFIRMATORY INFERENCE INVALID / SCIENTIFIC RESULT UNADJUDICATED**. It cannot be retroactively converted into a v1.2 result. Its descriptive components (point estimates, matching counts, balance diagnostics, data-quality results, reproducibility) retain the status assigned by the inference-validity audit; its primary p-values and Holm-adjusted significance carry no confirmatory weight.

**13. Re-execution rule.** After v1.2: (1) independent read-only audit of v1.2; (2) only after PASS, corrected re-execution; (3) corrected re-execution is a new registered analysis under v1.2; (4) old v1.1 p-values are never reused; (5) old v1.1 results are never mixed with v1.2 results. The re-execution uses the same data, matching, universe, statistic, dependence structure, and secondary firewall; only the registered inference changes.

**14. Secondary firewall (preserved).** All v1.1 restrictions remain (§21): no GJR/EGARCH rescue; no Engle–Ng rescue; no alternative-horizon rescue; no winsorization rescue; no intraday-RV rescue; no market selection; no class selection; no ML/K-means. Secondary analyses remain non-confirmatory.

---

## 1. Frozen Scientific Question

> **H01-L3 (pre-registered):** *For each market, the forward change in realized variance following a negative daily return shock differs from that following a positive daily return shock of equal absolute magnitude, after conditioning on the pre-shock realized-variance state. The expected direction of this asymmetry is asset-class specific, as frozen in §4.*

- Null form per class: the vol-state-conditioned, magnitude-matched difference in forward `Δln RV` between negative and positive shocks is zero.
- The claim is an **association** claim (statistical regularity), never a causal/mechanism claim (definition-lock §10).
- The claim is **not** return prediction, vol timing, short-vol, regime filtering, trend filtering, or a mean-reversion signal (definition-lock §17). Independence from DISC-021 and DISC-022 is preserved; H01 is exclusively a volatility-behavior hypothesis.

## 2. Primary Shock (Exposure) Definition

- **PRIMARY exposure:** the daily close-to-close log return `r_t` as a signed scalar.
- **Eligibility (frozen):** a shock day `t` is eligible for matching iff it passes the window rules of §8/§12/§13 (roll days, missing days, invalid rows, zero-RV windows) and `r_t ≠ 0`. A zero-return day (`r_t = 0`) is neither `NEG` nor `POS`, is excluded from matching, and is counted and reported.
- **Magnitude matching — frozen procedure (pre-registration decision; audit correction 1):** shocks are matched **within market** and **within pre-shock vol-state stratum** by **nearest-neighbour caliper matching on `|r_t|`** (Option B — caliper matching is the standard equal-covariate design; Austin 2011). This replaces the v1.0.0 rank-only rule, which did not bound the magnitude difference between paired shocks. Frozen algorithm:
  1. Within each (market, stratum) (frozen bounds, §7), collect the eligible shocks and split them into `NEG` (r_t < 0) and `POS` (r_t > 0). If either pool is empty, the (market, stratum) yields 0 matched pairs.
  2. Caliper `c = 0.25 × SD(|r|)` computed over **all eligible shocks in that (market, stratum)** (standard 0.25-standard-deviation matching caliper, Austin 2011). If fewer than 2 eligible shocks exist, `c` is undefined and the (market, stratum) yields 0 matched pairs. `c` is a constant on the exposure variable only — computed before any response is used — and is frozen, never re-estimated or tuned.
  3. **Reference pool** = the smaller of `NEG`/`POS` (equal sizes → `POS`, frozen); **match pool** = the other. Each pool is ordered by the frozen stable sort key `(|r_t| ascending, timestamp ascending)` (deterministic tie-break; audit correction 2).
  4. **Greedy one-to-one matching:** for each reference observation in frozen order, select the unmatched match-pool observation minimizing `| |r_ref| − |r_match| |` subject to `| |r_ref| − |r_match| | ≤ c`; ties in distance broken by smaller `|r|`, then earlier timestamp (frozen). Pair them and remove both from their pools. If no match-pool observation is within the caliper, the reference observation remains unmatched.
  5. Each shock is matched **at most once** (one-to-one, no reuse); matching is strictly **within (market, stratum)** — no cross-market, cross-stratum, or cross-era matching, no observation reuse.
  6. Unmatched shocks on either side are **counted and reported per (market, stratum)** (frozen rule; audit correction 3 — no adaptive trimming, no threshold).
  7. **Balance diagnostic (pre-registered; confirmatory/QC only, NOT a post-outcome selection rule):** per (market, stratum), report the mean `|r|` of matched `NEG` vs matched `POS` and their standardized mean difference alongside the results. It is reported; it never triggers re-matching, re-weighting, or rescinding of verdicts.
- **No percentile/z-score/event-threshold rule;** all eligible shocks enter the matching algorithm (§8). Only matched pairs enter the primary statistic.
- **SECONDARY (pre-declared, cannot rescue primary):** standardized shock `r_t/σ̂_{t−1}` and market-adjusted residual returns (Engle–Ng sign-bias discipline), used only as robustness diagnostics.

## 3. Primary Response Definition

- **PRIMARY response: the log change in realized variance** over the forward horizon relative to the pre-shock window:

  `Δln RV_t = ln(RV_{t+1..t+5}) − ln(RV_{t−5..t−1})`

- **RV construction (frozen across data resolutions, §12–§13):** a window's realized variance is the **sum of squared daily log returns** in that window.

  `RV_{a..b} = Σ_{τ=a..b} r_τ²`

- The log-change form is scale-invariant (unit-free), resolving cross-market comparability by construction (definition-lock §6). The response is a volatility **change**, not a level (Aït-Sahalia, Fan & Li 2013 definition).
- **GJR/EGARCH γ status (explicit, frozen):** γ is a **SECONDARY model representation / robustness diagnostic — NOT the primary hypothesis.** The following sentence is mandatory and cannot be altered at any later stage:

  > "A GJR/EGARCH coefficient does not replace the primary empirical response statistic and cannot rescue a failed primary result."

- The absolute-return response `E[|r_{t+h}|]` is a secondary alternative only.

## 4. Asset-Class Scope and Expected Directions (frozen)

Primary family classes are defined by the approved `FINAL_CLASSIFICATION.csv` asset_class field, mapped to the definition-lock §3 priors. No prior sign is invented for any class (locking rule).

### Layer A — Historical (HPD), primary universe: **22 markets**

Primary Layer A universe = the 28 validated CORE markets of `FINAL_CLASSIFICATION.csv`, **minus markets flagged `continuity_ok=False` in `PER_MARKET_VALIDATION.csv`** (ho, kc, pa, pb, pl, sb — structural continuity gate at the 5-day window scale), and **minus RESOLVED-NONUS roots** (aor, cac, lj, ll — non-US, quarantined-resolved). **Provenance (frozen; audit correction 7):** these `continuity_ok` exclusions **predate H01** and come from the frozen HPD acquisition/validation pipeline (`PER_MARKET_VALIDATION.csv`; rule `gaps_gt5d ≤ 2` AND `max_adj_roll_move_pct < 0.02`, where the flagged roll movements are classified EXPECTED CONTRACT-ROLL EFFECT in the acquisition report). They are **not H01 outcome-derived**, are not altered by H01, and are never re-admitted by outcome (§17 gate 11). Frozen universe:

ad, bp, c, cd, cl, cr, ct, dx, ed, fc, gc, hg, jo, jy, lh, o, s, sf, si, sp, us, w

| Class | Markets (roots) | Expected direction | Prior status |
|---|---|---|---|
| EQUITY_INDICES | sp | **Classic** (neg → larger vol increase) | ESTABLISHED |
| PRECIOUS_METALS | gc, si | **Inverse** (pos → larger vol increase) | ESTABLISHED |
| ENERGY_CRUDE | cl | **Classic** | ESTABLISHED (narrow) |
| COMMODITIES_OTHER | c, o, s, w (grains), ct, jo (softs), fc, lh (livestock), hg (copper — industrial-metals grouping of definition-lock §3) | **Inverse** | ESTABLISHED (broad) |
| FX | ad, bp, cd, dx, jy, sf | **Two-sided** — no prior sign | GENUINELY UNRESOLVED |
| RATES | ed, us | **Two-sided** — no prior sign | NO ESTABLISHED PRIOR |
| INDEX_COMMODITY | cr (CRB Index) | **Two-sided** — no prior sign (commodity basket index; no dedicated prior in the cited literature) | NO ESTABLISHED PRIOR |

### Layer B — Contemporary (M1), primary universe: **5 markets**

| Class | Markets (symbols) | Expected direction | Prior status |
|---|---|---|---|
| PRECIOUS_METALS | XAUUSD, XAGUSD | **Inverse** | ESTABLISHED |
| EQUITY_INDICES | USATECHIDXUSD | **Classic** | ESTABLISHED |
| FX | EURUSD | **Two-sided** — no prior sign | GENUINELY UNRESOLVED |
| CRYPTO | BTCUSD | **Two-sided** — no prior sign | GENUINELY UNRESOLVED |

**Classes present in both layers** (cross-era consistency testable, §10): PRECIOUS_METALS, EQUITY_INDICES, FX. **Layer A only:** ENERGY_CRUDE, COMMODITIES_OTHER, RATES, INDEX_COMMODITY. **Layer B only:** CRYPTO.

## 5. Primary Horizon and Windows

- **PRIMARY horizon: h = 5 trading days.** Forward window `[t+1, t+5]` vs pre-shock window `[t−5, t−1]` (shock day excluded from both windows).
- Literature anchor: Aït-Sahalia, Fan & Li (2013) document the effect at 5-day and 21-day horizons; the 1-day and 21-day horizons are **secondary only** and cannot rescue the primary.
- Overlapping forward windows create serial dependence; the pre-registered inference (§9) must (and does) address this.

## 6. Normalization

- **PRIMARY: within-market normalization.** Each market analyzed on its own scale; `Δln RV` is unit-free; `|r_t|` caliper matching is within-market and within-stratum (§2). No cross-market scaling in the primary.
- Within-asset-class aggregation uses **signed per-market statistics only** (means/counts of per-market results), never pooled raw responses across markets or classes, per definition-lock §8.
- No invented cross-market normalization is adopted.

## 7. Confound Control — Pre-Shock Volatility State (one PRIMARY, frozen)

**Confound:** symmetric volatility clustering can appear asymmetric if negative and positive shocks occur in different volatility states.

- **PRIMARY control — within-market stratification on the pre-shock realized-variance state:** for each market, freeze **terciles of `ln(RV_{t−5..t−1})`** computed once over the market's full eligible series (`ξ_low`, `ξ_mid`, `ξ_high`). These tercile bounds are treated as constants for the analysis and are NOT re-estimated inside any bootstrap/class step. Matching (§2) and the per-stratum statistic (§11) are computed **within** each (market, stratum).
- This isolates sign of shock from the pre-existing volatility state — the Engle–Ng sign-bias discipline in non-parametric form (definition-lock §9).
- **SECONDARY (pre-declared, cannot rescue primary):** regression adjustment using `ln(RV_back)` as a covariate in the pair-difference model; GJR/EGARCH γ; sign-bias regressions on standardized residuals.
- Do not overbuild: no HMM, clustering, or multi-regime state modeling in the primary.

## 8. Extreme-Shock Treatment

- **PRIMARY: use ALL eligible shocks.** No winsorization, no invented percentile or z-score threshold, no event-threshold strategy. Caliper matching (§2) handles magnitude comparability; extreme days are eligible but may remain unmatched if no opposite-sign shock lies within the frozen caliper — such days are counted and reported, never silently dropped or adaptively trimmed (audit correction 3).
- **SECONDARY (pre-declared, cannot rescue primary):** a literature-standard winsorization **only if** it can be specified a priori as documented below — none is adopted. Any additional trimming rule must be added as an explicit protocol amendment, never at execution.
- H01 is explicitly **not** converted into a threshold-based event rule.

## 9. Dependence-Aware Inference (ONE PRIMARY, frozen)

**Problem:** overlapping 5-day forward windows make consecutive shock responses serially dependent; treating shocks as independent would inflate significance. In addition, markets within a class can respond contemporaneously to common news, so cross-market dependence must be preserved at the class level (audit corrections 8 and 9).

- **PRIMARY inference — synchronized class-level calendar-block bootstrap (replaces the v1.0.0 within-market bootstrap + averaging):**
  1. **Resampling grid and block length:** for each class, define the **union calendar** = the sorted set of dates on which ≥ 1 market in the class has an eligible shock record. Block length **`L = 11` trading days** — the full span of the response windows (t−5..t+5). `L` is justified by the response DGP (a block of `L` consecutive union-calendar days preserves all serial dependence that overlapping 11-day response windows create) and is frozen, not tuned. `B = 10,000` replicates; single master seed **20260813** (§16) drives the block resampling.
  2. **Block resampling (circular, with replacement):** each replicate is formed by sampling union-calendar positions uniformly with replacement and concatenating the circular blocks of `L` consecutive union-calendar days starting at those positions (wrap-around covers the grid end; no truncation, no padding).
  3. **Per-market replicate statistics:** for each market `m`, the replicate stream is `m`'s eligible shock records whose dates fall in the sampled blocks, ordered by date. Recompute, within each (m, stratum), the caliper matching (§2) and the per-stratum statistic (§11) on that replicate stream, using the **frozen** tercile bounds; yield per-market bootstrap draws `d_m^(b)` = the mean over `m`'s strata that yield ≥ 1 matched pair in the replicate (if no stratum yields pairs, `m` contributes no draw to that replicate).
  4. **Class level:** `D_class^(b)` = equally weighted mean of `d_m^(b)` over the class's **primary-evaluable** markets (§11). Evaluable-market membership is fixed at the original-data stage and never re-selected inside a replicate (pairing/selection preservation).
  5. **Dependence preserved:** synchronized blocks keep same-date shocks across markets together (cross-market contemporaneous dependence); `L = 11` covers the response-window span within each market (within-market serial dependence). Missing-market behavior: a market simply has no record for union days on which it did not trade — inherent to the union-grid construction, never imputed.
  6. **p-value (v1.2.0 — null-imposing; replaces the v1.1.0 formula — see §9A and Amendment Record — v1.2.0):** two-sided null-test p = `Pr*( |D*_null| ≥ |D_obs| )` over the B null-imposed draws `D*_null` (data-level form, §9A.2; statistic-level pivot `D*_null = D* − D_obs` only where exactly equivalent, §9A.3). Monte-Carlo convention `(1 + count)/(B + 1)` with `count = #{b : |D*_null,b| ≥ |D_obs|}`. The v1.1.0 formula `2 × min( Pr*(D* ≥ D_obs), Pr*(D* ≤ D_obs) )` is **retired** — it compared the sampling distribution against `D_obs` and was not a test of H0. **CI:** percentile interval (2.5%, 97.5%) of the ordinary sampling replicate distribution (unchanged; sampling interval only, §9A.5).
- **SECONDARY (pre-declared, cannot rescue primary):** non-overlapping weekly sampling of the shock set; cluster-robust inference treating each market-year as a cluster. Reported only as robustness.

## 9A. Null-Imposing Inference (v1.2.0) — Operative Specification

This section is the operative null-inference specification; it replaces the p-value layer of §9.6 and §16. Registered outcome-blind; governance and rationale in Amendment Record — v1.2.0.

**9A.1 Null hypothesis.** `H0: D_class = 0` per primary class — the vol-state-conditioned, magnitude-matched difference in forward `ΔlnRV` between negative and positive shocks is zero (mean/class-location null). Not expanded beyond that (Amendment Record — v1.2.0, item 1).

**9A.2 Data-level null construction (authoritative).** Given the frozen v1.1 matched-pair dataset per (market `m`, stratum `s`):
1. `c_(m,s) = mean(d_i)` over the matched pairs in (m, s), `d_i = ΔlnRV(negative-shock day) − ΔlnRV(positive-shock day)` — computed once on the full original matched data; **frozen** for all bootstrap replicates, never re-estimated inside a replicate.
2. **Null transformation (shock-response level — the registered implementation).** For each (market `m`, stratum `s`), subtract `c_(m,s)/2` from the `ΔlnRV` response of every eligible negative-shock day in (m, s) and add `c_(m,s)/2` to the `ΔlnRV` response of every eligible positive-shock day in (m, s). The transformation is applied to **every eligible shock** — including shocks unmatched in the original sample that may become matched after bootstrap resampling — before rebuilt matching in each replicate. Equivalently, every pair's difference becomes `d_i^0 = d_i − c_(m,s)`. Any deterministic sign-split that produces pair difference `d_i − c_(m,s)` is mathematically equivalent; the ±`c_(m,s)/2` representation is the registered implementation.
3. Run the registered synchronized circular calendar-block resampling (§9.1–§9.5, §16) on the null-transformed response process: same union calendar per class, `L = 11`, `B = 10,000`, master seed `20260813`, circular wrap-around, matching rebuilt inside replicates with frozen calipers and tercile bounds (response-blind — pairing identical to the sampling construction), evaluable-market membership fixed, per-stratum/per-market/class statistics computed exactly as §11 specifies including the §9.3 empty-stratum rule. Matching and eligibility are unchanged by the transformation.

The replicate draws are the null draws `D*_null`, centered at zero by construction. The transformation is additive within each (market, stratum) and therefore preserves variances, covariances, serial dependence, and synchronized cross-market dependence of the response process.

**9A.3 Statistic-level pivot form.** `D*_null = D* − D_obs` is the equivalent representation when every evaluable market has all three strata represented in the replicate (equal 1/3 stratum weights and fixed equal market weights make the recentering constant exactly `D_obs`). Where the §9.3 empty-stratum rule creates a difference, the data-level form (9A.2) controls. The statistic-level shortcut is never silently substituted where it is not exact. Execution implements 9A.2.

**9A.4 p-value.** Two-sided: `p_two = Pr*( |D*_null| ≥ |D_obs| )` over the B null draws. Monte-Carlo convention (frozen): `p = (1 + count)/(B + 1)`, `count = #{b : |D*_null,b| ≥ |D_obs|}`. One-sided forms (only if a future amendment adopts directional tests): `Pr*(D*_null ≥ D_obs)` / `Pr*(D*_null ≤ D_obs)` with the same convention. The v1.1.0 formula `2 × min(Pr*(D* ≥ D_obs), Pr*(D* ≤ D_obs))` is retired and plays no role in the primary inference.

**9A.5 Confidence interval.** Percentile interval `(2.5%, 97.5%)` of the ordinary sampling draws `D*` — the registered sampling interval for `D_class`. It is not a p-value and is not replaced by the null distribution.

**9A.6 Limitations.** Block-bootstrap consistency is assumed for the registered dependence structure; the estimator contains greedy nearest-neighbour caliper matching; the protocol uses a nonparametric bootstrap with matching rebuilt in each replicate; Abadie–Imbens-style nearest-neighbour bootstrap caveats exist for fixed-M matching estimators; the exact construction here is not claimed to have a dedicated published theorem; this caveat applies to the sampling CI and the corrected hypothesis test alike; the correction does not claim stronger finite-sample guarantees than the methodology supports. This is a disclosure, not a claim of invalidity.

## 10. Two-Layer Interpretation (frozen structure)

- **Layer A** = historical HPD panel (1974–2004 per-root coverage; common window ~1987–2002). **Layer B** = contemporary 2021–2026 M1 panel.
- **No combined/pooled estimator spanning both layers** in the primary. The cross-era object is a **per-class directional-consistency comparison** (mirroring the TSMOM Condition-8 discipline at the class level, on a distributional rather than return-predictive object).
- Cross-era consistency is evaluated **only where the class exists in both layers** (PRECIOUS_METALS, EQUITY_INDICES, FX); Layer-A-only and Layer-B-only classes are evaluated within their layer. **Single-market layers (audit correction 6):** if a class has only one primary-evaluable market in a layer (e.g., EQUITY_INDICES: `sp` Layer A, `USATECHIDXUSD` Layer B; FX Layer B: `EURUSD`; CRYPTO: `BTCUSD`), that layer's contribution is **EVIDENCE-LIMITED/DESCRIPTIVE** (§18): it cannot anchor a strong cross-era replication, and the cross-era comparison is reported as evidence-limited — never as replicated strong evidence.
- Per-market primary uses each market's full validated series. A **secondary sensitivity** (cannot rescue) restricts Layer A to the common window 1987-01-13 → 2002-08-30, matching the TSMOM V2 discipline.

## 11. Primary Statistic and Sign Convention (frozen)

- Per-market, per-stratum statistic:

  `d_{m,s} = mean over matched pairs in (m, s) of [ ΔlnRV(negative-shock day) − ΔlnRV(positive-shock day) ]`

- Per-market statistic:

  `d_m = mean over the 3 strata of d_{m,s}`   (equally weighted strata — a large stratum cannot dominate)

- Class statistic:

  `D_class = mean over the class's primary-evaluable markets of d_m`   (equally weighted markets — a large market/observation-dense market cannot dominate)

- **Evaluability (frozen; audit correction 5):** a market is **primary-evaluable** iff **all 3** strata yield **≥ 30 matched pairs** in the original (pre-bootstrap) data. The floor of 30 matched pairs per stratum is a **structural rule of thumb** (the conventional sample size above which a mean is stable under the central-limit theorem; the per-stratum statistic is a mean of matched-pair differences) — it is **frozen pre-outcome and NOT derived from QuantForge data inspection**. A market failing the floor (or with a stratum that yields no matched pairs per §2) is excluded from `D_class` but fully retained in per-market diagnostics (its strata and counts are reported).
- **Class evaluability (frozen; audit correction 6):** a class supports a **primary** verdict iff it has **≥ 2 primary-evaluable markets**. A class with 0–1 evaluable markets is **EVIDENCE-LIMITED/DESCRIPTIVE** (§18): its statistics and (family-adjusted) p-value are still reported and it remains in the §15 family, but no primary verdict is assigned and it cannot anchor strong cross-era claims.

- **Sign convention (no per-class flips):** `D > 0` = negative shocks raise forward vol more → **classic** sign; `D < 0` = positive shocks raise forward vol more → **inverse** sign. A class's verdict maps `sign(D_class)` against that class's frozen expected direction (§4).
- For two-sided classes the claim is `|response asymmetry| ≠ 0` in either direction; the sign is then reported descriptively.

## 12. Historical Layer A — Data, Filters, and Exclusion Rules (frozen)

- **Sources:** continuous ratio-back-adjusted front series `front_<root>.csv` (columns `date, sym, close, adj_close`) approved by `FINAL_CLASSIFICATION.csv`; per-market `PER_MARKET_VALIDATION.csv`; manifest flags from `HPD_MANIFEST.csv`.
- **Daily series:** use the continuous ratio-back-adjusted close (`adj_close`) per trading day. Log return `r_t = ln(adj_close_t / adj_close_{t−1})` on the continuous series. Ratio back-adjustment is multiplicative and preserves the log-return sequence's sign structure and volatility response (definition-lock §13).
- **Roll-day rule (pre-registration decision, frozen):** a `roll day` is a trading day on which the contract symbol `sym` changes relative to the previous trading day in the continuous series. A shock day `t` is **excluded** if any of: `t` is a roll day, or **any** of the 10 window days (`t−5..t−1` and `t+1..t+5`) is a roll day. Rationale: declared rolls can create artificial 1-day return spikes that would contaminate both the shock and the RV windows. The excluded-count fraction will be reported as a diagnostic, not as an outcome.
- **Missing-day policy (frozen):** a shock day `t` is excluded unless **all 5** days in each window are present in the market's daily series (incomplete windows are dropped, not imputed).
- **Zero-RV policy (frozen; audit correction 4):** a shock day `t` is **ineligible** if either `RV_{t−5..t−1} = 0` or `RV_{t+1..t+5} = 0` (a window of five zero daily returns; `ln(0)` is undefined). Such days are excluded from matching and **counted and reported**. No arbitrary epsilon is added (no `RV + ε` transformation).
- **Invalid-row exclusions (frozen):** any daily row with nonpositive `adj_close`/`close`, or flagged `ohlc_inconsistent`, `weekend_rows`, `zero_vol_rows`, `zero_oi_rows` per the manifest discipline (already structural), is excluded and its day is treated as missing (so windows touching it are dropped by the rule above).
- **Continuity requirement:** markets with `continuity_ok=False` in `PER_MARKET_VALIDATION.csv` are excluded from the primary universe (§4) — a structural gate fixed before outcomes. No market is added or removed because of results.
- The ingestion pipeline is NOT modified.

## 13. Contemporary Layer B — Data, Measurement, RV Construction (frozen)

- **Sources:** QuantForge `data/m1/{XAUUSD,XAGUSD,EURUSD,BTCUSD,USATECHIDXUSD}_M1.csv` (column order `timestamp,open,high,low,close,volume`), coverage per market as recorded below.
- **Daily aggregation (frozen, matches TSMOM V1/V2 pipeline discipline):** a market's daily close for UTC day `d` is the **close of the last M1 bar whose timestamp falls on `d`**; duplicate timestamps keep the last occurrence; rows with an invalid/non-numeric close are skipped and counted; the resulting daily series is sorted by date.
- **PRIMARY contemporary RV (frozen pre-registration decision):** **daily-close realized variance, identical construction to Layer A** — `RV_{a..b} = Σ r_τ²` over daily log returns `r_τ = ln(C_τ/C_{τ−1})` from the aggregated daily closes. The primary is therefore a **comparable measurement object** across eras by construction; daily-based is the definition-lock §3/§6 primary.
- **SECONDARY (contemporary only, cannot rescue, never pooled with Layer A):** intraday realized variance from M1 bars (sum of squared 1-minute log returns within the window), reported only as a Layer-B robustness diagnostic and explicitly labeled a **different-frequency object** that is NOT comparable to the daily-based Layer A measure and NOT usable for cross-era consistency claims.
- **Layer B missing-day and zero-RV policy (frozen; audit correction 12 — mirrors §12):** a UTC day `d` is **present** for a market iff ≥ 1 valid M1 bar (numeric, non-null close per the aggregation rule) has a timestamp on `d`; a day with no bars (weekend, market closure) or only invalid bars is a **missing day**. A shock day `t` is excluded unless **all 5** days of each window are present (incomplete windows are dropped, not imputed). A shock day `t` is **ineligible** if either window's `RV = 0`. Coverage-edge days (a partial first/last bar day) count as present if they contain ≥ 1 valid bar. UTC-day boundaries are fixed by the bar timestamp; no calendar interpolation.
- **M1 data fingerprints (SHA-256, computed 2026-08-13):**

  | File | SHA-256 | Bytes | First bar | Last bar |
  |---|---|---|---|---|
  | BTCUSD_M1.csv | 97b853854d8f650d80e3972f159deab0b15911e19dd437e1dd10b3bab098409b | 140,914,949 | 2021-05-23 00:00 | 2026-05-22 23:59 |
  | EURUSD_M1.csv | 5106a518e65a9d3f4c8bfc74c14fad81240a9de278bd1c4577799a6f1b79813f | 114,009,218 | 2021-01-04 00:00 | 2026-06-30 23:59 |
  | USATECHIDXUSD_M1.csv | 39f25619bd26d72f4fdaa300a5c40002e4f4d46805050526ba98ec1c0a54bfc6 | 56,818,845 | 2023-09-01 00:00 | 2026-07-10 20:14 |
  | XAGUSD_M1.csv | 69444be954a869ebc831cd1253849222d8babc7a02940b2bb908a5179bcf5999 | 87,439,262 | 2021-07-13 00:00 | 2026-07-12 23:59 |
  | XAUUSD_M1.csv | 54cf61559673adc7f6917f086bd4ef8d71808c3834f2faa82cd9323ee119311c | 104,298,565 | 2021-04-12 11:00 | 2026-04-10 20:59 |

## 14. Unit of Inference

- **Primary unit of inference: the per-market statistic** `d_m`. Class-level `D_class` is an equally-weighted signed aggregation of per-market statistics (§11). Cross-market pooled estimators are **not** used in the primary.
- Per-market and per-class results are all reported; only class-level statistics form the primary multiple-comparison family (§15).

## 15. Multiple-Comparison Family (frozen)

- **Primary family:** one class-level statistic per class per layer → **7 Layer A classes + 4 Layer B classes = 11 primary class statistics.**
- **Correction:** Holm step-down procedure across the 11-member family at family-wise `α = 0.05` (two-sided rank/p bootstrap p per family member; precedent DISC-021/TSMOM V2 gate).
- Per-market results, secondary horizons (1-day, 21-day), standardized shocks, intraday Layer-B RV, GJR/EGARCH γ, sign-bias regressions, winsorization sensitivity, and the common-window sensitivity **all live outside the primary family** and cannot rescue it if the primary fails.
- No post-hoc family expansion; any new test requires a protocol amendment.

## 16. Reproducibility Block (frozen)

- Protocol version **1.2.0** (v1.0.0 frozen 2026-08-13 + v1.1.0 outcome-blind audit-correction amendment + v1.2.0 outcome-blind null-inference amendment — §9A and Amendment Record — v1.2.0), no further amendments permitted without a documented rationale and a re-audit.
- **Bootstrap parameters (audit corrections 8/9/10):** block length `L = 11` trading days (full response-window span t−5..t+5, justified by the response DGP — §9); `B = 10,000`; master RNG seed **`20260813`**. A single master seed drives the class-level block resampling; per-market replicate statistics are deterministic functions of the resampled streams (the v1.0.0 independent per-market bootstrap, and its per-market `master_seed + n` derivation, are replaced by synchronized class-level resampling — §9).
- **Bootstrap mechanics (frozen, §9):** circular moving blocks with replacement over each class's union calendar; wrap-around (no truncation, no padding); replicate = concatenation of sampled blocks in sampling order; caliper matching (§2) and per-stratum statistics recomputed within each replicate with frozen tercile bounds; one-to-one pairing preserved within replicates; evaluable-market membership fixed at the original-data stage; missing-market days simply absent. **p-value (v1.2.0 — null-imposing, §9A — replaces the v1.1.0 formula):** two-sided null-test `p = Pr*( |D*_null| ≥ |D_obs| )` over the B null-imposed draws `D*_null` (data-level form, §9A.2; `D*_null = D* − D_obs` only where exactly equivalent, §9A.3); Monte-Carlo convention `(1 + count)/(B + 1)` with `count = #{b : |D*_null,b| ≥ |D_obs|}`. The v1.1.0 formula `p = 2 × min(Pr*(D* ≥ D_obs), Pr*(D* ≤ D_obs))` is **retired** — it measured the sampling distribution against `D_obs` and was not a null test. **CI:** percentile interval (2.5%, 97.5%) of the ordinary sampling replicate distribution (unchanged; sampling interval only, §9A.5).
- **Determinism:** matching, strata, and statistics are pure functions of the allowed datasets plus the frozen parameters; no adaptive/outcome-driven selection anywhere.
- **Software:** Python 3 with the standard library + NumPy (pandas permitted for IO); exact interpreter/library versions are recorded in the execution metadata artifact at execution time and reproduced alongside results.
- **Seeds/parameters table** (`FROZEN_PARAMS`): shock = daily log return; response = Δln RV 5-day; strata = within-market ln(RV_back) terciles; matching = within-(market,stratum) nearest-neighbour caliper on |r|, caliper 0.25·SD(|r|), greedy one-to-one, stable tie-break (|r|, timestamp), r_t = 0 excluded (§2); statistic = d_{m,s}, d_m, D_class as §11; evaluability = ≥ 30 matched pairs in all 3 strata per market, ≥ 2 evaluable markets per primary class verdict; family = 11, Holm α=0.05; bootstrap = synchronized circular calendar blocks, L = 11, B = 10,000, seed 20260813; null-test p = Pr*(|D*_null| ≥ |D_obs|), MC convention (1+count)/(B+1), data-level form (§9A).
- **Artifact set (future, at execution, all under `output/research_discovery/H01_VOLATILITY_RESPONSE_ASYMMETRY/`):** execution script (deterministic, replayable); `experiment_metadata_H01_V1.json` (hashes, versions, seeds, row counts); daily series (HPD + M1) per market; matched-pair event table; per-market statistic table; bootstrap replicate file; class-level table; `results_H01_V1.json`; scientific report. No artifact may exist before the independent read-only audit of this protocol passes.

## 17. Data-Quality Gates (frozen; any failure → STOP, no improvisation)

1. **Fingerprint gate:** SHA-256 of every input file must match §13 (M1) and the HPD front-series table below (computed 2026-08-13). Mismatch → STOP.
2. **Universe gate:** exactly the frozen market sets of §4; no market added/removed.
3. **Date-range gate:** no data beyond the recorded coverage boundaries (§13; HPD per-root periods in `FINAL_CLASSIFICATION.csv`).
4. **Duplicate gate:** M1 duplicate timestamps and HPD duplicate dates counted and reported; ambiguous duplicates → STOP.
5. **Missingness gate:** per-market daily completeness and gap summary reported; incomplete windows dropped per §12.
6. **OHLC-validity gate:** nonpositive/`bad_close`/invalid rows counted per §13 and §12.
7. **Roll-consistency gate:** HPD `sym`-change detection reviewed against `PER_MARKET_VALIDATION.csv` roll counts/n_rolls; mismatch → STOP.
8. **Aggregation gate:** M1→daily aggregation recorded and spot-verified (last-bar close rule).
9. **RV-construction gate:** Layer B primary is the daily-based measure; the intraday measure is segregated as a different-frequency secondary object. If the Layer B daily-based construction cannot be reproduced from the raw bars, STOP.
10. **Leakage gate:** no forward-looking data; windows defined strictly on past data; no future rows referenced.
11. **Continuity gate:** `continuity_ok=False` roots excluded per §4 and never re-admitted by outcome.

### HPD front-series fingerprints (SHA-256, computed 2026-08-13)

front_ad `00dc57296975e0d27aa3f11adcc6d722c36f2efb24fd8fa6b6bd704194a19477` · front_aor `10c89a597730b2ff3831ba57f8cd80aa5e9cc7d49e5f75b48c163b1ed7b6626b` · front_bp `18f08b792f48c4f54fc9dbe59e23b23c751b9d05a9a2ff8a25a1338724def3fd` · front_c `8549b37ac540dab8f61b5ccb107204d06c2b2faab0ff19f8c5252fc78cb52de8` · front_cac `3e252053bb1b07187e6db03910acb5ecc770cbc48542918f8ed1c89099dc6253` · front_cd `f2c358b4614e8e98482343ec61a0590207a29b76deafe2fe2afea5dc9411b500` · front_cl `76e97e111b654f9ecfaa9438db50d37ca38bf3919c52c36529e32e53a05eb88a` · front_cr `eae1d16c472e5e714210db9023d3502eb738e292fc379226e56e728985de787f` · front_ct `3a0dfad2bc8d8e48da561b98cd79cac208dc8a903f7155e9ad17489daec8d0e6` · front_dx `44cbad3506ac278781a75a3281d3927ac640455eda44fec85980f90504dd298f` · front_ed `f5c8621b299954f3489bdf2f46cf838f6567c996f4c97ac666263605063f27a7` · front_fc `c267c6f953073b047d853cc79bdece6f6a0287fffa2127e2faa3cecbe13b6f4f` · front_gc `a2e7e0221900134334e8a04027d672f0a74d8e8ea915042ee933c0638a78dab0` · front_hg `3d2d2ac2077db8a9326d87570bc946bbd9659564c0164da383feb8e5c15959ad` · front_ho `b0cc47318072dc313823aeabf09934f8f158236030a781e432a9b4fd64548067` · front_jo `291b412805e3c1d254849c1040aaac9ac96f55b955fddc49189fb6b81c41d3e2` · front_jy `1d9976686e679e72de379709ab60cb478a4ed61c798873fd387de09a896e44e5` · front_kc `473f5ea81dbf0349ab20e387a0b8830a62942930524b496679e2bc257412206a` · front_lh `4ced26581e9320c277416c684e6790b06e43e7104d102b2c8d301ae66b137ee1` · front_lj `d29380f7a0adb53e0bf5fd07fde11541a2bde5189126134b2d19b3b9160c32d7` · front_ll `d29380f7a0adb53e0bf5fd07fde11541a2bde5189126134b2d19b3b9160c32d7` · front_o `891b7f114095032c48d5b9330fd7f09ffe73b056177edf40f67caf542097f671` · front_pa `12de3d06c7340a6687d71c1d9970efac02f8577629ccdd3ac32f3567841a4bed` · front_pb `62b088c2dadd1e15a4f460047c6c74743e5a97458755ee2ddc7194291599e244` · front_pl `915091cd13c9e2579df97d0f9b5e02cbff20506cb6b91a5d2c466363f2578764` · front_s `6bc0d21b4239af6cf1f84013268084f57de50c14eae2cc13f47c4b9b6ccf6ae4` · front_sb `4bce201f6ee89fe23769a1ff1740b9abb7bafa2545cf77bcb6174e10203e43cd` · front_sf `6cf1b8dd2b9cf20d2a78c514f7471f9619bdfa09b4774dafd3306d17cd989df8` · front_si `892278635bb55636abd16b642e83871c381167773d689d297d96d2899fb79adc` · front_sp `09451cdb44e09a453fc40888d8f0e9ba6b8ad79a9e45a4a05128683e2f2e721b` · front_us `3df550753dac5f801b62b9c86f42fb8db32ac7a02b281719f05e418d5e3e243d` · front_w `ef53eebdc1d99f187ff61dba3fb0d0a758841c4ee9b0eedab5ea8cc6c300fbd6`

**Notice:** `front_lj.csv` and `front_ll.csv` share an identical SHA-256 — the `ll` root is a label/data duplication of the Gilt series (RESOLVED-NONUS); neither is in the primary universe (§4).

## 18. Falsification / Decision Rules per Class (frozen)

For each class `c`, based on the family-adjusted two-sided **null-test** bootstrap p-value of `D_c` (§9A/§16, v1.2.0) and the sign of `D_c` relative to the class's frozen expected direction, subject first to **evaluability** (§11; audit correction 6):

- **Evaluability gate:** a class supports a **primary** verdict only if it has **≥ 2 primary-evaluable markets** (§11). A class with 0–1 evaluable markets receives an **EVIDENCE-LIMITED / DESCRIPTIVE** label: statistics and Holm-adjusted p-values are reported (the class remains in the §15 family) but no primary verdict is assigned, and the class cannot anchor strong cross-era claims. Single-market classes are **never** treated as strong replicated evidence (audit correction 11).
- **SUPPORT** (signed classes — EQUITY_INDICES, PRECIOUS_METALS, ENERGY_CRUDE, COMMODITIES_OTHER; primary-evaluable only):
  - `D_c` is statistically reliable (Holm-adjusted two-sided p < 0.05) with sign **matching** the expected direction; AND
  - direction is consistent across the class's evaluable markets (≥ 2/3 of primary-evaluable markets show the class sign; for exactly 2 evaluable markets both must agree — the rule is **never vacuous** for a single evaluable market); AND
  - where the class exists in **both** layers (PRECIOUS_METALS, EQUITY_INDICES), the Layer A and Layer B class statistics are **both** reliable in the expected direction (sign-matched across eras). If either layer's class is EVIDENCE-LIMITED, the cross-era claim is **EVIDENCE-LIMITED**, not strong replication.
- **CONTRADICTION** (signed classes): `D_c` is statistically reliable (p < 0.05) in the **opposite** direction of the expected sign; or evaluable markets within the class disagree in sign (consistency rule violated) while the class effect is reliable.
- **INCONCLUSIVE** (signed classes): otherwise (not reliable, CI includes null, inconsistent-but-unreliable, or class not primary-evaluable — the EVIDENCE-LIMITED label then applies).
- **Two-sided classes (FX, RATES, INDEX_COMMODITY, CRYPTO) — audit correction 10: the v1.0.0 ±0.2σ symmetry bound is REMOVED. The null is zero asymmetry; NO replacement margin is invented:**
  - **SUPPORT** = reliable sign-dependent asymmetry in either direction (Holm p < 0.05) with ≥ 2/3 of evaluable markets showing the class sign (a single evaluable market → EVIDENCE-LIMITED label).
  - **CONTRADICTION** = **not defined** for two-sided classes: no equivalence margin is pre-registered, so a reliable null result is reported descriptively as "no reliable asymmetry" rather than as a formal symmetry verdict.
  - **INCONCLUSIVE** = otherwise (failure to reliably distinguish from zero; unreliable; directionally inconsistent).
- **No non-pre-registered effect-size thresholds are introduced at execution.** Significance level α = 0.05, family = §15.

## 19. Cross-Class Interpretation (frozen)

- No universal "victory" or "defeat" verdict across classes; each class is classified independently (§18).
- Overall pattern is reported descriptively as a per-class SUPPORT / CONTRADICTION / INCONCLUSIVE vector against the literature-derived priors of §4, including the possibility that some classes contradict their priors (that is a legitimate outcome, not an error).
- Classes with no prior (FX, RATES, INDEX_COMMODITY, CRYPTO) are adjudicated only on the existence of sign-dependent response, never on direction.
- If MULTIPLE classes within a single asset-class-prior family contradict their priors, that is reported as a finding, not corrected.

## 20. Economic Firewall (frozen)

- H01 is exclusively a volatility-behavior hypothesis. The primary object is a distributional response asymmetry — NOT return predictability, profit, cost, Sharpe, or trade evaluation.
- **Prohibited in this task and in the H01 execution:** profit/return metrics, cost/spread accounting, break-even analysis, short-vol/vol-timing rules, position sizing, entry/exit signals, BOE detector construction, or any promotion to runtime.
- No cost model of any kind (HPD costs are UNOBSERVED and none may be fabricated).
- `D_class` verdicts carry scientific meaning only; they imply nothing about tradability.

## 21. Secondary Analyses (pre-declared, segregated; cannot rescue primary)

1. 1-day horizon (`RV_{t+1}` vs `RV_{t−1}`) per market/class.
2. 21-day horizon (3-week windows) per market/class.
3. Standardized shock `|r_t|/σ̂_{t−1}` variants of matching.
4. Alternative response: absolute-return `E[|r_{t+h}|]` difference.
5. Layer-B-only intraday (1-minute-bar) realized variance — different-frequency object, Layer B only.
6. GJR(1,1) and EGARCH(1,1) γ diagnostics, with the mandatory §3 caveat reproduced verbatim.
7. Engle–Ng sign-bias regressions on standardized residuals (secondary literature method).
8. Winsorization sensitivity (pre-registered cap, e.g., 95th percentile of |r| within market) — labeled sensitivity, not primary.
9. Common-window (1987-01-13 → 2002-08-30) Layer A sensitivity.
None of these may redefine the primary, its family, or its verdicts.

## 22. Prohibited Methods (frozen)

- No K-means, no HMM, no DBSCAN, no PCA-based state discovery, no random forest / neural net / clustering, no un-registered regime detection. Regime structure is a **separate future hypothesis** and is not imported into H01.
- No invented thresholds beyond the frozen ones (matching caliper `0.25·SD(|r|)` §2; minimum-pair/minimum-market evaluability §11; §21 winsorization cap).
- No reuse of DISC-021 Mean-Reversion or DISC-022 TSMOM machinery, parameters, or TEST holdout.

## 23. Stopping Rules (frozen)

Execution must **STOP** (and the audit chain re-engaged) if any of the following is discovered during implementation, before any outcome is finalized:

1. The shock-matching procedure (nearest-neighbour caliper within (market, stratum)) is ambiguous for any market's data (e.g., ties cannot be broken deterministically, or the caliper cannot be computed for a stratum).
2. The RV construction differs materially between Layer A (daily) and Layer B (daily-primary) in a way not covered by §12–§13, requiring a new scientific choice not made here.
3. HPD roll-day handling is unclear for any root (e.g., `sym` missing or discontinuous in a way inconsistent with `PER_MARKET_VALIDATION.csv`).
4. The bootstrap/inference design is found insufficient to preserve within-market serial dependence for some market (e.g., block length L = 11 cannot cover persistent dependence) or the synchronized class-level resampling cannot be constructed for some class's union calendar.
5. Any market's class membership is ambiguous between frozen classes.
6. Inference or statistic selection is observed to depend on inspected outcomes (selection-after-results).
7. Any new scientific choice arises during implementation that this protocol did not anticipate (no improvisation).
8. Historical vs contemporary measurement objects become incomparable in the primary (e.g., Layer B daily-based RV cannot be constructed as equivalent to Layer A).
9. Any data-quality gate of §17 fails and the failure requires a new scientific choice rather than a documented, protocol-compliant exclusion.
10. The identical-data duplication (lj/ll) or any other unrecognized duplicate is found among the primary universe markets.

## 24. Integrity Statement

- **Outcome-blind:** no H01 effect was computed; no experiment run; no GARCH/EGARCH/GJR fitted; no clustering; no threshold optimized; no restriction imposed from any QuantForge outcome. All choices rest on the external literature (Black 1976; Christie 1982; Nelson 1991; GJR 1993; Engle–Ng 1993; Aït-Sahalia–Fan–Li 2013; Baur 2012; Lucey & Tully 2006; Demiralay & Ulusoy 2014; Chen & Mu 2021; Osei-Assibey 2014; McKenzie 2002; Kakinaka & Umeno 2022; Austin 2011 — matching-caliper methodology) and on structural data facts (frozen fingerprints, coverage boundaries, continuity flags).
- **Artifact only:** this protocol is the sole file created by this task. No scripts, datasets, models, or result files were created; none may exist until the independent read-only audit passes.
- **Firewall:** no BOE, Assembly, Deployment, tests, contracts, or governance files modified (verified via `git status`).
- **v1.2.0 (amendment integrity):** the v1.2.0 null-inference amendment was written outcome-blind; it changes ONLY the null-testing/p-value layer (§9A); no H01 effect magnitude, class ranking, CI, p-value, or observed significance was used to select the method; the v1.1 execution remains frozen as **CONFIRMATORY INFERENCE INVALID / SCIENTIFIC RESULT UNADJUDICATED** and cannot be retroactively converted into a v1.2 result.
- **Authorized next action after this artifact (v1.2.0):** an **INDEPENDENT READ-ONLY AUDIT OF H01 V1.2 INFERENCE AMENDMENT**. No re-execution may begin before that audit passes.