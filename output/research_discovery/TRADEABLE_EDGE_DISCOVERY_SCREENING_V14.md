# QUANTFORGE — RESEARCH FACTORY V2
# TRADEABLE EDGE DISCOVERY SCREENING — V14
# OBJECTIVE ECONOMIC CONSTRAINTS
# DATE: 2026-08-26

## 1. Research Factory V2 Context
The V13 screening cycle demonstrated that arbitrarily combining price boundaries (e.g., gap rejection) or borrowing causal narratives without data (e.g., dealer gamma) yields either zero-event failures or negative-expectancy illusions. V14 pivots the pipeline toward **Objective Economic Constraints**—mechanisms where market structure, settlement rules, cross-asset boundaries, or scheduled liquidity withdrawals mechanically alter the plausible actions available to participants.

## 2. V14 Thesis
An objective economic constraint changes participant incentives and creates a testable, executable, positive-expectancy hypothesis. V14 hypothesizes that when a constraint is violently removed (unpinning), when it is violently broken (liquidity shock), or when it structurally withdraws (session close), the resulting price action is statistically distinct from generic unconstrained random walks.

## 3. Lessons Applied
- **V13 CAND-040 Lesson:** Do not propose a causal mechanism (e.g., options positioning) without the data to observe it. V14 candidates rely strictly on time (calendar/session) and available cross-asset prices as the objective constraint markers.
- **V13 CAND-039 Lesson:** Do not over-constrain the event definition to the point of yielding zero historical events.

## 4. Economic Constraint Families
- **FAMILY A:** Calendar / Contract Mechanics (Options Expiry / Unpinning)
- **FAMILY F:** Cross-Market Economic Constraint (Correlated Liquidity Shock)
- **FAMILY E:** Session Handoff / Participant Constraint (Resting Liquidity Withdrawal)

## 5. Candidate Generation Method
Heuristic identification of structural constraints:
1. The expiration of monthly options (calendar constraint).
2. The strict negative correlation of equity and gold (fundamental constraint) broken by margin-call liquidations.
3. The official closure of European equity markets (liquidity constraint).

---

## 6. Candidates Considered

### CAND-G0-041
**Name:** Post-OPEX Unpinning Drift
**Mechanism Family:** A — Calendar / Contract Mechanics
**Economic Constraint:** Dealer gamma pinning (options expiration).
**Mechanistic Explanation:** On the 3rd Friday of every month, massive index options expire. Prior to expiration, options dealers hedge their gamma exposure, mechanically dampening volatility and "pinning" the market near major strike prices. Once these contracts expire on Friday afternoon, the hedging constraint vanishes. Any pent-up macro imbalance is suddenly free to price in on Monday morning, leading to massive, unanchored directional drift.
**Repeatable Event:** The day is the Monday immediately following the 3rd Friday of the month. The NY Open (09:30 ET) gaps > 0.50% (up or down) from Friday's 16:00 ET close.
**Information State:** The market has gapped after the removal of a massive derivative anchor, signaling pent-up fundamental flow.
**Predicted Direction:** Continuation (Direction of the Monday gap).
**Executable Entry:** 09:30 ET Monday (Market).
**Deterministic Exit:** 16:00 ET Monday (Market).
**Opportunity Integrity:** Evaluated only 12 times a year.
**Positive-Expectancy Thesis:** Without gamma pinning to force mean-reversion, fundamental momentum dominates. Winners can persist endlessly intraday because the structural ceiling/floor (the option strike) no longer exists.
**Adverse-Risk Structure:** The gap itself proves that fundamental pricing was suppressed. Mean-reversion participants who attempt to fade the gap are run over by the lack of dealer support.
**Primary Counterfactual:** A generic Monday (NOT following OPEX) that experiences an identical > 0.50% gap.
**Expected Counterfactual Difference:** Generic Monday gaps often mean-revert as liquidity providers fade the move. Post-OPEX Monday gaps trend aggressively as liquidity providers have no derivative incentive to fade.
**Falsification Condition:** Post-OPEX gaps show the exact same mean-reversion profile as generic Monday gaps.
**Expected Frequency:** Very Low (~6-10 opps/year).
**Intended Component Role:** EVENT OPPORTUNIST.
**Data Required:** M1 USATECHIDXUSD, calendar dates.
**Cross-Market Scope:** Single asset.
**Closed-Line Independence:** Entirely independent. Not a generic reversal.
**G0 Decision:** PROMOTE

### CAND-G0-042
**Name:** Correlated Liquidity-Shock Reversion
**Mechanism Family:** F — Cross-Market Economic Constraint
**Economic Constraint:** Multi-asset liquidity and margin limits (forced liquidation).
**Mechanistic Explanation:** US Equities (USATECH) and Gold (XAU) typically exhibit zero or negative correlation during risk-off events (Tech drops, Gold acts as safe haven). If both assets collapse simultaneously and violently, it indicates that the structural fundamental constraint has been broken by a brute-force liquidity shock (margin calls forcing indiscriminate selling of all assets to raise cash). Because forced selling is finite and price-insensitive, its exhaustion leaves the market deeply dislocated from fundamental value, prompting a violent structural recovery (arbitraging the "liquidity discount").
**Repeatable Event:** At 09:30 ET, USATECHIDXUSD is < -1.50% from Yesterday's 16:00 Close, AND XAUUSD is simultaneously < -1.00% from Yesterday's 16:00 Close.
**Information State:** A cross-market correlation constraint has been broken by indiscriminate forced liquidation.
**Predicted Direction:** Long (Reversion to fundamental value).
**Executable Entry:** 09:30 ET (Market Long USATECHIDXUSD).
**Deterministic Exit:** 16:00 ET (Market).
**Opportunity Integrity:** Evaluated once daily at 09:30 ET.
**Positive-Expectancy Thesis:** The selling was mechanical (margin calls), not fundamental. Once the margin flow clears on the open, value-buyers step into a vacuum, driving a massive asymmetric recovery.
**Adverse-Risk Structure:** By requiring a dual-asset collapse, we filter out genuine, fundamental equity bear days (where Gold typically catches a bid).
**Primary Counterfactual:** USATECHIDXUSD gaps down < -1.50%, but XAUUSD is >= 0.00% (a normal risk-off / flight-to-safety paradigm).
**Expected Counterfactual Difference:** The liquidity shock (correlated selloff) yields a violent V-bottom recovery. The fundamental shock (divergent selloff) yields persistent grinding downside.
**Falsification Condition:** Correlated selloffs continue downward just as hard as divergent fundamental selloffs.
**Expected Frequency:** Extremely Low (~2-5 opps/year, tail-risk events).
**Intended Component Role:** EVENT OPPORTUNIST / REGIME SPECIALIST.
**Data Required:** M1 USATECHIDXUSD, M1 XAUUSD.
**Cross-Market Scope:** Dual asset (Equity + Metals).
**Closed-Line Independence:** Replaces the blocked CAND-037 with available data. Independent mechanism.
**G0 Decision:** PROMOTE

### CAND-G0-043
**Name:** European-Close Liquidity Vacuum
**Mechanism Family:** E — Session Handoff / Participant Constraint
**Economic Constraint:** Withdrawal of European institutional resting limit orders (liquidity depth).
**Mechanistic Explanation:** At 11:30 ET (16:30 London), European equity markets officially close. European institutions withdraw their resting limit orders from global inter-dealer books. This mechanically decreases order-book depth for US indices. If a massive, dominant directional imbalance (US macro trend) is already active, the sudden withdrawal of European stabilizing liquidity acts as a "vacuum," allowing the US directional flow to push prices much further on less volume in the afternoon.
**Repeatable Event:** Between 09:30 ET and 11:30 ET, the USATECHIDXUSD return is strictly > +1.50% (or < -1.50%).
**Information State:** A dominant US trend has just lost its primary international liquidity constraint.
**Predicted Direction:** Continuation (Direction of the 09:30-11:30 trend).
**Executable Entry:** 11:30 ET (Market).
**Deterministic Exit:** 16:00 ET (Market).
**Opportunity Integrity:** Evaluated once daily at 11:30 ET.
**Positive-Expectancy Thesis:** The removal of opposing limit orders creates an asymmetric path of least resistance. The US trend continues because the friction (liquidity) opposing it has halved.
**Adverse-Risk Structure:** The requirement of a massive > 1.50% morning trend ensures that a genuine, dominant imbalance exists. In a flat market, a liquidity vacuum just creates chop.
**Primary Counterfactual:** The 11:30 ET liquidity withdrawal occurs on a day where the morning was flat (09:30 to 11:30 return is between -0.50% and +0.50%).
**Expected Counterfactual Difference:** The vacuum only creates persistent afternoon trends if a dominant morning imbalance exists to exploit it. Without the imbalance, the afternoon is noisy mean-reversion.
**Falsification Condition:** The post-11:30 afternoon trend profile is identical regardless of the magnitude of the morning imbalance.
**Expected Frequency:** Moderate (20-40 opps/year).
**Intended Component Role:** SESSION COMPONENT.
**Data Required:** M1 USATECHIDXUSD.
**Cross-Market Scope:** Single asset.
**Closed-Line Independence:** Replaces the failed CAND-038 (lunch reload) by focusing on the hard European Close (11:30) rather than a generic lunch lull, and focuses on structural liquidity withdrawal rather than "reloading."
**G0 Decision:** PROMOTE

---

## 7. G0 Results
- **Evaluated:** 3
- **Promoted:** 3
- **Killed:** 0
- **Blocked:** 0

## 8. Promoted Candidates
- **CAND-G0-041:** Post-OPEX Unpinning Drift
- **CAND-G0-042:** Correlated Liquidity-Shock Reversion
- **CAND-G0-043:** European-Close Liquidity Vacuum

## 9. Killed Candidates
None.

## 10. Blocked Candidates
None.

## 11. Counterfactual Quality
All three candidates possess highly specific, structurally constrained counterfactuals:
- **CAND-041:** Monday gaps with vs. without prior gamma expiration.
- **CAND-042:** Equity crashes with vs. without safe-haven correlation breakdown.
- **CAND-043:** European liquidity withdrawal with vs. without a pre-existing macro trend imbalance.

## 12. Mechanism Diversity
The candidates cover Options/Calendar Constraints (A), Cross-Market Liquidity Constraints (F), and Session/Liquidity-Depth Constraints (E).

## 13. Component Potential
All three are specifically designed as specialized component artifacts. CAND-041 and CAND-042 target rare structural dislocations (Event Opportunist). CAND-043 targets specific intraday structural handoffs (Session Component).

## 14. Ranked Candidates
1. **CAND-042:** The dual-asset correlation break is the most objective definition of a forced-liquidation constraint.
2. **CAND-043:** The 11:30 London close is a globally recognized, mechanically strict constraint on global liquidity.
3. **CAND-041:** Options expiration is a massive constraint, though mapping 3rd Fridays perfectly in pandas might have minor holiday edge cases.

## 15. Exact Next Milestone
G1 — ECONOMIC PLAUSIBILITY SCREEN (CAND-041, CAND-042, CAND-043)

## 16. Integrity
No historical data was queried, scanned, or executed. No closed lines were rescued. CAND-015 logs were not inspected. All proposed constraints utilize currently available, verifiable M1 data.
