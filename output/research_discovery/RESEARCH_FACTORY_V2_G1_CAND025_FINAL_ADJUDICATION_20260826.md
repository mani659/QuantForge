# QuantForge — Research Factory V2
# CAND-025 G1 FINAL ADJUDICATION
# 2026-08-26

## 1. Executive Verdict
**HOLD**
The underlying mechanistic hypothesis (macro shock causing a liquidity void that subsequently mean-reverts) is directionally correct and observable without look-ahead bias. However, the resulting +1.25 mean net expectancy is extremely thin relative to the massive ~50-point standard deviation of the post-entry distribution. It is economically too fragile to justify an immediate G2 pilot in its current, unhedged form, though the core mechanism remains scientifically interesting.

## 2. Macro Event Timing
**PASS.**
- **Observable Macro Event:** Occurs at 08:30:00 EST (e.g. CPI/NFP release).
- **Condition Completion:** 08:35:00 EST (when the 08:30–08:34:59 M5 bar closes).
- **Signal Known:** 08:35:00 EST.
- **Executable Entry:** 08:35:00 EST (The precise open of the next M5 bar).
- **Measurement:** Gross return is measured strictly from the 08:35:00 open to the 09:30:00 open. 

## 3. Event Integrity
**PASS.**
The 157 events represent distinct, independent macro-shock occurrences. Duplicate suppression is implicitly enforced by the strict time window (only evaluating the single 08:30 M5 bar each day).

## 4. Timestamp / Look-Ahead
**PASS.**
- Timestamps are properly tz-localized to US/Eastern.
- Entry occurs at the 08:35 open, mathematically guaranteeing the 08:30 bar's close and True Range are fully realized before entry. 
- No future session information, MFE, or extreme tracking was used.

## 5. Executable Capture
**PASS.**
The +3.25 mean gross return is measured entirely *after* the initial 08:30–08:35 macro shock has concluded. The trade does not erroneously capture the macro candle itself.

## 6. Distribution
The full distribution of the 157 independent events reveals a massive variance profile:
- **Positive Count:** 82
- **Negative Count:** 75
- **Win Rate:** 52.23%
- **Mean Net:** +1.25 points
- **Median Net:** +2.64 points
- **Std Dev:** 49.74 points
- **5th Percentile:** -74.24 points
- **10th Percentile:** -62.77 points
- **25th Percentile:** -25.82 points
- **75th Percentile:** +30.75 points
- **90th Percentile:** +60.77 points
- **95th Percentile:** +74.59 points
- **Best Trade:** +188.58 points
- **Worst Trade:** -157.70 points
**Analysis:** The distribution is highly symmetric and broad-based (median slightly exceeds the mean). The positive expectancy is not the result of a few lucky outliers. However, the extreme standard deviation demonstrates the massive unhedged risk inherent in trading immediately post-shock.

## 7. Economic Margin
The +1.25 mean net is **TOO FRAGILE FOR G2**. 
A mean net of 1.25 against a standard deviation of ~50 provides an exceptionally low signal-to-noise ratio. A minor increase in friction (e.g. from 2.0 to 3.0 points due to widened post-CPI spreads) or execution slippage would instantly obliterate the expectancy. While the phenomenon exists, the unhedged structural execution is not economically robust enough for a live pilot.

## 8. Frequency
**PASS.**
Frequency is confirmed at 157 events (approximately 55 opportunities per year). This corresponds closely to the schedule of major US economic data releases (CPI, PPI, NFP, GDP, Fed decisions), validating that the candidate is capturing intended macroeconomic shocks rather than random noise.

## 9. Mechanism Integrity
**PASS.**
The frozen object correctly evaluates the sequence: *macro shock → liquidity void → reversal behavior*. The +3.25 gross margin is strictly the post-shock mean reversion drift as liquidity theoretically refills the void.

## 10. G2 Object Identity
**NOT APPLICABLE (HOLD).**
If this concept is ever revisited, it must remain the exact frozen object. Any attempt to add a stop-loss or filter to tame the ~50-point standard deviation would constitute a new G0 candidate.

## 11. Final G1 Decision
**HOLD**

## 12. CAND-015 Firewall
CAND-015's 7-Day Forward Observation remains entirely isolated, protected, and its incomplete forward results were not inspected or utilized during this G1 adjudication.

## 13. Integrity
All timing bounds and distributions were independently audited without modifying the frozen candidate rules or introducing arbitrary parameter changes.
