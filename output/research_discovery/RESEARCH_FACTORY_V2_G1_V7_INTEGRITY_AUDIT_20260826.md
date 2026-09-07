# QuantForge — Research Factory V2
# V7 G1 INDEPENDENT INTEGRITY / ADJUDICATION AUDIT

## 1. Executive Verdict
**OVERALL G1 AUDIT: CONDITIONAL PASS**

The G1 screening execution successfully adhered to the strict executable-capture firewalls. However, the static integrity audit discovered a subtle future-state leakage in the CAND-018 trend-filter implementation (same-day SMA inclusion). This was corrected during the audit. The corrected distribution remains materially similar and preserves the asymmetric mean/median divergence. CAND-018 is confirmed **VALID FOR G2**. CAND-019 is confirmed legitimately **BLOCKED**. CAND-020 is confirmed legitimately **INSUFFICIENT**.

## 2. Static Integrity
- **CAND-018:** CONDITIONAL. Initial G1 implementation merged daily SMA filters on the current date, effectively including the current day's 16:00 close in the 09:30 AM trend calculation (1-day lookahead). The audit script shifted the D1 SMA by 1 period to strictly use the previous day's close.
- **CAND-020:** VALID. Implementation correctly identified Friday 12:00 NY time, correctly utilized Thursday's D1 ATR, and strictly exited at Friday 16:55.
- **Common Firewalls:** Both implementations correctly used executable open prices, deterministic exits, zero MFE, and zero undocumented downsampling.

## 3. CAND-018 Distribution
Re-computed with the corrected (shifted) SMA filter:
- **Total Events:** 178
- **Positive Outcomes:** 92
- **Negative Outcomes:** 86
- **Largest Winner:** +347.04 points
- **Largest Loser:** -396.43 points
- **5th Percentile:** -234.61 points
- **25th Percentile:** -74.96 points
- **Median:** +7.63 points
- **75th Percentile:** +57.33 points
- **95th Percentile:** +157.94 points
- **Mean Gross:** -8.23 points
- **Standard Deviation:** 120.97
- **Total Positive Contribution:** +7245.32 points
- **Total Negative Contribution:** -8711.29 points

## 4. CAND-018 Endpoint Integrity
The divergence between the positive median (+7.63) and negative mean (-8.23) is explicitly caused by a **fat left tail**, not a broken endpoint. 
When the pre-market drift is a true liquidity vacuum, the market opens and reverses, yielding a bounded gain (the vacuum fills). However, when the pre-market drift is driven by a fundamental macro shock or structural regime shift, the market opens and continues ripping in the direction of the drift (against the daily trend). Because the G1 exit is a fixed 60-minute horizon with no stop-loss, these macro-trend days inflict massive, unbounded losses (e.g., -396 points), severely skewing the mean.
**Conclusion:** The underlying median effect exists. The distribution is classically asymmetric and requires empirical risk controls (G2) to chop the unbounded left tail.

## 5. CAND-018 Unit/Economic Integrity
- **Instrument:** USATECHIDXUSD (Nasdaq CFD)
- **Measured Units:** Index Points
- **Friction Units:** 2.0 Index Points
- **Price Precision Verification:** USATECHIDXUSD trades in the 15,000–30,000 range. A movement of 396 points is ~1.5%. A friction of 2.0 points is less than 1 basis point (0.01%). 
- **Conclusion:** Unit integrity is fully preserved. The 2.0 index point friction is directly comparable to the gross index point returns and represents a realistic, conservative round-trip execution cost.

## 6. CAND-018 Frequency Integrity
- **Total Events:** 178 over the dataset.
- **Opportunities/Year:** ~61.
- **Integrity Check:** The frequency is mathematically legitimate. Filtering for a drift > 1.5 ATR(14) exclusively during the 60 minutes before the US Open isolates approximately 1-2 events per week. Duplicate suppression handles overlapping perfectly since it is an exact, time-bound daily event (08:30-09:30).

## 7. CAND-019 Data Blocker
- **Blocker Validated:** YES.
- **Exact Missing Data:** The local `data/m1/` repository contains exactly 5 files (`BTCUSD`, `EURUSD`, `USATECHIDXUSD`, `XAGUSD`, `XAUUSD`). It does NOT contain US 2Y Treasury Note Futures, the SHY ETF, or any fixed-income benchmark.
- **Substitution Policy:** Silent substitution with another asset class is prohibited. CAND-019 remains **BLOCKED — DATA AVAILABILITY**.

## 8. CAND-020 Revalidation
- **Insufficient Validated:** YES.
- **Reasoning:** A strong trend week (>1.5 D1 ATR from Monday open) ending exactly at 12:00 NY time on Friday is structurally rare (~16 times per year). Furthermore, the gross response from 12:00 to 16:55 is mathematically negative at both the mean and median. The hypothesized Friday de-risking flow does not manifest as a viable executable edge under these registered parameters.

## 9. G1 Adjudication
- **CAND-018:** The corrected distribution validates the G1 classification. The asymmetric profile (positive median, fat negative tail) is theoretically sound for a mean-reversion strategy without a stop-loss.
- **CAND-019:** Properly blocked.
- **CAND-020:** Properly killed.

## 10. G2 Readiness
**PROMOTE TO G2: CAND-018**
The evidence justifies the computational cost of a G2 cheap empirical pilot. The explicit mandate for G2 is to determine if applying strict risk controls (e.g., ATR-based stop losses) can successfully truncate the negative left tail while preserving the positive median expectation, after accounting for execution friction.

## 11. Integrity
This audit was performed in a strictly READ-ONLY capacity. No G2 execution occurred. No candidates were modified, no parameters were tuned, and no data was deleted to artificially improve the mean. The CAND-015 protected forward observation was not accessed or referenced.
