# QuantForge — Research Factory V2
# G1 ECONOMIC PLAUSIBILITY SCREEN — V9
# 2026-08-26

## 1. G1 Objective
Determine whether the frozen V9 G0 mechanisms produce enough real, executable, post-entry economic movement in the predicted direction to overcome realistic friction and earn a cheap G2 empirical pilot.

## 2. Static Integrity
**PASS.**
For all candidates:
- Event matching V9 strict definition.
- Event fully known before entry.
- Entry price executable.
- Measurement strictly post-entry.
- Deterministic, frozen exit.
- No MFE or future extreme contamination.
- No hidden parameters or data leakage.

## 3. CAND-025
### Macro Shock Liquidity Void Reversal
- **Qualifying Events:** 157
- **Frequency:** 54.98 / year
- **Mean Gross:** +3.25 points
- **Median Gross:** +4.64 points
- **Friction:** 2.0 points
- **Mean Net:** +1.25 points
- **Median Net:** +2.64 points
- **Win Rate:** 52.23%
- **Best Trade (Gross):** +190.58 points
- **Worst Trade (Gross):** -155.70 points

## 4. CAND-026
### US Open Initial Balance Trap
- **Qualifying Events:** 521
- **Frequency:** 182.45 / year
- **Mean Gross:** -10.75 points
- **Median Gross:** -11.24 points
- **Friction:** 2.0 points
- **Mean Net:** -12.75 points
- **Median Net:** -13.24 points
- **Win Rate:** 41.84%
- **Best Trade (Gross):** +722.24 points
- **Worst Trade (Gross):** -968.61 points

## 5. CAND-027
### Intraday Trend Inventory Unwind
- **Qualifying Events:** 16
- **Frequency:** 5.60 / year
- **Mean Gross:** -40.52 points
- **Median Gross:** -23.71 points
- **Friction:** 2.0 points
- **Mean Net:** -42.52 points
- **Median Net:** -25.71 points
- **Win Rate:** 43.75%
- **Best Trade (Gross):** +131.77 points
- **Worst Trade (Gross):** -259.85 points

## 6. Friction
- **Instrument:** USATECHIDXUSD (Nasdaq 100 CFD / NQ Futures proxy)
- **Friction:** 2.0 points per round trip
- **Reasoning:** 2.0 points provides a strict, conservative aggregate covering crossing the bid/ask spread (typically 0.5-1.0 pt), commissions, and modest institutional slippage during semi-volatile hours.

## 7. Frequency
- **CAND-025:** ~55/year (1 per week). Adequate for testing. Max 1 event per day.
- **CAND-026:** ~182/year. Excellent frequency. Max 1 event per day.
- **CAND-027:** ~5.6/year (16 total). Severely clustered and sparse due to the strict 1.5 ATR threshold.

## 8. Distribution
- **CAND-025:** POSITIVE MEAN / POSITIVE MEDIAN
- **CAND-026:** NEGATIVE MEDIAN / NEGATIVE MEAN
- **CAND-027:** NEGATIVE MEDIAN / NEGATIVE MEAN

## 9. Executable-Capture Verification
- **CAND-025:** PASS. Evaluates movement strictly from 08:35 to 09:30, after the 08:30 macro shock completes.
- **CAND-026:** PASS. Evaluates movement starting from the next M5 open after the trap candle closes.
- **CAND-027:** PASS. Evaluates movement strictly from 15:00 to 15:55, explicitly ignoring the prior daily trend.

## 10. G1 Classification
- **CAND-025:** PASS — MARGINAL. Both mean and median net expectancies are positive, confirming the presence of a post-entry structural drift. However, the +1.25 mean net is thin and requires strict out-of-sample stress testing in G2 to ensure it is not merely absorbing noise.
- **CAND-026:** INSUFFICIENT. The failure mechanism was completely contradicted by the negative expected value. False breaks tended to reverse back into the trend rather than causing a massive unwind.
- **CAND-027:** INSUFFICIENT. The 1.5 ATR event threshold yielded almost no events (16), and the few that triggered had severely negative expectancy. The predicted liquidation mechanism is overpowered by continuation momentum into the close.

## 11. G2 Promotions
- **CAND-G0-025**

## 12. Kill / Block / Invalid List
- **Killed:** CAND-026 (INSUFFICIENT), CAND-027 (INSUFFICIENT).
- **Blocked/Invalid:** None.

## 13. Resource Use
- **Data:** Local USATECH M1 CSV. No tick data or Parquet used.
- **Execution:** Lightweight, deterministic Python scan. No ML or optimization.

## 14. CAND-015 Independence
- CAND-015's 7-Day Forward Observation was completely isolated and its incomplete results were explicitly ignored.

## 15. Integrity
All G1 bounds, strict definitions, and post-entry capture measurements were verified. No parameters were swept, no proxies were used, and no outlier trimming was performed to rescue underperforming candidates.
