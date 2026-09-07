# QUANTFORGE — RESEARCH FACTORY V2
# G4 ECONOMIC VALIDATION — CAND-G0-015

## 1. Economic Objective
Determine whether the scientifically supported conditional behavior of CAND-G0-015 remains economically viable when evaluated as a frozen, deterministic economic object after realistic execution costs.

## 2. Frozen Candidate Identity
**CAND-G0-015** — Nasdaq-Crypto Information Absorption Lag

## 3. Frozen Economic Definition
- **Event:** USATECHIDXUSD M5 return > 3 * 30-day SMA of M5 ATR.
- **Entry:** BTCUSD executed strictly at the close of the M5 anomaly bar.
- **Exit:** BTCUSD executed strictly at the close 60 minutes (12 bars) post-entry.
- **Conditioning Split:** D1 ATR < 30-day SMA (LOW) vs D1 ATR >= 30-day SMA (HIGH). State is shifted by 1 day to strictly preclude look-ahead bias.

## 4. Cost Model
- **Base Cost:** 3.0 bps round-trip transaction friction, applied equally across all events and states.
- **Stress Cost:** 6.0 bps (2x base friction).

## 5. Development Results
The first 50% chronological partition:
- **LOW VOL:** +2206.9 bps Cumulative, +9.99 bps Mean, -637.3 bps Max DD.
- **HIGH VOL:** -555.3 bps Cumulative, -1.86 bps Mean, -2533.8 bps Max DD.

## 6. Holdout Results
The second 50% chronological partition, strictly untouched prior to this stage:
- **LOW VOL:** +1423.5 bps Cumulative, +8.90 bps Mean, -823.5 bps Max DD.
- **HIGH VOL:** -3149.6 bps Cumulative, -8.75 bps Mean, -3757.5 bps Max DD.

## 7. Full-Sample Results

| Sample | State | N | Mean Net | Median Net | Win Rate | PF | Cumulative | Max DD |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| Development | LOW | 221 | +9.99 | +5.01 | 54.8% | 1.39 | +2206.9 | -637.3 |
| Development | HIGH | 298 | -1.86 | -2.84 | 47.7% | 0.96 | -555.3 | -2533.8 |
| Holdout | LOW | 160 | +8.90 | +6.35 | 53.1% | 1.33 | +1423.5 | -823.5 |
| Holdout | HIGH | 360 | -8.75 | +2.76 | 50.8% | 0.81 | -3149.6 | -3757.5 |
| Full | LOW | 381 | +9.53 | +5.08 | 54.1% | 1.36 | +3630.5 | -823.5 |
| Full | HIGH | 658 | -5.63 | -0.94 | 49.4% | 0.88 | -3704.9 | -4122.5 |

## 8. Yearly / Period Results (LOW VOL)
- **2023:** N=44, Mean = -2.59, Cum = -114.1, Max DD = -383.4
- **2024:** N=177, Mean = +13.11, Cum = +2321.0, Max DD = -637.3
- **2025:** N=118, Mean = +11.41, Cum = +1346.4, Max DD = -823.5
- **2026 (YTD):** N=42, Mean = +1.84, Cum = +77.2, Max DD = -406.4
*Observation:* The economic edge persists broadly. While 2023 was a very slight loser (-114 bps cumulatively for the year), 2024 and 2025 generated substantial, consistent returns. Drawdowns are strictly contained across all years.

## 9. Distribution / Tail Analysis
The positive economics in the LOW VOL state are structurally broad. They do not rely on a small handful of outlier winners. The win rate is solidly above 54%, and the median is cleanly positive (+5.08 bps). The most crucial feature of the LOW VOL condition is that it avoids the massive adverse left-tail drawdowns observed in the HIGH VOL state (-823 bps Max DD vs -4,122 bps Max DD).

## 10. Cost Stress
Tested exclusively at exactly 2x base friction (6.0 bps round-trip):
- **Mean Net:** +6.53 bps
- **Median Net:** +2.08 bps
- **Cumulative:** +2487.5 bps
- **Profit Factor:** 1.24
- **Max DD:** -901.4 bps
*Observation:* The LOW VOL state comfortably survives the 100% hike in transaction costs. The economic sign remains strictly positive, and the drawdown profile barely degrades.

## 11. Economic Gates
- **Base Case Positive?** Yes (+3,630 bps cumulative).
- **Holdout Gate Passed?** Yes (+1,423 bps cumulative in untouched sample).
- **Stress Case Passed?** Yes (+2,487 bps cumulative at 2x friction).

## 12. Economic Classification
**ECONOMICALLY VIABLE**
The frozen candidate cleanly passes all mandated economic, holdout, and stress gates.

## 13. G5 Recommendation
**G5 READY**

## 14. Integrity
The economic validation was performed strictly on the frozen G3 object. No thresholds, parameters, rules, or executions were modified. The holdout period remained unviolated.
