# QUANTFORGE — RESEARCH FACTORY V2
# G1 ECONOMIC PLAUSIBILITY SCREEN — V16
# DATE: 2026-08-27

## 1. G1 Objective
To determine whether the exact frozen V16 candidates (CAND-047, 048, 049) produce genuine, executable, post-entry economic expectancy after realistic friction. A secondary objective is to strictly separate observed price behavior from the proposed causal mechanism to prevent assuming causal validity just because an event is profitable.

## 2. Static Integrity
- **CAND-047 (Fixing-Window Liquidity Transfer):** PASSED. Valid M1 capture.
- **CAND-048 (Sequential Macro-Release Dislocation):** PASSED. Valid M1 capture.
- **CAND-049 (Cross-Market Lead-Lag Asymmetry):** PASSED. Valid M1 capture.
No look-ahead, no MFE/future extrema substitution, no optimization.

## 3. Data Availability
- USATECHIDXUSD_M1.csv (Available locally)
- XAUUSD_M1.csv (Available locally)
- XAGUSD_M1.csv (Available locally)
**Availability:** FULL PASS for price artifact testing. However, exact dealer inventory (CAND-047), institutional consensus records (CAND-048), and cross-market order flow (CAND-049) are unobservable. The price artifacts are testable, but the underlying mechanisms remain strictly hypothesized.

## 4. CAND-047
- **N:** Treatment: 4, Counterfactual: 14
- **Opportunities/Year:** Extremely low (~2-3)
- **Mean Gross:** Not applicable (Negative expectancy)
- **Median Gross:** Not applicable
- **Mean Net:** -43.62 bps
- **Median Net:** -37.41 bps
- **Win Rate:** 0.0%
- **Verdict:** INSUFFICIENT

## 5. CAND-048
- **N:** Treatment: 0, Counterfactual: 0
- **Opportunities/Year:** 0
- **Mean Gross:** N/A
- **Median Gross:** N/A
- **Mean Net:** N/A
- **Median Net:** N/A
- **Win Rate:** N/A
- **Verdict:** INSUFFICIENT. The strict event definition (a 1% absolute move in the 08:30-09:30 pre-market hour followed by an exact touch of the 08:30 close price during the cash session) yielded zero events in the available dataset.

## 6. CAND-049
- **N:** Treatment: 0, Counterfactual: 704
- **Opportunities/Year:** 0
- **Mean Gross:** N/A
- **Median Gross:** N/A
- **Mean Net:** N/A
- **Median Net:** N/A
- **Win Rate:** N/A
- **Verdict:** INSUFFICIENT. A 1% absolute return in Gold exclusively within the single 09:30-10:30 ET window, accompanied by Silver remaining entirely flat (<0.2%), yielded zero historical events.

## 7. Counterfactual Comparison
- **CAND-047:** The treatment produced negative expectancy (-43.62 bps mean net, 0% win rate). The counterfactual produced significantly better results (-7.04 bps mean net, 57% win rate). **FLAG — CONDITION DOES NOT ADD DEMONSTRATED VALUE.**
- **CAND-048:** N=0 for both treatment and counterfactual. No comparison possible.
- **CAND-049:** Treatment yielded N=0. Counterfactual yielded N=704 (Mean Net=0.15 bps, Median Net=-3.99 bps). No comparison possible.

## 8. Executable Capture
**PASS.** All events were strictly measured from entry at the exact minute the condition was confirmed, with exits at a deterministic closing timestamp (16:00 ET). No pre-entry movement was included in the PnL.

## 9. Friction
- **USATECHIDXUSD:** 2 bps round-trip friction assumed.
- **XAGUSD / XAUUSD:** 2 bps round-trip friction assumed.
- **Rationale:** Standard conservative estimates for high-liquidity assets.

## 10. Frequency
- **CAND-047:** N=4. Extreme outlier/tail event.
- **CAND-048:** N=0. Overconstrained event definition.
- **CAND-049:** N=0. Overconstrained event definition.

## 11. Distribution
- **CAND-047:** 
  - Mean Net: -43.62 bps
  - Median Net: -37.41 bps
  - Win Rate: 0.0%
  - Standard Deviation: ~40 bps
  - 5th Percentile: -98.50 bps
  - 95th Percentile: -1.16 bps
  - Worst Trade: -98.50 bps
  - Best Trade: -1.16 bps
- **CAND-048 / 049:** N/A (Zero Events)
**FLAG:** NEGATIVE MEAN

## 12. Payoff Structure
- **CAND-047:** Outlier-dependent negative payoff. The mechanism actively destroys value relative to its counterfactual.

## 13. Mechanism vs Observed Behavior
### CAND-047
- **OBSERVED:** A 15:00 ET price drop following a large morning trend.
- **HYPOTHESIZED:** Dealers aggressively flattening intraday risk.
- **DIRECTLY MEASURABLE:** NO.

### CAND-048
- **OBSERVED:** A 09:30-11:30 price cross of the 08:30 level following an 08:30 gap.
- **HYPOTHESIZED:** Cash-session participants invalidating pre-market consensus.
- **DIRECTLY MEASURABLE:** NO.

### CAND-049
- **OBSERVED:** Silver price response following a 1% Gold shock.
- **HYPOTHESIZED:** Information diffusion / cross-market arbitrage.
- **DIRECTLY MEASURABLE:** NO.

## 14. G1 Classification
- **CAND-047:** INSUFFICIENT
- **CAND-048:** INSUFFICIENT (Zero Events)
- **CAND-049:** INSUFFICIENT (Zero Events)

## 15. G2 Promotions
**NONE.**

## 16. Component Candidates
**NONE.** No candidates produced viable per-event economics to justify retention.

## 17. Blocked / Insufficient / Invalid
- **CAND-047:** INSUFFICIENT (Negative Expectancy).
- **CAND-048:** INSUFFICIENT (Zero Events).
- **CAND-049:** INSUFFICIENT (Zero Events).

## 18. Existing Register
- **CAND-024:** COMPONENT-CANDIDATE — RETAINED / NOT REINTRODUCED
- **CAND-035:** COMPONENT-CANDIDATE — EVENT OPPORTUNIST
- **CAND-042:** COMPONENT-CANDIDATE — EVENT OPPORTUNIST / NOT SCIENTIFICALLY QUALIFIED
- **CAND-025:** RETAINED BUT UNQUALIFIED
- **CAND-032:** CLOSED — G3 INCONCLUSIVE

## 19. CAND-015 Independence
**CAND-015:** 7-DAY FORWARD OBSERVATION ACTIVE / PROTECTED. Not inspected.

## 20. Integrity
- No parameters were optimized. 
- No event definitions were modified to manufacture events for CAND-048 or CAND-049. 
- MFE/future extrema were strictly excluded. 
- The required V16 frozen definitions were exactly tested.
