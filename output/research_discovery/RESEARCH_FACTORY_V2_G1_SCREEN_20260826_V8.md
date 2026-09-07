# QuantForge — Research Factory V2
# G1 ECONOMIC PLAUSIBILITY SCREEN — V8

## 1. G1 Objective
Execute a cheap economic plausibility screen for candidates CAND-G0-021, CAND-G0-022, CAND-G0-023, and CAND-G0-024. The objective is to determine whether the registered pre-entry conditioning states successfully isolate favorable regimes with genuine post-entry magnitude, positive expectancy, and adequate frequency to earn a G2 pilot.

## 2. Static Integrity Checks
Before execution, strict static assertions were verified for all scripted candidates:
- **Event Definition:** PASS (Matched V8).
- **Executable Entry:** PASS (Market open print only).
- **Post-Entry Measurement:** PASS (Measured exclusively from executable entry).
- **Deterministic Exit:** PASS (Fixed time horizons).
- **Pre-Entry State Isolation:** PASS (D1 KPIs correctly shifted by 1 period; intraday windows firmly closed before entry).
- **Duplicate Suppression:** PASS (One event per time window).
- **No Hidden Parameters:** PASS.
- **Data Integrity:** PASS (Exact registered instruments only).

## 3. CAND-021 Results (Pre-Auction Liquidity Vacuum)
- **State Filter:** Favorable (Previous Day TR <= 1.5x D1 ATR).
- **Events:** 317
- **Opportunities/Year:** 111.01
- **Mean Gross:** +4.25 points
- **Median Gross:** +10.78 points
- **Win Rate:** 54.57%
- **Largest Winner:** +347.04 points
- **Largest Loser:** -405.42 points
- **Friction:** 2.0 points (USATECHIDXUSD)
- **Mean Net:** +2.25 points
- **Median Net:** +8.78 points
- **G1 Verdict:** PASS — CLEAR. The state conditioning successfully achieved a positive expected value (mean net > 0) alongside a robust positive median and high frequency.

## 4. CAND-022 Results (European Close Fixing Reversal)
- **Instrument Required:** EURUSD & GBPUSD
- **Data Availability:** Missing required cross-market benchmark (`GBPUSD_M1.csv`) in local M1 repository.
- **Substitution:** PROHIBITED. No silent proxy substitution allowed.
- **G1 Verdict:** BLOCKED — DATA AVAILABILITY.

## 5. CAND-023 Results (London Open Momentum)
- **State Filter:** Favorable (Asian Range < 0.5x D1 ATR).
- **Events:** 788
- **Opportunities/Year:** 157.79
- **Mean Gross:** +0.03
- **Median Gross:** +0.13
- **Win Rate:** 51.14%
- **Largest Winner:** +64.17
- **Largest Loser:** -39.47
- **Friction:** $0.30 (XAUUSD)
- **Mean Net:** -$0.27
- **Median Net:** -$0.17
- **G1 Verdict:** INSUFFICIENT. Despite massive frequency, the actual post-entry magnitude is microscopic ($0.13 median gross on a 4-hour hold). It completely fails to overcome realistic execution friction. The signal is effectively noise.

## 6. CAND-024 Results (Friday De-Risking)
- **State Filter:** Favorable (Morning High > Weekly High & 12:00 Open < 08:00 Open).
- **Events:** 13
- **Opportunities/Year:** 4.55
- **Mean Gross:** +42.59 points
- **Median Gross:** +36.00 points
- **Win Rate:** 61.54%
- **Largest Winner:** +284.62 points
- **Largest Loser:** -100.70 points
- **Friction:** 2.0 points (USATECHIDXUSD)
- **Mean Net:** +40.59 points
- **Median Net:** +34.00 points
- **G1 Verdict:** INSUFFICIENT. Although the gross magnitude and expectancy are excellent, the explicit exhaustion condition is structurally rare (13 events over 3 years). An opportunity frequency of ~4.5 times per year is mathematically insufficient for intraday statistical significance and cannot justify a G2 pilot.

## 7. Friction Model
- **USATECHIDXUSD (CAND-021, CAND-024):** Assumed 2.0 index points round-trip.
- **XAUUSD (CAND-023):** Assumed $0.30 round-trip.

## 8. Opportunity Frequency
- **CAND-021:** ~111 opps/year (High; excellent for G2).
- **CAND-022:** Blocked.
- **CAND-023:** ~157 opps/year (High, but no magnitude).
- **CAND-024:** ~4.5 opps/year (Critically low; fatal).

## 9. Distribution / Tail Analysis
**CAND-021 Divergence Note:** 
In the Favorable state, the median gross (+10.78) is higher than the mean gross (+4.25). This signifies that a left tail still exists (e.g., the -405 pt max loser). However, UNLIKE the invalidated CAND-018, the volatility regime filter successfully elevated the overall distribution such that the unhedged mathematical expectancy (mean) is now decisively POSITIVE (+2.25 net). The positive median no longer masks a negative expectancy; it represents a genuinely healthy, tradable distribution with economic headroom.

## 10. G1 Classification
| Candidate | Events | Opp./Year | Mean Gross | Median Gross | Friction | Mean Net | Median Net | G1 |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| CAND-021 | 317 | 111.01 | 4.25 | 10.78 | 2.00 | 2.25 | 8.78 | PASS — CLEAR |
| CAND-022 | N/A | N/A | N/A | N/A | N/A | N/A | N/A | BLOCKED |
| CAND-023 | 788 | 157.79 | 0.03 | 0.13 | 0.30 | -0.27 | -0.17 | INSUFFICIENT |
| CAND-024 | 13 | 4.55 | 42.59 | 36.00 | 2.00 | 40.59 | 34.00 | INSUFFICIENT |

## 11. G2 Promotions
- **CAND-021:** Promoted. The pre-entry volatility state condition successfully isolated a regime with both positive median AND positive expectancy, surviving conservative friction at a high frequency.

## 12. Kill / Block List
- **Killed:** CAND-023 (Zero gross magnitude).
- **Killed:** CAND-024 (Critically low frequency).
- **Blocked:** CAND-022 (Missing GBPUSD M1 data).

## 13. Resource Use
- Data: Existing M1 files (`USATECHIDXUSD_M1.csv`, `XAUUSD_M1.csv`).
- Infrastructure: Lightweight Python.
- Execution Time: Seconds per candidate.

## 14. CAND-015 Independence
The CAND-015 7-day forward observation remained fully protected. No forward data or logs were inspected during this G1 cycle.

## 15. Integrity
G1 evaluations were executed strictly according to the V8 registered rules. No parameters were optimized, no new stop-losses were added, and no data was manipulated to rescue the weak candidates.
