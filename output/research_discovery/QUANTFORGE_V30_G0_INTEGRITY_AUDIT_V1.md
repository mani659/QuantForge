# QUANTFORGE — V30 G0 INTEGRITY AUDIT

**Date:** 2026-08-31
**Status:** COMPLETE

---

## 1. Purpose

Independent prior-art and integrity audit of V30 G0 candidates before V30 G1.
Primary concern: CAND-090 appears identical to V29 CAND-087.

---

## 2. Authoritative Sources

- V29 G0: `TRADEABLE_EDGE_DISCOVERY_SCREENING_V29.md` (CAND-087 definition)
- V29 G1: `RESEARCH_FACTORY_V2_G1_SCREEN_20260830_V29.md` (CAND-087 G1 result)
- V30 G0: `TRADEABLE_EDGE_DISCOVERY_SCREENING_V30.md` (CAND-089/090/091 definitions)
- Unified Knowledge Ledger V1
- Cross-Research Object Ledger
- Negative Knowledge Ledger
- RESEARCH_DISCOVERY_DATABASE.md
- RESEARCH_TIMELINE.md

---

## 3. V30 G0 Original Claims

V30 G0 claimed three NEW candidates:
- CAND-089: Acceptance Velocity Decay (NEW)
- CAND-090: Recovery Quality Differential (NEW — conditional on CAND-087 check)
- CAND-091: Cumulative Directional Exhaustion (NEW)

---

## 4. CAND-089 Prior-Art Audit

### Research Question

> Do structural level breaks preceded by decaying acceptance velocity produce larger directional moves than breaks at levels with stable/increasing velocity?

### Mechanism

Information processing dynamics: declining acceptance velocity → participant accumulation with declining conviction → forced exits on break → directional amplification.

### Observable

Acceptance velocity (rate of range convergence after level test), velocity decay rate (second derivative), structural level (20-bar rolling high/low).

### Temporal Structure

Event-level: measured across multiple level tests, with velocity decay computed over the most recent L tests (L=3). Dynamic because it requires CHANGE in velocity over time.

### Economic Consequence

Larger directional displacement after level breaks when velocity has decayed. Forced-exit amplification creates fat tails in break direction.

### Existing Overlaps

| Candidate | Overlap | Assessment |
|---|---|---|
| CAND-083 | Rejection COUNT at levels | DISTINCT — velocity (speed) vs count (quantity). Different observable, different mechanism. CAND-083 counts rejections; CAND-089 measures acceptance speed dynamics. |
| CAND-081 | Post-failure trapped state | DISTINCT — CAND-089 is about the process BEFORE the break; CAND-081 is about the state AFTER the break. |
| CAND-086 | Information absorption failure | DISTINCT — CAND-086 counted failed directional impulses; CAND-089 measures acceptance velocity at structural levels. Different observable, different mechanism. |
| CAND-077 | Volatility character transition | DISTINCT — regime-level vs event-level. Different temporal level, different observable. |
| APEX HIGH_VOL | Volatility persistence | DISTINCT — regime-level vs level-specific. |
| SMC BOS+OB | Structural break + order block | DISTINCT — SMC measures the break event; CAND-089 measures pre-break acceptance dynamics. |

### NEW / EXTENSION / REDUNDANT

> **NEW**

No existing candidate measures acceptance velocity or its decay at structural levels. CAND-083 counts rejections (a different observable). The velocity-decay dynamic is genuinely distinct.

### Decision

> **PASS — ELIGIBLE FOR G1**

---

## 5. CAND-090 Prior-Art Audit

### CAND-087 Comparison

#### Research Question

| Dimension | CAND-087 (V29) | CAND-090 (V30) | Match? |
|---|---|---|---|
| Core question | Does recovery quality after disturbance reveal temporary vs genuine information? | Do high-quality recoveries produce more favorable downstream economics? | **SAME** |
| What is measured | Recovery quality after large disturbance | Recovery quality after structural event | **SAME** |

#### Mechanism

| Dimension | CAND-087 | CAND-090 | Match? |
|---|---|---|---|
| Pre-event | Large adverse move (>2× ATR) | Structural break / large move | **SAME** (CAND-090 slightly broader) |
| Recovery quality definition | Speed (5-bar) + completeness (10-bar) | Speed + consistency + smoothness + adverse excursion | **SAME CORE** (CAND-090 adds smoothness/excursion metrics) |
| Participant constraint | Trapped participant resolution | Participant urgency / inventory | **SAME** (different words for same concept) |
| Economic mechanism | Weak recovery → trapped participants remain → forced exits → continuation | Low-quality recovery → participants hesitant → retracement fails → original move resumes | **SAME PREDICTION** |
| Direction | With disturbance direction (continuation) | With retracement direction (continuation of retracement = original move resumes) | **SAME** |

#### Observable

| Variable | CAND-087 | CAND-090 | Distinct? |
|---|---|---|---|
| Recovery speed | 5-bar fraction recovered | Bars to 50% retracement | Same concept, different parameterization |
| Recovery completeness | 10-bar fraction recovered | Consistency (% bars in direction) | Same concept, different metric |
| Recovery smoothness | Not measured | Std of bar-to-bar returns | New metric — but same underlying concept |
| Adverse excursion | Not measured | Max adverse move during recovery | New metric — but same underlying concept |
| Disturbance size | ATR-normalized | Event magnitude | Same concept |

#### Temporal Definition

| Parameter | CAND-087 | CAND-090 |
|---|---|---|
| Recovery window | 10 bars | 30 bars |
| Holding period | 20 bars | 60 bars |
| Entry timing | Bar 10 after disturbance | After quality classification |

Different parameter values, but the same temporal structure: measure recovery → classify → trade.

#### Counterfactual

| Element | CAND-087 | CAND-090 |
|---|---|---|
| Treatment | Weak recovery (<25%) | Low-quality recovery |
| Control | Strong recovery (>75%) | High-quality recovery |
| Comparison | Weak vs strong in same direction | Low vs high quality in same direction |

**IDENTICAL counterfactual structure.**

#### Failure Mode

Both would fail if recovery quality does not contain meaningful economic information. Same failure mode.

#### G1 Measurement

Both would use the same G1 test: compare forward returns conditional on recovery quality. Different parameters, same test.

### Exact Distinction

CAND-090 differs from CAND-087 only in:

1. **Additional metrics:** smoothness and adverse excursion (minor additions to same concept)
2. **Different parameters:** 30-bar window vs 10-bar, 60-bar holding vs 20-bar (parameter variation)
3. **Broader event trigger:** "structural break, large move, session transition" vs ">2× ATR move" (slightly broader)
4. **Different wording:** "urgency/inventory" vs "trapped participant resolution" (same concept, different language)

**None of these constitute a material, economically meaningful distinction at the level of mechanism, observable, temporal structure, or economic consequence.**

### NEW / EXTENSION / REDUNDANT

> **A — REDUNDANT**

CAND-090 is the same economic hypothesis as CAND-087 in materially the same observable form. The additional metrics (smoothness, excursion) are minor augmentations to the same recovery-quality concept. The parameter differences (10 vs 30 bars, 20 vs 60 holding) are implementation choices, not mechanism distinctions.

### Decision

> **CAND-090 MUST BE CLOSED / REJECTED AS REDUNDANT**

CAND-090 is not eligible for V30 G1.

---

## 6. CAND-091 Prior-Art Audit

### Research Question

> Do structural events occurring during cumulative directional exhaustion produce larger counter-trend moves than events during non-exhausted conditions?

### Mechanism

Directional exhaustion dynamics: cumulative directional distance depletes marginal participants → exhausted market → larger counter-trend moves on catalyst.

### Observable

Cumulative directional distance (sum of returns over rolling window), distance-to-range ratio, trend consistency.

### Temporal Structure

State-level: measured over rolling 100-bar windows. Dynamic because it requires CUMULATIVE movement over time — the transition from "trending" to "exhausted" is a time-dependent process.

### Economic Consequence

Larger counter-trend moves when exhaustion is present. Fat tails in counter-trend direction. Sensitivity amplification to catalysts.

### Existing Overlaps

| Candidate | Overlap | Assessment |
|---|---|---|
| CAND-077 | Volatility character transition | DISTINCT — CAND-091 measures CUMULATIVE DIRECTIONAL distance, not volatility regime. A market can be volatile but not exhausted, or exhausted but not volatile. Different observable, different mechanism. |
| CAND-083 | Rejection accumulation at levels | DISTINCT — CAND-083 is event-level (rejection count at structural levels); CAND-091 is state-level (cumulative directional distance). Different temporal level, different observable. |
| CAND-086 | Information absorption failure | DISTINCT — CAND-086 counted failed directional impulses; CAND-091 measures cumulative distance over time. Different mechanism. |
| CAND-078 | Trend exhaustion (CLOSED) | DISTINCT — CAND-078 was in a different mechanism family and was closed for insufficient evidence. CAND-091 uses a different observable (cumulative distance) and a different economic mechanism (participant depletion). |
| CAND-080 | Path dependence (CLOSED) | DISTINCT — CAND-080 was about opening-range path dependence; CAND-091 is about cumulative directional exhaustion. Different mechanism. |
| TSMOM | Time-series momentum (early QuantForge) | DISTINCT — TSMOM was about trend-following; CAND-091 is about exhaustion-conditioned event response. Different research question. |
| APEX HIGH_VOL | Volatility persistence | DISTINCT — regime-level vs directional exhaustion. Different observable. |

### NEW / EXTENSION / REDUNDANT

> **NEW**

No existing candidate measures cumulative directional distance as a condition for event economics. CAND-077 measures volatility character (different observable). CAND-083 measures rejection count (different observable). The exhaustion mechanism is genuinely distinct.

### Decision

> **PASS — ELIGIBLE FOR G1**

---

## 7. Dynamic-vs-Static Audit

### CAND-089

The meaningful object is **velocity DECAY** (change in acceptance velocity over time), not static low velocity. The second derivative is essential. **PASS** — dynamic requirement satisfied.

### CAND-090

Recovery quality is measured over a TIME WINDOW after events. The classification depends on the TRAJECTORY, not a static threshold. However, the concept is REDUNDANT with CAND-087 regardless. **NOT APPLICABLE** — candidate is rejected.

### CAND-091

The meaningful object is **cumulative** directional distance (accumulation over time), not a single large move. The dynamic nature is essential: exhaustion requires that the market has BEEN moving (process), not that it HAS moved (state). **PASS** — dynamic requirement satisfied.

---

## 8. Cross-Research Redundancy Audit

| Candidate | APEX | SMC | QuantForge RF | Assessment |
|---|---|---|---|---|
| CAND-089 | No acceptance velocity concept | No acceptance dynamics | CAND-083 counts rejections (different) | NEW |
| CAND-090 | No recovery quality concept | No recovery dynamics | **CAND-087 = SAME CONCEPT** | REDUNDANT |
| CAND-091 | HIGH_VOL persistence (different) | No exhaustion concept | CAND-077 vol character (different) | NEW |

---

## 9. Closed-Line Firewall

> **PASS**

No V19–V29 closed hypothesis was reopened or used as a positive input.

---

## 10. State Firewall

CAND-077/081/083: **NOT MODIFIED, NOT OPTIMIZED, NOT COMBINED**

---

## 11. Exploratory Observation Firewall

CAND-077 >15 bps: **NOT IMPORTED**
CAND-088 aligned-break: **NOT IMPORTED**

---

## 12. Forward Runtime Protection

CAND-015/024/035: **ACTIVE / PROTECTED / UNTOUCHED**

---

## 13. G1 Readiness

| Candidate | Status | G1 Eligible? |
|---|---|---|
| CAND-089 | NEW | YES |
| CAND-090 | REDUNDANT (same as CAND-087) | **NO** |
| CAND-091 | NEW | YES |

---

## 14. Required V30 Correction

**CAND-090 must be removed from V30.**

V30 now contains **2 eligible candidates** (CAND-089, CAND-091), not 3.

The V30 G0 instruction required "exactly THREE genuinely new candidates."
One candidate failed the prior-art integrity audit. The correct outcome
is to report the failure, not to invent a replacement.

If the owner authorizes, a corrected G0 candidate-generation pass may
restore the candidate count. That is a separate explicitly authorized task.

---

## 15. Governance Decision

### V30 G0 Integrity

> **BLOCKED — CORRECTION REQUIRED**

CAND-090 is REDUNDANT with CAND-087. It must be removed.

### V30 G1 Readiness

> **LIMITED — G1 ELIGIBLE CANDIDATES: CAND-089, CAND-091**

G1 may proceed with 2 candidates if owner authorizes.

Alternatively, a corrected G0 may restore the count to 3.

---

## 16. Integrity

| Check | Status |
|---|---|
| CAND-089 prior art audited | ✓ |
| CAND-090 compared against CAND-087 | ✓ — REDUNDANT |
| CAND-091 prior art audited | ✓ |
| Dynamic-vs-static checked | ✓ |
| Cross-research ledger checked | ✓ |
| No new statistics calculated | ✓ |
| No experiment executed | ✓ |
| No G1 executed | ✓ |
| No relational testing executed | ✓ |
| No optimization executed | ✓ |
| No State modified | ✓ |
| No closed candidate reopened | ✓ |
| No forward runtime inspected | ✓ |
| V30 readiness explicitly determined | ✓ |
| SESSION_HANDOFF updated | ✓ |
| No candidate invented to preserve count | ✓ |

---

**Artifact:** `output/research_discovery/QUANTFORGE_V30_G0_INTEGRITY_AUDIT_V1.md`
