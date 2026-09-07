# QUANTFORGE — RESEARCH FACTORY V2
# G1 CLOSURE — V10
# DATE: 2026-08-26

## 1. V10 Cycle Summary
The V10 G1 Economic Plausibility Screen is formally closed. The cycle yielded zero G2 candidates. Three candidates were blocked due to lack of strict data availability (proxy substitution is prohibited), and one candidate was empirically insufficient. No candidates from V10 have been promoted or retained for system assembly.

## 2. Candidate Results
- **CAND-028 (Volume Impact Exhaustion Reversal):** BLOCKED — TRUE VOLUME DATA UNAVAILABLE.
- **CAND-029 (Rates/FX Lead-Lag Dispersion):** BLOCKED — REQUIRED RATES/FX DATA UNAVAILABLE.
- **CAND-031 (Volatility/Price Decoupling):** BLOCKED — VIX / IMPLIED VOLATILITY DATA UNAVAILABLE.
- **CAND-030 (Asian Session Value Area Rejection):** INSUFFICIENT. (N = 374, Frequency = 68.20/year, Mean gross = -0.25 pips, Median gross = +7.18 pips, Friction = 1.00 pip, Mean net = -1.25 pips, Median net = +6.18 pips, Win rate = 75.13%). 

## 3. Data Blockers
**LESSON:** Missing data must produce BLOCKED, not proxy substitution.
- CAND-028 must not replace true institutional/traded volume with broker tick volume.
- CAND-029 must not substitute another rates instrument for the exact required yield proxy.
- CAND-031 must not substitute ATR/realized volatility for implied volatility.
If the registered scientific claim requires data that does not exist in the local dataset, the candidate cannot be evaluated.

## 4. CAND-030 Distribution Lesson
**LESSON:** High win rate and positive median do NOT establish positive economic expectancy.
CAND-030 is the canonical example: despite a 75.13% win rate and a +6.18 pip median net outcome, the -1.25 pip mean net expectancy renders the artifact entirely unviable. The left tail (max loser -124.10 pips) consumes the high-frequency median wins. 

## 5. Component Governance
A candidate may not become a component merely because it has a high hit rate or attractive median outcome. Component eligibility strictly requires economically credible per-event expectancy (positive mean net). A failed artifact must not be rescued by adding filters or tweaking definitions; any materially different version must be explicitly registered as a new G0 candidate.

## 6. System Assembly Status
- **CAND-024 (Friday De-Risking):** COMPONENT-CANDIDATE / RETAINED / NOT REINTRODUCED. It must not be assembled with anything yet.
- **CAND-025 (Macro Shock Reversal):** RETAINED BUT UNQUALIFIED. No G2.

## 7. CAND-015 Protection
- **CAND-015:** 7-DAY FORWARD OBSERVATION ACTIVE / PROTECTED. Its incomplete results must not be inspected.

## 8. Next G0 Principle
The next discovery cycle must deliberately diversify away from repeatedly finding:
> **HIGH WIN RATE + NEGATIVE EXPECTANCY / LEFT-TAIL REVERSAL**

The search must prioritize mechanisms where the economic thesis naturally suggests:
- Asymmetric positive payoff;
- Continuation after information arrival;
- Persistent repricing;
- Controlled adverse excursion;
- Positive expectancy rather than merely a high hit rate.
This is a generation preference to guide mechanism selection, not a rigid numerical cutoff.

## 9. Integrity
No rerun of CAND-030 was attempted. No new filters, stop-losses, or take-profits were added to rescue its negative expectancy. No proxy data was substituted. The cycle concludes strictly on the available evidence.
