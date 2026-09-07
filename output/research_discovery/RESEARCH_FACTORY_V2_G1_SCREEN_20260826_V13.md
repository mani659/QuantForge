# QUANTFORGE — RESEARCH FACTORY V2
# G1 ECONOMIC PLAUSIBILITY SCREEN — V13
# DATE: 2026-08-26

## 1. G1 Objective
Determine whether the exact frozen V13 objects create a genuinely executable post-entry economic response with plausible positive expectancy after friction, separating observed price behavior from the proposed causal mechanism.

## 2. Static Integrity
- **CAND-038:** PASS. Lunch pull-back and reload condition fully observable before 13:00 entry.
- **CAND-039:** PASS. Gap-fill rejection strictly bounded.
- **CAND-040:** PASS. ATR compression and morning breakout mathematically defined and observable before 10:30 entry.

## 3. Data Availability
All candidates successfully executed using `USATECHIDXUSD_M1.csv`.
*Note on CAND-040:* The options implied volatility (gamma positioning) data does not exist in the repository. We tested the explicit price behavior (compression -> expansion) but cannot scientifically validate the "dealer gamma" causal explanation.

## 4. CAND-038 (Mid-Day Counter-Trend Reload)
- **N:** 11 (4.38 opps/year)
- **Mean Gross:** +6.69
- **Median Gross:** -16.88
- **Mean Net:** +4.69
- **Median Net:** -18.88
- **Win Rate:** 45.45%
- **Std Dev:** 123.04
- **Best/Worst:** +304.77 / -196.43

## 5. CAND-039 (Structural Gap-Fill Rejection)
- **N:** 0 (0 opps/year)
- **Mean/Median:** N/A
- **Analysis:** The strictly defined structural rejection (touching yesterday's close but failing to exceed it by more than 0.1%, followed by a collapse below the open) never occurred in the dataset. The event is too highly constrained.

## 6. CAND-040 (Volatility Compression Expansion)
- **N:** 9 (5.14 opps/year)
- **Mean Gross:** -16.99
- **Median Gross:** -21.16
- **Mean Net:** -18.99
- **Median Net:** -23.16
- **Win Rate:** 44.44%
- **Std Dev:** 62.72
- **Best/Worst:** +94.71 / -112.49

## 7. Counterfactual Comparison
### CAND-038 Counterfactual (Lunch Extension)
- **Mean Net:** -50.34
- **Analysis:** The counterfactual descriptively validates the mechanism: a lunch extension leads to massive afternoon mean-reversion (-50.34 points), whereas the lunch pull-back (CAND-038) structurally resists it (+4.69 points). However, the absolute economics of the reload are too weak to trade.

### CAND-039 Counterfactual (Gap-Fill Accepted)
- **Mean Net:** -54.94
- **Analysis:** Gap-fills that were structurally accepted and held yielded heavy negative expectancy for shorts. Because the primary rejection condition (N=0) never triggered, a formal counterfactual comparison is impossible.

### CAND-040 Counterfactual (Expansion from Extended Vol)
- **Mean Net:** +92.21 (N=2)
- **Analysis:** The counterfactual contradicts the hypothesis. The expansion from compression yielded negative expectancy (-18.99), while the expansion from an already extended volatility regime (the presumed "exhaustion" state) yielded massive positive continuation. 

## 8. Executable Capture
- **CAND-038:** PASS. 13:00 Open execution.
- **CAND-039:** PASS. 10:30 Open execution.
- **CAND-040:** PASS. 10:30 Open execution.
All measurements used strictly post-entry data.

## 9. Friction
- **USATECHIDXUSD:** 2.0 points round-trip (Conservative baseline).

## 10. Frequency
- **CAND-038:** 4.38 opps/year.
- **CAND-039:** 0 opps/year.
- **CAND-040:** 5.14 opps/year.
All V13 candidates suffered from extreme low frequency. 

## 11. Distribution
- **CAND-038:** Positive Mean / Negative Median. Extreme right-skew reliance.
- **CAND-039:** N/A.
- **CAND-040:** Negative Mean / Negative Median.

## 12. Payoff Structure
- **CAND-038:** Payoff Ratio: 1.33. The positive mean (+4.69) is entirely dependent on a single +304 point outlier. The median is deeply negative (-18.88), indicating structural decay on a typical day. Expectancy is NOT broad-based.
- **CAND-040:** Payoff Ratio: 0.61. Downside dominates upside structurally.

## 13. Mechanism-vs-Behavior Separation
- **CAND-038:** We observed that lunch extensions mean-revert heavily, while lunch pull-backs hold up slightly better. This does not explicitly prove "institutional reloading".
- **CAND-040:** We observed that compression breakouts fail to continue intraday. The dealer gamma hypothesis could not be validated due to missing options data, and the price behavior actively contradicted the assumed continuation.

## 14. G1 Classification
- **CAND-038:** INSUFFICIENT. Despite the counterfactual outperformance, the absolute economics rely entirely on outliers (negative median).
- **CAND-039:** INSUFFICIENT. Zero events.
- **CAND-040:** INSUFFICIENT. Negative economics. Mechanism contradicted by counterfactual.

## 15. G2 Promotions
**NONE.**

## 16. Component Candidates
**NONE.**

## 17. Blocked / Insufficient / Invalid
- **CAND-038:** INSUFFICIENT.
- **CAND-039:** INSUFFICIENT.
- **CAND-040:** INSUFFICIENT.

## 18. Existing Artifact Register
- **CAND-024:** COMPONENT-CANDIDATE — RETAINED / NOT REINTRODUCED
- **CAND-035:** COMPONENT-CANDIDATE — EVENT OPPORTUNIST

## 19. CAND-015 Independence
Confirmed. No inspection or integration of CAND-015 occurred.

## 20. Integrity
Strict protocol observed. No parameters were optimized to force frequency. No unregistered proxies were used for the missing gamma data.
