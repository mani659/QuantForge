# QUANTFORGE — RESEARCH FACTORY V2
# G1 ECONOMIC PLAUSIBILITY SCREEN — V15
# DATE: 2026-08-26

## 1. G1 Objective
Determine whether the V15 frozen objects (CAND-044, CAND-045, CAND-046) produce a genuine executable post-entry economic response with plausible positive expectancy after friction. Explicitly separate observed price behavior from proposed causal mechanisms, evaluating the discriminating power of their formal counterfactuals.

## 2. Static Integrity
**PASS.** All candidates were strictly evaluated according to their frozen V15 definitions using deterministic entry/exit timestamps. No future information, MFE, or post-hoc optimizations were utilized.

## 3. Data Availability
**PASS.** Evaluated using available local M1 OHLCV for USATECHIDXUSD and XAUUSD.
**CAVEAT:** Institutional flow, true order-book depth, and stop-loss execution data are unavailable. Causal mechanisms invoking these factors remain inherently untestable.

## 4. CAND-044 (Initial Balance Trap Liquidation)
- **Events (N):** 4
- **Opportunities/Year:** 2.27
- **Mean Gross:** -38.20
- **Median Gross:** -122.04
- **Mean Net:** -40.20
- **Median Net:** -124.04
- **Win Rate:** 25.00%
- **Friction:** 2.0
- **Payoff Ratio:** 1.81

## 5. CAND-045 (Safe-Haven Confirmed Risk-Off)
- **Events (N):** 7
- **Opportunities/Year:** 3.03
- **Mean Gross:** +72.34
- **Median Gross:** +50.44
- **Mean Net:** +70.34
- **Median Net:** +48.44
- **Win Rate:** 85.71%
- **Friction:** 2.0
- **Payoff Ratio:** 0.56

## 6. CAND-046 (Opening Print Capitulation Pivot)
- **Events (N):** 33
- **Opportunities/Year:** 12.04
- **Mean Gross:** -11.67
- **Median Gross:** -11.55
- **Mean Net:** -13.67
- **Median Net:** -13.55
- **Win Rate:** 45.45%
- **Friction:** 2.0
- **Payoff Ratio:** 0.97

## 7. Counterfactual Comparison
### CAND-044 Counterfactual (Tight IB Range Break)
- **Treatment Net (N=4):** -40.20 (Mean) / -124.04 (Median)
- **CF Net (N=208):** -7.68 (Mean) / -1.49 (Median)
- **Result:** Trapping a large morning trend performs *worse* than breaking a tight morning range, directly contradicting the forced liquidation hypothesis.

### CAND-045 Counterfactual (Unconfirmed Equity Selloff)
- **Treatment Net (N=7):** +70.34 (Mean) / +48.44 (Median)
- **CF Net (N=21):** +95.88 (Mean) / +71.60 (Median)
- **Result:** While confirmed macro panics are highly profitable (85% win rate), *unconfirmed* panics are actually *more* profitable and more frequent. Safe-haven confirmation provides a high win rate but actively filters out massive standalone equity plunges.

### CAND-046 Counterfactual (Chop Crossing Open)
- **Treatment Net (N=33):** -13.67 (Mean) / -13.55 (Median)
- **CF Net (N=33):** +25.27 (Mean) / +29.11 (Median)
- **Result:** Crossing the Open after a large excursion yields negative expectancy, while crossing it in a tight chop range yields positive expectancy. This explicitly contradicts the structural capitulation hypothesis.

## 8. Executable Capture
**PASS.** Return measurement correctly began exactly at the entry timestamps for all candidates.

## 9. Friction
**PASS.** Conservative 2.0 points per round trip applied uniformly.

## 10. Frequency
All candidates exhibited very low frequency (2 to 12 opps/year).

## 11. Distribution
- **CAND-044:** Extreme negative median (-124).
- **CAND-045:** Broad-based positive distribution (both mean and median strongly positive, high win rate).
- **CAND-046:** Symmetrical negative distribution (mean and median identical).

## 12. Payoff Structure
- **CAND-044:** Negative expectancy.
- **CAND-045:** High win rate (85%) masks a low payoff ratio (0.56) due to a constrained right tail.
- **CAND-046:** Negative expectancy.

## 13. Mechanism vs Behavior
### CAND-044
> **OBSERVED:** Breaking the extreme of a massive morning trend yields strong negative drift (the break often fails).
> **HYPOTHESIZED:** Trapped trend-followers produce forced liquidation. (Contradicted by data).

### CAND-045
> **OBSERVED:** Equity crashes confirmed by Gold strength drift lower into the close with a high win rate, but unconfirmed equity crashes drift lower *with greater magnitude*.
> **HYPOTHESIZED:** Broad macro risk-off liquidation drives persistent selloffs without mean-reversion. (Data shows unconfirmed equity-specific shocks are actually more aggressive).

### CAND-046
> **OBSERVED:** Price crossing the Opening Print after a massive excursion tends to revert, failing to generate continuation momentum.
> **HYPOTHESIZED:** Participants are forced to unwind underwater accumulated inventory. (Contradicted by data).

## 14. G1 Classification
- **CAND-044:** INSUFFICIENT (Negative expectancy).
- **CAND-045:** INSUFFICIENT (Counterfactual outperforms treatment; the constraint actively reduces the economic capture).
- **CAND-046:** INSUFFICIENT (Negative expectancy).

## 15. G2 Promotions
**NONE.**

## 16. Component Candidates
**NONE.**

## 17. Blocked / Insufficient / Invalid
All three candidates are INSUFFICIENT.

## 18. Existing Register
- **CAND-024:** COMPONENT-CANDIDATE — RETAINED / NOT REINTRODUCED
- **CAND-035:** COMPONENT-CANDIDATE — EVENT OPPORTUNIST
- **CAND-042:** COMPONENT-CANDIDATE — EVENT OPPORTUNIST / NOT SCIENTIFICALLY QUALIFIED

## 19. CAND-015 Independence
**PASS.** CAND-015 was fully protected. Incomplete forward results were not inspected.

## 20. Integrity
No optimization or parameter tuning occurred. The results decisively prove the value of rigorous counterfactual benchmarking: hypotheses that sound mechanistically perfect often fail completely when confronted with empirical price action and their direct counterfactuals.
