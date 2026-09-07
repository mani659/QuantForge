# QUANTFORGE — RESEARCH FACTORY V2
# G1 ECONOMIC PLAUSIBILITY SCREEN — V18
# DATE: 2026-08-27

## 1. G1 Objective
Determine whether the exact frozen V18 artifacts satisfy the four G0 requirements (mechanism-specific condition, meaningful counterfactual, positive economic headroom, sufficient observability) when tested against historical M1 data.

## 2. Frozen Identity
- **CAND-G0-053:** Friday Cash-Close Settlement Reversion
- **CAND-G0-054:** Post-Shock Volatility Absorption
- **CAND-G0-055:** Initial Balance False Breakout

## 3. Static Integrity
All candidates PASSED static integrity checks. Events, entries, and exits were completely deterministic. No look-ahead, MFE, or future extrema were utilized.

## 4. Data Availability
- **PRICE ARTIFACT TESTABILITY:** YES. (All mechanisms were explicitly defined using available USATECHIDXUSD M1 price/volume constructs).
- **PROPOSED MECHANISM OBSERVABILITY:** NO. (The causal mechanisms—institutional weekend flattening for CAND-053, institutional absorption for CAND-054, and trapped momentum capital for CAND-055—remain unobservable in price data).

## 5. CAND-053 (Friday Cash-Close Settlement Reversion)
- **N:** 3
- **Opportunities/Year:** ~1
- **Mean Gross:** -1.75 bps
- **Median Gross:** -10.89 bps
- **Friction:** 2 bps round-trip
- **Mean Net:** -3.75 bps
- **Median Net:** -12.89 bps
- **Win Rate:** 33.3%
- **Counterfactual Mean/Median:** -4.99 bps / 0.98 bps
- **Verdict:** INSUFFICIENT — NEGATIVE EXPECTANCY / EVIDENCE-LIMITED

## 6. CAND-054 (Post-Shock Volatility Absorption)
- **N:** 0
- **Opportunities/Year:** 0
- **Mean Gross:** N/A
- **Median Gross:** N/A
- **Friction:** 2 bps round-trip
- **Mean Net:** N/A
- **Median Net:** N/A
- **Win Rate:** N/A
- **Counterfactual Mean/Median:** -77.29 bps / -86.99 bps
- **Verdict:** INSUFFICIENT — ZERO FREQUENCY

## 7. CAND-055 (Initial Balance False Breakout)
- **N:** 210
- **Opportunities/Year:** ~70-100
- **Mean Gross:** +19.93 bps
- **Median Gross:** +18.98 bps
- **Friction:** 2 bps round-trip
- **Mean Net:** +17.93 bps
- **Median Net:** +16.98 bps
- **Win Rate:** 61.9%
- **Counterfactual Mean/Median:** +23.65 bps / +18.68 bps
- **Verdict:** INSUFFICIENT — COUNTERFACTUAL SUPERIOR

## 8. Counterfactual Comparison
- **CAND-053:** Treatment (-3.75 bps) vs Counterfactual (-4.99 bps). **SIMILAR.** (Neither has positive economic headroom, sample size is negligible).
- **CAND-054:** N=0. No comparison possible.
- **CAND-055:** Treatment (+17.93 bps) vs Counterfactual (+23.65 bps). **COUNTERFACTUAL SUPERIOR.** The explicit "false breakout" mechanism actively degrades the opportunity compared to fading simple price approaches to the IB boundary.

## 9. Counterfactual Superiority Gate
- **CAND-053:** FAILED (No statistical separation, negative absolute economics).
- **CAND-054:** FAILED (Zero treatment events).
- **CAND-055:** FAILED (Counterfactual Superior).

## 10. Absolute Economic Headroom
Only CAND-055 demonstrated meaningful absolute economic headroom (+17.93 bps), but it failed the Counterfactual Gate. CAND-053 had negative absolute economics.

## 11. Executable Capture
**PASS.** All events were strictly measured from the deterministic post-confirmation entry.

## 12. Friction
- **Instrument:** USATECHIDXUSD
- **Cost:** 2 bps round-trip.
- **Rationale:** Standard conservative estimate for highly liquid index products.

## 13. Frequency
- **CAND-053:** EVIDENCE-LIMITED (N=3).
- **CAND-054:** EVIDENCE-LIMITED (N=0).
- **CAND-055:** HIGH (N=210).

## 14. Distribution
- **CAND-055 (Only statistically significant candidate):** Mean Net (+17.93), Median Net (+16.98). 5th Percentile: ~ -100 bps, 95th Percentile: ~ +120 bps. Best Trade: +209.13, Worst Trade: -239.06. Average Win: +57.88, Average Loss: -46.98. **BROAD-BASED POSITIVE EXPECTANCY.**

## 15. Payoff Structure
- **CAND-055:** Broad-based (Pos Contrib: 7524.40, Neg Contrib: -3758.68). Not reliant on a single outlier.

## 16. Mechanism vs Price Behavior
### CAND-053
- **OBSERVED:** Friday afternoon price reversions following a >1.5% trend.
- **HYPOTHESIZED:** Weekend settlement forced liquidation.
- **DIRECTLY OBSERVABLE:** NO.

### CAND-054
- **OBSERVED:** A 0.8% shock followed by a tightly contained 30m range.
- **HYPOTHESIZED:** Institutional absorption of aggressive shock flow.
- **DIRECTLY OBSERVABLE:** NO.

### CAND-055
- **OBSERVED:** A pierce of the IB boundary followed by a close back inside.
- **HYPOTHESIZED:** Liquidation of trapped momentum breakout capital.
- **DIRECTLY OBSERVABLE:** NO.

## 17. G1 Classification
- **CAND-053:** INSUFFICIENT (Negative Expectancy / Evidence-Limited)
- **CAND-054:** INSUFFICIENT (Zero Frequency)
- **CAND-055:** INSUFFICIENT (Counterfactual Superior)

## 18. G2 Promotions
**NONE.**

## 19. Component Candidates
**NONE.** While CAND-055 had excellent absolute economics, its counterfactual was superior. A profitable treatment with a more profitable counterfactual is NOT a qualifying mechanism artifact.

## 20. Existing Register
- **CAND-024:** COMPONENT-CANDIDATE — RETAINED / NOT REINTRODUCED
- **CAND-035:** COMPONENT-CANDIDATE — EVENT OPPORTUNIST
- **CAND-042:** COMPONENT-CANDIDATE — EVENT OPPORTUNIST / NOT SCIENTIFICALLY QUALIFIED
- **CAND-025:** RETAINED BUT UNQUALIFIED
- **CAND-032:** CLOSED — G3 INCONCLUSIVE

## 21. CAND-015 Independence
**CAND-015:** 7-DAY FORWARD OBSERVATION ACTIVE / PROTECTED. Not inspected.

## 22. Integrity
- No parameters were optimized or relaxed.
- MFE/future extrema were strictly excluded.
- The required V18 frozen definitions were exactly tested.
