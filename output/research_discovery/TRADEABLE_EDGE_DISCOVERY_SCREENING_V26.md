# TRADEABLE EDGE DISCOVERY SCREENING — V26
# DYNAMIC MARKET-STATE / ECONOMIC DISPLACEMENT DISCOVERY
# DATE: 2026-08-29
# STATUS: G0 COMPLETE — 3 CANDIDATES

---

## 1. G0 Status

V26 G0 COMPLETE. Three candidates generated, each testing a dynamic state-transition mechanism rather than a static condition. Zero G1 execution.

---

## 2. V25 Closure Context

V25 produced 3/3 economically negative candidates (CAND-074, CAND-075, CAND-076). The settlement/benchmark and cross-market-direction families both failed. The critical V25 lesson:

> Even theoretically compelling participant-constraint mechanisms did not produce measurable directional displacement in the M1 representation.

This means V26 must NOT generate more static-condition or participant-constraint candidates. Instead, V26 explores whether the **transition between states** — not the states themselves — creates economic consequence.

---

## 3. G1 V3 Framework Applied

V26 candidates will be evaluated under the ratified G1 V3 two-layer architecture:

- **Layer 1:** Hard validity gates (9 binary checks)
- **Layer 2:** Economic evidence adjudication (holistic, no threshold gates)

This is G0 only — no G1 execution occurs.

---

## 4. External Statistical Research Priors

> PROVISIONAL EXTERNAL RESEARCH INPUT — NOT VALIDATED QUANTFORGE EVIDENCE

A custom-bot statistical analysis (Aug 7–29, 2026) provided observations that inspired V26 hypotheses. Key priors used:

1. **Volatility development vs exhaustion:** ATR Factor 1.0–1.5 appeared favorable; >2.0–2.5 appeared poor. Research concept: the transition from compressed to expanding vol may matter more than the static vol level.

2. **ADX non-monotonicity:** Extreme ADX percentile appeared associated with exhaustion, not trend strength. Research concept: the rate-of-change of trend indicators may predict transitions.

3. **Execution-quality state:** Volume spikes, spread widening, and ATR spikes appeared to degrade execution. Research concept: liquidity transitions may alter event economics.

These are starting points for hypothesis generation. They are NOT validated QuantForge evidence and their thresholds are NOT imported.

---

## 5. Candidate 077 — Volatility Compression-to-Expansion Transition Event

### Candidate ID
CAND-077

### Name
Volatility Compression-to-Expansion Transition Event

### Artifact Type
STANDALONE ALPHA (provisional)

### Mechanism Family
Dynamic State Transition — Volatility Development (Family A)

### Initial State
Compressed volatility: ATR (14-bar) percentile over the trailing 200 bars is below the 25th percentile. This represents a market in a narrow range where participants have reduced position sizes and the market is "coiled."

### Transition
First 1-bar close that breaks above the 14-bar ATR high of the compressed period. The transition bar must have volume above the 20-bar average volume, confirming genuine expansion rather than noise.

### Post-Transition State
Expanding volatility: ATR is now above its 50th percentile. Participants are increasing position sizes. The market is moving from equilibrium to disequilibrium.

### Participant Constraint
During compression, participants reduce position sizes and tighten stops. When the compression breaks, these tight stops are triggered in sequence, creating a cascade of forced exits that amplifies the breakout direction. The transition from low-urgency to high-urgency participation is the economic mechanism.

### Why the Transition Matters
The same breakout magnitude in an already-expanded market is less likely to produce follow-through because participants are already positioned for volatility. The COMPRESSION-TO-EXPANSION transition captures the moment when participants are least prepared for the move and most likely to be forced to react.

### Economic Consequence
When volatility expands from a compressed state:
1. Tight stops are triggered, creating cascading directional pressure;
2. Position builders enter, adding to the directional flow;
3. The transition attracts momentum-following capital;
4. The displacement should exceed the displacement of the same move in an already-expanded market.

### Hypothesis
USATECHIDXUSD breakouts that occur during the transition from compressed volatility to expanding volatility produce larger directional displacement in the breakout direction than breakouts that occur during already-expanded volatility, measured over a 30-minute post-breakout window.

### Observable Variables
- 14-bar ATR percentile (trailing 200 bars)
- 20-bar average volume
- Breakout bar volume
- 30-minute post-breakout return

### Exact Setup
1. Compute 14-bar ATR on USATECHIDXUSD M1 bars
2. Compute ATR percentile over trailing 200 bars
3. Identify "compressed" periods: ATR percentile < 25th percentile for at least 20 consecutive bars
4. Identify "expansion trigger": first bar where close > high of the compressed period AND volume > 20-bar average volume

### Exact Confirmation
The expansion trigger bar must satisfy:
- Close above the highest close of the preceding compressed period
- Volume above 20-bar average
- ATR percentile was below 25th percentile within the last 5 bars

### Exact Entry
At the close of the expansion trigger bar (end of the bar that confirms the transition).

### Exact Exit
30 minutes (30 bars) after entry.

### Direction
Long (in the direction of the breakout).

### Rearm Rule
One event per compression period. Maximum one event per day.

### Expected Distribution Change
The transition from compressed to expanded volatility should produce:
- Larger mean displacement in the breakout direction;
- Higher win rate than breakouts in already-expanded markets;
- More persistent directional movement (less immediate mean-reversion).

### Economic Headroom
If the compression-to-expansion transition produces 5+ bps of additional displacement compared to already-expanded breakouts, this exceeds 2 bps friction. The mechanism is structural: tight stops cascade during transitions, creating forced directional flow that does not exist in already-expanded conditions.

### Counterfactual
Breakouts (close above recent high with volume > average) that occur when ATR percentile is already above 50th percentile (already-expanded state, NOT transitioning). The counterfactual isolates whether the compression-to-expansion transition itself adds displacement beyond the breakout signal alone.

### Why Counterfactual Is Discriminating
The counterfactual uses the SAME breakout signal (close above high + volume) but in a DIFFERENT volatility state (already-expanded vs transitioning). This isolates the transition effect from the breakout effect.

### Data Availability
USATECHIDXUSD M1 data is available. ATR, volume, and price are all computable from the dataset. No hidden data required.

### Causal Observability
The volatility state transition is directly observable. The breakout trigger is observable. The participant cascade mechanism (tight stops triggering) is hypothesized but the price consequence is directly measurable.

### Prior-Art
NEW. No previous QuantForge candidate tested volatility compression-to-expansion transitions as a directional mechanism. CAND-063 tested "volatility compression" as a static condition (not a transition). CAND-066 tested "volatility expansion" as a static condition. This candidate tests the TRANSITION between states.

### Closed-Line Check
No overlap with V19–V25. No overlap with DISC-021–026. No overlap with CAND-006–CAND-076.

### Standalone Potential
MODERATE. If the transition produces consistent directional displacement, this could operate as an independent daily strategy.

### Rare-Event Potential
MODERATE. Compression periods occur periodically (perhaps 20–40 times/year), making this a moderate-frequency candidate.

### Component Potential
MODERATE. The volatility-transition signal could serve as a filter for other Alpha candidates (e.g., "only enter during transition states").

### State Potential
HIGH. The volatility-transition state itself could be valuable as a regime filter for multiple downstream Alphas.

### Regime Potential
MODERATE. The candidate is inherently regime-dependent (only fires during transitions).

### Information-Sharing Potential
The volatility-transition state could inform any Alpha that benefits from trending/expanding conditions.

### Expected Failure Mode
The breakout may not produce follow-through even during transitions. The compression definition may be too narrow (rare events) or too broad (noisy events). The volume confirmation may filter out genuine transitions.

### Proposed G1 Measurement
Measure USATECHIDXUSD return from expansion-trigger close to 30-minute exit. Compare to counterfactual (same breakout in already-expanded state). Report: N, mean net, median net, win rate, counterfactual delta, payoff distribution.

---

## 6. Candidate 078 — Trend Exhaustion Transition → Mean-Reversion Event

### Candidate ID
CAND-078

### Name
Trend Exhaustion Transition → Mean-Reversion Event

### Artifact Type
STANDALONE ALPHA (provisional)

### Mechanism Family
Dynamic State Transition — Trend Development/Exhaustion (Family B)

### Initial State
Developing trend: 8+ consecutive same-direction closes on USATECHIDXUSD M1 bars. This represents genuine directional momentum where participants are positioned and adding.

### Transition
First bar that closes in the OPPOSITE direction after 8+ consecutive same-direction closes. The reversal bar must have volume above the 20-bar average, confirming genuine participant activity rather than noise.

### Post-Transition State
Trend exhaustion: the trend has lost momentum. Participants who were positioned during the trend are now reducing exposure. The market transitions from trending to mean-reverting.

### Participant Constraint
During the trend, participants accumulate positions in the trend direction. As the trend extends, latecomers enter at progressively worse prices. When the trend finally reverses, these late participants are trapped. Their forced exits (stop-losses, margin calls, risk-model reductions) create directional pressure in the reversal direction. The transition from trending to exhausted state triggers a cascade of forced position reduction.

### Why the Transition Matters
A single counter-trend bar in the middle of a strong trend is noise — the trend resumes. But a counter-trend bar after 8+ consecutive same-direction bars represents genuine exhaustion. The economic consequence is different because the participant positioning is different: in the middle of a trend, counter-trend flow is small; at exhaustion, counter-trend flow is amplified by trapped participants.

### Economic Consequence
When a trend exhausts:
1. Late-entering trend participants are trapped and must exit;
2. Their exits create directional pressure in the reversal direction;
3. The reversal attracts counter-trend capital;
4. The displacement should exceed the displacement of a random counter-trend bar.

### Hypothesis
USATECHIDXUSD M1 bars that close in the opposite direction after 8+ consecutive same-direction closes produce larger mean-reversion displacement in the reversal direction than random counter-trend bars, measured over a 15-minute post-reversal window.

### Observable Variables
- Consecutive same-direction close count
- Reversal bar volume
- 15-minute post-reversal return

### Exact Setup
1. Count consecutive same-direction closes on USATECHIDXUSD M1 bars
2. Identify "trend exhaustion trigger": first bar that closes in the opposite direction after 8+ consecutive same-direction closes
3. Confirm: reversal bar volume > 20-bar average volume

### Exact Confirmation
The reversal bar must:
- Close in the opposite direction of the preceding 8+ consecutive same-direction closes
- Have volume above 20-bar average
- Follow at least 8 consecutive same-direction closes

### Exact Entry
At the close of the exhaustion trigger bar (end of the bar that confirms the reversal).

### Exact Exit
15 minutes (15 bars) after entry.

### Direction
Against the preceding trend (mean-reversion).

### Rearm Rule
One event per trend exhaustion. Maximum one event per day.

### Expected Distribution Change
The exhaustion transition should produce:
- Larger mean-reversion displacement than random counter-trend bars;
- Higher win rate for the mean-reversion trade;
- More persistent counter-trend movement (less immediate trend resumption).

### Economic Headroom
If exhaustion-driven mean-reversion produces 5+ bps of additional displacement compared to random counter-trend bars, this exceeds 2 bps friction. The mechanism is structural: trapped participants create forced exit pressure that does not exist during random counter-trend bars.

### Counterfactual
Counter-trend bars (close in opposite direction) that occur after 2–4 consecutive same-direction closes (early trend, NOT exhausted). The counterfactual isolates whether the exhaustion transition itself adds mean-reversion displacement beyond the basic counter-trend signal.

### Why Counterfactual Is Discriminating
The counterfactual uses the SAME counter-trend signal (close in opposite direction + volume) but in a DIFFERENT trend state (early trend vs exhausted). This isolates the exhaustion effect from the basic counter-trend effect.

### Data Availability
USATECHIDXUSD M1 data is available. Consecutive close count and volume are computable. No hidden data required.

### Causal Observability
The consecutive close count is directly observable. The reversal bar is observable. The participant-exit cascade mechanism is hypothesized but the price consequence is directly measurable.

### Prior-Art
NEW. No previous QuantForge candidate tested trend exhaustion as a directional mechanism. CAND-070 tested "Sustained Momentum Micro-Structure Failure" but used a different mechanism (fading the first structure break in an overheated trend, which was FALSIFIED). CAND-078 tests a different hypothesis: exhaustion after extended consecutive closes, not structure-break fading.

### Closed-Line Check
No overlap with V19–V25. No overlap with DISC-021–026. CAND-070 (falsified) tested a different mechanism (MSS fading). This candidate tests exhaustion-driven mean-reversion.

### Standalone Potential
MODERATE. If exhaustion transitions produce consistent mean-reversion, this could operate independently.

### Rare-Event Potential
LOW-MODERATE. Extended trends (8+ consecutive closes) occur periodically (perhaps 30–60 times/year).

### Component Potential
MODERATE. The exhaustion signal could serve as a filter for other mean-reversion Alphas.

### State Potential
MODERATE. The exhaustion state could inform downstream Alpha qualification.

### Regime Potential
MODERATE. The candidate is inherently regime-dependent (only fires at trend exhaustion).

### Information-Sharing Potential
Could inform any mean-reversion module about when trend exhaustion is occurring.

### Expected Failure Mode
The 8-consecutive threshold may be too high (rare) or too low (noisy). The reversal may not produce follow-through if the trend resumes immediately. The volume confirmation may filter out genuine exhaustion events.

### Proposed G1 Measurement
Measure USATECHIDXUSD return from exhaustion-trigger close to 15-minute exit (reversal direction). Compare to counterfactual (same counter-trend signal after 2–4 consecutive closes). Report: N, mean net, median net, win rate, counterfactual delta, payoff distribution.

---

## 7. Candidate 079 — Cross-Market Volatility Regime Transition → Information Transmission

### Candidate ID
CAND-079

### Name
Cross-Market Volatility Regime Transition → Information Transmission

### Artifact Type
ALPHA / EVENT (provisional)

### Mechanism Family
Cross-Market State Transition (Family E)

### Initial State
Low gold volatility: XAUUSD 14-bar ATR percentile (trailing 200 bars) is below 25th percentile. Gold is in a compressed, low-urgency state.

### Transition
Gold volatility transitions from compressed to expanded: ATR percentile crosses above 50th percentile within 30 minutes of being below 25th percentile. This is a rapid volatility expansion in Gold.

### Post-Transition State
Gold is in an expanded-volatility state. This reflects a fundamental repricing event in Gold — potentially driven by geopolitical news, central bank action, or risk-sentiment shift.

### Participant Constraint
When Gold reprices rapidly (volatility expansion from compressed state), it reflects information that affects global risk sentiment. US Tech participants must incorporate this information. The structural constraint is:
- Gold has already repriced (volatility expanded);
- US Tech participants observe the Gold repricing;
- They must adjust their positions accordingly;
- This adjustment creates directional pressure in US Tech.

### Why the Transition Matters
A static "Gold is volatile" condition does not predict Tech direction. But a RAPID TRANSITION from compressed to expanded Gold volatility represents a genuine information arrival. The transition captures the moment when new information enters the market and must be incorporated by participants in correlated assets.

### Economic Consequence
When Gold volatility transitions rapidly from compressed to expanded:
1. Gold has experienced a genuine repricing event;
2. Risk sentiment has shifted;
3. US Tech participants must incorporate this shift;
4. The incorporation creates directional pressure in Tech proportional to the Gold repricing magnitude;
5. The displacement should exceed normal intraday noise.

### Hypothesis
When XAUUSD 14-bar ATR percentile transitions from below 25th to above 50th percentile within 30 minutes, USATECHIDXUSD produces a directional response in the SAME direction as the Gold move over the subsequent 30 minutes. The magnitude of the Tech response is proportional to the Gold repricing magnitude.

### Observable Variables
- XAUUSD 14-bar ATR percentile (trailing 200 bars)
- XAUUSD directional move during the volatility transition
- USATECHIDXUSD 30-minute return after Gold transition

### Exact Setup
1. Compute XAUUSD 14-bar ATR, percentile over trailing 200 bars
2. Identify "Gold volatility transition": ATR percentile crosses from <25th to >50th within 30 minutes
3. Measure Gold directional move during the transition (direction + magnitude)
4. Measure USATECHIDXUSD return from 30 minutes after Gold transition trigger to 60 minutes after

### Exact Confirmation
The Gold volatility transition must:
- ATR percentile was below 25th within the last 30 bars
- ATR percentile is now above 50th
- The transition occurred within 30 minutes
- Gold moved at least 10 bps during the transition period

### Exact Entry
30 minutes after the Gold volatility transition trigger (allowing time for information to reach US Tech participants).

### Exact Exit
60 minutes after the Gold volatility transition trigger (30-minute holding period).

### Direction
Same direction as the Gold move during the volatility transition.

### Rearm Rule
One event per Gold volatility transition. Maximum one event per day.

### Expected Distribution Change
The cross-market volatility transition should produce:
- Larger directional displacement in Tech than during normal Gold-volatile periods;
- Higher correlation between Gold direction and Tech direction during transition;
- More persistent Tech displacement (information incorporation takes time).

### Economic Headroom
If Gold volatility transitions produce 5+ bps of directional displacement in Tech, this exceeds 2 bps friction. The mechanism is structural: genuine information arrival in Gold creates forced repricing in correlated assets.

### Counterfactual
USATECHIDXUSD return during 30-minute windows when Gold volatility is already expanded (ATR percentile >50th for 30+ minutes, NOT transitioning). The counterfactual isolates whether the volatility TRANSITION itself adds directional value beyond the static expanded-volatility state.

### Why Counterfactual Is Discriminating
The counterfactual uses the SAME Tech time window but in a DIFFERENT Gold volatility state (already-expanded vs transitioning). This isolates the transition effect from the static volatility effect.

### Data Availability
Both XAUUSD and USATECHIDXUSD M1 data are available. ATR, percentile, and price are computable. No hidden data required.

### Causal Observability
The Gold volatility transition is directly observable. The Gold directional move is observable. The Tech response is directly measurable. The information-transmission mechanism is hypothesized but the price consequence is directly measurable.

### Prior-Art
CAND-071 tested Gold→Tech direction (static direction). CAND-076 tested Gold overnight→Tech open (static direction). CAND-079 tests a DIFFERENT mechanism: Gold volatility REGIME TRANSITION → Tech directional response. The hypothesis is not "Gold direction predicts Tech direction" but rather "a rapid change in Gold's volatility regime creates information that Tech participants must incorporate."

### Closed-Line Check
CAND-079 is an EXTENSION of the Gold→Tech line but tests a materially different mechanism:
- CAND-071: Gold static direction → Tech direction
- CAND-076: Gold overnight direction → Tech direction
- CAND-079: Gold volatility regime transition → Tech directional response

The key distinction: CAND-079 requires a VOLATILITY REGIME CHANGE in Gold, not just a price direction. This is a state-transition hypothesis, not a static-direction hypothesis.

### Standalone Potential
MODERATE. If Gold volatility transitions produce consistent directional displacement in Tech, this could operate independently.

### Rare-Event Potential
MODERATE-HIGH. Rapid Gold volatility transitions from compressed to expanded occur perhaps 30–60 times/year, making this a moderate-frequency candidate.

### Component Potential
HIGH. The Gold volatility-transition signal could serve as a cross-market risk filter for any US Tech Alpha.

### State Potential
HIGH. The Gold volatility-transition state could be valuable as a regime indicator for multiple downstream Alphas.

### Regime Potential
MODERATE. The candidate is inherently regime-dependent (only fires during Gold volatility transitions).

### Information-Sharing Potential
Could inform any US Tech module about regime changes originating in Gold markets.

### Expected Failure Mode
Gold volatility transitions may not predict Tech direction. The 30-minute delay may be too long (information already incorporated) or too short (information not yet incorporated). The mechanism may have been arbitraged away.

### Proposed G1 Measurement
Measure USATECHIDXUSD return from 30-min post-transition to 60-min post-transition, conditioned on Gold direction during transition. Compare to counterfactual (same Tech window during already-expanded Gold volatility). Report: N, mean net, median net, win rate, counterfactual delta, payoff distribution.

---

## 8. Dynamic-vs-Static Rationale

### CAND-077
The compression-to-expansion transition matters because:
- A breakout in an already-expanded market is noise;
- A breakout after prolonged compression is a genuine state change;
- The participant dynamics are different: in compression, stops are tight and positions are small; at transition, stops cascade and positions expand;
- A static "low ATR" condition would not capture the transition dynamics.

### CAND-078
The trend-exhaustion transition matters because:
- A counter-trend bar in the middle of a trend is noise;
- A counter-trend bar after 8+ consecutive same-direction closes represents genuine exhaustion;
- The participant dynamics are different: early in a trend, counter-trend flow is small; at exhaustion, trapped participants create forced exit pressure;
- A static "high ADX" condition would not capture the exhaustion dynamics.

### CAND-079
The Gold volatility regime transition matters because:
- Static "Gold is volatile" does not predict Tech direction;
- A rapid transition from compressed to expanded Gold volatility represents genuine information arrival;
- The participant dynamics are different: during normal Gold volatility, Tech participants are indifferent; during a Gold volatility transition, they must adjust positions;
- A static "Gold direction" condition would not capture the regime-transition dynamics.

---

## 9. Economic Displacement Comparison

| Candidate | Transition | Expected Mechanism | Structural vs Statistical |
|---|---|---|---|
| CAND-077 | Compressed → Expanded vol | Stop cascade + position building | Structural (forced exits) |
| CAND-078 | Trending → Exhausted | Trapped participant exits | Structural (forced exits) |
| CAND-079 | Gold low vol → High vol | Cross-market information arrival | Structural (information incorporation) |

All three candidates identify state transitions where participant dynamics change materially. None rely on static conditions.

---

## 10. Mechanism Diversity

| Candidate | Mechanism Family | Distinct Mechanism |
|---|---|---|
| CAND-077 | Volatility Development | Compression-to-expansion transition |
| CAND-078 | Trend Exhaustion | Consecutive-close exhaustion transition |
| CAND-079 | Cross-Market State Transition | Gold volatility regime transition |

All three candidates come from different mechanism families. All three test dynamic transitions rather than static conditions. No candidate is a cosmetic variant of another.

---

## 11. External Research Priors Used

| Prior | How Used | Threshold Imported? |
|---|---|---|
| Volatility development > exhaustion | CAND-077 uses compression-to-expansion transition | NO — ATR percentile defined independently |
| ADX non-monotonicity | CAND-078 uses exhaustion after consecutive closes, not ADX | NO — consecutive close count defined independently |
| Execution-quality state | CAND-077 uses volume confirmation | NO — volume > 20-bar average is a simple filter, not an import |

No external thresholds were imported. The external analysis provided research concepts only.

---

## 12. Prior-Art / Redundancy

| Candidate | Classification | Notes |
|---|---|---|
| CAND-077 | NEW | No previous candidate tested compression-to-expansion transitions |
| CAND-078 | NEW | No previous candidate tested consecutive-close exhaustion |
| CAND-079 | EXTENSION | Gold→Tech line: CAND-071 (direction), CAND-076 (overnight direction), CAND-079 (volatility regime transition) — materially different mechanism |

---

## 13. Closed-Line Firewall

No V26 candidate reopens or rescues any closed research line. CAND-079 is classified as an EXTENSION of the Gold→Tech line but tests a materially different mechanism (volatility regime transition vs static direction).

---

## 14. Protected Forward Runtime

### CAND-015
> ACTIVE / PROTECTED / UNTOUCHED

### CAND-024
> ACTIVE / PROTECTED / UNTOUCHED

### CAND-035
> ACTIVE / PROTECTED / UNTOUCHED

Do not modify, inspect, or adjudicate forward results.

---

## 15. G1

> NOT EXECUTED

---

## 16. System Assembly

> NOT EXECUTED

---

## 17. Next Milestone

> G1 — ECONOMIC PLAUSIBILITY SCREEN (V26)
