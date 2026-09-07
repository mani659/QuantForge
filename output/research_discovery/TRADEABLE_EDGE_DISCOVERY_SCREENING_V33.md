# TRADEABLE EDGE DISCOVERY SCREENING — V33

## 1. G0 Status

> V33 G0 COMPLETE — 3 NEW CANDIDATES FROM KNOWLEDGE-GAP ANALYSIS

Date: 2026-09-01
Market: USATECHIDXUSD M1
Data range: 2023-09-01 to 2026-07-10 (~2.9 years)

## 2. V30–V32 Lessons Applied

The following accumulated negative knowledge explicitly informed V33 discovery:

1. **Conditional information is common; monetizable economics are rare.** Large N and positive treatment-vs-control separation do not guarantee tradeable Alpha.

2. **Static thresholds repeatedly fail.** No `indicator > X` hypothesis has survived G1.

3. **Dynamic transitions are more interesting but still frequentlyuneconomic.** V26–V32 provide multiple examples.

4. **State objects can be genuinely informative without being tradeable.** CAND-077/081/083 remain governed examples.

5. **Individually interesting States may not combine positively.** SEED-002: CAND-083 + CAND-081 = NO INCREMENTAL INFORMATION.

6. **Candidate redundancy is a real risk.** CAND-087 ≈ CAND-090, CAND-093 ≈ CAND-094, CAND-097 ≈ DISC-021.

7. **Validated scientific primitives do not automatically produce economic modules.** APEX contains many valid M1/M2 findings with M3/M4 = 0.

8. **Negative knowledge is an asset.** Use it to identify what NOT to repeat.

9. **Shock-magnitude asymmetry does not produce directional downstream advantage.** CAND-095: DOWN slightly better than UP, contradicting hypothesis.

10. **Volatility deceleration outperforms acceleration.** CAND-096: opposite of hypothesized direction. Genuine conditional information but wrong direction.

## 3. Cross-Research Knowledge Base

### QuantForge RF (V19–V32)

88 candidates registered. 0 G2 promotions. 3 State Review Eligible objects (CAND-077/081/083). 24 negative economic findings. 16 scientific primitives. 3 State Observations.

### APEX_CORE

12 objects. 6 validated scientific primitives (HIGH_VOL distribution/persistence/predictability, session-transition LNO distribution/scale, BTC transferability). ZERO validated economic modules (M3=0, M4=0).

### SMC_STREAM

7 objects. BOS+OB (M4 FAILED), CHOCH (M3 FAILED). Validated event extraction but failed economics.

### Custom-bot Observations

1 object. PROVISIONAL / NOT VALIDATED.

### State Library

| Candidate | Mechanism | Classification |
|---|---|---|
| CAND-059 | First Touch > Subsequent Touch | STATE-ARTIFACT |
| CAND-065 | Deep Sweep > Shallow Sweep | STATE OBSERVATION |
| CAND-069 | Mid-session > Morning | STATE OBSERVATION |
| CAND-077 | Vol compression → expansion | STATE REVIEW ELIGIBLE |
| CAND-079 | Gold vol transition → Tech | STATE OBSERVATION |
| CAND-081 | Structural level failure trap | STATE REVIEW ELIGIBLE |
| CAND-083 | Cumulative rejection pressure | STATE REVIEW ELIGIBLE |

## 4. Knowledge-Gap Analysis

### Mechanism Families Heavily Explored (>5 candidates each)

| Family | Count | Status |
|---|---|---|
| Event Sequence | 14 | Multiple closures, diminishing returns |
| Cross-Market | 11 | Mostly blocked or negative |
| Structural | 10 | Mixed, CAND-081/083 State-eligible |
| Market Microstructure | 9 | Mostly negative or blocked |
| Volatility | 7 | CAND-077 State-eligible, CAND-096 contradicted |
| Settlement | 3 | All economically negative |

### Mechanism Families Under-Explored (<3 candidates)

| Family | Count | Status |
|---|---|---|
| Execution Stress | 0 | Never tested |
| Event-Cluster Dynamics | 0 | Never tested (CAND-092 tested single-event recency) |
| Volatility Regime Transition Quality | 0 | CAND-077 tested regime state, not transition quality |
| Positioning Dynamics | 0 | CAND-081/083 touch on this but focus on structural failure |
| Information Absorption Capacity | 0 | Never tested as standalone mechanism |

### V32 Deferred Gaps

| Gap | V32 Status | V33 Status |
|---|---|---|
| Execution stress and spread dynamics | DEFERRED | **ADDRESSABLE** |
| Event-cluster response decay | DEFERRED | **ADDRESSABLE** |

### Genuine Blind Spots Identified

1. **Event density effects on response quality.** No candidate tests how clustering of structural events degrades the market's response capacity. CAND-092 tested time-since-single-event; event clustering is a distinct mechanism.

2. **Volatility regime transition quality.** CAND-077 tested compressed→expanded as a state. No candidate tests the SPEED or SMOOTHNESS of the transition itself. A smooth transition may indicate orderly repricing; a sharp transition may indicate stress.

3. **Execution stress as a conditioning variable.** Spread dynamics after large moves have been observed in custom-bot research but never tested as a formal hypothesis. Wider spreads may indicate forced positioning and urgency.

## 5. Candidate 1

### Candidate ID

CAND-098

### Name

Event-Cluster Response Degradation

### Expression Class

STATE / CONDITION

### Mechanism Family

Event-Cluster Dynamics

### Why This Gap Exists

No candidate tests how the CLUSTERING of structural events (multiple events in quick succession) degrades the market's capacity to produce a clean directional response to each subsequent event. CAND-092 tested time-since-single-event (recency); event clustering tests the cumulative effect of multiple recent events.

### Prior Research Coverage

- CAND-092 (Event-Information Decay): tested recency of a single prior event. CLOSED — ECONOMICALLY NEGATIVE.
- 14 Event Sequence candidates: mostly tested event detection, not cluster effects.
- No candidate has tested event density / clustering as a conditioning variable.

### Pre-State

Market has experienced one or more structural events (breaks, rejections) within a defined recent window.

### Transition / Evolution

The NUMBER of structural events within the lookback window increases. Each additional event represents additional information absorption by the market.

### Post-State

The market's response capacity to a new structural event is potentially degraded by the cumulative processing of recent events.

### Participant / Market Constraint

When multiple events cluster, participants must repeatedly reassess positioning. Each event adds uncertainty and forces re-evaluation. The cumulative effect may:
- Widen spreads (execution stress)
- Increase position confusion (information overload)
- Reduce directional conviction (uncertainty accumulation)
- Create forced exits from previous event-conditioned positions

### Economic Mechanism

The economic mechanism is:

> Event clustering creates information overload and positioning confusion, reducing the market's ability to produce a clean directional response to each new event.

This is distinct from:
- CAND-092 (single-event recency): tests time since ONE event, not cumulative effect of MULTIPLE events
- CAND-091 (directional exhaustion): tests cumulative directional moves, not event clustering
- CAND-083 (rejection accumulation): tests rejection count at a structural level, not event density across the market

### Economic Consequence

If event clustering degrades response quality, then:
- Events occurring in clusters should produce wider distributions (more noise)
- Events occurring in isolation should produce tighter distributions (cleaner signal)
- The MEAN response may not change, but the SIGNAL-TO-NOISE ratio should degrade with cluster density

### Core Hypothesis

> Structural events occurring in high-density clusters produce wider outcome distributions and lower signal-to-noise ratios compared to events occurring in isolation.

### Observable Variables

Available in USATECHIDXUSD M1 data:
- Structural event detection (breaks, rejections) — deterministic from OHLC
- Event timestamps — deterministic
- Event cluster density — count of events within N-bar lookback
- Forward return distribution — deterministic from OHLC

### Observable vs Inferred vs Unknown

- Observable: event count within lookback window, forward returns
- Inferred: information overload, positioning confusion (theoretical mechanism)
- Unknown: exact threshold for cluster density, optimal lookback window

### Exact Setup

- Event: any structural break (bar-to-bar move > threshold)
- Treatment: event occurs when ≥K other structural events have occurred within L bars
- Control: event occurs when <K other structural events have occurred within L bars
- Lookback: L bars (to be frozen before G1)
- Cluster threshold: K events (to be frozen before G1)

### Exact Confirmation

Treatment wider distribution than control. Treatment lower signal-to-noise than control.

### Exact Entry

Not applicable — this is a STATE / CONDITION, not a standalone Alpha.

### Exact Exit / Evaluation

Forward return distribution measured over H bars after event (to be frozen before G1).

### Direction

No directional prediction. This is a distributional hypothesis: cluster events produce wider distributions.

### Rearm Rule

After each event, re-evaluate cluster density for the next event.

### Dynamic-vs-Static Rationale

The hypothesis REQUIRES the temporal clustering dimension. A static count of "total events" would not capture the density effect. The cluster density must be measured within a rolling window relative to each event.

### Expected Distribution Change

Treatment (clustered events): wider standard deviation, heavier tails, lower signal-to-noise.
Control (isolated events): tighter standard deviation, lighter tails, higher signal-to-noise.

### Economic Headroom

If cluster events produce significantly wider distributions, this could be used as:
- A STATE filter to avoid trading during high-density clusters
- A risk-management signal to reduce position size during clusters
- A conditional modifier for other Alpha candidates

### Conceptual Counterfactual

Events occurring when no other events have occurred recently (isolated events). Same event class, different cluster context.

### Counterfactual Discrimination

The counterfactual is well-defined: same structural event, different cluster density. The treatment and control share the same event definition but differ in the number of recent prior events.

### Data Availability

USATECHIDXUSD M1: sufficient historical data for event detection and cluster measurement.

### Causal Observability

Event timestamps and cluster density are directly observable. Forward returns are directly observable. The mechanism (information overload) is inferred but the observable proxy (cluster density) is measurable.

### Prior-Art

No QuantForge candidate has tested event-cluster effects. CAND-092 tested single-event recency. Event-sequence research (14 candidates) focused on event detection, not cluster dynamics.

### Closed-Line Check

- CAND-092: tested time-since-single-event. Different mechanism.
- CAND-091: tested cumulative directional exhaustion. Different mechanism.
- CAND-083: tested rejection count at structural level. Different mechanism.
- None of the closed Event Sequence candidates tested cluster density.

### Standalone Potential

Low — this is primarily a STATE / CONDITION that modifies the economics of other events.

### Rare-Event Potential

Low — cluster events are common, not rare.

### State Potential

HIGH — event cluster density could serve as a market-state indicator that modifies the economics of any downstream Alpha.

### Regime Potential

MODERATE — high cluster density may define a "stressed" regime.

### Modular Potential

HIGH — could improve entry quality by avoiding cluster conditions, or improve risk management by reducing exposure during clusters.

### Expected Failure Mode

The cluster density threshold may be too sensitive to parameterization. If the result depends heavily on the specific K and L values, the hypothesis may not be robust.

### Proposed G1 Measurement

Treatment vs control comparison on forward return distribution (mean, median, standard deviation, skewness, kurtosis, win rate). Primary evaluation: distribution width (standard deviation) and signal-to-noise.

### G0 Quality Decision

> G1 ELIGIBLE — genuinely distinct mechanism, observable, testable, not a variant of prior candidates.

---

## 6. Candidate 2

### Candidate ID

CAND-099

### Name

Volatility Regime Transition Quality

### Expression Class

STATE / CONDITION

### Mechanism Family

Volatility Dynamics

### Why This Gap Exists

CAND-077 tested volatility regime STATE (compressed vs expanded). No candidate tests the QUALITY of the transition itself — how smoothly or abruptly the market moves from one volatility regime to another. A smooth transition may indicate orderly repricing; a sharp transition may indicate stress and forced positioning.

### Prior Research Coverage

- CAND-077 (Vol Compression → Expansion): tested regime STATE. STATE REVIEW ELIGIBLE (+1.67 bps delta).
- CAND-080 (Vol Regime Quality Transition): attempted to test transition quality but failed due to zero events in counterfactual.
- CAND-096 (Volatility Acceleration Gradient): tested rate of change of volatility. CLOSED — HYPOTHESIS CONTRADICTED.

### Pre-State

Market is in a defined volatility regime (e.g., compressed).

### Transition / Evolution

The volatility regime changes from compressed to expanded (or vice versa). The TRANSITION itself has measurable quality characteristics:
- Speed: how quickly the regime changes (number of bars)
- Smoothness: how orderly the transition is (variance of the transition path)
- Completeness: whether the transition reaches a stable new regime or overshoots

### Post-State

Market enters a new volatility regime. The quality of the transition may affect the economics of subsequent events.

### Participant / Market Constraint

The transition quality reflects HOW the market processes the regime change:
- Smooth transition: orderly repricing, participants adjust gradually, information is absorbed efficiently
- Sharp transition: forced repositioning, participants are caught off-guard, information is absorbed under stress
- Incomplete transition: uncertainty about the new regime, participants hesitate

### Economic Mechanism

The economic mechanism is:

> The quality (smoothness, speed, completeness) of a volatility regime transition reflects the degree of participant preparedness and orderly repricing, which affects the economics of subsequent events in the new regime.

This is distinct from:
- CAND-077: tested regime STATE (compressed vs expanded), not transition quality
- CAND-080: attempted transition quality but failed due to zero events
- CAND-096: tested rate of change (acceleration), not transition quality

### Economic Consequence

If transition quality matters, then:
- Smooth transitions may produce better subsequent economics (orderly repricing)
- Sharp transitions may produce worse subsequent economics (stress, forced positioning)
- The transition quality could serve as a State indicator for downstream Alpha candidates

### Core Hypothesis

> The smoothness of a volatility regime transition predicts the quality of subsequent market behavior. Smooth transitions produce tighter distributions; sharp transitions produce wider distributions.

### Observable Variables

Available in USATECHIDXUSD M1 data:
- Volatility regime detection (ATR percentile or similar) — deterministic from OHLC
- Transition detection (regime change point) — deterministic
- Transition smoothness: variance of the transition path (variance of ATR changes during transition)
- Transition speed: number of bars from regime A to regime B
- Forward return distribution — deterministic from OHLC

### Observable vs Inferred vs Unknown

- Observable: transition speed, transition path variance, forward returns
- Inferred: participant preparedness, orderly repricing (theoretical mechanism)
- Unknown: optimal smoothness threshold, transition detection method

### Exact Setup

- Event: volatility regime transition (compressed → expanded or expanded → compressed)
- Treatment: smooth transition (low path variance during transition)
- Control: sharp transition (high path variance during transition)
- Smoothness measure: variance of ATR changes during the transition window

### Exact Confirmation

Smooth transitions produce tighter forward distributions than sharp transitions.

### Exact Entry

Not applicable — this is a STATE / CONDITION, not a standalone Alpha.

### Exact Exit / Evaluation

Forward return distribution measured over H bars after transition completes.

### Direction

No directional prediction. This is a distributional hypothesis: smooth transitions produce tighter distributions.

### Rearm Rule

After each regime transition, evaluate transition quality.

### Dynamic-vs-Static Rationale

The hypothesis REQUIRES the transition quality dimension. A static regime state (CAND-077) does not capture how the market arrived at the new regime. The transition path itself carries information.

### Expected Distribution Change

Smooth transitions: tighter standard deviation, lighter tails, higher signal-to-noise.
Sharp transitions: wider standard deviation, heavier tails, lower signal-to-noise.

### Economic Headroom

If transition quality predicts distribution characteristics, this could serve as:
- A State filter for downstream Alpha candidates
- A risk-management signal (reduce exposure after sharp transitions)
- A regime-quality indicator

### Conceptual Counterfactual

Sharp volatility regime transitions (same regime change, different transition quality).

### Counterfactual Discrimination

Well-defined: same regime change, different transition quality. Treatment and control share the same regime transition but differ in transition path characteristics.

### Data Availability

USATECHIDXUSD M1: sufficient historical data for volatility regime detection and transition quality measurement.

### Causal Observability

Transition speed and path variance are directly observable. Forward returns are directly observable. The mechanism (participant preparedness) is inferred but the observable proxy (transition quality) is measurable.

### Prior-Art

- CAND-077: tested regime STATE, not transition quality
- CAND-080: attempted transition quality but failed (zero events)
- CAND-096: tested acceleration (rate of change), not transition quality
- No QuantForge candidate has successfully tested transition quality

### Closed-Line Check

- CAND-077: STATE REVIEW ELIGIBLE — regime state. Different mechanism.
- CAND-080: CLOSED — zero events in counterfactual. Different mechanism.
- CAND-096: CLOSED — HYPOTHESIS CONTRADICTED. Different mechanism (acceleration vs quality).

### Standalone Potential

Low — this is primarily a STATE / CONDITION.

### Rare-Event Potential

Low — regime transitions are moderately frequent.

### State Potential

HIGH — transition quality could serve as a market-state indicator that modifies the economics of downstream events.

### Regime Potential

HIGH — this IS a regime-quality indicator.

### Modular Potential

HIGH — could improve entry quality by conditioning on transition quality, or improve risk management by adjusting exposure after sharp transitions.

### Expected Failure Mode

Transition quality measurement may be too noisy or parameter-sensitive. The smoothness threshold may not be robust across different market conditions.

### Proposed G1 Measurement

Treatment vs control comparison on forward return distribution (mean, median, standard deviation, skewness, kurtosis, win rate). Primary evaluation: distribution width and signal-to-noise.

### G0 Quality Decision

> G1 ELIGIBLE — genuinely distinct mechanism, builds on CAND-077 State knowledge, observable, testable.

---

## 7. Candidate 3

### Candidate ID

CAND-100

### Name

Spread-Conditioned Execution Stress

### Expression Class

STATE / CONDITION

### Mechanism Family

Market Microstructure

### Why This Gap Exists

No candidate has tested spread dynamics as a conditioning variable. Custom-bot research observed that spread conditions may define execution-quality states, but no formal hypothesis was tested. Wider spreads after large moves may indicate forced positioning and urgency, creating a distinct market environment.

### Prior Research Coverage

- Custom-bot observations: spread conditions may define execution-quality states. PROVISIONAL / NOT VALIDATED.
- CAND-042 (Correlated Liquidity-Shock Reversion): COMPONENT-CANDIDATE, N=5, not a spread study.
- No QuantForge candidate has tested spread widening as a conditioning variable.

### Pre-State

Market is in a normal spread environment (tight spreads, orderly execution).

### Transition / Evolution

A large move occurs, causing spread widening. The magnitude and duration of spread widening reflects:
- Execution urgency (forced liquidation, margin calls)
- Liquidity withdrawal (market makers pulling quotes)
- Information asymmetry (informed traders dominating)
- Order book imbalance (one-sided pressure)

### Post-State

The market is in a high-spread environment. The spread condition may affect the economics of subsequent events by altering:
- Execution costs
- Position entry quality
- Market maker behavior
- Liquidity availability

### Participant / Market Constraint

Wide spreads create a specific market environment:
- Higher execution costs reduce net economics
- Forced positioning (margin calls, stop-outs) creates predictable flow
- Market makers widen spreads to compensate for adverse selection
- Liquidity withdrawal amplifies price moves
- Information asymmetry increases (informed traders can execute at wide spreads)

### Economic Mechanism

The economic mechanism is:

> Spread widening after a large move reflects forced positioning and liquidity stress, creating a distinct market environment where subsequent events have different economics than during normal spread conditions.

This is distinct from:
- CAND-095 (shock-magnitude asymmetry): tested shock direction, not spread dynamics
- CAND-096 (volatility acceleration): tested volatility rate of change, not execution quality
- CAND-077 (vol compression → expansion): tested volatility regime, not spread regime

### Economic Consequence

If spread conditions matter, then:
- Events during wide-spread periods may have different economics than events during tight-spread periods
- Wide-spread periods may indicate forced positioning that creates predictable subsequent flow
- The spread condition could serve as a State indicator for risk management

### Core Hypothesis

> Events occurring during periods of elevated spread (relative to recent normal) produce different forward return distributions than events occurring during normal spread conditions.

### Observable Variables

Available in USATECHIDXUSD M1 data:
- Spread measurement (bid-ask spread from tick data or OHLC proxy)
- Spread regime: elevated vs normal (relative to recent rolling window)
- Structural events (breaks, rejections) — deterministic from OHLC
- Forward return distribution — deterministic from OHLC

### Observable vs Inferred vs Unknown

- Observable: spread levels, event detection, forward returns
- Inferred: forced positioning, liquidity stress, information asymmetry (theoretical mechanism)
- Unknown: optimal spread threshold, spread measurement method, lookback window

### Exact Setup

- Event: structural break (bar-to-bar move > threshold)
- Treatment: event occurs when spread is elevated (> threshold relative to recent normal)
- Control: event occurs when spread is normal
- Spread measurement: bid-ask spread or OHLC-derived proxy
- Spread threshold: elevation relative to rolling window (to be frozen before G1)

### Exact Confirmation

Events during elevated spread periods produce different forward distributions than events during normal spread periods.

### Exact Entry

Not applicable — this is a STATE / CONDITION, not a standalone Alpha.

### Exact Exit / Evaluation

Forward return distribution measured over H bars after event.

### Direction

No strong directional prediction. The hypothesis is distributional: spread condition affects the economics of subsequent events.

### Rearm Rule

After each event, evaluate spread condition for the next event.

### Dynamic-vs-Static Rationale

The hypothesis REQUIRES the spread condition to be measured relative to recent history. A static spread threshold would not capture the regime-like nature of spread dynamics. The spread must be evaluated in context of recent normal conditions.

### Expected Distribution Change

Elevated spread periods: potentially wider distributions (forced positioning creates noise), potentially different mean (forced liquidation creates predictable flow). Normal spread periods: tighter distributions, more orderly price discovery.

### Economic Headroom

If spread conditions predict distribution characteristics, this could serve as:
- A State filter for downstream Alpha candidates
- A risk-management signal (reduce exposure during wide spreads)
- An execution-quality indicator
- A forced-positioning detector

### Conceptual Counterfactual

Events occurring during normal spread conditions (same event class, different spread environment).

### Counterfactual Discrimination

Well-defined: same structural event, different spread condition. Treatment and control share the same event definition but differ in spread environment.

### Data Availability

USATECHIDXUSD M1: spread data may be available from tick data or can be proxied from OHLC (high-low range as a spread proxy). If actual bid-ask spread is unavailable, the OHLC-based proxy is a valid alternative.

### Causal Observability

Spread levels are observable (or proxyable). Event detection and forward returns are directly observable. The mechanism (forced positioning) is inferred but the observable proxy (spread condition) is measurable.

### Prior-Art

- Custom-bot observations: spread conditions may define execution-quality states. PROVISIONAL.
- No QuantForge candidate has tested spread dynamics as a conditioning variable.
- APEX documented spread conditions as potentially important but no economic expression was tested.

### Closed-Line Check

- No closed QuantForge candidate tested spread dynamics.
- Custom-bot observations are PROVISIONAL / NOT VALIDATED.
- This is a genuinely new mechanism for QuantForge.

### Standalone Potential

Low — this is primarily a STATE / CONDITION.

### Rare-Event Potential

Low — elevated spread periods are moderately frequent.

### State Potential

HIGH — spread condition could serve as a market-state indicator that modifies the economics of downstream events.

### Regime Potential

HIGH — spread regime could define execution-quality states.

### Modular Potential

HIGH — could improve execution quality by avoiding entry during wide spreads, or improve risk management by reducing exposure during liquidity stress.

### Expected Failure Mode

Spread measurement may be noisy or unavailable. If OHLC proxy is used, it may not accurately reflect true bid-ask spread. The spread threshold may be parameter-sensitive.

### Proposed G1 Measurement

Treatment vs control comparison on forward return distribution (mean, median, standard deviation, skewness, kurtosis, win rate). Primary evaluation: distribution width and signal-to-noise.

### G0 Quality Decision

> G1 ELIGIBLE — genuinely distinct mechanism, addresses V32 deferred gap, observable (or proxyable), testable.

---

## 8. Candidate Diversity Audit

| Dimension | CAND-098 | CAND-099 | CAND-100 |
|---|---|---|---|
| Mechanism Family | Event-Cluster Dynamics | Volatility Dynamics | Market Microstructure |
| Expression Class | STATE / CONDITION | STATE / CONDITION | STATE / CONDITION |
| Primary Observable | Event cluster density | Transition path variance | Spread level |
| Temporal Dimension | Rolling window event count | Transition path quality | Spread regime relative to normal |
| Economic Mechanism | Information overload from clustering | Participant preparedness during transitions | Forced positioning from liquidity stress |
| Closest Prior | CAND-092 (single-event recency) | CAND-077 (regime state) | Custom-bot observations (provisional) |
| Distinctness | Tests cumulative multi-event effects, not single-event recency | Tests transition quality, not regime state | Tests execution quality, never tested before |

All three candidates are genuinely distinct in mechanism, observable, and economic rationale.

## 9. Economic Mechanism Comparison

| Candidate | Economic Question | Market Process | Observable Proxy |
|---|---|---|---|
| CAND-098 | Does event clustering degrade response quality? | Information overload, positioning confusion | Event count within rolling window |
| CAND-099 | Does transition quality affect subsequent economics? | Participant preparedness, orderly repricing | Transition path variance |
| CAND-100 | Does spread condition affect event economics? | Forced positioning, liquidity stress | Spread level relative to normal |

The three candidates address different market processes:
- CAND-098: information processing capacity
- CAND-099: regime change quality
- CAND-100: execution environment quality

## 10. Knowledge Gap Coverage

| Gap | Candidate | Coverage |
|---|---|---|
| Event-cluster response decay | CAND-098 | DIRECTLY ADDRESSED |
| Volatility regime transition quality | CAND-099 | DIRECTLY ADDRESSED |
| Execution stress and spread dynamics | CAND-100 | DIRECTLY ADDRESSED |
| Shock-magnitude asymmetry | — | CLOSED (CAND-095) |
| Volatility acceleration | — | CLOSED (CAND-096) |
| Post-shock self-correction | — | CLOSED (CAND-097 = DISC-021) |

## 11. Cross-Research Redundancy Audit

| Candidate | QuantForge RF | APEX_CORE | SMC_STREAM | Custom-Bot |
|---|---|---|---|---|
| CAND-098 | No overlap (CAND-092 = single-event) | No overlap | No overlap | No overlap |
| CAND-099 | CAND-077 related but distinct (state vs quality) | No overlap | No overlap | No overlap |
| CAND-100 | No overlap | APEX observed spread importance (provisional) | No overlap | Custom-bot observed spread conditions |

## 12. V30/V32 Negative Knowledge Used

- CAND-095 failure: shock-magnitude asymmetry does not produce directional advantage → V33 candidates avoid directional asymmetry claims
- CAND-096 failure: volatility deceleration outperforms acceleration → V33 CAND-099 avoids acceleration framing, focuses on transition quality
- CAND-097 failure: mean reversion after shock = DISC-021 → V33 avoids all mean-reversion variants
- SEED-002 failure: condition combinations may not add value → V33 candidates are independent, not combinations
- V30 failures: velocity, exhaustion, recovery variants fail → V33 avoids these families

## 13. State Library Firewall

CAND-077/081/083: NOT MODIFIED, NOT OPTIMIZED, NOT COMBINED

V33 candidates are independent new hypotheses. CAND-099 builds on CAND-077's State knowledge (regime transitions are informative) but tests a materially distinct mechanism (transition quality vs regime state).

## 14. SEED-002 Negative Relational Knowledge

SEED-002: TESTED NEGATIVE — NO INCREMENTAL INFORMATION

V33 does NOT test relational combinations. Each candidate is tested independently.

## 15. APEX RB001–RB004 Firewall

RB001–RB004: DESIGNED / NOT EXECUTED

V33 does not execute or modify APEX branches. V33 candidates are independent of APEX modular research.

## 16. CAND-088 Firewall

CAND-088: CLOSED / HYPOTHESIS CONTRADICTED

Aligned-break observation: EXPLORATORY / PROVISIONAL

V33 does not use aligned-break observation as positive evidence.

## 17. Closed-Line Firewall

All V19–V32 closures preserved. No closed candidate reopened. DISC-021 (Mean Reversion) permanently closed.

## 18. External Research Prior

Custom-bot spread observations: PROVISIONAL / NOT VALIDATED

V33 CAND-100 addresses the same domain (spread dynamics) but formulates an independent, testable hypothesis. The custom-bot observation is provenance, not evidence.

## 19. Data Feasibility

| Candidate | Required Data | Available? |
|---|---|---|
| CAND-098 | OHLC, event detection, timestamps | YES |
| CAND-099 | OHLC, ATR, regime detection | YES |
| CAND-100 | OHLC or tick data, spread measurement | PARTIAL (OHLC proxy available; actual bid-ask may require tick data) |

CAND-100 may require an OHLC-based spread proxy if actual bid-ask data is unavailable. This is a known limitation but not a blocker.

## 20. Protected Forward Runtime

CAND-015/024/035: ACTIVE / PROTECTED / UNTOUCHED

V33 does not inspect forward performance.

## 21. G1

> NOT EXECUTED

## 22. G2

> NOT EXECUTED

## 23. Relational Testing

> NOT EXECUTED

## 24. Modular Bot Experiments

> NOT EXECUTED

## 25. System Assembly

> NOT EXECUTED

## 26. Next Milestone

> V33 G0 INTEGRITY / PRIOR-ART AUDIT
