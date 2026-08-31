# TRADEABLE EDGE DISCOVERY SCREENING — V30

## 1. G0 Status

> **COMPLETE**

V30 G0 — Fresh mechanism discovery cycle. Three genuinely new candidates
from distinct economic mechanism families.

## 2. Research Context

V30 follows:
- V19–V29 Research Factory completion
- Cross-Research Knowledge Ledger (64 objects across QuantForge RF, APEX, SMC)
- SEED-002 relational experiment: NO INCREMENTAL INFORMATION
- Unified Research Knowledge Ledger V1
- Relational Research Governance Framework

**Current position:** 33+ candidates reconciled. 0 G2 promotions. 3 State
Review Eligible objects. Relational framework governed. SEED-002 tested
negative. Forward candidates protected.

## 3. Cross-Research Knowledge Used

The cross-research ledger served as a **knowledge map** — identifying
heavily explored families, failed pathways, validated scientific primitives,
and knowledge gaps. It was NOT used as a combination search engine.

**Key insights from the ledger:**

| Insight | Implication for V30 |
|---|---|
| Event Sequence: 12 closures (most explored family) | Avoid event-sequencing candidates |
| Structural: 10 closures | Avoid pure structural-level candidates |
| Volatility: 8 closures + 3 volatility/regime | Volatility-as-filter is exhausted |
| Market Microstructure: 8 closures | Pure microstructure is exhausted |
| Cross-Market: 8 closures | Cross-market without data is blocked |
| SEED-002: combining two States failed | Quality of a single event may matter more than quantity of pre-conditions |
| APEX: 6 scientific primitives, 0 economic modules | Scientific ≠ economic — must explain WHY economics emerge |
| SMC: BOS+OB gross +1.01 bps but M4 failed | Gross effect ≠ economic viability |
| CAND-077/081/083: conditional deltas exist but small | Standalone conditional edges are weak — need mechanism-driven economics |

**Under-explored mechanism families:**
- Time-dependent information processing
- Recovery/response quality
- Cumulative directional exhaustion
- Acceptance dynamics (distinct from rejection)
- Elasticity of market response

## 4. Lessons from SEED-002

SEED-002 tested whether CAND-083 (pre-failure rejection pressure) adds
incremental information to CAND-081 (post-failure trapped participant state).

**Result:** NO INCREMENTAL INFORMATION. Control superior by -1.78 bps.

**Lesson applied to V30:**
- Not all conceptually plausible combinations produce positive information
- The QUANTITY of pre-conditions may matter less than the QUALITY of a single event
- Mechanism-first design is essential — the economic reason must explain why
  the market should behave differently, not just that conditions "combine"
- V30 must focus on mechanisms where the economic consequence is clear and
  distinct, not on accumulating more conditions

**SEED-002 was NOT rescued, reversed, or used as a V30 seed.**

## 5. Knowledge Gaps Identified

After auditing the complete cross-research knowledge base, the following
gaps appear under-explored:

### Gap 1: Time-Dependent Information Processing

No candidate has tested how the MARKET's rate of information acceptance
varies over time after an event. Existing candidates test static thresholds
or event counts, but not the temporal dynamics of acceptance itself.

### Gap 2: Response Quality as Economic Information

SEED-002 showed that combining two State objects doesn't help. But the
QUALITY of a single event's recovery (speed, consistency, magnitude) may
itself contain economic information — independent of pre-conditions.

### Gap 3: Cumulative Directional Exhaustion

CAND-077 captures volatility character transitions. But no candidate
tests whether CUMULATIVE directional movement creates exhaustion that
has distinct economic consequences beyond what volatility captures.

### Gap 4: Acceptance vs Rejection

CAND-083 tests rejection COUNT. But acceptance DYNAMICS (how quickly price
stabilizes at a level) are a fundamentally different observable that may
carry distinct economic information.

### Gap 5: Response Elasticity

After a significant move, the market's SENSITIVITY to subsequent events
may change. This is distinct from volatility (which measures magnitude of
moves) and from trapped-participant states (which measure positioning).

## 6. Candidate 1

### Candidate ID

CAND-089

### Name

Acceptance Velocity Decay

### Artifact Type

STANDALONE ALPHA / STATE / CONDITION

### Mechanism Family

Information Processing Dynamics

### Pre-State

Price has established near or at a structural level through one or more
tests. A population of participants has formed positions relative to this
level.

### Transition

The rate at which the market accepts (stabilizes at) the current price
level begins to decline. Acceptance velocity = the speed at which
successive bars close within a narrowing range of the level. High velocity
= rapid stabilization. Low velocity = prolonged uncertainty.

### Post-State

A low-acceptance-velocity condition exists: the market is struggling to
accept the current price level despite repeated tests. This creates a
buildup of participants whose positions become vulnerable to forced exit
if the level finally breaks.

### Participant / Market Constraint

**Information processing constraint:** The market's ability to incorporate
the level's significance into participant positioning degrades when the
level is tested repeatedly without clear resolution.

**Positioning constraint:** Participants who entered at or near the level
accumulate over time. When acceptance velocity is low, more participants
are "unsure" — their conviction is low, and they will exit quickly if
the level breaks against them.

### Why Transition Matters

The DECLINE in acceptance velocity is the critical signal — not the absolute
velocity. A market that was accepting a level but begins to reject it is
in a different economic state than one that never accepted it. The
transition from acceptance to non-acceptance indicates that the collective
assessment of the level's significance is changing.

### Economic Mechanism

When acceptance velocity decays at a structural level:

1. **Participant accumulation:** More participants position at the level,
   but with declining conviction.
2. **Forced-exit potential:** If the level breaks, the accumulated
   positions create forced-exit flow that amplifies the move.
3. **Directional asymmetry:** The direction of the break is amplified by
   the velocity decay — the faster the decay, the more participants are
   trapped, the larger the forced-exit flow.
4. **Time value:** The decay process itself takes time, creating a
   window during which the market is "loading" for a directional move.

This mechanism differs from CAND-083 (rejection COUNT) because it measures
the SPEED and CONSISTENCY of acceptance, not just whether the level held.
Two levels with the same rejection count but different acceptance velocities
may produce different economic outcomes.

### Economic Consequence

- **Directional displacement:** Larger moves after level breaks when
  acceptance velocity has decayed.
- **Asymmetric tails:** The forced-exit flow creates fat tails in the
  direction of the break.
- **Persistence:** The accumulated position unwinding takes time, creating
  persistence in the post-break direction.

### Core Hypothesis

> Structural level breaks preceded by decaying acceptance velocity produce
> larger and more persistent directional moves than breaks at levels with
> stable or increasing acceptance velocity.

### Observable Variables

1. **Acceptance velocity:** Rate of change of the rolling range (high-low)
   within a window after a level test. Measured as the slope of the
   range-convergence over successive bars.
2. **Velocity decay rate:** Second derivative of acceptance velocity.
   Negative = decelerating acceptance.
3. **Level test count:** Number of times the level has been tested
   (context, not the primary variable).
4. **Structural level:** 20-bar rolling high/low (established convention).

### Observable vs Inferred vs Unknown

**Observable:**
- Acceptance velocity (from M1 OHLC)
- Velocity decay rate (from velocity time series)
- Level tests (from price-level interaction)
- Post-break return (from forward prices)

**Inferred:**
- Participant accumulation (inferred from test count and velocity)
- Forced-exit flow (inferred from post-break magnitude)
- Conviction level (inferred from velocity — lower velocity = lower conviction)

**Unknown:**
- Actual participant positioning
- Actual stop placement
- Whether forced exits dominate vs. new directional entry

### Exact Setup

For each structural level (20-bar rolling high/low):
1. Identify level tests (price touches level within tolerance)
2. After each test, measure acceptance velocity: the rate at which the
   bar range (high-low) converges toward the level over the subsequent
   K bars (K = 20, consistent with structural lookback)
3. Compute velocity decay: the change in acceptance velocity over the
   most recent L tests (L = 3)
4. Flag levels where velocity is declining (decay rate < 0)

### Exact Confirmation

The candidate confirms when:
- A structural level break occurs (close beyond level by breakout threshold)
- AND the level showed decaying acceptance velocity in the preceding tests
- AND the break direction is against the accumulated positions

### Exact Entry

Fade direction: enter opposite to the break (fade the break). This is
counter-intuitive for a "forced-exit amplification" mechanism, but the
hypothesis is that the FORCED EXIT creates a temporary overshoot that
reverses. Alternatively, enter IN the direction of the break if the
hypothesis is that forced exits amplify the move.

**Proposed direction:** WITH the break (ride the forced-exit amplification).
The economic mechanism suggests that decay → trapped participants → forced
exits → directional amplification. Therefore the trade is in the direction
of the break, not against it.

### Exact Exit

60-minute holding period (consistent with existing protocol).

### Direction

WITH the break (long if break is upward, short if break is downward).

### Rearm Rule

60-bar minimum between events (consistent with deduplication protocol).

### Dynamic-vs-Static Rationale

This candidate is inherently DYNAMIC because:
- It requires measuring a CHANGE in acceptance velocity (decay)
- The key signal is the DECLINE over time, not a static threshold
- A static velocity level would miss the critical transition from
  accepting to not-accepting
- The mechanism depends on the PROCESS of acceptance deterioration

If the decay/transition were removed, the hypothesis would reduce to
"levels with low acceptance velocity produce larger breaks" — which is a
static threshold candidate. The decay dynamic is essential.

### Expected Distribution Change

Compared to structural breaks without velocity decay:
- Higher mean return (directional amplification)
- Higher median return (broad-based, not outlier-dependent)
- Higher win rate (directional conviction in break direction)
- Wider positive tail (forced-exit amplification)
- Narrower negative tail (less counter-flow when exits dominate)

### Economic Headroom

Acceptance velocity decay affects a specific subset of structural breaks.
If the mechanism is real, the affected subset may be small (perhaps 10-20%
of all structural breaks). This limits frequency but may produce larger
per-event economics.

### Conceptual Counterfactual

Structural level breaks where acceptance velocity was STABLE or INCREASING
in the preceding tests. These represent breaks at levels where the market
was converging toward acceptance — the break is therefore a "surprise"
rather than a "loaded" move.

### Counterfactual Discrimination

The counterfactual discriminates because:
- Same structural-level event class
- Same market, timeframe, holding period
- Same cost model
- Only difference: velocity trajectory (declining vs stable/increasing)
- The economic mechanism specifically requires the DECLINE — stable
  velocity should not produce the same forced-exit amplification

### Data Availability

USATECHIDXUSD M1: ✓ (primary dataset)
XAUUSD M1: ✓ (available)
BTCUSD M1: ✓ (available)

All required variables (OHLC, timestamp) are available. No volume, no
depth, no proprietary data required.

### Causal Observability

The acceptance velocity is directly observable from M1 OHLC data. The
decay rate is computable. The structural level is deterministic. The
post-break return is observable. The causal chain (velocity decay →
participant accumulation → forced exits → directional amplification) is
plausible but not directly observable.

### Prior-Art

> **NEW**

No existing candidate tests acceptance velocity or its decay.
- CAND-083 tests rejection COUNT (static), not acceptance SPEED (dynamic)
- CAND-081 tests failure trap (event-level), not acceptance dynamics
- CAND-077 tests volatility character (regime-level), not level-specific
  acceptance
- APEX HIGH_VOL tests distributional persistence, not acceptance velocity
- SMC BOS+OB tests structural break + order block, not acceptance dynamics

### Closed-Line Check

No overlap with any closed mechanism family:
- Not Event Sequence (12 closures) — this tests information processing
- Not Structural (10 closures) — this tests velocity, not level quality
- Not Volatility (8 closures) — this tests acceptance speed, not vol
- Not Market Microstructure (8 closures) — this tests dynamics, not structure
- Not Cross-Market (8 closures) — single-market mechanism

### Standalone Potential

> **YES** — If the mechanism is real, the directional amplification from
> forced exits should be independently measurable.

### Rare-Event Potential

> **CONDITIONAL** — Depends on frequency of velocity-decay episodes.
> If rare, may qualify as rare-event Alpha.

### Component Potential

> **YES** — Could serve as a directional filter for structural-level events.

### State Potential

> **YES** — Acceptance velocity decay at a structural level could be a
> governed State condition that modifies the economics of subsequent breaks.

### Regime Potential

> **NO** — This is event-level, not regime-level.

### Expected Failure Mode

The most likely failure modes:
1. Velocity decay is too noisy to produce clean signals
2. The forced-exit amplification is small relative to costs
3. The counterfactual (stable velocity) is not economically distinct
4. The mechanism may exist but be too infrequent for standalone economics

### Proposed G1 Measurement

- Detect structural level breaks on USATECHIDXUSD M1
- Classify by acceptance velocity trajectory (decaying vs stable)
- Compute forward returns for each group
- Compare mean, median, win rate, distribution
- Apply 2 bps friction

### G0 Quality Decision

> **PASS**

- Genuinely new mechanism (information processing dynamics)
- Not a disguised prior candidate
- Not a State-library variant
- Not SEED-002 rescue
- Economically plausible (forced-exit amplification mechanism)
- Observable (M1 OHLC data)
- Has credible counterfactual
- Realistic G1 measurement
- No hindsight, no threshold mining, no protected-runtime dependency

---

## 7. Candidate 2

### Candidate ID

CAND-090

### Name

Recovery Quality Differential

### Artifact Type

STANDALONE ALPHA / STATE / CONDITION

### Mechanism Family

Response Quality Dynamics

### Pre-State

A significant directional event has occurred (structural break, large move,
session transition). The market begins to recover or retrace.

### Transition

The QUALITY of the initial recovery varies across events. Recovery quality
is defined by the speed and consistency of the retracement:
- **High quality:** Rapid, consistent retracement (bars move smoothly
  back toward origin, with minimal adverse excursion)
- **Low quality:** Slow, choppy retracement (bars fluctuate, fail to
  sustain retracement direction, adverse excursion frequent)

### Post-State

A recovery quality differential exists: some events produce high-quality
recoveries while others produce low-quality recoveries. The quality of
the recovery contains information about participant urgency and positioning
that is NOT captured by the event itself.

### Participant / Market Constraint

**Urgency constraint:** Participants who need to exit (forced exits, margin
calls, stop runs) create urgency that manifests as rapid, consistent price
movement. Participants who are merely reacting to news or opportunity create
less urgent, more choppy movement.

**Inventory constraint:** After a significant move, the market's inventory
of orders in the retracement direction determines the quality of the
recovery. High inventory = smooth recovery. Low inventory = choppy recovery.

### Why Transition Matters

The RECOVERY QUALITY is the signal — not the event itself. Two identical
events (same structural break, same magnitude) can produce different
recovery qualities depending on the participant population and inventory
state. This means recovery quality contains INCREMENTAL information beyond
the event definition.

This is particularly relevant after SEED-002: combining two State objects
(CAND-083 + CAND-081) didn't add information. But the quality of a
SINGLE event's recovery may contain information that the event definition
alone misses.

### Economic Mechanism

Recovery quality reflects participant urgency and inventory:

1. **High-quality recovery:** Participants are eager to re-enter or cover.
   The retracement is driven by genuine demand/supply imbalance.
   Implication: The retracement is likely to continue (persistence).
2. **Low-quality recovery:** Participants are hesitant. The retracement
   is weak and may fail. Implication: The original move may resume
   (reversal of retracement).

This creates a conditional economic consequence:
- High-quality recovery → continuation of retracement → fade the original
  move has positive economics
- Low-quality recovery → failure of retracement → original move resumes

### Economic Consequence

- **Directional persistence:** High-quality recoveries persist; low-quality
  recoveries fail.
- **Asymmetric tails:** High-quality recoveries have larger positive tails
  (in retracement direction); low-quality recoveries have larger negative
  tails (original move resumes).
- **Win rate:** Trading with high-quality recoveries should have higher
  win rate than trading with low-quality recoveries.

### Core Hypothesis

> Structural events followed by high-quality recoveries (rapid, consistent
> retracement) produce more favorable downstream economics in the
> retracement direction than events followed by low-quality recoveries
> (slow, choppy retracement).

### Observable Variables

1. **Recovery speed:** Number of bars from event to first meaningful
   retracement (e.g., 50% of event magnitude).
2. **Recovery consistency:** Ratio of bars moving in retracement direction
   vs total bars in the recovery window.
3. **Recovery smoothness:** Standard deviation of bar-to-bar returns during
   recovery window (lower = smoother = higher quality).
4. **Adverse excursion during recovery:** Maximum adverse move during the
   recovery window (lower = higher quality).

### Observable vs Inferred vs Unknown

**Observable:**
- Recovery speed (from M1 OHLC)
- Recovery consistency (from bar directions)
- Recovery smoothness (from return volatility)
- Adverse excursion (from OHLC)
- Event magnitude (from OHLC)
- Post-recovery return (from forward prices)

**Inferred:**
- Participant urgency (inferred from recovery speed/consistency)
- Inventory state (inferred from recovery smoothness)

**Unknown:**
- Actual order flow
- Actual participant intentions
- Whether urgency is from forced exits or voluntary re-entry

### Exact Setup

For each structural event (defined by existing protocol — breakout failure
or large move):
1. Identify the event and its magnitude
2. Measure recovery quality over the first K bars after the event (K = 30)
3. Compute:
   - Speed: bars to 50% retracement
   - Consistency: % of bars in retracement direction
   - Smoothness: std of bar-to-bar returns during recovery
   - Adverse excursion: max adverse move during recovery
4. Classify as high-quality (top tercile on composite score) or
   low-quality (bottom tercile)

### Exact Confirmation

The candidate confirms when:
- A structural event occurs
- AND the recovery quality classification is made within the recovery window
- AND the subsequent return in the retracement direction is compared between
  high-quality and low-quality groups

### Exact Entry

Enter in the retracement direction after the recovery quality classification.
The hypothesis is that high-quality recoveries produce continuation in the
retracement direction.

### Exact Exit

60-minute holding period from the point of recovery quality classification.

### Direction

WITH the retracement (long if retracement is upward, short if downward).

### Rearm Rule

60-bar minimum between events.

### Dynamic-vs-Static Rationale

This candidate is DYNAMIC because:
- Recovery quality is measured over a TIME WINDOW after the event
- The quality changes as the recovery unfolds (early vs late recovery)
- The classification depends on the TRAJECTORY, not a static threshold
- Removing the temporal dynamics would reduce it to "large events have
  different returns" — which is static and likely already captured

The transition from "event occurred" to "recovery quality assessed" is the
critical dynamic. The quality itself changes over time as the recovery
develops.

### Expected Distribution Change

Compared to low-quality recoveries:
- Higher mean return in retracement direction (continuation)
- Higher median return (broad-based)
- Higher win rate
- Narrower negative tail (less retracement failure)
- Wider positive tail (stronger continuation)

### Economic Headroom

Recovery quality should affect a meaningful fraction of structural events
(maybe 30-40% in each quality tercile). Frequency is adequate for standalone
testing.

### Conceptual Counterfactual

Structural events followed by low-quality recoveries (slow, choppy
retracement). The economic mechanism requires that recovery quality
contains information about participant urgency — events with low-quality
recoveries should show weaker continuation or reversal.

### Counterfactual Discrimination

The counterfactual discriminates because:
- Same event class
- Same market, timeframe, holding period
- Same cost model
- Only difference: quality of the initial recovery
- The mechanism specifically requires quality — if quality doesn't matter,
  both groups should perform identically

### Data Availability

USATECHIDXUSD M1: ✓ (primary dataset)
All required variables available from OHLC.

### Causal Observability

Recovery quality is directly observable from M1 OHLC data. The link between
recovery quality and participant urgency is inferred, not directly observable.

### Prior-Art

> **NEW**

No existing candidate tests recovery quality as a conditional signal.
- CAND-081 tests the trapped STATE, not the recovery QUALITY
- CAND-087 (V29) tested "recovery quality differential" but was CLOSED
  for invalid counterfactual. This candidate uses a DIFFERENT mechanism
  (response quality) with a DIFFERENT definition and DIFFERENT
  counterfactual. The V28 G1 artifact must be checked to confirm no
  overlap. If overlap exists, classify as EXTENSION and note the distinction.

**Note:** CAND-087 was classified as "Recovery Quality Differential" in V29.
However, CAND-087 was CLOSED with invalid counterfactual. This V30 candidate
uses a different mechanism (response quality as information about participant
urgency) and a different counterfactual (quality-conditional vs. event-
conditional). If repository evidence indicates this is merely a retry of
CAND-087, it should be REJECTED as an extension. The agent must verify
this during G1 by comparing the exact definitions.

### Closed-Line Check

If this is distinct from CAND-087:
- New mechanism family (Response Quality Dynamics)
- Different observable variables
- Different economic mechanism
- Different counterfactual

If this is an extension of CAND-087:
- REJECT — V30 is NEW DISCOVERY ONLY

### Standalone Potential

> **YES** — Recovery quality directly affects the economics of trading
> the retracement direction.

### Rare-Event Potential

> **NO** — Recovery quality varies across a wide range of events, not
> limited to rare occurrences.

### Component Potential

> **YES** — Could serve as a quality filter for retracement trades.

### State Potential

> **YES** — Recovery quality state could modify the economics of subsequent
> events in the retracement direction.

### Regime Potential

> **NO** — This is event-level, not regime-level.

### Expected Failure Mode

1. Recovery quality may not contain information beyond the event magnitude
2. The quality classification may be too noisy for clean separation
3. The mechanism may be real but too small to survive friction
4. CAND-087 overlap may disqualify this as NEW

### Proposed G1 Measurement

- Detect structural events on USATECHIDXUSD M1
- Measure recovery quality for each event
- Classify by quality tercile
- Compute forward returns for high vs low quality
- Apply 2 bps friction
- Compare mean, median, win rate, distribution

### G0 Quality Decision

> **PASS (CONDITIONAL)**

- Genuinely new mechanism IF distinct from CAND-087
- Economically plausible (response quality → participant urgency → economics)
- Observable (M1 OHLC data)
- Has credible counterfactual
- Realistic G1 measurement
- **CONDITION:** Must verify non-overlap with CAND-087 during G1

---

## 8. Candidate 3

### Candidate ID

CAND-091

### Name

Cumulative Directional Exhaustion

### Artifact Type

STATE / CONDITION

### Mechanism Family

Directional Exhaustion Dynamics

### Pre-State

The market has experienced sustained directional movement over a defined
period. A directional trend has established with measurable cumulative
distance.

### Transition

The cumulative directional distance (total net movement in the trend
direction over N bars) reaches a threshold where the market's ability to
continue in that direction degrades. The transition is from "trending with
conviction" to "trending with exhaustion."

### Post-State

A directional exhaustion condition exists: the market has moved far enough
in one direction that the remaining participants willing to push in that
direction are depleting. The constraint is participant INVENTORY — as the
trend progresses, fewer participants have positions to add and more
participants have positions to reduce.

### Participant / Market Constraint

**Inventory constraint:** As a directional trend progresses, the pool of
participants who can add to the trend direction depletes. Early trend
participants are already fully positioned. Late entrants are fewer and
have less conviction.

**Information constraint:** The information that drove the initial move
is increasingly "priced in" as the trend continues. Each additional bar
of trend contains less NEW information than the previous bar.

**Urgency asymmetry:** Participants entering early have high urgency
(strong conviction). Participants entering late have lower urgency (FOMO
or weak conviction). The declining urgency manifests as deteriorating
trend quality.

### Why Transition Matters

The transition from "trending" to "exhausted" is the critical signal.
A market that is merely "trending" is in a different economic state than
one that is "exhausted." The exhaustion condition implies:
1. Diminishing marginal participants in the trend direction
2. Accumulating participants in the counter-trend direction (taking profits)
3. Increased sensitivity to counter-trend catalysts
4. Potential for rapid reversal if a catalyst emerges

### Economic Mechanism

Cumulative directional exhaustion creates economic consequences through:

1. **Participant depletion:** The trend direction runs out of marginal
   buyers/sellers. Each additional unit of trend requires more price
   incentive to attract the remaining participants.
2. **Counter-trend accumulation:** As the trend progresses, profit-taking
   and counter-trend entries accumulate, creating a latent reversal force.
3. **Sensitivity amplification:** The exhausted market is more sensitive
   to new information — a small catalyst can trigger a disproportionate
   reversal because the counter-trend force is loaded.
4. **Asymmetric response:** The market responds more strongly to
   counter-trend catalysts than to trend-continuation catalysts when
   exhaustion is present.

This mechanism is distinct from CAND-077 (volatility character transition)
because it measures CUMULATIVE directional distance, not volatility regime.
A market can be volatile but not exhausted, or exhausted but not volatile.

### Economic Consequence

- **Reversal probability:** Higher probability of counter-trend movement
  when exhaustion is present.
- **Asymmetric tails:** Fat tails in the counter-trend direction.
- **Sensitivity:** Smaller catalysts produce larger moves when the market
  is exhausted.
- **Persistence of reversal:** Counter-trend moves after exhaustion may
  persist longer because they are driven by genuine participant depletion,
  not just noise.

### Core Hypothesis

> Structural events occurring during cumulative directional exhaustion
> conditions produce larger counter-trend moves (or smaller trend-continuation
> moves) than the same events occurring during non-exhausted trending
> conditions.

### Observable Variables

1. **Cumulative directional distance:** Sum of bar-to-bar returns in the
   dominant direction over a rolling window (e.g., 100 bars).
2. **Distance-to-range ratio:** Cumulative distance divided by the total
   range over the same window. Higher = more directional.
3. **Trend consistency:** Percentage of bars moving in the dominant
   direction over the window.
4. **Exhaustion threshold:** The cumulative distance at which the market's
   continuation probability begins to decline (to be estimated from data).

### Observable vs Inferred vs Unknown

**Observable:**
- Cumulative directional distance (from M1 OHLC)
- Distance-to-range ratio (from OHLC)
- Trend consistency (from bar directions)
- Post-event return (from forward prices)

**Inferred:**
- Participant inventory depletion (inferred from cumulative distance)
- Counter-trend accumulation (inferred from exhaustion condition)
- Sensitivity amplification (inferred from event response)

**Unknown:**
- Actual participant positioning
- Actual inventory levels
- Whether exhaustion is from depletion or information absorption

### Exact Setup

1. For each bar, compute cumulative directional distance over the prior
   N bars (N = 100, approximately 1.5 trading days on M1)
2. Compute distance-to-range ratio and trend consistency
3. Classify bars as "exhausted" (cumulative distance > threshold) or
   "non-exhausted" (cumulative distance ≤ threshold)
4. For each structural event, check whether it occurs during an exhausted
   or non-exhausted condition

### Exact Confirmation

The candidate confirms when:
- A structural event occurs
- AND the market is in an exhaustion condition at the time of the event
- AND the event's directional outcome is compared between exhausted and
  non-exhausted conditions

### Exact Entry

Enter COUNTER to the dominant exhaustion direction. The hypothesis is that
exhaustion creates larger counter-trend moves.

### Exact Exit

60-minute holding period.

### Direction

COUNTER to the dominant exhaustion direction.

### Rearm Rule

60-bar minimum between events.

### Dynamic-vs-Static Rationale

This candidate is DYNAMIC because:
- Exhaustion is defined by CUMULATIVE movement over time
- The transition from "trending" to "exhausted" is a time-dependent process
- The key signal is the ACCUMULATION of directional distance, not a
  static price level
- Removing the cumulative/temporal aspect would reduce it to "price has
  moved far" — which is static and likely already captured by overextension
  metrics

The dynamic nature is essential: exhaustion requires that the market has
BEEN moving (process), not that it HAS moved (state).

### Expected Distribution Change

Compared to non-exhausted conditions:
- Higher mean return in counter-trend direction
- Higher median return
- Higher win rate for counter-trend entries
- Wider positive tail in counter-trend direction
- Narrower negative tail (less trend continuation during exhaustion)

### Economic Headroom

Exhaustion conditions may occur in 10-20% of the trading period. This
limits frequency but may produce larger per-event economics because the
mechanism involves genuine participant depletion.

### Conceptual Counterfactual

Structural events occurring during NON-exhausted trending conditions
(same market, same timeframe, same event class, but the cumulative
directional distance is below the exhaustion threshold). These events
occur when the trend still has marginal participants available.

### Counterfactual Discrimination

The counterfactual discriminates because:
- Same event class
- Same market, timeframe, holding period
- Same cost model
- Only difference: exhaustion condition (cumulative distance above/below
  threshold)
- The mechanism specifically requires exhaustion — non-exhausted trends
  should not show the same counter-trend amplification

### Data Availability

USATECHIDXUSD M1: ✓ (primary dataset)
All required variables available from OHLC.

### Causal Observability

Cumulative directional distance is directly observable. The link between
distance and participant exhaustion is inferred, not directly observable.

### Prior-Art

> **NEW**

No existing candidate tests cumulative directional exhaustion as a
condition for event economics.
- CAND-077 tests volatility character, not directional exhaustion
- CAND-083 tests rejection count at levels, not cumulative distance
- CAND-084 tested compression → expansion (CLOSED — redundant with CAND-077)
- APEX HIGH_VOL tests volatility persistence, not directional exhaustion
- TSMOM research (early QuantForge) tested time-series momentum but was
  about trend-following, not exhaustion-conditioned event economics

### Closed-Line Check

- Not CAND-077 (volatility character) — different observable, different
  mechanism
- Not CAND-084 (compression → expansion) — CLOSED, and different mechanism
- Not TSMOM — different research question (trend-following vs exhaustion-
  conditioned event response)

### Standalone Potential

> **CONDITIONAL** — Depends on frequency and magnitude of exhaustion-
> conditioned events. May serve better as a State/Condition.

### Rare-Event Potential

> **NO** — Exhaustion occurs across a range of market conditions.

### Component Potential

> **YES** — Could serve as a directional filter: "do not trade with the
> trend when exhaustion is present."

### State Potential

> **YES** — Directional exhaustion is a natural State condition that
> modifies the economics of structural events.

### Regime Potential

> **CONDITIONAL** — If exhaustion persists over extended periods, it could
> be regime-like. But the primary classification is State/Condition.

### Expected Failure Mode

1. Exhaustion threshold may be too arbitrary (need data-driven calibration)
2. The mechanism may be real but too infrequent for standalone testing
3. The counter-trend response may be too small to survive friction
4. Exhaustion may overlap with CAND-077 volatility transitions

### Proposed G1 Measurement

- Compute cumulative directional distance for each bar on USATECHIDXUSD M1
- Classify structural events by exhaustion condition
- Compute forward returns for exhausted vs non-exhausted events
- Compare mean, median, win rate, distribution
- Apply 2 bps friction

### G0 Quality Decision

> **PASS**

- Genuinely new mechanism (directional exhaustion dynamics)
- Not a disguised prior candidate
- Not a State-library variant
- Not SEED-002 rescue
- Economically plausible (participant depletion → counter-trend amplification)
- Observable (M1 OHLC data)
- Has credible counterfactual
- Realistic G1 measurement
- No hindsight, no threshold mining, no protected-runtime dependency

---

## 9. Candidate Diversity Audit

| Dimension | CAND-089 | CAND-090 | CAND-091 |
|---|---|---|---|
| Mechanism Family | Information Processing Dynamics | Response Quality Dynamics | Directional Exhaustion Dynamics |
| Core Observable | Acceptance velocity decay | Recovery speed/consistency | Cumulative directional distance |
| Temporal Level | Event-level (post-test dynamics) | Event-level (post-event recovery) | State-level (cumulative over time) |
| Direction | WITH break (forced-exit amplification) | WITH retracement (continuation) | COUNTER to exhaustion direction |
| Primary Constraint | Information processing | Urgency/inventory | Participant depletion |
| State/Alpha Role | Both | Both | Primarily State |
| Overlap with Prior | None identified | CAND-087 check required | None identified |

**Assessment:** The three candidates come from genuinely different mechanism
families with different observables, different economic mechanisms, and
different directions. CAND-090 requires a CAND-087 overlap check during G1.

## 10. Economic Mechanism Comparison

| Candidate | Mechanism | Why Economics Should Change |
|---|---|---|
| CAND-089 | Acceptance velocity decay | Slow acceptance → trapped participants → forced exits → directional amplification |
| CAND-090 | Recovery quality differential | High-quality recovery → participant urgency → retracement continuation |
| CAND-091 | Cumulative directional exhaustion | Exhaustion → participant depletion → counter-trend amplification |

Each mechanism explains a DIFFERENT economic pathway. No two candidates
share the same causal chain.

## 11. Counterfactual Quality

| Candidate | Counterfactual | Quality |
|---|---|---|
| CAND-089 | Stable/increasing acceptance velocity | Strong — same event class, different velocity trajectory |
| CAND-090 | Low-quality recovery | Strong — same event class, different recovery quality |
| CAND-091 | Non-exhausted trending | Strong — same event class, different cumulative distance |

All three counterfactuals are well-defined and discriminating.

## 12. Cross-Research Redundancy Audit

| Candidate | Potential Overlap | Assessment |
|---|---|---|
| CAND-089 | CAND-083 (rejection count) | DISTINCT — velocity vs count, dynamic vs static |
| CAND-089 | APEX HIGH_VOL persistence | DISTINCT — level-specific vs regime-level |
| CAND-090 | CAND-081 (trapped state) | DISTINCT — recovery quality vs trapped state |
| CAND-090 | CAND-087 (recovery quality) | **REQUIRES G1 CHECK** — may be extension |
| CAND-091 | CAND-077 (vol volatility) | DISTINCT — directional exhaustion vs vol character |
| CAND-091 | TSMOM (early QuantForge) | DISTINCT — exhaustion-conditioned events vs trend-following |

## 13. State Firewall

CAND-077, CAND-081, CAND-083: **NOT MODIFIED, NOT OPTIMIZED, NOT COMBINED**

None of the V30 candidates use State objects as inputs. Each candidate
derives its mechanism independently from market observables.

## 14. Exploratory Observation Firewall

CAND-077 >15 bps: **NOT IMPORTED**
CAND-088 aligned-break: **NOT IMPORTED**

Neither exploratory observation was used as a V30 premise.

## 15. Closed-Line Firewall

> **PASS**

No V19–V29 closed hypothesis was reopened or used as a positive input.
Closed knowledge was used only to identify what NOT to search for.

## 16. External Research Priors

Custom-bot observations: **NOT IMPORTED**

No external thresholds, strategy rules, or proprietary observations were
used in V30 candidate design.

## 17. Data Feasibility

All three candidates use only:
- M1 OHLC data (available for USATECHIDXUSD, XAUUSD, BTCUSD)
- Timestamp (for session/time-of-day context)
- Computed variables (velocity, recovery quality, cumulative distance)

No volume, no depth, no proprietary data required.

## 18. Protected Forward Runtime

CAND-015/024/035:

> **ACTIVE / PROTECTED / UNTOUCHED**

No forward performance was inspected. No V30 candidate depends on forward
results.

## 19. G1

> **NOT EXECUTED**

## 20. G2

> **NOT EXECUTED**

## 21. System Assembly

> **NOT EXECUTED**

## 22. Next Milestone

> **G1 — ECONOMIC PLAUSIBILITY SCREEN**

V30 G1 will:
1. Verify CAND-090 is distinct from CAND-087
2. Execute frozen definitions for each candidate
3. Measure economic plausibility
4. Classify each candidate for further governance
