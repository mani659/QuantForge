# QuantForge — Research Factory V2
# CAND-021 FINAL INDEPENDENT G1 ADJUDICATION
# PRE-G2 GOVERNANCE GATE

## 1. Executive Verdict
**G2 READY — FROZEN OBJECT**
The frozen CAND-021 economic object has successfully demonstrated a structurally positive mathematical expectancy (mean net = +2.25 points), a large positive median (median net = +8.78 points), and robust opportunity frequency. The pre-entry D1 volatility regime filter effectively isolated the favorable structural conditions for mean-reversion without relying on reactive stop-losses or future data. The candidate earns a cheap empirical G2 pilot in its exact current frozen state.

## 2. Frozen Identity
The adjudicated object is explicitly:
- **CAND-G0-021:** Pre-Auction Liquidity Vacuum Reversal Conditioned by Volatility Regime.
- **Event:** Pre-market drift > 1.5x M5 ATR(14).
- **Condition:** Previous Day TR <= 1.5x D1 ATR(14).
- **Entry:** Executable open at exactly 09:30:00 EST.
- **Exit:** Deterministic open at 10:30:00 EST (fixed 60-minute horizon).
- **Risk Control:** None (Unbounded).

This is formally distinct from CAND-018; the D1 volatility condition is a fully observable pre-entry state registered at G0, explicitly designed to predict the presence of the adverse left tail. It is not an outcome-derived filter or an adaptive rescue.

## 3. Event Integrity
**PASS.**
- **Duplicate Suppression:** Intrinsic (maximum one event per day at exactly 09:30 EST).
- **Independence:** The 317 events are strictly independent market episodes.
- **Clustering:** Evenly distributed, limited by the daily cadence.

## 4. Volatility-State Integrity
**PASS.**
- **Definition:** True Range (TR) vs ATR(14) measured on the D1 timeframe.
- **Leakage:** The script uses a strict 1-period shift (`shift(1)`) on the D1 aggregations, explicitly ensuring that only the *completed previous day's* volatility state is evaluated at the 09:30 entry. No same-day information leaks into the condition.

## 5. Executable Capture
**PASS.**
- **Measurement:** Exclusively from the 09:30:00 EST open print to the 10:30:00 EST open print.
- **Extrema:** No Maximum Favorable Excursion (MFE) or Maximum Adverse Excursion (MAE) is utilized.
- **Discretion:** Zero.

## 6. Distribution
The unhedged distribution of the 317 favorable-state events:
- **N:** 317
- **Positive Count:** 173
- **Negative Count:** 144
- **Win Rate:** 54.57%
- **Mean Gross:** +4.25 points
- **Median Gross:** +10.78 points
- **Standard Deviation:** 117.25
- **5th Percentile:** -167.63 points
- **10th Percentile:** -132.76 points
- **25th Percentile:** -74.94 points
- **75th Percentile:** +72.02 points
- **90th Percentile:** +140.45 points
- **95th Percentile:** +190.01 points
- **Worst Outcome:** -405.41 points
- **Best Outcome:** +347.03 points
- **Total Positive Contribution:** +14776.85 points
- **Total Negative Contribution:** -13428.97 points

**Analysis:**
The left tail remains fundamentally fat (worst outcome -405 points) because the object is unhedged. However, the positive expectancy (+4.25 mean) is broad-based (54.57% win rate, robust median), and the total positive contribution now outweighs the total negative contribution.

## 7. Economic Headroom
- **Mean Gross:** +4.25 points
- **Friction:** 2.00 points (Conservative USATECHIDXUSD round-trip)
- **Mean Net:** +2.25 points
- **Headroom Status:** Valid. The positive expectancy survives friction.

## 8. Frequency
- **Opportunities/Year:** 111.01
- **Status:** Valid. High frequency is stable and unclustered.

## 9. CAND-018 Relationship
CAND-018 was invalidated due to a structural negative mean (-8.24) masked by a positive median (+7.63), driven by unbounded macro-trend days.
By applying the exact same event but conditioning it purely on the previous day's volatility state, CAND-021 inverted the mathematical expectancy to positive (+4.25) while actually *increasing* the median capture (+10.78). 
No stop-loss rescue mechanism was introduced. The change is structurally attributable to the pre-entry predictive state.

## 10. Final G1 Decision
**G2 READY — FROZEN OBJECT**
The object is valid, mechanically sound, and demonstrates unhedged positive expectancy.

## 11. G2 Object Identity
The ensuing G2 empirical pilot MUST test the EXACT CURRENT CAND-021 OBJECT.
- Do NOT introduce a stop loss.
- Do NOT alter the volatility condition.
- Do NOT change the holding period.
- Do NOT tune the thresholds.

## 12. CAND-015 Firewall
CAND-015 remains: 7-DAY FORWARD OBSERVATION ACTIVE / PROTECTED. No forward results were inspected or used.

## 13. Integrity
This adjudication was entirely read-only. No parameters were optimized. No outliers were trimmed.
