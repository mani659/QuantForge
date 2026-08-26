# QuantForge — G0 Candidate Generation
# TRADEABLE EDGE DISCOVERY SCREENING V6

## 1. Research Factory V2 Context

Under the Research Factory V2 doctrine, QuantForge operates as an Economic-First / Cost-Aware Research Funnel. The core research objective is to investigate Conditional Market Behavior—specifically, whether a repeatable event or state transition produces an asymmetric, mathematically favorable post-event return distribution after accounting for executable friction. 

This document represents the execution of the G0 milestone for the V6 cycle, incorporating the Opportunity Integrity and Conditional Behavior lessons from V5.

## 2. G0 Objective

The objective of this screening is to identify a small number of genuinely different market mechanisms (prioritizing cross-market lead/lag, relative mispricing, and state transitions) that can be deterministically tested for economic headroom. The focus is strictly on finding conditional market behavior that can become an executable economic edge.

## 3. Candidate Generation Method

Candidates were generated conceptually by selecting distinct mechanism families (Family A, D, and E) defined in the V6 G0 brief. No data was mined, scanned, or backtested to derive these candidates. The mechanisms rely on fundamental market structure axioms (e.g., latency in information absorption, volatility state transitions) and explicitly define Opportunity Integrity parameters prior to any empirical G1 testing.

---

## 4. Candidate Cards

### CAND-G0-015
**Name:** Nasdaq-Crypto Information Absorption Lag
**Mechanism Family:** Family A (Cross-Market Lead/Lag)
**Causal Hypothesis:** Institutional equity liquidity (Nasdaq) absorbs and prices in macro risk-on/risk-off shocks almost instantly. Cryptocurrency liquidity, despite being 24/7, exhibits a brief latency in fully matching the magnitude of the equity macro shock during overlapping US hours, creating a delayed directional continuation in BTCUSD.
**Event:** USATECHIDXUSD experiences a sudden M5 directional shock (>3 times its 30-day M5 ATR).
**Event Completion:** The close of the M5 anomaly bar.
**Executable Entry:** Market order on BTCUSD at the exact close time of the USATECHIDXUSD anomaly bar.
**Direction:** In the direction of the USATECHIDXUSD M5 return.
**Deterministic Exit:** Fixed 60-minute horizon.
**Post-Entry Response:** The subsequent 60-minute directional drift of BTCUSD as it fully prices in the macro shock.
**Conditioning KPI:** The prevailing VIX/Nasdaq macro volatility regime (D1 ATR > 30-day SMA vs D1 ATR < 30-day SMA). The hypothesis is that high-volatility macro regimes produce more reliable cross-market spillovers.
**Opportunity Integrity:**
- **Onset:** USATECHIDXUSD M5 return > 3 ATR.
- **Completion:** Close of the M5 bar.
- **Re-arm / Duplicate Suppression:** Hard 60-minute lockout on BTCUSD entries.
- **Overlap Handling:** If a new Nasdaq shock occurs within the 60-minute window, it is ignored until the re-arm is met.
**Expected Frequency:** Moderate (1-3 times a week during US hours).
**Economic Headroom:** UNKNOWN.
**Cross-Market Scope:** USATECHIDXUSD (Leader) → BTCUSD (Lagging).
**Cheapest Data:** M5 synchronized.
**G1 Screen Concept:** Measure the median 60-minute post-entry return of BTCUSD conditioned on the D1 equity volatility regime, minus spread.
**Falsification Condition:** BTCUSD moves instantaneously with Nasdaq, leaving no post-entry drift, or the drift is smaller than the bid-ask spread.
**Closed-Line Independence:** Entirely new mechanism. Avoids pure mean-reversion or single-asset technicals.

---

### CAND-G0-016
**Name:** Asynchronous FX Information Arrival
**Mechanism Family:** Family E (Price-Discovery / Information Absorption)
**Causal Hypothesis:** Highly correlated cross-rates (e.g., EURUSD and GBPUSD) generally move together on USD-driven news. When one pair experiences a massive localized volatility shock while the other does not, it represents localized European/UK news. The lagging pair will eventually absorb the cross-rate adjustment (EURGBP repricing) through a sympathetic directional drift.
**Event:** EURUSD H1 True Range exceeds 2 standard deviations of its 30-day mean, WHILE GBPUSD H1 True Range remains strictly below 1 standard deviation.
**Event Completion:** The close of the H1 bar meeting the divergence condition.
**Executable Entry:** Market order on GBPUSD at the close of the H1 event bar.
**Direction:** In the direction of the EURUSD H1 return.
**Deterministic Exit:** Fixed 4-hour horizon.
**Post-Entry Response:** The sympathetic directional adjustment of GBPUSD over the next 4 hours.
**Conditioning KPI:** Time of Day (London Session vs. NY Session). The hypothesis is that liquidity asymmetry during NY hours delays the GBPUSD adjustment longer than during London hours.
**Opportunity Integrity:**
- **Onset:** Divergent H1 volatility expansion.
- **Completion:** Close of the divergent H1 bar.
- **Re-arm / Duplicate Suppression:** Both pairs must record an H1 True Range below their respective 1 SD thresholds for 4 consecutive hours before a new event can trigger.
- **Overlap Handling:** New shocks during the 4-hour re-arm window are ignored.
**Expected Frequency:** Low to Moderate (news-driven).
**Economic Headroom:** UNKNOWN.
**Cross-Market Scope:** EURUSD (Leader) → GBPUSD (Lagging).
**Cheapest Data:** H1.
**G1 Screen Concept:** Measure the 4-hour forward return of GBPUSD following an asynchronous EURUSD shock, conditioned by session.
**Falsification Condition:** GBPUSD does not consistently drift in the EURUSD direction, or the EURGBP cross absorbs the entire imbalance instantly via arbitrage.
**Closed-Line Independence:** Avoids the closed Session Range Expansion (DISC-024) by relying on relative cross-pair divergence rather than absolute time-of-day expansion.

---

### CAND-G0-017
**Name:** Macro Compression Breakout Continuation
**Mechanism Family:** Family D (State Transition)
**Causal Hypothesis:** Prolonged, extreme volatility compression indicates a lack of market consensus. When a breakout finally occurs, it forces structural re-pricing and stop-loss cascades. Breakouts that align with the historical pre-compression trend are hypothesized to have a strong asymmetric continuation compared to counter-trend false breaks.
**Event:** XAUUSD transitions from extreme D1 compression (Bollinger Band Width < 10th percentile over 252 days) to an H4 structural breakout (H4 close outside the D1 Bollinger Bands).
**Event Completion:** The close of the H4 breakout bar.
**Executable Entry:** Market order on XAUUSD at the close of the H4 breakout bar.
**Direction:** In the direction of the H4 breakout.
**Deterministic Exit:** Fixed 3-day (72-hour) horizon.
**Post-Entry Response:** The multi-day sustained directional movement.
**Conditioning KPI:** Pre-compression macro trend (D1 200-SMA slope is positive vs. negative). Breakouts aligning with the 200-SMA slope should have a higher mathematical expectancy.
**Opportunity Integrity:**
- **Onset:** D1 BB Width < 10th percentile, followed by H4 close outside D1 BB.
- **Completion:** H4 close.
- **Re-arm / Duplicate Suppression:** Price must re-enter the bands, revert to the H4 20-SMA, and close completely inside the moving average envelope before a new breakout is recognized.
- **Overlap Handling:** Hard suppression of any further H4 closes outside the band until the re-arm is fully met.
**Expected Frequency:** Low.
**Economic Headroom:** UNKNOWN.
**Cross-Market Scope:** XAUUSD.
**Cheapest Data:** H4 / D1.
**G1 Screen Concept:** Measure the 72-hour deterministic return of the breakout, separated by alignment with the pre-compression trend, against a realistic friction barrier.
**Falsification Condition:** Compression breakouts revert to the mean instantly, making them false breakouts regardless of macro trend alignment.
**Closed-Line Independence:** This is a breakout/trend-initiation hypothesis, distinct from Mean Reversion (DISC-021) or Volatility Reset (CAND-013).

---

## 5. Opportunity Integrity
All three candidates explicitly define an event onset, completion, re-arm condition, and duplicate suppression logic.
- CAND-015 uses a hard 60-minute lockout.
- CAND-016 uses a 4-hour baseline volatility reset requirement.
- CAND-017 uses a structural mean-reversion reset (touching H4 20-SMA).
This prevents event cascades and overlapping measurement windows.

## 6. Conditional-Behavior Logic
- CAND-015 tests if macro volatility state influences cross-market lag.
- CAND-016 tests if session liquidity (London vs NY) dictates information absorption speed.
- CAND-017 tests if pre-compression trend alignment dictates breakout continuation.
None of these KPIs are arbitrary data-mined filters; they represent structural liquidity and momentum axioms.

## 7. Economic Headroom
All three candidates have UNKNOWN conceptual economic headroom and require G1 screening to evaluate if the directional asymmetry overcomes bid-ask friction.

## 8. Closed-Line Review
- No candidate attempts to rescue Mean Reversion (DISC-021) or TSMOM (DISC-022).
- No candidate is a superficial variant of CAND-012 or CAND-013.
- The mechanisms explore Lead/Lag, FX Asymmetry, and State Transitions, which are new to the Research Factory.

## 9. Candidate Ranking
1. **CAND-G0-016** (Asynchronous FX Information Arrival) - High causal clarity, cleanly testable.
2. **CAND-G0-015** (Nasdaq-Crypto Information Absorption Lag) - Excellent cross-market logic, but M5 synchronization may introduce slight complexity.
3. **CAND-G0-017** (Macro Compression Breakout Continuation) - Classic mechanism, but lower expected frequency.

## 10. G0 Decisions
- **CAND-G0-015:** PROMOTE TO G1
- **CAND-G0-016:** PROMOTE TO G1
- **CAND-G0-017:** PROMOTE TO G1

## 11. Proposed G1 Screens
- Deterministic extraction of CAND-015 on M5 data (USATECHIDXUSD/BTCUSD).
- Deterministic extraction of CAND-016 on H1 data (EURUSD/GBPUSD).
- Deterministic extraction of CAND-017 on H4 data (XAUUSD).

## 12. Integrity
No historical data was scanned. No backtests were run. No tick data was touched. No parameters were optimized.

## 13. Next Milestone
**G1 — ECONOMIC PLAUSIBILITY SCREEN**
