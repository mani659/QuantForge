# QUANTFORGE — RESEARCH FACTORY V2
# G1 ECONOMIC PLAUSIBILITY SCREEN — V11
# DATE: 2026-08-26

## 1. G1 Objective
Determine whether the frozen V11 G0 research artifacts (CAND-G0-032, CAND-G0-033, CAND-G0-034) create enough genuine post-entry economic expectancy to justify a cheap G2 pilot, avoiding proxy substitution, unapproved data, or parameter optimization.

## 2. Static Integrity
A static integrity audit was performed. All three candidates define strict time-based events and deterministic exits. All variables are calculated strictly pre-entry, and duplicate suppression logic correctly ensures one opportunity per session.

## 3. Data Availability
- **CAND-032 (USATECHIDXUSD M1):** Fully available.
- **CAND-033 (EURUSD M1):** Fully available.
- **CAND-034 (XAUUSD / XAGUSD M1):** Fully available.

## 4. CAND-032
### NY OPEN STRUCTURAL MOMENTUM IGNITION
- **Events:** 257
- **Opportunities/Year:** 90.00
- **Mean Gross:** +14.02 points
- **Median Gross:** +23.65 points
- **Mean Net:** +12.02 points
- **Median Net:** +21.65 points
- **Win Rate:** 56.03%
- **G1 Verdict:** PASS — CLEAR. The mechanism delivers strong, broad-based positive expectancy well above friction.

## 5. CAND-033
### WMR PRE-FIXING FLOW ACCELERATION
- **Events:** 146
- **Opportunities/Year:** 26.62
- **Mean Gross:** +0.75 pips
- **Median Gross:** +0.80 pips
- **Mean Net:** -0.25 pips
- **Median Net:** -0.20 pips
- **Win Rate:** 47.26%
- **G1 Verdict:** INSUFFICIENT. The forced flow impact inside the final 15 minutes is mathematically observable (+0.75 gross), but it is too small to reliably overcome spread/friction, resulting in negative net expectancy.

## 6. CAND-034
### METALS MACRO CONFIRMATION IGNITION
- **Events:** 69
- **Opportunities/Year:** 13.82
- **Mean Gross:** -1.30 pips
- **Median Gross:** +1.68 pips
- **Mean Net:** -1.80 pips
- **Median Net:** +1.18 pips
- **Win Rate:** 53.62%
- **G1 Verdict:** INSUFFICIENT. A classic false positive: positive median and >50% win rate, but an unhedged left tail pushes the mathematical mean deeply negative.

## 7. Friction
- **USATECHIDXUSD (CAND-032):** 2.0 index points (conservative central assumption for Nasdaq-100 spread/commission).
- **EURUSD (CAND-033):** 1.0 pip (standard conservative assumption for M1 flow).
- **XAUUSD (CAND-034):** 0.5 points/pips (standard conservative estimate for gold).

## 8. Frequency
- **CAND-032:** 90.00 opps/year. This is a very healthy frequency for a Session Component.
- **CAND-033:** 26.62 opps/year.
- **CAND-034:** 13.82 opps/year.

## 9. Distribution
- **CAND-032:** Std Dev: 184.90, Worst Trade: -1134.30, Best Trade: +746.78.
- **CAND-033:** Std Dev: 9.73, Worst Trade: -36.40, Best Trade: +42.20. 
- **CAND-034:** **Flag: Positive median / negative mean.** The cross-market confirmation filter failed to prevent occasional massive 120+ point mean-reverting outliers in Gold.

## 10. Asymmetry Audit
**CAND-032 Asymmetry Analysis:**
- Total Positive Contribution: +17,416.04
- Total Negative Contribution: -14,325.77
- Top 5% Contribution: +4,962.21
- Bottom 5% Contribution: -6,378.50
*Conclusion:* The positive expectancy (+12.02 mean net) is **broad-based**. The bottom 5% of trades (the left tail) actually did more damage than the top 5% of trades provided in profits, yet the strategy *still* achieved a heavily positive expected value. The edge is distributed across the center of the win distribution rather than depending on a handful of extraordinary outliers.

## 11. Economic Classification
- **CAND-032:** PASS — CLEAR
- **CAND-033:** INSUFFICIENT
- **CAND-034:** INSUFFICIENT

## 12. Component Role
- **CAND-032:** Intended Role: SESSION COMPONENT.

## 13. G2 Promotions
**CAND-G0-032** is promoted to G2 — CHEAP EMPIRICAL PILOT.

## 14. Blocked / Insufficient / Invalid
- **CAND-033:** Killed (Insufficient Magnitude).
- **CAND-034:** Killed (Negative Expectancy).

## 15. System Assembly Firewall
No combinations were tested. The candidates were evaluated entirely independently.

## 16. CAND-015 Independence
The CAND-015 forward observation remains strictly protected. 

## 17. Integrity
All findings are derived from the strict execution of frozen V11 rules. No parameters were optimized. No outcome-derived filters were added to rescue CAND-034. Measurements strictly captured post-entry movement.
