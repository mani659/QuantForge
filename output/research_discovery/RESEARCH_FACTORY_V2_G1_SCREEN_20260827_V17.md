# QUANTFORGE — RESEARCH FACTORY V2
# G1 ECONOMIC PLAUSIBILITY SCREEN — V17
# DATE: 2026-08-27

## 1. G1 Objective
To determine whether each exact frozen V17 artifact produces a genuine, executable, post-entry economic response that survives realistic friction and possesses meaningful separation from its registered counterfactual. Crucially, G1 must separate observed price behavior from the proposed SMC/economic narrative, which remains untestable with price data alone.

## 2. Frozen Identity
- **CAND-G0-050:** Cash-Session PDH Liquidity Sweep
- **CAND-G0-051:** Precious Metals Ratio Dislocation
- **CAND-G0-052:** Lunch-Window Volatility Contraction Breakout

## 3. Static Integrity
All candidates PASSED static integrity checks. No undocumented filters, no MFE lookahead, and no future extrema were used. All variables are derived exactly as specified in the V17 definitions, and return measurement begins strictly on the first close after execution.

## 4. Data Availability
- `USATECHIDXUSD_M1.csv`, `XAUUSD_M1.csv`, and `XAGUSD_M1.csv` are available locally.
- **Blockers:** While the price artifacts are perfectly testable, the proposed causal mechanisms (trapped stop liquidity for CAND-050, industrial arbitrage flow for CAND-051, and institutional order execution for CAND-052) remain structurally unobservable.

## 5. CAND-050 (Cash-Session PDH Liquidity Sweep)
- **N:** 49
- **Opportunities/Year:** ~15-25
- **Mean Gross:** 28.15 bps
- **Median Gross:** 10.78 bps
- **Friction:** 2 bps round-trip
- **Mean Net:** 26.15 bps
- **Median Net:** 8.78 bps
- **Win Rate:** 59.2%
- **Counterfactual Mean/Median:** 39.86 bps / 28.57 bps
- **Verdict:** INSUFFICIENT — COUNTERFACTUAL SUPERIOR

## 6. CAND-051 (Precious Metals Ratio Dislocation)
- **N:** 1
- **Opportunities/Year:** <1
- **Mean Gross:** -7.20 bps
- **Median Gross:** -7.20 bps
- **Friction:** 2 bps round-trip
- **Mean Net:** -9.20 bps
- **Median Net:** -9.20 bps
- **Win Rate:** 0.0%
- **Counterfactual Mean/Median:** 275.87 bps / 275.87 bps
- **Verdict:** INSUFFICIENT — ZERO FREQUENCY (N=1)

## 7. CAND-052 (Lunch-Window Volatility Contraction Breakout)
- **N:** 248
- **Opportunities/Year:** ~80-120
- **Mean Gross:** 2.01 bps
- **Median Gross:** 1.54 bps
- **Friction:** 2 bps round-trip
- **Mean Net:** 0.01 bps
- **Median Net:** -0.46 bps
- **Win Rate:** 48.8%
- **Counterfactual Mean/Median:** -23.42 bps / -20.80 bps
- **Verdict:** INSUFFICIENT — FLAT EXPECTANCY

## 8. Counterfactual Comparison
- **CAND-050 (PDH Sweep):** The treatment (explicitly sweeping the PDH) produced +26.15 bps mean net. However, the counterfactual (approaching the PDH without piercing it) produced +39.86 bps mean net. The liquidity sweep condition actively degrades the opportunity. **COUNTERFACTUAL SUPERIOR.**
- **CAND-051 (Ratio Dislocation):** With N=1, no statistical comparison is possible. 
- **CAND-052 (Lunch Contraction Breakout):** The treatment (+0.01 bps mean net) vastly outperformed the counterfactual (-23.42 bps mean net). The volatility contraction condition successfully filtered out severe negative-expectancy chop. **TREATMENT CLEARLY SUPERIOR.** However, the absolute return is entirely flat.

## 9. Executable Capture
**PASS.** All events were strictly measured from entry at the exact minute the condition was confirmed, with exits at a deterministic closing timestamp (16:00 ET).

## 10. Friction
- **USATECHIDXUSD:** 2 bps round-trip.
- **XAGUSD / XAUUSD:** 2 bps round-trip.
- **Rationale:** Standard conservative estimates for highly liquid assets.

## 11. Frequency
- **CAND-050:** Moderate (N=49)
- **CAND-051:** Rare (N=1)
- **CAND-052:** High (N=248)

## 12. Distribution
- **CAND-050:** Pos Mean (+26.15), Pos Median (+8.78). 5th: -93.40, 95th: +120+ bps (Estimated). Best: +204.88, Worst: -93.40.
- **CAND-051:** N=1.
- **CAND-052:** Flat Mean (+0.01), Neg Median (-0.46). 5th: -100+ bps, 95th: +100+ bps. Best: +218.07, Worst: -205.27.

## 13. Payoff Structure
- **CAND-050:** Broad-based positive (Pos Contrib: 1763, Neg Contrib: -482).
- **CAND-051:** N/A.
- **CAND-052:** Perfectly flat. Pos Contrib (5401) is identical to Neg Contrib (-5399).

## 14. Counterfactual Superiority Gate
- **CAND-050:** FAILED. Condition does not add value.
- **CAND-051:** N/A (N=1).
- **CAND-052:** PASSED. Condition actively improves economics relative to counterfactual, though absolute economics remain flat.

## 15. Mechanism vs Price Behavior
### CAND-050
- **OBSERVED:** A 0.05%-0.25% pierce of the PDH followed by a reversal close.
- **HYPOTHESIZED:** Retail stop-runs and trapped breakout capital.
- **DIRECTLY OBSERVABLE:** NO.

### CAND-051
- **OBSERVED:** A 1.5% drop in Silver while Gold is flat.
- **HYPOTHESIZED:** Isolated liquidity shock followed by arbitrage repricing.
- **DIRECTLY OBSERVABLE:** NO.

### CAND-052
- **OBSERVED:** A <0.25% range during the 11:30-13:00 window.
- **HYPOTHESIZED:** Complete withdrawal of institutional order flow.
- **DIRECTLY OBSERVABLE:** NO.

## 16. G1 Classification
- **CAND-050:** INSUFFICIENT
- **CAND-051:** INSUFFICIENT
- **CAND-052:** INSUFFICIENT

## 17. G2 Promotions
**NONE.**

## 18. Component Candidates
**NONE.** No candidates produced viable per-event economics to justify retention. CAND-050 is profitable but its counterfactual is superior. CAND-052 passes the counterfactual gate but its absolute per-event economics are too flat.

## 19. Existing Register
- **CAND-024:** COMPONENT-CANDIDATE — RETAINED / NOT REINTRODUCED
- **CAND-035:** COMPONENT-CANDIDATE — EVENT OPPORTUNIST
- **CAND-042:** COMPONENT-CANDIDATE — EVENT OPPORTUNIST / NOT SCIENTIFICALLY QUALIFIED
- **CAND-025:** RETAINED BUT UNQUALIFIED
- **CAND-032:** CLOSED — G3 INCONCLUSIVE

## 20. CAND-015 Independence
**CAND-015:** 7-DAY FORWARD OBSERVATION ACTIVE / PROTECTED. Not inspected.

## 21. Integrity
- No parameters were optimized.
- MFE/future extrema were strictly excluded.
- The required V17 frozen definitions were exactly tested.
