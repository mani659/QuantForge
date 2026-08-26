# QUANTFORGE — RESEARCH FACTORY V2
# CAND-G0-015 G2 INTEGRITY + ADJUDICATION AUDIT

## 1. Executive Verdict
**VALID — PROMOTION EARNED**
The G2 conditional asymmetry is a valid, reproducible consequence of the frozen candidate definition. All economic and structural constraints were respected. The underlying event is identical across states, and the pre-entry volatility condition correctly predicts a structural divergence in return distributions.

## 2. G2 Identity
**CAND-G0-015** — Nasdaq-Crypto Information Absorption Lag

## 3. Frozen Candidate Trace
- **Event Definition:** 3x ATR shock on M5 Nasdaq.
- **Entry/Exit:** 100% deterministic (M5 close to 60-min forward close).
- **Lockout:** 60-minute lockout successfully suppressed overlapping anomalies.
- **Cost Application:** 3.0 bps round-trip applied exactly once per event. No exclusions were made after calculating results.

## 4. Conditional-State Integrity
- **Logic:** `D1 ATR < 30-day SMA` versus `D1 ATR >= 30-day SMA`.
- **Integrity:** The state is calculated using D1 data and explicitly shifted by 1 day (`shift(1)`). The condition is strictly pre-entry, outcome-blind, and immune to future leakage. No results-based state selection occurred.

## 5. Development/Holdout Integrity
- **Logic:** A strict chronological 50/50 split of the full dataset.
- **Integrity:** The split is purely deterministic and outcome-blind. The holdout period remained entirely untouched during development, and no parameters were optimized or selected using holdout data.

## 6. Distribution Analysis
**High-Vol Holdout Divergence (Mean = -8.75 bp vs Median = +2.76 bp):**
- The median is positive because slightly more than half the events win.
- The mean is deeply negative due to a massive left-tail skew. The Average Win is +75.06 bp, but the Average Loss is -95.40 bp.
- There were 46 large negative observations (< -100 bp).
- The largest 5% of losses accounted for ~30% of all losing PnL. The largest 10% accounted for ~43%. The high volatility state produces extreme adverse tail events that destroy expectancy.

**Low-Vol Stability:**
- Mean = +9.53 bp, Median = +5.08 bp.
- The top 5% of winners contribute only 19% of the total winning PnL.
- The positive expectancy is structurally distributed across the sample, not dominated by a few massive outliers.

## 7. Temporal Stability
- The low-volatility effect persisted strongly across multiple periods.
- 2024 and 2025 provided the largest aggregate performance, but 2026 YTD remains positive (+1.84 bp mean).
- The development mean (+9.99 bp) and holdout mean (+8.90 bp) are nearly identical.

## 8. Event Independence
- The ~260 valid events per year are genuinely independent opportunities, strictly enforced by the 60-minute lockout. There are no artificially repeated clusters of overlapping bars inflating the event count.

## 9. Economic Headroom
- The friction calculation (3.0 bps and 6.0 bps) was applied correctly and identically to both states. The low-volatility state possesses genuine economic headroom (+6.53 bps net at doubled friction). No hidden cost advantages were assigned.

## 10. Unsupported Claims
- The G2 report correctly used the phrase "materially significant" rather than "statistically significant." However, no formal scientific inference, t-test, or bootstrap was actually performed in G2. Any assumption of formal statistical significance is currently **UNSUPPORTED** and must be tested in G3.

## 11. G2 Adjudication
**VALID — PROMOTION EARNED**

## 12. G3 Recommendation
**G3 READY — SCIENTIFIC VALIDATION**

## 13. Integrity
The G2 result is a scientifically valid representation of one event + one executable object conditioned by one pre-registered state variable. No optimization occurred.
