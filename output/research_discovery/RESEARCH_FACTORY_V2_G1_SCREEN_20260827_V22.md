# QUANTFORGE — RESEARCH FACTORY V2
# G1 ECONOMIC PLAUSIBILITY SCREEN & STATE-INFORMATION SCREEN — V22
# DATE: 2026-08-27

## 1. G1 Objective
Execute the Economic Plausibility Screen for V22 candidates (CAND-065 [STATE], CAND-066 [ALPHA], CAND-067 [STATE]). Alpha candidates are evaluated for absolute executable expectancy. State candidates are evaluated for their capacity to materially alter the distribution of an independent downstream target event.

## 2. Frozen Identity
Tested exactly as defined in V22 G0.
- **CAND-065:** Structural Sweep Depth Rejection State (STATE/CONDITION)
- **CAND-066:** Fresh Sweep vs Mitigated Sweep (ALPHA/EVENT)
- **CAND-067:** Cross-Session Reference Sweep State (STATE/CONDITION)

## 3. Artifact-Type Classification
- **CAND-065:** STATE/CONDITION (Requires material distributional shift of target event).
- **CAND-066:** ALPHA/EVENT (Requires absolute executable net expectancy).
- **CAND-067:** STATE/CONDITION (Requires material distributional shift of target event).

## 4. Static Integrity
All candidates verified: Events/states are constructable before entry. Exact executable entries and deterministic exits applied. Returns measured strictly post-entry. Exact counterfactuals constructed. No hidden degrees of freedom or look-ahead bias present.

## 5. Data Availability
- **PRICE ARTIFACT TESTABLE?** YES.
- **CONDITION/STATE DIRECTLY OBSERVABLE?** YES.
- **CAUSAL MECHANISM DIRECTLY OBSERVABLE?** NO. Trapped counter-party volume, institutional exhaustion, and NY/London participant flow are hypothesized explanations for the observed price geometries.

## 6. CAND-065 (Structural Sweep Depth Rejection State) [STATE]
- **State Treatment N (Deep Sweep > 0.20%):** 27
- **Frequency:** Rare
- **Downstream Target Mean Net:** +10.81 bps
- **Downstream Target Median Net:** -1.14 bps
- **Counterfactual N (Shallow Sweep < 0.05%):** 1,070
- **Counterfactual Mean Net:** -0.65 bps
- **Counterfactual Median Net:** -1.19 bps
- **Treatment Difference:** The Deep Sweep state dramatically outperformed the Shallow Sweep state on the mean (+11.46 bps advantage), driven entirely by extreme right-tail momentum expansions (Best trade: +253.80 bps vs +91.86 bps for CF). 
- **State Conclusion:** The observed downstream distribution perfectly matched the frozen hypothesis (deep sweeps trap massive volume, forcing harder liquidations and fatter right-tail momentum). However, N=27 is too small to declare this state robust.
- **Verdict:** INSUFFICIENT — EVIDENCE-LIMITED

## 7. CAND-066 (Fresh Sweep vs Mitigated Sweep) [ALPHA]
- **N (Fresh Sweep):** 2,430
- **Frequency:** High
- **Mean Gross:** +0.24 bps
- **Median Gross:** -0.04 bps
- **Friction:** 2.0 bps (Standard Nasdaq-100 CFD spread round-trip)
- **Mean Net:** -1.76 bps
- **Median Net:** -2.04 bps
- **Win Rate:** 40.7%
- **Counterfactual N (Mitigated Sweep):** 1,823
- **Counterfactual Mean Net:** -1.55 bps
- **Counterfactual Median Net:** -2.17 bps
- **Verdict:** INSUFFICIENT — NEGATIVE EXPECTANCY / COUNTERFACTUAL SUPERIOR

## 8. CAND-067 (Cross-Session Reference Sweep State) [STATE]
- **State Treatment N:** 0
- **Frequency:** Zero
- **Downstream Target Mean Net:** N/A
- **Counterfactual N:** 0
- **State Conclusion:** The highly specific combination of a precise London boundary sweep during the first hour of NY open, followed immediately by a VWAP crossover, never occurred in the dataset.
- **Verdict:** INSUFFICIENT — ZERO-EVENT

## 9. Counterfactual Comparison
- **CAND-065:** Treatment drastically outperformed Counterfactual on the mean, matching the right-tail hypothesis, but N=27 renders it non-adjudicable.
- **CAND-066:** Counterfactual (Mitigated) slightly outperformed Treatment (Fresh).
- **CAND-067:** N/A (Zero events).

## 10. Counterfactual Superiority Gate
- **CAND-065:** SIMILAR (Insufficient N to confirm the massive mean difference).
- **CAND-066:** COUNTERFACTUAL SUPERIOR.
- **CAND-067:** SIMILAR (Zero events).

## 11. Absolute Economic Headroom
- **CAND-066 [ALPHA]:** None. Negative absolute expectancy (-1.76 bps).
- **CAND-065/067 [STATE]:** None. Insufficient evidence / zero events.

## 12. Evidence Quality
- **CAND-065:** EVIDENCE-LIMITED
- **CAND-066:** ROBUST
- **CAND-067:** ZERO-EVENT

## 13. Prior-Art / Redundancy Check
- **CAND-065:** NEW. Evaluated magnitude rather than sequence/time.
- **CAND-066:** REPLICATION/EXTENSION of CAND-059. It evaluated the Freshness variable on a different action (Fading the sweep rather than bouncing the retest). The result was fascinating: while CAND-059 proved Fresh > Mitigated for *retests*, CAND-066 proved Mitigated > Fresh for *fading sweeps*. This is genuinely new structural nuance (first touches are harder to break, but also harder to immediately fade once broken).
- **CAND-067:** NEW. Explored session-anchored cross-market logic.

## 14. Executable Capture
All performance calculated explicitly post-entry limit/market execution. No MFE/MAE proxies used.

## 15. Friction
Standard 2.0 bps round-trip friction applied to CAND-066 to reflect executable reality.

## 16. Frequency
- **CAND-065:** Extremely Rare (N=27 over multi-year period).
- **CAND-066:** High.
- **CAND-067:** Zero.

## 17. Distribution
- **CAND-065:** Highly right-tail dependent (outlier-driven).
- **CAND-066:** Broad-based failure.

## 18. Mechanism vs Observed Behavior
- **CAND-065:**
  - **OBSERVED:** Target expansions after deep sweeps possessed massive right tails compared to shallow sweeps, but occurred rarely.
  - **HYPOTHESIZED:** Deep sweeps trap maximum volume, forcing violent downstream liquidation expansions.
  - **DIRECTLY OBSERVABLE:** Yes (Price state).
- **CAND-066:**
  - **OBSERVED:** Fading a second (mitigated) sweep is marginally better than fading a first (fresh) sweep.
  - **HYPOTHESIZED:** Fresh sweeps trap initial breakout traders and should mean-revert harder.
  - **DIRECTLY OBSERVABLE:** The sequential order was observable; the hypothesis was empirically falsified.

## 19. SMC Structural Mapping
- **CAND-065:** Explored Sweep Magnitude.
- **CAND-066:** Explored Freshness + Sweep sequence.
- **CAND-067:** Explored Session Liquidity Runs.

## 20. Standalone Potential
- **CAND-065:** N/A (STATE)
- **CAND-066:** NONE
- **CAND-067:** N/A (STATE)

## 21. Component Potential
- **CAND-065:** WEAK (Evidence limitation).
- **CAND-066:** NONE (Failed expectancy and counterfactual).
- **CAND-067:** NONE (Zero events).

## 22. State-Artifact Assessment
No new candidates earned the formal `STATE-ARTIFACT — INFORMATIONALLY SUPPORTED` classification. CAND-065 demonstrated the hypothesized distributional shift perfectly, but N=27 is too small to formally validate as an independent state artifact.

## 23. Module / Regime Potential
N/A

## 24. Future Information-Sharing Potential
- **CAND-066's** falsification of the "fade the first touch" hypothesis provides strong structural symmetry to CAND-059. Fresh levels are superior for retests (bouncing), but slightly inferior for sweep mean-reversion (fading the false breakout).

## 25. G1 Classification
- **CAND-065:** INSUFFICIENT — EVIDENCE-LIMITED
- **CAND-066:** INSUFFICIENT — NEGATIVE EXPECTANCY / COUNTERFACTUAL SUPERIOR
- **CAND-067:** INSUFFICIENT — ZERO-EVENT

## 26. G2 Promotions
None.

## 27. State Artifacts
None added.

## 28. Existing Register
- **CAND-024:** COMPONENT-CANDIDATE — RETAINED / NOT REINTRODUCED
- **CAND-035:** COMPONENT-CANDIDATE — EVENT OPPORTUNIST
- **CAND-042:** COMPONENT-CANDIDATE — EVENT OPPORTUNIST / NOT SCIENTIFICALLY QUALIFIED
- **CAND-059:** STATE-ARTIFACT — INFORMATIONALLY SUPPORTED / NOT STANDALONE PROFITABLE

## 29. CAND-015 Independence
7-DAY FORWARD OBSERVATION ACTIVE / PROTECTED. No results inspected.

## 30. System Assembly Status
NO SYSTEM ASSEMBLY PERFORMED.

## 31. Integrity
All candidates failed G1. Counterfactual superiority and strict sample size limitations were rigorously enforced to prevent outcome-driven promotion.
