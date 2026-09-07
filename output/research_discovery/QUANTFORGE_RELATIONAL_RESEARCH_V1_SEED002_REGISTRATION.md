# QUANTFORGE — RELATIONAL RESEARCH V1

## Phase 1: Governance Completion + First Hypothesis Registration

### SEED-002: CAND-083 × CAND-081

**Date:** 2026-08-31
**Status:** GOVERNANCE COMPLETE — SEED-002 REGISTERED
**Experiment:** NOT EXECUTED

---

## 1. Purpose

This milestone completes the remaining governance questions for relational research and formally registers SEED-002 as the first relational hypothesis. No experiment is executed. No statistics are calculated. No thresholds are optimized.

---

## 2. Governance Questions

### Q1: Minimum Sample / Evidence Quality

**Decision:** No universal minimum N is ratified. Minimum sample requirements are evidence-quality-dependent, governed by the same holistic adjudication framework used for G1 V3. Rare relational events are not automatically rejected but must demonstrate sufficient evidence quality through the existing gate framework. The 9 hard validity gates apply to relational findings as they do to standalone candidates.

**Rationale:** A universal N threshold would be arbitrary and could reject genuinely informative rare relationships. The existing evidence-quality markers (N=3, N=10) serve as reference points, not gates.

### Q2: Confirmation Sample

**Decision:** Relational confirmation must use temporal separation. The dataset will be partitioned chronologically into:
- **Discovery sample:** Historical data up to a pre-specified cut date
- **Confirmation sample:** Data after the cut date

The confirmation sample must be pre-registered BEFORE discovery measurement. Candidate definitions must be frozen before confirmation. Overlapping event periods are handled by ensuring events in the confirmation sample do not use information from the discovery period.

**Rationale:** Temporal separation is the cleanest method for preventing information leakage and is consistent with QuantForge's existing walk-forward approach.

### Q3: Incremental Information Test

**Decision:** The required comparisons are:

| Population | Description |
|---|---|
| Baseline | All structural failures without CAND-083 precondition |
| A alone (CAND-083 without CAND-081) | Structural failures with rejection pressure but without trapped-participant state |
| B alone (CAND-081 without CAND-083) | Structural failures with trapped participants but without accumulated rejection |
| A+B (both conditions) | Structural failures preceded by rejection pressure AND exhibiting trapped-participant state |

The central question is:

> Does A+B demonstrate incremental economic information beyond max(A-alone, B-alone)?

The six outcome cases (complementarity, A-dominates, B-dominates, redundancy, harmful interaction, selection artifact) will be explicitly classified.

### Q4: Relational Counterfactual

**Decision:** The strongest conceptual counterfactual for SEED-002 is:

> CAND-081-type post-failure event WITH CAND-083 precondition

versus:

> comparable CAND-081-type post-failure event WITHOUT CAND-083 precondition

This comparison is preferable to "all events without both conditions" because it isolates the incremental information that CAND-083 adds to the CAND-081 population specifically.

### Q5: Multiple Testing Control

**Decision:** The existing governance is sufficient:
1. Hypothesis registration before measurement
2. Limited predeclared relationships (SEED-002 is the first)
3. Mechanism-based pairing (temporal pre/post structural failure chain)
4. Provenance tracking
5. Research-family accounting

No additional formal multiplicity correction is required at this stage because only one relationship is being registered.

### Q6: Rare Relational Events

**Decision:** Relational events that become rare after conditioning are not automatically rejected. They are governed by the same evidence-quality framework as standalone rare events. The rare-event principle applies: rare ≠ weak, but rare evidence must be distinguished from unstable/insufficient evidence.

### Q7: Temporal / Sequence Relationships

**Decision:** SEED-002 requires a specific temporal sequence:
- CAND-083 (accumulated rejection) MUST precede the structural failure
- CAND-081 (post-failure trapped state) MUST follow the structural failure
- No future-information leakage is permitted

The temporal relationship is: A → structural failure → B → downstream event

### Q8: Causal Language

**Decision:** Unless causal evidence exists, findings will use:
- "conditional association" or "incremental information"
- NOT "causal effect"

SEED-002 is a conditional hypothesis, not a causal proof. The mechanism is plausible but unproven.

---

## 3. Governance Decisions

All eight governance questions have been resolved. The governance framework is now COMPLETE for relational research execution.

---

## 4. Relational Definitions

| Term | Definition |
|---|---|
| Input A | CAND-083 — Pre-failure accumulated rejection pressure |
| Input B | CAND-081 — Post-failure trapped participant condition |
| Relational treatment | Structural failure preceded by CAND-083 AND exhibiting CAND-081 |
| Baseline | All structural failures without CAND-083 precondition |
| Counterfactual | CAND-081 events without CAND-083 precondition |
| Incremental question | Does CAND-083 add information beyond CAND-081 alone? |

---

## 5. Counterfactual Framework

The counterfactual for SEED-002 compares:

**Treatment:** Structural failures preceded by accumulated rejection pressure (CAND-083) that exhibit trapped-participant state (CAND-081)

**Counterfactual:** Structural failures that exhibit trapped-participant state (CAND-081) but WITHOUT accumulated rejection pressure (CAND-083)

**Why this comparison:** It isolates the incremental information that rejection-pressure accumulation adds to the post-failure trapped-participant population specifically. The comparison preserves structural-event class, market, timeframe, and execution context while removing the defining relational condition (CAND-083 precondition).

---

## 6. Incremental Information Framework

Future experiment must establish:

1. CAND-081-alone economics (already established: +1.23 bps conditional delta)
2. CAND-083-alone economics (already established: +4.60 bps conditional delta)
3. CAND-083 + CAND-081 joint economics (the relational measurement)
4. Incremental delta: (A+B) minus (A-alone or B-alone as appropriate)
5. Classification into one of six outcome cases

---

## 7. Multiple Testing Controls

Only SEED-002 is registered. No multiplicity correction is needed. Future relational milestones will be limited to 2-5 predeclared relationships per cycle.

---

## 8. Discovery vs Confirmation

**Discovery:** Full historical dataset, preliminary finding
**Confirmation:** Temporally separated sample, pre-registered before discovery
**Promotion pathway:** Discovery → Preliminary finding → Confirmation → Relational Alpha Candidate → G1 → G2

---

## 9. Rare Relational Evidence

Governed by existing evidence-quality framework. No universal N threshold. Rare relationships evaluated on mechanism quality, evidence coherence, and counterfactual validity.

---

## 10. Temporal Relationship Rules

SEED-002 temporal sequence:

```
structural area
      ↓
repeated unsuccessful acceptance attempts (CAND-083 accumulation)
      ↓
structural break / failure
      ↓
CAND-081 post-failure trapped condition
      ↓
downstream event economics
```

A must precede the structural failure. B must follow the structural failure. No future-information leakage.

---

## 11. Causal-Language Rules

SEED-002 is:

> CONDITIONAL ASSOCIATION HYPOTHESIS — NOT CAUSAL PROOF

The mechanism is plausible (accumulated rejection → more trapped participants → larger forced-exit flow) but causality is not established by this registration.

---

## 12. SEED-002 Hypothesis

**Registered hypothesis:**

> Does a structural failure preceded by the CAND-083 accumulated rejection condition produce materially different downstream economics when the CAND-081 post-failure trapped-participant condition occurs, compared with comparable structural failures lacking the CAND-083 precondition?

---

## 13. CAND-083 Definition

**Status:** STATE REVIEW ELIGIBLE — PRESERVED

**Concept:** Repeated unsuccessful attempts to establish price acceptance at a structural area may progressively increase the population of participants whose positions become vulnerable to forced exit, creating a distinct market condition when the structure ultimately fails.

**Observable:** Rejection count at structural level (20-bar high/low)

**Evidence:** N=2,318, +4.60 bps conditional delta (largest in RF history), 9/9 gates, valid counterfactual (N=316, CF=-6.93 bps)

**Threshold:** NO numerical rejection-count threshold is ratified.

---

## 14. CAND-081 Definition

**Status:** STATE REVIEW ELIGIBLE — PRESERVED

**Concept:** The presence of a trapped participant population following a failed structural break creates a specific market condition that may modify the economics of subsequent events through forced exit flow.

**Observable:** Structural level (20-bar high/low), breakout event, failure within 5 bars

**Evidence:** N=3,887, +1.23 bps mean / +2.33 bps median conditional delta, 9/9 gates, valid counterfactual (N=3,364, CF=-2.01 bps)

**Threshold:** NO numerical threshold is ratified.

---

## 15. Temporal Relationship

```
CAND-083 (accumulated rejection) → structural failure → CAND-081 (trapped state) → downstream economics
```

This is a pre/post temporal chain. CAND-083 captures the pre-failure condition. CAND-081 captures the post-failure condition. They occupy different temporal phases of the same structural failure process.

---

## 16. Economic Mechanism

The proposed mechanism:

1. Repeated rejection at a structural level accumulates participants with vulnerable positions
2. When the structural level ultimately fails, these participants are trapped
3. Forced exits from trapped positions create directional pressure
4. The combination of accumulated rejection (CAND-083) + post-failure trapping (CAND-081) may produce stronger downstream economics than either condition alone

This is a **plausible mechanism**, not a proven one.

---

## 17. Conceptual Counterfactual

**Treatment:** Structural failures with accumulated rejection pressure (CAND-083) that exhibit trapped-participant state (CAND-081)

**Counterfactual:** Structural failures with trapped-participant state (CAND-081) but WITHOUT accumulated rejection pressure (CAND-083)

**Why this comparison:** It isolates the incremental information that CAND-083 adds to the CAND-081 population. The comparison preserves structural-event class, market, timeframe, and execution context.

---

## 18. Incremental Question

The future experiment must establish:

1. Does CAND-081 behave differently when preceded by CAND-083?
2. Does CAND-083 add information beyond CAND-081 alone?
3. Does CAND-081 add information beyond CAND-083 alone?
4. Is A+B materially different from baseline?
5. Does the relationship survive costs?
6. Is the result broad-based?
7. Is the relationship economically large enough to matter?
8. Does the relationship persist out-of-sample?

---

## 19. Admission Decision

**SEED-002 IS FORMALLY REGISTERED.**

Both inputs satisfy admission criteria:
- CAND-083: STATE REVIEW ELIGIBLE, provenance documented, 9/9 gates, conditional delta established
- CAND-081: STATE REVIEW ELIGIBLE, provenance documented, 9/9 gates, conditional delta established
- Relationship: mechanism-based pairing (pre/post structural failure), temporal sequence defined, counterfactual designed
- No closed-line violations
- No forward-runtime contamination
- No threshold optimization

---

## 20. Relational Lifecycle

SEED-002 current position:

```
PROPOSED → GOVERNANCE REVIEW → ADMITTED → REGISTERED → [DISCOVERY] → [CONFIRMATION] → ...
```

Current status: **REGISTERED**

Next step: **CONTROLLED RELATIONAL DISCOVERY EXPERIMENT — SEED-002 ONLY** (requires separate owner authorization)

---

## 21. Provenance Requirements

```
Input A: CAND-083
   ↓
Source: V28 G1 artifact (TRADEABLE_EDGE_DISCOVERY_SCREENING_V28.md)
   ↓
Governance: STATE REVIEW ELIGIBLE (CAND-083 State Governance Review)
   ↓
Input B: CAND-081
   ↓
Source: V27 G1 artifact (TRADEABLE_EDGE_DISCOVERY_SCREENING_V27.md)
   ↓
Governance: STATE REVIEW ELIGIBLE (CAND-077+081 State Governance Review)
   ↓
Registered relational hypothesis: SEED-002
   ↓
Registration artifact: This document
   ↓
Future: Discovery measurement → Confirmation measurement → Final governance outcome
```

---

## 22. CAND-088 Firewall

> CAND-088 original hypothesis = CLOSED / CONTRADICTED
> Aligned-break observation = EXPLORATORY / PROVISIONAL
> NOT admitted into relational testing
> Requires new independently governed G0
> NOT used to expand SEED-002

---

## 23. Closed-Line Firewall

> SEED-002 is admissible ONLY because:
> - CAND-083 is STATE REVIEW ELIGIBLE
> - CAND-081 is STATE REVIEW ELIGIBLE
> - The relationship has a distinct pre/post mechanism
> - Governance explicitly permits relational research
>
> Closed candidates remain NEGATIVE KNOWLEDGE
> No closed candidate is used as a positive relational input

---

## 24. Forward Runtime Protection

> CAND-015: ACTIVE / PROTECTED / UNTOUCHED
> CAND-024: ACTIVE / PROTECTED / UNTOUCHED
> CAND-035: ACTIVE / PROTECTED / UNTOUCHED
>
> Forward evidence NOT used in SEED-002
> Forward performance NOT inspected
> Forward results NOT incorporated

---

## 25. State Library

| Object | Classification | Status |
|---|---|---|
| CAND-059 | STATE-ARTIFACT | PRESERVED |
| CAND-065 | STATE OBSERVATION | PRESERVED |
| CAND-069 | STATE OBSERVATION | PRESERVED |
| CAND-077 | STATE REVIEW ELIGIBLE | PRESERVED |
| CAND-079 | STATE OBSERVATION | PRESERVED |
| CAND-081 | STATE REVIEW ELIGIBLE | PRESERVED — INPUT B FOR SEED-002 |
| CAND-083 | STATE REVIEW ELIGIBLE | PRESERVED — INPUT A FOR SEED-002 |

No classification changes.

---

## 26. Future Experimental Requirements

When authorized, the SEED-002 experiment must:

1. Use frozen CAND-083 and CAND-081 definitions
2. Construct the relational treatment population (A+B)
3. Construct the counterfactual population (B without A)
4. Construct the baseline population (all structural failures)
5. Measure downstream economics for each population
6. Compute incremental deltas
7. Classify into one of six outcome cases
8. Apply the 9 hard validity gates
9. Use temporal discovery/confirmation separation
10. Document all results with full provenance

---

## 27. Integrity Check

| Check | Status |
|---|---|
| No relational experiment executed | ✓ |
| No A+B statistics calculated | ✓ |
| No thresholds optimized | ✓ |
| No State definitions changed | ✓ |
| CAND-077 remains STATE REVIEW ELIGIBLE | ✓ |
| CAND-081 remains STATE REVIEW ELIGIBLE | ✓ |
| CAND-083 remains STATE REVIEW ELIGIBLE | ✓ |
| CAND-088 remains exploratory/provisional | ✓ |
| No closed candidate reopened | ✓ |
| Forward runtime untouched | ✓ |
| SEED-002 formally registered | ✓ |
| Registration contains no fabricated evidence | ✓ |

---

## 28. Governance Decision

> **OPTION A: GOVERNANCE QUESTIONS SUFFICIENTLY RESOLVED**
>
> SEED-002 IS FORMALLY REGISTERED — NOT TESTED
>
> Next permitted task: CONTROLLED RELATIONAL DISCOVERY EXPERIMENT — SEED-002 ONLY

---

*End of Relational Research V1 — SEED-002 Registration.*
