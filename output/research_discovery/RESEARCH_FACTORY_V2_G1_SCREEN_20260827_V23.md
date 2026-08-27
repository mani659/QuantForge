# QUANTFORGE — RESEARCH FACTORY V2
# G1 ECONOMIC PLAUSIBILITY SCREEN — V23
# DATE: 2026-08-27

## 1. G1 Objective
Execute the Economic Plausibility Screen for V23 Alpha candidates (CAND-068, CAND-069, CAND-070). Evaluate absolute executable expectancy, counterfactual superiority, and evidence frequency without adding SMC filters or post-hoc conditions.

## 2. Frozen Identity
Tested exactly as defined in V23 G0.
- **CAND-068:** Post-Shock Absorption Reversal (ALPHA/EVENT)
- **CAND-069:** NY Mid-Session Reversal Anchor (ALPHA/EVENT)
- **CAND-070:** Sustained Momentum Micro-Structure Failure (ALPHA/EVENT)

## 3. Artifact-Type Classification
All candidates are ALPHA/EVENTS, requiring absolute executable net expectancy and counterfactual outperformance.

## 4. Static Integrity
All candidates verified: Events are fully constructable before entry. Exact executable entries and deterministic exits applied. Returns measured strictly post-entry. Exact counterfactuals constructed. No hidden degrees of freedom or look-ahead bias present.

## 5. Data Availability
- **PRICE ARTIFACT TESTABLE?** YES.
- **CONDITION/STATE DIRECTLY OBSERVABLE?** YES.
- **CAUSAL MECHANISM DIRECTLY OBSERVABLE?** NO. Stop runs, macro news shocks, and session liquidity pools are hypothesized explanations for the observed price geometries.

## 6. CAND-068 (Post-Shock Absorption Reversal)
- **N (3 Inside Bars):** 7
- **Frequency:** Extremely Rare
- **Mean Gross:** -4.62 bps
- **Median Gross:** +1.38 bps
- **Friction:** 2.0 bps
- **Mean Net:** -6.62 bps
- **Median Net:** -0.62 bps
- **Win Rate:** 28.6%
- **Counterfactual N (Immediate Fade):** 1,463
- **Counterfactual Mean Net:** -1.54 bps
- **Counterfactual Median Net:** -1.23 bps
- **Treatment Difference:** The 3-inside-bar absorption pattern after a massive 5x shock is far too rare (N=7). Fading those 7 events performed worse than immediate fading.
- **Verdict:** INSUFFICIENT — EVIDENCE-LIMITED / NEGATIVE EXPECTANCY

## 7. CAND-069 (NY Mid-Session Reversal Anchor)
- **N (Mid-Day 11:30-12:30 Anchor):** 612
- **Frequency:** Moderate
- **Mean Gross:** +2.75 bps
- **Median Gross:** +2.01 bps
- **Friction:** 2.0 bps
- **Mean Net:** +0.75 bps
- **Median Net:** +0.01 bps
- **Win Rate:** 50.0%
- **Counterfactual N (Morning 09:30-10:30 Anchor):** 458
- **Counterfactual Mean Net:** -0.51 bps
- **Counterfactual Median Net:** +1.35 bps
- **Treatment Difference:** Mid-day anchor fades outperformed morning anchor fades on the mean (+0.75 bps vs -0.51 bps).
- **Verdict:** INSUFFICIENT — NEGATIVE/INSUFFICIENT EXPECTANCY (Fails to clear the >5 bps absolute headroom required for Alpha validation).

## 8. CAND-070 (Sustained Momentum Micro-Structure Failure)
- **N (High Momentum > 0.5%):** 58
- **Frequency:** Low but plausible
- **Mean Gross:** -5.19 bps
- **Median Gross:** -1.38 bps
- **Friction:** 2.0 bps
- **Mean Net:** -7.19 bps
- **Median Net:** -3.38 bps
- **Win Rate:** 34.5%
- **Counterfactual N (Chop < 0.2%):** 996
- **Counterfactual Mean Net:** -2.64 bps
- **Counterfactual Median Net:** -1.95 bps
- **Treatment Difference:** Counterfactual significantly outperformed Treatment.
- **Verdict:** INSUFFICIENT — NEGATIVE EXPECTANCY / COUNTERFACTUAL SUPERIOR (Hypothesis Falsified).

## 9. Counterfactual Comparison
- **CAND-068:** Counterfactual (Immediate Fade) outperformed Treatment on the mean, though N=7 makes it statistically void.
- **CAND-069:** Treatment outperformed Counterfactual on the mean, but absolute expectancy was negligible.
- **CAND-070:** Counterfactual (Chop) outperformed Treatment (High Momentum). Fading structure breaks in a runaway trend performs *worse* than fading them in chop.

## 10. Counterfactual Superiority Gate
- **CAND-068:** COUNTERFACTUAL SUPERIOR (Evidence-Limited).
- **CAND-069:** TREATMENT SUPERIOR.
- **CAND-070:** COUNTERFACTUAL SUPERIOR.

## 11. Absolute Economic Headroom
None.
- **CAND-068:** Negative.
- **CAND-069:** +0.75 bps net is insufficient to pass as a standalone Alpha (failed to clear >5 bps minimum requirement).
- **CAND-070:** Negative.

## 12. Evidence Quality
- **CAND-068:** EVIDENCE-LIMITED
- **CAND-069:** ROBUST
- **CAND-070:** ROBUST

## 13. Prior-Art / Redundancy Check
- **CAND-068:** NEW.
- **CAND-069:** NEW. Explored mid-day session geometry vs morning geometry.
- **CAND-070:** NEW. Explored microstructure failure (MSS) purely mapped to preceding momentum.

## 14. Executable Capture
All performance calculated explicitly post-entry execution. No MFE/MAE proxies used. Deterministic 15-minute / time-of-day exits applied.

## 15. Friction
Standard 2.0 bps round-trip friction applied to all candidates to reflect executable reality.

## 16. Frequency
- **CAND-068:** Extremely Rare (N=7).
- **CAND-069:** Moderate (N=612).
- **CAND-070:** Low but plausible (N=58).

## 17. Distribution
- **CAND-068:** Evidence-limited.
- **CAND-069:** Broad-based, highly balanced win-rate (50.0%) and symmetric win/loss averages (+50.52 bps / -49.03 bps) creating flat expectancy.
- **CAND-070:** Broad-based failure.

## 18. Mechanism vs Observed Behavior
- **CAND-068:**
  - **OBSERVED:** 3 inside bars after a massive shock almost never occurs (N=7).
  - **HYPOTHESIZED:** Shock absorption creates mean-reversion vacuum.
  - **DIRECTLY OBSERVABLE:** Yes (Price state).
- **CAND-069:**
  - **OBSERVED:** Fading mid-day anchors is marginally better than morning anchors, but produces ~0 bps net edge.
  - **HYPOTHESIZED:** Mid-day anchors are vulnerable to early afternoon trap liquidity sweeps.
  - **DIRECTLY OBSERVABLE:** Yes.
- **CAND-070:**
  - **OBSERVED:** Fading the very first structure break in an overheated trend loses heavily (-7.19 bps net) and performs worse than in chop.
  - **HYPOTHESIZED:** First break triggers stop cascade.
  - **DIRECTLY OBSERVABLE:** The failure is observable; the hypothesis is empirically falsified. (The trend likely just resumes and crushes the early counter-trend entry).

## 19. SMC Structural Mapping
- **CAND-068:** N/A
- **CAND-069:** Session Liquidity Sweep.
- **CAND-070:** Micro Market Structure Shift (MSS).

## 20. Standalone Potential
- **CAND-068:** NONE
- **CAND-069:** NONE
- **CAND-070:** NONE

## 21. Component Potential
- **CAND-068:** NONE
- **CAND-069:** WEAK (Insufficient expectancy).
- **CAND-070:** NONE

## 22. State-Artifact Assessment
N/A (No State candidates in V23).

## 23. Module / Regime Potential
N/A

## 24. Future Information-Sharing Potential
- **CAND-070's** falsification provides an excellent microstructure lesson: **Do not fade the first micro-structure break in an overheated trend.** The trend is vastly more likely to resume and stop out the mean-reversion trade. Structure breaks are "safer" to fade in low-momentum chop.

## 25. G1 Classification
- **CAND-068:** INSUFFICIENT — EVIDENCE-LIMITED / NEGATIVE EXPECTANCY
- **CAND-069:** INSUFFICIENT — NEGATIVE/INSUFFICIENT EXPECTANCY
- **CAND-070:** INSUFFICIENT — NEGATIVE EXPECTANCY / COUNTERFACTUAL SUPERIOR

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
All candidates failed G1. The rigid requirement for intrinsic absolute positive expectancy > 5 bps correctly killed CAND-069, despite its slight mathematical superiority over its counterfactual, preventing the promotion of statistically flat noise.
