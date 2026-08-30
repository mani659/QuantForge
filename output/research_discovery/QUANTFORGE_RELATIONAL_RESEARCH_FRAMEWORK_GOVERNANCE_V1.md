# QUANTFORGE — RELATIONAL RESEARCH FRAMEWORK & GOVERNANCE V1
# DATE: 2026-08-30
# STATUS: GOVERNANCE FRAMEWORK ESTABLISHED
# NO EXPERIMENT / NO G2 / NO INTERACTION TESTING

---

## 1. Mission

Relational research answers whether independently researched behavioural artifacts, when occurring together, produce economically meaningful information that neither artifact demonstrates alone.

The purpose of this framework is to establish a defensible, reproducible, anti-overfitting governance architecture that allows QuantForge to progress from:

> individual behavioural discovery → conditional relationships → potentially tradeable composite Alpha

without corrupting existing evidence, reopening closed lines, mining arbitrary combinations, or contaminating future discovery.

---

## 2. Problem Statement

QuantForge has evaluated 33 candidates across V19–V29 with 0 G2 promotions. However, three objects demonstrate meaningful conditional separation (CAND-077: +1.67 bps, CAND-081: +1.23 bps, CAND-083: +4.60 bps) despite negative standalone economics.

Standalone-only discovery may be insufficient because:

1. The eventual trading system may require multiple specialized modules with contextual conditioning
2. Individual behaviours may contain complementary information that only manifests under specific conditions
3. State objects may modify the economics of downstream events
4. The research architecture must support both standalone Alpha discovery AND relational/conditional discovery

However:

> A negative standalone candidate must NEVER be automatically rescued by combination.

Relational research must prove genuine incremental information rather than manufacturing apparent profitability through selection or multiple testing.

---

## 3. Definitions

### Artifact
A repository-established research object with traceable provenance, documented mechanism, and known classification.

### State
A market condition or participant constraint that may modify the economics of downstream events. States are not themselves entry signals. Examples: CAND-077 (volatility character), CAND-081 (post-failure trapped participants), CAND-083 (accumulated rejection pressure).

### Event
An objectively defined, deterministic market occurrence. Examples: structural break, large directional move, session open.

### Condition
A contextual variable that modifies event economics. States are a subset of conditions.

### Standalone Alpha
A candidate with demonstrated positive absolute economics after realistic trading costs, valid counterfactual, and 9/9 hard gate compliance.

### Relational Hypothesis
A testable proposition that the conditional occurrence of two or more independently researched objects produces economically meaningful information beyond what either object demonstrates alone.

### Conditional Enrichment
The phenomenon where Object A's economics change materially when Object B is simultaneously present. The enrichment may be positive (improvement) or negative (deterioration).

### Incremental Information
The economically meaningful information that Object B adds beyond what Object A demonstrates independently. This is the central question of relational research.

### Interaction
A relationship where A+B produces economically different outcomes from the sum of A-alone and B-alone effects. True interaction implies non-additive effects.

### Redundancy
The situation where A and B identify essentially the same economic population. A+B produces no improvement over A alone or B alone.

### Confounding
The situation where A appears to improve B's economics, but the apparent improvement is actually driven by an unobserved third variable correlated with both A and B.

### Selection Artifact
The situation where A+B appears profitable because the combined condition is extremely selective, creating a small sample with extreme outcomes that do not generalize.

### Relational Alpha
A candidate whose economics derive primarily from the relationship between independently researched objects rather than from either object alone.

---

## 4. Admission Rules

### Which objects may enter relational research

| Class | Admission | Requirements |
|---|---|---|
| STATE REVIEW ELIGIBLE | ADMISSIBLE | Must have: (1) provenance in G1 artifact, (2) documented mechanism, (3) 9/9 gate compliance, (4) conditional delta established, (5) no numerical threshold ratified that could be optimized |
| STATE OBSERVATION | CONDITIONALLY ADMISSIBLE | Must have: (1) provenance, (2) documented mechanism, (3) acknowledged as weaker evidence than STATE REVIEW ELIGIBLE |
| STATE-ARTIFACT | ADMISSIBLE | Must have: (1) provenance, (2) documented mechanism, (3) informationally supported classification |
| Standalone Alpha (hypothetical future) | ADMISSIBLE | Must have: G2 qualification or equivalent evidence standard |
| Unexpected observations | CONDITIONALLY ADMISSIBLE | Must have: (1) provenance documented, (2) explicitly classified as exploratory, (3) governance review before admission (see §14) |
| Closed candidates | NOT ADMISSIBLE as positive inputs | May contribute negative knowledge only (see §15) |
| Protected forward candidates | NOT ADMISSIBLE | CAND-015/024/035 permanently excluded (see §16) |

### Admission criteria (all must be satisfied)

1. **Provenance exists** — the object has a documented research artifact with exact evidence
2. **Original evidence is traceable** — G0 definition, G1 results, and governance decisions are recorded
3. **Classification is known** — the object's current governance status is explicit
4. **Mechanism is documented** — the proposed economic mechanism is stated, even if unproven
5. **Data availability is established** — the object can be measured using available data
6. **Temporal semantics are defined** — when the object is known relative to the event it conditions
7. **Look-ahead status is known** — the object does not use future information
8. **Threshold provenance is known** — any numerical thresholds used in the original definition are documented and frozen
9. **Research status is known** — the object's stage in the G0/G1/G2 lifecycle is explicit
10. **Closed-line restrictions are respected** — the object is not a rescued closed candidate

---

## 5. Exclusion Rules

### Permanently excluded

- Closed candidates (CAND-071–076, CAND-078, CAND-080, CAND-082, CAND-084–088) — may NOT be used as positive relational inputs
- Protected forward candidates (CAND-015, CAND-024, CAND-035) — permanently excluded
- Any object whose original evidence was contradicted by its own G1 result

### Conditionally excluded

- Objects whose mechanism is identical or substantially similar to another object (redundancy risk)
- Objects whose conditional delta is negligible (insufficient evidence for relational value)
- Objects whose sample size is insufficient for reliable relational measurement

### Exclusion rationale

Closed candidates contribute negative knowledge: "this mechanism alone did not produce standalone economics." They do NOT contribute positive knowledge: "this mechanism will produce economics when combined with X." The distinction is critical.

---

## 6. Hypothesis Schema

Every relational hypothesis must contain:

### Inputs
Which objects are being related? What are their exact classifications and provenance?

### Temporal relationship
Does A occur before B? Simultaneously? After B? Throughout a state window?

### Causal claim
Is the hypothesis claiming causation? Conditional association? Information enrichment? The framework strongly discourages unsupported causal claims.

### Expected direction
What economic difference is expected? Which direction should the conditional delta move?

### Mechanism
Why should the relationship exist? What participant or market constraint explains the expected economic difference?

### Counterfactual
What population represents the appropriate comparison? (See §7)

### Incremental question
Does B add information beyond A? Does A add information beyond B? (See §8)

### Provenance
What is the origin of each input object? What governance decisions have been made about each?

### Registration
The hypothesis must be frozen BEFORE any relational measurement is performed.

---

## 7. Counterfactual Framework

### Counterfactual hierarchy (from strongest to weakest)

1. **Same event class, same time period, same market** — the strongest counterfactual
2. **Same event class, same market, different time period** — acceptable if no regime change
3. **Same event class, different market** — acceptable if markets are economically similar
4. **Same mechanism family, different specific event** — weaker but potentially useful
5. **Unrelated event class** — weakest, only useful for extreme comparisons

### Relational counterfactual structure

For a relational hypothesis "A + B":

| Population | Description | Purpose |
|---|---|---|
| Unconditional baseline | All events, no conditioning | Establishes base economics |
| A alone | Events where A is present, B is absent | Establishes A's standalone contribution |
| B alone | Events where B is present, A is absent | Establishes B's standalone contribution |
| A + B | Events where both A and B are present | The relational treatment |
| Neither A nor B | Events where neither is present | Establishes the floor |

The critical comparison is:

> Is A+B economically superior to max(A-alone, B-alone)?

If A+B ≈ A alone, then B adds nothing (redundancy or B-dominated).
If A+B ≈ B alone, then A adds nothing (redundancy or A-dominated).
If A+B > max(A-alone, B-alone), genuine complementarity exists.
If A+B < min(A-alone, B-alone), harmful interaction exists.

### Sample independence

Overlapping conditions affect sample independence. If A and B frequently co-occur, the A+B population may be largely a subset of A-alone or B-alone, creating correlated samples. The framework must account for this through:
- Explicit sample counts for each population
- Overlap documentation
- Independence assessment

---

## 8. Incremental Information Framework

### Central question

> Does Object B add economically meaningful information beyond what Object A demonstrates independently?

### Comparison structure

For each candidate pair (A, B):

1. Measure A-alone economics (already established by G1)
2. Measure B-alone economics (already established by G1)
3. Measure A+B economics (the relational measurement)
4. Compute incremental delta: (A+B) minus A-alone
5. Assess whether the incremental delta is:
   - Broad-based (median positive)
   - Outlier-dependent (mean positive, median negative/zero)
   - Negligible
   - Negative (harmful interaction)

### Six outcomes

| Case | A alone | B alone | A+B | Interpretation |
|---|---|---|---|---|
| 1. Genuine complementarity | Weak | Weak | Materially superior | Both contribute unique information |
| 2. A dominates | Strong | Weak | ≈ A alone | B adds nothing |
| 3. B dominates | Weak | Strong | ≈ B alone | A adds nothing |
| 4. Redundancy | Similar | Similar | ≈ A alone ≈ B alone | Same economic population |
| 5. Harmful interaction | Any | Any | Worse than one or both | Combination destroys value |
| 6. Selection artifact | Any | Any | Appears superior due to small N or extreme outliers | Not generalizable |

The framework must explicitly classify each relational finding into one of these six cases.

---

## 9. Multiple Testing Controls

### The combination explosion problem

With 3 State objects, 3 observations, 1 unexpected finding, and potentially 10+ future candidates, the number of possible combinations grows rapidly. Exhaustive combinatorial mining followed by selection of the best result is explicitly prohibited.

### Controls

1. **Hypothesis registration** — every relational hypothesis must be registered BEFORE measurement. The hypothesis must state which objects are being related, why, and what economic difference is expected.

2. **Limited predeclared relationships** — each relational milestone should test a small number (2-5) of predeclared relationships, not exhaustively test all combinations.

3. **Mechanism-based pairing** — relationships must be motivated by a plausible economic mechanism, not by statistical convenience. "These two things co-occur" is not sufficient.

4. **Provenance tracking** — every relational measurement must record which inputs were used, when the hypothesis was registered, and what the expected direction was.

5. **Research-family accounting** — the framework must track how many relational hypotheses have been tested in each family to enable multiplicity assessment.

6. **Separation between discovery and confirmation** — exploratory relational findings must be confirmed in independent data before promotion (see §10).

---

## 10. Discovery / Confirmation Separation

### Relational discovery

"Could A and B interact?"

This is the initial exploration. It uses the full historical dataset and produces a preliminary finding.

### Relational confirmation

"Does the A+B relationship survive independent confirmation?"

This uses a temporally separated or out-of-sample dataset to verify the discovery finding.

### Separation requirements

1. Discovery and confirmation must use different time periods
2. The confirmation sample must be pre-specified (not selected after seeing discovery results)
3. The confirmation must test the exact same hypothesis registered during discovery
4. If confirmation fails, the relationship is CLOSED (not rescued)
5. A discovery-stage relationship must NOT immediately become a G2 candidate

### Promotion pathway

```
Relational discovery
    ↓
Preliminary finding (exploratory)
    ↓
Hypothesis registration for confirmation
    ↓
Confirmation in independent data
    ↓
If confirmed: RELATIONAL ALPHA CANDIDATE
    ↓
G1 (adapted for relational inputs)
    ↓
G2 (if justified)
    ↓
Forward evidence
```

---

## 11. Relational Lifecycle

### State machine

```
PROPOSED
    ↓
ADMISSION REVIEW (provenance, eligibility)
    ↓
REGISTERED (hypothesis frozen)
    ↓
DISCOVERY (full-sample relational measurement)
    ↓
    ├→ CLOSED (insufficient evidence / contradicted / redundant)
    ↓
PRELIMINARY FINDING (exploratory)
    ↓
CONFIRMATION (independent sample)
    ↓
    ├→ CLOSED (confirmation failed)
    ↓
RELATIONAL ALPHA CANDIDATE
    ↓
G1 ADAPTATION (relational version of economic plausibility screen)
    ↓
    ├→ CLOSED (economics insufficient)
    ↓
G2 ELIGIBLE
    ↓
FORWARD EVIDENCE
    ↓
SYSTEM VALUE
```

### Possible final classifications

| Classification | Meaning |
|---|---|
| CLOSED | Relationship does not produce meaningful economic information |
| REDUNDANT | A and B identify the same economic population |
| CONTRADICTED | Evidence contradicts the hypothesized relationship |
| INSUFFICIENT | Evidence is suggestive but sample too small or noisy |
| INFORMATIONALLY INTERESTING | Conditional separation exists but economics insufficient |
| STATE-CONDITIONED RELATIONSHIP | A modifies B's economics under specific conditions (State) |
| RELATIONAL ALPHA CANDIDATE | Genuine incremental information confirmed in independent data |
| PROMOTION ELIGIBLE | Meets G2 requirements through relational pathway |

---

## 12. Promotion Rules

### How a relational finding enters existing Alpha governance

A relational finding does NOT bypass existing G0/G1/G2 governance. The pathway is:

1. The relational hypothesis is a new research object with its own lifecycle
2. It must pass G1 (adapted for relational inputs) — including the 9 hard validity gates
3. It must demonstrate standalone economics (not merely conditional separation)
4. It must pass G2 if justified
5. The existing economic gates remain fully operative

### G1 adaptation for relational inputs

The 9 hard validity gates apply equally to relational candidates. Additional relational gates include:
- Both input objects have documented provenance
- The hypothesis was registered before measurement
- The counterfactual is valid and discriminating
- The incremental information is genuine (not redundant or confounded)
- Confirmation in independent data has been performed
- The combination does not merely rescue a failed standalone candidate

### Absolute economics vs conditional delta

The existing distinction is preserved:
- Positive conditional delta does NOT automatically qualify a relational Alpha
- Negative absolute economics do NOT automatically disqualify a relational finding from State classification
- The same adjudication framework (ECONOMICALLY NEGATIVE / INFORMATIONALLY INTERESTING / ECONOMICALLY PROMISING / QUALIFICATION-WORTHY) applies

---

## 13. State Relationship Governance

### How CAND-077/081/083 may participate

The three governed States are admissible relational inputs subject to the admission rules in §4.

### Conceptual temporal chain (NOT TESTED — governance assessment only)

```
CAND-077: volatility character transition
    ↓
CAND-083: accumulated rejection pressure
    ↓
structural failure
    ↓
CAND-081: post-failure trapped participant state
    ↓
downstream event economics
```

This chain is a conceptual hypothesis for governance assessment only. It has NOT been tested. It has NOT been validated. It represents a possible future relational research direction.

### Governance assessment

The framework SHOULD permit future sequence hypotheses of this type because:
1. Each State object has documented provenance
2. The temporal relationship is plausible (volatility transition → rejection accumulation → structural failure → trapped state)
3. The mechanism is economically coherent
4. The hypothesis can be tested with deterministic event definitions

However:
1. The hypothesis must be formally registered before testing
2. Each component must retain its independent governance status
3. The combination must not be used to rescue any individual component
4. Confirmation in independent data must be performed

---

## 14. Unexpected Observation Governance

### CAND-088 aligned-break observation

**Provenance:** Discovered inside the counterfactual of CAND-088 (Session Sequence Asymmetry), a hypothesis that was contradicted by its own G1 result.

**Classification:** EXPLORATORY OBSERVATION — PROVISIONAL BEHAVIORAL ARTIFACT

**Provenance treatment:**
- The aligned-break result (+4.07 bps net mean, 58.3% WR, N=556) has documented provenance
- It was NOT the original hypothesis
- It was discovered during counterfactual evaluation
- It must NOT inherit CAND-088's candidate status
- It must NOT be used as a standalone Alpha
- It must NOT be automatically admitted to relational research

**Admission pathway:**
1. The observation must be formally registered as a new behavioral fact
2. A new G0 hypothesis must be generated if the observation is to be tested
3. The hypothesis must be tested under the standard G0/G1 governance
4. Only after passing G1 can it enter relational research
5. The provenance ("discovered inside a contradicted hypothesis's counterfactual") must be permanently recorded

**Why this treatment:**
- Counterfactual observations have higher false-positive risk than pre-registered hypotheses
- The observation may be a selection artifact (testing many counterfactual conditions)
- The provenance must be transparent to prevent circular reasoning

---

## 15. Closed-Line Firewall

### Preventing rescue through combinations

The framework explicitly prevents relational research from becoming a loophole for reopening closed research.

**Rule 1:** A closed candidate may NOT be used as a positive relational input.

**Rule 2:** A closed candidate may contribute negative knowledge: "this mechanism alone did not produce standalone economics."

**Rule 3:** A closed candidate's mechanism may NOT be re-tested through combination with another object.

**Rule 4:** If a closed candidate's mechanism is conceptually similar to a relational hypothesis, the relationship must be independently justified — it cannot inherit the closed candidate's evidence.

**Rule 5:** The phrase "CAND-X failed alone, therefore let's combine CAND-X with Y" is explicitly prohibited.

### Examples

| Scenario | Permitted? | Rationale |
|---|---|---|
| "CAND-084 failed, but maybe it works with CAND-077" | NO | CAND-084 is closed/redundant. CAND-077 is a governed State. Combining them would rescue CAND-084. |
| "CAND-088 was contradicted, but the aligned-break finding is interesting" | CONDITIONAL | The aligned-break observation has documented provenance but requires a NEW G0 hypothesis before testing. |
| "CAND-077 + CAND-083 might interact" | YES (governance permitting) | Both are governed State objects with documented provenance. The relationship must be independently justified. |

---

## 16. Forward Runtime Firewall

CAND-015, CAND-024, and CAND-035 remain:

> ACTIVE / PROTECTED / UNTOUCHED

Relational research must not:
- Use their forward results
- Tune around them
- Compare them
- Infer relationships from their live/demo behaviour
- Alter their runtime status
- Use them as relational inputs
- Use them as counterfactual benchmarks

Forward evidence remains a separate evidence stream.

---

## 17. Multi-Module Architecture Implications

### How the framework supports the eventual system

If no standalone Alpha achieves sufficient economics, QuantForge may pursue:

> multiple small but independently validated event modules + contextual State conditioning + regime specialization → profitable system

The relational framework supports this by:
1. Establishing which State objects modify which event economics
2. Identifying complementary behaviours that produce superior joint economics
3. Separating genuine complementarity from redundancy
4. Providing governance pathways from individual behaviours to validated composite modules

### Module architecture (conceptual only — not designed here)

| Module | Event | State Condition | Evidence Standard |
|---|---|---|---|
| Module A | Independently validated event | State-conditioned | G2-qualified |
| Module B | Different independently validated event | Different State condition | G2-qualified |
| Module C | Rare structural event | None required | G2-qualified |

Modules may coexist without requiring a single universal strategy. The relational framework determines which State objects condition which events, enabling module-level optimization without portfolio-level overfitting.

### Important distinction

Relational research (finding whether A modifies B) is different from System Assembly (deciding Module A + Module B should run together in production). Relational research belongs before final system assembly.

---

## 18. Knowledge / Relationship Registry

### Recommended schema

| Object A | Relationship | Object B | Evidence | Status | Provenance |
|---|---|---|---|---|---|
| CAND-077 | hypothesized conditioning | CAND-083 | untested | proposed | V26/V28 governance |
| CAND-083 | hypothesized pre/post relation | CAND-081 | untested | proposed | V27/V28 governance |
| aligned-break observation | conditioning | CAND-077 | untested | proposed | V29 G1 counterfactual |
| CAND-077 | State conditioning | downstream event | untested | proposed | State governance review |

### Registry requirements

1. Every proposed relationship must be registered before testing
2. Every tested relationship must record: inputs, hypothesis, counterfactual, result, classification
3. Every contradicted relationship must be recorded as CONTRADICTED
4. Every confirmed relationship must record: confirmation sample, confirmation result
5. The registry must be maintained in `research/knowledge/RELATIONSHIP_REGISTRY.md` (new file, when first relationship is registered)

---

## 19. Open Governance Questions

The following questions require future governance decisions and are NOT resolved by this framework:

### Q1: Minimum sample size for relational events
What is the minimum N for a relational finding to be considered reliable? This is a future protocol decision, not yet ratified.

### Q2: Multiplicity correction method
What statistical method should be used for multiple relational hypothesis testing? This requires a future protocol decision.

### Q3: Confirmation sample specification
How should the confirmation sample be pre-specified? Temporal split? Market split? Both?

### Q4: Relational G1 adaptation details
What specific modifications are needed to the 9 hard validity gates for relational candidates? This requires a future protocol decision.

### Q5: Relational G2 requirements
What additional evidence is required beyond standard G2 for a relational Alpha to be promoted?

### Q6: State interaction authorization
When are interaction studies between governed States authorized? What governance review is required?

### Q7: CAND-088 aligned-break hypothesis generation
Should a new G0 cycle be dedicated to testing the aligned-break observation, or should it wait for a natural discovery cycle?

### Q8: Relational research milestone scheduling
Should relational research be interleaved with discovery cycles (V30, V31, etc.) or conducted as separate milestones?

---

## 20. Recommended Next Milestone

### Primary recommendation: V30 G0

Relational research is now GOVERNED but not yet READY for execution. The framework is established, but:

1. No relational hypothesis has been formally registered
2. No confirmation protocol has been designed
3. The open governance questions (§19) require resolution before execution
4. The existing discovery pipeline (V30 G0) should continue to generate new standalone candidates

### After V30 G0/G1:

If V30 produces additional State Review Eligible objects or standalone candidates, the relational research framework becomes more valuable because there are more legitimate inputs.

### Relational research execution timing:

Relational research should begin when:
1. At least 2 objects have STATE REVIEW ELIGIBLE status AND documented conditional deltas
2. A relational hypothesis has been formally registered with pre-specified counterfactual
3. The open governance questions (§19) have been resolved
4. The owner authorizes relational experimentation

### Therefore:

> V30 G0 is the next permitted milestone.
> Relational research execution is authorized AFTER governance questions are resolved and at least 2 STATE REVIEW ELIGIBLE objects exist with documented conditional deltas (currently satisfied: CAND-077, CAND-081, CAND-083).

---

*End of Relational Research Framework & Governance V1.*
