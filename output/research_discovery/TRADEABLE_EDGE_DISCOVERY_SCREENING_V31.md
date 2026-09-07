# TRADEABLE EDGE DISCOVERY SCREENING — V31

## 1. G0 Status

> **COMPLETE**

V31 G0 — Cross-research knowledge-led fresh mechanism discovery. Three genuinely new candidates from under-explored economic mechanism space.

## 2. Research Context

V31 follows:
- V19–V30 Research Factory completion (35+ candidates, 0 G2 promotions)
- Cross-Research Knowledge Ledger (64 objects across QuantForge RF, APEX, SMC)
- Unified Research Knowledge Ledger V1
- SEED-002 relational experiment: NO INCREMENTAL INFORMATION
- V30 closure: CAND-089 (NO INCREMENTAL INFO), CAND-091 (CONTRADICTED), CAND-090 (REDUNDANT)
- V30 G1 integrity audit: VERIFIED WITH DOCUMENTATION CORRECTIONS
- Relational Research Governance Framework

**Current position:** 35+ candidates reconciled. 0 G2 promotions. 3 State Review Eligible objects. Relational framework governed. SEED-002 tested negative. V30 permanently closed. Forward candidates protected.

## 3. Cross-Research Knowledge Base Used

### Knowledge used to avoid duplication

The following mechanism families are heavily explored and/or have extensive negative knowledge:

| Family | Candidates | Negative Records | Status |
|---|---|---|---|
| Event Sequence | 14 | 12 | EXHAUSTED — avoid |
| Cross-Market | 11 | 8 | EXHAUSTED — avoid |
| Structural | 10 | 10 | EXHAUSTED — avoid |
| Market Microstructure | 9 | 8 | EXHAUSTED — avoid |
| Volatility (direct) | 7+ | 8 | EXHAUSTED — avoid |
| Information Processing Dynamics | 1 | 1 | V30 CAND-089 FAILED |
| Directional Exhaustion Dynamics | 1 | 1 | V30 CAND-091 CONTRADICTED |
| Recovery Quality | 2 | 1 | V29 CAND-087 + V30 CAND-090 REDUNDANT |
| Session raw breakout | — | 1 | APEX C05 CLOSED |
| BOS/OB standalone | — | 1 | SMC M4 FAILED |
| CHOCH standalone | — | 1 | SMC M3 FAILED |
| Funding/carry | — | 1 | APEX C14 CLOSED |
| Simple cross-market direction | — | 1 | V25 CLOSED |

### Knowledge used to identify gaps

| Gap | Source of Evidence | Why Under-Explored |
|---|---|---|
| Information decay after structural events | No candidate tests temporal persistence of event information | Existing candidates test event detection, not information persistence |
| Price-discovery friction at structural levels | APEX validated session-transition LNO distribution (p=0.0001) but no economic expression | Scientific primitive exists; economic pathway untested |
| Path-dependent event severity | CAND-083 tests rejection COUNT but not the SEQUENCE of approaches | Existing candidates count rejections, not characterize approach dynamics |

### Knowledge NOT used as evidence

- Custom-bot operational observations (provisional, unaudited)
- APEX RB001–RB004 (designed, not executed)
- CAND-077 >15 bps exploratory observation (requires new G0)
- CAND-088 aligned-break observation (requires new G0)
- SEED-002 negative result (used only as negative knowledge, not as evidence for V31)

## 4. V30 Lessons

V30 demonstrated three failure modes:

1. **Acceptance velocity decay (CAND-089):** Measuring velocity dynamics at structural levels produced no economic separation. The mechanism may exist but is too weak or the observable proxy is imprecise.

2. **Cumulative directional exhaustion (CAND-091):** Exhaustion WORSENED economics — added dispersion without return. The hypothesis was contradicted.

3. **Recovery quality (CAND-090):** Already represented by CAND-087 — rejected as redundant at G0 integrity audit.

**Lesson applied to V31:** Do not test velocity dynamics, exhaustion dynamics, or recovery quality. Focus on genuinely different mechanism families. Do not assume that "more information about the same event" produces better economics.

## 5. SEED-002 Lesson

SEED-002 tested CAND-083 → CAND-081 and found NO INCREMENTAL INFORMATION. The treatment performed WORSE than the control.

**Lesson applied to V31:** Do not accumulate conditions. Do not assume that combining scientifically interesting observations produces economic value. Each V31 candidate must independently explain WHY economics emerge from its mechanism.

## 6. Knowledge Gaps Identified

### Gap 1: Information Decay After Structural Events

**Source:** No candidate in V19–V30 tests the temporal persistence of event information. Existing candidates detect events (breaks, failures, rejections) but do not measure how quickly the market absorbs the information content of those events.

**Why under-explored:** The research factory has focused on event detection and conditioning, not on the temporal dynamics of information absorption after events.

**Why it might matter economically:** If event information decays at a measurable rate, then the timing of subsequent trades relative to the information decay could affect economics. Markets that have partially absorbed event information may respond differently to new catalysts than markets that retain full event information.

### Gap 2: Price-Discovery Friction at Structural Levels

**Source:** APEX validated session-transition LNO distribution difference (p=0.0001, V07) and LNO scale component (1.65x, V08). These are scientifically validated primitives showing that price behavior at session transitions differs from non-transition periods. But no economic expression has been tested.

**Why under-explored:** APEX focused on scientific validation; economic expression was left unresolved. QuantForge focused on USATECHIDXUSD structural levels, not session-transition microstructure.

**Why it might matter economically:** If price-discovery friction (the market's difficulty in incorporating new price information at structural levels) varies across market conditions, then the quality of price discovery at a level may contain economic information about whether the level will hold or break.

### Gap 3: Path-Dependent Event Severity

**Source:** CAND-083 counts rejections at structural levels (3+ rejections = treatment). But the SEQUENCE and CHARACTER of those rejections — whether price approaches the level cleanly or through choppy, multi-directional movement — is not captured.

**Why under-explored:** The research factory has used rejection count as the primary observable for structural-level interaction. The qualitative character of the approach has not been tested.

**Why it might matter economically:** Two structural levels with the same rejection count but different approach patterns (clean vs choppy) may produce different break economics because the participant populations and positioning differ.

## 7. Candidate 1

### Candidate ID

CAND-092

### Name

Event-Information Decay

### Expression Class

STATE / CONDITION

### Mechanism Family

Information Persistence Dynamics

### Pre-State

A structural event has occurred (breakout, failure, large move). The market has absorbed some but not all of the information content of the event.

### Transition / Evolution

Over time after the event, the market's "memory" of the event decays. The information content of the event becomes progressively less relevant to subsequent price behavior. This decay is not instantaneous — it follows a measurable trajectory.

### Post-State

A low-information-remaining condition exists: the event's information has been largely absorbed by the market. Subsequent catalysts encounter a market that has already incorporated the prior event's implications. Conversely, a high-information-remaining condition means the market has NOT fully absorbed the event, and subsequent catalysts may interact with the unresolved information.

### Participant / Market Constraint

**Information constraint:** Participants process event information at a finite rate. After a structural event, some participants have adjusted their positions while others have not. The rate of adjustment determines how quickly the event's information is incorporated into prices.

**Attention constraint:** Market attention is finite. After a significant event, attention is high and information processing is fast. As time passes, attention shifts to new information, and the residual information from the prior event becomes less actionable.

### Economic Mechanism

When event information remains high (recent event, not yet fully absorbed):
- The market is more sensitive to confirmatory or disconfirmatory information
- Subsequent catalysts in the same direction as the event may have amplified effects (confirmation bias)
- Subsequent catalysts in the opposite direction may have muted effects (the market is "anchored" to the event)

When event information has decayed (older event, largely absorbed):
- The market responds more symmetrically to new catalysts
- The event's directional bias has faded
- The market is in a more "neutral" information state

This creates a conditional economic consequence: the same downstream catalyst may produce different economic outcomes depending on how much information from the prior structural event remains in the market.

### Economic Consequence

- **Conditional catalyst response:** Catalysts during high-information-remaining periods produce larger directional moves in the event direction
- **Asymmetric response:** Confirmatory catalysts are amplified; disconfirmatory catalysts are muted during high-information periods
- **Persistence:** The information-decay trajectory determines how long the event's directional bias persists

### Core Hypothesis

> Structural events occurring during high-information-remaining conditions (recent prior event, information not yet fully absorbed) produce different downstream economics than the same events occurring during low-information-remaining conditions (older prior event, information largely absorbed).

### Observable Variables

1. **Time since last structural event:** Number of bars since the most recent structural break or failure (proxies for information decay stage)
2. **Event magnitude:** Size of the prior event in bps (larger events may have longer information persistence)
3. **Post-event price trajectory:** Whether price has moved toward or away from the event direction since the event (partial absorption indicator)
4. **Information-remaining score:** Composite of time-since-event and post-event trajectory

### Observable vs Hypothesis

**Observable:**
- Time since last event (from timestamps)
- Event magnitude (from OHLC)
- Post-event price movement (from forward prices relative to event)
- Downstream event returns (from forward prices)

**Hypothesis:**
- Participant information processing rate (inferred from time-decay pattern)
- Attention allocation (inferred from post-event trajectory)

**Unknown:**
- Actual participant positioning
- Whether decay is from genuine information absorption or attention shift
- Whether decay rate varies by market regime

### Exact Setup

1. Detect structural level breaks on USATECHIDXUSD M1 (20-bar lookback, 3 bps threshold)
2. For each break, compute the time since the previous structural event (any type)
3. Classify as "high information remaining" (time since event < median) or "low information remaining" (time >= median)
4. Also compute event magnitude and post-event trajectory
5. For each subsequent structural event, check whether it occurs during high or low information-remaining condition
6. Compute forward returns for both groups

### Exact Confirmation

The candidate confirms when:
- A structural event occurs
- AND the market is in a defined information-remaining condition (based on time since prior event)
- AND the event's downstream economics are compared between high and low information conditions

### Exact Entry

At the time of the downstream structural event, enter WITH the event direction.

### Exact Exit / Evaluation

60-minute holding period (consistent with existing protocol).

### Direction

WITH the event direction (long if up break, short if down break).

### Rearm Rule

60-bar minimum between events.

### Dynamic-vs-Static Rationale

This candidate is inherently DYNAMIC because:
- It requires measuring the TIME since a prior event (temporal decay)
- The key signal is the STAGE of information absorption, not a static threshold
- The mechanism depends on the PROCESS of information decay over time
- Removing the temporal aspect would reduce it to "events near other events have different returns" — which is static and likely already captured

The dynamic nature is essential: information decay requires that time has PASSED since the event (process), not just that an event occurred (state).

### Expected Distribution Change

Compared to low-information-remaining conditions:
- High-information periods: larger directional displacement, higher win rate, more asymmetric tails
- Low-information periods: smaller displacement, more symmetric response, lower win rate

### Economic Headroom

Information decay affects all subsequent structural events. If the decay trajectory is economically meaningful, it could condition a significant fraction of events (perhaps 40-60% in each group depending on the median split).

### Conceptual Counterfactual

Structural events occurring during low-information-remaining conditions (sufficient time has passed since the prior event that its information has been largely absorbed). These events occur in a more "neutral" information state.

### Counterfactual Discrimination

The counterfactual discriminates because:
- Same event class (structural break)
- Same market, timeframe, holding period
- Same cost model
- Only difference: time since prior event (information decay stage)
- The mechanism specifically requires information persistence — if information decays instantly, both groups should perform identically

### Data Availability

USATECHIDXUSD M1: ✓ (primary dataset)
All required variables available from OHLC and timestamps.

### Causal Observability

Time since event is directly observable. Event magnitude is observable. Post-event trajectory is observable. The link between time-decay and information absorption is inferred, not directly observable.

### Prior-Art

> **NEW**

No existing candidate tests information decay after structural events.
- CAND-077 tests volatility character transition (regime-level, not event-level decay)
- CAND-081 tests failure trap (event-level state, not temporal decay)
- CAND-083 tests rejection count (accumulation, not temporal persistence)
- CAND-089 tested acceptance velocity (velocity dynamics, not information persistence)
- APEX HIGH_VOL tests volatility persistence (regime-level, not event-information decay)
- No candidate measures time-since-event as a conditioning variable

### Closed-Line Check

- Not Event Sequence (14 closures) — this tests information persistence, not event ordering
- Not Structural (10 closures) — this tests temporal decay, not level quality
- Not Volatility (8 closures) — this tests information decay, not volatility regime
- Not Information Processing Dynamics (CAND-089 closed) — CAND-089 tested velocity at levels; this tests time-decay after events

### Standalone Potential

> **CONDITIONAL** — May serve better as a State/Condition that modifies economics of subsequent events.

### Rare-Event Potential

> **NO** — Information decay is a continuous process, not a rare event.

### State Potential

> **YES** — Information-remaining condition could be a governed State that modifies the economics of subsequent structural events.

### Regime Potential

> **CONDITIONAL** — If information decay varies by market regime, it could be regime-like.

### Modular Potential

> **YES** — Could serve as a timing filter: "trade with events when information from prior events is still elevated."

### Expected Failure Mode

1. Information decay may be too rapid to produce measurable economic differences
2. Time-since-event may be a noisy proxy for genuine information absorption
3. The mechanism may exist but be too small to survive friction
4. The median split may not discriminate meaningful information states

### Proposed G1 Measurement

- Detect structural breaks on USATECHIDXUSD M1
- Compute time since prior event for each break
- Classify by information-remaining condition (above/below median time)
- Compute forward returns for both groups
- Apply 2 bps friction
- Compare mean, median, win rate, distribution

### G0 Quality Decision

> **PASS**

- Genuinely new mechanism (information persistence dynamics)
- Not a disguised prior candidate
- Not a State-library variant
- Not SEED-002 rescue
- Economically plausible (information decay affects catalyst response)
- Observable (time-since-event from timestamps)
- Has credible counterfactual
- Realistic G1 measurement
- No hindsight, no threshold mining, no protected-runtime dependency

---

## 8. Candidate 2

### Candidate ID

CAND-093

### Name

Price-Discovery Friction Gradient

### Expression Class

STATE / CONDITION

### Mechanism Family

Microstructure Information Dynamics

### Pre-State

Price is approaching a structural level. The market is in the process of price discovery — determining whether the level will hold or break.

### Transition / Evolution

As price interacts with the structural level, the SMOOTHNESS of the price trajectory changes. In some cases, price approaches the level cleanly (direct, monotonic approach). In other cases, price oscillates, reverses, and re-approaches multiple times (choppy, non-monotonic approach). The smoothness of the approach reflects the market's clarity about the level's significance.

### Post-State

A price-discovery friction condition exists:
- **Low friction:** Price approached the level cleanly → the market has clear consensus about the level → breaks at low-friction levels are "surprises" with high conviction
- **High friction:** Price approached the level with oscillation → the market is uncertain about the level → breaks at high-friction levels are "expected" with lower conviction

### Participant / Market Constraint

**Consensus constraint:** When price approaches a level cleanly, the market has reached consensus about the level's significance. Participants on both sides have clear expectations. A break at such a level produces strong directional conviction because the consensus is violated.

**Uncertainty constraint:** When price oscillates near a level, the market has NOT reached consensus. Participants are uncertain. A break at such a level produces weaker conviction because the uncertainty has not been resolved.

### Economic Mechanism

Low-friction (clean) approach → level break produces:
- Larger directional displacement (consensus violation)
- Higher win rate (strong conviction)
- More persistent follow-through (genuine directional conviction)

High-friction (choppy) approach → level break produces:
- Smaller directional displacement (uncertainty already partially priced in)
- Lower win rate (weak conviction)
- Less persistent follow-through (uncertainty may reassert)

This creates a conditional economic consequence: the quality of price discovery at a structural level (measured by approach smoothness) contains information about the economics of subsequent breaks.

### Economic Consequence

- **Directional displacement:** Clean-approach breaks produce larger moves
- **Conviction:** Clean-approach breaks have higher win rates
- **Persistence:** Clean-approach breaks show more follow-through
- **Asymmetric tails:** Clean-approach breaks have fatter positive tails (in break direction)

### Core Hypothesis

> Structural level breaks preceded by low-friction (clean, monotonic) price approach produce larger directional moves and higher win rates than breaks preceded by high-friction (choppy, oscillatory) price approach.

### Observable Variables

1. **Approach smoothness:** Standard deviation of bar-to-bar returns during the approach to the structural level (lower = smoother = lower friction)
2. **Approach monotonicity:** Percentage of bars moving in the direction of the level during approach (higher = more monotonic = lower friction)
3. **Approach duration:** Number of bars from first touch to break (shorter = faster = potentially lower friction)
4. **Oscillation count:** Number of direction changes during approach (fewer = cleaner = lower friction)

### Observable vs Hypothesis

**Observable:**
- Return volatility during approach (from OHLC)
- Directional consistency during approach (from bar directions)
- Approach duration (from timestamps)
- Oscillation count (from bar directions)
- Downstream returns (from forward prices)

**Hypothesis:**
- Market consensus about level significance (inferred from approach smoothness)
- Participant conviction (inferred from approach monotonicity)

**Unknown:**
- Actual limit order placement at levels
- Whether smooth approach reflects genuine consensus or thin liquidity
- Whether choppy approach reflects disagreement or normal microstructure

### Exact Setup

1. Detect structural level breaks on USATECHIDXUSD M1 (20-bar lookback, 3 bps threshold)
2. For each break, examine the approach to the level: the bars from first touch to break
3. Compute approach smoothness (std of returns during approach)
4. Compute approach monotonicity (% bars in break direction during approach)
5. Classify as "low friction" (smooth, monotonic) or "high friction" (choppy, oscillatory) using composite score
6. Compute forward returns for both groups

### Exact Confirmation

The candidate confirms when:
- A structural level break occurs
- AND the approach quality is classified (low vs high friction)
- AND downstream economics are compared between friction conditions

### Exact Entry

At the break, enter WITH the break direction.

### Exact Exit / Evaluation

60-minute holding period.

### Direction

WITH the break.

### Rearm Rule

60-bar minimum between events.

### Dynamic-vs-Static Rationale

This candidate is DYNAMIC because:
- It requires measuring the TRAJECTORY of price approach over time (not just the level itself)
- The key signal is the SMOOTHNESS of the approach process, not a static level attribute
- The mechanism depends on the QUALITY of the price-discovery process
- Removing the trajectory aspect would reduce it to "clean levels break differently" — which is static

The dynamic nature is essential: price-discovery friction requires that the market has BEEN approaching the level (process), not just that the level EXISTS (state).

### Expected Distribution Change

Compared to high-friction breaks:
- Low-friction breaks: higher mean return, higher median return, higher win rate, wider positive tail
- High-friction breaks: lower mean return, lower win rate, more symmetric distribution

### Economic Headroom

Approach quality varies across all structural breaks. If the mechanism is real, it could condition a meaningful fraction of events.

### Conceptual Counterfactual

Structural level breaks preceded by high-friction (choppy, oscillatory) price approach. These breaks occur when the market has NOT reached consensus about the level.

### Counterfactual Discrimination

The counterfactual discriminates because:
- Same event class (structural break)
- Same market, timeframe, holding period
- Same cost model
- Only difference: quality of approach (smooth vs choppy)
- The mechanism specifically requires approach quality — if approach doesn't matter, both groups should perform identically

### Data Availability

USATECHIDXUSD M1: ✓ (primary dataset)
All required variables available from OHLC.

### Causal Observability

Approach smoothness is directly observable from M1 OHLC. The link between smoothness and consensus is inferred.

### Prior-Art

> **NEW**

No existing candidate tests approach smoothness as a conditioning variable for structural breaks.
- CAND-083 tests rejection COUNT (how many times level held), not approach CHARACTER
- CAND-081 tests failure trap (post-break state), not pre-break approach quality
- SMC BOS+OB tests break + order block, not approach trajectory
- APEX session-transition tests distributional differences, not approach smoothness

### Closed-Line Check

- Not Structural (10 closures) — tests approach dynamics, not level quality
- Not CAND-083 (rejection count) — tests approach character, not rejection count
- Not SMC BOS+OB — tests approach trajectory, not break + order block

### Standalone Potential

> **CONDITIONAL** — May serve better as a State/Condition.

### Rare-Event Potential

> **NO** — Approach quality varies across all breaks.

### State Potential

> **YES** — Price-discovery friction could be a State condition modifying break economics.

### Regime Potential

> **NO** — Event-level, not regime-level.

### Modular Potential

> **YES** — Could serve as a quality filter for structural-break trades.

### Expected Failure Mode

1. Approach smoothness may be too noisy to produce clean separation
2. The mechanism may exist but be too small to survive friction
3. Choppy approach may be normal microstructure, not genuine uncertainty
4. The composite score may not discriminate meaningful friction levels

### Proposed G1 Measurement

- Detect structural breaks on USATECHIDXUSD M1
- Compute approach smoothness for each break
- Classify by friction condition
- Compute forward returns for both groups
- Apply 2 bps friction

### G0 Quality Decision

> **PASS**

- Genuinely new mechanism (microstructure information dynamics)
- Not a disguised prior candidate
- Economically plausible (approach quality reflects market consensus)
- Observable (M1 OHLC)
- Has credible counterfactual
- Realistic G1 measurement
- No hindsight, no threshold mining

---

## 9. Candidate 3

### Candidate ID

CAND-094

### Name

Path-Dependent Event Severity

### Expression Class

STATE / CONDITION

### Mechanism Family

Event-Path Dynamics

### Pre-State

Price is interacting with a structural level. The path by which price reaches the level varies: some paths are direct (price moves straight to the level), while others are indirect (price wanders, reverses, and approaches the level from multiple directions).

### Transition / Evolution

The CHARACTER of the path to the level affects the participant population:
- **Direct path:** Participants who positioned along the path have clear directional conviction. Their positions are concentrated and aligned.
- **Indirect path:** Participants who positioned during the wandering have mixed conviction. Their positions are dispersed and misaligned.

### Post-State

A path-dependent condition exists:
- **Direct-path levels:** Clean participant population with aligned positioning → breaks produce strong directional moves (position unwinding is coordinated)
- **Indirect-path levels:** Mixed participant population with dispersed positioning → breaks produce weaker, choppier moves (position unwinding is uncoordinated)

### Participant / Market Constraint

**Positioning alignment constraint:** When price approaches a level directly, the participants who entered during the approach have similar positioning (all directional, all near the level). When price approaches indirectly, the participants have diverse positioning (some long, some short, some at different levels).

**Unwinding coordination constraint:** When a direct-path level breaks, the trapped participants unwind together, creating coordinated forced-exit flow. When an indirect-path level breaks, the unwinding is scattered, creating less directional pressure.

### Economic Mechanism

Direct-path approach → level break produces:
- Larger directional displacement (coordinated unwinding)
- Higher win rate (clean participant population)
- More persistent follow-through (genuine directional conviction)

Indirect-path approach → level break produces:
- Smaller directional displacement (scattered unwinding)
- Lower win rate (mixed participant population)
- Less persistent follow-through (uncertainty reasserts)

This is DISTINCT from CAND-083 (rejection count) because:
- CAND-083 counts HOW MANY TIMES the level held
- CAND-094 measures HOW PRICE REACHED the level (the path character)
- Two levels with the same rejection count can have very different path characters

This is DISTINCT from CAND-093 (approach friction) because:
- CAND-093 measures smoothness of approach (microstructure noise)
- CAND-094 measures the overall path geometry (direct vs indirect trajectory)
- Smoothness is a local property; path geometry is a global property

### Economic Consequence

- **Directional displacement:** Direct-path breaks produce larger moves
- **Conviction:** Direct-path breaks have higher win rates
- **Persistence:** Direct-path breaks show more follow-through
- **Asymmetric tails:** Direct-path breaks have fatter tails in break direction

### Core Hypothesis

> Structural level breaks preceded by direct (straight, monotonic) price paths to the level produce larger directional moves than breaks preceded by indirect (wandering, multi-directional) price paths.

### Observable Variables

1. **Path directness:** Ratio of net directional distance to total path length over the approach window (higher = more direct)
2. **Path efficiency:** Net displacement divided by total absolute bar-to-bar movement (higher = more efficient = less wasted motion)
3. **Direction changes:** Number of sign changes in bar-to-bar returns during approach (fewer = more direct)
4. **Approach window:** The bars from the start of the approach (first significant move toward the level) to the break

### Observable vs Hypothesis

**Observable:**
- Path directness (from OHLC returns)
- Path efficiency (from cumulative vs total movement)
- Direction changes (from bar direction sign changes)
- Downstream returns (from forward prices)

**Hypothesis:**
- Participant positioning alignment (inferred from path directness)
- Unwinding coordination (inferred from path efficiency)

**Unknown:**
- Actual participant positioning
- Whether direct path reflects genuine conviction or low volatility
- Whether indirect path reflects disagreement or normal market noise

### Exact Setup

1. Detect structural level breaks on USATECHIDXUSD M1 (20-bar lookback, 3 bps threshold)
2. For each break, trace the path from the start of the approach to the break
3. Compute path directness (net displacement / total movement)
4. Compute path efficiency and direction changes
5. Classify as "direct path" (high directness) or "indirect path" (low directness)
6. Compute forward returns for both groups

### Exact Confirmation

The candidate confirms when:
- A structural level break occurs
- AND the path to the level is classified (direct vs indirect)
- AND downstream economics are compared between path conditions

### Exact Entry

At the break, enter WITH the break direction.

### Exact Exit / Evaluation

60-minute holding period.

### Direction

WITH the break.

### Rearm Rule

60-bar minimum.

### Dynamic-vs-Static Rationale

This candidate is DYNAMIC because:
- It requires tracing the TRAJECTORY of price over time (not just the level)
- The key signal is the GEOMETRY of the path (directness, efficiency), not a static attribute
- The mechanism depends on the HISTORY of how price reached the level
- Removing the path aspect would reduce it to "levels with different approach patterns" — which is static

### Expected Distribution Change

Compared to indirect-path breaks:
- Direct-path breaks: higher mean return, higher win rate, wider positive tail
- Indirect-path breaks: lower mean return, lower win rate, more symmetric

### Economic Headroom

Path character varies across all structural breaks. Could condition a meaningful fraction of events.

### Conceptual Counterfactual

Structural level breaks preceded by indirect (wandering, multi-directional) price paths. These breaks occur when the participant population is dispersed and misaligned.

### Counterfactual Discrimination

The counterfactual discriminates because:
- Same event class, market, timeframe, cost model
- Only difference: path geometry (direct vs indirect)
- The mechanism specifically requires path character — if path doesn't matter, both groups should perform identically

### Data Availability

USATECHIDXUSD M1: ✓ (primary dataset)
All required variables from OHLC.

### Causal Observability

Path directness is directly observable. Link between path and participant alignment is inferred.

### Prior-Art

> **NEW**

- CAND-083 counts rejections (COUNT), not path character (GEOMETRY)
- CAND-093 measures approach smoothness (LOCAL property), not path directness (GLOBAL property)
- No existing candidate traces price trajectory geometry to structural levels

### Closed-Line Check

Distinct from CAND-083 (rejection count), CAND-093 (approach friction), and all closed structural candidates.

### Standalone Potential

> **CONDITIONAL** — Better as State/Condition.

### Rare-Event Potential

> **NO**

### State Potential

> **YES** — Path-dependent condition could modify break economics.

### Regime Potential

> **NO**

### Modular Potential

> **YES** — Could serve as a quality filter for structural-break trades.

### Expected Failure Mode

1. Path directness may be too noisy
2. Direct path may simply reflect low volatility (not genuine conviction)
3. The mechanism may be too small to survive friction
4. Approach window definition may be ambiguous

### Proposed G1 Measurement

- Detect structural breaks on USATECHIDXUSD M1
- Compute path directness for each break
- Classify by path condition
- Compute forward returns
- Apply 2 bps friction

### G0 Quality Decision

> **PASS**

- Genuinely new mechanism (event-path dynamics)
- Distinct from CAND-083 (count) and CAND-093 (smoothness)
- Economically plausible (path geometry reflects participant alignment)
- Observable (M1 OHLC)
- Has credible counterfactual
- Realistic G1 measurement
- No hindsight, no threshold mining

---

## 10. Candidate Diversity Audit

| Dimension | CAND-092 | CAND-093 | CAND-094 |
|---|---|---|---|
| Mechanism Family | Information Persistence Dynamics | Microstructure Information Dynamics | Event-Path Dynamics |
| Core Observable | Time since prior event | Approach smoothness | Path directness |
| Temporal Level | Inter-event (time between events) | Intra-event (approach to level) | Intra-event (trajectory to level) |
| Primary Constraint | Information decay | Market consensus | Positioning alignment |
| Expression Class | State/Condition | State/Condition | State/Condition |
| Overlap with Prior | None identified | None identified | Distinct from CAND-083/093 |

**Assessment:** Three candidates from genuinely different mechanism families with different observables, different economic mechanisms, and different temporal levels. No two candidates share the same causal chain.

## 11. Economic Mechanism Comparison

| Candidate | Mechanism | Why Economics Should Change |
|---|---|---|
| CAND-092 | Information decay | Market memory of prior events affects response to new catalysts |
| CAND-093 | Price-discovery friction | Approach smoothness reflects consensus, which affects break conviction |
| CAND-094 | Path-dependent severity | Path geometry reflects participant alignment, which affects unwinding coordination |

Each mechanism explains a DIFFERENT economic pathway. No two candidates share the same causal chain.

## 12. Prior-Art / Cross-Research Redundancy Audit

| Candidate | Potential Overlap | Assessment |
|---|---|---|
| CAND-092 | CAND-077 (vol transition) | DISTINCT — CAND-092 is event-level time decay; CAND-077 is regime-level character |
| CAND-092 | APEX HIGH_VOL persistence | DISTINCT — regime-level vs event-level |
| CAND-093 | CAND-083 (rejection count) | DISTINCT — approach character vs rejection count |
| CAND-093 | SMC BOS+OB | DISTINCT — approach quality vs break+order-block |
| CAND-094 | CAND-083 (rejection count) | DISTINCT — path geometry vs rejection count |
| CAND-094 | CAND-093 (approach friction) | DISTINCT — global path vs local smoothness |
| CAND-094 | CAND-089 (velocity decay) | DISTINCT — path geometry vs velocity dynamics |

## 13. State Library Firewall

CAND-077/081/083: **NOT MODIFIED, NOT OPTIMIZED, NOT COMBINED**

## 14. SEED-002 Negative Knowledge

SEED-002 = NO INCREMENTAL INFORMATION. Not retested. Not reversed. Used only as negative knowledge.

## 15. APEX RB001–RB004 Firewall

All four: **DESIGNED / NOT EXECUTED**

Not used as evidence. Not executed.

## 16. CAND-088 Exploratory Firewall

> CLOSED / HYPOTHESIS CONTRADICTED
> aligned-break observation remains exploratory

Not imported as V31 positive input.

## 17. Closed-Line Firewall

No V19–V30 closed hypothesis was reopened. No closed candidate was used as a positive rescue input.

## 18. External Research Prior

Custom-bot observations remain: PROVISIONAL / NOT VALIDATED. Not imported as evidence. May inform conceptual direction only.

## 19. Data Feasibility

All three candidates use USATECHIDXUSD M1 OHLC data. No volume required. No proprietary data required. All variables observable from repository datasets.

## 20. Protected Forward Runtime

CAND-015/024/035: **ACTIVE / PROTECTED / UNTOUCHED**

## 21. G1

> **NOT EXECUTED**

## 22. G2

> **NOT EXECUTED**

## 23. System Assembly

> **NOT EXECUTED**

## 24. Next Milestone

> **G1 — ECONOMIC PLAUSIBILITY SCREEN**
