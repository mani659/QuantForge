# TRADEABLE EDGE DISCOVERY SCREENING — V27
# DATE: 2026-08-30
# STATUS: V27 G0 COMPLETE — 3 CANDIDATES GENERATED
# NO G1 / NO G2 / NO EXPERIMENT EXECUTION

---

## 1. G0 Status

> V27 G0 COMPLETE — 3 CANDIDATES GENERATED

Three candidates spanning three distinct dynamic state-transition mechanism families. All candidates are genuinely new — no overlap with V19–V26 or historical candidates.

---

## 2. V26 Lessons

V26 produced the first positive conditional deltas in Research Factory history:

- CAND-077: +1.67 bps delta (compression → expansion transition)
- CAND-079: +0.78 bps delta (Gold vol transition → Tech)
- CAND-078: -0.25 bps delta (counterfactual superior)

Key lesson: **Dynamic state transitions produce more conditional information than static conditions.** V27 must build on this by exploring genuinely different transition types.

CAND-077's post-closure filter observation (breakout >15 bps = 64.8% WR, +8.41 bps) is classified as EXPLORATORY EVIDENCE ONLY — not validated, not a threshold, not a V27 input.

---

## 3. G1 V3 Framework

Ratified. Two-layer architecture:
- Layer 1: 9 binary hard validity gates
- Layer 2: Economic evidence adjudication

Four artifact classes: Standalone Alpha, Rare-Event Alpha, State/Condition, Regime/Specialist.

No universal hard economic thresholds. Evidence-based holistic adjudication.

---

## 4. External Statistical Research Priors

> PROVISIONAL EXTERNAL RESEARCH INPUT — NOT VALIDATED QUANTFORGE EVIDENCE

Used as conceptual starting points only:
- A: Static regime labels may be less useful than regime drift
- B: Volatility development may differ from already-expanded volatility
- C: ADX may be non-monotonic (extreme = possible exhaustion)
- D: Execution quality may deteriorate during certain liquidity states
- E: R-velocity after entry may contain trade-health information

No thresholds imported. All V27 definitions are independent.

---

## 5. Candidate 1 — CAND-080

### Candidate ID
CAND-080

### Name
Volatility Regime Quality Transition

### Artifact Type
Alpha / Event (provisional) — may also serve as State/Condition

### Mechanism Family
Volatility Development — Regime Character Transition

### Pre-Transition State
Market is in a smooth, low-noise trending state:
- ATR is moderate (not compressed, not expanded)
- Price advances/retracts in consistent direction with small counter-moves
- Intraday bars show limited overlap (clean directional structure)
- Measured by: ATR percentile in 30th–60th range + low bar-to-bar directional inconsistency

### Transition
A transition occurs where the market shifts from smooth directional movement to choppy, high-noise movement within the same volatility level:
- ATR level remains roughly constant (no major expansion)
- Bar-to-bar directional inconsistency increases sharply
- Counter-moves become larger relative to directional moves
- The market character changes from "trending" to "choppy"

### Post-Transition State
Market is now choppy and noisy:
- Same ATR level but higher directional inconsistency
- Frequent reversals within the bar sequence
- Stops on both sides are being triggered
- Participants who entered during the smooth phase are being shaken out

### Participant Constraint
During the smooth trending phase, participants accumulate directional positions with tight stops. The regime quality transition (smooth → choppy) triggers stop cascades on both sides without a clear directional resolution, creating forced two-way flow that did not exist during the smooth phase.

### Why the Transition Matters
This is fundamentally different from CAND-077:
- CAND-077 = volatility LEVEL change (compressed → expanding)
- CAND-080 = volatility CHARACTER change (smooth → choppy at same level)

A market can be choppy at low ATR or smooth at high ATR. The character of the volatility matters independently of its magnitude.

### Economic Consequence
The choppy regime following a smooth phase may create:
- Increased frequency of false breakouts
- Higher stop-hit rate on both sides
- Reduced follow-through on directional moves
- Potential for mean-reversion strategies to outperform trend-following

The hypothesis tests whether the transition itself creates a measurable shift in the distribution of subsequent directional moves.

### Hypothesis
When a market transitions from smooth directional movement to choppy movement (at roughly the same ATR level), the subsequent N-bar return distribution changes measurably compared with:
1. Continued smooth movement (no transition)
2. Already-choppy movement (no transition)

The transition is the signal, not the static state.

### Observable Variables
- ATR (20-bar, M1)
- Bar-to-bar directional inconsistency (rolling measure of how often consecutive bars close in opposite directions)
- Smooth-to-choppy transition detection (directional inconsistency increases by >50% from recent average while ATR remains within 80% of its recent level)
- Subsequent N-bar return (directional move quality)

### Exact Setup
1. Compute 20-bar ATR on USATECHIDXUSD M1
2. Compute directional inconsistency ratio: fraction of last 20 bars where close direction differs from previous close direction
3. Detect transition: directional inconsistency increases from <35% (smooth) to >50% (choppy) while ATR remains within 80%–120% of its 20-bar average
4. Wait for next bar close after transition detection
5. Enter SHORT in direction opposite the prior smooth trend (fade the trapped trend participants)
6. Exit after 60 minutes

### Exact Confirmation
- Directional inconsistency must cross from below 35% to above 50%
- ATR must remain within 80%–120% of its 20-bar average (no major expansion)
- The transition must occur within a 10-bar window

### Exact Entry
At the close of the first bar where directional inconsistency exceeds 50% after being below 35%, enter in the direction OPPOSITE the prior smooth trend.

### Exact Exit
60 minutes (M1 bars) after entry.

### Direction
FADE the prior smooth trend direction (counter-trend entry after regime quality deterioration).

### Rearm Rule
After exit, do not re-enter for 60 minutes (1-hour cooldown). Each transition is an independent event.

### Dynamic-vs-Static Rationale
If the hypothesis could be equally expressed as "when directional inconsistency > 50%, fade the trend" without the transition requirement, it would fail this test. The transition requirement is essential because:
- Already-choppy markets may have different economics (participants are already adapted)
- The transition creates a specific population of trapped participants who were positioned for the smooth regime
- The forced-exit flow from these trapped participants is specific to the transition, not to the static choppy state

### Expected Distribution Change
The transition from smooth to choppy should:
- Increase the probability of a reversal (trapped participants exit)
- Decrease the probability of trend continuation
- Create a broader distribution (more uncertainty = larger potential moves in either direction)
- Shift the mean return toward the counter-trend direction

### Economic Headroom
If the trapped-participant exit flow creates even 2–3 bps of systematic directional pressure, this could survive friction. The transition is relatively rare (not every choppy period follows a smooth period), which may concentrate the effect.

### Counterfactual
The same fade-the-trend entry applied to:
1. Continuation of the smooth trend (no transition occurred)
2. Already-choppy markets (no transition — market was already choppy)

The counterfactual isolates the VALUE OF THE TRANSITION versus:
- Continuing to trend (smooth phase)
- Already being choppy (no transition event)

### Counterfactual Discrimination
The counterfactual is discriminating because it specifically removes the transition event while preserving the choppy state. If the fade works equally well in already-choppy markets, the transition adds no value. If the fade works only after the transition, the trapped-participant mechanism is supported.

### Data Availability
USATECHIDXUSD M1 data. ATR computable. Directional inconsistency computable. No volume required.

### Causal Observability
- OBSERVED: Regime quality transition and subsequent price behavior
- HYPOTHESIZED: Trapped participant exits creating forced flow
- UNPROVEN: Actual participant positioning or stop placement

### Prior-Art
NEW. No previous QuantForge candidate tested the "smooth-to-choppy regime quality transition" as a directional signal.

Historical check:
- CAND-077: volatility level change (compressed → expanding), NOT character change
- CAND-078: trend exhaustion (consecutive closes), NOT regime quality
- CAND-079: cross-market vol transition, NOT single-market character

### Closed-Line Check
No overlap with V19–V26. No overlap with DISC-021–028. No overlap with CAND-059–CAND-079.

### Standalone Potential
Moderate. The fade-the-trend entry may produce positive expectancy if trapped-participant exits are economically meaningful.

### Rare-Event Potential
Low-moderate. The smooth-to-choppy transition occurs at moderate frequency (~100–300/year estimated). Not rare enough for dedicated rare-event track unless economics are very strong.

### Component Potential
HIGH. If validated, this could serve as a State/Condition that suppresses trend-following entries or selects mean-reversion entries during choppy regimes.

### State Potential
HIGH. The regime quality transition is a genuine State concept — it describes a change in market conditions that could modify the behavior of other strategies.

### Regime Potential
MODERATE. Could become a regime specialist that is active only during choppy regimes.

### Expected Failure Mode
The most likely failure is that the choppy regime does not produce enough directional reversal pressure to survive friction. The transition may be too gradual to create a sharp forced-exit event.

### Proposed G1 Measurement
- N (number of smooth-to-choppy transitions)
- Frequency per year
- Mean/median return of counter-trend fade entry
- Win rate
- Counterfactual comparison (smooth continuation, already-choppy)
- Conditional delta (transition vs no-transition)
- Distribution shape (median, tail, worst event)

---

## 6. Candidate 2 — CAND-081

### Candidate ID
CAND-081

### Name
Structural Level Failure Trap

### Artifact Type
Alpha / Event (provisional) — may also serve as State/Condition

### Mechanism Family
Post-Event State Transition — Failed Breakout Trap

### Pre-Transition State
Price is approaching a significant structural level:
- Prior session high/low
- Prior day high/low
- Significant price level from recent trading (e.g., 20-bar high/low)
- Price is within 2 bps of the level

### Transition
Price breaks through the structural level by at least 3 bps (confirmed breakout), but then FAILS to continue in the breakout direction within 5 bars:
- Breakout occurs (price closes beyond level by 3+ bps)
- Within 5 bars, price reverses back through the level
- The breakout has FAILED — participants who entered on the breakout are now trapped

### Post-Transition State
The failed breakout has created a trap:
- Long participants who entered on the upside breakout are now underwater (price below their entry)
- Short participants who entered on the downside breakout are now underwater
- The level has been "tested and rejected" — it acts as a reference point for stop placement
- Forced exit flow from trapped participants creates directional pressure

### Participant Constraint
Participants who enter on a confirmed breakout expect continuation. When the breakout fails within 5 bars, these participants face losses. Their stops are placed beyond the breakout level. As price reverses through the level, stops are triggered, creating forced exit flow that accelerates the reversal.

### Why the Transition Matters
This is fundamentally different from:
- CAND-078 (trend exhaustion): CAND-081 requires a SPECIFIC structural level break and failure, not just consecutive same-direction closes
- CAND-059 (first touch > subsequent touch): CAND-081 requires the BREAK and FAIL, not just the touch
- CAND-065 (deep sweep > shallow sweep): CAND-081 requires the FAILURE after the break, not just the sweep depth

The key insight is that the FAILURE creates a specific population of trapped participants who did not exist before the breakout attempt.

### Economic Consequence
The trapped-participant exit flow should:
- Create directional pressure against the breakout direction
- Accelerate the reversal through the structural level
- Produce a measurable directional move in the opposite direction of the failed breakout
- Create an executable event with defined entry (after failure confirmation) and exit

### Hypothesis
When price breaks a significant structural level by 3+ bps but reverses back through the level within 5 bars, the subsequent N-bar return is:
- Directionally biased against the failed breakout direction
- Larger in magnitude than random reversals at the same level
- Economically meaningful after friction

### Observable Variables
- USATECHIDXUSD M1 price
- Structural level identification (20-bar high/low)
- Breakout detection (close beyond level by 3+ bps)
- Failure detection (close back through level within 5 bars)
- Subsequent N-bar return

### Exact Setup
1. Identify the 20-bar high (rolling, M1) as the structural level
2. Detect breakout: bar closes above 20-bar high by 3+ bps
3. Within the next 5 bars, detect failure: price closes back below the 20-bar high
4. After failure confirmation, enter SHORT at the close of the failure bar
5. Exit after 60 minutes

### Exact Confirmation
- Breakout bar must close 3+ bps above the 20-bar high
- Failure must occur within 5 bars of the breakout
- Failure bar must close below the 20-bar high

### Exact Entry
At the close of the first bar that closes below the 20-bar high after a confirmed breakout (within 5-bar window), enter SHORT.

### Exact Exit
60 minutes (M1 bars) after entry.

### Direction
SHORT (against the failed upside breakout). Mirror for downside failures: enter LONG after failed downside breakout.

### Rearm Rule
After exit, do not re-enter for 60 minutes. Each structural level failure is an independent event.同一 structural level cannot generate multiple events within 4 hours.

### Dynamic-vs-Static Rationale
If the hypothesis could be equally expressed as "when price is below the 20-bar high, go short" without the break-and-fail requirement, it would fail this test. The break-and-fail is essential because:
- It creates a specific population of trapped participants (those who entered on the breakout)
- The forced-exit flow is specific to the trap, not to the static position below the level
- The timing of the reversal is linked to the trap formation, not to the static level

### Expected Distribution Change
The failed breakout should:
- Increase the probability of continued reversal (trapped exits accelerate)
- Create a larger directional move than random reversals at the same level
- Produce a more asymmetric payoff (limited upside for the breakout, larger downside as stops cascade)
- Show higher win rate for counter-breakout entries than for random entries

### Economic Headroom
If trapped-participant exits create even 2–3 bps of systematic directional pressure, this could survive friction. The structural level provides a natural stop placement (beyond the breakout level), limiting risk.

### Counterfactual
The same entry applied to:
1. Successful breakouts (price breaks the level and continues — no failure)
2. Random reversals at the same level (no breakout attempt occurred)

The counterfactual isolates the VALUE OF THE TRAP versus:
- Successful breakouts (no trap)
- Random reversals (no trap formation)

### Counterfactual Discrimination
The counterfactual is discriminating because it specifically removes the trap event while preserving the structural level. If the fade works equally well for random reversals at the same level, the trap adds no value. If the fade works only after the trap, the trapped-participant mechanism is supported.

### Data Availability
USATECHIDXUSD M1 data. Price computable. Structural level computable. No volume required.

### Causal Observability
- OBSERVED: Breakout, failure, and subsequent price behavior
- HYPOTHESIZED: Trapped breakout participants creating forced exit flow
- UNPROVEN: Actual participant positioning or stop placement

### Prior-Art
NEW. No previous QuantForge candidate tested the "structural level break and failure trap" as a directional signal.

Historical check:
- CAND-059: first touch > subsequent touch (different — no break-and-fail required)
- CAND-065: deep sweep > shallow sweep (different — no failure requirement)
- CAND-070: momentum micro-structure failure (different — tested fading first structure break in trend, which was falsified)
- CAND-055: IB false breakout (similar concept but different mechanism — IB is a time-based level, not a structural price level; CAND-055 was outperformed by its counterfactual)

### Closed-Line Check
No overlap with V19–V26. No overlap with DISC-021–028. No overlap with CAND-059–CAND-079.

### Standalone Potential
Moderate. The trap mechanism is well-understood in market microstructure. If the trapped-participant exits create measurable pressure, this could be a standalone Alpha.

### Rare-Event Potential
LOW. Structural level failures occur frequently (~200–500/year estimated). This is not a rare-event candidate.

### Component Potential
HIGH. If validated, this could serve as a State/Condition that identifies trap states for other strategies.

### State Potential
HIGH. The "trapped participant" state is a genuine market condition that could modify the behavior of other strategies. The trap creates a specific, measurable, time-bounded market condition.

### Regime Potential
LOW. This is not a regime specialist — it is an event-driven candidate.

### Expected Failure Mode
The most likely failure is that the structural level is not precise enough to create a sharp trap. If participants place stops loosely beyond the level, the forced exit flow may be diffuse and not create measurable pressure. Additionally, the 5-bar failure window may be too tight or too loose.

### Proposed G1 Measurement
- N (number of structural level failures)
- Frequency per year
- Mean/median return of counter-breakout fade entry
- Win rate
- Counterfactual comparison (successful breakouts, random reversals)
- Conditional delta (trap vs no-trap)
- Distribution shape (median, tail, worst event)

---

## 7. Candidate 3 — CAND-082

### Candidate ID
CAND-082

### Name
Post-Expansion Retracement Quality State

### Artifact Type
State / Condition (primary) — may also serve as Alpha with sufficient displacement

### Mechanism Family
State Transition + Event Interaction — Volatility Development Quality

### Pre-Transition State
A significant volatility expansion has occurred:
- ATR has expanded from compressed (<25th percentile) to expanded (>50th percentile) over a defined window
- Price has moved directionally during the expansion
- The expansion is the "event" (similar to CAND-077's initial trigger)

### Transition
After the expansion, the market retraces part of the move:
- Price pulls back from the expansion's directional move
- The retracement is measured as a fraction of the expansion's range
- The retracement quality is assessed: how cleanly does the market retrace?

The key transition is:
> Expansion event → Retracement assessment → Entry decision based on retracement quality

### Post-Transition State
The retracement has either:
- QUALITY RETRACEMENT: Price retraces 30–60% of the expansion range in a controlled manner (low volatility during retracement, clean structure)
- POOR RETRACEMENT: Price retraces >60% or retraces with high volatility (the expansion's gains are being given back rapidly)

The hypothesis is that QUALITY RETRACEMENTS lead to better continuation outcomes than POOR RETRACEMENTS.

### Participant Constraint
After a volatility expansion:
- Participants who entered during the expansion are in profit
- Some participants take profits, creating retracement pressure
- If the retracement is quality (controlled, low-vol), it suggests healthy profit-taking without panic
- If the retracement is poor (rapid, high-vol), it suggests the expansion's gains are being rejected
- The retracement quality reflects the "health" of the post-expansion market state

### Why the Transition Matters
This is fundamentally different from CAND-077:
- CAND-077 = entry at the compression → expansion transition
- CAND-082 = entry AFTER the expansion, conditioned on retracement quality

CAND-082 asks: "After an expansion occurs, does the quality of the subsequent retracement contain information about whether continuation will succeed?"

This is a STATE concept: the retracement quality defines a market condition that could modify the behavior of other strategies.

### Economic Consequence
If quality retracements lead to better continuation:
- Entry after quality retracement should have higher win rate and larger mean return
- Entry after poor retracement should have lower win rate and smaller/negative mean return
- The retracement quality filter could improve the economics of any expansion-based Alpha

### Hypothesis
After a volatility expansion event:
- Quality retracements (30–60% retracement, low volatility during retracement) are associated with higher continuation probability
- Poor retracements (>60% retracement, high volatility during retracement) are associated with lower continuation probability
- The retracement quality state contains incremental information about the downstream outcome distribution

### Observable Variables
- ATR (20-bar, M1) for expansion detection
- Expansion range (directional move during expansion)
- Retracement depth (fraction of expansion range retraced)
- Retracement volatility (ATR during retracement vs ATR during expansion)
- Subsequent continuation (return in the original expansion direction)

### Exact Setup
1. Detect volatility expansion: ATR transitions from <25th percentile to >50th percentile (using 100-bar rolling window)
2. Record expansion direction and range
3. Wait for retracement: price pulls back from expansion's directional move
4. Measure retracement depth: fraction of expansion range retraced
5. Measure retracement quality: ATR during retracement period vs ATR during expansion period
6. Classify retracement:
   - QUALITY: 30–60% retracement + retracement ATR < 70% of expansion ATR
   - POOR: >60% retracement OR retracement ATR > 100% of expansion ATR
7. Entry: at close of retracement assessment bar, enter in the original expansion direction (for QUALITY retracements)
8. Exit: 60 minutes after entry

### Exact Confirmation
- Expansion must be detected (ATR percentile transition)
- Retracement must reach 30% of expansion range
- Retracement quality must be assessed (ATR comparison)
- Entry only for QUALITY retracements

### Exact Entry
At the close of the bar where retrachment quality is assessed as QUALITY, enter in the original expansion direction.

### Exact Exit
60 minutes (M1 bars) after entry.

### Direction
IN THE ORIGINAL EXPANSION DIRECTION (continuation trade after quality retracement).

### Rearm Rule
After exit, do not re-enter for 60 minutes. Each expansion-retracement cycle is an independent event.

### Dynamic-vs-Static Rationale
If the hypothesis could be equally expressed as "after ATR expansion, enter in the expansion direction" without the retracement quality requirement, it would fail this test. The retracement quality is essential because:
- Not all retracements are equal — quality retracements suggest healthy market structure
- Poor retracements may indicate the expansion is being rejected
- The retracement quality is a STATE that modifies the probability of continuation
- Without the quality filter, the expansion-only entry may be too noisy

### Expected Distribution Change
Quality retracements should:
- Increase the probability of continuation (higher win rate)
- Increase the mean return in the expansion direction
- Reduce the left-tail risk (fewer catastrophic failures)
- Create a more favorable risk/reward profile than unfiltered expansion entries

### Economic Headroom
If quality retracements improve win rate by 5–10% and increase mean return by 2–3 bps, this could survive friction. The retracement quality filter reduces frequency but improves selectivity.

### Counterfactual
The same expansion-direction entry applied to:
1. POOR retracements (rapid, high-vol retracement)
2. No retracement (direct continuation without pullback)
3. Deep retracement (>60%)

The counterfactual isolates the VALUE OF THE QUALITY RETRACEMENT STATE versus:
- Poor retracements (same event, different state)
- No retracement (different event entirely)
- Deep retracement (different state)

### Counterfactual Discrimination
The counterfactual is discriminating because it specifically compares quality retracements to poor retracements after the same expansion event. If continuation works equally well regardless of retracement quality, the state adds no value. If quality retracements produce materially better outcomes, the state is validated.

### Data Availability
USATECHIDXUSD M1 data. ATR computable. Retracement depth computable. Retracement volatility computable. No volume required.

### Causal Observability
- OBSERVED: Expansion event, retracement quality, and subsequent continuation
- HYPOTHESIZED: Healthy profit-taking (quality) vs panic selling (poor) creating different continuation dynamics
- UNPROVEN: Actual participant behavior during retracement

### Prior-Art
NEW. No previous QuantForge candidate tested "post-expansion retracement quality" as a State/Condition.

Historical check:
- CAND-077: compression → expansion transition (entry AT transition, not after retracement)
- CAND-078: trend exhaustion (consecutive closes, not retracement quality)
- CAND-040: volatility expansion (tested expansion itself, not retracement quality)
- CAND-054: post-shock volatility absorption (similar concept but different mechanism — shock absorption, not expansion retracement)

### Closed-Line Check
No overlap with V19–V26. No overlap with DISC-021–028. No overlap with CAND-059–CAND-079.

### Standalone Potential
LOW-MODERATE. The retracement quality filter may not produce enough displacement on its own. Primary value is as a State/Condition.

### Rare-Event Potential
LOW. Expansion events are moderate frequency. Quality retracements subset this further.

### Component Potential
VERY HIGH. This is designed as a State/Condition. If validated, the retracement quality state could:
- Filter expansion-based entries (only enter after quality retracement)
- Modify position sizing (larger size after quality retracement)
- Suppress entries after poor retracement
- Serve as a component in any future system that uses volatility expansion

### State Potential
VERY HIGH. The retracement quality is a genuine market condition:
- It is objectively measurable
- It describes the "health" of the post-expansion state
- It could modify the behavior of multiple downstream strategies
- It is a time-bounded, specific market condition

### Regime Potential
LOW. This is not a regime specialist — it is a state-conditioned event.

### Expected Failure Mode
The most likely failure is that the retracement quality distinction is not sharp enough to create measurable economic difference. The 30–60% quality range and the 70% ATR threshold may not be the right boundaries. Additionally, the expansion-retracement-continuation sequence may be too slow to capture in M1 data.

### Proposed G1 Measurement
- N (number of expansion events with quality retracements)
- N for poor retracements (comparison group)
- Frequency per year
- Mean/median continuation return for quality vs poor retracements
- Win rate for quality vs poor
- Conditional delta (quality state vs poor state)
- Distribution shape comparison

---

## 8. Dynamic Transition Comparison

| | CAND-080 | CAND-081 | CAND-082 |
|---|---|---|---|
| Pre-state | Smooth trending | Approaching structural level | Post-expansion |
| Transition | Smooth → choppy | Break → fail | Expansion → retracement |
| Post-state | Choppy regime | Trapped participants | Quality/poor retracement |
| Entry timing | At transition | After failure confirmation | After retracement assessment |
| Direction | Counter-trend | Counter-breakout | Continuation |
| Primary class | Alpha / State | Alpha / State | State / Alpha |

All three are genuinely distinct from each other and from V26 candidates.

---

## 9. Economic Mechanism Comparison

| | CAND-080 | CAND-081 | CAND-082 |
|---|---|---|---|
| Mechanism | Regime character change traps trend participants | Breakout failure traps breakout participants | Retracement quality reflects expansion health |
| Forced flow source | Stops triggered by choppy regime | Stops triggered by level failure | Profit-taking quality reflects conviction |
| Expected displacement | Moderate | Moderate-High | Low-Moderate |
| Primary value | State/Condition | Alpha/Event | State/Condition |

---

## 10. Counterfactual Quality

All three candidates use discriminating counterfactuals:

- CAND-080: Compares choppy-after-smooth to smooth continuation and already-choppy
- CAND-081: Compares failed breakouts to successful breakouts and random reversals
- CAND-082: Compares quality retracements to poor retracements after same expansion

Each counterfactual isolates the specific transition mechanism while preserving the broader market context.

---

## 11. Data Feasibility

All candidates use USATECHIDXUSD M1 data:
- ATR: computable
- Price levels: computable
- Directional inconsistency: computable
- Retracement depth: computable
- Retracement volatility: computable

No volume required. No cross-market data required. No unavailable data sources.

---

## 12. External Research Priors Used

- A (regime drift): CAND-080's smooth-to-choppy transition is a specific form of regime drift
- B (volatility development): CAND-082's retracement quality is a specific form of volatility development assessment
- C (ADX non-monotonicity): Not directly used, but the concept that extreme states may represent exhaustion informed CAND-080's regime character approach

No thresholds were imported from external research. All definitions are independent.

---

## 13. Prior-Art / Redundancy

| Candidate | Classification | Reason |
|---|---|---|
| CAND-080 | NEW | No prior candidate tested regime character transitions |
| CAND-081 | NEW | No prior candidate tested structural level break-and-fail traps |
| CAND-082 | NEW | No prior candidate tested post-expansion retracement quality as State |

No V27 candidate is an extension of any V19–V26 candidate.

---

## 14. Closed-Line Firewall

> PASS

No V27 candidate reopens any closed research line.

---

## 15. Current State Library

| Candidate | Classification |
|---|---|
| CAND-059 | STATE-ARTIFACT |
| CAND-065 | STATE OBSERVATION |
| CAND-069 | STATE OBSERVATION |
| CAND-077 | STATE REVIEW ELIGIBLE |
| CAND-079 | STATE OBSERVATION |

V27 candidates may create new State hypotheses but do not modify existing classifications.

---

## 16. Protected Forward Runtime

CAND-015:
> ACTIVE / PROTECTED / UNTOUCHED

CAND-024:
> ACTIVE / PROTECTED / UNTOUCHED

CAND-035:
> ACTIVE / PROTECTED / UNTOUCHED

---

## 17. CAND-077

> STATE REVIEW ELIGIBLE — OWNER REVIEW REQUIRED

Do not reopen or optimize. V27 candidates are independent of CAND-077.

---

## 18. G1

> NOT EXECUTED

---

## 19. System Assembly

> NOT EXECUTED

---

## 20. Next Milestone

> G1 — ECONOMIC PLAUSIBILITY SCREEN
