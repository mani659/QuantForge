# QuantForge — RESEARCH FACTORY V2
# G1 ECONOMIC PLAUSIBILITY SCREEN — SMC CAND-010 & CAND-011

## 1. Objective

Execute the G1 Economic Plausibility Screen for CAND-G0-010 (HTF POI + CHOCH Reversal) and CAND-G0-011 (Double Top/Bottom + RSI Divergence) derived from the SMC hypothesis register. The objective is to determine if the frozen executable definitions contain sufficient post-entry headroom to justify a G2 pilot.

## 2. Candidate Definitions

- **CAND-G0-010 (HTF POI + M1/M5 CHOCH Reversal):**
  - **POI:** Previous day's high or low.
  - **Trigger:** Price crosses POI, followed by a confirmed M5 swing structure, and an M5 close breaking the immediately preceding opposing swing (CHOCH).
  - **Executable Entry:** Market order on the open of the next M5 bar post-CHOCH.
  - **Deterministic Exit:** Fixed 2-hour horizon.

- **CAND-G0-011 (Double Top/Bottom + RSI Divergence):**
  - **Trigger:** Two 20-bar rolling extrema separated by 20–100 bars. Price of Swing 2 within 0.1% of Swing 1. 14-period RSI at Swing 2 at least 5 points less extreme. Confirmed when price crosses 10-period SMA.
  - **Executable Entry:** Market order on the close of the confirming bar.
  - **Deterministic Exit:** Fixed 4-hour horizon.

## 3. Static Assertions

| Assertion | CAND-010 | CAND-011 |
| :--- | :--- | :--- |
| **Trigger Exact** | PASS | PASS |
| **Entry Exact** | PASS | PASS |
| **Exit Exact** | PASS | PASS |
| **Holding Period Exact** | PASS | PASS |
| **Friction Explicit** | PASS | PASS |
| **No-MFE Endpoint** | PASS | PASS |
| **No Hindsight Entry** | PASS | PASS |

## 4. Data Sources

- **Source:** Repository M1 dataset (`data/m1/`).
- **Instruments:** `EURUSD_M1.csv` (CAND-010), `XAUUSD_M1.csv` (CAND-011).
- **Date Range:** ~5 years (2021-2026).
- **Infrastructure:** Python Pandas scripts in `research/scratch/`. No tick data or Parquet used.

## 5. Candidate 010 Results

- **Total POI/CHOCH Events:** 20,726
- **Valid Entries:** 20,726
- **Median Gross Post-Entry Return:** 0.00 bps
- **Mean Gross Post-Entry Return:** -0.02 bps
- **Lower Quartile Return:** -5.52 bps
- **Frequency:** ~4,145 per year.
- **Holding Period:** 2 hours (fixed).

## 6. Candidate 011 Results

- **Total Setups:** 4,026
- **Valid Entries:** 4,026
- **Median Gross Post-Entry Return:** +0.16 bps
- **Mean Gross Post-Entry Return:** +0.08 bps
- **Lower Quartile Return:** -16.83 bps
- **Frequency:** ~805 per year.
- **Holding Period:** 4 hours (fixed).

## 7. Executable-Capture Verification

- **CAND-G0-010:** Verified. Measurements start on the M5 open *after* the CHOCH confirmation bar closes. No pre-entry excursion is captured.
- **CAND-G0-011:** Verified. Measurements start precisely at the close of the SMA-crossing confirmation bar. No discretionary top-picking occurred.

## 8. Frequency Analysis

- Both candidates generated sufficient frequency for evaluation. However, the high event count coupled with near-zero expected value strongly falsifies the hypotheses as standalone directional edges. The structures do not consistently predict post-entry price movement.

## 9. Friction Analysis

- **CAND-G0-010 (EURUSD M5):** 1.0 bps round-trip spread assumption. With 0.00 bps gross median return, the net headroom is -1.0 bps. Friction consumes 100% of the non-existent edge.
- **CAND-G0-011 (XAUUSD M5):** 3.0 bps round-trip spread assumption. With +0.16 bps gross median return, the net headroom is -2.84 bps. 

## 10. G1 Classification

- **CAND-G0-010: INSUFFICIENT.** Despite robust frequency, the CHOCH pattern following a POI sweep provides literally zero predictive edge over the subsequent 2 hours.
- **CAND-G0-011: INSUFFICIENT.** The RSI divergence double-top provides negligible structural advantage (+0.16 bps gross), which is instantly destroyed by trading friction.

## 11. G2 Readiness

- **CAND-G0-010:** DO NOT PROMOTE. (Zero economic headroom).
- **CAND-G0-011:** DO NOT PROMOTE. (Zero net headroom).

## 12. Closed-Line Firewall

- **CAND-G0-010:** Stayed structurally distinct from DISC-025 by enforcing the M5 CHOCH break, avoiding a simple wick-sweep rescue.
- **CAND-G0-011:** Stayed distinct from DISC-021 by enforcing strict dual-swing geometric constraints rather than pure z-score displacement.

## 13. Integrity

- **No Hidden Parameters:** Thresholds were frozen at G0.
- **No MFE / Future-Extrema Contamination:** Strictly enforced fixed time-horizon exits.
- **No Discretionary Chart Labeling:** Swing detection and RSI divergence were entirely algorithmic.

## 14. Next Milestone

> **G0 — CANDIDATE GENERATION**
