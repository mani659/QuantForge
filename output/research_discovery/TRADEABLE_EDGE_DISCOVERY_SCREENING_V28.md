# TRADEABLE EDGE DISCOVERY SCREENING — V28
# DATE: 2026-08-30
# STATUS: V28 G0 COMPLETE — 3 CANDIDATES GENERATED
# NO G1 / NO G2 / NO EXPERIMENT EXECUTION

---

## 1. G0 Status

> V28 G0 COMPLETE — 3 CANDIDATES GENERATED

Three candidates spanning three distinct economic mechanism families. All genuinely new — no overlap with V19–V27 or historical candidates.

---

## 2. Post-V27 Starting State

V27 produced 0 G2 promotions. Two State Review Eligible objects exist (CAND-077, CAND-081). The State library is governed. V28 begins from a clean conceptual space.

---

## 3. V19–V27 Lessons

- Static conditions produce less conditional information than dynamic transitions
- Settlement/benchmark mechanisms failed (V25)
- Dynamic state transitions show more promise (V26: +1.67 bps, V27: +1.23 bps)
- Counterfactual validity is critical (CAND-080 failed due to invalid CF)
- State hypothesis must not be contradicted by median evidence (CAND-082)
- Absolute economics remain the primary standalone gate
- Frequency is not value; mechanism quality is

---

## 4. Current State Library

| Candidate | Classification |
|---|---|
| CAND-059 | STATE-ARTIFACT |
| CAND-065 | STATE OBSERVATION |
| CAND-069 | STATE OBSERVATION |
| CAND-077 | STATE REVIEW ELIGIBLE |
| CAND-079 | STATE OBSERVATION |
| CAND-081 | STATE REVIEW ELIGIBLE |

---

## 5. G1 V3 Framework

Ratified. Two-layer architecture: 9 hard validity gates + economic evidence adjudication. No universal hard economic thresholds.

---

## 6. External Statistical Research Priors

> PROVISIONAL EXTERNAL RESEARCH INPUT — NOT VALIDATED QUANTFORGE EVIDENCE

Used as conceptual starting points only. No thresholds imported.

---

## 7. Candidate 1 — CAND-083

### Candidate ID
CAND-083

### Name
Cumulative Rejection Pressure Sweep

### Artifact Type
Alpha / Event (provisional)

### Mechanism Family
Failed Information / Expectation Reset — Rejection Cascade

### Pre-State
Price repeatedly tests a structural level (20-bar rolling high/low) and fails to break through. Each rejection represents a failed breakout attempt where participants accumulated positions expecting continuation.

### Transition
The level is finally broken with conviction (close beyond level by 5+ bps), but the cumulative rejected-participant population creates a specific post-break dynamics: the breakout attracts trend-following participants while the rejected participants' accumulated exposure creates a directional force.

### Post-State
After the breakout, price reverses back through the level within 10 bars. The reversal is accelerated by:
1. Trend followers who entered on the breakout are now trapped
2. The cumulative rejected participants' directional pressure manifests
3. The combination creates a larger reversal than a single rejection would produce

### Affected Participants
- Trend followers who entered on the breakout (trapped)
- Participants who were rejected at the level and may have accumulated counter-position
- Stop-loss placement beyond the breakout level creates a cascade zone

### Participant Constraint
Each failed attempt to break the level creates participants who expected the break to succeed. When the level finally breaks and fails, ALL of these accumulated participants are simultaneously trapped. The cumulative trapped population is larger than what a single rejection would create.

### Economic Mechanism
The cumulative rejection count is a proxy for the size of the trapped participant population. More rejections → more trapped participants → larger forced exit flow → larger reversal after the breakout failure.

The key hypothesis: the NUMBER OF REJECTIONS before the breakout correlates with the magnitude of the subsequent reversal.

### Economic Consequence
If cumulative rejections create proportional trapped-participant pressure, then:
- Breakouts after many rejections should produce larger reversals
- The reversal magnitude should be proportional to the rejection count
- The economic displacement should exceed friction

### Hypothesis
When price breaks a structural level after 3+ failed attempts, the subsequent reversal is larger than when price breaks after 0-1 failed attempts. The cumulative rejection count contains information about the trapped-participant population size.

### Observable Variables
- USATECHIDXUSD M1 price
- 20-bar rolling high/low (structural level)
- Rejection count (number of times price touched level but closed back below/above within 5 bars)
- Breakout detection (close beyond level by 5+ bps)
- Reversal detection (close back through level within 10 bars)
- Subsequent N-bar return

### Exact Setup
1. Identify the 20-bar rolling high as the structural level
2. Count rejections: within the last 50 bars, count how many times price touched the level (within 1 bp) but closed back below it within 5 bars
3. Detect breakout: bar closes above the 20-bar high by 5+ bps
4. Wait for reversal: within 10 bars, price closes back below the 20-bar high
5. After reversal confirmation, enter SHORT at the close of the reversal bar
6. Exit after 60 minutes
7. Only enter if rejection count >= 3

### Exact Confirmation
- Breakout bar must close 5+ bps above the 20-bar high
- Reversal must occur within 10 bars
- Rejection count must be >= 3 (cumulative rejections before breakout)

### Exact Entry
At the close of the first bar that closes below the 20-bar high after a confirmed breakout (within 10-bar window), enter SHORT. Only if rejection count >= 3.

### Exact Exit
60 minutes (M1 bars) after entry.

### Direction
SHORT (against the failed upside breakout). Mirror for downside: enter LONG after failed downside breakout with 3+ rejections.

### Rearm Rule
After exit, do not re-enter for 60 minutes. Each structural level is independent.

### Dynamic-vs-Static Rationale
If the hypothesis could be expressed as "when price is below the 20-bar high, go short" it would fail. The cumulative rejection count is essential because:
- It measures the SIZE of the trapped participant population
- More rejections create more trapped participants
- The forced exit flow is proportional to the cumulative trapped population
- A single rejection does not create the same pressure

### Expected Distribution Change
Higher rejection count should produce:
- Larger reversal magnitude (more trapped participants)
- Higher win rate for counter-breakout entries
- More asymmetric payoff (bounded upside, larger downside)
- Distribution shift toward larger negative returns for the breakout direction

### Economic Headroom
If 3+ rejections create 2-3 bps of additional directional pressure beyond a single rejection, this could survive friction. The mechanism is well-understood in market microstructure (stop cascade after cumulative rejections).

### Counterfactual
Same breakout-reversal entry applied to:
1. Breakouts with 0-1 rejections (fresh break, no cumulative trap)
2. Breakouts with 2 rejections (moderate cumulative trap)

The counterfactual isolates the VALUE OF CUMULATIVE REJECTIONS versus:
- Fresh breaks (no cumulative trap)
- Moderate rejections (smaller cumulative trap)

### Counterfactual Discrimination
The counterfactual is discriminating because it specifically removes the cumulative rejection count while preserving the breakout-reversal event. If the fade works equally well regardless of rejection count, the cumulative mechanism adds no value.

### Data Availability
USATECHIDXUSD M1 data. Price computable. Structural level computable. Rejection count computable. No volume required.

### Causal Observability
- OBSERVED: Rejection count, breakout, reversal, subsequent price behavior
- HYPOTHESIZED: Cumulative trapped participants creating proportional exit flow
- UNPROVEN: Actual participant positioning or stop placement

### Prior-Art
NEW. No previous QuantForge candidate tested cumulative rejection count as a directional signal.

Historical check:
- CAND-081: structural level break-and-fail (single break-and-fail, no cumulative rejection count)
- CAND-059: first touch > subsequent touch (different — no cumulative count)
- CAND-065: deep sweep > shallow sweep (different — no rejection counting)

### Closed-Line Check
No overlap with V19–V27. No overlap with DISC-021–028. No overlap with CAND-059–CAND-082.

### Standalone Potential
Moderate. The cumulative rejection mechanism is well-understood. If the trapped-participant population is proportional to rejection count, the economic displacement should be measurable.

### Rare-Event Potential
Low-moderate. Breakouts after 3+ rejections occur at moderate frequency (~100-300/year estimated).

### Component Potential
HIGH. If validated, the rejection count could serve as a State/Condition that sizes or filters breakout-reversal entries.

### State Potential
HIGH. The cumulative rejection count describes a market condition (size of trapped population) that could modify other strategies' behavior.

### Regime Potential
LOW. This is event-driven, not regime-dependent.

### Expected Failure Mode
The most likely failure is that the rejection count does not correlate with the trapped-participant population size. If participants place stops loosely, the cumulative pressure may not create measurable displacement.

### Proposed G1 Measurement
- N (number of breakouts after 3+ rejections)
- Frequency per year
- Mean/median return of counter-breakout fade entry
- Win rate
- Counterfactual comparison (0-1 rejections, 2 rejections)
- Conditional delta (3+ vs 0-1 rejections)
- Distribution shape

---

## 8. Candidate 2 — CAND-084

### Candidate ID
CAND-084

### Name
Intraday Range Compression → Expansion Asymmetry

### Artifact Type
Alpha / Event (provisional)

### Mechanism Family
Market Microstructure / Execution Condition — Range Dynamics

### Pre-State
Intraday range (highest high minus lowest low since session open) is compressed relative to recent history. The market has been quiet, with limited price movement during the current session.

### Transition
The compressed intraday range is broken by a directional move that expands the range beyond a defined threshold relative to the recent average range. The expansion is the event.

### Post-State
After the range expansion, the market enters a period of directional continuation. The hypothesis is that the direction of the expansion is preserved because:
- Participants who were positioned during the quiet period are now forced to adjust
- The expansion creates a reference point (the pre-expansion range)
- Price tends to continue in the expansion direction because the compressed period created a population of participants on the wrong side

### Affected Participants
- Participants who were positioned during the compressed range (now potentially trapped)
- Participants who enter after the expansion (trend followers)
- The expansion direction reflects which side was trapped

### Participant Constraint
During range compression, participants accumulate positions on both sides. The expansion breaks one side's positions. The trapped participants on the wrong side are forced to exit, creating directional pressure in the expansion direction.

### Economic Mechanism
Range compression → expansion creates a directional impulse. The compression period accumulates a population of participants who will be forced to exit when the expansion occurs. The expansion direction reflects which side was trapped, and the forced exit flow creates continuation pressure.

### Economic Consequence
If range compression creates a trapped population that generates continuation pressure, then:
- Breakout entries in the expansion direction should outperform fade entries
- The continuation should be stronger after more extreme compression
- The effect should be directionally consistent (expansion direction = continuation direction)

### Hypothesis
When intraday range compresses to below 50% of its 20-bar rolling average, and then expands by breaking above the average, subsequent continuation in the expansion direction produces positive expectancy. The compression creates a trapped population whose forced exits generate continuation pressure.

### Observable Variables
- USATECHIDXUSD M1 price
- Intraday range (session high - session low, rolling 20-bar)
- Range compression ratio (current range / 20-bar average range)
- Expansion detection (range crosses above average)
- Subsequent N-bar return in expansion direction

### Exact Setup
1. Compute intraday range: rolling 20-bar high minus rolling 20-bar low
2. Compute range average: 100-bar rolling average of intraday range
3. Detect compression: current range < 50% of average
4. Detect expansion: range crosses above 100% of average
5. Record expansion direction (up or down)
6. Enter in expansion direction at the close of the expansion bar
7. Exit after 60 minutes

### Exact Confirmation
- Range must be below 50% of average before expansion
- Range must cross above 100% of average during expansion
- Expansion direction must be clear (close above/below prior range midpoint)

### Exact Entry
At the close of the first bar where the range crosses above 100% of its 100-bar average after being below 50%, enter in the expansion direction.

### Exact Exit
60 minutes (M1 bars) after entry.

### Direction
IN THE EXPANSION DIRECTION (continuation trade).

### Rearm Rule
After exit, do not re-enter for 60 minutes. Each compression-expansion cycle is independent.

### Dynamic-vs-Static Rationale
If the hypothesis could be expressed as "when range > average, enter in the direction of the move" it would fail. The compression requirement is essential because:
- It identifies the specific population of trapped participants
- Compression creates the conditions for forced exit flow
- Without compression, the expansion lacks the trapped-population mechanism
- The transition from compressed to expanded is the signal

### Expected Distribution Change
After compression → expansion:
- Continuation in the expansion direction should be more likely
- The expansion direction should be preserved by trapped-participant exits
- The win rate should be higher than for random entries after expansion
- The mean return should be positive in the expansion direction

### Economic Headroom
If compression creates 2-3 bps of continuation pressure, this could survive friction. The mechanism is intuitive: quiet markets accumulate positions, expansion triggers exits, exits create continuation.

### Counterfactual
The same continuation entry applied to:
1. Expansions without prior compression (no trapped population)
2. Already-expanded markets (no transition)

The counterfactual isolates the VALUE OF COMPRESSION versus:
- No compression (no trapped population)
- Already expanded (no transition event)

### Counterfactual Discrimination
The counterfactual is discriminating because it specifically removes the compression requirement while preserving the expansion event. If continuation works equally well regardless of prior compression, the compression adds no value.

### Data Availability
USATECHIDXUSD M1 data. Price computable. Range computable. No volume required.

### Causal Observability
- OBSERVED: Range compression, expansion, continuation
- HYPOTHESIZED: Trapped participants during compression creating continuation pressure
- UNPROVEN: Actual participant positioning

### Prior-Art
NEW. No previous QuantForge candidate tested intraday range compression → expansion as a directional signal.

Historical check:
- CAND-077: ATR percentile compression → expansion (different — ATR-based, not range-based)
- CAND-040: volatility expansion (tested expansion itself, not range compression)
- CAND-077 uses ATR percentile and directional inconsistency; CAND-084 uses intraday range and range ratio

### Closed-Line Check
No overlap with V19–V27. No overlap with DISC-021–028. No overlap with CAND-059–CAND-082.

### Standalone Potential
Moderate. The compression-expansion-continuation mechanism is intuitive. If trapped participants create measurable continuation pressure, this could be a standalone Alpha.

### Rare-Event Potential
LOW. Range compressions and expansions occur frequently. This is not a rare-event candidate.

### Component Potential
HIGH. If validated, range compression state could filter or size entries for other strategies.

### State Potential
HIGH. Range compression describes a market condition (quiet, accumulated positions) that could modify other strategies' behavior.

### Regime Potential
MODERATE. Could become a regime specialist active during compression-to-expansion transitions.

### Expected Failure Mode
The most likely failure is that range compression does not create enough trapped-participant pressure to survive friction. The compression may be too gradual to create a sharp trapped population. Additionally, the 50%/100% thresholds may not be the right boundaries.

### Proposed G1 Measurement
- N (number of compression → expansion events)
- Frequency per year
- Mean/median return of continuation entry
- Win rate
- Counterfactual comparison (no compression, already expanded)
- Conditional delta (compression vs no-compression)
- Distribution shape

---

## 9. Candidate 3 — CAND-085

### Candidate ID
CAND-085

### Name
Approach Velocity → Breakout Continuation

### Artifact Type
Alpha / Event (provisional)

### Mechanism Family
Event Sequence / Path Dependence — Approach Dynamics

### Pre-State
Price is approaching a structural level (20-bar rolling high/low). The approach is characterized by its velocity: how quickly price moves toward the level.

### Transition
The approach velocity is measured as the rate of price change over the N bars leading up to the level test. High velocity means price moved rapidly toward the level. Low velocity means price drifted gradually.

### Post-State
Price breaks through the structural level. The hypothesis is that:
- HIGH-VELOCITY approaches create trapped participants on the wrong side (those who were positioned against the move)
- LOW-VELOCITY approaches allow orderly positioning (participants can adjust before the break)
- Therefore, breakouts after high-velocity approaches produce larger continuation moves

### Affected Participants
- Participants who were positioned against the approaching move (trapped by high velocity)
- Participants who enter on the breakout (trend followers)
- The velocity determines HOW MANY participants are trapped

### Participant Constraint
High-velocity approach means price moved quickly against some participants' positions. These participants could not exit before the level was reached. When the breakout occurs, these trapped participants are forced to exit, creating continuation pressure proportional to the approach velocity.

### Economic Mechanism
The approach velocity is a proxy for the size and urgency of the trapped participant population. Faster approaches trap more participants (they can't exit in time), creating larger forced exit flow after the breakout.

### Economic Consequence
If approach velocity correlates with trapped-participant population size, then:
- Breakouts after high-velocity approaches should produce larger continuation
- The continuation magnitude should be proportional to the approach velocity
- The effect should survive friction if the velocity-trapped relationship is strong

### Hypothesis
When price breaks a structural level (20-bar high/low) after a high-velocity approach (price moved toward the level at >2x average bar-to-bar rate over the last 20 bars), the subsequent continuation is larger than after a low-velocity approach. The approach velocity contains information about the trapped-participant population.

### Observable Variables
- USATECHIDXUSD M1 price
- 20-bar rolling high/low (structural level)
- Approach velocity (absolute price change over last 20 bars / 20-bar average absolute change)
- Breakout detection (close beyond level by 3+ bps)
- Subsequent N-bar return in breakout direction

### Exact Setup
1. Identify the 20-bar rolling high as the structural level
2. Compute approach velocity: |close[i] - close[i-20]| / mean(|close[j] - close[j-1]| for j in [i-20, i])
3. Detect breakout: bar closes above the 20-bar high by 3+ bps
4. Classify approach: velocity > 2.0 = HIGH, velocity < 0.5 = LOW
5. Enter in breakout direction at the close of the breakout bar
6. Exit after 60 minutes
7. Only enter if approach velocity > 2.0 (HIGH velocity)

### Exact Confirmation
- Breakout bar must close 3+ bps above the 20-bar high
- Approach velocity must exceed 2.0 (high velocity)
- No additional filters

### Exact Entry
At the close of the breakout bar, enter in the breakout direction (LONG for upside breakout). Only if approach velocity > 2.0.

### Exact Exit
60 minutes (M1 bars) after entry.

### Direction
IN THE BREAKOUT DIRECTION (continuation trade).

### Rearm Rule
After exit, do not re-enter for 60 minutes. Each structural level is independent.

### Dynamic-vs-Static Rationale
If the hypothesis could be expressed as "when price breaks the 20-bar high, go long" it would fail. The approach velocity is essential because:
- It measures HOW price reached the level (not just that it reached it)
- High velocity means participants were caught off-guard
- The trapped population is proportional to the velocity
- Low-velocity approaches allow orderly positioning, reducing trapped pressure

### Expected Distribution Change
High-velocity approaches should produce:
- Larger continuation moves (more trapped participants)
- Higher win rate for breakout entries
- More asymmetric payoff (bounded downside, larger upside)
- Distribution shift toward larger positive returns in breakout direction

### Economic Headroom
If high-velocity approaches create 2-3 bps of additional continuation pressure, this could survive friction. The mechanism is intuitive: fast moves trap more participants, trapped participants create forced exit flow, forced exits create continuation.

### Counterfactual
The same breakout continuation entry applied to:
1. Low-velocity approaches (velocity < 0.5)
2. Medium-velocity approaches (velocity 0.5-2.0)

The counterfactual isolates the VALUE OF HIGH APPROACH VELOCITY versus:
- Low velocity (no trapped population)
- Medium velocity (moderate trapped population)

### Counterfactual Discrimination
The counterfactual is discriminating because it specifically removes the velocity requirement while preserving the breakout event. If continuation works equally well regardless of approach velocity, the velocity adds no value.

### Data Availability
USATECHIDXUSD M1 data. Price computable. Velocity computable. No volume required.

### Causal Observability
- OBSERVED: Approach velocity, breakout, continuation
- HYPOTHESIZED: High velocity trapping participants, creating continuation pressure
- UNPROVEN: Actual participant positioning

### Prior-Art
NEW. No previous QuantForge candidate tested approach velocity as a directional signal.

Historical check:
- CAND-081: structural level break-and-fail (no velocity component)
- CAND-083: cumulative rejections (different mechanism — count-based, not velocity-based)
- No prior candidate measured the RATE of approach to a structural level

### Closed-Line Check
No overlap with V19–V27. No overlap with DISC-021–028. No overlap with CAND-059–CAND-082.

### Standalone Potential
Moderate. The approach velocity mechanism is well-understood in market microstructure. If fast moves trap more participants, the continuation should be measurable.

### Rare-Event Potential
LOW. Breakouts after high-velocity approaches occur frequently. This is not a rare-event candidate.

### Component Potential
HIGH. If validated, approach velocity could serve as a State/Condition that sizes or filters breakout entries.

### State Potential
HIGH. Approach velocity describes a market condition (how participants were caught) that could modify other strategies' behavior.

### Regime Potential
LOW. This is event-driven, not regime-dependent.

### Expected Failure Mode
The most likely failure is that approach velocity does not correlate with trapped-participant population size. If participants place stops widely, the velocity may not create measurable trapped pressure. Additionally, the 2.0 velocity threshold may not be the right boundary.

### Proposed G1 Measurement
- N (number of breakouts after high-velocity approaches)
- Frequency per year
- Mean/median return of breakout continuation entry
- Win rate
- Counterfactual comparison (low velocity, medium velocity)
- Conditional delta (high vs low velocity)
- Distribution shape

---

## 10. Mechanism Comparison

| | CAND-083 | CAND-084 | CAND-085 |
|---|---|---|---|
| Mechanism | Cumulative rejection pressure | Range compression → expansion | Approach velocity → continuation |
| What matters | How many times level rejected | How quiet before expansion | How fast price reached level |
| Trapped population source | Rejected breakout participants | Compressed-range participants | Wrong-side participants during approach |
| Direction | Counter-breakout (fade) | Continuation (expansion direction) | Continuation (breakout direction) |
| Timeframe | Event-level (minutes) | Session-level (hours) | Event-level (minutes) |

All three are genuinely distinct from each other and from V26/V27 candidates.

---

## 11. Dynamic Transition Comparison

| | CAND-083 | CAND-084 | CAND-085 |
|---|---|---|---|
| Transition type | Rejection accumulation → breakout failure | Compression → expansion | Approach → breakout |
| Essential element | Cumulative count | Range ratio | Velocity ratio |
| Static reduction fails? | Yes (count is essential) | Yes (compression is essential) | Yes (velocity is essential) |

---

## 12. Economic Consequence Comparison

| | CAND-083 | CAND-084 | CAND-085 |
|---|---|---|---|
| Expected direction | Counter-breakout | Continuation | Continuation |
| Trapped population | Rejected participants | Compressed-range participants | Wrong-side participants |
| Displacement source | Forced exit flow | Forced exit flow | Forced exit flow |
| Expected magnitude | Moderate | Moderate | Moderate |

---

## 13. Counterfactual Quality

All three use discriminating counterfactuals:
- CAND-083: Compares 3+ rejections to 0-1 rejections
- CAND-084: Compares compression-expansion to no-compression expansion
- CAND-085: Compares high-velocity to low-velocity approaches

Each isolates the specific mechanism while preserving the broader event.

---

## 14. Data Feasibility

All candidates use USATECHIDXUSD M1 data:
- Price: computable
- Structural levels: computable
- Rejection count: computable
- Range: computable
- Velocity: computable

No volume required. No cross-market data required.

---

## 15. Prior-Art / Redundancy

| Candidate | Classification | Reason |
|---|---|---|
| CAND-083 | NEW | No prior candidate tested cumulative rejection count |
| CAND-084 | NEW | No prior candidate tested intraday range compression → expansion |
| CAND-085 | NEW | No prior candidate tested approach velocity |

No V28 candidate is an extension of any V19–V27 candidate.

---

## 16. External Research Priors Used

- None directly used. All V28 definitions are independent.

---

## 17. State Library Interaction

V28 candidates do NOT reproduce:
- CAND-077 (vol character transition — different mechanism)
- CAND-081 (structural level failure trap — CAND-083 uses cumulative rejections, not single failure)
- CAND-079 (Gold direction → Tech — no cross-market)
- Any other protected State object

Each V28 candidate introduces a genuinely distinct observable and mechanism.

---

## 18. Closed-Line Firewall

> PASS

No V28 candidate reopens any closed research line.

---

## 19. Protected Forward Runtime

CAND-015:
> ACTIVE / PROTECTED / UNTOUCHED

CAND-024:
> ACTIVE / PROTECTED / UNTOUCHED

CAND-035:
> ACTIVE / PROTECTED / UNTOUCHED

---

## 20. G1

> NOT EXECUTED

---

## 21. G2

> NOT EXECUTED

---

## 22. System Assembly

> NOT EXECUTED

---

## 23. Next Milestone

> G1 — ECONOMIC PLAUSIBILITY SCREEN
