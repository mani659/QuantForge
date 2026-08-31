# QUANTFORGE — V32 G0 INTEGRITY AUDIT

## 1. Purpose

Perform a strict, independent **V32 G0 Integrity and Prior-Art Audit** for:
- CAND-095 — Shock-Magnitude Asymmetry
- CAND-096 — Volatility Acceleration Gradient
- CAND-097 — Post-Shock Overshoot Reversion

Determine whether the three V32 G0 candidates genuinely satisfy **NEW DISCOVERY ONLY** under the complete QuantForge / APEX / SMC knowledge base.

## 2. Authoritative Sources

- `docs/SESSION_HANDOFF.md`
- `output/research_discovery/TRADEABLE_EDGE_DISCOVERY_SCREENING_V32.md`
- `output/research_discovery/QUANTFORGE_CROSS_RESEARCH_KNOWLEDGE_INTEGRATION_V1.md`
- `research/knowledge/RESEARCH_DISCOVERY_DATABASE.md`
- `research/knowledge/RESEARCH_TIMELINE.md`
- `research/knowledge/unified_ledger/QUANTFORGE_CROSS_RESEARCH_OBJECT_LEDGER_V1.csv`
- `research/knowledge/unified_ledger/QUANTFORGE_RESEARCH_CANDIDATE_LEDGER_V1.csv`
- `research/knowledge/unified_ledger/QUANTFORGE_NEGATIVE_KNOWLEDGE_LEDGER_V1.csv`
- `output/research_discovery/H01_VOLATILITY_RESPONSE_ASYMMETRY_DEFINITION_LOCK_V1.md`
- `output/research_discovery/LIQUIDITY_SWEEP_RESEARCH_LINE_CLOSURE_GOVERNANCE_RECORD_V1.md`

## 3. V32 G0 Original Claims

| Candidate | Claimed Status | Mechanism Family | Expression Class |
|---|---|---|---|
| CAND-095 | NEW | Directional Response Asymmetry | STATE / CONDITION |
| CAND-096 | NEW | Volatility Dynamics | STATE / CONDITION |
| CAND-097 | NEW | Mean-Reversion Dynamics | STANDALONE ALPHA / STATE |

## 4. Candidate Definition Reconstruction

| Definition Element | CAND-095 | CAND-096 | CAND-097 |
|---|---|---|---|
| Research question | Does shock direction (up vs down) produce different downstream economics? | Does volatility acceleration (rate of change) alter downstream event economics? | Do large moves overshoot and partially revert? |
| Expression class | STATE / CONDITION | STATE / CONDITION | STANDALONE ALPHA / STATE |
| Mechanism family | Directional Response Asymmetry | Volatility Dynamics | Mean-Reversion Dynamics |
| Pre-state | Large directional move (>1.5× ATR) | Volatility in some state | Large directional move occurred |
| Transition | Shock direction creates different participant dynamics | Volatility accelerates (second derivative positive) | Price overshoots shock level |
| Post-state | Direction-dependent response condition | Volatility-acceleration condition | Partial reversion toward pre-shock level |
| Observable | Shock direction (OHLC) | Volatility acceleration (second difference of ATR) | Overshoot and reversion magnitude |
| Temporal structure | Event-level (post-shock) | State-level (volatility evolution) | Event-level (post-shock sequence) |
| Downstream event | Forward returns after shock | Structural break during acceleration | Reversion trade (counter to shock) |
| Economic consequence | Asymmetric tails, different persistence | Escalating uncertainty → adaptation lag | Overshoot correction → reversion profit |
| Counterfactual | Large UP moves (same magnitude, opposite direction) | Structural breaks during deceleration | Large moves that do NOT overshoot |

## 5. CAND-095 Prior-Art Audit

### 5.1 Research Question

Does the direction of a large shock (up vs down) produce systematically different downstream economics?

### 5.2 Mechanism

Direction-dependent participant response: up-shocks trap shorts, down-shocks trap longs. Short-sale constraints create asymmetry.

### 5.3 Observable

Shock direction from OHLC. Shock magnitude >1.5× ATR.

### 5.4 Temporal Structure

Event-level: detect shock → classify direction → compute forward returns.

### 5.5 Relevant Prior Art

**H01 Volatility Response Asymmetry (leverage effect):**
- Tests: return → volatility change (negative shocks raise subsequent volatility more than positive shocks)
- Mechanism: leverage effect — return sign affects volatility response
- **INDEPENDENT from CAND-095:** H01 tests volatility response to signed returns; CAND-095 tests price continuation after directional shocks. Different economic objects.

**DISC-025 Liquidity Sweep Reversal:**
- Tests: sweep of Asian extreme → wick rejection → directional reversal
- Mechanism: auction-mechanics stop-run → reversal
- **INDEPENDENT from CAND-095:** DISC-025 tests a specific auction mechanism; CAND-095 tests general shock-direction asymmetry.

**CAND-088 Session Sequence Asymmetry:**
- Tests: opening bias → opposite-direction structural break → trapped participants
- Mechanism: path-dependent participant trapping
- **INDEPENDENT from CAND-095:** CAND-088 tests session-opening direction vs break direction; CAND-095 tests shock direction per se.

**CAND-091 Cumulative Directional Exhaustion:**
- Tests: cumulative directional distance → depleted participants
- Mechanism: participant depletion from sustained direction
- **CLOSED / HYPOTHESIS CONTRADICTED** — not positive prior art.

**CAND-083 Rejection Accumulation:**
- Tests: repeated rejections at structural level → trapped participants
- Mechanism: accumulation of failed participation
- **INDEPENDENT from CAND-095:** CAND-083 tests rejection count, not shock direction.

**CAND-077 Volatility Compression→Expansion:**
- Tests: volatility regime transition
- Mechanism: regime change
- **INDEPENDENT from CAND-095:** Different mechanism entirely.

### 5.6 Economic Distinction

```
Prior mechanism (H01): Return sign → volatility change (leverage effect)
V32 mechanism: Shock direction → price continuation asymmetry
Shared component: Direction-dependent response
Material distinction: H01 tests volatility response; CAND-095 tests price continuation
Same economic question? NO — different response variable
Same downstream event? NO — different economic object
Same counterfactual? NO — H01 uses matched-magnitude returns; CAND-095 uses opposite-direction shocks
Same participant mechanism? PARTIALLY — both involve directional participant response
Final: NEW
```

### 5.7 NEW / EXTENSION / REDUNDANT / INVALID

> **NEW**

CAND-095 tests a genuinely different economic object from H01 (price continuation vs volatility response). The concept of directional shock-response asymmetry in price continuation has not been tested by any prior QuantForge candidate. The mechanism (short-sale constraints, institutional flow asymmetry) is economically plausible.

### 5.8 Decision

> **ELIGIBLE FOR G1**

CAND-095 is genuinely new. The closest prior art (H01) tests a different economic object (volatility response vs price continuation). The mechanism is distinct and economically plausible.

## 6. CAND-096 Prior-Art Audit

### 6.1 Research Question

Does the rate of change of volatility (acceleration) alter downstream event economics?

### 6.2 Mechanism

Volatility acceleration → escalating uncertainty → participant adaptation lag → different downstream economics.

### 6.3 Observable

Volatility acceleration (second derivative of rolling ATR).

### 6.4 Temporal Structure

State-level: compute acceleration → classify direction → condition structural breaks.

### 6.5 CAND-077 Comparison

```
Prior mechanism (CAND-077): Volatility regime transition (compressed → expanded)
V32 mechanism: Volatility acceleration (rate of change of volatility)
Shared component: Both involve volatility dynamics
Material distinction: CAND-077 tests discrete regime state; CAND-096 tests continuous acceleration rate
Same economic question? PARTIALLY — both test whether volatility dynamics affect economics
Same downstream event? YES — structural breaks
Same counterfactual? NO — CAND-077 uses regime state; CAND-096 uses acceleration direction
Same participant mechanism? SIMILAR — both involve market stress/uncertainty
```

### 6.6 CAND-080 Comparison

CAND-080 tested volatility regime quality transition — found INSUFFICIENT (zero events).

**DISTINCT from CAND-096:** CAND-080 tested regime quality; CAND-096 tests acceleration rate.

### 6.7 APEX Comparison

APEX HIGH_VOL tests volatility level and distributional properties.

**DISTINCT from CAND-096:** APEX tests level; CAND-096 tests acceleration (second derivative).

### 6.8 Economic Distinction

The critical question: Is "volatility is accelerating" economically different from "volatility is transitioning from compressed to expanded"?

The answer is: **PARTIALLY.** CAND-077 captures the regime transition in discrete form. CAND-096 captures it in continuous form. The economic mechanism (adaptation lag, risk-management stress) is plausible for both, but the observables are different enough to constitute a distinct test.

However, there is significant overlap: periods of volatility acceleration often coincide with regime transitions. The acceleration measurement may simply be a noisier version of what CAND-077 captures discretely.

### 6.9 NEW / EXTENSION / REDUNDANT / INVALID

> **NEW — BUT WITH SIGNIFICANT OVERLAP WITH CAND-077**

CAND-096 tests a genuinely different observable (acceleration vs regime state). The economic mechanism (adaptation lag during accelerating volatility) is plausible. However, the overlap with CAND-077 is substantial — acceleration often accompanies regime transitions.

### 6.10 Decision

> **ELIGIBLE FOR G1 — WITH CAVEAT**

CAND-096 is technically new (different observable, different temporal structure). The overlap with CAND-077 should be noted but does not disqualify it. The G1 test will determine whether acceleration carries independent information beyond what CAND-077 already captured.

## 7. CAND-097 Prior-Art Audit

### 7.1 Research Question

Do large moves overshoot and partially revert within a fixed window?

### 7.2 Mechanism

Overshooting → partial reversion → the reversion amount contains information about whether the shock was genuine information or noise.

### 7.3 Observable

Shock magnitude, overshoot amount, reversion amount, reversion ratio.

### 7.4 Temporal Structure

Event-level: detect shock → measure overshoot → measure reversion → classify by reversion ratio.

### 7.5 DISC-021 Mean-Reversion Comparison

**THIS IS THE CRITICAL COMPARISON.**

| Dimension | DISC-021 Mean Reversion | CAND-097 |
|---|---|---|
| Trigger | Extreme displacement (rolling z-score) | Large directional move (>1.5× ATR) |
| Precondition | Displacement exceeds threshold | Shock magnitude exceeds threshold |
| Event | Displacement → recoil → persistence | Shock → overshoot → reversion |
| Observable | Price z-score / ATR-relative displacement | Overshoot and reversion magnitude |
| Temporal structure | Displacement detection → forward returns | Shock detection → overshoot measurement → reversion trade |
| Economic mechanism | Displaced price reverts toward mean | Overshooting price partially reverts toward pre-shock level |
| Participant constraint | Market participants correct mispricing | Market participants correct overshoot |
| Expected direction | COUNTER to displacement (mean reversion) | COUNTER to shock (mean reversion) |
| Counterfactual | Non-displaced periods | Large moves that do NOT overshoot |
| Failure mode | Economic non-viability (costs consume effect) | Economic non-viability (costs consume effect) |
| Economic consequence | Reversion profit from displacement correction | Reversion profit from overshoot correction |
| Same underlying hypothesis? | **YES** | **YES** |

**Assessment:**

DISC-021 tested: "extreme displacement → recoil → persistence" as a mean-reversion hypothesis. The trigger was z-score-based displacement. The mechanism was: price moves too far, then reverts.

CAND-097 tests: "large move → overshoot → reversion" as a mean-reversion hypothesis. The trigger is ATR-based shock magnitude. The mechanism is: price overshoots, then partially reverts.

**The economic mechanism is IDENTICAL:** price moves too far (by some definition), then comes back (partially or fully).

The operationalization differs:
- DISC-021: z-score displacement → recoil
- CAND-097: ATR-based shock → overshoot → reversion

But the economic question is the same: **does excessive price movement predict reversion?**

DISC-021 already answered this: **statistically observable but economically non-viable** (costs consume the effect).

### 7.6 Reversal / Exhaustion Comparison

**CAND-078 Trend Exhaustion:**
- Tests: 8+ consecutive same-direction closes → reversal bar
- Mechanism: trend exhaustion → mean reversion
- **CLOSED / ECONOMICALLY NEGATIVE** — exhaustion transition adds no value
- **Same mechanism family:** mean reversion after extreme movement

**CAND-082 Post-Expansion Retracement:**
- Tests: volatility expansion → retracement quality
- Mechanism: post-expansion correction
- **INFORMATIONALLY INTERESTING** — but State hypothesis contradicted
- **Related mechanism:** retracement after expansion

**CAND-091 Cumulative Directional Exhaustion:**
- Tests: cumulative directional distance → depleted participants
- Mechanism: participant exhaustion → counter-trend amplification
- **CLOSED / HYPOTHESIS CONTRADICTED**
- **Related mechanism:** exhaustion-driven reversal

### 7.7 Shock-Response Comparison

**DISC-025 Liquidity Sweep Reversal:**
- Tests: sweep of Asian extreme → wick rejection → reversal
- Mechanism: auction-mechanics stop-run → reversal
- **CLOSED / ECONOMICALLY NON-VIABLE** (translation failure, not behavioral failure)
- **Different mechanism:** auction mechanics, not general overshoot

**CAND-086 Information Absorption Failure Cascade:**
- Tests: repeated failed directional moves → trapped participants
- Mechanism: failure accumulation → eventual continuation
- **CLOSED / ECONOMICALLY NEGATIVE**
- **Different mechanism:** failure accumulation, not overshoot reversion

### 7.8 Economic Distinction

```
Prior mechanism (DISC-021): Displacement → recoil → persistence (mean reversion)
V32 mechanism: Shock → overshoot → partial reversion (mean reversion)
Shared component: Price moves too far, then reverts
Material distinction: TRIGGER DIFFERS (displacement vs shock), MECHANISM IDENTICAL (reversion)
Same economic question? YES — does excessive price movement predict reversion?
Same downstream event? YES — reversion trade
Same counterfactual? SIMILAR — non-displaced vs non-overshooting periods
Same participant mechanism? YES — market participants correct mispricing
Final: REDUNDANT
```

### 7.9 NEW / EXTENSION / REDUNDANT / INVALID

> **REDUNDANT WITH DISC-021**

CAND-097 is mean reversion after a large move. DISC-021 is mean reversion after extreme displacement. The economic mechanism is identical: price moves too far, then reverts. The operationalization differs (ATR-based shock vs z-score displacement), but the economic question is the same.

DISC-021 already established that this mechanism is **statistically observable but economically non-viable** due to execution costs consuming the effect.

Adding "overshoot measurement" does not change the underlying mechanism. It is a different way to detect the same phenomenon.

### 7.10 Decision

> **REJECTED — REDUNDANT WITH DISC-021**

CAND-097 does not represent a genuinely new economic mechanism. It is mean reversion after a large move, which is exactly what DISC-021 tested and closed as economically non-viable.

## 8. Candidate-to-Candidate Redundancy

### CAND-095 ↔ CAND-096

**DISTINCT.** CAND-095 tests shock direction → price continuation. CAND-096 tests volatility acceleration → event economics. Different mechanisms, different observables, different economic questions.

### CAND-095 ↔ CAND-097

**DISTINCT (before CAND-097 rejection).** CAND-095 tests directional asymmetry in continuation. CAND-097 tests mean reversion after overshoot. Different directions (WITH shock vs COUNTER to shock), different mechanisms.

### CAND-096 ↔ CAND-097

**DISTINCT.** CAND-096 tests volatility dynamics. CAND-097 tests price reversion. Different mechanisms entirely.

## 9. Dynamic-vs-Static Audit

### CAND-095

**PASS.** Requires shock identification + direction classification + forward return comparison. Cannot be reduced to "large moves have different returns" — the direction asymmetry is essential.

### CAND-096

**PASS.** Requires volatility acceleration (second derivative) measurement. Cannot be reduced to "high volatility events have different returns" — the acceleration rate is essential.

### CAND-097

**FAIL (rejected anyway).** Requires shock → overshoot → reversion sequence. The temporal structure is dynamic, but the mechanism is redundant with DISC-021.

## 10. Economic Mechanism Novelty

### CAND-095

```
Prior mechanism (H01): Return sign → volatility change (leverage effect)
V32 mechanism: Shock direction → price continuation asymmetry
Shared component: Direction-dependent response
Material economic distinction: H01 tests volatility response; CAND-095 tests price continuation
Same participant constraint? PARTIALLY — both involve directional participant response
Same downstream consequence? NO — different economic objects
Same test? NO — different experimental design
Final: NEW
```

### CAND-096

```
Prior mechanism (CAND-077): Volatility regime transition (discrete)
V32 mechanism: Volatility acceleration (continuous second derivative)
Shared component: Volatility dynamics affecting economics
Material economic distinction: CAND-077 tests regime state; CAND-096 tests acceleration rate
Same participant constraint? SIMILAR — both involve adaptation to volatility changes
Same downstream consequence? SIMILAR — both condition structural breaks
Same test? NO — different observables and temporal structure
Final: NEW (with overlap caveat)
```

### CAND-097

```
Prior mechanism (DISC-021): Displacement → recoil → persistence (mean reversion)
V32 mechanism: Shock → overshoot → partial reversion (mean reversion)
Shared component: Price moves too far, then reverts
Material economic distinction: NONE — same mechanism, different trigger
Same participant constraint? YES — market participants correct mispricing
Same downstream consequence? YES — reversion profit
Same test? SIMILAR — different trigger detection, same economic question
Final: REDUNDANT
```

## 11. Cross-Research Redundancy Map

| Candidate | Potential Overlap | Assessment |
|---|---|---|
| CAND-095 | H01 (leverage effect) | DISTINCT — price continuation vs volatility response |
| CAND-095 | DISC-025 (sweep reversal) | DISTINCT — general shock direction vs auction mechanics |
| CAND-095 | CAND-088 (session sequence) | DISTINCT — shock direction vs opening-bias sequence |
| CAND-096 | CAND-077 (regime transition) | OVERLAP — acceleration vs discrete transition |
| CAND-096 | CAND-080 (regime quality) | DISTINCT — acceleration vs quality |
| CAND-096 | APEX HIGH_VOL (level) | DISTINCT — acceleration vs level |
| CAND-097 | **DISC-021 (mean reversion)** | **REDUNDANT — same mechanism** |
| CAND-097 | CAND-078 (trend exhaustion) | SAME FAMILY — mean reversion after extreme |
| CAND-097 | DISC-025 (sweep reversal) | RELATED — reversal after specific trigger |
| CAND-097 | CAND-091 (exhaustion) | SAME FAMILY — counter-trend after extreme |

## 12. Closed-Line Firewall

- Mean Reversion / DISC-021 = **CLOSED** — CAND-097 REDUNDANT with this line
- CAND-078 = CLOSED / ECONOMICALLY NEGATIVE
- CAND-087 = CLOSED
- CAND-088 = CLOSED / HYPOTHESIS CONTRADICTED
- CAND-089 = CLOSED / NO INCREMENTAL INFORMATION
- CAND-090 = CLOSED / REDUNDANT WITH CAND-087
- CAND-091 = CLOSED / HYPOTHESIS CONTRADICTED
- CAND-092 = CLOSED / ECONOMICALLY NEGATIVE
- CAND-093 = CLOSED / ECONOMICALLY NEGATIVE
- CAND-094 = CLOSED / REDUNDANT WITH CAND-093
- SEED-002 = TESTED NEGATIVE / NO INCREMENTAL INFORMATION

## 13. State Firewall

- CAND-059 — STATE-ARTIFACT: PRESERVED
- CAND-065 — STATE OBSERVATION: PRESERVED
- CAND-069 — STATE OBSERVATION: PRESERVED
- CAND-077 — STATE REVIEW ELIGIBLE: PRESERVED
- CAND-079 — STATE OBSERVATION: PRESERVED
- CAND-081 — STATE REVIEW ELIGIBLE: PRESERVED
- CAND-083 — STATE REVIEW ELIGIBLE: PRESERVED

## 14. CAND-088 Firewall

CAND-088 = CLOSED / HYPOTHESIS CONTRADICTED
Aligned-break observation = EXPLORATORY / PROVISIONAL

Not imported as V32 positive input.

## 15. SEED-002 Firewall

SEED-002 = TESTED NEGATIVE — NO INCREMENTAL INFORMATION
Not retested. Used only as negative knowledge.

## 16. APEX RB001–RB004 Firewall

All four: DESIGNED / NOT EXECUTED
Not used as evidence. Not executed.

## 17. Forward Runtime Protection

- CAND-015 = ACTIVE / PROTECTED / UNTOUCHED
- CAND-024 = ACTIVE / PROTECTED / UNTOUCHED
- CAND-035 = ACTIVE / PROTECTED / UNTOUCHED

Not inspected. Not used as evidence.

## 18. G0 Integrity Decision

| Candidate | Classification | Reason |
|---|---|---|
| CAND-095 | **NEW** | Genuinely different economic object from H01 (price continuation vs volatility response) |
| CAND-096 | **NEW** | Different observable from CAND-077 (acceleration vs regime state), with overlap caveat |
| CAND-097 | **REDUNDANT** | Same mechanism as DISC-021 (mean reversion after extreme movement) |

## 19. G1 Readiness

> **PARTIAL — 2 ELIGIBLE CANDIDATES**

CAND-095 and CAND-096 are eligible for G1. CAND-097 is rejected as redundant with DISC-021.

G1 may proceed with CAND-095 and CAND-096 if owner authorizes.

## 20. Required Correction

**CAND-097 must be removed from the V32 candidate set.**

V32 now contains 2 eligible candidates, not 3.

If governance requires a corrected G0 pass to restore the candidate count to 3:
> V32 G0 CORRECTION REQUIRED — OWNER AUTHORIZATION

Do NOT generate a replacement candidate in this audit.

## 21. Governance Decision

- **CAND-095:** ELIGIBLE FOR G1 — NEW
- **CAND-096:** ELIGIBLE FOR G1 — NEW (with CAND-077 overlap caveat)
- **CAND-097:** REJECTED — REDUNDANT WITH DISC-021

V32 candidate count: **2** (reduced from 3)

## 22. Integrity

- CAND-095 prior art checked: H01, DISC-025, CAND-088, CAND-091, CAND-083, CAND-077
- CAND-096 compared to CAND-077: overlap documented, distinction maintained
- CAND-096 compared to CAND-080: distinct
- CAND-096 compared to APEX HIGH_VOL: distinct
- CAND-097 compared to DISC-021: **REDUNDANT — same mechanism**
- CAND-097 compared to CAND-078: same family
- CAND-097 compared to DISC-025: related but different trigger
- CAND-097 compared to CAND-091: same family
- Candidate-to-candidate redundancy checked
- Dynamic-vs-static requirement checked
- No economic testing occurred
- No G1 occurred
- No relational testing occurred
- No APEX RB branch executed
- No State modified
- No closed candidate reopened
- No replacement candidate invented
- Candidate quota did not override integrity
- SESSION_HANDOFF to be updated
- Database/timeline to be updated
- Candidate ledger to be updated
- Git staged diff to be limited to authorized files
