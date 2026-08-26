# QuantForge — RESEARCH FACTORY V2
# G1 ECONOMIC PLAUSIBILITY SCREEN — CAND-G0-006 / 007 / 008

## 1. Objective

Execute the first formal G1 Economic Plausibility Screen under the hardened Research Factory V2 contract. Evaluate CAND-G0-006, CAND-G0-007, and CAND-G0-008 to determine if they possess valid, executable post-entry economic headroom to justify a cheap G2 pilot. This execution strictly enforces the prohibition of MFE, future extrema, and undocumented proxies.

## 2. Frozen Candidate Definitions

- **CAND-G0-006 (Crypto-to-Equity Risk-On Impulse Lead):**
  - **Trigger:** BTCUSD directional return in the 2 hours preceding 09:30 ET > 3x its 14-day ATR.
  - **Executable Entry:** USATECHIDXUSD exactly at the close of the 09:30 ET M1 bar.
  - **Deterministic Exit:** 16:00 ET cash session close.

- **CAND-G0-007 (Weekend Gap Regime Continuation):**
  - **Trigger:** Weekend gap > 1.5x 14-day ATR, remaining unfilled through hour 2.
  - **Executable Entry:** Hour-2 close.
  - **Deterministic Exit:** Friday session close.

- **CAND-G0-008 (Safe-Haven Metal Divergence):**
  - **Trigger:** Daily return of XAUUSD > +1.5% AND XAGUSD < -1.0%.
  - **Executable Entry:** Long XAUUSD / Short XAGUSD at the daily close.
  - **Deterministic Exit:** 5 trading days later at the daily close.

## 3. Static Definition Assertions

| Assertion | CAND-006 | CAND-007 | CAND-008 |
| :--- | :--- | :--- | :--- |
| **Trigger Exact** | PASS | PASS | PASS |
| **Entry Exact** | PASS | PASS | PASS |
| **Exit Exact** | PASS | PASS | PASS |
| **Holding Period Exact** | PASS | PASS | PASS |
| **Market Universe Exact** | PASS | PASS | PASS |
| **Thresholds Exact** | PASS | PASS | PASS |
| **Friction Explicit** | PASS | PASS | PASS |
| **No-MFE Endpoint** | PASS | PASS | PASS |
| **No Proxy Substitution** | PASS | PASS | PASS |
| **No Down-sampling** | PASS | PASS | PASS |

## 4. Data Sources

- **Source:** Repository cheap dataset (`data/m1/`).
- **Instruments:** `BTCUSD_M1.csv`, `USATECHIDXUSD_M1.csv`, `EURUSD_M1.csv`, `XAUUSD_M1.csv`, `XAGUSD_M1.csv`.
- **Date Range:** 2021-04-12 to 2026-04-10 (5 years of M1 data).
- No production tick data, Parquet files, or Stage 1/2 infrastructure was used.

## 5. Friction Assumptions

- **CAND-006 (USATECHIDXUSD):**
  - One-way spread assumption: 2.0 bps.
  - Round-trip equivalent: 4.0 bps.
  - Applied twice (entry and exit). Evidence: TRACEABLE (observed historical MT5 spreads).
- **CAND-007 (EURUSD):**
  - One-way spread assumption: 0.5 bps.
  - Round-trip equivalent: 1.0 bps.
  - Applied twice. Evidence: TRACEABLE.
- **CAND-008 (XAUUSD & XAGUSD):**
  - One-way spread assumption: XAU (1.5 bps), XAG (3.0 bps).
  - Round-trip equivalent: 9.0 bps (combined portfolio).
  - Applied twice for both legs. Evidence: TRACEABLE.

## 6. Candidate-Level Results

### CAND-006
- **Events Found:** 1 event over 5 years.
- **Median Gross Return:** +74.24 bps.
- **Frequency Issue:** The trigger condition (BTC moving > 3 Daily ATR in exactly 2 hours) is structurally too rare to form an active strategy.

### CAND-007
- **Triggers Found:** 2 weekend gaps > 1.5 ATR.
- **Events Found:** 0 events.
- **Execution Issue:** Neither of the 2 massive weekend gaps remained unfilled for 2 hours. Both immediately mean-reverted, killing the entry.

### CAND-008
- **Triggers Found:** 0 events.
- **Frequency Issue:** Over 5 years of daily data, there was not a single day where Gold rose > 1.5% while Silver simultaneously fell > 1.0%.

## 7. Executable Entry Verification

- **CAND-006:** Verified. Measurement begins exactly at the 09:30 ET close.
- **CAND-007:** Verified conceptually. Measurement explicitly programmed to begin at the hour-2 close (but 0 qualifying events).
- **CAND-008:** Verified conceptually. Measurement explicitly programmed to begin at the daily close (but 0 qualifying events).

## 8. Deterministic Exit Verification

- **CAND-006:** Verified. Exits strictly at the 16:00 ET close. No intraday MFE was captured.
- **CAND-007:** Verified conceptually. Exits at the deterministic Friday 16:59 ET close.
- **CAND-008:** Verified conceptually. Exits exactly 5 days post-entry.

## 9. Gross Headroom

- **CAND-006:** +74.24 bps (Median), +74.24 bps (Mean), +74.24 bps (Lower Quartile), 1 Event.
- **CAND-007:** N/A (0 events).
- **CAND-008:** N/A (0 events).

## 10. Net Headroom

- **CAND-006:** +70.24 bps (Gross minus 4 bps round-trip friction).
- **CAND-007:** N/A.
- **CAND-008:** N/A.

## 11. Frequency

- **CAND-006:** 0.2 events per year (1 event in 5 years). Average hold 6.5 hours. Overlap risk 0%. INSUFFICIENT to matter.
- **CAND-007:** 0 events in 5 years. INSUFFICIENT.
- **CAND-008:** 0 events in 5 years. INSUFFICIENT.

## 12. G1 Classification

- **CAND-006: INSUFFICIENT.** While the single event had clear economic headroom, the frozen trigger is structurally too rare to constitute a tradeable strategy.
- **CAND-007: BLOCKED (INSUFFICIENT).** The required phenomenon (massive gaps that do not fill) does not occur in the 5-year dataset.
- **CAND-008: BLOCKED (INSUFFICIENT).** The required cross-market divergence phenomenon never occurred in the 5-year dataset.

## 13. G2 Recommendation

- **CAND-006:** DO NOT PROMOTE. (Frequency failure).
- **CAND-007:** DO NOT PROMOTE. (Frequency/Existence failure).
- **CAND-008:** DO NOT PROMOTE. (Frequency/Existence failure).

## 14. Infrastructure Used

- Pure Python Pandas scripts (`research/scratch/g1_006.py`, `g1_007.py`, `g1_008.py`).
- Read-only M1 CSV data from `data/m1/`.
- No Stage 1, Stage 2, Parquet, or Tick infrastructure used.

## 15. Integrity

- **NO MFE:** MFE was not computed or used.
- **NO FUTURE EXTREMA:** All exits were deterministic time-horizons.
- **NO PRE-ENTRY CAPTURE:** Post-entry measurement strictly enforced.
- **NO PROXY SUBSTITUTIONS:** Candidate definitions used EXACTLY as written.
- **NO PARAMETER OPTIMIZATION:** Triggers (3 ATR, 1.5 ATR, +1.5%/-1.0%) were NOT altered to artificially produce events.

## 16. Next Milestone

> **G0 — CANDIDATE GENERATION**
