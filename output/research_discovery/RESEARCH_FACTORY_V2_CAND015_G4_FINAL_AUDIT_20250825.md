# QUANTFORGE — RESEARCH FACTORY V2
# CAND-G0-015 G4 FINAL ECONOMIC AUDIT

## 1. Executive Verdict
**VALID — G5 READY**
The G4 Economic Validation successfully implemented a frozen translation of the scientifically supported CAND-015 object. No economic assumptions were hidden, accounting is mathematically flawless, and the chronological holdout boundaries were strictly respected. The classification of "ECONOMICALLY VIABLE" is structurally correct.

## 2. Identity Chain
- **Event Definition:** 3x M5 ATR shock. Intact.
- **Entry/Exit:** 60-minute deterministic hold. Intact.
- **Volatility State:** D1 ATR < 30d SMA with 1-day `shift()`. Intact.
- **Lockout:** 60-minute chronological suppression. Intact.
- **Friction:** 3.0 bps. Intact.
The identity chain from G0 through G3 has not been compromised by any G4-specific economic tuning.

## 3. Trade Accounting
The script employs `gross = (exit - entry) / entry * 10000` mapped against direction, followed immediately by `net = gross - friction`.
- Returns are strictly calculated on executable close-prices.
- Friction is fully integrated into every trade exactly once.
- There are no slippage benefits or favorable execution assumptions.

## 4. Cost Model
- **Base Cost:** 3.0 bps round-trip transaction friction correctly subtracted from the gross return of every trade regardless of volatility regime. 
- **Stress Cost:** 6.0 bps (exactly 2x friction) correctly applied in the stress validation. Costs are never subtracted twice.

## 5. Development/Holdout Integrity
The script mechanically sliced the chronologically sorted trade array into two precise 50/50 halves (`iloc[:mid_idx]` and `iloc[mid_idx:]`). 
- No date selection or year-based trimming occurred.
- The holdout period remained strictly untouched by parameter optimization because there were no parameters optimized in G4.

## 6. Economic Gate
The "ECONOMICALLY VIABLE" classification is accurately applied. The object:
- Produced a positive base case.
- Remained structurally positive in the holdout.
- Remained positive at 2x friction.

## 7. Profit Factor
- Calculated as `abs(wins.sum() / losses.sum())` where `wins` are `net > 0` and `losses` are `net <= 0`. 
- Zero-net trades are appropriately classified as losses. 
- Costs are correctly included.

## 8. Cumulative Return
Calculated as the simple additive sum of `net` basis points (`cumsum()`).
- Reported +3630.5 bp (LOW) and -3704.9 bp (HIGH) precisely match the accounting logic.
- No compounding was silently applied to inflate figures.

## 9. Drawdown
Drawdown logic uses an exact chronological running sequence: `cum - cum.cummax()`. 
- The resulting max drawdown is the true realized equity peak-to-trough absolute basis point drop. 
- It correctly does not reset at year boundaries.

## 10. Temporal Stability
**Objective Evidence:** The LOW-VOL condition yields positive aggregate returns across the development (+2206.9 bps) and holdout (+1423.5 bps) partitions. Annual analysis reveals a negative period in 2023 (N=44, Cum=-114.1 bps), but strong positive consistency in 2024, 2025, and 2026 YTD. The overall effect remains structurally stable despite the localized 2023 dip.

## 11. Tail Dependence
The economics do not rely on massive outlier windfalls. The median is cleanly positive (+5.08 bps), the win rate is >54%, and as validated in G3, the top 5% of winners contribute <20% of the aggregate PnL. The economics are generated through a broad baseline advantage.

## 12. High-Vol Comparator
The HIGH-VOL state is perfectly constructed as the absolute complement (`>= 30d SMA`) to the LOW-VOL state, ensuring the scientific comparator remains untampered.

## 13. Stress Case
The 2x friction stress (6.0 bps) simply swapped the subtracted cost against the exact same trade series (`tdf['net_2x']`). No rules were altered to force the stress case to pass.

## 14. Research Degrees of Freedom
**NO HIDDEN DEGREES OF FREEDOM.**
The G4 execution script contains exactly zero parameters capable of optimization. Everything is a rigid port from G3.

## 15. G4 Adjudication
**VALID**

## 16. G5 Recommendation
**G5 READY**

## 17. Integrity
The G4 economic execution represents a flawless, deterministic reflection of the scientifically authorized object. All trade accounting is mechanically robust and free of look-ahead bias.
