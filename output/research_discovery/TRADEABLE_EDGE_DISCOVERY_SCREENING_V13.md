# QUANTFORGE — RESEARCH FACTORY V2
# TRADEABLE EDGE DISCOVERY SCREENING — V13
# MECHANISM-FIRST / POSITIVE-EXPECTANCY / COMPONENT-AWARE
# DATE: 2026-08-26

## 1. Research Factory V2 Context
The objective of the QuantForge Research Factory V2 is the systematic discovery of independent behavioral artifacts with positive economic expectancy. V13 prioritizes identifying artifacts that may have lower frequency but possess robust, scientifically distinguishable mechanics, aimed at diversifying the future Component Register.

## 2. V13 Research Objective
Search for mechanisms that produce positive expectancy driven by structural market behavior, paired with a mechanistic counterfactual that enables explicit scientific falsification. V13 strictly avoids reproducing generic breakout, reversal, or lead/lag patterns that rely merely on historical data mining.

## 3. Lessons Applied
- **CAND-035 Lesson:** A rare event (4 opportunities/year) with exceptionally strong per-event economics (+62.36 mean net) is a highly valuable COMPONENT-CANDIDATE (Event Opportunist). V13 actively embraces specialized, lower-frequency mechanisms if the positive-expectancy logic is structurally sound.
- **CAND-036 / CAND-032 Lesson:** Volatile indices produce massive left-tail variance that paralyzes inference. Mechanisms must inherently limit downside exposure structurally, rather than relying on assumed mean-reversion, to survive the G3 variance trap.

## 4. Candidate Generation Method
- **Method:** Heuristic identification of specific institutional liquidity behaviors (lunch lulls, gap-fill rejections, and volatility regime transitions) that generate predictable directional imbalances.
- **Constraints:** M1 OHLCV data only; strict counterfactual definition required; executable capture mandatory.

## 5. Mechanism Families
- **FAMILY B:** Price Acceptance / Repricing
- **FAMILY D:** Session Transition
- **FAMILY E:** Volatility / Range State Transition

---

## 6. Candidates Considered

### CAND-G0-038
**Name:** Mid-Day Counter-Trend Reload
**Mechanism Family:** D — Session Transition
**Mechanistic Explanation:** Institutional participation often recedes during the NY lunch hour (12:00-13:00 ET). If the market established a massive directional trend in the morning, the lunch lull frequently allows a low-volume counter-trend pullback (profit taking). When institutional volume returns at 13:00 ET, they "reload" in the direction of the dominant morning trend at structurally advantageous prices.
**Repeatable Event:** Between 09:30 ET and 12:00 ET, the USATECHIDXUSD return is > +1.0%. Between 12:00 ET and 13:00 ET, the return is strictly negative (< 0.00%).
**Information State:** A dominant macro trend has paused for a low-volume liquidity reset.
**Predicted Direction:** Long (Continuation of the morning trend).
**Executable Entry:** 13:00 ET (Market).
**Deterministic Exit:** 16:00 ET (Market).
**Opportunity Integrity:** Evaluated once daily at 13:00 ET.
**Positive-Expectancy Thesis:** Upside is driven by the structural re-engagement of the dominant daily imbalance. Downside is bounded because the counter-trend pullback already flushed weak hands.
**Adverse-Risk Structure:** Structural flows actively defend the morning trend upon returning to the desk.
**Primary Counterfactual:** The morning trend is > +1.0%, but the 12:00-13:00 ET lunch period ALSO produces a positive return (> 0.00%).
**Expected Counterfactual Difference:** A counter-trend reload (CAND-038) yields strong continuation into the close. An exhausting lunch extension (counterfactual) yields late-day mean reversion and negative expectancy.
**Falsification Condition:** The post-13:00 return distribution is identical regardless of whether the lunch hour pulled back or extended.
**Expected Frequency:** Low to Moderate (15-25 events/year).
**Intended Component Role:** SESSION COMPONENT / REGIME SPECIALIST.
**Data Required:** M1 USATECHIDXUSD.
**Cross-Market Scope:** Single asset.
**Closed-Line Independence:** Entirely independent. Not related to Friday flows or month-end flows.
**G0 Decision:** PROMOTE

### CAND-G0-039
**Name:** Structural Gap-Fill Rejection
**Mechanism Family:** B — Price Acceptance / Repricing
**Mechanistic Explanation:** When the market gaps down aggressively at the open, structural mean-reversion participants attempt to buy the market to "fill the gap" (touch yesterday's close). If the market successfully touches yesterday's close but is violently rejected (failing to penetrate it and immediately collapsing back below the daily open), it confirms overwhelming seller dominance and the absolute failure of mean-reversion.
**Repeatable Event:** NY Open (09:30 ET) is < Yesterday's Close by at least -0.50%. Between 09:30 and 10:30 ET, the High touches Yesterday's Close but does not exceed it by more than +0.10%. At 10:30 ET, the price is strictly below the 09:30 ET Open.
**Information State:** The market definitively tested and rejected structural mean-reversion, trapping early buyers.
**Predicted Direction:** Short (Trend Down).
**Executable Entry:** 10:30 ET (Market).
**Deterministic Exit:** 16:00 ET (Market).
**Opportunity Integrity:** Evaluated once daily at 10:30 ET.
**Positive-Expectancy Thesis:** Trapped gap-fill buyers are forced to liquidate throughout the afternoon, creating persistent, one-directional downside flow. 
**Adverse-Risk Structure:** The structural ceiling (Yesterday's Close) has already been tested and confirmed as hard resistance, strictly limiting the probability of a massive afternoon short-squeeze.
**Primary Counterfactual:** The market gaps down, touches Yesterday's Close, but at 10:30 ET is trading strictly *above* the 09:30 ET Open.
**Expected Counterfactual Difference:** The rejected gap-fill yields heavy negative drift. The accepted/held gap-fill yields noisy, choppy mean-reversion with positive or zero drift.
**Falsification Condition:** The post-10:30 return distributions for the rejected state and the accepted state are statistically identical.
**Expected Frequency:** Low (10-20 events/year).
**Intended Component Role:** EVENT OPPORTUNIST / REGIME SPECIALIST.
**Data Required:** M1 USATECHIDXUSD.
**Cross-Market Scope:** Single asset.
**Closed-Line Independence:** Distinct from the PDH acceptance (CAND-036) as it focuses on explicit gap-fill rejection mechanics.
**G0 Decision:** PROMOTE

### CAND-G0-040
**Name:** Volatility Compression Expansion
**Mechanism Family:** E — Volatility / Range State Transition
**Mechanistic Explanation:** Markets alternate between low volatility and high volatility. A sudden, massive directional move originating from a compressed-volatility regime forces structural participants (options dealers, risk-parity funds) to dynamically re-hedge, amplifying the move. The same move occurring in an already high-volatility regime is merely noise and leads to exhaustion.
**Repeatable Event:** The prior 3-day ATR is strictly less than the 10-day ATR (volatility compression). The NY morning session range (09:30-10:30 ET) strictly exceeds the entire 3-day ATR. The 10:30 ET price closes in the top 10% of the morning range.
**Information State:** The market has structurally transitioned from a compressed state into a high-momentum expansion phase.
**Predicted Direction:** Long.
**Executable Entry:** 10:30 ET (Market).
**Deterministic Exit:** 16:00 ET (Market).
**Opportunity Integrity:** Evaluated once daily at 10:30 ET.
**Positive-Expectancy Thesis:** Volatility expansion from compression creates persistent, asymmetric trend days due to forced institutional re-hedging (gamma squeeze).
**Adverse-Risk Structure:** The structural origin (compression) implies that the market is inherently unbalanced and searching for a new equilibrium, favoring large trends over choppy mean-reversion.
**Primary Counterfactual:** The exact same morning event occurs (1st hour range > 3-day ATR, closing near the highs), but the 3-day ATR is strictly *greater* than the 10-day ATR (already in a high-volatility regime).
**Expected Counterfactual Difference:** Expansion from compression yields massive continuation. Expansion from an already extended volatility state yields exhaustion and mean-reversion.
**Falsification Condition:** The post-10:30 continuation returns are identical regardless of the preceding volatility regime.
**Expected Frequency:** Low (10-25 events/year).
**Intended Component Role:** REGIME SPECIALIST.
**Data Required:** M1 USATECHIDXUSD.
**Cross-Market Scope:** Single asset.
**Closed-Line Independence:** A completely new mechanistic family (E) not previously evaluated.
**G0 Decision:** PROMOTE

---

## 7. G0 Results
- **Evaluated:** 3
- **Promoted:** 3
- **Killed:** 0
- **Blocked:** 0

## 8. Promoted Candidates
- **CAND-G0-038:** Mid-Day Counter-Trend Reload
- **CAND-G0-039:** Structural Gap-Fill Rejection
- **CAND-G0-040:** Volatility Compression Expansion

## 9. Killed Candidates
None.

## 10. Blocked Candidates
None.

## 11. Counterfactual Quality
All three candidates possess highly specific, behaviorally distinct counterfactuals that are easily codifiable in G1/G3 without using arbitrary data shuffling. This provides a direct path to scientific falsification.

## 12. Mechanism Diversity
The candidates cover Session Transition (D), Price Repricing (B), and Volatility Transition (E).

## 13. Component Potential
All three are specifically designed as specialized, low-frequency, high-expectancy component artifacts (Event Opportunists or Regime Specialists) intended for future System Assembly, embracing the lessons learned from CAND-035.

## 14. Ranked Candidates
1. **CAND-039:** Incredible structural logic with explicitly bounded downside risk via the rejected ceiling.
2. **CAND-038:** Pure structural flow-based thesis utilizing intraday institutional schedules.
3. **CAND-040:** Strong mathematical foundation in volatility cyclicality and dealer hedging.

## 15. Exact Next Milestone
G1 — ECONOMIC PLAUSIBILITY SCREEN (CAND-038, CAND-039, CAND-040)

## 16. Integrity
No historical data was queried, scanned, or executed. No closed lines were rescued. CAND-015 logs were not inspected. No data infrastructure generation was assumed.
