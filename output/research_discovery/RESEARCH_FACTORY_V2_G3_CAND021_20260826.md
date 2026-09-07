# QuantForge — Research Factory V2
# CAND-021 G3 SCIENTIFIC VALIDATION
# 2026-08-26

## 1. G3 Objective
Determine whether the observed conditional post-entry effect (Pre-entry D1 Volatility State isolating a favorable mean-reversion regime) is scientifically distinguishable from the null hypothesis of exchangeable state assignments.

## 2. Frozen Identity
**PASS.**
The exact frozen CAND-021 event definition, entry mechanics, 60-minute deterministic exit, and 2.0-point friction were strictly used without modification, filtering, or risk controls.

## 3. Primary Hypothesis
The pre-entry D1 volatility state meaningfully alters the post-entry response to the pre-auction liquidity vacuum event, with the FAVORABLE state yielding a higher mean net return than the ADVERSE state.

## 4. Null Hypothesis
Under the null, the assignment of the observed pre-entry volatility-state labels (FAVORABLE / ADVERSE) is exchangeable with respect to the post-entry returns, subject to the independence structure of the daily events.

## 5. Dependence Analysis
Because events are limited to a maximum of one per day and the exit is bounded to exactly 60 minutes, there are no overlapping trades. However, daily volatility regimes cluster. Since the scientific question specifically tests the difference between the regime labels, a standard label permutation test (shuffling the FAV/ADV labels across the fixed set of realized daily returns) is the appropriate inference method to construct the null distribution.

## 6. Primary Statistic
- **Total Events:** 381
- **Favorable (Low Volatility) N:** 317 | Mean Net: +2.25 points
- **Adverse (High Volatility) N:** 64 | Mean Net: +4.34 points
- **Primary Statistic (FAV - ADV Difference):** -2.09 points

**Analysis:** The observed difference is actually *negative*. The ADVERSE state produced a higher mean net return than the FAVORABLE state, which directly opposes the primary hypothesis.

## 7. Confidence Interval
- **Method:** 10,000 Bootstrapped Resamples (Seed: 42)
- **95% CI for Difference:** [-38.90 points, +35.17 points]
**Analysis:** The confidence interval is extremely wide (spanning nearly 74 points), confirming that the severe variance caused by the unhedged left tail completely overwhelms any conditional signal from the pre-entry state. 

## 8. Formal Test
- **Test Type:** Label Permutation Test
- **Replicates:** 10,000 (Seed: 42)
- **Two-Sided p-value:** 0.8991
- **One-Sided p-value:** 0.5531

## 9. Permutation / Placebo
When the volatility state labels were randomly shuffled, the resulting difference distributions easily engulfed the observed -2.09 difference. The observed alignment is utterly indistinguishable from a randomized state assignment.

## 10. Temporal Robustness
- **Development Difference (FAV - ADV):** -4.15 points (FAV: 1.56, ADV: 5.71)
- **Holdout Difference (FAV - ADV):** +3.61 points (FAV: 3.84, ADV: 0.23)
**Analysis:** The effect does not even have consistent sign stability across time. The "favorable" state was worse in development and marginally better in holdout, purely due to the random clustering of severe macro shocks.

## 11. Tail Robustness
G3 strictly retained all observations, including the extreme left-tail macro shocks. The presence of these outliers drives the massive standard deviation and results in the wide confidence intervals. Removing them would artificially manufacture a significant p-value but would violate the frozen object definition and ignore the economic reality of the unhedged strategy.

## 12. Multiple Testing
Only a single, predeclared primary hypothesis test was conducted on the single defined endpoint. No p-hacking or multiple testing occurred.

## 13. Scientific Classification
**CONTRADICTED**
The hypothesis that the pre-entry D1 volatility state meaningfully isolates a more profitable regime is scientifically contradicted by the registered statistical test (p = 0.8991). The observed difference (-2.09) is fully explained by chance (statistical noise). The underlying phenomenon simply has a weakly positive expected value (+2.60 mean net) across all events indiscriminately, and the proposed G0 state condition adds zero statistically significant predictive value.

## 14. G4 Readiness
G4 is **NOT EXECUTED**. 
The scientific effect is contradicted. The object must be returned to G0.

## 15. Integrity
All assertions verified before inference. No hidden parameters, filtering, state leakage, endpoint changes, or date-range optimization were employed. G3 was executed precisely as defined.
