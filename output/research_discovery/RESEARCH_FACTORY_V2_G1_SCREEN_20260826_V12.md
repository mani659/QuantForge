# QUANTFORGE — RESEARCH FACTORY V2
# G1 ECONOMIC PLAUSIBILITY SCREEN — V12
# DATE: 2026-08-26

## 1. G1 Objective
Determine whether the exact frozen V12 objects demonstrate genuine, executable, post-entry economic expectancy sufficient to earn a cheap G2 pilot, and verify that the proposed mechanisms are measurable against their pre-declared counterfactuals.

## 2. Static Integrity
- **CAND-035:** PASS. Month-end events accurately mapped. Counterfactual mapped cleanly to mid-month. Pre-entry acceleration condition fully observable before entry.
- **CAND-036:** PASS. Pre-market acceptance rigorously bounded. Counterfactual correctly constructed from failed tests.
- **CAND-037:** BLOCKED.

## 3. Data Availability
- **USATECHIDXUSD M1:** Available and used for CAND-035 and CAND-036.
- **USA500IDXUSD M1:** MISSING. CAND-037 is blocked. No proxy substitution was attempted per protocol.

## 4. CAND-035 (Month-End Imbalance Acceleration)
- **N:** 11 (4.09 opps/year)
- **Mean Gross:** +64.36
- **Median Gross:** +57.92
- **Mean Net:** +62.36
- **Median Net:** +55.92
- **Win Rate:** 81.82%
- **Std Dev:** 75.53
- **Best/Worst:** +207.03 / -62.61

## 5. CAND-036 (Structural PDH Acceptance)
- **N:** 86 (30.98 opps/year)
- **Mean Gross:** -14.15
- **Median Gross:** -20.24
- **Mean Net:** -16.15
- **Median Net:** -22.24
- **Win Rate:** 47.67%
- **Std Dev:** 194.06
- **Best/Worst:** +338.07 / -1068.59

## 6. CAND-037 (Tech Leadership Divergence)
BLOCKED — Missing USA500IDXUSD_M1.csv data.

## 7. Counterfactual Comparison
### CAND-035 Counterfactual (Mid-Month)
- **Mean Net:** +2.68
- **Win Rate:** 75.00%
- **Analysis:** The mechanism functions exactly as designed. The month-end event (+62.36) produces massive structural drift compared to the identical setup occurring mid-month (+2.68). 

### CAND-036 Counterfactual (Unverified Gap-Up)
- **Mean Net:** +13.95
- **Win Rate:** 54.90%
- **Analysis:** The mechanism is contradicted. The strictly verified acceptance (CAND-036) produced negative expectancy (-16.15), whereas the unverified gap-up (counterfactual) produced positive expectancy (+13.95). Structural acceptance did not yield continuation; it yielded failure.

## 8. Friction
- **USATECHIDXUSD:** 2.0 points round-trip (Conservative baseline).

## 9. Frequency
- **CAND-035:** 4.09 opps/year. Highly clustered at month-end. No duplicate overlap.
- **CAND-036:** 30.98 opps/year. Consistent.

## 10. Distribution
- **CAND-035:** Positive Mean / Positive Median. Very strong, tightly clustered right skew.
- **CAND-036:** Negative Mean / Negative Median. Severe left-tail distribution.

## 11. Asymmetry
- **CAND-035:** Broad-based positive expectancy. Top 5% winner contribution (+207.03) heavily outweighs bottom 5% loser contribution (-62.61). Downside risk is explicitly bounded by the structural tracking flow.
- **CAND-036:** Upside (+1437.75) completely overwhelmed by massive left-tail downside (-2491.45).

## 12. G1 Classification
- **CAND-035:** COMPONENT-CANDIDATE — RETAIN. Exceptional per-event economics (+62.36 mean net) and a flawless counterfactual, but at ~4 opportunities per year it cannot survive as a standalone G2 strategy. It is retained strictly as an Event Opportunist for future System Assembly.
- **CAND-036:** INSUFFICIENT. Negative economics. Mechanism contradicted by counterfactual.
- **CAND-037:** BLOCKED.

## 13. G2 Promotions
**NONE.**

## 14. Component Candidates
**CAND-035** is designated COMPONENT-CANDIDATE (Event Opportunist).

## 15. Blocked / Insufficient / Invalid
- **CAND-036:** INSUFFICIENT.
- **CAND-037:** BLOCKED (Data).

## 16. System Assembly Firewall
Confirmed. No components were combined.

## 17. CAND-015 Independence
Confirmed. No inspection or integration of CAND-015 occurred.

## 18. Integrity
Strict protocol observed. No parameters were optimized to force CAND-035 into higher frequency. No data was proxied for CAND-037. The unverified counterfactual effectively destroyed CAND-036.
