# QUANTFORGE — H01 NULL-DISTRIBUTION METHODOLOGY DECISION V1

**Date:** 2026-08-15
**Task type:** OUTCOME-BLIND, READ-ONLY STATISTICAL-METHODOLOGY STUDY — determines the correct hypothesis-testing construction for the already-frozen H01 matched-pair statistic.
**Scope:** methodology only. NO recomputation of H01 results; NO inspection of effect magnitudes; NO new p-values; NO bootstrap/matching rerun; NO GARCH/EGARCH/GJR; NO protocol modification; NO experiment.
**Status:** COMPLETE — decision recorded in §10.
**Answer to the registered question (from the post-execution inference audit):** the registered p-value was computed against the block-resampling *sampling* distribution relative to the observed statistic, not against any *null* distribution. This artifact determines, from statistical first principles, which null construction is scientifically valid for testing H0: D_class = 0 while preserving the registered dependence structure and asset-class design.

---

## 1. Executive Verdict

### A — VALID NULL-IMPOSING METHOD IDENTIFIED

**The recommended method is the null-centered synchronized circular calendar-block bootstrap**, implemented as a data-level recentering of the matched-pair differences per (market, volatility stratum) by their observed stratum means, followed by the registered block resampling (identical blocks, seed stream, caliper matching, and statistic recomputation). Its statistic-level equivalent is the *recentered bootstrap pivot*: form null draws `D*_null = D* − D_obs` and compute the two-sided p-value as `Pr*(|D*_null| ≥ |D_obs|)`.

The method:
- tests exactly the registered null (per-class zero asymmetry of the vol-state-conditioned, magnitude-matched difference, §1 of the protocol);
- preserves the registered dependence structure **without modification**: within-market serial dependence (L = 11 blocks covering the t−5..t+5 response span), cross-market contemporaneous dependence (synchronized union-calendar resampling), and the rebuild-matching-inside-replicates design (matching is response-blind, so null replicates pair identically to sampling replicates);
- requires **no new estimators** (unlike bootstrap-t) and **no sign-exchangeability of shocks** (unlike permutation tests);
- supports both two-sided and one-sided class priors, and is compatible with the registered Holm 11-member family and the registered two-sided-p decision rules (§18).

**Rejected as primary:** (1) matched-pair sign-flip/permutation — its null is strictly stronger than H0 (joint sign-symmetry of the pair-difference vector) and it is not size-controlled under the serial dependence that overlapping 11-day windows create; (2) bootstrap-t — second-order-superior but requires a new registered standard-error estimator for a statistic that recomputes greedy matching inside replicates, adding machinery the block bootstrap does not need for first-order validity; (3) any model-based (GARCH-family) null — barred by the protocol's own §3 caveat and §22.

**This decision changes no scientific object.** The statistic, matching, calipers, terciles, strata, evaluability rules, family, horizons, universes, and layers remain frozen. Only the construction of the p-value — the defective registered step — is identified here, at the conceptual level, for a later registered v1.2 inference amendment.

---

## 2. The Frozen Object Under Test (recap, protocol v1.1.0)

The scientific claim (protocol §1): *for each market, the forward change in realized variance following a negative daily return shock differs from that following a positive daily return shock of equal absolute magnitude, after conditioning on the pre-shock realized-variance state*; null form per class: that difference is zero.

Frozen construction (protocol §2, §11):
- Shock = daily log return `r_t`; eligible shocks split into NEG/POS per (market, stratum) and matched one-to-one by nearest-neighbour caliper on `|r|` (caliper `0.25·SD(|r|)`, greedy, deterministic tie-break, reference pool = smaller pool, `r_t = 0` excluded).
- Stratum = within-market tercile of `ln(RV_{t−5..t−1})` (frozen bounds).
- Response = `ΔlnRV = ln(RV_{t+1..t+5}) − ln(RV_{t−5..t−1})`; `RV = Σ r²`.
- Per-market, per-stratum statistic `d_{m,s}` = mean over matched pairs in (m, s) of [ΔlnRV(neg) − ΔlnRV(pos)]; `d_m` = mean over the 3 strata; `D_class` = equally weighted mean over the class's primary-evaluable markets.
- Evaluability: ≥ 30 matched pairs in all 3 strata (market); ≥ 2 evaluable markets (primary class verdict; single-market classes = EVIDENCE-LIMITED/DESCRIPTIVE).
- Registered inference machinery (protocol §9, §16): synchronized class-level circular calendar-block bootstrap over each class's union calendar; block length **L = 11 trading days** (the full response span t−5..t+5, justified by the response DGP); **B = 10,000**; single master seed **20260813**; circular wrap-around blocks (no truncation, no padding); per-market replicate statistics recomputed with frozen tercile bounds and calipers, matching rebuilt inside each replicate; evaluable-market membership fixed at the original-data stage.
- Registered p-value (protocol §9.6, §16): `p = 2 × min(Pr*(D* ≥ D_obs), Pr*(D* ≤ D_obs))`. **This is the defective step** (post-execution inference audit): the bootstrap distribution D* is a sampling distribution centered at D_obs, so this quantity measures the skewness of the bootstrap distribution around D_obs and is ~1 regardless of whether the null holds; it is not a test of H0.
- Registered CI: percentile interval (2.5%, 97.5%) of the replicate distribution.
- Registered decision rules (§18): SUPPORT/CONTRADICTION keyed on **Holm-adjusted two-sided p < 0.05** (family of 11, α = 0.05) plus sign consistency; INCONCLUSIVE otherwise.

---

## 3. The Four Statistical Objects (the distinction the registered design conflated)

1. **Sampling distribution** — the distribution of the estimator D_class under the *observed* data-generating process (its actual sampling variability), centered at the true (unknown) value and estimated, under the observed DGP, at D_obs. The registered block resampling produces exactly this: D* centered at (approximately) D_obs. It answers: "how much would D_class fluctuate if the same process were re-realized?"

2. **Confidence-interval bootstrap** — a procedure that uses the sampling distribution to build intervals for the parameter (here: percentile CI). Its validity is a coverage statement about the *parameter*; it does **not** require any null hypothesis, and it is not, by itself, a hypothesis test. A valid CI does not imply that any particular p-value is valid.

3. **Null distribution** — the distribution a test statistic takes *when H0 holds*, i.e., centered at the null value (0 for D_class) and reflecting the dependence structure of the statistic under H0. It can be obtained (i) at the data level (transform the data so H0 holds, then resample — recentering, sign-flip/permutation, model-constrained resampling), or (ii) by pivoting the sampling distribution (the recentered bootstrap: D* − D_obs approximates D_class − D_true, which under H0 equals D_class), or (iii) implicitly by CI-inversion (compare the null value to the sampling distribution).

4. **Hypothesis-test p-value** — the probability, **under the null distribution**, that the statistic is at least as extreme as the observed value. It is only a p-value if the distribution it is computed against is a null distribution for the tested hypothesis.

The registered defect in one sentence: the formula `2 × min(Pr*(D* ≥ D_obs), Pr*(D* ≤ D_obs))` computes the tail of the **sampling** distribution at the **observed statistic** — it never references the null value 0 and is invariant to shifting the whole distribution by any constant. It is therefore not a p-value for H0: D_class = 0 (it has zero power against that null). The machinery that produces D* is sound; the reference point (D_obs instead of a null-centered distribution) is the error.

---

## 4. Method 1 — Matched-Pair Sign-Flip / Permutation

**Construction.** Condition on the observed matched pairs. Under H0 (no sign asymmetry), the two responses within each pair are exchangeable, so the pair difference `d_i = ΔlnRV(neg) − ΔlnRV(pos)` is symmetric about 0. Generate the null by randomly flipping the sign of each pair difference (`d_i → s_i d_i`, `s_i ∈ {±1}`, equal probability; equivalently swapping the neg/pos labels within each pair), recompute the statistic, repeat; p = tail probability of the flipped-statistic distribution at D_obs.

**Analysis across the registered dimensions.**

| Dimension | Assessment |
|---|---|
| Exact null assumed | Joint **sign-symmetry** of the pair-difference vector: `(s_1 d_1, …, s_n d_n) =d (d_1, …, d_n)` for all sign assignments. This is **strictly stronger** than H0 (zero *mean* asymmetry per stratum / D_class = 0). A process with E[d] = 0 but nonzero skewness or autocovariance does **not** satisfy it. |
| Exchangeability/symmetry requirements | Full conditional sign-symmetry of the joint law of the d-vector. Fails for serially dependent d_i. |
| Matched pairs | Operates **only on the observed pairing** (conditional on the original matching). It does not rebuild matching, so it tests the null conditional on the observed sample — a different inferential object than the registered design, whose replicates recompute matching. |
| Overlapping 11-day windows | The d_i are serially dependent (windows of adjacent shocks overlap up to ~10 lags). Per-pair sign flips randomize independently and **destroy the autocovariance of the d-process**: the permutation variance of the mean is ≈ (1/n²)Σd_i², omitting the 2ΣCov(d_i,d_j) terms. With the positive autocorrelation overlapping windows induce, the true null variance is larger → the test is **anti-conservative** (over-rejects). |
| Within-market serial dependence | Not preserved by per-pair flips. A *blocked* sign-flip (flip all pairs whose shock dates fall in one block) preserves within-block dependence but (a) makes block-boundary choice arbitrary, (b) randomizes only ~T/L units (79–1010), and (c) is dominated by the block bootstrap the design already uses. |
| Cross-market contemporaneous dependence | Per-pair flips randomize each market's pairs independently, breaking the same-date synchronization the registered design deliberately preserves. The null covariance across markets is wrong. |
| Volatility strata | Pairs are within-stratum and flips preserve stratum membership, but the null is imposed on the pooled pair set — it does not use the stratum structure as a conditioning level. |
| Unequal NEG/POS pool sizes | Irrelevant to the test (matching already balanced pools); the test conditions on the observed matched/unmatched counts. No new handling needed, but also none provided for the unmatched-shock information. |
| What it tests | Joint sign-symmetry of the observed pair differences — **not** D_class = 0 in general. Under the actual H0 (mean-zero with dependence), size is not controlled. |
| Finite-sample limitations | Exactness holds only under independence + full sign-symmetry; neither holds here. Blocked variants are only approximately valid, boundary-sensitive, and lower-power. |
| One-sided / two-sided | Both directions are mechanically available, but the validity caveats dominate; not recommendable as primary. |

**Rejected variant — response-level sign-flip.** Flipping the *response* of individual shocks (`ΔlnRV → −ΔlnRV`) before matching is **invalid** and must not be adopted: it imposes the null that the response marginal distribution is symmetric about 0, but the response process has a nonzero (volatility-drift) mean and is not sign-symmetric. Only the *pair-difference* sign-flip corresponds to the exchangeability of the two members within a matched pair.

**Verdict:** NOT valid as the primary test for this design. The dependence structure — within-market overlapping windows and cross-market synchronization — is the registered design's core feature (audit corrections 8–9) and a permutation null cannot preserve it without approximating the block bootstrap anyway.

---

## 5. Method 2 — Null-Centered Synchronized Block Bootstrap (RECOMMENDED)

**Construction (data-level form).** Let `c_{m,s}` = the observed mean of the matched-pair differences in (market m, stratum s) on the original data — a **frozen constant** (like the calipers and tercile bounds), computed on the full eligible series. Recenter every pair difference by its stratum constant: `d_i → d_i − c_{m(i),s(i)}`. Because matching is **response-blind** (uses |r|, stratum, and dates only), recentering changes nothing about the matching. Then apply the **registered** synchronized circular calendar-block resampling exactly as frozen (union calendar per class, L = 11, B = 10,000, master seed 20260813, wrap-around, matching rebuilt inside replicates with frozen calipers/terciles, evaluable-market membership fixed), computing the class statistic on the recentered pair differences. The resulting draws form the null distribution `D*_null`, centered at 0 by construction.

**Statistic-level equivalent (recentered pivot).** Since the recentering subtracts, within each replicate, (approximately) the same weighted combination of stratum means that produces D_obs, the null draw equals `D* − D_obs` up to replicate pair-count weighting. The clean implementation is: keep the registered sampling draws D* and define `D*_null = D* − D_obs`. This is the standard bootstrap hypothesis-test construction for a location statistic when resampling is not performed under the null (Davison & Hinkley 1997, §4.4; Hall & Wilson 1991).

**p-value (two-sided — matches the registered §18 rule structure):**

```
p = Pr*( |D*_null| ≥ |D_obs| )
```

i.e., the two-sided tail of the null distribution at the observed statistic; equivalently `p = Pr*( |D* − D_obs| ≥ |D_obs| )` in the pivot form. One-sided forms (if a future amendment ever adopts directional tests for signed classes — the current §18 rules use two-sided p plus sign-consistency, which the recommended method preserves): `p⁺ = Pr*(D*_null ≥ D_obs)` and `p⁻ = Pr*(D*_null ≤ D_obs)`. Monte-Carlo convention (denominator B vs B+1) is a pre-registration detail.

**Analysis across the registered dimensions.**

| Dimension | Assessment |
|---|---|
| Exact null assumed | H0: the vol-state-conditioned, magnitude-matched difference is zero **per class** (registered null, §1). The stratum-level recentering imposes the (scientifically natural, stronger) stratum-conditional symmetry; under either, D_class = 0. A response process with nonzero drift or skewness is fully preserved — the recentering removes only the sign-asymmetric component. |
| Exchangeability/symmetry requirements | **None** beyond the bootstrap consistency conditions the registered machinery already presupposes (the statistic converges to a well-defined limit; block resampling consistent for the sampling distribution). No sign-exchangeability of shocks, no symmetry of the response distribution. |
| Matched pairs | Preserved exactly: matching is response-blind, so null replicates pair identically to sampling replicates; the rebuild-matching-inside-replicates design is unchanged. |
| Overlapping 11-day windows | Preserved: L = 11 blocks are the registered treatment of the response-window overlap. The null distribution inherits the full within-window serial dependence. |
| Within-market serial dependence | Preserved by the registered block machinery; no change. |
| Cross-market contemporaneous dependence | Preserved by the synchronized union-calendar resampling; same-date shocks across markets stay together in both sampling and null replicates. |
| Volatility strata | The null is imposed at exactly the conditioning level of the hypothesis (per market × stratum), consistent with §7's confound-control structure; tercile bounds remain frozen. |
| Unequal NEG/POS pool sizes | Unchanged: matching handles pool sizes identically in null and sampling replicates; unmatched shocks remain excluded and counted. |
| What it tests | **D_class = 0** (per-class null), with the stratum-level symmetry as the imposed mechanism. Exactly the registered hypothesis. |
| Finite-sample limitations | First-order (percentile-level) validity, not second-order; accuracy limited by the block-bootstrap convergence (block count 79–1010; L fixed at the response span by registration — not revisited here); skewness of the sampling distribution can affect the recentered tail slightly; the recentering constants are estimated on the full sample (as are calipers/terciles), which is standard bootstrap practice. |
| One-sided / two-sided | Both, directly and unambiguously; the two-sided form is the one the registered §18 rules use. |

**Relationship to the registered percentile CI.** The percentile CI (2.5%, 97.5%) remains the reported interval and remains valid as a sampling interval (post-execution audit §6). The CI-inversion test ("reject iff 0 ∉ percentile CI", p = 2·min(Pr*(D* ≥ 0), Pr*(D* ≤ 0))) is the same family's CI-consistent form and is also first-order valid; the recentered pivot is preferred for hypothesis testing because it uses the pivotal absolute deviation rather than the raw, non-pivotal percentile tails (Hall & Wilson 1991). The v1.2 amendment may register either the recentered pivot or the CI-inversion form; both are null-imposing, dependence-preserving, and test the registered null. **The recommendation below registers the recentered pivot as primary.**

**Verdict:** VALID, first-order, minimal-change, dependence-preserving. **RECOMMENDED.**

---

## 6. Method 3 — Bootstrap-t / Studentized Test

**Construction.** Studentize the statistic: `t = D_class / ŝ`, where `ŝ` is a consistent standard-error estimator for D_class that accounts for within-market serial dependence and cross-market contemporaneous dependence (e.g., a block-based time-series SE or a nested block bootstrap). Bootstrap replicates `t* = (D* − D_obs)/ŝ*` with `ŝ*` recomputed inside each replicate; p from the t* distribution at the observed t.

**Analysis across the registered dimensions.**

| Dimension | Assessment |
|---|---|
| Exact null assumed | H0: D_class = 0, tested through the pivotal statistic t. |
| Exchangeability/symmetry requirements | Same bootstrap consistency conditions as Method 2; the pivotal construction is asymptotically more accurate (second-order) when the SE is consistent and the statistic is not too heavy-tailed. |
| Matched pairs | Same as Method 2, plus an SE estimator for a statistic computed via greedy matching inside replicates — a non-smooth composition that makes a clean analytic SE difficult. |
| Overlapping windows / serial / cross-market dependence | Handled by the SE choice; requires the SE to be block-robust. |
| Volatility strata / unequal pools | Same as Method 2; SE must be aggregated consistently across strata and markets. |
| What it tests | D_class = 0 via a pivotal statistic. |
| Finite-sample limitations | Needs a **new registered SE estimator** (not in the protocol — a new scientific choice); a nested bootstrap is expensive (outer B × inner b); studentization can be fragile when the response has heavy tails (extreme shocks are eligible by registration §8); the block-bootstrap's own convergence (block-length choice) may dominate the second-order gain. |
| One-sided / two-sided | Both. |

**Verdict:** VALID and theoretically superior in the second order (Hall & Wilson 1991), **but** it requires new machinery (a registered SE definition) and can be fragile for heavy-tailed re-matched statistics. It is an admissible *enhancement* for a future robustness layer, **not** the required primary fix. First-order validity of the recentered pivot (Method 2) is sufficient for the registered decision rules; the v1.2 amendment should not be burdened with a new SE estimator.

---

## 7. Other Methods Considered (brief)

- **iid (non-block) bootstrap / independent per-market bootstrap:** rejected — breaks exactly the dependence the registered L = 11 synchronized design was built to preserve (audit corrections 8–9). Not a null-distribution question; a regression of the design.
- **Parametric/model-based null (GARCH-family sign tests, sign-bias regressions):** rejected for the primary — the protocol's primary object is non-parametric (§3, §7), the mandatory §3 caveat bars GJR/EGARCH from the primary, and §22 prohibits importing GARCH machinery into the primary. They remain registered secondaries, non-rescuing.
- **Shock-level sign-relabeling permutation** (randomly reassign NEG/POS labels to shocks within (market, stratum), keep responses on their dates, rebuild matching): a cousin of Method 1. It preserves the response process's serial dependence but requires sign-process exchangeability under the null and conditions on marginal sign counts; it is only approximately valid and is dominated by the block bootstrap, which needs no such assumption. Rejected as primary.
- **Subsampling:** different rate/coverage properties and not the registered framework; mentioned only as a future robustness option, not recommended.
- **Block-permutation hybrids:** approximate, boundary-arbitrary, dominated by the block bootstrap; rejected as primary.

---

## 8. Comparative Summary

| Dimension | M1 sign-flip/permutation | M2 null-centered block bootstrap | M3 bootstrap-t |
|---|---|---|---|
| Null tested | joint sign-symmetry of pair differences (stronger than H0) | D_class = 0 (stratum-level mechanism) | D_class = 0 (pivotal) |
| Size control under overlapping-window dependence | **No** (anti-conservative; autocovariance destroyed) | Yes (first-order; L = 11 preserved) | Yes (second-order, if SE consistent) |
| Cross-market synchronization | Broken by independent flips | Preserved (synchronized blocks) | Preserved (with block-robust SE) |
| Matching rebuild in replicates | Not applicable (conditions on observed pairs) | Preserved (matching response-blind) | Preserved |
| Strata handling | Not used as conditioning level | Null imposed per (market, stratum) | Same as M2 |
| Unequal pool sizes | Conditioned on | Unchanged (matching handles) | Unchanged |
| New machinery required | None (but invalid) | **None** | New SE estimator (nested bootstrap) |
| Exactness | Exact only if independence + full symmetry (false here) | Asymptotic (first-order) | Asymptotic (second-order) |
| One/two-sided priors | Mechanically yes; validity fails | Yes, both | Yes, both |
| Verdict | **REJECTED** | **RECOMMENDED** | Admissible enhancement, not required |

---

## 9. Conceptual Definition of the Recommended Method (statistical level only — not a protocol amendment)

**Name:** Null-centered synchronized circular calendar-block bootstrap (recentered pivot form).

1. **Sampling draws (unchanged from registration):** for each class, generate the B = 10,000 block-resampled class statistics D* using the registered union-calendar circular block machinery (L = 11, master seed 20260813, matching rebuilt inside replicates with frozen calipers and terciles, evaluable-market membership fixed).
2. **Null draws (the correction):** `D*_null = D* − D_obs`. (Equivalently, at the data level: recenter every matched-pair difference by its observed (market, stratum) mean `c_{m,s}` — frozen constants — and run the identical resampling; matching is response-blind so pairing is unchanged. The two forms agree up to replicate pair-count weighting.)
3. **Null distribution:** the empirical distribution of `D*_null` over the B draws — centered at 0, inheriting the full registered dependence structure (within-market L = 11 blocks, synchronized cross-market draws).
4. **p-value (two-sided, matching §18):** `p = Pr*(|D*_null| ≥ |D_obs|)`. One-sided forms available: `Pr*(D*_null ≥ D_obs)` / `Pr*(D*_null ≤ D_obs)`.
5. **Everything else remains as registered:** statistic, matching, calipers, terciles, strata, evaluability, 11-member Holm family at α = 0.05, percentile CI as the reported interval, layers, universes, horizons.

**What the method does NOT require (explicitly):**
- no sign-exchangeability of shocks, no symmetry of the response marginal distribution (volatility drift is preserved);
- no changes to matching, strata, calipers, terciles, evaluability, family, or universe;
- no new estimators, no nested bootstrap, no GARCH-family machinery;
- no inspection of effect magnitudes (the construction is justified solely by what distribution obtains under H0).

---

## 10. Decision

### A — VALID NULL-IMPOSING METHOD IDENTIFIED

The null-centered synchronized circular calendar-block bootstrap (recentered pivot, §9) is the scientifically valid hypothesis-testing construction for the frozen H01 statistic. It tests the registered null D_class = 0, preserves the registered dependence structure exactly, requires no new estimators, and is first-order valid under the bootstrap consistency conditions the registered machinery already presupposes. The sign-flip/permutation family is rejected because its null is stronger than H0 and it is not size-controlled under the overlapping-window dependence; bootstrap-t is a valid second-order enhancement but not required for the registered decision rules.

**Boundary of this decision (anti-curve-fitting):** this artifact authorizes nothing beyond identifying the method. It does NOT amend the protocol, does NOT compute any p-value, does NOT rerun anything, and does NOT change any frozen parameter. The recentering constants (`c_{m,s}`) are a function of the data and are only defined at execution; the construction, not any number, is the object of this decision.

---

## 11. What Remains Frozen (unchanged by this decision)

- H01 scientific question, asset-class priors, expected directions (§4);
- market universes (22 HPD Layer A; 5 M1 Layer B);
- shock definition, matching algorithm, caliper, tie-break, reference-pool rule (§2);
- volatility strata and tercile construction (§7);
- response definition, RV construction, 5-day horizon (§3, §5);
- minimum-pair/minimum-market evaluability rules (§11);
- bootstrap block length L = 11, B = 10,000, master seed 20260813, synchronized circular block machinery (§9, §16);
- 11-member primary family, Holm at α = 0.05 (§15);
- percentile CI as the reported interval;
- secondary analyses and their non-rescuing status (§21);
- prohibited methods (§22) and the economic firewall (§20).

The only item this decision touches is the p-value construction, and it does so at the conceptual level only.

---

## 12. Exact Next Task

1. **Independent READ-ONLY audit of this methodology decision** — verify the null-distribution reasoning, the dependence analysis, the A/B/C classification, and the outcome-blind integrity (no p-values computed, no results inspected, no protocol modification).
2. **Separately registered H01 v1.2 inference amendment** — written outcome-blind, fixing only the inference step (§9/§16 p-value and any consequential §18 wording), pre-registering the recentered pivot construction (or the CI-inversion form, if the amendment prefers CI-consistency), the Monte-Carlo convention (B vs B+1), and the one-sided/two-sided forms, with all other frozen elements unchanged.
3. **Independent audit of the v1.2 amendment** before any re-execution.

The current H01 V1 result remains frozen and labeled as affected by the inference defect until the amendment path is completed.

---

## 13. Integrity Statement

- **Outcome-blind:** no H01 effect magnitude, CI, or p-value was used to choose the method; no result was recomputed; no new p-value was produced; no bootstrap or matching was rerun.
- **Read-only:** the only file created by this task is this artifact; no protocol, script, dataset, result, or governance file was modified.
- **Methodology grounded in primary statistical literature:** bootstrap hypothesis testing and recentering (Davison & Hinkley 1997 §4.4; Hall & Wilson 1991; Lahiri 2003; Politis, Romano & Wolf 1999), matched-pairs permutation/exchangeability theory (Lehmann & Romano 2005; Rosenbaum 2002), block bootstrap under dependence (Künsch 1989; Lahiri 2003), and the registered matching-caliper framework (Austin 2011).
- **No curve-fitting:** the method is justified by what distribution obtains under H0, never by the observed H01 results; no parameter, horizon, class, or universe is selected or re-selected here.
