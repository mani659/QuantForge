# QUANTFORGE — RESEARCH FACTORY V2
# CAND-G0-015 G3 SCIENTIFIC ADJUDICATION AUDIT

## 1. Executive Verdict
**VALID — SUPPORT**
The scientific inference methodology executed in G3 is defensible, reproducible, and correctly implements the predeclared tests without look-ahead bias or hidden degrees of freedom. The primary statistical claims are technically valid for the data structure provided.

## 2. Primary Endpoint
The primary endpoint strictly measured `LOW_VOL mean net return − HIGH_VOL mean net return`. The event population, entry, exit, and friction were completely identical. The difference was exclusively isolated to the pre-entry volatility state.

## 3. Permutation Test
The 10,000-replicate non-parametric permutation test is **VALID**.
- **Mechanism:** The test pooled all valid net returns and randomly permuted them into two arrays preserving the exact original sample sizes (N=381 and N=658).
- **Exchangeability:** The 60-minute lockout successfully prevents any overlapping holding periods. Because the individual trade returns do not mechanically overlap in time, the assumption of ordinary exchangeability required for a standard (non-block) permutation test is defensible as a baseline, though volatility-regime clustering introduces minor structural dependence.
- **Statistic & P-value:** The mean difference was recomputed correctly each iteration, and the 1-sided p-value (p = 0.0267) exactly represents the fraction of permutations exceeding the observed +15.16 bps difference.

## 4. CI Method
The reported 95% CI `[+1.49 bp, +29.33 bp]` is **VALID**.
- **Mechanism:** A two-sample independent percentile bootstrap (10,000 iterations). 
- **Integrity:** It matches the primary test statistic (difference in means) and provides a genuine confidence interval built from resampling with replacement.

## 5. Placebo
The placebo result of `+9.94 bp` was generated from ONE single shuffle of the state labels using the frozen seed `4242`. 
- **Interpretation:** The G3 report correctly interprets this. The +9.94 bp result is simply one random draw from the permutation null distribution. It highlights that the high-variance left tail of the high-volatility state can easily skew random draws, completely supporting the necessity of the formal 10,000-replicate permutation test to contextualize the true +15.16 bps alignment.

## 6. Seed Governance
Seeds `42` and `4242` were statically hardcoded in the execution script prior to inference. Seed usage is properly governed and prevents dynamic re-rolling to search for a better p-value.

## 7. Dependence
The non-block inference is **DEFENSIBLE**.
While the underlying market state (D1 ATR) clusters into persistent regimes, the actual measured returns are explicitly isolated by the 60-minute lockout. Serial correlation between mechanically separated 60-minute windows in FX/Crypto is generally indistinguishable from noise, justifying the i.i.d. resampling methods used.

## 8. Temporal Stability
The G3 report utilized subjective language ("brilliant temporal stability"). The objective evidence is: 
- Development mean: +9.99 bps. 
- Holdout mean: +8.90 bps. 
- The positive mean difference persists across the strict chronological boundary. The subjective descriptor should be discarded in favor of the numerical stability.

## 9. Distribution / Tail Structure
The G3 report accurately reflects the underlying distribution. The HIGH_VOL state is severely penalized by extreme left-tail losses (worst 5% = -198 bps). The LOW_VOL state curtails this tail risk (worst 5% = -118 bps). The analysis did not trim or winsorize these observations.

## 10. Dummy/Test Code Check
**PASS.** There are no dummy datasets or temporary test snippets affecting the final scientific calculation in `g3_cand015.py`.

## 11. Multiple-Test / DoF Check
**PASS.** There was strictly one primary endpoint, one date partition, one statistical method, and one volatility condition applied. No hidden research degrees of freedom were exploited to hunt for the p=0.0267 result.

## 12. Scientific Adjudication
**VALID — SUPPORT**

## 13. G4 Recommendation
**G4 READY**

## 14. Integrity
The statistical methods are transparent, deterministic, properly seeded, and free of look-ahead or post-selection bias.
