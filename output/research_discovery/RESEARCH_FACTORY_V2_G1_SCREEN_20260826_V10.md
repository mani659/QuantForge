# QUANTFORGE — RESEARCH FACTORY V2
# G1 ECONOMIC PLAUSIBILITY SCREEN — V10
# DATE: 2026-08-26

## 1. G1 Objective
Determine whether the frozen V10 G0 research artifacts (CAND-G0-028, CAND-G0-029, CAND-G0-030, CAND-G0-031) demonstrate enough executable post-entry economic magnitude and opportunity frequency to justify a cheap G2 pilot. This G1 screen strictly tests exact registered V10 objects against existing local M1 data without downsampling, proxy substitution, or parameter optimization.

## 2. Static Integrity
A static assertion was performed against all V10 candidates. The data requirements for CAND-028, CAND-029, and CAND-031 failed to match existing local datasets. Proxy substitution is strictly prohibited under V2 doctrine.

## 3. Data Availability Audit
- **CAND-028 (Volume Impact):** BLOCKED. Requires true traded institutional volume. Available local M1 data for FX/Indices contains only broker tick volume, which cannot be silently substituted for true volume shock mechanisms.
- **CAND-029 (Rates/FX Dispersion):** BLOCKED. Requires M1/M5 pricing for USDJPY and US 10-Year Yield (or TLT). These instruments are absent from the local repository.
- **CAND-031 (Volatility/Price Decoupling):** BLOCKED. Requires M5 VIX data. This is absent from the local repository. Proxy substitution (e.g., using ATR) is prohibited because the frozen mechanism explicitly relies on cross-market implied volatility decoupling.
- **CAND-030 (Asian Session Rejection):** EVALUABLE. Tested using exact EURUSD M1 data accurately aggregated to M15 boundaries as required by the mechanism.

## 4. CAND-028
- **Verdict:** BLOCKED — DATA QUALITY. True volume data unavailable.

## 5. CAND-029
- **Verdict:** BLOCKED — DATA AVAILABILITY. Required fixed-income and JPY data absent.

## 6. CAND-030
### ASIAN SESSION VALUE AREA REJECTION
- **Instrument:** EURUSD
- **Events:** 374
- **Opportunities/Year:** 68.20
- **Mean Gross:** -0.25 pips
- **Median Gross:** +7.18 pips
- **Win Rate:** 75.13%
- **Best Trade:** +34.80 pips
- **Worst Trade:** -124.10 pips
- **Standard Deviation:** 21.92 pips
- **Friction:** 1.00 pip (Conservative spread assumption)
- **Mean Net:** -1.25 pips
- **Median Net:** +6.18 pips
- **G1 Verdict:** INSUFFICIENT.

## 7. CAND-031
- **Verdict:** BLOCKED — DATA AVAILABILITY. Required VIX data absent.

## 8. Friction
- **EURUSD (CAND-030):** Assumed 1.0 pip (0.00010) round-trip friction. This is a conservative central assumption for M1/M15 session boundaries.

## 9. Frequency
- **CAND-030:** ~68 opportunities/year. This is a viable frequency for a **SESSION COMPONENT** if the economics were positive. However, the negative mean expectancy renders the frequency irrelevant.

## 10. Distribution
**CAND-030 Flag: positive median / negative mean**
The candidate presents a severe unhedged left tail. The structural logic holds true most of the time (75.13% win rate and positive +6.18 median net). However, when the Asian session boundary breaks cleanly without reversion, the directional drift destroys the expectancy. A -124.10 pip outlier forces the unhedged mathematical expectancy negative (-1.25 pips net). Consistent with the CAND-018 precedent, a positive median masking a negative mean is structurally non-viable.

## 11. Economic Plausibility
None of the V10 candidates passed the economic plausibility screen. CAND-030 suffers from a negative expected value. The others lack necessary data to evaluate.

## 12. Component Role
- **CAND-030:** Intended as a Session Component, but disqualified due to negative expectancy.

## 13. G1 Classification
- **CAND-028:** BLOCKED
- **CAND-029:** BLOCKED
- **CAND-030:** INSUFFICIENT
- **CAND-031:** BLOCKED

## 14. G2 Promotions
**NONE.**

## 15. Blocked / Killed List
- **Blocked:** CAND-028, CAND-029, CAND-031 (Data Availability/Quality).
- **Killed:** CAND-030 (Negative Expectancy / Severe Left Tail).

## 16. System Assembly Firewall
No combinations were attempted. No opportunity union was created. No system-level risk modelling or weighted backtesting occurred.

## 17. CAND-015 Independence
The CAND-015 7-day forward observation remains fully protected. Its partial forward results were not inspected or utilized.

## 18. Integrity
All findings are derived from the strict execution of frozen V10 rules. No parameters were optimized. No stop-losses were added to rescue CAND-030 from its left tail. No unauthorized proxy data was used to force evaluation of the blocked candidates.
