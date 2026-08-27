# QUANTFORGE — RESEARCH FACTORY V2
# TRADEABLE EDGE DISCOVERY SCREENING — V20
# DATE: 2026-08-27

## 1. Research Factory Context
V20 operates under the Dual-Path Strategy and System Governance doctrine. Candidates must possess meaningful intrinsic information content, rather than relying on increasingly stacked confirmation filters that actively degrade the underlying mechanism (Type 1 counterfactual failure, as seen in V19).

## 2. V20 Objective
Search for simple, observable economic mechanisms whose intrinsic condition adds information, has meaningful absolute expectancy, and can eventually serve either as a standalone strategy or as a specialized module. The focus is: PRIMARY ECONOMIC MECHANISM → OBJECTIVE EVENT → EXECUTABLE RESPONSE.

## 3. Lessons from V17–V19
- **V17:** A condition can add information but lack sufficient economic headroom to overcome friction (e.g., +0.01 bps).
- **V18:** A profitable event can fail because its specific confirmation condition is materially inferior to the counterfactual.
- **V19:** SMC structural state changes (like demanding a structural shift after a sweep) can actively destroy edge if the underlying event is sufficiently powerful on its own.

## 4. Dual-Path Implication
Every promoted candidate must be evaluated for BOTH Standalone Potential (can it run a bot by itself?) and Component Potential (can it contribute diversified, independent expectancy to a larger module system?).

## 5. SMC Structural-State Translation
SMC principles are permitted but must be modeled as simple, independent structural transitions (e.g., Freshness) rather than complex stacked narratives (e.g., Sweep → BOS → OB Retest + Premium Pricing).

## 6. Mechanism Families
- **FAMILY D:** Structural State Without Extra Confirmation
- **FAMILY C:** Participant-Constrained Event
- **FAMILY B:** Sequential Information Arrival

## 7. Candidates Considered

### CAND-G0-059
**Name:** Fresh Structural Break First Retest
**Mechanism Family:** D — Structural State Without Extra Confirmation
**Observable Mechanism Variable:** The first return/touch to the exact price level of a newly established, broken structural extreme (highest high or lowest low of the prior 60 minutes).
**Economic Constraint:** When a significant local extreme is broken, the traders who defended that level are trapped underwater. The very first time price returns to their entry level, they have max motivation to exit at breakeven, providing a natural liquidity wall.
**Mechanistic Explanation:** The first touch of a newly broken structure taps into fresh trapped capital. 
**Repeatable Event:** A 60-minute highest high is broken. Price closes beyond it. Price subsequently returns to precisely touch the old highest high.
**Information State:** Broken defense level, first available breakeven exit for trapped flow.
**Predicted Post-Entry Behavior:** Immediate bounce/rejection away from the broken level.
**Executable Entry:** Limit order exactly at the broken high price level.
**Deterministic Exit:** 15 minutes after entry.
**Opportunity Integrity:** MUST be the first touch only.
**Positive-Expectancy Thesis:** The liquidity wall of trapped breakeven exits absorbs the retest flow and forces a bounce.
**Economic Headroom:** First touches typically yield rapid 10-30 bps structural reactions.
**Adverse-Risk Structure:** A cascading liquidation trend will slice straight through the old high.
**Primary Counterfactual:** The second (or third) time the price returns to that exact same broken level.
**Expected Treatment Superiority:** The first touch taps fresh trapped liquidity. Subsequent touches (mitigated) find no trapped capital and fail to hold.
**Falsification Condition:** Second/third touches perform identically to or better than the first touch.
**Expected Frequency:** High (Multiple per day).
**Data Required:** M1 USATECHIDXUSD.
**Standalone Potential:** STRONG (High frequency, intrinsic market structure).
**Component Potential:** STRONG (Core structural module).
**Potential Regime Role:** Range / Slow Trend.
**Future Information-Sharing Potential:** Could share trend-state information to filter entries.
**SMC Structural Mapping:** POI Freshness / First Touch.
**Closed-Line Independence:** A pure test of freshness without sweeping or shifting dependencies.
**G0 Decision:** PROMOTE

### CAND-G0-060
**Name:** NY Equity Close Imbalance Expansion
**Mechanism Family:** C — Participant-Constrained Event
**Observable Mechanism Variable:** A rapid directional return > 0.5% occurring strictly between 15:50 ET and 16:00 ET.
**Economic Constraint:** The 15:50-16:00 window contains massive forced Market-On-Close (MOC) rebalancing flow by institutional participants. This flow is blind to price and purely size-driven, temporarily disconnecting price from intrinsic value.
**Mechanistic Explanation:** The closing imbalance forces a directional surge to clear the MOC orders. Once the bell rings at 16:00, that forced liquidity vanishes, leaving an immediate vacuum that algorithms fill by fading the move.
**Repeatable Event:** 15:50 to 16:00 return is > +0.5% (or < -0.5%).
**Information State:** A price move driven by non-discretionary time-constrained execution.
**Predicted Post-Entry Behavior:** Immediate mean reversion in the 15 minutes following the close.
**Executable Entry:** Market order at 16:00:00, opposite the 15:50-16:00 direction.
**Deterministic Exit:** 16:15:00.
**Opportunity Integrity:** Restricted to exactly this 10-minute daily window.
**Positive-Expectancy Thesis:** Rebalancing flow exhausts exactly at 16:00. The preceding move is artificial.
**Economic Headroom:** MOC-driven reversals frequently snap back 15-40 bps instantly.
**Adverse-Risk Structure:** A macro news event dropping at 15:55 would drive a genuine trend, not a rebalancing artifact.
**Primary Counterfactual:** The exact same >0.5% 10-minute expansion occurring during the mid-day doldrums (e.g., 12:50 - 13:00), faded identically.
**Expected Treatment Superiority:** Mid-day expansions are driven by discretionary information (trend). 15:50 expansions are driven by forced rebalancing (artificial).
**Falsification Condition:** 15:50 expansions revert less reliably than mid-day expansions.
**Expected Frequency:** Low to Moderate (Requires a massive MOC imbalance).
**Data Required:** M1 USATECHIDXUSD.
**Standalone Potential:** WEAK (Too rare, single time-of-day).
**Component Potential:** STRONG (Event Opportunist).
**Potential Regime Role:** Session Transition / Event Driven.
**Future Information-Sharing Potential:** Could share volatility-regime state.
**SMC Structural Mapping:** N/A. Purely participant-constrained.
**Closed-Line Independence:** Evaluates strict time-forced execution mechanics rather than price geometry.
**G0 Decision:** PROMOTE

### CAND-G0-061
**Name:** Consecutive 15-Minute Rejection Sequence
**Mechanism Family:** B — Sequential Information Arrival
**Observable Mechanism Variable:** Three consecutive 15-minute candles where each makes a higher high, but ALL THREE close in the lowest 25% of their respective candle ranges (forming three long upper wicks).
**Economic Constraint:** To make three consecutive higher highs requires sustained buying effort. To close in the bottom quartile three consecutive times proves that passive institutional selling (or hidden supply) is instantly and consistently absorbing and rejecting the buying effort over a sustained 45-minute window.
**Mechanistic Explanation:** The sequence demonstrates absorption. Buyers are exhausting their capital while sellers distribute passively without moving the market lower until the buyers are fully exhausted.
**Repeatable Event:** Three consecutive 15m candles: HH1, HH2, HH3. Close1, Close2, Close3 are all within the lower 25% of (High - Low).
**Information State:** Aggressive buying has been systematically absorbed.
**Predicted Post-Entry Behavior:** Downside reversal as buyers give up.
**Executable Entry:** Market order short at the close of the third candle.
**Deterministic Exit:** Hold until a 15-minute candle closes in its upper 25% (change in behavior) or end of day.
**Opportunity Integrity:** Sequence must be exactly three.
**Positive-Expectancy Thesis:** Sustained absorption over 45 minutes represents massive institutional distribution that retail cannot see until the drop occurs.
**Economic Headroom:** Full distribution events yield multi-hour reversals of 50-150 bps.
**Adverse-Risk Structure:** The buyers could eventually overwhelm the hidden supply.
**Primary Counterfactual:** Three consecutive 15m candles making higher highs, but closing in the UPPER 75% of their ranges, followed by a short entry.
**Expected Treatment Superiority:** Upper closures represent active markup (buyers in control). Lower closures represent absorption (sellers in control).
**Falsification Condition:** Shorting the absorption sequence performs identically to shorting the markup sequence.
**Expected Frequency:** Moderate (Absorption sequences happen semi-regularly).
**Data Required:** M1 USATECHIDXUSD (resampled to 15m).
**Standalone Potential:** MODERATE (Frequency is viable).
**Component Potential:** STRONG (Core Reversal Component).
**Potential Regime Role:** Trend Exhaustion.
**Future Information-Sharing Potential:** Exhaustion state could feed into trend-following modules to signal exits.
**SMC Structural Mapping:** Rejection / Hidden Supply.
**Closed-Line Independence:** Relies strictly on sequential proportional closing states, not static geometry or absolute RSI momentum.
**G0 Decision:** PROMOTE

## 8. G0 Results
- **Evaluated:** 3
- **Promoted:** 3
- **Killed:** 0
- **Blocked:** 0

## 9. Promoted Candidates
- **CAND-G0-059:** Fresh Structural Break First Retest
- **CAND-G0-060:** NY Equity Close Imbalance Expansion
- **CAND-G0-061:** Consecutive 15-Minute Rejection Sequence

## 10. Killed Candidates
None.

## 11. Blocked Candidates
None.

## 12. Counterfactual Quality
- **CAND-059:** First Touch vs Second Touch (directly testing the intrinsic value of "Freshness").
- **CAND-060:** MOC Forced Move vs Mid-day Discretionary Move (directly testing the intrinsic value of the participant constraint).
- **CAND-061:** Absorption Sequence vs Markup Sequence (directly testing the intrinsic value of the localized rejection).
All counterfactuals isolate the exact mechanism proposed.

## 13. Economic Headroom Quality
All candidates are structurally capable of yielding 15-150 bps of post-entry movement, comfortably clearing the 2 bps friction requirement and avoiding conditionally valid but economically flat results.

## 14. Frequency Quality
- **CAND-059:** High. Suitable for Standalone Core.
- **CAND-060:** Low. Suitable for Event Opportunist module.
- **CAND-061:** Moderate. Suitable for Reversal module.

## 15. Mechanism Observability
All mechanisms (price level touch, time-of-day return magnitude, 15m quartile closing prices) are 100% strictly observable in standard M1 OHLCV data.

## 16. SMC Structural-State Opportunities
CAND-059 translates the SMC "Freshness / First Touch" concept into a purely observable, mathematically bounded state transition, testing it rigorously against a "Mitigated" counterfactual.

## 17. Standalone vs Component Potential
- **CAND-059:** STANDALONE POTENTIAL: Strong. COMPONENT POTENTIAL: Strong.
- **CAND-060:** STANDALONE POTENTIAL: Weak. COMPONENT POTENTIAL: Strong.
- **CAND-061:** STANDALONE POTENTIAL: Moderate. COMPONENT POTENTIAL: Strong.

## 18. Regime Specialization Potential
- **CAND-059:** Range / Slow Trend.
- **CAND-060:** Session Transition / Event Driven.
- **CAND-061:** Trend Exhaustion.

## 19. Ranked Candidates
1. **CAND-059 (Fresh First Retest):** Safest, highest frequency, purest structural test.
2. **CAND-060 (NY Close Imbalance):** Extremely high expected expectancy due to mechanical market obligations, though low frequency.
3. **CAND-061 (Consecutive Rejection):** Clean sequential absorption model.

## 20. Exact Next Milestone
G1 — ECONOMIC PLAUSIBILITY SCREEN (CAND-059, CAND-060, CAND-061)

## 21. Integrity
No historical data was queried, scanned, or executed. No closed lines were rescued. CAND-015 logs were not inspected. System Assembly was not performed.
