# QuantForge — SMC HYPOTHESIS REGISTER V1

## 1. Provenance

> Owner-supplied hypotheses — NOT VALIDATED.

These concepts represent owner-supplied Smart Money Concepts (SMC) and related behavioral models. They are hypotheses requiring independent algorithmic validation under the Research Factory V2 doctrine. They are not accepted facts. Statements such as "contains institutional orders" are treated strictly as causal hypotheses subject to falsification.

## 2. Hypothesis Classification

- **H1:** Color-Independent OB + FVG (Order Block is the candle preceding an FVG).
- **H2:** HTF POI + M1/M5 CHOCH Reversal (HTF sweep followed by lower-timeframe structural shift).
- **H3:** Leading Diagonal / Five-Wave Trend Initiation (Fibonacci retracement after 5-wave impulse from POI).
- **H4:** Ending Diagonal / Wave-5 Throw-Under or Throw-Over (Terminal sweep of a 5-wave structure).
- **H5:** Two-Bar Reversal + Low Volume (Engulfing at POI with low volume on the reversal bar).
- **H6:** Double Top/Bottom + RSI Divergence (Structural double top/bottom + momentum divergence).

## 3. Formalization Assessment

- **H1:** FORMALIZABLE WITH DEFINITIONS. (An FVG can be deterministically defined as a gap between candle $t-2$ high and candle $t$ low. OB is simply candle $t-2$. Requires formalization, but no discretionary logic).
- **H2:** FORMALIZABLE WITH DEFINITIONS. (Requires objective definition of "HTF POI" and exact swing-structure logic for "CHOCH", e.g., wick vs close, minimum pivot distance).
- **H3:** DISCRETIONARY / NOT YET FORMALIZABLE. (Objective Elliott-wave labeling is historically fraught with hindsight bias and discretionary parameter tuning).
- **H4:** DISCRETIONARY / NOT YET FORMALIZABLE. (Requires trendline boundary drawing and wave counting, both highly subjective).
- **H5:** FORMALIZABLE WITH DEFINITIONS. (Requires definition of "low volume" relative to a moving average or session profile, plus volume data audit).
- **H6:** FORMALIZABLE. (RSI divergence and swing matching tolerances can be defined mathematically without discretion).

## 4. Economic-Capture Assessment

- **H1:** UNKNOWN. (Currently only a structural definition, lacks an entry/exit sequence).
- **H2:** MARGINAL. (Entry is clear via CHOCH, but needs deterministic exit and friction must be weighed against tight M1 structures).
- **H3:** BLOCKED. (Due to discretionary labeling).
- **H4:** BLOCKED. (Due to discretionary labeling).
- **H5:** UNKNOWN. (Needs deterministic entry trigger following the second bar and a fixed exit).
- **H6:** UNKNOWN. (Needs exact entry trigger and exit, e.g., breaking the neckline or fixed horizon).

## 5. Data Requirements

- **H1, H2, H6:** Require M1 data, potentially aggregated for HTF POIs (e.g., M15/H1).
- **H5 (Volume):** Requires a volume audit. Tick volume in FX/CFDs may not reliably map to institutional liquidity. Requires verification of volume consistency in `data/m1/`.
- **H3, H4:** N/A (Blocked).

## 6. Closed-Line Independence

- **H1 (OB/FVG):** NEW primitive.
- **H2 (POI + CHOCH):** ADJACENT to Liquidity Sweep (DISC-025). DISC-025 used a sweep + wick rejection + confirmation close. H2 relies on a structural swing break (CHOCH). It is not a direct rescue, but close.
- **H3/H4:** N/A (Blocked).
- **H5 (Low Vol Reversal):** NEW. Contrasts with CAND-G0-004 (High Volume Impact Reversal).
- **H6 (RSI Div):** ADJACENT to Mean Reversion (DISC-021). Must ensure the divergence is structural and not just deep z-score displacement disguised by a bounded oscillator.

## 7. Research-Family Grouping

- **Family 1: Structural Reversals at Liquidity Extremes (H2, H5, H6).** All three hypotheses rely on price reaching a Point of Interest (POI) and exhibiting a specific lower-timeframe confirmation (CHOCH, Volume Anomaly, or Momentum Divergence).
- **Family 2: Structural Primitives (H1).** OB/FVG is not a trading strategy itself but a building block that defines a POI.
- **Family 3: Wave Mechanics (H3, H4).** Elliott Wave structures.

## 8. G0 Candidates Worth Considering

Only hypotheses that can be reduced to deterministic trigger, executable entry, deterministic exit, and post-entry response are eligible.
- **H2 (CHOCH Reversal):** If POI and CHOCH are mathematically frozen.
- **H5 (Low Volume Reversal):** If volume data passes audit.
- **H6 (Double Top RSI Div):** If divergence is strictly quantified.

## 9. Blocked/Rejected Hypotheses

- **H3:** BLOCKED (Discretionary wave labeling).
- **H4:** BLOCKED (Discretionary diagonal/wave labeling).

## 10. G1 Prerequisites

Before G1 execution, any selected G0 candidate must specify:
1. Observable Trigger
2. Executable Entry (No hindsight/MFE)
3. Deterministic Exit
4. Explicit Friction

## 11. Integrity

- No hypotheses were assumed to be true.
- SMC nomenclature was translated to mechanistic hypotheses.
- Hindsight-reliant concepts (Elliott Waves) were aggressively blocked.
- No G1/G2 execution occurred.
- No backtests or data scans were run.
