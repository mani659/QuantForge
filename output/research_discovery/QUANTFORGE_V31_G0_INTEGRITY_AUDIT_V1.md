# QUANTFORGE — V31 G0 INTEGRITY AUDIT

**Date:** 2026-08-31
**Status:** COMPLETE

---

## 1. Purpose

Determine whether V31 G0 candidates genuinely satisfy NEW DISCOVERY ONLY under the complete cross-research knowledge base.

## 2. Authoritative Sources

- V31 G0: `TRADEABLE_EDGE_DISCOVERY_SCREENING_V31.md`
- V28 G0: `TRADEABLE_EDGE_DISCOVERY_SCREENING_V28.md` (CAND-085 definition)
- V29 G0: `TRADEABLE_EDGE_DISCOVERY_SCREENING_V29.md` (CAND-088 definition)
- Cross-Research Integration: `QUANTFORGE_CROSS_RESEARCH_KNOWLEDGE_INTEGRATION_V1.md`
- Unified Knowledge Ledger: `QUANTFORGE_UNIFIED_RESEARCH_KNOWLEDGE_LEDGER_V1.md`
- Candidate Ledger: `QUANTFORGE_RESEARCH_CANDIDATE_LEDGER_V1.csv`
- Negative Knowledge Ledger: `QUANTFORGE_NEGATIVE_KNOWLEDGE_LEDGER_V1.csv`

---

## 3. V31 G0 Original Candidate Claims

| ID | Name | Mechanism Family | Claimed Status |
|---|---|---|---|
| CAND-092 | Event-Information Decay | Information Persistence Dynamics | NEW |
| CAND-093 | Price-Discovery Friction Gradient | Microstructure Information Dynamics | NEW |
| CAND-094 | Path-Dependent Event Severity | Event-Path Dynamics | NEW |

---

## 4. CAND-092 Prior-Art Audit

### 4.1 Research Question

> Does the information content of a prior structural event decay over time, changing the downstream response to subsequent events?

### 4.2 Economic Mechanism

Time since prior event → information absorption stage → market sensitivity to catalysts → different downstream economics.

### 4.3 Observable

Time since last structural event, event magnitude, post-event price trajectory.

### 4.4 Temporal Structure

Inter-event: measures the TIME GAP between successive structural events.

### 4.5 Relevant Prior Art

| Prior | Concept | Overlap? | Assessment |
|---|---|---|---|
| CAND-077 | Volatility character transition | NO | Regime-level vs event-level time decay |
| CAND-081 | Structural failure trap | NO | Post-break state vs inter-event decay |
| CAND-083 | Rejection accumulation | NO | Rejection count vs time decay |
| CAND-085 | Approach velocity | NO | Approach dynamics vs information decay |
| CAND-088 | Session sequence | NO | Opening bias vs inter-event timing |
| CAND-089 | Acceptance velocity decay | NO | Velocity at levels vs information persistence |
| APEX HIGH_VOL | Volatility persistence | NO | Regime-level vs event-level |
| APEX V04/V05 | Predicted persistence → RV/excursion | NO | Regime-level persistence, not event-info decay |

### 4.6 Exact Distinction

No prior candidate measures time-since-event as a conditioning variable for downstream event economics. Existing candidates test event detection, event conditioning, or regime persistence — but not the temporal decay of event information.

### 4.7 Classification

> **A — NEW**

### 4.8 Decision

> **ELIGIBLE FOR G1**

---

## 5. CAND-093 Prior-Art Audit

### 5.1 Research Question

> Does the smoothness of price approach to a structural level reflect market consensus and affect break economics?

### 5.2 Economic Mechanism

Approach smoothness → market consensus → break conviction → directional displacement.

### 5.3 Observable

Return volatility during approach, directional consistency, oscillation count.

### 5.4 Temporal Structure

Intra-event: measures the CHARACTER of the approach trajectory to the level.

### 5.5 CAND-085 Comparison

```
Prior mechanism (CAND-085):
Approach VELOCITY (speed of price movement toward level) determines
post-breakout continuation. High velocity → trapped participants →
continuation.

V31 proposed mechanism (CAND-093):
Approach SMOOTHNESS (noise/friction during approach) determines
break economics. Smooth approach → consensus → larger break.

Shared component:
Both measure the CHARACTER of how price reaches a structural level.

Material distinction:
CAND-085 measures SPEED (how fast). CAND-093 measures SMOOTHNESS
(how noisy). These are different observables with different
economic interpretations:
- Speed → trapped participants (those who couldn't exit in time)
- Smoothness → market consensus (clarity about level significance)

Same economic question?
NO — CAND-085 asks "does speed trap participants?"
     CAND-093 asks "does smoothness reflect consensus?"

Same downstream event?
YES — both are structural level breaks.

Same counterfactual?
NO — CAND-085: high vs low velocity (CF was invalid — zero events)
     CAND-093: smooth vs choppy approach (CF should be valid)

Same participant mechanism?
NO — CAND-085: forced exits from trapped slow participants
     CAND-093: conviction from consensus clarity

Final classification:
NEW operationalization with different economic mechanism.
CAND-085 FAILED due to invalid counterfactual (zero events),
not due to mechanism failure. CAND-093 uses a different observable
that should produce valid counterfactuals.
```

### 5.6 CAND-089 Comparison

```
Prior mechanism (CAND-089):
Acceptance velocity DECAY at structural levels — range convergence
trajectory over multiple tests. CLOSED: no incremental information.

V31 proposed mechanism (CAND-093):
Approach smoothness at structural level — local noise during
approach trajectory.

Shared component:
Both measure dynamics at structural levels.

Material distinction:
CAND-089 measures CHANGE in velocity across multiple tests (decay).
CAND-093 measures NOISE during a single approach (smoothness).
CAND-089 is inter-test (across multiple level interactions).
CAND-093 is intra-event (during one approach).

Same economic question?
NO — decay vs smoothness

Same participant mechanism?
NO — velocity decline vs consensus clarity

Final classification:
DISTINCT
```

### 5.7 CAND-083 Comparison

```
Prior mechanism (CAND-083):
Cumulative REJECTION COUNT at structural levels. 3+ rejections =
treatment. STATE REVIEW ELIGIBLE.

V31 proposed mechanism (CAND-093):
Approach SMOOTHNESS — noise during approach to level.

Shared component:
Both characterize the interaction between price and structural levels.

Material distinction:
CAND-083 counts HOW MANY TIMES the level held (quantity).
CAND-093 measures HOW PRICE BEHAVED during approach (quality).
A level can have many rejections with smooth approaches, or few
rejections with choppy approaches. Different observables.

Same economic question?
NO — rejection count vs approach quality

Final classification:
DISTINCT
```

### 5.8 CAND-081 Comparison

```
Prior mechanism (CAND-081):
POST-FAILURE trapped participant state. STATE REVIEW ELIGIBLE.

V31 proposed mechanism (CAND-093):
PRE-BREAK approach quality.

Shared component:
Both involve structural level interactions.

Material distinction:
CAND-081 is POST-break (what happens after failure).
CAND-093 is PRE-break (what happened during approach).
Different temporal phase, different mechanism.

Same economic question?
NO — post-failure state vs pre-break approach quality

Final classification:
DISTINCT
```

### 5.9 APEX/SMC Comparison

No APEX or SMC research tests approach smoothness as a conditioning variable for structural breaks. APEX session-transition research tests distributional differences, not approach microstructure.

### 5.10 Exact Distinction

CAND-093 measures the LOCAL noise character of price approach to a structural level. This is distinct from:
- CAND-085 (speed, not smoothness)
- CAND-089 (velocity decay across tests, not single-approach noise)
- CAND-083 (rejection count, not approach quality)
- CAND-081 (post-break state, not pre-break approach)

The economic mechanism — approach smoothness reflecting market consensus — is genuinely different from all prior mechanisms.

### 5.11 Classification

> **A — NEW**

The CAND-085 comparison is the closest call. Both measure "approach character." But the economic mechanisms differ (speed/trapped-participants vs smoothness/consensus), the observables differ (velocity vs noise), and the counterfactuals differ (CAND-085's was invalid; CAND-093's should be valid). CAND-085's failure was due to counterfactual design, not mechanism invalidity.

### 5.12 Decision

> **ELIGIBLE FOR G1**

---

## 6. CAND-094 Prior-Art Audit

### 6.1 Research Question

> Does the path geometry (directness) of price approach to a structural level reflect participant alignment and affect break economics?

### 6.2 Economic Mechanism

Path directness → participant positioning alignment → unwinding coordination → directional displacement.

### 6.3 Observable

Path efficiency (net displacement / total movement), direction changes, approach monotonicity.

### 6.4 Temporal Structure

Intra-event: traces the GLOBAL trajectory from approach start to break.

### 6.5 CAND-088 Comparison

```
Prior mechanism (CAND-088):
SESSION SEQUENCE — opening bias direction vs structural break direction.
Opposite-sequence traps opening participants. CLOSED: contradicted.

V31 proposed mechanism (CAND-094):
PATH GEOMETRY — directness of price trajectory to level reflects
participant alignment.

Shared component:
Both are path-dependent.

Material distinction:
CAND-088 measures SEQUENCE (which came first: bias or break).
CAND-094 measures GEOMETRY (how price traveled to the level).
CAND-088 is about temporal ordering of two events.
CAND-094 is about the trajectory of one approach.

Same economic question?
NO — sequence trapping vs alignment from path

Final classification:
DISTINCT from CAND-088
```

### 6.6 CAND-083 Comparison

```
Prior mechanism (CAND-083):
REJECTION COUNT — how many times level held.

V31 proposed mechanism (CAND-094):
PATH DIRECTNESS — how price traveled to the level.

Shared component:
Both characterize level interaction.

Material distinction:
Count vs geometry. Different observables, different mechanisms.

Final classification:
DISTINCT
```

### 6.7 CAND-081 Comparison

```
Prior mechanism (CAND-081):
POST-FAILURE trapped state.

V31 proposed mechanism (CAND-094):
PRE-BREAK path geometry.

Final classification:
DISTINCT (different temporal phase)
```

### 6.8 CAND-085 Comparison

```
Prior mechanism (CAND-085):
APPROACH VELOCITY — speed of price movement.

V31 proposed mechanism (CAND-094):
PATH DIRECTNESS — geometry of trajectory.

Shared component:
Both measure approach character.

Material distinction:
Speed (scalar) vs geometry (trajectory shape).
CAND-085: how FAST. CAND-094: how DIRECT.

Final classification:
DISTINCT from CAND-085
```

### 6.9 APEX/SMC Comparison

No APEX or SMC research tests path geometry as a conditioning variable.

### 6.10 CAND-093 COMPARISON — CRITICAL

```
V31 CAND-093: Price-Discovery Friction Gradient
Approach SMOOTHNESS → consensus → break economics.

V31 CAND-094: Path-Dependent Event Severity
Path DIRECTNESS → alignment → break economics.

Shared component:
BOTH measure the QUALITY OF THE APPROACH to a structural level.

Material distinction:
CAND-093: LOCAL smoothness (return volatility during approach)
CAND-094: GLOBAL directness (trajectory efficiency)

But: A choppy path (low smoothness) is typically also an indirect
path (low directness). A smooth path is typically also direct.
These are HIGHLY CORRELATED measurements of the same underlying
concept: approach quality.

Same economic question?
ESSENTIALLY YES — both ask "does approach quality affect break economics?"

Same downstream event?
YES — structural level breaks.

Same counterfactual?
ESSENTIALLY YES — good approach vs bad approach.

Same participant mechanism?
ESSENTIALLY YES — both claim approach quality reflects participant
state (consensus/alignment).

Final classification:
REDUNDANT WITH EACH OTHER
```

### 6.11 Classification

> **C — REDUNDANT WITH CAND-093**

CAND-094 and CAND-093 are different measurements of the same underlying economic concept: approach quality to a structural level. While the specific observables differ (smoothness vs directness), they would produce highly correlated treatment populations and test the same economic question. One of them is sufficient to test the approach-quality mechanism.

### 6.12 Decision

> **CLOSED / REDUNDANT — NOT ELIGIBLE FOR G1**

---

## 7. Candidate-to-Candidate Redundancy

| Pair | Assessment |
|---|---|
| CAND-092 vs CAND-093 | DISTINCT — inter-event decay vs intra-event approach quality |
| CAND-092 vs CAND-094 | DISTINCT — inter-event decay vs intra-event path geometry |
| CAND-093 vs CAND-094 | **REDUNDANT** — both measure approach quality; different observables but same mechanism |

CAND-093 and CAND-094 are both "approach quality" candidates. They would produce correlated results and test the same economic question. Only one is needed.

---

## 8. Dynamic-vs-Static Audit

| Candidate | Dynamic Requirement | Assessment |
|---|---|---|
| CAND-092 | TIME-SINCE-EVENT (temporal decay) | **PASS** — requires measuring elapsed time and decay trajectory |
| CAND-093 | PATH CHARACTER / FRICTION (approach smoothness) | **PASS** — requires measuring trajectory noise over approach window |
| CAND-094 | PATH GEOMETRY (directness) | **PASS** — but redundant with CAND-093 |

---

## 9. Cross-Research Redundancy Audit

| Candidate | APEX | SMC | QF RF | Assessment |
|---|---|---|---|---|
| CAND-092 | HIGH_VOL persistence (different — regime vs event) | No info-decay concept | No time-since-event candidates | NEW |
| CAND-093 | No approach-smoothness concept | No approach-quality concept | CAND-085 velocity (distinct), CAND-089 velocity-decay (distinct) | NEW |
| CAND-094 | No path-geometry concept | No path concept | **CAND-093 = SAME MECHANISM** | REDUNDANT |

---

## 10. State Firewall

CAND-077/081/083: **NOT MODIFIED, NOT OPTIMIZED, NOT COMBINED**

---

## 11. Closed-Line Firewall

No V19–V30 closed hypothesis reopened. No closed candidate used as positive input.

---

## 12. CAND-088 Firewall

CAND-088: CLOSED / HYPOTHESIS CONTRADICTED. Aligned-break observation: EXPLORATORY / PROVISIONAL. Not imported as V31 positive input.

---

## 13. SEED-002 Firewall

SEED-002: TESTED NEGATIVE. Not retested. Not reversed. Used only as negative knowledge.

---

## 14. APEX RB001–RB004 Firewall

All four: DESIGNED / NOT EXECUTED. Not used as evidence.

---

## 15. Forward Runtime Protection

CAND-015/024/035: ACTIVE / PROTECTED / UNTOUCHED.

---

## 16. G0 Integrity Decision

| Candidate | Classification | Eligible? |
|---|---|---|
| CAND-092 | **A — NEW** | YES |
| CAND-093 | **A — NEW** (distinct from CAND-085; different mechanism and observable) | YES |
| CAND-094 | **C — REDUNDANT WITH CAND-093** | **NO** |

---

## 17. G1 Readiness

> **LIMITED — 2 ELIGIBLE CANDIDATES**

G1 may proceed with CAND-092 and CAND-093 if owner authorizes.

CAND-094 is closed as redundant with CAND-093.

---

## 18. Required Correction

**CAND-094 must be removed from V31.** It is redundant with CAND-093 — both measure approach quality to structural levels, just with different observables (smoothness vs directness). The economic mechanism is the same.

If governance requires a replacement to restore the candidate count to 3:

> V31 G0 CORRECTION REQUIRED — OWNER AUTHORIZATION

Do NOT generate a replacement during this audit.

---

## 19. Governance Decision

### V31 G0 Integrity

> **PARTIAL — 1 CANDIDATE REDUNDANT**

### V31 G1 Readiness

> **LIMITED — G1 ELIGIBLE: CAND-092, CAND-093 (2 candidates)**

---

## 20. Integrity

| Check | Status |
|---|---|
| CAND-092 prior art audited | ✓ |
| CAND-093 compared with CAND-085 | ✓ — DISTINCT |
| CAND-093 compared with CAND-089 | ✓ — DISTINCT |
| CAND-093 compared with CAND-083 | ✓ — DISTINCT |
| CAND-093 compared with CAND-081 | ✓ — DISTINCT |
| CAND-094 compared with CAND-088 | ✓ — DISTINCT |
| CAND-094 compared with CAND-083 | ✓ — DISTINCT |
| CAND-094 compared with CAND-081 | ✓ — DISTINCT |
| CAND-094 compared with CAND-085 | ✓ — DISTINCT |
| CAND-094 compared with CAND-093 | ✓ — **REDUNDANT** |
| APEX/SMC checked | ✓ |
| Candidate-to-candidate redundancy checked | ✓ |
| Dynamic-vs-static checked | ✓ |
| No economics calculated | ✓ |
| No experiment executed | ✓ |
| No G1 executed | ✓ |
| No relational test executed | ✓ |
| No State modified | ✓ |
| No closed candidate reopened | ✓ |
| Forward runtime untouched | ✓ |
| SESSION_HANDOFF updated | ✓ |

---

**Artifact:** `output/research_discovery/QUANTFORGE_V31_G0_INTEGRITY_AUDIT_V1.md`
