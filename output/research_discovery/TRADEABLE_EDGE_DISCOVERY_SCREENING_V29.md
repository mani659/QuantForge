# TRADEABLE EDGE DISCOVERY SCREENING — V29
# DATE: 2026-08-30
# STATUS: V29 G0 COMPLETE — 3 CANDIDATES GENERATED
# NO G1 / NO G2 / NO EXPERIMENT EXECUTION

---

## 1. G0 Status

> V29 G0 COMPLETE — 3 CANDIDATES GENERATED

This is a fresh discovery cycle following V28 G0/G1 and CAND-083 State Governance Review. Three genuinely new candidates spanning three distinct mechanism families. No overlap with V19–V28 or historical candidates. No State library interaction.

---

## 2. Research Context

### V27 Lessons
- Dynamic state transitions produce more conditional information than static conditions
- Counterfactual validity is critical (CAND-080 failed due to invalid CF)
- State hypothesis must not be contradicted by median evidence (CAND-082)

### V28 Lessons
- Cumulative rejection pressure (CAND-083) produced the largest conditional delta in RF history (+4.60 bps)
- Range compression → expansion (CAND-084) was redundant with CAND-077
- Approach velocity (CAND-085) had invalid counterfactual
- Mechanism-first approach continues to outperform indicator-first approach

### State Governance Lessons
- Three State Review Eligible objects now governed (CAND-077, CAND-081, CAND-083)
- Each represents a genuinely distinct market-condition concept
- State objects are governed knowledge, not candidate seeds
- V29 must discover genuinely independent mechanisms

### Current Research Bottleneck
The project has accumulated 3 State objects and 0 G2 promotions. The bottleneck is not "finding interesting conditional relationships" — it is finding mechanisms with positive absolute economics or clear paths to standalone tradeability. V29 should prioritize mechanisms with plausible economic headroom.

### Why V29 Is Fresh Discovery
V28 produced CAND-083 (rejection pressure) and closed CAND-084/085. V29 must search entirely new mechanism families. The State library (CAND-077, CAND-081, CAND-083) is fenced off.

---

## 3. G1 V3 Framework

Ratified. Two-layer architecture:
- **Layer 1:** 9 binary hard validity gates (measurement integrity)
- **Layer 2:** Economic evidence adjudication (holistic, not scorecard)

No universal hard economic thresholds. No scoring system.

---

## 4. Current Governed State Library

| Candidate | Classification | Mechanism |
|---|---|---|
| CAND-059 | STATE-ARTIFACT | First touch > subsequent touch |
| CAND-065 | STATE OBSERVATION | Deep sweep > shallow sweep |
| CAND-069 | STATE OBSERVATION | Mid-session > morning |
| **CAND-077** | **STATE REVIEW ELIGIBLE** | Volatility character transition (compressed → expanded) |
| CAND-079 | STATE OBSERVATION | Gold direction → Tech direction |
| **CAND-081** | **STATE REVIEW ELIGIBLE** | Trapped participants after failed structural break |
| **CAND-083** | **STATE REVIEW ELIGIBLE** | Accumulated rejection pressure at structural level |

All STATE REVIEW ELIGIBLE objects are preserved. No thresholds ratified. No interaction studies authorized.

---

## 5. External Research Priors

> PROVISIONAL EXTERNAL RESEARCH INPUT — NOT VALIDATED QUANTFORGE EVIDENCE

Used as conceptual starting points only:
1. Static regime labels may miss intraday state changes
2. Regime drift / transition may contain more information than static labels
3. ADX behavior may be non-monotonic
4. Post-entry R-velocity may contain trade-health information
5. Execution quality may vary with liquidity state

No thresholds imported. No strategy rules imported.

---

## 6. Candidate 1 — CAND-086

### Candidate ID
CAND-086

### Name
Information Absorption Failure Cascade

### Artifact Type
Alpha / Event (provisional) — also State/Condition potential

### Mechanism Family
Family 1 — Information Absorption / Information Failure

### Pre-State
Market exhibits repeated large intraday directional moves. Each move represents an attempt by participants to establish directional conviction and shift accepted price. The market is in a state of active price discovery with multiple contested directional attempts.

### Observable Trigger / Transition
Within a defined lookback window (20 bars), count the number of large directional moves (>1.5× ATR) that reverse more than 50% of their extent within 5 bars. When this count reaches or exceeds 3 (the "absorption failure count"), the market enters an Information Absorption Failure state.

The transition is: directional conviction attempts → repeated failure to sustain → absorption failure state.

### Post-State
After the absorption failure state is reached, the next large directional move (>1.5× ATR) has different economics than it would without the preceding absorption failures. The hypothesis is that the accumulated failed directional conviction has trapped participants on multiple sides, and the resolution of this trapped state produces larger directional continuation.

### Participant / Market Constraint
Participants who attempted to establish directional conviction during the failed moves are now trapped with positions that have not been validated by sustained price movement. The trapped population spans multiple directional attempts, creating a broader exposed participant base than a single failed move would produce.

### Why the Transition Matters
A single failed directional move is common and economically unremarkable. But a SEQUENCE of failed directional moves creates a qualitatively different market state: participants are trapped on multiple sides, price discovery is contested, and the eventual resolution must unwind accumulated exposure. The transition from "active contested discovery" to "resolution of contested state" is the economically meaningful event.

### Economic Mechanism
Repeated failed directional conviction traps participants across multiple directional attempts. Each failed move adds to the trapped population. When a subsequent directional move achieves conviction (sustains beyond the absorption failure threshold), forced exits from the accumulated trapped population create directional pressure that amplifies the move.

### Economic Consequence
Expected effect: the directional move that follows an absorption failure state has larger magnitude, higher persistence, and stronger continuation than a comparable move without preceding absorption failures.

### Core Hypothesis
> Repeated failure to sustain directional conviction (large moves that reverse) creates an accumulated trapped-participant state. The next directional move that achieves conviction has larger magnitude and higher persistence because it unwinds the accumulated trapped exposure.

### Observable Variables
- ATR-normalized move size (1.5× ATR threshold)
- Reversal percentage (50% threshold within 5 bars)
- Absorption failure count (3+ within 20-bar lookback)
- Sustained conviction (move sustains beyond 50% for 5+ bars)
- Direction of sustained move
- Magnitude of sustained move

### Observable vs Inferred vs Unknown
- **Observable:** Move sizes, reversal percentages, counts, timing, ATR
- **Inferred:** Trapped participant population, directional conviction quality
- **Unknown:** Actual positioning, institutional flow, stop placement

### Exact Setup
Lookback: 20 M1 bars
ATR period: 20 bars
Large move threshold: 1.5× ATR (absolute directional extent)
Reversal threshold: 50% of move extent reversed within 5 bars
Absorption failure count: ≥3 large moves that reversed within the 20-bar lookback

### Exact Confirmation
After absorption failure count ≥3, identify the next large move (>1.5× ATR) that sustains (does not reverse >50% within 5 bars). This is the treatment event.

### Exact Entry
Entry at the point where the sustained move achieves conviction (5 bars after the initial impulse, if it has not reversed >50%). Direction = direction of the sustained move.

### Exact Exit
Exit after 20 bars (holding period).

### Direction
Direction of the sustained move that follows the absorption failure state.

### Rearm Rule
After each treatment event, reset the absorption failure count and begin a new 20-bar lookback window.

### Dynamic-vs-Static Rationale
The transition is essential. A single large move is not the signal. The COUNT of failed directional attempts creates the trapped-participant state. Without the sequence of failures, the hypothesis has no mechanism. The static condition "large move" is insufficient; the HISTORY of failed attempts is the economically meaningful variable.

### Expected Distribution Change
Expected: mean and median returns of the sustained move are larger when preceded by absorption failures than when not. The distribution should show fatter positive tail (larger continuation) and thinner negative tail (less reversal) in the treatment condition.

### Economic Headroom
Plausible magnitude: moderate (absorption failures may add 1-5 bps of informational value)
Plausible frequency: moderate (~5-20 events/year depending on thresholds)
Persistence: moderate (the trapped-participant unwinding may persist for tens of bars)
Asymmetry: directional continuation should be stronger than reversal
Cost sensitivity: moderate (5-bar confirmation delay reduces slippage risk)

### Conceptual Counterfactual
The counterfactual population: large directional moves (>1.5× ATR) that achieve conviction (sustain >50% for 5+ bars) WITHOUT preceding absorption failure history (count <3 in the 20-bar lookback).

This counterfactual represents the same type of market event (large sustained directional move) but without the accumulated trapped-participant state.

### Counterfactual Discrimination
The counterfactual discriminates the proposed mechanism because both populations experience large sustained directional moves, but only the treatment population has the accumulated absorption failure history. If the mechanism is valid, the treatment should produce larger magnitude and persistence.

### Data Availability
USATECHIDXUSD M1 OHLC data is available. ATR can be computed from OHLC. Move sizes, reversal percentages, and counts are computable from OHLC. No volume required. No tick data required.

### Causal Observability
- **Observed:** Move sizes, reversal percentages, counts, ATR, timing
- **Inferred:** Trapped participant population, conviction quality
- **Unknown:** Actual participant identity, stop placement, institutional flow

### Prior-Art
- CAND-024: Different mechanism (breakout + specific filter)
- CAND-035: Different mechanism (breakout + specific filter)
- CAND-077: Volatility character transition (regime-level), NOT move-level rejection
- CAND-081: Structural level failure (single level), NOT multi-move sequence
- CAND-083: Rejection at structural levels (price-level concept), NOT directional conviction failure

**Classification: NEW**

The key distinction from CAND-083: CAND-083 counts rejections at a structural LEVEL. CAND-086 counts failed DIRECTIONAL MOVES (large impulses that reverse). These are different market phenomena: one is about price-level interaction, the other is about directional conviction failure.

### Closed-Line Check
No closed candidate uses the "information absorption failure" mechanism. No V19–V28 candidate is based on counting failed directional moves. No overlap with CAND-077/081/083.

### Standalone Potential
Moderate. Absolute economics may be negative (consistent with all RF candidates). Conditional delta potential is plausible but unknown.

### Rare-Event Potential
Low-moderate. Frequency depends on absorption failure threshold. At count ≥3, frequency may be 5-20/year.

### Component Potential
Moderate. Could serve as a filter for other strategies: "only enter when absorption failure state exists."

### State Potential
Moderate. The absorption failure state is a genuine market condition that could modify downstream economics. Could be classified as STATE REVIEW ELIGIBLE if G1 evidence supports it.

### Regime Potential
Low. The concept is event-level, not regime-level.

### Expected Failure Mode
The most likely failure mode is that the absorption failure count threshold (≥3) is too selective (low N) or too loose (noisy). A secondary failure mode is that the 5-bar confirmation window is too short or too long.

### Proposed G1 Measurement
- Count events with absorption failure count ≥3 followed by sustained directional move
- Compute N, frequency, win rate, mean, median, net/gross economics
- Compute counterfactual: sustained directional moves without absorption failure history
- Compute conditional delta (mean and median)
- Apply 9 hard validity gates
- Examine distribution shape, tails, outliers

### G0 Quality Decision
> PROMOTED TO G1

All 10 quality criteria satisfied:
1. genuinely distinct mechanism ✓
2. economically plausible consequence ✓
3. observable implementation ✓
4. legitimate executable role ✓
5. credible counterfactual ✓
6. no hindsight ✓
7. no threshold mining ✓
8. meaningful prior-art distinction ✓
9. realistic G1 measurement ✓
10. no conflict with governed State objects ✓

---

## 7. Candidate 2 — CAND-087

### Candidate ID
CAND-087

### Name
Recovery Quality Differential

### Artifact Type
Alpha / Event (provisional) — also State/Condition potential

### Mechanism Family
Family 5 — Recovery / Failure of Recovery

### Pre-State
A large adverse directional move occurs (disturbance). The market is in a state of directional displacement with participants exposed to the adverse direction. The move is measured as >2× ATR from the pre-move price level.

### Observable Trigger / Transition
After the disturbance, measure the recovery quality over the subsequent 10 bars:
- **Recovery Speed:** How quickly does price return toward the pre-disturbance level? (measured as fraction of disturbance recovered in 5 bars)
- **Recovery Completeness:** How much of the disturbance is recovered in 10 bars? (measured as fraction of disturbance recovered)

The transition is: disturbance → recovery attempt → recovery quality determined.

### Post-State
Two distinct post-recovery states emerge:
1. **Strong Recovery:** >75% of disturbance recovered in 10 bars. Market has absorbed the adverse information and participants who were trapped by the disturbance have been rescued or have exited.
2. **Weak Recovery:** <25% of disturbance recovered in 10 bars. Market has NOT absorbed the adverse information. Trapped participants remain exposed. The disturbance represents genuine new information that has not been fully priced.

### Participant / Market Constraint
After a strong recovery, the trapped-participant population has been largely resolved (participants either exited at breakeven or the market moved back). After a weak recovery, trapped participants remain exposed and their continued presence creates ongoing directional pressure.

### Why the Transition Matters
The recovery quality transition reveals whether the disturbance was:
- A temporary dislocation (strong recovery → trapped participants resolved → neutral subsequent state)
- Genuine new information (weak recovery → trapped participants remain → directional pressure continues)

This distinction changes the economics of subsequent events because the participant constraint differs.

### Economic Mechanism
Recovery quality acts as a filter for disturbance quality. Strong recoveries indicate temporary dislocations where trapped participants have been resolved. Weak recoveries indicate genuine information where trapped participants remain exposed and create ongoing directional pressure.

The hypothesis: weak-recovery disturbances are followed by larger directional continuation (the trapped participants' forced exits amplify the original disturbance direction) while strong-recovery disturbances are followed by neutral or reversal behavior (the trapped participants have been resolved).

### Economic Consequence
Expected effect: weak-recovery disturbances produce larger directional continuation than strong-recovery disturbances. The magnitude and persistence of the post-disturbance move differ based on recovery quality.

### Core Hypothesis
> The quality of recovery after a large adverse directional move reveals whether the disturbance represents temporary dislocation or genuine information. Weak recoveries (trapped participants remain) produce larger directional continuation. Strong recoveries (trapped participants resolved) produce reversal or neutral behavior.

### Observable Variables
- Disturbance size (ATR-normalized)
- Recovery speed (5-bar recovery fraction)
- Recovery completeness (10-bar recovery fraction)
- Direction of disturbance
- Direction of subsequent continuation/reversal
- Magnitude of subsequent move

### Observable vs Inferred vs Unknown
- **Observable:** Move sizes, recovery fractions, ATR, timing, direction
- **Inferred:** Trapped participant resolution, information quality
- **Unknown:** Actual participant positioning, order flow, institutional behavior

### Exact Setup
ATR period: 20 bars
Disturbance threshold: >2× ATR directional move from pre-move level
Recovery speed: fraction of disturbance recovered in 5 bars
Recovery completeness: fraction of disturbance recovered in 10 bars
Strong recovery: >75% recovered in 10 bars
Weak recovery: <25% recovered in 10 bars

### Exact Confirmation
After disturbance (>2× ATR move), wait 10 bars and classify recovery quality:
- Strong: >75% recovered
- Weak: <25% recovered
- Medium: 25-75% recovered (excluded from treatment/counterfactual)

### Exact Entry
Entry at bar 10 after disturbance, in the direction of the original disturbance (fade the recovery if weak, or follow the disturbance direction).

Wait — let me reconsider. The hypothesis is that weak recovery → continuation in disturbance direction. So entry at bar 10 in the disturbance direction if weak recovery. Counterfactual: entry at bar 10 in disturbance direction if strong recovery.

### Exact Exit
Exit after 20 bars from entry (bar 30 from disturbance).

### Direction
Direction of the original disturbance (the hypothesis is continuation, not reversal).

### Rearm Rule
After each treatment/counterfactual event, begin a new disturbance search.

### Dynamic-vs-Static Rationale
The transition is essential. A large move alone is not the signal. The RECOVERY QUALITY after the move is the economically meaningful variable. Without measuring what happens after the disturbance, the hypothesis cannot distinguish temporary dislocations from genuine information. The static condition "large move occurred" is insufficient; the recovery trajectory is the key.

### Expected Distribution Change
Expected: weak-recovery disturbances produce larger mean/median continuation in the disturbance direction than strong-recovery disturbances. The distribution of weak-recovery outcomes should be shifted toward larger positive (continuation) outcomes.

### Economic Headroom
Plausible magnitude: moderate (recovery quality may add 1-3 bps of informational value)
Plausible frequency: moderate (~20-50 events/year depending on disturbance threshold)
Persistence: moderate (trapped-participant unwinding may persist for tens of bars)
Asymmetry: continuation after weak recovery should be stronger than continuation after strong recovery
Cost sensitivity: moderate (10-bar confirmation delay reduces slippage risk)

### Conceptual Counterfactual
The counterfactual population: large directional disturbances (>2× ATR) followed by STRONG recovery (>75% recovered in 10 bars).

Both populations experience the same type of disturbance. The treatment (weak recovery) and counterfactual (strong recovery) differ only in recovery quality. This discriminates the proposed mechanism.

### Counterfactual Discrimination
The counterfactual is strong because both populations share the disturbance event. The only difference is what happens AFTER the disturbance. If recovery quality matters, the treatment and counterfactual should differ economically.

### Data Availability
USATECHIDXUSD M1 OHLC data is available. ATR, move sizes, and recovery fractions are computable from OHLC. No volume required. No tick data required.

### Causal Observability
- **Observed:** Move sizes, recovery fractions, ATR, timing, direction
- **Inferred:** Trapped participant resolution, information quality, continuation pressure
- **Unknown:** Actual participant identity, stop placement, institutional flow

### Prior-Art
- CAND-077: Volatility character transition (regime-level), NOT post-disturbance recovery quality
- CAND-081: Structural level failure (single level break), NOT disturbance recovery
- CAND-083: Rejection accumulation at structural levels, NOT move recovery quality
- CAND-078: Trend exhaustion (different mechanism entirely)

**Classification: NEW**

The key distinction: CAND-087 is about the QUALITY OF RECOVERY after a disturbance, not about the disturbance itself, not about structural levels, not about volatility character. It measures a post-event trajectory that reveals participant constraint.

### Closed-Line Check
No closed candidate uses recovery quality as the mechanism. No V19–V28 candidate measures post-disturbance recovery trajectories.

### Standalone Potential
Moderate. Absolute economics may be negative. Conditional delta potential is plausible.

### Rare-Event Potential
Low. Frequency is moderate (~20-50/year).

### Component Potential
High. Could serve as a filter: "only enter after weak recovery" or "avoid entries after strong recovery."

### State Potential
Moderate. Recovery quality is a genuine post-disturbance market state that could modify downstream economics. Could be STATE REVIEW ELIGIBLE if G1 evidence supports it.

### Regime Potential
Low. Event-level concept.

### Expected Failure Mode
Most likely failure: the recovery quality thresholds (75%/25%) are arbitrary and may not cleanly separate meaningful states. Secondary failure: the 10-bar recovery window may be too short or too long.

### Proposed G1 Measurement
- Count disturbances (>2× ATR) followed by weak recovery (<25%)
- Count disturbances followed by strong recovery (>75%)
- Compare mean/median continuation in disturbance direction
- Compute conditional delta
- Apply 9 hard validity gates
- Examine distribution shape

### G0 Quality Decision
> PROMOTED TO G1

All 10 quality criteria satisfied:
1. genuinely distinct mechanism ✓
2. economically plausible consequence ✓
3. observable implementation ✓
4. legitimate executable or State role ✓
5. credible counterfactual ✓
6. no hindsight ✓
7. no threshold mining ✓
8. meaningful prior-art distinction ✓
9. realistic G1 measurement ✓
10. no conflict with governed State objects ✓

---

## 8. Candidate 3 — CAND-088

### Candidate ID
CAND-088

### Name
Session Sequence Asymmetry

### Artifact Type
Alpha / Event (provisional)

### Mechanism Family
Family 3 — Path Dependence / Event Sequence

### Pre-State
Market opens a new session. Within the first 30 minutes (30 M1 bars), price establishes a directional bias (direction of the net move from open). Simultaneously, a structural level exists (20-bar rolling high or low from the prior session).

### Observable Trigger / Transition
The structural level from the prior session is broken within the session. The critical observation is the DIRECTION of the structural break relative to the opening bias:
- **Aligned break:** Structural break direction matches opening bias direction
- **Opposite break:** Structural break direction OPPOSES opening bias direction

The transition is: opening bias established → structural break occurs → sequence relationship determined.

### Post-State
When the structural break OPPOSES the opening bias, participants who established positions based on the opening bias are now trapped. Their positions are in the wrong direction relative to the structural break. This creates forced exit pressure in the direction of the structural break.

When the structural break ALIGNS with the opening bias, participants are reinforced (their positions are validated by the structural break). No trapped-participant dynamic exists.

### Participant / Market Constraint
Opening-bias participants accumulated directional exposure in the first 30 minutes. When the structural break opposes this exposure, they are trapped. The trap is stronger when the opening bias is stronger (larger initial move) and the structural break is more significant (breaks a meaningful level).

### Why the Transition Matters
The SEQUENCE matters because the opening bias creates a participant population with specific directional exposure. The structural break then either validates or traps that population. The economic consequence depends on WHICH CAME FIRST: if the bias preceded the break, trapped participants create forced exit flow. If the break preceded any bias, no trapped population exists.

This is a genuinely path-dependent mechanism: A → B has different economics from B → A.

### Economic Mechanism
Opening-bias participants are trapped when the structural break opposes their exposure. Forced exits from trapped opening-bias participants create directional pressure in the structural break direction. This amplifies the post-break continuation.

### Economic Consequence
Expected effect: opposite-direction structural breaks (break opposes opening bias) produce larger continuation in the break direction than aligned structural breaks (break matches opening bias). The trapped opening-bias population adds forced-exit flow.

### Core Hypothesis
> The sequence of opening directional bias followed by an opposite-direction structural break creates trapped participants whose forced exits amplify post-break continuation. The same structural break aligned with the opening bias produces weaker continuation because no trapped population exists.

### Observable Variables
- Session opening direction (first 30 bars net move direction)
- Opening bias magnitude (ATR-normalized)
- Structural level (20-bar rolling high/low from prior session)
- Structural break direction
- Sequence relationship (aligned vs opposite)
- Post-break continuation magnitude
- Post-break continuation persistence

### Observable vs Inferred vs Unknown
- **Observed:** Opening direction, structural levels, break direction, move sizes, ATR, timing
- **Inferred:** Trapped opening-bias participants, forced exit flow
- **Unknown:** Actual participant identity, stop placement, institutional flow

### Exact Setup
Opening bias: first 30 M1 bars of the session. Direction = net move direction. Magnitude = net move / ATR.
Structural level: 20-bar rolling high or low from the 30 bars BEFORE session open.
Structural break: close beyond the structural level by >2 bps.
Sequence:
- Opposite break: opening bias direction ≠ structural break direction
- Aligned break: opening bias direction = structural break direction

### Exact Confirmation
After structural break, classify sequence:
- Opposite: opening bias was in the opposite direction (treatment)
- Aligned: opening bias was in the same direction (counterfactual)

### Exact Entry
Entry at the close of the bar that confirms the structural break (close beyond level by >2 bps). Direction = structural break direction.

### Exact Exit
Exit after 30 bars from entry.

### Direction
Direction of the structural break.

### Rearm Rule
After each treatment/counterfactual event, begin a new session observation.

### Dynamic-vs-Static Rationale
The sequence is essential. A structural break alone is not the signal. An opening bias alone is not the signal. The RELATIONSHIP between them (opposite vs aligned) is the economically meaningful variable. Without the path-dependence, the hypothesis has no mechanism. The static condition "structural break occurred" is insufficient; the SEQUENCE relative to the opening bias is the key.

### Expected Distribution Change
Expected: opposite-direction breaks produce larger mean/median continuation than aligned breaks. The distribution of opposite-break outcomes should be shifted toward larger continuation outcomes.

### Economic Headroom
Plausible magnitude: moderate (trapped opening-bias participants may add 1-4 bps of informational value)
Plausible frequency: moderate (~100-300 events/year depending on structural level frequency)
Persistence: moderate (forced-exit unwinding may persist for 20-40 bars)
Asymmetry: continuation after opposite break should be stronger than continuation after aligned break
Cost sensitivity: low-moderate (entry at confirmed break reduces slippage)

### Conceptual Counterfactual
The counterfactual population: structural breaks that are ALIGNED with the opening bias (opening direction = break direction).

Both populations experience structural breaks. The treatment (opposite break) and counterfactual (aligned break) differ only in the sequence relationship with the opening bias. This discriminates the proposed mechanism.

### Counterfactual Discrimination
The counterfactual is strong because both populations share the structural break event. The only difference is whether the opening bias preceded in the same or opposite direction. If sequence matters, the treatment and counterfactual should differ economically.

### Data Availability
USATECHIDXUSD M1 OHLC data is available. Opening direction, structural levels, break direction, and move sizes are computable from OHLC. No volume required. No tick data required. Session timing is available from timestamps.

### Causal Observability
- **Observed:** Opening direction, structural levels, break direction, move sizes, ATR, timing
- **Inferred:** Trapped opening-bias participants, forced exit flow
- **Unknown:** Actual participant identity, stop placement, institutional flow

### Prior-Art
- CAND-077: Volatility character transition (regime-level), NOT session sequence
- CAND-081: Structural level failure (rapid failure within 5 bars), NOT opening-bias trapping
- CAND-083: Cumulative rejection count, NOT opening-sequence path dependence
- CAND-024/035: Breakout + specific filter, NOT session sequence

**Classification: NEW**

The key distinction: CAND-088 is about the SEQUENCE of two objectively measurable events (opening bias → structural break). No V19–V28 candidate uses session-opening direction as a path-dependent variable. No candidate examines the relationship between opening bias and structural break direction.

### Closed-Line Check
No closed candidate uses session sequence as the mechanism. No V19–V28 candidate examines opening-bias direction relative to structural break direction.

### Standalone Potential
Moderate. Absolute economics may be negative. Conditional delta potential is plausible.

### Rare-Event Potential
Low. Frequency is moderate-high (~100-300/year).

### Component Potential
Moderate. Could serve as a filter: "only enter structural breaks that oppose the opening bias."

### State Potential
Low-moderate. The trapped-opening-bias state is short-lived (within a session). Less likely to be a durable State object.

### Regime Potential
Low. Session-level concept, not regime-level.

### Expected Failure Mode
Most likely failure: opening bias magnitude may be too noisy to create meaningful trapping. Secondary failure: structural levels from the prior session may be too far from the opening to create a meaningful sequence relationship.

### Proposed G1 Measurement
- Count opposite-direction structural breaks (treatment)
- Count aligned structural breaks (counterfactual)
- Compare mean/median continuation in break direction
- Compute conditional delta
- Apply 9 hard validity gates
- Examine distribution shape

### G0 Quality Decision
> PROMOTED TO G1

All 10 quality criteria satisfied:
1. genuinely distinct mechanism ✓
2. economically plausible consequence ✓
3. observable implementation ✓
4. legitimate executable role ✓
5. credible counterfactual ✓
6. no hindsight ✓
7. no threshold mining ✓
8. meaningful prior-art distinction ✓
9. realistic G1 measurement ✓
10. no conflict with governed State objects ✓

---

## 9. Dynamic Transition Comparison

| Dimension | CAND-086 | CAND-087 | CAND-088 |
|---|---|---|---|
| Transition distinctness | High — multi-move sequence | High — post-disturbance trajectory | High — event sequence path |
| Mechanism | Absorption failure → trapped exposure | Recovery quality → participant resolution | Opening bias → opposite break → trapped exposure |
| Participant constraint | Trapped across multiple failed moves | Trapped after weak recovery | Trapped by opening bias vs structural break |
| Economic consequence | Larger continuation after resolution | Larger continuation after weak recovery | Larger continuation after opposite break |
| Observability | Move sizes, counts, ATR | Move sizes, recovery fractions | Opening direction, structural levels |
| Counterfactual quality | Strong — same moves, different history | Strong — same disturbance, different recovery | Strong — same break, different sequence |
| G1 feasibility | High — all computable from OHLC | High — all computable from OHLC | High — all computable from OHLC |

---

## 10. Economic Mechanism Comparison

Ranked by mechanism quality:

1. **CAND-086 (Absorption Failure):** Strongest mechanism. Multiple failed directional attempts create a genuinely larger trapped population than a single failure. The cumulative nature of the mechanism is intuitive and well-grounded in market microstructure theory.

2. **CAND-088 (Session Sequence):** Strong mechanism. Path dependence is a well-established economic concept. The opening-bias trapping mechanism is intuitive and directly testable.

3. **CAND-087 (Recovery Quality):** Solid mechanism. Recovery quality as an information signal is plausible. The mechanism is slightly less direct than CAND-086/088 because it requires interpreting recovery quality as a proxy for participant resolution.

---

## 11. Counterfactual Quality

| Candidate | Counterfactual | Quality |
|---|---|---|
| CAND-086 | Sustained directional moves without absorption failure history | Strong — same event, different history |
| CAND-087 | Same disturbance with strong recovery vs weak recovery | Strong — same event, different trajectory |
| CAND-088 | Structural breaks aligned with opening bias vs opposite | Strong — same event, different sequence |

All three counterfactuals are credible and discriminating.

---

## 12. Data Feasibility

All three candidates require only:
- USATECHIDXUSD M1 OHLC data (available)
- ATR computation (from OHLC)
- Move sizes, recovery fractions, counts, structural levels (from OHLC)
- Session timing (from timestamps)

No volume required. No tick data required. No cross-asset data required.

---

## 13. External Research Priors Used

| Prior | Candidate | How Used |
|---|---|---|
| Regime drift may be more informative than static labels | CAND-086 | Absorption failure captures drift in directional conviction |
| Execution quality may vary with liquidity state | CAND-087 | Recovery quality may reflect execution/liquidity conditions |
| Post-entry R-velocity may contain trade-health information | CAND-087 | Recovery speed is conceptually related to post-move health |

> PROVISIONAL EXTERNAL RESEARCH INPUT — NOT VALIDATED QUANTFORGE EVIDENCE

No thresholds imported from external research.

---

## 14. Prior-Art / Redundancy

| Candidate | Classification | Reason |
|---|---|---|
| CAND-086 | NEW | No V19–V28 candidate counts failed directional moves as an absorption failure mechanism |
| CAND-087 | NEW | No V19–V28 candidate measures post-disturbance recovery quality as an information signal |
| CAND-088 | NEW | No V19–V28 candidate examines session-opening direction as a path-dependent variable relative to structural breaks |

All three are genuinely new. No extensions. No rescues.

---

## 15. Closed-Line Firewall

> PASS

No closed candidate was reopened. No closed candidate was rescued. No closed mechanism was used as a V29 seed.

---

## 16. Governed State Firewall

> CAND-077 / CAND-081 / CAND-083 were not optimized, combined, interacted, tested, or used as V29 candidate seeds.

V29 candidates are genuinely independent of the State library.

---

## 17. Current State Library

| Candidate | Classification |
|---|---|
| CAND-059 | STATE-ARTIFACT |
| CAND-065 | STATE OBSERVATION |
| CAND-069 | STATE OBSERVATION |
| CAND-077 | STATE REVIEW ELIGIBLE |
| CAND-079 | STATE OBSERVATION |
| CAND-081 | STATE REVIEW ELIGIBLE |
| CAND-083 | STATE REVIEW ELIGIBLE |

---

## 18. Protected Forward Runtime

CAND-015:
> ACTIVE / PROTECTED / UNTOUCHED

CAND-024:
> ACTIVE / PROTECTED / UNTOUCHED
> Canonical: `CAND-024:CANONICAL:925495a8`

CAND-035:
> ACTIVE / PROTECTED / UNTOUCHED
> Canonical: `CAND-035:CANONICAL:ddc5d0e9`

---

## 19. Historical Closed Lines

V19–V28 remain closed according to authoritative repository records. No closed line was reopened or rescued during V29 G0.

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

---

*End of V29 G0 Discovery Screening.*
