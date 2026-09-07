# QUANTFORGE — V33 G0 INTEGRITY / PRIOR-ART AUDIT

## 1. Audit Mission

Perform a strict, independent, READ-ONLY integrity and prior-art audit of the three V33 G0 candidates:

- CAND-098 — Event-Cluster Response Degradation
- CAND-099 — Volatility Regime Transition Quality
- CAND-100 — Spread-Conditioned Execution Stress

The objective is to determine whether these candidates are genuinely novel, materially distinct from prior QuantForge research, economically coherent, and sufficiently well-defined to justify future G1 authorization.

This is NOT G1. No experiments were executed. No economic testing was performed.

## 2. Authoritative Repository State

- HEAD: `b7edfca` — `docs: complete V33 G0 knowledge-gap discovery`
- Branch: `main`
- V32: CLOSED / VERIFIED
- V31: CLOSED / VERIFIED
- State Library: CAND-077/081/083 STATE REVIEW ELIGIBLE
- SEED-002: TESTED NEGATIVE
- Forward Runtime: CAND-015/024/035 ACTIVE / PROTECTED / UNTOUCHED
- APEX RB001-RB004: DESIGNED / NOT EXECUTED
- Data limitation: Volume unavailable/zero. Bid/ask/spread: UNAVAILABLE (confirmed in data_feed.py).

## 3. Prior-Art Methodology

For each candidate:
1. Identify closest prior candidate(s)
2. Compare mechanism, observable, temporal structure, economic question
3. Apply adversarial test: "Would a knowledgeable researcher regard this as the same mechanism?"
4. Assess three-layer novelty: mechanism, observable, economic question
5. Determine data feasibility
6. Assign final disposition

## 4. CAND-098 — Event-Cluster Response Degradation

### 4.1 Candidate Definition

- Mechanism: Event clustering degrades market response quality through information overload
- Observable: Count of structural events within N-bar rolling window
- Temporal: Event cluster density measured relative to each event
- Hypothesis: Clustered events produce wider distributions, lower signal-to-noise
- Expression: STATE / CONDITION

### 4.2 Closest Prior Candidates

| Candidate | Mechanism | Observable |
|---|---|---|
| CAND-092 | Event-information decay (recency of single event) | Time since last event |
| CAND-083 | Rejection accumulation at structural level | Rejection count at specific price level |
| CAND-091 | Cumulative directional exhaustion | Cumulative directional move magnitude |
| CAND-089 | Acceptance velocity decay | Velocity of acceptance at structural level |

### 4.3 Three-Layer Novelty Assessment

**Layer A — Mechanism novelty:**
CAND-092 mechanism: "Information content of a prior event decays over time." This is a SINGLE-EVENT, TEMPORAL-DECAY mechanism.
CAND-098 mechanism: "Multiple events in quick succession overload the market's processing capacity." This is a MULTI-EVENT, CUMULATIVE-LOAD mechanism.

These are materially different economic mechanisms:
- CAND-092: "How long ago?" (temporal decay)
- CAND-098: "How many recently?" (cumulative load)

A market can have a single recent event (high CAND-092 recency, low CAND-098 density) or multiple distant events (low CAND-092 recency, high CAND-098 density). The observables are not redundant.

**Layer B — Observable novelty:**
- CAND-092: Time since last event (continuous, single-event)
- CAND-098: Count of events within rolling window (discrete, multi-event)

These are different observables measuring different market properties.

**Layer C — Economic-question novelty:**
- CAND-092: "Does information content of a single event decay in a way that affects downstream economics?"
- CAND-098: "Does clustering of multiple events degrade the market's response capacity?"

Different economic questions. CAND-092 asks about temporal decay of one event. CAND-098 asks about cumulative overload from multiple events.

### 4.4 Adversarial Test

```
Candidate: CAND-098
-> Closest prior: CAND-092
-> Shared mechanism: Both involve event effects on downstream behavior
-> Shared observable: None (time-since vs event-count)
-> Shared temporal structure: Both use rolling windows, but different semantics
-> Shared economic question: No (decay of one event vs overload from many)
-> Material difference: MULTI-EVENT CUMULATIVE LOAD vs SINGLE-EVENT TEMPORAL DECAY
-> Verdict: CLEARLY NOVEL
```

### 4.5 Additional Prior-Art Check

- CAND-083 (rejection accumulation): Tests rejection count at a SPECIFIC STRUCTURAL LEVEL. CAND-098 tests event density ACROSS THE MARKET. Different scope, different mechanism.
- CAND-091 (directional exhaustion): Tests cumulative DIRECTIONAL MOVES. CAND-098 counts structural EVENTS regardless of direction. Different observable.
- 14 Event Sequence candidates: Tested event detection, not cluster dynamics.

### 4.6 Negative-Knowledge Constraints

- CAND-092 CLOSED / ECONOMICALLY NEGATIVE: This tested single-event recency, not multi-event clustering. Does not falsify CAND-098.
- CAND-091 CLOSED / HYPOTHESIS CONTRADICTED: This tested directional exhaustion, not event clustering. Does not falsify CAND-098.
- No prior result directly falsifies the event-clustering hypothesis.

### 4.7 Data Feasibility

- Required: OHLC (available), event detection (deterministic from OHLC), timestamps (available), forward returns (deterministic from OHLC)
- ALL REQUIRED DATA AVAILABLE
- No volume dependency
- No bid/ask dependency

### 4.8 Temporal-Semantic Audit

- Anchor: structural event (bar-to-bar move > threshold)
- Observation: event cluster density (count within N-bar lookback)
- Outcome: forward return distribution over H bars
- No leakage: cluster density computed from PAST events only
- No overlap: outcome window starts after event
- CLEAN temporal structure

### 4.9 Parameter Audit

| Parameter | Status |
|---|---|
| Event threshold (bar-to-bar move > X) | STRUCTURAL — standard break detection |
| Lookback window (N bars) | REQUIRES FREEZE — data-resolution driven |
| Cluster count threshold (K events) | REQUIRES FREEZE — mechanism-driven |
| Outcome horizon (H bars) | REQUIRES FREEZE — data-resolution driven |

Parameters requiring freeze are standard for G1. No optimization needed.

### 4.10 Final Disposition

> **PASS — G1 ELIGIBLE**

CAND-098 is genuinely novel. The multi-event cumulative-load mechanism is materially distinct from CAND-092's single-event temporal-decay mechanism. The observable is different. The economic question is different. Data is available. Temporal structure is clean.

## 5. CAND-099 — Volatility Regime Transition Quality

### 5.1 Candidate Definition

- Mechanism: Transition quality (smoothness) affects subsequent economics through participant preparedness
- Observable: Variance of ATR changes during transition window
- Temporal: Transition detected at regime change point, quality measured during transition
- Hypothesis: Smooth transitions produce tighter distributions; sharp transitions produce wider distributions
- Expression: STATE / CONDITION

### 5.2 Closest Prior Candidates

| Candidate | Mechanism | Observable |
|---|---|---|
| CAND-077 | Volatility regime STATE (compressed vs expanded) | ATR percentile (static state) |
| CAND-096 | Volatility acceleration (rate of change) | Second derivative of ATR |
| CAND-080 | Vol regime quality transition (attempted, failed) | Transition quality (zero events) |

### 5.3 Three-Layer Novelty Assessment

**Layer A — Mechanism novelty:**
CAND-077 mechanism: "Compressed → expanded volatility transition creates a specific market condition." This tests the REGIME STATE.
CAND-099 mechanism: "The smoothness of the transition reflects participant preparedness, affecting subsequent economics." This tests the TRANSITION QUALITY.

Distinction: REGIME CHANGE vs REGIME TRANSITION CHARACTER.

A regime change can be smooth or sharp. CAND-077 does not distinguish between these. CAND-099 does.

However, the adversarial question is: Does "transition quality" represent a new mechanism, or a new descriptive statistic over an already-researched transition?

The mechanism (participant preparedness during transition) is conceptually distinct from CAND-077's mechanism (tight stops cascading during state change). But the observable (variance of ATR changes during transition) may be highly correlated with what CAND-096 already measured (acceleration = rate of ATR change).

**Layer B — Observable novelty:**
- CAND-077: ATR percentile (static state)
- CAND-096: Second derivative of ATR (acceleration)
- CAND-099: Variance of ATR changes during transition (path smoothness)

These are related but distinct:
- Acceleration = direction and magnitude of ATR change
- Path variance = consistency of ATR changes during transition

A smooth transition has consistent positive changes (low variance). A choppy transition has inconsistent changes (high variance). These are different statistical properties.

However, there is a risk that acceleration and path variance are highly correlated, making CAND-099 redundant with CAND-096. The G1 test will determine this empirically.

**Layer C — Economic-question novelty:**
- CAND-077: "Does the compressed-to-expanded transition create different downstream economics?"
- CAND-096: "Does the rate of volatility change affect downstream economics?"
- CAND-099: "Does the smoothness of the transition affect downstream economics?"

These are different questions:
- CAND-077 asks about the transition event itself
- CAND-096 asks about the speed of change
- CAND-099 asks about the quality/consistency of the transition

### 5.4 Adversarial Test

```
Candidate: CAND-099
-> Closest prior: CAND-077 (regime state), CAND-096 (acceleration)
-> Shared mechanism: All involve volatility transitions
-> Shared observable: None (percentile vs acceleration vs path variance)
-> Shared temporal structure: All use transition detection, but different quality measures
-> Shared economic question: Closely related but distinct
-> Material difference: TRANSITION QUALITY (smoothness) vs STATE (regime) vs RATE (acceleration)
-> Verdict: MATERIALLY DISTINCT BUT ADJACENT
```

### 5.5 CAND-080 Precedent

CAND-080 attempted to test "vol regime quality transition" but failed due to ZERO EVENTS in the counterfactual. This is a critical prior result.

CAND-099 must avoid the same fate. The key difference: CAND-080 may have over-constrained the transition definition. CAND-098 uses a broader regime detection method (ATR percentile) which should produce more events.

However, this remains a risk factor. The G1 test will determine whether sufficient events exist.

### 5.6 Negative-Knowledge Constraints

- CAND-077 STATE REVIEW ELIGIBLE: Regime transitions are informative. CAND-099 builds on this knowledge.
- CAND-096 HYPOTHESIS CONTRADICTED: Acceleration outperformed in the opposite direction. CAND-099 does NOT use acceleration; it uses path variance. But the correlation risk remains.
- CAND-080 ZERO EVENTS: Transition quality may be difficult to measure with sufficient sample size.

### 5.7 Data Feasibility

- Required: OHLC (available), ATR computation (deterministic), regime detection (deterministic from ATR), transition detection (deterministic), forward returns (deterministic)
- ALL REQUIRED DATA AVAILABLE
- No volume dependency
- No bid/ask dependency

### 5.8 Temporal-Semantic Audit

- Anchor: volatility regime transition (compressed → expanded or vice versa)
- Observation: transition quality measured during transition window
- Outcome: forward return distribution after transition completes
- No leakage: transition quality computed from transition path (before outcome)
- No overlap: outcome window starts after transition completes
- POTENTIAL ISSUE: Transition window and outcome window may overlap if transition is slow. Must be frozen carefully.

### 5.9 Parameter Audit

| Parameter | Status |
|---|---|
| Regime definition (ATR percentile thresholds) | STRUCTURAL — standard volatility regime |
| Transition detection method | REQUIRES FREEZE — must be deterministic |
| Transition window length | REQUIRES FREEZE — data-resolution driven |
| Smoothness threshold (high vs low variance) | REQUIRES FREEZE — mechanism-driven |
| Outcome horizon (H bars) | REQUIRES FREEZE — data-resolution driven |

### 5.10 Final Disposition

> **PASS — G1 ELIGIBLE**

CAND-099 is materially distinct from CAND-077 (state vs quality) and CAND-096 (acceleration vs path smoothness). The mechanism (participant preparedness during transition) is conceptually distinct. However, the adjacency to CAND-096 is notable — the G1 test must determine whether path variance carries independent information beyond what acceleration already captures. The CAND-080 zero-events precedent is a risk factor but not a disqualifier.

## 6. CAND-100 — Spread-Conditioned Execution Stress

### 6.1 Candidate Definition

- Mechanism: Spread widening reflects forced positioning and liquidity stress
- Observable: Spread level relative to rolling normal
- Temporal: Spread regime evaluated at event time
- Hypothesis: Events during elevated spread periods produce different forward distributions
- Expression: STATE / CONDITION

### 6.2 Data Feasibility — CRITICAL FAILURE

**The core observable (bid-ask spread) is NOT AVAILABLE in the governed dataset.**

Evidence from `research/g6_forward/data_feed.py`:
```python
"bid": "unavailable",
"ask": "unavailable",
"true_spread": "unavailable"
```

SESSION_HANDOFF confirms:
> "Volume data unavailable / zero for both USATECHIDXUSD and XAUUSD M1 data."

The V33 artifact proposes an "OHLC-derived proxy" (high-low range). However:

1. **High-low range is a VOLATILITY measure, not a spread measure.** Using it as a spread proxy would make CAND-100 effectively a volatility-conditioned hypothesis, overlapping with CAND-077 (vol regime) and CAND-096 (vol acceleration).

2. **The mechanism requires actual spread information.** The hypothesis claims spread widening reflects "forced positioning, liquidity stress, information asymmetry." These mechanisms are specific to bid-ask dynamics, not to price range. A high-low range proxy cannot distinguish between:
   - Wide spread due to forced positioning (the hypothesized mechanism)
   - Wide range due to normal volatility (already tested by CAND-077/096)

3. **The OHLC proxy conflates two different market properties.** If the observable is just volatility in disguise, the hypothesis collapses into a retest of CAND-077 or CAND-096 under different terminology.

### 6.3 Adversarial Test

```
Candidate: CAND-100
-> Closest prior: Custom-bot spread observations (PROVISIONAL)
-> Shared mechanism: Spread as execution-quality indicator
-> Shared observable: UNAVAILABLE (bid/ask spread not in dataset)
-> Proposed proxy: High-low range (= volatility, not spread)
-> Shared economic question: If proxy is used, overlaps with vol research
-> Material difference: CANNOT BE ASSESSED — core observable missing
-> Verdict: DATA INFEASIBLE
```

### 6.4 Why the OHLC Proxy Fails

The V33 artifact states:
> "Spread measurement: bid-ask spread or OHLC-derived proxy"

But this conflates two fundamentally different market properties:

| Property | What it measures | Available? |
|---|---|---|
| Bid-ask spread | Execution cost, liquidity, information asymmetry | NO |
| High-low range | Price volatility, directional movement | YES |

Using high-low range as a spread proxy would test:
> "Do events during high-volatility periods produce different distributions?"

This is EXACTLY what CAND-077 (vol regime) and CAND-096 (vol acceleration) already test. The mechanism (forced positioning, liquidity stress) requires actual spread information that the proxy cannot provide.

### 6.5 Negative-Knowledge Constraints

- Custom-bot observations: PROVISIONAL / NOT VALIDATED. The observation that "spread conditions may define execution-quality states" was never tested with actual spread data.
- No prior QuantForge candidate tested spread dynamics. But the reason is data availability, not lack of interest.

### 6.6 Final Disposition

> **FAIL — DATA INFEASIBLE**

The core observable (bid-ask spread) is not available in the governed dataset. The proposed OHLC proxy (high-low range) is a volatility measure, not a spread measure, and would collapse the hypothesis into existing volatility research (CAND-077/CAND-096). The mechanism (forced positioning, liquidity stress) requires actual spread information that cannot be reconstructed from OHLC alone.

CAND-100 cannot proceed to G1 in its current form. If bid-ask data becomes available in the future, the hypothesis could be reformulated. But under current data constraints, it is not testable.

## 7. Cross-Candidate Semantic Comparison

| Dimension | CAND-098 | CAND-099 | CAND-100 |
|---|---|---|---|
| Mechanism | Information overload from clustering | Participant preparedness during transitions | Forced positioning from spread stress |
| Observable | Event count in rolling window | Path variance of ATR changes | Spread level (UNAVAILABLE) |
| Closest prior | CAND-092 (single-event recency) | CAND-077 (regime state), CAND-096 (acceleration) | Custom-bot observations (provisional) |
| Novelty | CLEARLY NOVEL | MATERIALLY DISTINCT BUT ADJACENT | DATA INFEASIBLE |
| G1 eligible | YES | YES | NO |

## 8. Data-Feasibility Audit

| Candidate | Required Data | Available? | Blocker? |
|---|---|---|---|
| CAND-098 | OHLC, event detection, timestamps | YES | No |
| CAND-099 | OHLC, ATR, regime detection | YES | No |
| CAND-100 | Bid-ask spread | NO | YES — core observable unavailable |

## 9. Temporal-Semantic Audit

| Candidate | Anchor | Observation | Outcome | Leakage Risk |
|---|---|---|---|---|
| CAND-098 | Structural event | Cluster density (past events) | Forward returns | LOW — past events only |
| CAND-099 | Regime transition | Transition quality (during transition) | Forward returns | MODERATE — transition window may overlap outcome |
| CAND-100 | Structural event | Spread regime (at event time) | Forward returns | N/A — data infeasible |

## 10. Parameter Audit

| Candidate | Parameters Requiring Freeze |
|---|---|
| CAND-098 | Lookback window, cluster count threshold, outcome horizon |
| CAND-099 | Regime thresholds, transition detection method, transition window, smoothness threshold, outcome horizon |
| CAND-100 | N/A — not G1-eligible |

## 11. Negative-Knowledge Constraints

| Prior Finding | Constrains | Impact |
|---|---|---|
| CAND-092 CLOSED (economically negative) | CAND-098 | Does not falsify — different mechanism (single vs multi-event) |
| CAND-083 STATE REVIEW ELIGIBLE | CAND-098 | Does not falsify — different scope (structural level vs market-wide) |
| CAND-077 STATE REVIEW ELIGIBLE | CAND-099 | Supports — regime transitions are informative |
| CAND-096 HYPOTHESIS CONTRADICTED | CAND-099 | Adjacent risk — path variance may correlate with acceleration |
| CAND-080 ZERO EVENTS | CAND-099 | Risk factor — transition quality may be difficult to measure |
| Custom-bot spread observations | CAND-100 | Does not help — data unavailable |

## 12. Final G1-Readiness Disposition

| Candidate | Disposition | Rationale |
|---|---|---|
| CAND-098 | **PASS — G1 ELIGIBLE** | Clearly novel mechanism, distinct observable, different economic question, data available |
| CAND-099 | **PASS — G1 ELIGIBLE** | Materially distinct from CAND-077/096, but adjacent — G1 will determine if path variance adds independent information |
| CAND-100 | **FAIL — DATA INFEASIBLE** | Core observable (bid-ask spread) unavailable. OHLC proxy conflates with volatility research. |

## 13. Governance Conclusion

### V33 Candidate Count

> **2 G1-eligible candidates** (CAND-098, CAND-099)
> **1 data-infeasible candidate** (CAND-100)

### V33 G1 Authorization

V33 G1 is authorized for CAND-098 and CAND-099 only.

CAND-100 is NOT authorized for G1. It requires reformulation if bid-ask data becomes available, or permanent closure under current data constraints.

### Candidate Count Rule

The original V33 G0 targeted 2-4 candidates. Two survive the integrity audit. This is within the acceptable range. No replacement for CAND-100 is generated — research integrity overrides quota.

### Firewall Verification

- No experiment executed
- No performance inspected
- No protected candidate touched
- No relational execution
- No APEX execution
- No closed candidate reopened
- No threshold mining
- No optimization
- Forward runtime untouched
- State library unchanged
- SEED-002 preserved
