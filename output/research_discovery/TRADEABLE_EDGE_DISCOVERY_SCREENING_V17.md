# QUANTFORGE — RESEARCH FACTORY V2
# TRADEABLE EDGE DISCOVERY SCREENING — V17
# DATE: 2026-08-27

## 1. Research Factory Context
The V16 G1 cycle demonstrated that hypotheses relying on unobservable variables (e.g., dealer inventory, unmeasurable institutional consensus) or overconstrained price sequences often fail empirical screening due to zero observable events or negative expectancy. V17 restores the factory to G0 with a strict mandate to isolate mechanisms that are directly, objectively measurable in existing data.

## 2. V17 Objective
To discover tradeable artifacts where the mechanism variable is itself observable, utilizing price relationships, measurable range/volatility structures, or documented reference transitions. The goal is to find mechanisms whose presence demonstrably changes post-entry economics relative to a close counterfactual, avoiding untestable causal stories.

## 3. Lessons from V16
- **Unobservable Variables Fail:** If we cannot measure dealer gamma, order-book depth, or macro-consensus shifts, we cannot rely on them as G0 constraints.
- **Overconstraint Extinguishes Opportunity:** Requiring exact ticks (e.g., touching the exact 08:30 open after a 1% excursion) guarantees zero events. We must use robust, measurable zones or ranges.

## 4. Observable-Mechanism Principle
The V17 pipeline requires that the exact variable defining the economic constraint must be calculable directly from available M1 OHLCV data. 

## 5. Mechanism Families
- **FAMILY C:** Reference-Price Acceptance (Observable price anchor acceptance/rejection)
- **FAMILY A:** Observable Price Parity (Measurable cross-market relationship deviations)
- **FAMILY D:** Session Participant Transition (Measurable volatility state transition across known participant windows)

## 6. Candidates Considered

### CAND-G0-050
**Name:** Cash-Session PDH Liquidity Sweep
**Mechanism Family:** C — Reference-Price Acceptance
**Observable Mechanism Variable:** The exact price level of the Previous Day's High (PDH).
**Economic Constraint:** The PDH is a universally observable liquidity pool (buy stops). A genuine breakout expands; a liquidity sweep pierces it just enough to trigger resting stops, then violently rejects, leaving breakout buyers structurally trapped.
**Mechanistic Explanation:** Momentum algorithms and retail participants place buy-stops just above the PDH. When price breaches the PDH slightly but fails to hold (reversing back below), it confirms the move was a stop-run by larger participants rather than a genuine breakout. The trapped longs are forced to liquidate, accelerating a reversal.
**Repeatable Event:** Between 09:30 and 15:00 ET, price pierces the exact PDH by more than 0.05% but less than 0.25% (the observable sweep). Within 15 minutes of the peak, price closes back below the exact PDH level.
**Information State:** An observable liquidity sweep has occurred and the breakout has explicitly failed.
**Predicted Post-Entry Behavior:** Continuation downward (Short) as trapped buyers liquidate.
**Executable Entry:** The close of the 1-minute bar that crosses back below the PDH (Market Short).
**Deterministic Exit:** 16:00 ET (Market).
**Opportunity Integrity:** Evaluated continuously intraday; single trigger per day (first cross).
**Positive-Expectancy Thesis:** Forced liquidation is price-insensitive. Once the PDH rejection is confirmed, trapped longs must sell to close, providing a strong directional tailwind.
**Adverse-Risk Structure:** The rejection could be a temporary pullback before a true breakout. However, the strict requirement of an immediate close back below the PDH filters out strong structural breakouts.
**Primary Counterfactual:** Price approaches within 0.1% of the PDH but strictly fails to pierce it, then reverses downward.
**Expected Counterfactual Difference:** Reversing *near* the highs traps nobody. Reversing *after* a sweep explicitly traps breakout capital. The sweep should yield significantly higher negative momentum.
**Falsification Condition:** Reversals following a PDH sweep perform identically to (or worse than) reversals that simply approach the PDH without breaching it.
**Expected Frequency:** Moderate (~30-50 opps/year).
**Data Required:** M1 USATECHIDXUSD (with Daily PDH calculation).
**Intended Component Role:** EVENT OPPORTUNIST.
**Closed-Line Independence:** Distinct from CAND-036 (which tested pre-market gap acceptance). This tests intraday liquidity sweeps.
**G0 Decision:** PROMOTE

### CAND-G0-051
**Name:** Precious Metals Ratio Dislocation
**Mechanism Family:** A — Observable Price Parity
**Observable Mechanism Variable:** The XAUUSD / XAGUSD return ratio.
**Economic Constraint:** Gold and Silver share a deeply linked macro-economic foundation. If Silver experiences a violent, isolated liquidity shock while Gold remains entirely stable, the structural parity is broken by non-fundamental flow.
**Mechanistic Explanation:** When XAGUSD crashes but XAUUSD remains flat, the deviation is driven by an isolated Silver liquidation event rather than a genuine macro risk-off regime. Because the overarching macro environment (Gold) hasn't changed, industrial arbitrageurs and value buyers will step in to restore the historical price parity.
**Repeatable Event:** Between 09:30 and 11:30 ET, XAUUSD moves between -0.2% and +0.2% (stable macro). Simultaneously, XAGUSD drops > 1.5% (isolated liquidity shock).
**Information State:** An explicitly observable, isolated dislocation in the precious metals ratio has occurred without macro sponsorship.
**Predicted Post-Entry Behavior:** XAGUSD recovers to restore the ratio (Long XAG).
**Executable Entry:** 11:30 ET (Market Long XAGUSD).
**Deterministic Exit:** 16:00 ET (Market).
**Opportunity Integrity:** Evaluated once daily at 11:30 ET.
**Positive-Expectancy Thesis:** Arbitrage capital is explicitly incentivized to close the statistical dislocation. The lack of Gold movement proves the Silver drop is unsupported by broader macro forces.
**Adverse-Risk Structure:** Silver can trend independently due to industrial news. However, massive 1.5% isolated shocks are typically liquidity-driven and overextended.
**Primary Counterfactual:** Between 09:30 and 11:30 ET, XAUUSD drops > 1.0% AND XAGUSD drops > 1.5%.
**Expected Counterfactual Difference:** A sponsored shock (Gold also dropping) implies a genuine macro regime shift, where Silver will likely continue trending lower. The isolated shock (treatment) should mean-revert aggressively.
**Falsification Condition:** Isolated Silver shocks trend downward just as relentlessly as macro-sponsored Silver shocks.
**Expected Frequency:** Low to Moderate (~15-30 opps/year).
**Data Required:** M1 XAUUSD, M1 XAGUSD.
**Intended Component Role:** CROSS-MARKET COMPONENT / REGIME SPECIALIST.
**Closed-Line Independence:** Entirely independent. Focuses on observable ratio dislocations rather than sequential information diffusion (CAND-049).
**G0 Decision:** PROMOTE

### CAND-G0-052
**Name:** Lunch-Window Volatility Contraction Breakout
**Mechanism Family:** D — Session Participant Transition
**Observable Mechanism Variable:** The high-low range of the 11:30-13:00 ET period.
**Economic Constraint:** The structural withdrawal of institutional volume during the NY lunch hour creates an observable volatility contraction.
**Mechanistic Explanation:** When the 11:30-13:00 ET window exhibits an extremely tight range, it confirms a complete withdrawal of directional participation. As full institutional desks return at 13:00 ET, any immediate breakout from this tight constraint represents fresh, unified afternoon directional flow.
**Repeatable Event:** The High-to-Low range from 11:30 to 13:00 ET is strictly < 0.25% (an observable extreme volatility contraction). Between 13:00 and 14:00 ET, price breaks the 11:30-13:00 High (or Low).
**Information State:** A highly constrained period of liquidity withdrawal has ended, and new directional institutional flow has explicitly triggered a breakout.
**Predicted Post-Entry Behavior:** Continuation in the direction of the breakout.
**Executable Entry:** The exact minute the 11:30-13:00 High (or Low) is broken (Market).
**Deterministic Exit:** 16:00 ET (Market).
**Opportunity Integrity:** Evaluated daily. Single trigger.
**Positive-Expectancy Thesis:** Breaking out of a mathematically verified volatility contraction means the market is transitioning from an inactive state to an active directional state, providing a clean path of least resistance into the close.
**Adverse-Risk Structure:** Breakouts can be faded. But explicitly waiting for a verified lunch contraction ensures the breakout is driven by returning participants rather than just random chop.
**Primary Counterfactual:** The 11:30-13:00 ET High-to-Low range is wide (> 0.60%). Price then breaks the high/low of that wide range between 13:00 and 14:00 ET.
**Expected Counterfactual Difference:** Breaking out of an extreme, observable liquidity contraction triggers fresh directional momentum. Breaking out of a wide, unconstrained range is just normal continuation and is highly prone to mean-reversion exhaustion.
**Falsification Condition:** Breakouts from tight lunch contractions perform identically to breakouts from wide, volatile lunch ranges.
**Expected Frequency:** Moderate (~30-50 opps/year).
**Data Required:** M1 USATECHIDXUSD.
**Intended Component Role:** SESSION COMPONENT.
**Closed-Line Independence:** Focuses explicitly on a measurable volatility state transition (range width) rather than a simple time-of-day momentum reload (CAND-038).
**G0 Decision:** PROMOTE

## 7. G0 Results
- **Evaluated:** 3
- **Promoted:** 3
- **Killed:** 0
- **Blocked:** 0

## 8. Promoted Candidates
- **CAND-G0-050:** Cash-Session PDH Liquidity Sweep
- **CAND-G0-051:** Precious Metals Ratio Dislocation
- **CAND-G0-052:** Lunch-Window Volatility Contraction Breakout

## 9. Killed Candidates
None.

## 10. Blocked Candidates
None.

## 11. Observable-Mechanism Quality
- **CAND-050:** The PDH level and the <0.25% sweep depth are perfectly observable mathematically.
- **CAND-051:** The differential return between Gold and Silver is perfectly observable.
- **CAND-052:** The high-low range of the lunch window is perfectly observable.

## 12. Counterfactual Quality
- **CAND-050:** Close approach vs. explicit sweep (Trapped capital vs no trapped capital).
- **CAND-051:** Correlated shock vs. Isolated shock (Macro sponsored vs non-sponsored).
- **CAND-052:** Wide-range breakout vs. Contraction breakout (Exhausted momentum vs fresh momentum).
All three counterfactuals represent highly specific, mechanically distinct states.

## 13. Mechanism Diversity
The candidates cover Reference-Price Acceptance (C), Observable Price Parity (A), and Session Participant Volatility Transition (D).

## 14. Component Potential
All three are specifically designed as specialized component artifacts. CAND-050 targets intraday liquidity events (Event Opportunist). CAND-051 targets cross-market parity breaks (Cross-Market Component). CAND-052 targets specific session handoffs (Session Component).

## 15. Ranked Candidates
1. **CAND-051 (Precious Metals Ratio Dislocation):** Structural parity between Gold and Silver is one of the most robust observable mechanisms in macro finance.
2. **CAND-052 (Lunch-Window Volatility Contraction Breakout):** Mechanically sound, highly observable volatility state transition.
3. **CAND-050 (Cash-Session PDH Liquidity Sweep):** Structurally strong, but exact sweep tolerances (0.05% to 0.25%) may require careful empirical observation to ensure sufficient event frequency.

## 16. Exact Next Milestone
G1 — ECONOMIC PLAUSIBILITY SCREEN (CAND-050, CAND-051, CAND-052)

## 17. Integrity
No historical data was queried, scanned, or executed. No closed lines were rescued. CAND-015 logs were not inspected. All proposed constraints utilize currently available, verifiable M1 data. System Assembly was not performed.
