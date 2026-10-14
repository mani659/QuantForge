# TASK123 — False-Negative Audit

**Question:** Does the research pipeline reject plausible hypotheses before
a fair test?

## Finding 1: The admission gate excludes on mechanism-identity grounds
without testing the exact implementation — HIGH RISK

**Evidence:** R1 (RG-TREND-001) and R2 (RG-REVERT-001) were excluded at
admission (Task101 Q3=C) and mechanism gate (Q4=A) as **mechanism-identity
rulings**, not empirical failures. Neither was ever tested. The owner
rulings explicitly state they are "not an empirical failure" and that the
exact regression-residual implementation was "never empirically tested."

**Why this creates false-negative risk:** The §99.1 similarity test
(shared component, material distinction, same economic question, downstream
event, counterfactual, participant mechanism) is applied by **assessment**,
not by **testing**. A hypothesis that shares a surface feature with a
closed family (e.g., "reversal") can be excluded without ever determining
whether the specific implementation would have produced different results.
The regression concepts were excluded because they were judged
mechanistically equivalent to protected families — but this equivalence was
never empirically established.

**Counterargument:** The firewall exists to prevent redundant re-testing of
known-closed mechanisms. Testing every variant would be expensive. The
ruling is that the cost of a false negative (losing a genuinely distinct
idea) exceeds the cost of a false positive (wasting budget on a variant).

**Assessment:** The current process errs toward false negatives. The
exclusions are defensible as governance decisions but are **not evidence of
economic failure**. The distinction between "administrative exclusion"
(governance/resource decision) and "economic failure" (empirical result)
is systematically blurred in the ledger's failure_class taxonomy.

## Finding 2: Single-shot tests with no inferential statistics — SYSTEMATIC
POWER DEFICIT

**Evidence:** 93 of 107 evaluated rows are single-configuration
(n_configs=1, no neighborhood). 58 have UNKNOWN sample size. 85 have
UNKNOWN costs. The dominant failure class is STATISTICALLY_UNSUPPORTED (39
rows) — meaning the test could not distinguish the hypothesis from noise,
not that the hypothesis was shown to be economically non-viable.

**Why this creates false-negative risk:** A single-shot test with N=1-50
events and no statistical power analysis cannot detect a true but modest
edge. The Task-65 frontier analysis (referenced in task67) established that
the detectable region for most tested designs sits **outside** the
reliable-detection frontier — meaning most tests were underpowered by
construction, not by bad luck.

**Concrete example:** CAND-025 (macro shock void reversal) was tested with
N=157 events, mean net +1.25 pts, SD ~50 pts. The NO-GO in TASK120 was
correct per the frozen bars, but the wide confidence interval means the
mechanism cannot be declared falsified — only "not shown to be viable at
this sample size." A larger-N test (if lawful data existed) could have
resolved the question; the data limitation is the binding constraint, not
the hypothesis.

## Finding 3: Similarity exclusions without comparative testing —
UNRESOLVED

**Evidence:** EXT-054 (Connors RSI(2)) was rejected at admission as an
"indicator-level re-expression of the closed mean-reversion mechanism"
without empirical testing. The ruling was mechanism-identity, not economic.

**Assessment:** This is a governance decision, not a falsification. The
distinction is correctly recorded in the task99 record but is lost when the
ledger classifies it alongside empirically tested candidates.

## Finding 4: Cost blindness in the Lane A track — STRUCTURAL

**Evidence:** 85 of 107 evaluated Lane A rows have UNKNOWN cost treatment.
The Lane B track (13 prototypes) had explicit owner-frozen cost inputs.
The Lane A track's cost-blindness means most Lane A "economic failures"
cannot be distinguished from "would have failed under any cost assumption"
vs "would have passed at realistic costs."

## Summary classification of historical exclusions

| Category | Count | Nature |
|---|---:|---|
| Justified by direct economic evidence | ~30 | Lane B prototypes with frozen costs + Lane A with adequate N and known costs |
| Justified as governance/resource decisions, not economic failure | ~36 | NOT_EVALUATED + similarity exclusions (R1/R2, EXT-054) |
| Statistically inconclusive (underpowered) | ~55 | STATISTICALLY_UNSUPPORTED + SAMPLE_INSUFFICIENT rows with small N |
| Potentially affected by implementation/measurement defect | ~10 | DATA_FAILURE + DATA_ALIGNMENT_FAILURE + RS-404 (dividend input) |
| Insufficiently documented to adjudicate | ~12 | PARTIALLY_VERIFIED composite rows |

**Net assessment:** The pipeline has a demonstrated false-negative risk
from (a) mechanism-identity exclusions without implementation testing and
(b) systematic power deficits in single-shot designs. These are process
defects, not evidence of a fundamentally exhausted opportunity space.
