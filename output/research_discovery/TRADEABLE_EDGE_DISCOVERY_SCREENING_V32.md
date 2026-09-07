# TRADEABLE EDGE DISCOVERY SCREENING — V32

## 1. G0 Status

> **COMPLETE**

V32 G0 — Knowledge-gap / economic-mechanism discovery. Three genuinely new candidates from under-explored economic mechanism space.

## 2. V30–V31 Lessons

| Lesson | Implication for V32 |
|---|---|
| Conditional information is common; monetizable economics are rare | Do not assume positive delta = tradeable Alpha |
| Static thresholds repeatedly fail | No indicator > threshold candidates |
| Dynamic transitions are interesting but frequently uneconomic | Test mechanisms, not just transitions |
| State objects can be informative without being tradeable | Consider modular/expression roles |
| States may not combine positively (SEED-002) | Do not accumulate conditions |
| Candidate redundancy is real (CAND-087≈090, CAND-093≈094) | Aggressively prevent re-labeling |
| Scientific primitives ≠ economic modules | APEX M1/M2 findings need economic translation |
| Negative knowledge is an asset | Use it to identify what NOT to repeat |

## 3. Cross-Research Knowledge Base

64 objects across QuantForge RF, APEX_CORE, SMC_STREAM, custom-bot, watchlist.

**Most explored families (avoid):** Event Sequence (14), Cross-Market (11), Structural (10), Market Microstructure (9), Volatility (7).

**Closed/failed mechanisms (learn from):** Information Processing Dynamics, Directional Exhaustion, Response Quality, Information Failure, Information Persistence, Microstructure Information Dynamics.

**Validated scientific primitives (not monetized):** HIGH_VOL distribution/persistence, session-transition LNO, LNO scale, BTC transferability.

## 4. Knowledge-Gap Analysis

### Gap 1: Shock-Magnitude Asymmetry

**Coverage:** No candidate tests whether the DIRECTION of a large move (up vs down) produces systematically different downstream economics. Existing candidates test event detection, event conditioning, and regime transitions — but not direction-dependent response asymmetry.

**Why genuine:** The research factory has consistently treated up-breaks and down-breaks symmetrically (direction = with-break). But market microstructure theory suggests that buying and selling pressure may be asymmetric due to short-sale constraints, margin dynamics, and institutional flow patterns.

**Closest prior:** CAND-088 tested opening-bias direction vs break direction (sequence). CAND-092 tested time-since-event. Neither tests whether shock direction itself produces different economics.

**Why negative knowledge doesn't close it:** Prior failures tested event detection and conditioning, not direction-asymmetry per se.

### Gap 2: Volatility Acceleration

**Coverage:** CAND-077 tested volatility REGIME transition (compressed → expanded). No candidate tests the RATE OF CHANGE of volatility (acceleration/deceleration) as a conditioning variable.

**Why genuine:** Volatility level and volatility regime have been tested. But the first derivative (is volatility increasing or decreasing) is a different observable that may carry distinct economic information about market stress evolution.

**Closest prior:** CAND-077 (regime transition). Volatility acceleration is the continuous version of what CAND-077 captures discretely.

**Why negative knowledge doesn't close it:** CAND-077 tested regime transitions, not acceleration rates. The mechanisms are related but the observables are different.

### Gap 3: Post-Shock Self-Correction

**Coverage:** CAND-087/090 tested recovery quality and found it weak. But recovery quality measured the TRAJECTORY of recovery (speed/consistency). No candidate tests whether large moves systematically OVERSHOOT and partially REVERT within a fixed window.

**Why genuine:** The self-correction mechanism is different from recovery quality. Recovery quality asks "how fast does price return?" Self-correction asks "does price overshoot and mean-revert?" The economic mechanism is different: overshooting implies temporary mispricing that corrects; recovery quality implies trapped participants exiting.

**Closest prior:** CAND-087/090 (recovery quality — closed for weak/redundant). Mean-reversion research (early QuantForge — closed for insufficient evidence).

**Why negative knowledge doesn't close it:** CAND-087 tested recovery trajectory, not overshoot/reversion. Early mean-reversion research was static, not shock-conditioned.

### Gap 4: Execution Stress and Spread Dynamics

**Coverage:** No candidate tests spread widening or execution quality deterioration as a conditioning variable. APEX documented that spread conditions may define execution-quality states, but no economic expression was tested.

**Why genuine:** Execution costs are real and measurable. If spread widening after large moves creates a distinct execution environment, it could affect the economics of subsequent events.

**Closest prior:** APEX custom-bot observations (provisional). No QuantForge candidate.

**Why negative knowledge doesn't close it:** Execution stress has never been tested as a formal candidate.

### Gap 5: Event-Cluster Response Decay

**Coverage:** CAND-092 tested time-since-event (single prior event). No candidate tests whether the RESPONSE TO A NEW EVENT decays when multiple prior events have occurred in quick succession (event clustering).

**Why genuine:** A single event may produce a clean response. But when multiple events cluster, the market's capacity to respond may degrade. This is different from CAND-092 (which tests time-since-one-event) because it tests the cumulative effect of multiple recent events.

**Closest prior:** CAND-092 (time-since-event — closed for mixed evidence). Event-sequence research (14 closures).

**Why negative knowledge doesn't close it:** CAND-092 tested recency of a single event, not the cumulative effect of event clusters.

## 5. Candidate 1

### Candidate ID

CAND-095

### Name

Shock-Magnitude Asymmetry

### Expression Class

STATE / CONDITION

### Mechanism Family

Directional Response Asymmetry

### Why This Gap Exists

No candidate has tested whether the DIRECTION of a large move (up vs down) produces systematically different downstream economics. The research factory has treated up and down events symmetrically.

### Prior Research Coverage

- CAND-088 tested opening-bias direction vs break direction (sequence asymmetry)
- CAND-092 tested time-since-event (recency)
- Neither tests whether shock direction itself is economically informative

### Pre-State

A large directional move has occurred (e.g., >1.5× ATR in one direction). The market has experienced a significant shock.

### Transition / Evolution

The DIRECTION of the shock creates different participant dynamics:
- Large UP move: short-sellers are trapped, long-holders are emboldened
- Large DOWN move: long-holders are trapped, short-sellers are emboldened
- The asymmetry in participant response creates different downstream economics

### Post-State

A direction-dependent response condition exists. The market's response to subsequent events depends on whether the prior shock was up or down, not just that a shock occurred.

### Participant / Market Constraint

**Short-sale constraint:** Down-shocks may produce larger forced exits (long liquidation) than up-shocks (short covering) because short-selling is inherently more constrained. This creates asymmetric participant response.

**Institutional flow:** Institutional buying and selling patterns are asymmetric. Large down-moves may trigger different institutional behavior than large up-moves.

### Economic Mechanism

Large DOWN moves → trapped longs → forced liquidation → potentially larger continuation or faster reversal
Large UP moves → trapped shorts → short covering → potentially different continuation/reversal dynamics

The asymmetry creates conditional economics: the same subsequent event may produce different outcomes depending on the direction of the prior shock.

### Economic Consequence

- **Directional displacement:** Down-shocks may produce larger subsequent moves in either direction
- **Asymmetric tails:** Different tail behavior for up-shock vs down-shock markets
- **Persistence:** Different persistence patterns for up vs down shocks
- **Reversal probability:** Different reversal probabilities after up vs down shocks

### Core Hypothesis

> Large directional moves in the DOWN direction produce different downstream economics than large directional moves in the UP direction, due to asymmetric participant response dynamics.

### Observable Variables

1. **Shock direction:** Whether the large move was up or down (from OHLC)
2. **Shock magnitude:** Size of the move in bps (from OHLC)
3. **Prior trend:** Direction of the trend before the shock (from OHLC)
4. **Downstream returns:** Forward returns after the shock (from forward prices)

### Observable vs Inferred vs Unknown

**Observable:**
- Shock direction (from OHLC)
- Shock magnitude (from OHLC)
- Forward returns (from forward prices)

**Inferred:**
- Participant positioning (inferred from direction + magnitude)
- Forced exit flow (inferred from shock direction)

**Unknown:**
- Actual participant identity
- Actual stop placement
- Whether institutional flow drives the asymmetry

### Exact Setup

1. Detect large directional moves on USATECHIDXUSD M1 (bar-to-bar move > 1.5× rolling 100-bar ATR)
2. Classify by direction: UP shock vs DOWN shock
3. Compute forward returns for both groups
4. Compare mean, median, win rate, distribution

### Exact Confirmation

The candidate confirms when:
- A large directional move occurs
- AND its direction is classified (up vs down)
- AND downstream economics are compared between up-shock and down-shock conditions

### Exact Entry

At the close of the shock bar, enter in the shock direction.

### Exact Exit / Evaluation

60-minute holding period.

### Direction

WITH the shock direction.

### Rearm Rule

60-bar minimum between events.

### Dynamic-vs-Static Rationale

This candidate is DYNAMIC because:
- It requires identifying a large MOVE (transition from normal to shocked state)
- The key signal is the DIRECTION of the shock, not a static level
- The mechanism depends on the participant RESPONSE to the shock
- Removing the move/direction would reduce it to "large moves have different returns" — which is static

### Expected Distribution Change

Compared to up-shocks:
- Down-shocks: potentially larger mean return, different tail behavior, different persistence
- The direction of the difference is hypothesized but not predetermined

### Economic Headroom

Large moves occur frequently enough to produce meaningful sample sizes. If the asymmetry is real, it could condition a significant fraction of events.

### Conceptual Counterfactual

Large UP moves. The counterfactual is the same shock magnitude in the opposite direction. The mechanism specifically requires direction-dependent response — if direction doesn't matter, both groups should perform identically.

### Counterfactual Discrimination

The counterfactual discriminates because:
- Same shock magnitude class
- Same market, timeframe, holding period
- Same cost model
- Only difference: shock direction
- The mechanism specifically requires directional asymmetry

### Data Availability

USATECHIDXUSD M1: ✓ (primary dataset)
All required variables from OHLC.

### Causal Observability

Shock direction is directly observable. Link between direction and participant response is inferred.

### Prior-Art

> **NEW**

- CAND-088 tested opening-bias direction vs break direction (sequence), not shock direction per se
- No candidate tests whether up-shocks and down-shocks produce different downstream economics
- APEX HIGH_VOL tests volatility level, not shock direction

### Closed-Line Check

Distinct from all closed candidates. No prior candidate tested direction-dependent shock response.

### Standalone Potential

> **CONDITIONAL** — May serve better as State/Condition.

### Rare-Event Potential

> **NO** — Large moves occur regularly.

### State Potential

> **YES** — Shock direction could be a State condition modifying subsequent event economics.

### Regime Potential

> **NO** — Event-level, not regime-level.

### Modular Potential

> **YES** — Could serve as a directional filter: "adjust position sizing based on prior shock direction."

### Expected Failure Mode

1. Direction asymmetry may be too small to detect
2. The mechanism may exist but be dominated by noise
3. The 1.5× ATR threshold may not discriminate meaningful shocks
4. Up/down asymmetry may not survive friction

### Proposed G1 Measurement

- Detect large moves on USATECHIDXUSD M1 (>1.5× ATR)
- Classify by direction
- Compute forward returns for both groups
- Apply 2 bps friction

### G0 Quality Decision

> **PASS**

- Genuinely new mechanism (directional response asymmetry)
- Not a disguised prior candidate
- Economically plausible (short-sale constraints, institutional flow asymmetry)
- Observable (OHLC direction)
- Has credible counterfactual
- Realistic G1 measurement
- No hindsight, no threshold mining

---

## 6. Candidate 2

### Candidate ID

CAND-096

### Name

Volatility Acceleration Gradient

### Expression Class

STATE / CONDITION

### Mechanism Family

Volatility Dynamics

### Why This Gap Exists

CAND-077 tested volatility REGIME transitions (compressed → expanded). No candidate tests the RATE OF CHANGE of volatility (acceleration) as a conditioning variable. Volatility level and regime have been explored; the first derivative has not.

### Prior Research Coverage

- CAND-077: Volatility regime transition (STATE REVIEW ELIGIBLE, +1.67 bps delta)
- APEX HIGH_VOL: Volatility distributional primitive (validated scientific, not economic)
- No candidate tests volatility acceleration (rate of change of volatility)

### Pre-State

The market is in some volatility state. Volatility is either increasing, stable, or decreasing.

### Transition / Evolution

Volatility begins to ACCELERATE (rate of increase is itself increasing). This is different from volatility being HIGH — it is volatility INCREASING AT AN INCREASING RATE. The acceleration indicates that the market is entering a period of escalating uncertainty.

### Post-State

A volatility-acceleration condition exists. The market is not just volatile — it is becoming MORE volatile at an increasing rate. This escalating uncertainty may alter the economics of subsequent events because participants are adjusting to rapidly changing conditions.

### Participant / Market Constraint

**Uncertainty escalation:** When volatility accelerates, participants face rapidly changing risk conditions. Their positioning may become suboptimal as they struggle to adapt.

**Risk-management stress:** Accelerating volatility stresses risk-management systems, potentially triggering forced position reductions that amplify the move.

**Adaptation lag:** Participants need time to adapt to changing volatility. During acceleration, they are perpetually behind.

### Economic Mechanism

Volatility acceleration → escalating uncertainty → participant adaptation lag → potentially larger or more persistent moves during the acceleration period.

Decelerating volatility → declining uncertainty → participant adaptation → potentially smaller or more mean-reverting moves.

### Economic Consequence

- **Magnitude:** Accelerating volatility may produce larger subsequent moves
- **Persistence:** Accelerating volatility may produce more persistent trends
- **Asymmetry:** Different tail behavior during acceleration vs deceleration
- **Reversal:** Decelerating volatility may signal pending reversal

### Core Hypothesis

> Structural events occurring during periods of volatility acceleration (increasing rate of volatility change) produce different downstream economics than events during volatility deceleration.

### Observable Variables

1. **Volatility level:** Rolling ATR or realized volatility (from OHLC)
2. **Volatility change:** First difference of volatility (from rolling computation)
3. **Volatility acceleration:** Second difference of volatility (change of change)
4. **Direction of acceleration:** Positive (accelerating) vs negative (decelerating)

### Observable vs Inferred vs Unknown

**Observable:**
- Volatility level (from OHLC)
- Volatility change (from computation)
- Volatility acceleration (from computation)
- Forward returns (from forward prices)

**Inferred:**
- Participant adaptation lag (inferred from acceleration)
- Risk-management stress (inferred from acceleration rate)

**Unknown:**
- Actual risk-management triggers
- Whether acceleration is from genuine uncertainty or mechanical effects

### Exact Setup

1. Compute rolling 100-bar ATR on USATECHIDXUSD M1
2. Compute first difference (volatility change) and second difference (acceleration)
3. Detect structural level breaks (20-bar lookback, 3 bps threshold)
4. For each break, check whether volatility is accelerating or decelerating
5. Compute forward returns for both groups

### Exact Confirmation

The candidate confirms when:
- A structural break occurs
- AND volatility acceleration is classified (accelerating vs decelerating)
- AND downstream economics are compared

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
- It requires measuring the RATE OF CHANGE of volatility (second derivative)
- The key signal is ACCELERATION (change of change), not level
- The mechanism depends on the EVOLUTION of volatility over time
- Removing the acceleration would reduce it to "high volatility events have different returns" — which is static and already tested

### Expected Distribution Change

Compared to decelerating volatility:
- Accelerating: potentially larger moves, more persistence, different tails

### Economic Headroom

Volatility acceleration varies continuously. Could condition a meaningful fraction of events.

### Conceptual Counterfactual

Structural breaks during volatility deceleration (volatility change is decreasing). Same event class, different volatility dynamics.

### Counterfactual Discrimination

- Same event class, market, timeframe, cost model
- Only difference: volatility acceleration vs deceleration
- Mechanism specifically requires acceleration — level alone is insufficient

### Data Availability

USATECHIDXUSD M1: ✓
All required variables from OHLC.

### Causal Observability

Volatility acceleration is directly observable. Link to participant adaptation is inferred.

### Prior-Art

> **NEW**

- CAND-077 tested regime TRANSITION (discrete), not acceleration (continuous first derivative)
- APEX HIGH_VOL tests volatility LEVEL, not acceleration
- No candidate tests volatility acceleration

### Closed-Line Check

Distinct from CAND-077 (regime transition vs acceleration rate).

### Standalone Potential

> **CONDITIONAL**

### Rare-Event Potential

> **NO**

### State Potential

> **YES**

### Regime Potential

> **CONDITIONAL** — Acceleration itself is regime-like.

### Modular Potential

> **YES** — Could serve as a risk filter: "reduce exposure during volatility acceleration."

### Expected Failure Mode

1. Acceleration may be too noisy at M1
2. The mechanism may be subsumed by CAND-077
3. The second derivative may not carry independent information

### Proposed G1 Measurement

- Compute volatility acceleration for each break
- Classify by acceleration direction
- Compute forward returns
- Apply 2 bps friction

### G0 Quality Decision

> **PASS**

- Genuinely new (acceleration ≠ regime transition)
- Economically plausible (adaptation lag, risk-management stress)
- Observable (from OHLC)
- Has credible counterfactual
- Realistic G1

---

## 7. Candidate 3

### Candidate ID

CAND-097

### Name

Post-Shock Overshoot Reversion

### Expression Class

STANDALONE ALPHA / STATE

### Mechanism Family

Mean-Reversion Dynamics

### Why This Gap Exists

CAND-087/090 tested recovery quality (trajectory) and found it weak. Early mean-reversion research was static. No candidate tests whether large moves systematically OVERSHOOT and partially REVERT within a fixed window — a specific, testable mean-reversion mechanism conditioned on shock magnitude.

### Prior Research Coverage

- CAND-087/090: Recovery quality (CLOSED — weak/redundant)
- Early mean-reversion research: Static, insufficient evidence
- CAND-092: Time-since-event (different mechanism)
- No candidate tests shock-conditioned overshoot/reversion

### Pre-State

A large directional move has occurred (shock). The market has moved significantly in one direction.

### Transition / Evolution

After the shock, price continues briefly in the shock direction (momentum/overshoot), then PARTIALLY REVERTS toward the pre-shock level. The reversion is not complete — it is partial — suggesting the market overshoots but retains some directional information.

### Post-State

A self-correction condition exists: the market has partially reverted from the shock, but not fully. The remaining gap between current price and the pre-shock level represents unresolved directional information.

### Participant / Market Constraint

**Overshooting constraint:** Markets tend to overshoot due to momentum, herding, and liquidity effects. The overshoot creates a temporary mispricing.

**Partial reversion constraint:** The market corrects the overshoot but not completely, because some of the directional information was genuine. The partial reversion creates a measurable economic pattern.

### Economic Mechanism

Large shock → overshoot → partial reversion → the reversion amount contains information about:
- Whether the shock was genuine information or noise
- The degree of overshooting
- The expected residual directional movement

### Economic Consequence

- **Directional displacement:** Markets that overshoot more may produce larger reversion moves
- **Magnitude:** The reversion magnitude may be proportional to the overshoot
- **Persistence:** Partial reversion may persist over the evaluation window
- **Asymmetric tails:** Overshoot → reversion creates predictable tail behavior

### Core Hypothesis

> Large directional moves that overshoot (extend beyond the fundamental level) produce partial reversion within a fixed evaluation window, with the reversion magnitude proportional to the overshoot amount.

### Observable Variables

1. **Shock magnitude:** Size of the initial move in bps (from OHLC)
2. **Overshoot amount:** How far price extends beyond the initial shock (from forward OHLC)
3. **Reversion amount:** How much price returns toward pre-shock level (from forward OHLC)
4. **Reversion ratio:** Reversion / overshoot (efficiency of correction)

### Observable vs Inferred vs Unknown

**Observable:**
- Shock magnitude (from OHLC)
- Overshoot (from forward OHLC)
- Reversion (from forward OHLC)
- Reversion ratio (computed)

**Inferred:**
- Whether overshoot is from genuine mispricing or information
- Participant positioning during overshoot

**Unknown:**
- Actual participant intentions
- Whether reversion is from mean-reversion or new information

### Exact Setup

1. Detect large directional moves on USATECHIDXUSD M1 (>1.5× ATR)
2. Measure the overshoot: how far price extends beyond the initial shock within a measurement window (e.g., 10 bars)
3. Measure the reversion: how much price returns toward the pre-shock level within the evaluation window (60 bars)
4. Compute reversion ratio = reversion / overshoot
5. Classify by reversion ratio (high reversion vs low reversion)
6. Compute forward returns for both groups

### Exact Confirmation

The candidate confirms when:
- A large move occurs
- AND the overshoot/reversion is measured
- AND downstream economics are compared between high-reversion and low-reversion conditions

### Exact Entry

At the point of maximum overshoot (or at a fixed point after the shock), enter COUNTER to the shock direction (fade the overshoot).

### Exact Exit / Evaluation

60-minute holding period from entry.

### Direction

COUNTER to the shock direction (mean-reversion trade).

### Rearm Rule

60-bar minimum.

### Dynamic-vs-Static Rationale

This candidate is DYNAMIC because:
- It requires identifying a SHOCK (transition from normal to shocked state)
- It requires measuring OVERSHOOT (price extending beyond the shock)
- It requires measuring REVERSION (price returning toward pre-shock level)
- The mechanism depends on the SEQUENCE: shock → overshoot → reversion
- Removing the sequence would reduce it to "large moves revert" — which is static

### Expected Distribution Change

Compared to low-reversion conditions:
- High-reversion: potentially larger mean return in reversion direction, higher win rate
- The reversion trade should capture the overshoot correction

### Economic Headroom

Large moves occur regularly. If overshoot/reversion is a real pattern, it could produce meaningful standalone economics.

### Conceptual Counterfactual

Large moves that do NOT overshoot (price stays near the shock level without extending). These moves may represent genuine information rather than noise-driven overshoot.

### Counterfactual Discrimination

- Same shock magnitude class
- Same market, timeframe
- Same cost model
- Only difference: whether the move overshoots and reverts
- Mechanism specifically requires overshoot → reversion sequence

### Data Availability

USATECHIDXUSD M1: ✓
All required variables from OHLC.

### Causal Observability

Overshoot and reversion are directly observable. Link to mean-reversion mechanism is inferred.

### Prior-Art

> **NEW**

- CAND-087/090 tested recovery QUALITY (trajectory), not overshoot/REVERSION (magnitude)
- Early mean-reversion was static, not shock-conditioned
- No candidate tests shock-conditioned overshoot → reversion

### Closed-Line Check

Distinct from CAND-087/090 (quality vs magnitude), CAND-092 (time-decay vs reversion), early mean-reversion (static vs shock-conditioned).

### Standalone Potential

> **YES** — Could independently define a tradeable mean-reversion event.

### Rare-Event Potential

> **NO**

### State Potential

> **YES** — Overshoot/reversion state could modify economics of subsequent events.

### Regime Potential

> **NO**

### Modular Potential

> **YES** — Could serve as an exit/timing module: "expect reversion after overshoot."

### Expected Failure Mode

1. Overshoot may be too noisy to measure cleanly
2. The reversion may be too small to survive friction
3. Mean-reversion at M1 may be dominated by transaction costs
4. The mechanism may be subsumed by existing volatility research

### Proposed G1 Measurement

- Detect large moves on USATECHIDXUSD M1 (>1.5× ATR)
- Measure overshoot and reversion
- Classify by reversion ratio
- Compute forward returns for fade trades
- Apply 2 bps friction

### G0 Quality Decision

> **PASS**

- Genuinely new mechanism (shock-conditioned overshoot/reversion)
- Not a disguised prior candidate (distinct from CAND-087/090 quality, distinct from early mean-reversion)
- Economically plausible (overshooting is a well-documented market phenomenon)
- Observable (OHLC overshoot/reversion)
- Has credible counterfactual
- Realistic G1 measurement
- No hindsight, no threshold mining

---

## 8. Candidate Diversity Audit

| Dimension | CAND-095 | CAND-096 | CAND-097 |
|---|---|---|---|
| Mechanism Family | Directional Response Asymmetry | Volatility Dynamics | Mean-Reversion Dynamics |
| Core Observable | Shock direction | Volatility acceleration | Overshoot/reversion ratio |
| Temporal Level | Event-level (post-shock) | State-level (volatility evolution) | Event-level (post-shock) |
| Primary Constraint | Short-sale/institutional flow | Adaptation lag | Overshooting |
| Expression Class | State/Condition | State/Condition | Standalone Alpha / State |
| Direction | WITH shock | WITH break | COUNTER to shock |

**Assessment:** Three candidates from genuinely different mechanism families with different observables, different economic mechanisms, and different directions.

## 9. Economic Mechanism Comparison

| Candidate | Mechanism | Why Economics Should Change |
|---|---|---|
| CAND-095 | Directional asymmetry | Up/down shocks create different participant dynamics |
| CAND-096 | Volatility acceleration | Escalating uncertainty creates adaptation lag |
| CAND-097 | Overshoot reversion | Market overshoots large moves and partially reverts |

Each explains a DIFFERENT economic pathway.

## 10. Knowledge Gap Coverage

| Gap | Candidate | Coverage |
|---|---|---|
| Shock-magnitude asymmetry | CAND-095 | ✓ |
| Volatility acceleration | CAND-096 | ✓ |
| Post-shock self-correction | CAND-097 | ✓ |
| Execution stress | — | Not covered (deferred) |
| Event-cluster response decay | — | Not covered (deferred) |

Three of five identified gaps are addressed.

## 11. Cross-Research Redundancy Audit

| Candidate | Potential Overlap | Assessment |
|---|---|---|
| CAND-095 | CAND-088 (session sequence) | DISTINCT — shock direction vs opening-bias sequence |
| CAND-095 | CAND-092 (time-since-event) | DISTINCT — direction vs recency |
| CAND-096 | CAND-077 (regime transition) | DISTINCT — acceleration rate vs discrete transition |
| CAND-096 | APEX HIGH_VOL (level) | DISTINCT — acceleration vs level |
| CAND-097 | CAND-087/090 (recovery quality) | DISTINCT — overshoot/reversion magnitude vs recovery trajectory |
| CAND-097 | Early mean-reversion | DISTINCT — shock-conditioned vs static |

## 12. V30/V31 Negative Knowledge Used

- V30: Velocity decay failed → avoid velocity-based mechanisms
- V30: Exhaustion contradicted → avoid cumulative-distance exhaustion
- V30: Recovery quality redundant → avoid recovery-trajectory concepts
- V31: Event-information decay mixed → avoid time-since-event as primary variable
- V31: Price-discovery friction mixed → avoid approach-smoothness as primary variable
- SEED-002: State combination failed → do not accumulate conditions

## 13. State Library Firewall

CAND-077/081/083: **NOT MODIFIED, NOT OPTIMIZED, NOT COMBINED**

## 14. SEED-002 Negative Relational Knowledge

SEED-002 = NO INCREMENTAL INFORMATION. Not retested. Used only as negative knowledge.

## 15. APEX RB001–RB004 Firewall

All four: DESIGNED / NOT EXECUTED. Not used as evidence.

## 16. CAND-088 Firewall

> CLOSED / HYPOTHESIS CONTRADICTED
> aligned-break observation remains exploratory

Not imported as V32 positive input.

## 17. Closed-Line Firewall

No V19–V31 closed hypothesis reopened. No closed candidate used as positive input.

## 18. External Research Prior

Custom-bot observations remain: PROVISIONAL / NOT VALIDATED. Not imported as evidence.

## 19. Data Feasibility

All three candidates use USATECHIDXUSD M1 OHLC data. No volume required. No proprietary data required.

## 20. Protected Forward Runtime

CAND-015/024/035: **ACTIVE / PROTECTED / UNTOUCHED**

## 21. G1

> **NOT EXECUTED**

## 22. G2

> **NOT EXECUTED**

## 23. Relational Testing

> **NOT EXECUTED**

## 24. Modular Bot Experiments

> **NOT EXECUTED**

## 25. System Assembly

> **NOT EXECUTED**

## 26. Next Milestone

> **V32 G0 INTEGRITY / PRIOR-ART AUDIT**
