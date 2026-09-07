# QUANTFORGE — V35 G1 ECONOMIC PLAUSIBILITY SCREEN

## CAND-103 + CAND-104

**Date:** 2026-09-02
**Status:** COMPLETE — BOTH CANDIDATES CLOSED
**Market:** USATECHIDXUSD M1
**Data range:** 2023-09-01 to 2026-07-10 (~2.9 years, 906,815 bars)
**Cost assumption:** 2 bps round-trip friction

---

## 1. Mission

Execute V35 G1 Economic Plausibility Screen for CAND-103 (Multi-Timeframe Break Coordination) and CAND-104 (Post-Magnitude Directional Drift).

---

## 2. Authoritative Inputs

- V35 G0: `output/research_discovery/TRADEABLE_EDGE_DISCOVERY_SCREENING_V35.md`
- V35 G0 Integrity Audit: `output/research_discovery/QUANTFORGE_V35_G0_INTEGRITY_AUDIT_V1.md`
- G1 V3 Framework: `output/research_discovery/QUANTFORGE_G1_ECONOMIC_QUALIFICATION_FRAMEWORK_V3_RATIFICATION_V1.md`
- G0 Process Refinement: `output/research_discovery/QUANTFORGE_G0_MECHANISM_OBSERVABLE_CHALLENGE_V1.md`

---

## 3. Frozen Candidate Definitions

### CAND-103 — Multi-Timeframe Break Coordination

- **Research question:** Does coordinated structural breaking across multiple timeframes contain information different from a single-timeframe break?
- **Expression class:** STATE / CONDITION
- **Mechanism family:** Multi-Timeframe Interaction
- **Treatment:** 2+ timeframe levels broken simultaneously
- **Control:** 1 timeframe level broken
- **Expected effect:** Multi-timeframe breaks produce tighter distributions and stronger continuation
- **Outcome horizon:** 60 bars on M1
- **Timeframes:** M15, H1, H4

### CAND-104 — Post-Magnitude Directional Drift

- **Research question:** Does unusually large volatility-adjusted price movement contain information about subsequent directional drift?
- **Expression class:** STATE / CONDITION
- **Mechanism family:** Directional Dynamics
- **Observable:** Volatility-adjusted move magnitude (move size / ATR)
- **Treatment:** Moves exceeding magnitude threshold (2x, 3x, 4x, 5x ATR)
- **Control:** Moves below threshold
- **Expected effect:** Very large moves produce stronger directional continuation
- **Outcome horizon:** 60 bars on M1

---

## 4. Dataset / Experiment Identity

- **Dataset:** USATECHIDXUSD M1
- **Date range:** 2023-09-01 to 2026-07-10
- **Bars:** 906,815
- **Break detection:** ATR-based (1.5x ATR, 100-bar ATR lookback)
- **Multi-timeframe:** M15, H1, H4 (rolling high/low break detection)
- **Cost model:** 2 bps round-trip
- **Script:** `research/v35_g1_experiment.py`
- **Execution environment:** Python 3.11, pandas, numpy

---

## 5. Nine Hard Validity Gates

### CAND-103

| Gate | PASS/FAIL | Evidence |
|---|---|---|
| 1. Deterministic definition | PASS | Rolling high/low break detection is deterministic from OHLC |
| 2. Executable entry | PASS | Signal formed at M1 bar completion |
| 3. No hindsight contamination | PASS | No post-entry signal definition |
| 4. Correct cost normalization | PASS | 2 bps applied consistently |
| 5. Data integrity | PASS | M1 OHLC sufficient for multi-timeframe aggregation |
| 6. Legitimate counterfactual | PASS | Same event class, different timeframe scope |
| 7. Causal claims limited to observables | PASS | Hypothesis stated in observable terms |
| 8. No future-bar dependency | PASS | Uses only completed bars |
| 9. Reproducible | PASS | Deterministic from OHLC data |

### CAND-104

| Gate | PASS/FAIL | Evidence |
|---|---|---|
| 1. Deterministic definition | PASS | Magnitude computation is deterministic from OHLC |
| 2. Executable entry | PASS | Signal formed at bar completion |
| 3. No hindsight contamination | PASS | No post-entry signal definition |
| 4. Correct cost normalization | PASS | 2 bps applied consistently |
| 5. Data integrity | PASS | M1 OHLC sufficient for magnitude computation |
| 6. Legitimate counterfactual | PASS | Same event class, different magnitude |
| 7. Causal claims limited to observables | PASS | Hypothesis stated in observable terms |
| 8. No future-bar dependency | PASS | Uses only completed bars |
| 9. Reproducible | PASS | Deterministic from OHLC data |

**All 9 hard gates PASS for both candidates.**

---

## 6. CAND-103 Implementation Integrity

### Event Definition

- **Structural break:** Bar range > 1.5x ATR(100)
- **Multi-timeframe break:** M1 bar's high/low exceeds the rolling high/low of 2+ higher timeframes (M15, H1, H4)
- **Treatment:** 2+ timeframes broken simultaneously
- **Control:** 1 timeframe broken
- **Deduplication:** Minimum 60 bars between events

### Semantic Freeze Verification

| Element | G0 Definition | G1 Implementation | Match |
|---|---|---|---|
| Timeframe set | M15, H1, H4 | M15, H1, H4 | YES |
| Break detection | Rolling high/low exceedance | Rolling high/low exceedance | YES |
| Treatment | 2+ timeframes broken | 2+ timeframes broken | YES |
| Outcome window | 60 bars | 60 bars | YES |

**Semantic integrity:** PASS

---

## 7. CAND-103 Temporal Integrity

### Higher-Timeframe Look-Ahead Protection

The implementation uses `df['high'].rolling(tf).max().shift(1)` to compute the rolling high for each timeframe. The `.shift(1)` ensures only COMPLETED higher-timeframe bars are used. No future information enters the signal.

**Temporal integrity:** PASS

---

## 8. CAND-103 Sample Construction

- **Total M1 bars:** 906,815
- **M15 breaks:** 255,803
- **H1 breaks:** 121,714
- **H4 breaks:** 59,031
- **Total events (deduped):** 14,177
- **Treatment (2+ timeframes):** 5,049
- **Control (1 timeframe):** 9,128

### Sample Balance

Treatment:Control ratio = 1:1.8. Reasonable balance.

---

## 9. CAND-103 Economic Results

| Metric | Treatment (Multi-TF) | Control (Single-TF) | Delta |
|---|---|---|---|
| N | 5,049 | 9,128 | — |
| Gross Mean | +0.39 bps | +0.52 bps | -0.13 bps |
| Gross Median | +0.96 bps | +0.82 bps | +0.14 bps |
| Net Mean | -1.61 bps | -1.48 bps | -0.13 bps |
| Net Median | -1.04 bps | -1.18 bps | +0.14 bps |
| Win Rate | 52.6% | 52.8% | -0.3% |
| Std Dev | 28.02 bps | 28.80 bps | -0.78 bps |

### Direction-Specific Analysis

| Group | Direction | N | Mean | WR |
|---|---|---|---|---|
| Treatment | UP | 2,640 | +0.07 bps | 50.7% |
| Treatment | DOWN | 2,409 | +0.74 bps | 54.6% |
| Control | UP | 4,544 | +0.79 bps | 51.6% |
| Control | DOWN | 4,584 | +0.26 bps | 54.1% |

### Interpretation

- **Mean delta is essentially zero** (-0.13 bps). Multi-timeframe breaks produce virtually no economic separation from single-timeframe breaks.
- **Median delta is trivially positive** (+0.14 bps). Not economically meaningful.
- **Win rate delta is negligible** (-0.3%).
- **Distribution width is similar** (28.02 vs 28.80 bps std). Multi-timeframe breaks do NOT produce tighter distributions as predicted.
- **The hypothesis is contradicted.** Multi-timeframe breaks do not produce different economics than single-timeframe breaks.

---

## 10. CAND-103 Mechanism Interpretation

The experiment found NO economic separation between multi-timeframe and single-timeframe breaks. This contradicts the hypothesis that cross-timeframe coordination produces different economics.

**What the experiment actually demonstrated:** Cross-timeframe break coordination is conditionally associated with virtually identical economic outcomes to single-timeframe breaks. The mean delta is -0.13 bps (essentially zero).

**Mechanism implications:** The "participant coordination" mechanism is not supported by the evidence. Multi-timeframe breaks may simply be a consequence of strong directional moves, not a distinct market condition.

**Confounds:** The treatment and control groups may differ in trend state, volatility state, or session distribution. However, the economic separation is so small that these confounds are unlikely to explain the result.

---

## 11. CAND-103 Adjudication

### Evidence Profile

- Mean delta: -0.13 bps (essentially zero)
- Median delta: +0.14 bps (trivially positive)
- WR delta: -0.3% (negligible)
- Distribution width: similar (28.02 vs 28.80 bps)
- Hypothesis predicted: tighter distributions for treatment — CONTRADICTED

### Classification

> **CLOSED — ECONOMICALLY NEGATIVE**

**Rationale:** Multi-timeframe break coordination produces virtually no economic separation from single-timeframe breaks. The mean delta is -0.13 bps (essentially zero). The hypothesis that multi-timeframe breaks produce tighter distributions is contradicted (28.02 vs 28.80 bps std). The mechanism (participant coordination) is not supported.

---

## 12. CAND-104 Implementation Integrity

### Event Definition

- **Move magnitude:** Absolute bar return / ATR(100)
- **Treatment:** Moves exceeding magnitude threshold (2x, 3x, 4x, 5x ATR)
- **Control:** Moves below threshold
- **Deduplication:** Minimum 60 bars between events

### Semantic Freeze Verification

| Element | G0 Definition | G1 Implementation | Match |
|---|---|---|---|
| Magnitude normalization | Move size / ATR | Absolute bar return / ATR | YES |
| Threshold | Pre-declared | 2x, 3x, 4x, 5x ATR | YES |
| Outcome window | 60 bars | 60 bars | YES |

**Semantic integrity:** PASS

---

## 13. CAND-104 Magnitude Semantics

The implementation uses absolute bar return / ATR as the magnitude measure. This is a SINGLE-MOVE magnitude, not cumulative trend. The treatment is based on individual bar magnitude, not a lookback momentum measure.

**Magnitude semantic integrity:** PASS — the treatment is genuinely based on single-move magnitude, not cumulative directional trend.

---

## 14. CAND-104 Trend-Confound/Control Integrity

The G0 audit identified trend confound risk. The G1 implementation does NOT include a predeclared trend-control filter (none was specified in the frozen protocol).

**Trend-control limitation:** Without a predeclared trend-control methodology, the G1 experiment cannot definitively distinguish:
- Magnitude-specific drift (the hypothesized mechanism)
- Ordinary trend continuation (the alternative explanation)

This is a **methodology limitation**, not a measurement failure. The frozen protocol did not predeclare a trend-control filter.

---

## 15. CAND-104 Sample Construction

- **Total M1 bars:** 906,815
- **Bars > 2x ATR:** 16,021 (1.77%)
- **Bars > 3x ATR:** 3,722 (0.41%)
- **Bars > 4x ATR:** 1,262 (0.14%)
- **Bars > 5x ATR:** 579 (0.06%)
- **Total events (deduped):** 15,111

### Sample Distribution by Threshold

| Threshold | Treatment N | Control N |
|---|---|---|
| >= 2x ATR | 265 | 14,846 |
| >= 3x ATR | 56 | 15,055 |
| >= 4x ATR | 17 | 15,094 |

**Sample adequacy:** Thresholds 2x and 3x have adequate treatment samples. Threshold 4x has only 17 treatment events — very small.

---

## 16. CAND-104 Economic Results

| Threshold | Treatment N | Treatment Gross Mean | Control Gross Mean | Mean Delta | Median Delta | Treatment WR | Control WR |
|---|---|---|---|---|---|---|---|
| >= 2x ATR | 265 | -4.84 bps | +0.57 bps | -5.41 bps | -0.14 bps | 51.7% | 53.6% |
| >= 3x ATR | 56 | -4.65 bps | +0.49 bps | -5.14 bps | -0.66 bps | 50.0% | 53.6% |
| >= 4x ATR | 17 | +6.02 bps | +0.47 bps | +5.56 bps | +1.54 bps | 58.8% | 53.5% |

### Direction-Specific Analysis (>= 4x ATR)

| Direction | N | Mean | WR |
|---|---|---|---|
| UP | 8 | +12.53 bps | 75.0% |
| DOWN | 9 | +0.25 bps | 44.4% |

### Interpretation

- **At 2x and 3x ATR:** Large moves produce WORSE economics than the control (mean delta -5.41 and -5.14 bps). This CONTRADICTS the persistence hypothesis. Large moves are followed by mean reversion, not continuation.
- **At 4x ATR:** The pattern reverses (+5.56 bps delta), but N=17 is very small. This is likely driven by a few outlier events.
- **Direction asymmetry at 4x ATR:** UP moves produce +12.53 bps (N=8), DOWN moves produce +0.25 bps (N=9). The asymmetry is dramatic but based on extremely small samples.
- **The hypothesis is contradicted at 2x and 3x ATR.** The 4x ATR result is too small to draw conclusions.

---

## 17. CAND-104 Mechanism Interpretation

The experiment found that large volatility-adjusted moves (2x-3x ATR) are followed by WORSE economics than the control, contradicting the persistence hypothesis. The forced-repositioning mechanism is NOT supported at these thresholds.

**What the experiment actually demonstrated:** Very large moves (2x-3x ATR) are followed by mean reversion, not continuation. The mean delta is -5.41 bps at 2x ATR (control superior).

**Mechanism implications:** The forced-repositioning mechanism is not supported. Large moves may represent trend climax (exhaustion) rather than forced repositioning. The market may "digest" large moves through mean reversion.

**The 4x ATR result:** The positive delta at 4x ATR (+5.56 bps) is interesting but based on N=17. This cannot be distinguished from noise or outliers. Without a predeclared trend-control filter, the mechanism cannot be isolated.

---

## 18. CAND-104 Adjudication

### Evidence Profile

- At 2x ATR: Mean delta -5.41 bps (control superior). HYPOTHESIS CONTRADICTED.
- At 3x ATR: Mean delta -5.14 bps (control superior). HYPOTHESIS CONTRADICTED.
- At 4x ATR: Mean delta +5.56 bps (treatment superior). N=17 (very small).
- Direction asymmetry at 4x ATR: UP +12.53 bps (N=8), DOWN +0.25 bps (N=9). Extremely small samples.

### Classification

> **CLOSED — HYPOTHESIS CONTRADICTED**

**Rationale:** The persistence hypothesis is contradicted at 2x and 3x ATR thresholds. Large moves are followed by mean reversion, not continuation. The 4x ATR result is too small (N=17) to draw conclusions and may reflect outliers. The forced-repositioning mechanism is not supported.

---

## 19. Cross-Candidate Interpretation

Both candidates failed to produce economically meaningful conditional separation:

- **CAND-103:** Multi-timeframe breaks produce virtually no economic difference from single-timeframe breaks (mean delta -0.13 bps)
- **CAND-104:** Large moves are followed by mean reversion, not continuation (mean delta -5.41 bps at 2x ATR)

The evidence does not represent useful information for either candidate.

---

## 20. Limitations

1. **CAND-103:** The treatment/control split may be confounded with trend state. However, the economic separation is so small that confounds are unlikely to explain the result.
2. **CAND-104:** No predeclared trend-control filter. Cannot distinguish magnitude-specific drift from ordinary trend continuation. However, the hypothesis is contradicted at 2x-3x ATR regardless of trend control.
3. **CAND-104:** The 4x ATR result (N=17) is too small for reliable conclusions.
4. **Single instrument/timeframe:** Results specific to USATECHIDXUSD M1.

---

## 21. Governance Disposition

| Candidate | N (T/C) | Hard Gates | Net Mean | Net Median | WR | Mean Delta | Final Classification |
|---|---|---|---|---|---|---|---|
| CAND-103 | 5,049 / 9,128 | 9/9 PASS | -1.61 / -1.48 bps | -1.04 / -1.18 bps | 52.6% / 52.8% | -0.13 bps | ECONOMICALLY NEGATIVE |
| CAND-104 | 265 / 14,846 (2x) | 9/9 PASS | -6.84 / -1.43 bps | varies | 51.7% / 53.6% | -5.41 bps | HYPOTHESIS CONTRADICTED |

### Governance Verification

- ✅ No optimization
- ✅ No post-hoc thresholding
- ✅ No protected runtime inspection
- ✅ No relational testing
- ✅ No APEX execution
- ✅ No closed candidate reopened
- ✅ No G2 execution
- ✅ Forward runtime untouched
- ✅ State library unchanged

---

## 22. Reproducibility

- **Dataset:** USATECHIDXUSD M1 (`data/m1/USATECHIDXUSD_M1.csv`)
- **Date range:** 2023-09-01 to 2026-07-10
- **Bars:** 906,815
- **Cost assumption:** 2 bps round-trip
- **Script:** `research/v35_g1_experiment.py`
- **Frozen parameters:**
  - ATR lookback: 100
  - Break threshold: 1.5x ATR
  - Timeframes: M15, H1, H4
  - Outcome horizon: 60 bars
  - Min event separation: 60 bars
  - Magnitude thresholds: 2x, 3x, 4x, 5x ATR
- **Execution environment:** Python 3.11, pandas, numpy

---

*V35 G1 complete. Both candidates closed. No G2 promotions. V35 permanently closed.*
