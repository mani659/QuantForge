# QUANTFORGE — RESEARCH FACTORY V2
# G1 ECONOMIC PLAUSIBILITY SCREEN — V14
# DATE: 2026-08-26

## 1. G1 Objective
Determine whether the objective economic constraints hypothesized in V14 produce genuine, executable post-entry economic expectancy, while explicitly separating the observable price behavior from the unobservable causal narrative.

## 2. Static Integrity
- **CAND-041 (Post-OPEX Drift):** PASS. OPEX dates and Monday gap triggers mathematically defined and observable before 09:30 ET entry.
- **CAND-042 (Correlated Shock):** PASS. Cross-asset gap threshold observable strictly at 09:30 ET.
- **CAND-043 (Liquidity Vacuum):** PASS. Morning trend threshold observable at 11:30 ET.

## 3. Data Availability
All candidates executed successfully using `USATECHIDXUSD_M1.csv` and `XAUUSD_M1.csv`.
**CAUSAL DATA BLOCKERS:**
- CAND-041's "dealer gamma pinning" mechanism is UNTESTABLE (options IV/positioning data absent).
- CAND-042's "margin call / forced liquidation" mechanism is UNTESTABLE (institutional positioning data absent).
- CAND-043's "order-book depth reduction" mechanism is UNTESTABLE (Level 2 resting limit order data absent).
In all three cases, the price artifact is testable, but the proposed economic cause remains unproven narrative.

## 4. CAND-041 (Post-OPEX Unpinning Drift)
- **N:** 8 (3.54 opps/year)
- **Mean Gross:** +37.11
- **Median Gross:** -8.06
- **Mean Net:** +35.11
- **Median Net:** -10.06
- **Win Rate:** 50.00%
- **Std Dev:** 175.12
- **Best/Worst:** +409.93 / -174.83
- **Avg Win/Loss:** +173.44 / -103.22

## 5. CAND-042 (Correlated Liquidity-Shock Reversion)
- **N:** 5 (3.02 opps/year)
- **Mean Gross:** +65.20
- **Median Gross:** +230.20
- **Mean Net:** +63.20
- **Median Net:** +228.20
- **Win Rate:** 60.00%
- **Std Dev:** 415.37
- **Best/Worst:** +458.20 / -600.44
- **Avg Win/Loss:** +381.06 / -413.60

## 6. CAND-043 (European-Close Liquidity Vacuum)
- **N:** 18 (9.21 opps/year)
- **Mean Gross:** -1.80
- **Median Gross:** -16.96
- **Mean Net:** -3.80
- **Median Net:** -18.96
- **Win Rate:** 50.00%
- **Std Dev:** 179.60
- **Best/Worst:** +407.29 / -308.67
- **Avg Win/Loss:** +137.94 / -145.53

## 7. Counterfactual Comparison
### CAND-041 Counterfactual (Generic Monday Gap Continuation)
- **Mean Net:** -58.17 (Median -37.35). 
- **Descriptive Result:** Meaningful descriptive separation exists. Post-OPEX gaps (+35.11) perform vastly better than generic Monday gaps, which suffer heavy mean-reversion.

### CAND-042 Counterfactual (Divergent Shock: Tech drops, Gold holds)
- **Mean Net:** +47.76 (Median +134.52).
- **Descriptive Result:** Minimal descriptive separation. Massive NY Open drops revert heavily in both cases. The correlated shock reverts slightly harder, but sample sizes (N=5 vs N=7) are too tiny to establish a meaningful cross-market dependency over a standard reversion play.

### CAND-043 Counterfactual (11:30 Continuation after Flat Morning)
- **Mean Net:** -0.78 (Median -1.18).
- **Descriptive Result:** Meaningful descriptive separation, but backwards. The "vacuum" after a massive trend actually leads to worse performance (-3.80) than the vacuum after a flat morning, directly contradicting the continuation hypothesis.

## 8. Executable Capture
**PASS.** All measurements used strictly post-entry data.

## 9. Friction
- **USATECHIDXUSD:** 2.0 points round-trip (Conservative baseline).

## 10. Frequency
- **CAND-041:** 3.54 opps/year (Low).
- **CAND-042:** 3.02 opps/year (Extremely Low).
- **CAND-043:** 9.21 opps/year (Low).

## 11. Distribution
- **CAND-041:** Positive Mean / Negative Median. 
- **CAND-042:** Positive Mean / Positive Median.
- **CAND-043:** Negative Mean / Negative Median.

## 12. Payoff Structure
- **CAND-041:** Outlier dependent. The +35 mean relies entirely on a +409 point outlier. The median (-10.06) is negative, meaning the typical event decays.
- **CAND-042:** Broad-based positive median, though the worst-case tail (-600.44) is larger than the best-case win (+458.20).
- **CAND-043:** Symmetrical, slightly negative drift.

## 13. Mechanism vs Observed Behavior
- **CAND-041:** 
  - **OBSERVED:** Post-OPEX gaps resist mean-reversion significantly better than generic Monday gaps.
  - **HYPOTHESIZED:** Dealer gamma unpinning allows this. (Untestable).
- **CAND-042:** 
  - **OBSERVED:** Massive morning gap-downs revert violently, regardless of whether Gold drops with them or not.
  - **HYPOTHESIZED:** Margin-call forced liquidation creates the correlated drop. (Untestable).
- **CAND-043:** 
  - **OBSERVED:** Large morning trends do not systematically continue after 11:30 ET.
  - **HYPOTHESIZED:** European liquidity withdrawal enables continuation. (Untestable).

## 14. G1 Classification
- **CAND-041:** INSUFFICIENT. Negative median and extreme outlier reliance.
- **CAND-042:** COMPONENT-CANDIDATE — RETAIN. The economics are extremely positive (+63 mean / +228 median), but the sample size (N=5) is far too thin to survive chronological holdout validation in G2 as a standalone strategy. It is retained as a rare Event Opportunist.
- **CAND-043:** INSUFFICIENT. Negative economics.

## 15. G2 Promotions
**NONE.**

## 16. Component Candidates
**CAND-042 (Correlated Liquidity-Shock Reversion)** -> Retained as an Event Opportunist.

## 17. Blocked / Insufficient / Invalid
- **CAND-041:** INSUFFICIENT.
- **CAND-043:** INSUFFICIENT.

## 18. Existing Register
- **CAND-024:** COMPONENT-CANDIDATE — RETAINED / NOT REINTRODUCED
- **CAND-035:** COMPONENT-CANDIDATE — EVENT OPPORTUNIST
- **CAND-042:** COMPONENT-CANDIDATE — EVENT OPPORTUNIST

## 19. CAND-015 Independence
Confirmed. No inspection or integration of CAND-015 occurred.

## 20. Integrity
Strict execution protocol observed. Causal narratives were correctly partitioned from price reality.
