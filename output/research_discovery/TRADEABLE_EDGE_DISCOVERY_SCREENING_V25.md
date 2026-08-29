# TRADEABLE EDGE DISCOVERY SCREENING — V25
# ECONOMIC DISPLACEMENT MECHANISM DISCOVERY
# DATE: 2026-08-29
# STATUS: G0 COMPLETE — 3 CANDIDATES

---

## 1. G0 Status

V25 G0 COMPLETE. Three candidates generated, each from a distinct economic displacement mechanism family. Zero G1 execution.

---

## 2. Research Objective

V25 deliberately shifts the center of gravity away from small structural asymmetries, marginal timing differences, and generic reversals/sweeps/breakouts that dominated V19–V24. Instead, V25 searches for:

> MARKET CONSTRAINT → PARTICIPANT PRESSURE → OBSERVABLE STATE TRANSITION → ASYMMETRIC PRICE RESPONSE → EXECUTABLE EVENT

The core question for every candidate is:

> Why would market participants be forced, encouraged, or constrained to transact here and now?

---

## 3. V19–V24 Lessons Incorporated

The V19–V24 meta-review identified a dominant pattern: conditionally informative price structures that failed to produce sufficient economic displacement. V25 lessons applied:

1. **Price patterns ≠ economic mechanisms.** "Price tends to reverse here" is not a sufficient hypothesis. "A defined participant constraint becomes active at this time" is preferred.
2. **Conditional information ≠ monetizable alpha.** Treatment beating counterfactual by <1 bps is informative but economically unviable at retail friction.
3. **SMC-inspired hypotheses consistently fail.** Sweep/freshness/acceptance/MSS/IB/PDH mechanisms produced 0 G2 promotions across 6 cycles. V25 avoids these families.
4. **Mechanism diversity matters.** V19–V24 explored variations of the same 3–4 mechanism families. V25 uses entirely new families.
5. **Rare events are legitimate.** Low frequency with large per-event economics is a valid path.
6. **Economic displacement must exceed friction structurally, not marginally.** A mechanism that produces +1 bps expected move cannot survive 2 bps friction regardless of frequency.

---

## 4. Candidate 071–073 Closure Context

V24 candidates (CAND-071: Gold→Tech, CAND-072: Friday Compression, CAND-073: Lunch Reversal) all showed treatment superiority (real informational value) but negative absolute economics. V25 explicitly avoids:
- generic cross-market correlation without forcing mechanism (CAND-071 lesson);
- calendar-based structural patterns without participant constraint (CAND-072 lesson);
- session-based microstructure without participant pressure (CAND-073 lesson).

---

## 5. Candidate 074 — London Gold Fix Benchmark Execution Pressure

### Candidate ID
CAND-074

### Name
London Gold Fix Benchmark Execution Pressure

### Artifact Type
STANDALONE ALPHA / RARE-EVENT ALPHA (provisional)

### Mechanism Family
Settlement / Benchmark / Mandatory Flow (Family 1)

### Participant Constraint
The London Gold Fix (10:30 AM and 3:00 PM London time) is a benchmark price determination process where participants — central banks, gold miners, refiners, fabricators, and institutional investors — must transact at the determined fix price. These participants cannot choose their execution time; they are contractually or operationally obligated to transact at the fix.

### Why Now?
The fix creates a 10–20 minute window of concentrated, price-insensitive order flow. Participants submitting sell orders to the fix panel create temporary selling pressure that can move the fix price below the prevailing market. Participants submitting buy orders create the opposite. The fix window is a known, deterministic time when concentrated, non-discretionary order flow must be absorbed by the market.

### Hypothesis
When XAUUSD exhibits directional movement into the London AM Fix (10:30 AM London time), the fix window itself amplifies that direction because:
1. The directional move attracts offsetting fix orders (selling into strength, buying into weakness);
2. The fix determination process concentrates these orders into a narrow time window;
3. The fix price then becomes a reference for subsequent settlement, creating a second wave of activity.

### Observable Variables
- XAUUSD price direction in the 30 minutes before 10:30 AM London time;
- XAUUSD price during the fix window (10:30–10:50 AM London time);
- XAUUSD price in the 30 minutes after the fix window;
- Magnitude of pre-fix directional move.

### Exact Setup
Define "pre-fix directional move" as the XAUUSD price change from 10:00 AM to 10:30 AM London time.

### Exact Confirmation
The pre-fix move must exceed a defined magnitude threshold in either direction.

### Exact Entry
At 10:30 AM London time, enter XAUUSD in the direction of the pre-fix move.

### Exact Exit
At 11:00 AM London time (30 minutes after entry).

### Direction
Same direction as the pre-fix move (momentum into the fix window).

### Rearm Rule
One event per fix window. Maximum one event per day.

### Economic Displacement Logic
The fix participants are price-insensitive in the short term — they must transact at the fix regardless of small price changes. This creates temporary supply/demand imbalance concentrated in a 10–20 minute window. The pre-fix directional move indicates which side (buyers or sellers) has more pressure. The fix amplifies this because:
1. Sellers submitting to the fix sell into a market that is already moving down (if pre-fix is negative);
2. Buyers submitting to the fix buy into a market that is already moving up (if pre-fix is positive);
3. The fix price becomes a settlement reference, creating follow-on activity.

### Expected Asymmetry
The fix participants cannot delay or avoid their transaction. This is not discretionary flow — it is contractual/operational obligation. The concentration of non-discretionary flow should produce larger-than-normal price movement during the fix window.

### Economic Headroom
Gold trades ~$3,300/oz. A 10 bps move = ~$3.30. If the fix window produces even 5–10 bps of additional directional movement beyond the pre-fix move, this exceeds 2 bps friction. The mechanism is structural, not statistical.

### Counterfactual
Same time of day (10:00–10:30 AM direction, 10:30–11:00 AM outcome) on days WITHOUT a fix meeting, OR the same pre-fix move magnitude occurring at a random non-fix time. The counterfactual isolates whether the fix window itself adds directional value beyond the pre-existing momentum.

### Data Availability
XAUUSD M1 data is available in the repository. London fix time is deterministic and publicly known. No hidden data required.

### Causal Observability
The fix timing is observable. The price movement into and out of the fix is observable. The fix participant motivations are hypothesized (contractual obligation) but not directly observed. The price consequence is directly measurable.

### Prior-Art
NEW. No previous QuantForge candidate tested the London Gold Fix as an execution mechanism. CAND-035 tested month-end gold imbalance (different mechanism — end-of-month vs daily fix). CAND-033 tested WMR pre-fixing flow (different mechanism — WMR fix, not LBMA fix, and different hypothesis).

### Closed-Line Check
No overlap with V19–V24. No overlap with DISC-021–026. No overlap with CAND-006–CAND-073.

### Standalone Potential
MODERATE-TO-HIGH. If the fix window produces consistent directional amplification, this could operate as an independent daily strategy during fix days.

### Rare-Event Potential
LOW — the fix occurs daily (250+ days/year), so this is not a rare event. However, if the effect is selective (only on days with large pre-fix moves), the effective frequency could be lower.

### Component Potential
MODERATE. The fix-day direction signal could serve as a filter for other Gold strategies.

### State Potential
LOW. This is primarily an Alpha candidate.

### Regime Potential
LOW. The fix occurs regardless of market regime.

### Information-Sharing Potential
Could inform Gold direction at London hours, potentially useful as a morning session filter for Gold-related modules.

### Expected Failure Mode
The pre-fix move may be random noise rather than genuine directional pressure. The fix window may not amplify the direction if fix participants are evenly split. Counterfactual may show similar momentum continuation on non-fix days.

### Proposed G1 Measurement
Measure XAUUSD return from 10:30 to 11:00 AM London time, conditioned on pre-fix direction exceeding threshold. Compare to counterfactual (same time window on non-fix days, or same pre-fix magnitude at random times).

---

## 6. Candidate 075 — US Equity Closing Auction Concentrated Order Flow

### Candidate ID
CAND-075

### Name
US Equity Closing Auction Concentrated Order Flow

### Artifact Type
STANDALONE ALPHA / RARE-EVENT ALPHA (provisional)

### Mechanism Family
Settlement / Benchmark / Mandatory Flow (Family 1) — different mechanism from CAND-074

### Participant Constraint
The US equity closing auction at 4:00 PM ET matches buy and sell orders to determine a single closing price. Index funds, ETFs, and pension funds that must execute at the close (for NAV calculation, rebalancing, or mandate compliance) cannot choose when or at what price to transact — they must participate in the closing auction. This creates a concentrated window of price-insensitive order flow.

### Why Now?
The closing auction is the single most concentrated liquidity event in US equities. Approximately 6–8% of daily volume executes in the final minutes. Index rebalancing (monthly/quarterly), options expiry, and derivatives settlement all reference the closing price. Participants with closing-price mandates must transact regardless of short-term price direction.

### Hypothesis
When USATECHIDXUSD exhibits directional movement in the final 10 minutes before 4:00 PM ET (the MOC order submission window), the closing auction amplifies that direction because:
1. MOC orders submitted in the direction of the prevailing move create additional pressure;
2. The closing price becomes the reference for NAV calculation, creating follow-on activity;
3. The concentrated volume in the final minutes produces larger-than-normal price displacement.

### Observable Variables
- USATECHIDXUSD price direction from 3:50 PM to 4:00 PM ET;
- USATECHIDXUSD closing price vs 3:50 PM price;
- USATECHIDXUSD price in the first 30 minutes after close (next session open, if available);

### Exact Setup
Define "late-session directional move" as the USATECHIDXUSD price change from 3:50 PM to 3:59 PM ET.

### Exact Confirmation
The late-session move must exceed a defined magnitude threshold in either direction.

### Exact Entry
At 3:59 PM ET (one minute before close), enter USATECHIDXUSD in the direction of the late-session move.

### Exact Exit
At 4:00 PM ET close (capturing the closing auction itself).

### Direction
Same direction as the late-session move (momentum into the close).

### Rearm Rule
One event per day.

### Economic Displacement Logic
The closing auction is a deterministic, time-constrained execution window. Index funds and ETFs that must execute at the close create non-discretionary order flow concentrated in the final 2–3 minutes. When the late-session direction indicates which side has more pressure, the MOC orders in that direction amplify the move. The closing price then becomes the reference for NAV calculation, creating a self-reinforcing effect.

### Expected Asymmetry
The closing auction is the most concentrated liquidity event of the day. Participants cannot choose their execution time — they must participate at the close. This structural constraint creates temporary but large directional pressure.

### Economic Headroom
USATECHIDXUSD at ~30,000. A 10 bps move = 30 points. If the closing auction produces even 5–10 bps of additional directional movement, this is meaningful. The closing auction is known to produce larger-than-normal price dislocation.

### Counterfactual
Compare the closing auction return (3:59–4:00 PM) on days with large late-session moves vs the same late-session move occurring at a random time during the day. The counterfactual isolates whether the closing auction itself adds directional value beyond the late-session momentum.

### Data Availability
USATECHIDXUSD M1 data is available. 4:00 PM ET closing time is deterministic. No hidden data required.

### Causal Observability
The closing auction timing is observable. The price movement into and out of the close is observable. The MOC order flow motivations are hypothesized (mandate compliance) but not directly observed. The price consequence is directly measurable.

### Prior-Art
NEW. CAND-024 tested Friday de-risking (different mechanism — Friday-specific portfolio risk reduction, not daily closing auction). CAND-072 tested Friday compression (different mechanism — weekly range pattern). No previous candidate tested the daily closing auction as a directional mechanism.

### Closed-Line Check
No overlap with V19–V24. No overlap with DISC-021–026. No overlap with CAND-006–CAND-073.

### Standalone Potential
MODERATE-TO-HIGH. If the closing auction produces consistent directional amplification on high-momentum days, this could operate as an independent daily strategy.

### Rare-Event Potential
MODERATE. If the effect is selective (only on days with large late-session moves, perhaps ~50–80 days/year), the effective frequency enters the range where per-event economics matter more than frequency.

### Component Potential
MODERATE. The closing auction direction signal could serve as an end-of-day filter for other US Tech strategies.

### State Potential
LOW. This is primarily an Alpha candidate.

### Regime Potential
MODERATE. The closing auction effect may be stronger during high-volatility regimes when MOC order flow is larger.

### Information-Sharing Potential
Could inform end-of-day direction for any US Tech module.

### Expected Failure Mode
The late-session move may be random noise. The closing auction may not amplify the direction if MOC orders are balanced. The effect may be too small to survive friction. The counterfactual (random intraday windows) may show similar momentum continuation.

### Proposed G1 Measurement
Measure USATECHIDXUSD return from 3:59 PM to 4:00 PM ET, conditioned on late-session direction exceeding threshold. Compare to counterfactual (same return measurement at random intraday times with similar momentum).

---

## 7. Candidate 076 — Gold Overnight Repricing → Technology Index Opening Direction

### Candidate ID
CAND-076

### Name
Gold Overnight Repricing → Technology Index Opening Direction

### Artifact Type
ALPHA / EVENT

### Mechanism Family
Cross-Market Information Transmission (Family 3) — genuine sequencing, not generic correlation

### Participant Constraint
Gold and US Technology are both components of global risk sentiment, but they reprice at different times due to market microstructure:
1. Gold trades nearly 24 hours (亚洲, London, New York);
2. USATECHIDXUSD has limited overnight trading (electronic, thin);
3. When Gold reprices overnight (due to geopolitical events, central bank actions, or Asian session risk shifts), the information is transmitted to US Tech at the US open.

The constraint is:
> Gold has already repriced. US Tech participants must incorporate this information at the open, creating a delayed reaction.

### Why Now?
The US equity open at 9:30 AM ET is when the majority of institutional order flow enters the market. Overnight Gold repricing provides information about global risk sentiment that US Tech participants must incorporate. The first 30 minutes of US Tech trading represent the period of maximum information incorporation.

### Hypothesis
When Gold moves significantly overnight (defined as the move from the previous US close to the current pre-market), USATECHIDXUSD opens in the same direction but with a measurable delay, creating an executable opportunity at the US open.

### Observable Variables
- XAUUSD price at previous US close (4:00 PM ET);
- XAUUSD price at current US pre-market (9:00 AM ET);
- USATECHIDXUSD opening price at 9:30 AM ET;
- USATECHIDXUSD price at 10:00 AM ET.

### Exact Setup
Define "overnight Gold move" as (XAUUSD at 9:00 AM ET − XAUUSD at previous 4:00 PM ET) / previous close × 10,000 bps.

### Exact Confirmation
The overnight Gold move must exceed a defined magnitude threshold (e.g., ±30 bps) in either direction.

### Exact Entry
At 9:30 AM ET, enter USATECHIDXUSD in the direction of the overnight Gold move.

### Exact Exit
At 10:00 AM ET (30 minutes after entry).

### Direction
Same direction as the overnight Gold move (Gold up → Tech up; Gold down → Tech down).

### Rearm Rule
One event per day. Maximum one event per day.

### Economic Displacement Logic
Gold repricing overnight reflects global risk sentiment shifts that US Tech participants must incorporate at the open. The 30-minute window represents the period of maximum information incorporation. If Gold has moved significantly overnight, US Tech opens with a "gap" in risk repricing that gets filled during the first 30 minutes of trading. The institutional order flow at the open (portfolio rebalancing, risk model updates, hedging adjustments) creates directional pressure in the same direction as the Gold move.

### Expected Asymmetry
Gold is a leading indicator of global risk sentiment. When Gold moves significantly overnight, it reflects information that US Tech participants must incorporate at the open. The asymmetry comes from the delay — Gold has already repriced, but US Tech has not yet fully incorporated the information.

### Economic Headroom
If Gold moves 30+ bps overnight and US Tech follows with even 10–20 bps in the same direction, this exceeds 2 bps friction. The mechanism is structural (information transmission delay) rather than statistical.

### Counterfactual
Same time window (9:30–10:00 AM ET) on days WITHOUT significant overnight Gold movement. The counterfactual isolates whether the Gold information provides value beyond normal morning momentum.

### Data Availability
Both XAUUSD and USATECHIDXUSD M1 data are available. Overnight prices are observable. No hidden data required.

### Causal Observability
Gold overnight movement is observable. US Tech opening direction is observable. The information transmission mechanism (Gold → risk sentiment → Tech repricing) is hypothesized but the price consequence is directly measurable.

### Prior-Art
CAND-071 tested Gold→Tech information transmission but used a different mechanism (Gold evening/overnight move → Tech at 9:30–10:00 AM, with a 50 bps threshold). CAND-076 differs in:
1. Threshold: 30 bps (lower, capturing more events);
2. Entry timing: at the open (9:30 AM) vs during the first 30 minutes;
3. Hypothesis: delayed information incorporation at the open vs directional momentum;
4. Mechanism: institutional order flow at the open vs generic cross-market correlation.

CAND-071 used a 50 bps threshold and tested the 9:30–10:00 window. CAND-076 uses a 30 bps threshold and tests the open specifically. The economic mechanism (delayed information incorporation at the institutional order flow peak) is genuinely distinct from CAND-071's mechanism (Gold direction → Tech direction).

### Closed-Line Check
CAND-076 is an EXTENSION of CAND-071. The original hypothesis (Gold → Tech) is preserved, but the mechanism is materially different:
- CAND-071: Gold overnight direction → Tech 9:30–10:00 momentum;
- CAND-076: Gold overnight magnitude → Tech open repricing (institutional order flow).

This is not a rescue of CAND-071. CAND-071 failed on negative absolute economics (-1.99 bps). CAND-076 tests a different economic mechanism (information incorporation at the open) with different entry timing and threshold.

### Standalone Potential
MODERATE. If the Gold information provides consistent directional value at the US open, this could operate as an independent daily strategy.

### Rare-Event Potential
LOW — with a 30 bps threshold, events occur ~50–100 times/year, placing this in the normal-frequency range.

### Component Potential
MODERATE. The Gold direction signal could serve as an opening-session filter for other US Tech modules.

### State Potential
LOW. This is primarily an Alpha candidate.

### Regime Potential
MODERATE. The Gold→Tech transmission may be stronger during high-risk-sentiment regimes.

### Information-Sharing Potential
Could inform opening direction for any US Tech module. The Gold signal provides a cross-market risk-on/risk-off filter.

### Expected Failure Mode
The Gold overnight move may not predict Tech direction at the open. The 30 bps threshold may be too low (noise) or too high (rare). The counterfactual (random morning windows) may show similar momentum. The mechanism may have already been arbitraged away by high-frequency participants.

### Proposed G1 Measurement
Measure USATECHIDXUSD return from 9:30 to 10:00 AM ET, conditioned on overnight Gold move exceeding threshold. Compare to counterfactual (same time window on days without significant Gold movement).

---

## 8. Mechanism Diversity

| Candidate | Mechanism Family | Distinct Mechanism |
|---|---|---|
| CAND-074 | Settlement/Benchmark (Family 1) | London Gold Fix — daily benchmark execution pressure |
| CAND-075 | Settlement/Benchmark (Family 1) | US Equity Closing Auction — daily concentrated order flow |
| CAND-076 | Cross-Market Transmission (Family 3) | Gold overnight repricing → Tech open (information incorporation) |

While CAND-074 and CAND-075 both belong to the Settlement/Benchmark family, their mechanisms are materially different:
- CAND-074: Price determination process (fix) with contractual obligation;
- CAND-075: Order matching process (closing auction) with mandate compliance.

CAND-076 is in a different family entirely (Cross-Market Transmission).

All three candidates use different instruments and different times of day:
- CAND-074: XAUUSD, 10:30 AM London;
- CAND-075: USATECHIDXUSD, 4:00 PM ET;
- CAND-076: XAUUSD + USATECHIDXUSD, 9:30 AM ET.

---

## 9. Economic Displacement Comparison

| Candidate | Expected Displacement Source | Structural vs Statistical | Friction Headroom |
|---|---|---|---|
| CAND-074 | Fix participants must transact → concentrated flow → price amplification | Structural (contractual obligation) | If 5–10 bps amplification, exceeds 2 bps friction |
| CAND-075 | MOC orders must execute → concentrated flow → closing price amplification | Structural (mandate compliance) | If 5–10 bps amplification, exceeds 2 bps friction |
| CAND-076 | Gold info → Tech open → delayed repricing → directional flow | Structural (information delay) | If 10–20 bps Tech follow-through, exceeds 2 bps friction |

All three candidates identify structural participant constraints that could produce measurable displacement. None rely on statistical pattern matching alone.

---

## 10. Counterfactual Quality

| Candidate | Counterfactual | Discriminating Power |
|---|---|---|
| CAND-074 | Same time window on non-fix days, or same pre-fix magnitude at random times | STRONG — isolates fix window effect from general momentum |
| CAND-075 | Same late-session move at random intraday times | STRONG — isolates closing auction effect from general momentum |
| CAND-076 | Same time window on days without significant Gold movement | MODERATE — isolates Gold information from general morning momentum |

All counterfactuals are legitimately designed to isolate the specific mechanism being tested.

---

## 11. Data Feasibility

| Candidate | Required Data | Available? | Notes |
|---|---|---|---|
| CAND-074 | XAUUSD M1 | YES | London fix time is deterministic and publicly known |
| CAND-075 | USATECHIDXUSD M1 | YES | Closing auction time is deterministic |
| CAND-076 | XAUUSD M1 + USATECHIDXUSD M1 | YES | Both datasets in repository |

No candidate requires unavailable data.

---

## 12. Rare-Event Opportunities

None of the three candidates are inherently rare events. All occur daily. However, if the effect is selective (only on days meeting certain conditions), the effective frequency could be lower:

- CAND-074: Only on days with large pre-fix moves (~50–100/year);
- CAND-075: Only on days with large late-session moves (~50–80/year);
- CAND-076: Only on days with large overnight Gold moves (~50–100/year).

If per-event economics are strong enough, these could qualify for rare-event forward validation at reduced effective frequency.

---

## 13. State / Condition Opportunities

No V25 candidates are primarily State/Condition artifacts. All three are Alpha/Event candidates. However:

- CAND-076's Gold direction could serve as a risk-on/risk-off filter for other modules;
- CAND-075's late-session direction could serve as an end-of-day filter;
- CAND-074's pre-fix direction could serve as a London-session Gold filter.

These are secondary component potential, not primary classification.

---

## 14. Regime / Specialist Opportunities

- CAND-075 may be stronger during high-volatility regimes (larger MOC order flow);
- CAND-076 may be stronger during high-risk-sentiment regimes (larger Gold moves).

No V25 candidates are primarily Regime/Specialist artifacts.

---

## 15. Prior-Art / Redundancy

| Candidate | Classification | Notes |
|---|---|---|
| CAND-074 | NEW | No previous candidate tested London Gold Fix execution pressure |
| CAND-075 | NEW | No previous candidate tested daily closing auction as directional mechanism |
| CAND-076 | EXTENSION | CAND-071 tested Gold→Tech but different mechanism, timing, and threshold |

---

## 16. Closed-Line Firewall

No V25 candidate reopens or rescues any closed research line. CAND-076 is explicitly classified as an EXTENSION with a materially different mechanism from CAND-071.

---

## 17. Protected Forward Runtime

### CAND-015
> ACTIVE / PROTECTED / UNTOUCHED

### CAND-024
> ACTIVE / PROTECTED / UNTOUCHED
> Canonical: `CAND-024:CANONICAL:925495a8`

### CAND-035
> ACTIVE / PROTECTED / UNTOUCHED
> Canonical: `CAND-035:CANONICAL:ddc5d0e9`

Do not modify, inspect, or adjudicate forward results.

---

## 18. G1

> NOT EXECUTED

---

## 19. System Assembly

> NOT EXECUTED

---

## 20. Next Milestone

> G1 — ECONOMIC PLAUSIBILITY SCREEN (V25)
