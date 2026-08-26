# QuantForge — RESEARCH FACTORY V2
# G1 ECONOMIC PLAUSIBILITY SCREEN — V6
# CAND-G0-015 / CAND-G0-016 / CAND-G0-017

## 1. Objective
Execute the first G1 Economic Plausibility Screen for CAND-G0-015, CAND-G0-016, and CAND-G0-017 under the V6 definitions. The objective is to determine if each frozen event produces a repeatable, executable post-entry conditional return distribution with enough mathematical and economic headroom to justify G2.

## 2. Frozen Definitions
- **CAND-015:** USATECHIDXUSD M5 return > 3 * 30-day M5 ATR. BTCUSD entry at M5 close in shock direction. Exit 60-min later. KPI: D1 Nasdaq ATR > 30-day vs < 30-day. Re-arm: 60-min lockout.
- **CAND-016:** EURUSD H1 TR > 2 SD, GBPUSD H1 TR < 1 SD. GBPUSD entry in EURUSD direction. KPI: London/NY session. Re-arm: Both < 1 SD for 4 hours.
- **CAND-017:** XAUUSD D1 BB Width < 10th percentile over 252d. H4 breakout close outside D1 BB. Exit 72-hours later. KPI: D1 200-SMA slope alignment. Re-arm: Price reverts and crosses H4 20-SMA.

## 3. Static Assertions
- All shock/breakout definitions asserted.
- All entry/exit timings deterministic (no MFE/MAE).
- Opportunity integrity constraints (lockouts, re-arms) strictly applied.
- Friction assumed at 3.0 bps round-trip.

## 4. Data Sources
- USATECHIDXUSD_M1.csv and BTCUSD_M1.csv (resampled to M5 for CAND-015).
- XAUUSD_M1.csv (resampled to H4 and D1 for CAND-017).
- GBPUSD_M1.csv missing in local repository, blocking CAND-016.

## 5. Friction Model
3.0 bps round-trip applied to net expectancy calculations.

## 6. CAND-015 Results (Nasdaq-Crypto Lag)
- **Integrity:** 2,061 raw shocks, 1,022 suppressed by 60-minute lockout. 1,039 valid opportunities.
- **Low Volatility Regime (D1 ATR < 30-day SMA):** N=381 (76/yr). Median Net = +5.08 bps. Mean Net = +9.53 bps. Win Rate = 54.1%. Avg Win = 66.05 bps, Avg Loss = -57.01 bps.
- **High Volatility Regime (D1 ATR > 30-day SMA):** N=658 (131/yr). Median Net = -0.94 bps. Mean Net = -5.63 bps. Win Rate = 49.4%.

## 7. CAND-016 Results (Asynchronous FX Lag)
- **Integrity:** BLOCKED. Required historical GBPUSD M1 data is not present in the local repository.

## 8. CAND-017 Results (Macro Compression Breakout)
- **Integrity:** 126 raw H4 breakout bars, 103 suppressed by re-arm requirement. 23 valid independent opportunities.
- **Aligned with 200-SMA:** N=14 (2.8/yr). Median Net = +20.60 bps, Mean Net = +16.47 bps. Win Rate = 57.1%.
- **Counter to 200-SMA:** N=9 (1.8/yr). Median Net = +15.75 bps, Mean Net = +3.47 bps. Win Rate = 55.6%.

## 9. Opportunity Integrity
CAND-015 accurately suppressed nearly 50% of raw signals by enforcing the 60-minute lockout. CAND-017 suppressed 82% of raw breakout bars by forcing a strict mean-reversion re-arm before recognizing a new breakout cycle.

## 10. Conditional Behavior
- **CAND-015:** The low-volatility macro regime produced a strong positive asymmetric distribution, directly contradicting the hypothesis that high-volatility environments lead to better cross-market flow. The low-volatility environment appears to allow cleaner cross-market latency arbitrage, whereas high-volatility environments contain too much noise/whipsaw.
- **CAND-017:** Both trend-aligned and counter-trend breakouts produced positive mean/median returns, but the frequency was exceptionally low.

## 11. Mathematical Expectancy
- **CAND-015 (Low Vol):** Positive expectancy (54.1% win rate, larger average win than loss).
- **CAND-017:** Small sample positive expectancy, but too few events to establish confidence.

## 12. Economic Headroom
- **CAND-015 (Low Vol):** CLEAR. Meaningful positive net headroom (+9.53 bps average after 3 bps friction) with credible frequency (76 events per year).
- **CAND-017:** INSUFFICIENT due to lack of frequency (only 23 events in 5 years).

## 13. G1 Classification
- **CAND-015:** **CLEAR**
- **CAND-016:** **BLOCKED** (Missing GBPUSD data)
- **CAND-017:** **INSUFFICIENT** (Frequency failure)

## 14. G2 Readiness
- **CAND-015:** READY for G2 empirical pilot.
- **CAND-016:** NOT READY.
- **CAND-017:** NOT READY.

## 15. Closed-Line Review
CAND-015 is a novel cross-market lead/lag latency hypothesis completely independent of previous mean-reversion, session expansion, or TSMOM lines.

## 16. Integrity
- No duplicate events or cascades.
- 100% deterministic post-entry measurement.
- No MFE used.
- No tick data or heavy infrastructure deployed.

## 17. Next Milestone
**G2 — CHEAP EMPIRICAL PILOT** (for CAND-G0-015).
