# QUANTFORGE — RESEARCH FACTORY V2
# TRADEABLE EDGE DISCOVERY SCREENING — V12
# MECHANISM-DISCRIMINATING / COUNTERFACTUAL-FIRST DISCOVERY
# DATE: 2026-08-26

## 1. Research Factory V2 Context
The objective of the QuantForge Research Factory V2 is the systematic discovery of independent behavioral artifacts with positive economic expectancy. V12 candidate generation shifts focus from simple descriptive economics to scientific counterfactuals.

## 2. V12 Thesis
**Search for mechanisms where the event itself creates a distinctive causal prediction against a predeclared counterfactual.** The goal is to design candidates that are strictly falsifiable. A mechanism must predict that an observable event causes a specific post-entry response, and critically, that a mechanically defined counterfactual (where the mechanism is absent) behaves materially differently.

## 3. Lessons from CAND-032
CAND-032 (NY Open Structural Momentum) possessed strong descriptive out-of-sample economics (+12.02 mean net), yet failed G3 scientific validation (p=0.1133). Its extreme unhedged variance paralyzed inference, meaning its strong returns could not be mathematically separated from generic, random directional drift on highly volatile days. The primary lesson: *Positive expected returns do not automatically prove the registered mechanism.* G0 candidates must therefore have a strong, structural counterfactual built-in.

## 4. Candidate Generation Method
- **Method:** Heuristic identification of structural constraints, participant scheduling, and information state changes that yield testable counterfactuals.
- **Constraints:** M1 OHLCV data only; executable capture required; no look-ahead/MFE.
- **Requirement:** Every candidate must define a primary counterfactual and a falsification condition before advancing to G1.

## 5. Mechanism Families
- **FAMILY B:** Forced Flow / Scheduled Mechanics
- **FAMILY C:** Price Acceptance / Rejection
- **FAMILY D:** Cross-Market Confirmation / Disconfirmation

---

## 6. Candidates Considered

### CAND-G0-035
**Name:** Month-End Final-Hour Imbalance Acceleration
**Mechanism Family:** B — Forced Flow / Scheduled Mechanics
**Mechanistic Explanation:** Institutional equity rebalancing and benchmark-tracking flow heavily concentrate on the final trading day of the month, specifically forcing volume into the closing auction. If the daily trend is already established by 15:00 ET, forced tracking execution accelerates the trend into the close, overriding normal mean-reversion behavior.
**Repeatable Event:** Last trading day of the month. USATECHIDXUSD 15:00 ET price is > 09:30 ET open (Up Day).
**Information State:** The market is definitively up heading into the final hour of the monthly performance window.
**Predicted Direction:** Long.
**Executable Entry:** 15:00 ET (Market).
**Deterministic Exit:** 16:00 ET (Market).
**Opportunity Integrity:** 1 event per month maximum. No overlap.
**Positive-Expectancy Thesis:** Upside is driven by forced price-insensitive structural flow. Downside is bounded because the tracking flow actively resists mean-reversion during this specific hour.
**Adverse-Risk Structure:** Benchmark tracking dampens sudden adverse shocks in the final hour of the month.
**Primary Counterfactual:** The exact same NY session return (09:30-15:00 ET) occurring on the 15th of the month (a standard mid-month day).
**Expected Counterfactual Difference:** The mid-month day should exhibit standard late-day mean reversion or random drift, whereas the month-end day should exhibit persistent, accelerated directional drift.
**Falsification Condition:** The month-end final hour return distribution is statistically indistinguishable from the mid-month final hour return distribution.
**Data Required:** M1 USATECHIDXUSD.
**Cross-Market Scope:** Single asset.
**Intended Component Role:** EVENT OPPORTUNIST.
**Closed-Line Independence:** Fully independent of CAND-024 (Friday positional flow).
**G0 Decision:** PROMOTE

### CAND-G0-036
**Name:** Structural Prior-Day High Pre-Market Acceptance
**Mechanism Family:** C — Price Acceptance / Rejection
**Mechanistic Explanation:** The Prior Day High (PDH) is a major structural reference. If the market gaps above it, it often mean-reverts to fill the gap. However, if the market spends the entire pre-market hour (08:30-09:30 ET) trading strictly *above* the PDH, it indicates verified structural acceptance of higher prices, leading to NY session continuation.
**Repeatable Event:** Between 08:30 ET and 09:30 ET, the lowest printed price of USATECHIDXUSD remains strictly > the Prior Day High (09:30-16:00 ET High).
**Information State:** The market has structurally accepted the PDH breakout before the NY open, transitioning from "breakout" to "established value."
**Predicted Direction:** Long.
**Executable Entry:** 09:30 ET (Market).
**Deterministic Exit:** 16:00 ET (Market).
**Opportunity Integrity:** Evaluated once daily at 09:30 ET.
**Positive-Expectancy Thesis:** Continuation days from accepted breakouts are structurally unbounded and can trend heavily.
**Adverse-Risk Structure:** Failed acceptance leads to gap-fills, but the 60-minute pre-market duration filter specifically screens out weak gap-ups, isolating high-conviction structural shifts.
**Primary Counterfactual:** The NY Open (09:30 ET) opens > PDH, but the 08:30-09:30 ET period traded *below* the PDH at some point (an untested or partial gap-up).
**Expected Counterfactual Difference:** The accepted PDH yields a positive-expectancy continuation. The unverified gap-up counterfactual yields mean reversion (negative continuation expectancy).
**Falsification Condition:** Both the strictly accepted breakout and the unverified gap-up produce the exact same mean-reverting or drifting response.
**Data Required:** M1 USATECHIDXUSD.
**Cross-Market Scope:** Single asset.
**Intended Component Role:** CORE COMPONENT / REGIME SPECIALIST.
**Closed-Line Independence:** Distinct from CAND-032 (which was a London range breakout, not a multi-day structural PDH reference).
**G0 Decision:** PROMOTE

### CAND-G0-037
**Name:** Cross-Index Tech Leadership Divergence
**Mechanism Family:** D — Cross-Market Confirmation / Disconfirmation
**Mechanistic Explanation:** USATECH (NDX) acts as the high-beta structural leader for USA500 (SPX). When tech establishes a strong, persistent morning trend while the broader market lags or trades negatively, the divergence represents a mispricing of macroeconomic risk. USA500 is structurally forced to resolve the divergence by catching up to tech in the afternoon.
**Repeatable Event:** At 12:00 ET, USATECHIDXUSD return (from 09:30 ET open) is > +0.50%, AND USA500IDXUSD return (from 09:30 ET open) is < 0.00%.
**Information State:** A structural divergence exists where the high-beta leader is trending heavily while the broad aggregate is lagging.
**Predicted Direction:** Long USA500.
**Executable Entry:** 12:00 ET (Market) on USA500.
**Deterministic Exit:** 16:00 ET (Market) on USA500.
**Opportunity Integrity:** Evaluated once daily at 12:00 ET.
**Positive-Expectancy Thesis:** Arbitrage/relative-value tracking flows force the lagging index to reprice toward the leader, generating a directional afternoon edge.
**Adverse-Risk Structure:** Risk is limited because the primary driver (tech) has already established strong structural support for the day, reducing the probability of a massive afternoon broad-market collapse.
**Primary Counterfactual:** At 12:00 ET, USA500 return is < 0.00%, BUT USATECH return is ALSO < 0.00% (no divergence).
**Expected Counterfactual Difference:** Without tech leadership, USA500 drifts or continues lower. With tech leadership, USA500 sharply reverses upward.
**Falsification Condition:** The post-12:00 return distribution of USA500 is identical regardless of whether tech is up > +0.5% or down.
**Data Required:** M1 USATECHIDXUSD, M1 USA500IDXUSD.
**Cross-Market Scope:** Dual asset.
**Intended Component Role:** CROSS-MARKET COMPONENT.
**Closed-Line Independence:** Entirely new cross-market design.
**G0 Decision:** PROMOTE

---

## 7. G0 Results
- **Evaluated:** 3
- **Promoted:** 3
- **Killed:** 0
- **Blocked:** 0

## 8. Promoted Candidates
- **CAND-G0-035:** Month-End Final-Hour Imbalance Acceleration
- **CAND-G0-036:** Structural Prior-Day High Pre-Market Acceptance
- **CAND-G0-037:** Cross-Index Tech Leadership Divergence

## 9. Killed Candidates
None.

## 10. Blocked Candidates
None.

## 11. Counterfactual Quality
All three promoted candidates possess mechanically strictly defined counterfactuals that can be explicitly coded in G1/G3. Rather than testing against a random noise generator, these candidates can be tested against highly specific, behaviorally distinct market states to isolate the actual causal mechanism.

## 12. Mechanism Diversity
The three candidates cover three distinct mechanism families: Scheduled Flow (B), Structural Acceptance (C), and Cross-Market Divergence (D).

## 13. Ranked Candidates
1. **CAND-037:** Exceptionally clear cross-market mechanism with a perfect counterfactual.
2. **CAND-035:** Extremely strong flow-based economic logic, though lower frequency.
3. **CAND-036:** Strong structural logic, though potentially subject to higher baseline variance.

## 14. Component Potential
- CAND-035 targets EVENT OPPORTUNIST.
- CAND-036 targets CORE / REGIME SPECIALIST.
- CAND-037 targets CROSS-MARKET COMPONENT.

## 15. Exact Next Milestone
G1 — ECONOMIC PLAUSIBILITY SCREEN (CAND-035, CAND-036, CAND-037)

## 16. Integrity
No historical data was queried, scanned, or executed during candidate generation. No closed lines were rescued. CAND-015 logs were not inspected. All designs are strictly theoretical at this stage.
