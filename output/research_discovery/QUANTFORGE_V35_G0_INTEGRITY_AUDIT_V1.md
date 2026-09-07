# QUANTFORGE — V35 G0 INTEGRITY / PRIOR-ART AUDIT

## CAND-103 + CAND-104

**Date:** 2026-09-02
**Status:** AUDIT COMPLETE
**Scope:** Independent semantic, novelty, and G1-readiness audit of V35 G0 candidates

---

## 1. Mission

Perform a strict, adversarial, READ-ONLY G0 integrity audit of CAND-103 (Multi-Timeframe Break Coordination) and CAND-104 (Post-Magnitude Directional Drift).

This audit determines whether each candidate is genuinely distinct, semantically well-defined, data-feasible, and sufficiently defensible to proceed to G1.

This is NOT G1. No experiments. No outcome data. No optimization.

---

## 2. Authoritative Repository State

- **HEAD:** `6f11efa` — `docs: add V35 G0 commit SHA to SESSION_HANDOFF`
- **Branch:** `main`
- **V34 COMPLETE:** CAND-101 CLOSED (ECONOMICALLY NEGATIVE), CAND-102 CLOSED (HYPOTHESIS CONTRADICTED)
- **V33 COMPLETE:** CAND-098 CLOSED (ECONOMICALLY NEGATIVE), CAND-099 CLOSED (HYPOTHESIS CONTRADICTED), CAND-100 DATA INFEASIBLE
- **V32 COMPLETE:** CAND-095 CLOSED (ECONOMICALLY NEGATIVE), CAND-096 CLOSED (HYPOTHESIS CONTRADICTED)
- **V31 COMPLETE:** CAND-092 CLOSED (ECONOMICALLY NEGATIVE), CAND-093 CLOSED (ECONOMICALLY NEGATIVE)
- **V30 COMPLETE:** CAND-089 CLOSED, CAND-091 CLOSED (HYPOTHESIS CONTRADICTED)
- **G2 promotions:** 0 across all cycles
- **State Review Eligible:** CAND-077, CAND-081, CAND-083
- **SEED-002:** TESTED NEGATIVE
- **Forward runtime:** CAND-015/024/035 ACTIVE / PROTECTED / UNTOUCHED

---

## 3. Prior-Art Methodology

The audit compares each candidate against the complete repository of registered candidates, checking for material distinction at the level of:

- MECHANISM (economic process)
- OBSERVABLE (what is measured)
- TEMPORAL STRUCTURE (anchor → observation → outcome)
- ECONOMIC QUESTION (what is being asked)

Novel wording is not novelty. A new threshold is not novelty. A complementary sign is not automatically novelty.

---

## 4. CAND-103 Semantic Audit

### 4.1 Reconstructed Definition

```
MARKET PHENOMENON: Breaks across multiple timeframes produce different economics than single-timeframe breaks.
MECHANISM: Coordinated forced repositioning across participant groups operating at different timeframes.
OBSERVABLE: Number of timeframe levels broken in the same directional move.
EXPECTED EFFECT: Multi-timeframe breaks produce tighter distributions and stronger continuation.
TRADEABLE USE: State filter for risk management or conditional Alpha.
```

### 4.2 Link Quality Assessment

| Link | Assessment | Evidence |
|---|---|---|
| Market phenomenon | GOOD | Multi-timeframe analysis is fundamental to market participation |
| Mechanism | BORDERLINE | Coordinated repositioning is plausible but may simply be trend strength |
| Observable | GOOD | Number of timeframe levels broken is deterministic from OHLC |
| Expected effect | BORDERLINE | Tighter distributions plausible but may reflect trend, not coordination |
| Tradeable use | GOOD | State filter application is clear |

**Weakest link:** Mechanism — the "coordination" explanation may be confounded with "stronger trend."

### 4.3 Semantic Integrity

**Critical question:** Is this genuinely testing cross-timeframe coordination, or simply stronger trend confirmation?

**Analysis:** The observable (number of timeframe levels broken) is genuinely distinct from a trend-strength measure (e.g., return magnitude, ATR percentile). A move can be large enough to break a 15-minute high without breaking a 1-hour high — this is NOT a multi-timeframe break. Only when both are broken does the observable fire. This is a meaningful distinction.

However, the MECHANISM (participant coordination) is inferred, not directly observed. The observable captures the structural pattern; the mechanism explains why it matters. The distinction between "coordination" and "stronger trend" is real but must be explicitly acknowledged.

---

## 5. CAND-103 Prior-Art Comparison

| Prior candidate | Shared mechanism | Shared observable | Shared temporal structure | Material difference |
|---|---|---|---|---|
| CAND-077 (Vol compression→expansion) | Volatility state | ATR percentile | Rolling window | CAND-077 measured volatility STATE. CAND-103 measures cross-timeframe break COORDINATION. Different observable class. |
| CAND-096 (Volatility acceleration) | Volatility dynamics | Rate of vol change | Rolling window | CAND-096 measured vol ACCELERATION. CAND-103 measures cross-timeframe break SCOPE. Different observable. |
| CAND-095 (Shock magnitude asymmetry) | Shock response | Shock direction | Event-level | CAND-095 tested shock DIRECTION (up vs down). CAND-103 tests cross-timeframe break SCOPE. Different observable. |
| CAND-098 (Event-cluster density) | Event clustering | Event count in window | Event-level | CAND-098 counted events in a TIME window. CAND-103 counts events across TIMEFRAMES. Different dimension. |
| CAND-101 (Path-dependent sequencing) | Event order | Sequence type | Event-level | CAND-101 tested event ORDER. CAND-103 tests cross-timeframe SCOPE. Different dimension. |
| CAND-102 (Directional persistence) | Cumulative directional effects | Run length | Event-level | CAND-102 tested run LENGTH. CAND-103 tests cross-timeframe COORDINATION. Different dimension. |
| CAND-089 (Acceptance velocity) | Velocity dynamics | Velocity at levels | Event-level | CAND-089 measured velocity. CAND-103 measures cross-timeframe scope. Different observable. |

### 5.1 Critical Question

> If all timeframes point in the same direction, what makes this "coordination" rather than simply stronger trend state?

**Answer:** The observable is NOT "all timeframes point in the same direction" — it is "breaks occur simultaneously across multiple timeframes." A strong trend can exist without multi-timeframe breaks (e.g., price drifts higher without breaking any major level). Multi-timeframe breaks require specific structural events at specific timeframes, not just directional movement.

**However:** The distinction is real but the mechanism (coordination) is inferred. The observable captures the structural pattern; the mechanism explains why it matters. The audit notes this as a limitation, not a rejection.

### 5.2 Novelty Verdict

> **CLEARLY NOVEL**

No prior candidate has tested multi-timeframe break coordination. The observable is genuinely distinct from all prior work. The mechanism is plausible but inferred.

---

## 6. CAND-103 Mechanism–Observable Challenge

### 6.1 Mechanism Independence

**What phenomenon exists independently of the feature?**

Multi-timeframe analysis is fundamental to market participation. Traders at different timeframes respond to breaks at their respective levels. This phenomenon exists independently.

### 6.2 Proxy Challenge

**How can the observable occur without the claimed mechanism?**

Multi-timeframe breaks could occur simply because price is moving strongly. In a trending market, breaks at multiple timeframes happen naturally. The observable could reflect trend strength, not coordination.

### 6.3 Alternative Explanation

**What competing process could produce the same observable?**

1. Simple trend strength
2. Volatility regime (high-vol periods produce more breaks at all timeframes)
3. Timeframe nesting (lower-timeframe breaks are contained within higher-timeframe breaks)

### 6.4 Observable Fidelity

**Why does the observable reasonably measure the mechanism?**

The number of timeframe levels broken directly captures cross-timeframe coordination. However, the mechanism (participant coordination) is inferred.

### 6.5 Expected-Effect Bridge

**Why should the mechanism alter subsequent outcomes?**

If coordinated repositioning creates orderly repricing, subsequent distributions should be tighter and more directional.

### 6.6 Falsification

**What would clearly contradict the hypothesis?**

If multi-timeframe breaks produce identical distributions to single-timeframe breaks, the hypothesis is contradicted.

### 6.7 Tradeability

**What prevents the information surviving costs?**

1. Timing: identifying multi-timeframe breaks requires waiting for the move
2. Frequency: multi-timeframe breaks may be rare
3. Costs: small separation consumed by friction

### 6.8 Base Rate

**Why should G1 resources be spent?**

Genuinely unexplored mechanism dimension. Clean observable. Not a variant of prior candidates.

### 6.9 Confidence Dimensions

- **Mechanism Confidence:** MODERATE
- **Proxy Confidence:** MODERATE
- **Observable Information Potential:** MODERATE

---

## 7. CAND-103 Temporal Integrity

```
ANCHOR: A directional move that breaks one or more timeframe levels
OBSERVATION WINDOW: The move itself (identification of broken levels)
SIGNAL FORMATION: After the move completes
OUTCOME WINDOW: H bars after the move completes
```

**Temporal concerns:**

1. **Higher-timeframe bar closure:** If using M15 or H1 levels, the higher-timeframe bar must be COMPLETE before the level is considered broken. Using incomplete higher-timeframe bars would introduce look-ahead bias.

2. **Synchronization:** The move must be identified as a single event spanning multiple timeframes. If the move is gradual (breaking M15 first, then H1 later), the classification must handle this correctly.

3. **Deduplication:** A single large move breaking multiple timeframes should be counted once, not multiple times.

**Assessment:** Temporal integrity is PASSABLE with proper implementation, but requires careful handling of higher-timeframe bar closure. This is a G1-implementation concern, not a G0-rejection.

---

## 8. CAND-104 Semantic Audit

### 8.1 Reconstructed Definition

```
MARKET PHENOMENON: Very large directional moves (relative to recent volatility) produce directional drift.
MECHANISM: Forced repositioning (stop-losses, margin calls, systematic rebalancing) takes time to complete.
OBSERVABLE: Volatility-adjusted move magnitude (move size / ATR).
EXPECTED EFFECT: Very large moves produce stronger directional continuation.
TRADEABLE USE: Directional bias for position sizing or entry direction.
```

### 8.2 Link Quality Assessment

| Link | Assessment | Evidence |
|---|---|---|
| Market phenomenon | GOOD | Post-shock drift is a documented phenomenon |
| Mechanism | BORDERLINE | Forced repositioning is plausible but unverifiable with OHLC data |
| Observable | GOOD | Volatility-adjusted magnitude is deterministic from OHLC |
| Expected effect | BORDERLINE | Directional continuation plausible but may reflect momentum |
| Tradeable use | GOOD | Directional bias application is clear |

**Weakest link:** Mechanism — forced repositioning is a hypothesis, not a proven mechanism. The observable may capture simple momentum.

### 8.3 Semantic Integrity

**Critical question:** Is this genuinely distinct from "larger moves continue more" (generic momentum)?

**Analysis:** The observable (volatility-adjusted magnitude) is distinct from standard momentum (return-based lookback). Standard momentum measures persistent trends over a lookback period. CAND-104 measures the SIZE of a SINGLE move relative to recent volatility. These are different observables with different economic rationales.

However, the MECHANISM (forced repositioning) is inferred. The observable may capture simple momentum or trend continuation. The distinction must be explicitly acknowledged.

---

## 9. CAND-104 Prior-Art Comparison

| Prior candidate | Shared mechanism | Shared observable | Shared temporal structure | Material difference |
|---|---|---|---|---|
| CAND-095 (Shock magnitude asymmetry) | Shock response | Shock direction | Event-level | CAND-095 tested shock DIRECTION (up vs down). CAND-104 tests shock MAGNITUDE (size/ATR). Different observable. |
| CAND-096 (Volatility acceleration) | Volatility dynamics | Rate of vol change | Rolling window | CAND-096 measured vol ACCELERATION. CAND-104 measures move MAGNITUDE. Different observable. |
| CAND-091 (Directional exhaustion) | Cumulative directional effects | Cumulative directional moves | Event-level | CAND-091 tested CUMULATIVE exhaustion. CAND-104 tests SINGLE large move continuation. Different temporal structure. |
| CAND-092 (Event information decay) | Event recency | Time since single event | Event-level | CAND-092 measured time since event. CAND-104 measures move MAGNITUDE. Different observable. |
| CAND-102 (Directional persistence) | Cumulative directional effects | Run length | Event-level | CAND-102 tested run LENGTH. CAND-104 tests single move MAGNITUDE. Different observable. |
| DISC-021 (Mean reversion) | Displacement/reversion | Z-score displacement | Event-level | DISC-021 tested REVERSION after displacement. CAND-104 tests CONTINUATION after magnitude. OPPOSITE hypothesis. |

### 9.1 Critical Question

> Does CAND-104 introduce a genuinely new economic mechanism, or is it simply "larger shocks may continue" — a generic momentum hypothesis?

**Answer:** The OBSERVABLE is genuinely new (volatility-adjusted magnitude vs standard momentum return). The MECHANISM (forced repositioning) is a specific economic explanation that differs from generic momentum. However, the mechanism is inferred and unverifiable with OHLC data.

**Key distinction from CAND-095:** CAND-095 tested whether shock DIRECTION matters (up vs down). CAND-104 tests whether shock MAGNITUDE matters (large vs small). These are different questions about the same class of events.

**Key distinction from DISC-021:** DISC-021 tested REVERSION after extreme displacement. CAND-104 tests CONTINUATION after large magnitude. These are OPPOSITE hypotheses.

### 9.2 Novelty Verdict

> **MATERIALLY DISTINCT BUT ADJACENT**

The observable is genuinely distinct from prior work. The mechanism is plausible but inferred. The candidate is adjacent to momentum research but tests a different observable class (single-move magnitude vs persistent trend).

---

## 10. CAND-104 Mechanism–Observable Challenge

### 10.1 Mechanism Independence

**What phenomenon exists independently?**

Post-shock drift is documented in market microstructure literature. Forced repositioning after large moves is a recognized phenomenon.

### 10.2 Proxy Challenge

**How can the observable occur without the mechanism?**

Very large moves could reflect:
1. Trend climax (reversal, not continuation)
2. Volatility clustering (large moves cluster with other large moves)
3. News/event reaction (transient, not persistent)

### 10.3 Alternative Explanation

**What competing process could produce the same observable?**

1. Simple momentum (prices that went up continue going up)
2. Volatility clustering
3. Mean reversion (opposite of hypothesized direction)
4. Sample composition (few large moves driving the result)

### 10.4 Observable Fidelity

**Why does the observable reasonably measure the mechanism?**

Volatility-adjusted magnitude directly captures the core hypothesis. However, the mechanism (forced repositioning) is inferred.

### 10.5 Expected-Effect Bridge

**Why should the mechanism alter subsequent outcomes?**

If forced repositioning takes time to complete, directional drift should persist proportional to move magnitude.

### 10.6 Falsification

**What would clearly contradict the hypothesis?**

If very large moves produce NO directional bias, or produce REVERSAL bias, the hypothesis is contradicted.

### 10.7 Tradeability

**What prevents the information surviving costs?**

1. Timing: identifying the magnitude requires waiting for the move
2. Frequency: very large moves are rare
3. Costs: directional bias may be small
4. Regime dependence: effect may exist only in trending periods

### 10.8 Base Rate

**Why should G1 resources be spent?**

CAND-095 tested direction, not magnitude. This tests a different observable class. The forced-repositioning mechanism is economically plausible.

### 10.9 Confidence Dimensions

- **Mechanism Confidence:** MODERATE
- **Proxy Confidence:** MODERATE
- **Observable Information Potential:** MODERATE

---

## 11. Cross-Candidate Comparison

| Dimension | CAND-103 | CAND-104 |
|---|---|---|
| Mechanism | Cross-timeframe coordination | Forced repositioning after large moves |
| Observable | Number of timeframe levels broken | Volatility-adjusted move magnitude |
| Primary risk | Trend confound | Momentum confound |
| Novelty | CLEARLY NOVEL | MATERIALLY DISTINCT BUT ADJACENT |
| Mechanism Confidence | MODERATE | MODERATE |
| Proxy Confidence | MODERATE | MODERATE |
| Observable Information Potential | MODERATE | MODERATE |

**Redundancy check:** CAND-103 and CAND-104 are NOT redundant. They test different mechanisms, different observables, and different economic questions.

---

## 12. Data Feasibility

### CAND-103

**Required data:**
- M1 OHLC: YES
- Multi-timeframe aggregation: YES (deterministic from M1)
- Break detection: YES
- Forward return distribution: YES

**Data feasibility:** YES

### CAND-104

**Required data:**
- M1 OHLC: YES
- ATR computation: YES
- Move magnitude: YES
- Forward return distribution: YES

**Data feasibility:** YES

---

## 13. Parameter Audit

### CAND-103

| Parameter | Classification | Status |
|---|---|---|
| Timeframe definitions | STRUCTURAL | Pre-declare before G1 (e.g., M15, H1, H4) |
| Break threshold | STRUCTURAL | Pre-declare before G1 |
| Outcome horizon | STRUCTURAL | Pre-declare before G1 |
| Synchronization window | STRUCTURAL | Pre-declare before G1 (how close in time must breaks be) |

### CAND-104

| Parameter | Classification | Status |
|---|---|---|
| ATR lookback | STRUCTURAL | Pre-declare before G1 |
| Magnitude threshold | STRUCTURAL | Pre-declare before G1 |
| Outcome horizon | STRUCTURAL | Pre-declare before G1 |
| Minimum event spacing | STRUCTURAL | Pre-declare before G1 |

All parameters are STRUCTURAL and can be frozen before G1.

---

## 14. Final G1-Readiness Decisions

### CAND-103: Multi-Timeframe Break Coordination

| Criterion | Status |
|---|---|
| Mechanism novelty | CLEARLY NOVEL |
| Observable novelty | CLEARLY NOVEL |
| Temporal integrity | PASS (with higher-timeframe closure concern for G1) |
| Data feasibility | YES |
| Parameter discipline | ALL STRUCTURAL |
| Mechanism confidence | MODERATE |
| Proxy confidence | MODERATE |
| Observable information potential | MODERATE |

> **PASS — G1 ELIGIBLE**

### CAND-104: Post-Magnitude Directional Drift

| Criterion | Status |
|---|---|
| Mechanism novelty | MATERIALLY DISTINCT BUT ADJACENT |
| Observable novelty | CLEARLY NOVEL |
| Temporal integrity | PASS |
| Data feasibility | YES |
| Parameter discipline | ALL STRUCTURAL |
| Mechanism confidence | MODERATE |
| Proxy confidence | MODERATE |
| Observable information potential | MODERATE |

> **PASS — G1 ELIGIBLE**

---

## 15. Governance Conclusion

### V35 G0 INTEGRITY AUDIT — RESULT

| Candidate | Mechanism Novelty | Observable Novelty | Temporal Integrity | Data Feasible | Mechanism Confidence | Proxy Confidence | Final Disposition |
|---|---|---|---|---|---|---|---|
| CAND-103 | CLEARLY NOVEL | CLEARLY NOVEL | PASS | YES | MODERATE | MODERATE | **G1 ELIGIBLE** |
| CAND-104 | MATERIALLY DISTINCT BUT ADJACENT | CLEARLY NOVEL | PASS | YES | MODERATE | MODERATE | **G1 ELIGIBLE** |

### CAND-103

**Strongest prior-art objection:** May simply measure stronger trend state rather than cross-timeframe coordination.

**Strongest novelty argument:** The observable (number of timeframe levels broken) is genuinely distinct from all prior work. No candidate has tested cross-timeframe break coordination.

**Mechanism challenge:** MODERATE confidence. The coordination mechanism is plausible but inferred. The trend-confound risk is real but the observable is genuinely distinct.

**Temporal/data risks:** Higher-timeframe bar closure must be handled carefully to avoid look-ahead bias. This is a G1-implementation concern.

**Final verdict:** PASS — G1 ELIGIBLE

### CAND-104

**Strongest prior-art objection:** May simply be "larger moves continue more" — a generic momentum hypothesis.

**Why magnitude is distinct from prior shock research:** CAND-095 tested shock DIRECTION (up vs down). CAND-104 tests shock MAGNITUDE (size/ATR). These are different observable classes. Standard momentum uses return-based lookback measures; CAND-104 uses single-move volatility-adjusted magnitude.

**Mechanism challenge:** MODERATE confidence. The forced-repositioning mechanism is plausible but unverifiable with OHLC data. The momentum-confound risk is real.

**Final verdict:** PASS — G1 ELIGIBLE

### Cross-Candidate Conclusion

Both candidates survive the integrity audit. **2 G1-eligible candidates.**

### Governance Verification

- ✅ No G1 executed
- ✅ No outcome analysis
- ✅ No optimization
- ✅ No closed candidate reopened
- ✅ No CAND-099 inversion
- ✅ No relational testing
- ✅ No APEX execution
- ✅ No protected runtime inspection

### Files Changed

| File | Purpose |
|---|---|
| `output/research_discovery/QUANTFORGE_V35_G0_INTEGRITY_AUDIT_V1.md` | Integrity audit artifact |
| `docs/SESSION_HANDOFF.md` | Updated with audit results |
| `research/knowledge/RESEARCH_DISCOVERY_DATABASE.md` | Audit disposition recorded |
| `research/knowledge/RESEARCH_TIMELINE.md` | Audit timeline entry |

### Commit

SHA: pending

### SESSION_HANDOFF

Updated and verified.

### Next Permitted Task

> **V35 G1 — ECONOMIC PLAUSIBILITY SCREEN for CAND-103 and CAND-104**
