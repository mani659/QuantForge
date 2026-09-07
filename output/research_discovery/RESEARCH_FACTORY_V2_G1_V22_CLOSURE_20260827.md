# QUANTFORGE — RESEARCH FACTORY V2
# V22 G1 CLOSURE
# DATE: 2026-08-27

## 1. V22 Summary
V22 G1 is formally COMPLETED. Zero candidates earned G2 promotion. CAND-065 (State) showed a massive but evidence-limited sweep-depth effect. CAND-066 (Alpha) failed absolute expectancy and counterfactual tests. CAND-067 (State) generated zero events. 

## 2. CAND-065 (Structural Sweep Depth Rejection State)
- **Deep Sweep N:** 27
- **Mean Net:** +10.81 bps
- **Median Net:** -1.14 bps
- **Shallow Sweep N:** 1,070
- **Mean Net:** -0.65 bps
- **Median Net:** -1.19 bps
- **Observed Difference:** Deep sweeps +11.46 bps mean advantage vs shallow sweeps.
- **Final Status:** EVIDENCE-LIMITED — NOT VALIDATED AS A STATE ARTIFACT
- **Interpretation:** The observation that sweep depth may contain meaningful downstream information is preserved. However, the observed effect is currently supported by only 27 treatment events and a non-positive median. It is not promoted to a production/filter status and will not be re-tested with modified thresholds.

## 3. CAND-066 (Fresh Sweep vs Mitigated Sweep)
- **Treatment N (Fresh):** 2,430
- **Mean Net:** -1.76 bps
- **Median Net:** -2.04 bps
- **Counterfactual N (Mitigated):** 1,823
- **Counterfactual Mean Net:** -1.55 bps
- **Counterfactual Median Net:** -2.17 bps
- **Final Status:** INSUFFICIENT — NEGATIVE EXPECTANCY / COUNTERFACTUAL SUPERIOR

## 4. CAND-067 (Cross-Session Reference Sweep State)
- **Treatment N:** 0
- **Final Status:** INSUFFICIENT — ZERO EVENT
- **Interpretation:** The exact constrained logic yielded zero events. Criteria will not be relaxed.

## 5. Sweep-Depth Observation
The +11.46 bps right-tail shift following Deep Sweeps vs Shallow Sweeps (CAND-065) is preserved as a RESEARCH OBSERVATION. It validates the hypothesis that deep sweeps trap massive volume, forcing harder liquidations, but the low N prevents it from becoming a formalized artifact.

## 6. Conditional Freshness Lesson
CAND-059 previously demonstrated that FIRST TOUCH > SUBSEQUENT TOUCH for its tested retest (bounce) object. CAND-066 demonstrated that MITIGATED SWEEP > FRESH SWEEP for its tested fade object. Therefore, a profound governance lesson is established: FRESHNESS IS NOT A UNIVERSAL POSITIVE FILTER. The economic value of Freshness is explicitly conditional on the downstream Alpha/Event being traded.

## 7. State-vs-Alpha Dependency
State Information is not universally monotonic. A state artifact (like "Freshness") cannot be declared a "good filter" in isolation. Before a state is operationally attached to another module, its interaction with that specific Alpha must be separately validated.

## 8. Existing State Artifacts
- **CAND-059:** STATE-ARTIFACT — INFORMATIONALLY SUPPORTED / NOT STANDALONE PROFITABLE

## 9. Existing Component Register
- **CAND-024:** COMPONENT-CANDIDATE — RETAINED / NOT REINTRODUCED
- **CAND-035:** COMPONENT-CANDIDATE — EVENT OPPORTUNIST
- **CAND-042:** COMPONENT-CANDIDATE — EVENT OPPORTUNIST / NOT SCIENTIFICALLY QUALIFIED

## 10. CAND-015 Protection
- **CAND-015:** 7-DAY FORWARD OBSERVATION — ACTIVE / PROTECTED. No partial results were inspected.

## 11. V23 Direction
V23 will return emphasis to NEW ALPHA/EVENT DISCOVERY. The factory must discover intrinsically profitable, independently observable events rather than searching endlessly for specialized state filters without an underlying Alpha foundation. 

## 12. Integrity
All G1 closure decisions were objective. The inverse observation on Freshness (CAND-066) was preserved as a critical research lesson on state conditionality rather than used to reverse-engineer a rescue candidate.
