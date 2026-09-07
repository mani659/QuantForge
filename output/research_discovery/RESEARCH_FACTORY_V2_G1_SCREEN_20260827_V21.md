# QUANTFORGE — RESEARCH FACTORY V2
# G1 ECONOMIC PLAUSIBILITY SCREEN & STATE-INFORMATION SCREEN — V21
# DATE: 2026-08-27

## 1. G1 Objective
Execute the Economic Plausibility Screen for V21 candidates (CAND-062 [ALPHA], CAND-063 [STATE], CAND-064 [STATE]). Alpha candidates are evaluated for absolute executable expectancy. State candidates are evaluated for their capacity to materially alter the distribution of an independent downstream target event.

## 2. Frozen Identity
Tested exactly as defined in V21 G0.
- **CAND-062:** Late-Session Trend Exhaustion Fade (ALPHA/EVENT)
- **CAND-063:** Asian Session Volatility Compression State (STATE/CONDITION)
- **CAND-064:** Structural Acceptance Time-State (STATE/CONDITION)

## 3. Artifact-Type Classification
- **CAND-062:** ALPHA/EVENT (Requires absolute executable net expectancy).
- **CAND-063:** STATE/CONDITION (Requires material distributional shift of target event).
- **CAND-064:** STATE/CONDITION (Requires material distributional shift of target event).

## 4. Static Integrity
All candidates verified: Events/states are constructable before entry. Exact executable entries and deterministic exits applied. Returns measured strictly post-entry. Exact counterfactuals constructed. No hidden degrees of freedom or look-ahead bias present.

## 5. Data Availability
- **PRICE STATE OBSERVABLE?** YES.
- **CAUSAL EXPLANATION OBSERVABLE?** NO. Institutional intent and participant transitions are hypothesized explanations for the observed price geometries.

## 6. CAND-062 (Late-Session Trend Exhaustion Fade) [ALPHA]
- **N:** 61
- **Frequency:** Low to Moderate
- **Mean Gross:** -7.73 bps
- **Median Gross:** -3.92 bps
- **Friction:** 2.0 bps (Standard Nasdaq-100 CFD spread round-trip)
- **Mean Net:** -9.73 bps
- **Median Net:** -5.92 bps
- **Win Rate:** 42.6%
- **Counterfactual Mean Net:** -2.98 bps
- **Counterfactual Median Net:** +2.71 bps
- **Verdict:** INSUFFICIENT — NEGATIVE EXPECTANCY / COUNTERFACTUAL SUPERIOR

## 7. CAND-063 (Asian Session Volatility Compression State) [STATE]
- **State Treatment N:** 2 (Target breakouts occurring after <10th pctile Asian range)
- **Frequency:** Extremely Rare
- **Downstream Target Mean Net:** -3.47 bps
- **Downstream Target Median Net:** -3.47 bps
- **Counterfactual N:** 35 (Target breakouts occurring after >50th pctile Asian range)
- **Counterfactual Mean Net:** +2.55 bps
- **Treatment Difference:** N/A (Treatment N=2 is statistically insignificant).
- **State Conclusion:** The compression state did not add measurable information because the specific combination of extreme Asian compression followed immediately by a target >0.5% breakout was too rare to adjudicate.
- **Verdict:** INSUFFICIENT — EVIDENCE-LIMITED

## 8. CAND-064 (Structural Acceptance Time-State) [STATE]
- **State Treatment N:** 2302 (Retests occurring after >=15m acceptance beyond extreme)
- **Frequency:** High
- **Downstream Target Mean Net:** -4.94 bps
- **Downstream Target Median Net:** -2.98 bps
- **Win Rate:** 35.2%
- **Counterfactual N:** 1564 (Retests occurring after 1-5m sweep beyond extreme)
- **Counterfactual Mean Net:** -0.83 bps
- **Counterfactual Median Net:** -0.72 bps
- **Counterfactual Win Rate:** 44.6%
- **Treatment Difference:** The Counterfactual (Sweep) outperformed the Treatment (Acceptance) by 4.11 bps on the mean and nearly 10% on win rate.
- **State Conclusion:** The state adds immense informational value, but directly contradicts the frozen hypothesis. Time-based "Acceptance" actively *weakens* a level for a retest compared to a brief "Sweep". However, because the frozen artifact hypothesized Acceptance > Sweep, it formally fails the counterfactual gate.
- **Verdict:** INSUFFICIENT — COUNTERFACTUAL SUPERIOR

## 9. Counterfactual Comparison
- **CAND-062:** Counterfactual (Mid-Day) outperformed Treatment (Late-Session) by 6.75 bps.
- **CAND-063:** Non-adjudicable due to N=2.
- **CAND-064:** Counterfactual (Sweep) outperformed Treatment (Acceptance) by 4.11 bps.

## 10. Counterfactual Superiority Gate
- **CAND-062:** COUNTERFACTUAL SUPERIOR.
- **CAND-063:** SIMILAR (Insufficient N to declare superiority).
- **CAND-064:** COUNTERFACTUAL SUPERIOR.

## 11. State-Information Separation
CAND-064 demonstrated a massive separation between Treatment and Counterfactual over thousands of observations, proving that time-duration beyond a level is highly predictive of retest success. A 1-5 minute breach (Sweep) is structurally safer to retest than a >=15 minute breach (Acceptance). Though the artifact failed its hypothesis, this is highly valuable empirical truth for the factory's future design logic.

## 12. Absolute Economic Headroom
- **CAND-062 [ALPHA]:** None. Negative absolute expectancy (-9.73 bps).
- **CAND-063 [STATE]:** None. Insufficient evidence.
- **CAND-064 [STATE]:** Neither the state nor the counterfactual produced positive net expectancy on the downstream event, though the counterfactual was drastically closer to profitability.

## 13. Evidence Quality
- **CAND-062:** ROBUST
- **CAND-063:** EVIDENCE-LIMITED
- **CAND-064:** ROBUST

## 14. Executable Capture
All performance calculated explicitly post-entry limit/market execution. No MFE/MAE proxies used.

## 15. Distribution
- **CAND-062:** Negative mean, negative median, win rate < 50%.
- **CAND-064:** Broad-based underperformance of Acceptance vs Sweep.

## 16. Payoff Structure
- **CAND-062:** Broad-based failure.
- **CAND-064:** Broad-based failure of the acceptance condition.

## 17. Mechanism vs Observed Behavior
- **CAND-064:**
  - **OBSERVED:** Retests following a 15m breach failed more often (35% win rate) than retests following a 1-5m breach (44% win rate).
  - **HYPOTHESIZED:** 15m breach establishes acceptance and traps capital, making the level stronger.
  - **DIRECTLY OBSERVABLE:** The time-breach was perfectly observable; the hypothesis was empirically falsified.

## 18. SMC Structural Mapping
- **CAND-064** tested **Acceptance vs Sweep**. The data definitively proved that a quick Sweep makes a level safer to retest than sustained Acceptance.

## 19. Standalone Potential
- **CAND-062:** NOT VIABLE
- **CAND-063:** N/A (STATE)
- **CAND-064:** N/A (STATE)

## 20. Component Potential
- **CAND-062:** NONE
- **CAND-063:** NONE
- **CAND-064:** NONE (Failed the counterfactual hypothesis, though the inverse is highly informative).

## 21. Module / Regime Role
N/A

## 22. Future Information-Sharing Potential
- **CAND-064:** The empirical finding that "Sweep > Acceptance for Retests" is incredibly valuable. Future Alpha modules should actively prefer to retest levels that were only briefly breached rather than levels that experienced sustained breaches.

## 23. G1 Classification
- **CAND-062:** INSUFFICIENT — NEGATIVE EXPECTANCY / COUNTERFACTUAL SUPERIOR
- **CAND-063:** INSUFFICIENT — EVIDENCE-LIMITED
- **CAND-064:** INSUFFICIENT — COUNTERFACTUAL SUPERIOR

## 24. G2 Promotions
None.

## 25. State Artifacts
None added. CAND-064 possessed strong informational separation but contradicted its frozen hypothesis, failing the strict counterfactual gate. 

## 26. Existing Register
- **CAND-024:** COMPONENT-CANDIDATE — RETAINED / NOT REINTRODUCED
- **CAND-035:** COMPONENT-CANDIDATE — EVENT OPPORTUNIST
- **CAND-042:** COMPONENT-CANDIDATE — EVENT OPPORTUNIST / NOT SCIENTIFICALLY QUALIFIED
- **CAND-059:** STATE-ARTIFACT — INFORMATIONALLY SUPPORTED / NOT STANDALONE PROFITABLE

## 27. CAND-015 Independence
7-DAY FORWARD OBSERVATION ACTIVE / PROTECTED. No results inspected.

## 28. System Assembly Status
NO SYSTEM ASSEMBLY PERFORMED.

## 29. Integrity
All candidates failed G1. The separation between Event Economics and State Information was maintained. CAND-064's counterfactual superiority definitively falsified its hypothesis without attempts to artificially rescue the condition.
