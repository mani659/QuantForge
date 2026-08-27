# QUANTFORGE — RESEARCH FACTORY V2
# V16 G1 CLOSURE
# DATE: 2026-08-27

## 1. V16 Cycle Summary
V16 G1 is formally COMPLETED. No candidate earned G2 promotion. The cycle successfully validated that mechanisms dependent on unobservable variables (e.g., dealer inventory) or heavily constrained exact price sequencing (e.g., exact macro level retracements) either fail the counterfactual test or yield zero observable events in the available dataset. V16 is closed with NO new components added to the register.

## 2. CAND-047 (Fixing-Window Liquidity Transfer)
- **Verdict:** INSUFFICIENT — NEGATIVE EXPECTANCY / COUNTERFACTUAL SUPERIOR
- The treatment produced explicitly negative expectancy (-43.62 bps mean net, 0% win rate). The registered counterfactual materially outperformed the treatment (-7.04 bps mean net, 57% win rate), directly contradicting the value of the constraint. Not retained.

## 3. CAND-048 (Sequential Macro-Release Dislocation)
- **Verdict:** INSUFFICIENT — ZERO EVENTS
- The exact registered condition yielded zero historical events. The strict definition (a 1% move between 08:30 and 09:30, followed by an exact touch of the 08:30 level) was overconstrained. Not retained.

## 4. CAND-049 (Cross-Market Lead-Lag Asymmetry)
- **Verdict:** INSUFFICIENT — ZERO TREATMENT EVENTS
- The treatment condition yielded zero events. The registered counterfactual yielded 704 events (+0.15 bps mean net). Not retained.

## 5. Zero-Treatment-Event Rule
**NEW GOVERNANCE DOCTRINE:** 
> Zero treatment events do NOT scientifically contradict the mechanism. They establish only that the frozen event did not occur in the tested sample.
We must not relax event definitions post-hoc just to force an outcome. An overconstrained event simply means the opportunity frequency is insufficient for empirical validation within the given dataset.

## 6. Data/Mechanism Observability Lesson
V16 relied heavily on mechanisms where the critical independent variable (institutional dealer inventory, macro consensus shift, information diffusion) was unobservable. We could only test the resulting price artifact. Future cycles (V17) must prioritize **HIGH-OBSERVABILITY, MECHANISM-SPECIFIC MARKET BEHAVIORS** where the mechanism variable is itself directly measurable (e.g., price parity, reference acceptance, observable transitions).

## 7. Existing Component Register
The register remains strictly limited to previously retained artifacts. No V16 candidates were added.
- **CAND-024:** COMPONENT-CANDIDATE — RETAINED / NOT REINTRODUCED
- **CAND-035:** COMPONENT-CANDIDATE — EVENT OPPORTUNIST
- **CAND-042:** COMPONENT-CANDIDATE — EVENT OPPORTUNIST / NOT SCIENTIFICALLY QUALIFIED

## 8. CAND-015 Protection
**CAND-015:** 7-DAY FORWARD OBSERVATION ACTIVE / PROTECTED. No inspection of incomplete results is permitted.

## 9. Next G0 Principle
V17 G0 Candidate Generation will search exclusively for: **EVENTS WHERE THE MECHANISM VARIABLE IS ITSELF OBSERVABLE.** We will avoid hypotheses requiring inference of unseen institutional flow, positioning, or dealer gamma. The candidate must feature a measurable mechanism whose presence demonstrably changes post-entry economics relative to a close counterfactual.

## 10. Integrity
All closures were executed strictly based on objective G1 results. Zero-event candidates were closed without parameter tampering or post-hoc threshold relaxation. No closed lines were rescued.
