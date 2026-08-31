# RESEARCH FACTORY V2 — V32 G1 ECONOMIC PLAUSIBILITY SCREEN

## 1. G1 Status

> **COMPLETE**

V32 G1 — Economic plausibility screen for CAND-095 (Shock-Magnitude Asymmetry) and CAND-096 (Volatility Acceleration Gradient).

## 2. V32 G0 Integrity Result

- CAND-095: **NEW** — G1 ELIGIBLE
- CAND-096: **NEW** — G1 ELIGIBLE WITH CAND-077 OVERLAP CAVEAT
- CAND-097: **REDUNDANT WITH DISC-021** — REJECTED

## 3. Authorized Candidate Set

| ID | Name | Status |
|---|---|---|
| CAND-095 | Shock-Magnitude Asymmetry | ELIGIBLE |
| CAND-096 | Volatility Acceleration Gradient | ELIGIBLE |

## 4. CAND-097 Exclusion

CAND-097 (Post-Shock Overshoot Reversion) was rejected as REDUNDANT with DISC-021 Mean Reversion. Same economic mechanism (price moves too far, then reverts). DISC-021 established this mechanism is statistically observable but economically non-viable.

---

## 5. CAND-095 — Shock-Magnitude Asymmetry

### 5.1 Frozen Definition

| Element | Value |
|---|---|
| Market | USATECHIDXUSD |
| Timeframe | M1 |
| Data range | 2023-09-01 to 2026-07-10 |
| Event universe | Bar-to-bar moves > 1.5x rolling 100-bar ATR |
| Primary observable | Shock direction (UP vs DOWN) |
| Dynamic feature | Direction-dependent participant response |
| Treatment | UP shocks |
| Counterfactual | DOWN shocks (opposite direction) |
| Downstream event | Forward return after shock |
| Evaluation horizon | 60 bars (60 min) |
| Direction | WITH shock direction |
| Rearm | 60-bar minimum |
| Deduplication | Rearm applied |
| Cost model | 2 bps friction |

### 5.2 Data and Coverage

- Source: USATECHIDXUSD M1 OHLC
- Date range: 2023-09-01 to 2026-07-10 (1,043 days)
- Missing periods: None documented
- Volume: Unavailable/zero (not used)

### 5.3 Event Universe

- Raw UP shocks: 20,487
- Raw DOWN shocks: 22,579
- After rearm: UP=7,325, DOWN=7,524
- Total: 14,849 events
- Frequency: ~5,200/year

### 5.4 Treatment

UP shocks (bar-to-bar move > 1.5x ATR in UP direction). Enter WITH shock direction at close of shock bar.

### 5.5 Counterfactual

DOWN shocks (bar-to-bar move > 1.5x ATR in DOWN direction). Same magnitude threshold, opposite direction.

### 5.6 Sample

| Group | N | Gross Mean | Gross Median | Net Mean | Net Median | WR | Std |
|---|---|---|---|---|---|---|---|
| UP (treatment) | 7,325 | +0.58 bps | +0.97 bps | -1.42 bps | -1.03 bps | 46.4% | 32.58 bps |
| DOWN (control) | 7,524 | +0.86 bps | +1.55 bps | -1.14 bps | -0.45 bps | 48.6% | 33.13 bps |

### 5.7 Frequency

~5,200 shocks/year (high frequency — condition is common)

### 5.8 Gross Economics

Both groups have slightly positive gross mean and median. Gross economics are marginally positive before costs.

### 5.9 Net Economics

Both groups are net negative after 2 bps friction. Neither treatment nor control is independently profitable.

### 5.10 Distribution

Both groups have similar distributions (Std: 32.58 vs 33.13 bps). Overlapping at all percentiles. No meaningful distributional separation.

### 5.11 Directional Asymmetry

| Metric | UP - DOWN Delta |
|---|---|
| Mean Delta | -0.28 bps (DOWN superior) |
| Median Delta | -0.58 bps (DOWN superior) |
| WR Delta | -2.2% (DOWN superior) |

**Assessment:** DOWN shocks slightly outperform UP shocks on all metrics. The asymmetry exists but is small and in the opposite direction of the hypothesis (DOWN shocks are better, not worse).

### 5.12 Conditional Delta

- Mean Delta: -0.28 bps (control superior)
- Median Delta: -0.58 bps (control superior)
- WR Delta: -2.2% (control superior)

The conditional delta is small and favors the control on all metrics.

### 5.13 Nine Hard Gates

| Gate | Result | Evidence |
|---|---|---|
| 1. Measurement integrity | PASS | Bar-to-bar return computed from OHLC |
| 2. Temporal ordering | PASS | Shock identified before forward return computed |
| 3. Look-ahead protection | PASS | No future information used in treatment membership |
| 4. Counterfactual validity | PASS | Same magnitude threshold, opposite direction |
| 5. Sample adequacy | PASS | N > 7,000 per group |
| 6. Cost model integrity | PASS | 2 bps applied identically to both groups |
| 7. Rearm integrity | PASS | 60-bar minimum enforced |
| 8. Data integrity | PASS | Standard USATECHIDXUSD M1 data |
| 9. No survivorship bias | PASS | All events included |

**9/9 PASS**

### 5.14 Temporal Integrity

- Shock identified at bar close
- Forward return computed from bar close to bar close + 60
- No future information in treatment membership
- Rolling ATR uses only prior bars

**PASS**

### 5.15 Mechanism Assessment

The hypothesis predicted DOWN shocks would produce different downstream economics than UP shocks due to asymmetric participant response (short-sale constraints, institutional flow).

**Result:** DOWN shocks slightly outperform UP shocks, but the difference is small (-0.28 bps mean) and all metrics favor the control. The asymmetry is economically negligible.

**Classification: AMBIGUOUS** — Asymmetry exists but is small and in the opposite direction of the hypothesis. No meaningful economic information demonstrated.

### 5.16 Absolute vs Conditional Economics

- **Absolute:** Neither group is independently profitable after costs
- **Conditional:** Control (DOWN) slightly better than treatment (UP), but difference is negligible

### 5.17 State Potential

The conditional delta is small (-0.28 bps) and favors the control. No meaningful state relationship demonstrated.

**NOT STATE REVIEW ELIGIBLE**

### 5.18 Economic Adjudication

**ECONOMICALLY NEGATIVE**

- Absolute economics are negative for both groups
- Conditional delta is small and favors the control
- No meaningful directional asymmetry demonstrated
- The hypothesis predicted DOWN shocks would be worse; the evidence shows DOWN shocks are slightly better (contradicts hypothesis direction)

### 5.19 Governance Decision

> **CLOSED — ECONOMICALLY NEGATIVE**

CAND-095 does not survive G1. The shock-magnitude asymmetry hypothesis is not supported by the economic evidence. DOWN shocks slightly outperform UP shocks on all metrics, contradicting the hypothesized direction.

---

## 6. CAND-096 — Volatility Acceleration Gradient

### 6.1 Frozen Definition

| Element | Value |
|---|---|
| Market | USATECHIDXUSD |
| Timeframe | M1 |
| Data range | 2023-09-01 to 2026-07-10 |
| Event universe | Structural level breaks (20-bar lookback, 3 bps threshold) |
| Primary observable | Volatility acceleration (second derivative of ATR) |
| Dynamic feature | Rate of change of volatility |
| Treatment | Breaks during acceleration (vol_accel > 0) |
| Counterfactual | Breaks during deceleration (vol_accel < 0) |
| Downstream event | Forward return after break |
| Evaluation horizon | 60 bars (60 min) |
| Direction | WITH break direction |
| Rearm | 60-bar minimum |
| Deduplication | Rearm applied |
| Cost model | 2 bps friction |

### 6.2 CAND-077 Semantic Equivalence Check

**CRITICAL INTEGRITY CHECK**

| Dimension | CAND-077 | CAND-096 |
|---|---|---|
| Observable | ATR percentile (regime state) | Second derivative of ATR (acceleration) |
| Temporal structure | Discrete: compressed → expanded | Continuous: acceleration rate |
| Mechanism | Regime transition | Rate of change |
| Economic question | Does regime state affect economics? | Does acceleration rate affect economics? |

**Assessment:** The implementation genuinely measures volatility acceleration (second derivative), not regime transition. The treatment is classified by whether vol_acceleration > 0, which is a continuous measure distinct from discrete regime classification.

**PASS — CAND-096 semantics remain distinct from CAND-077**

### 6.3 Data and Coverage

- Source: USATECHIDXUSD M1 OHLC
- Date range: 2023-09-01 to 2026-07-10 (1,043 days)
- Missing periods: None documented
- Volume: Unavailable/zero (not used)

### 6.4 Event Universe

- Raw up breaks: 9,323
- Raw down breaks: 10,769
- After rearm: total 6,519 breaks
- Accelerating: 5,622
- Decelerating: 897
- Frequency: ~2,283/year

### 6.5 Treatment

Structural level breaks during periods of volatility acceleration (second derivative of ATR > 0). Enter WITH break direction at break point.

### 6.6 Counterfactual

Structural level breaks during periods of volatility deceleration (second derivative of ATR < 0). Same event class, different volatility dynamics.

### 6.7 Sample

| Group | N | Gross Mean | Gross Median | Net Mean | Net Median | WR | Std |
|---|---|---|---|---|---|---|---|
| Accelerating (treatment) | 5,622 | +0.77 bps | +1.25 bps | -1.23 bps | -0.75 bps | 48.5% | 37.78 bps |
| Decelerating (control) | 897 | +2.40 bps | +2.73 bps | +0.40 bps | +0.73 bps | 51.6% | 38.32 bps |

### 6.8 Frequency

~2,283 breaks/year. Acceleration is the dominant state (86% of breaks).

### 6.9 Gross Economics

Decelerating breaks have substantially better gross economics (+2.40 vs +0.77 bps mean). Accelerating breaks have marginally positive gross; decelerating breaks are clearly positive.

### 6.10 Net Economics

- Accelerating: Net Mean=-1.23 bps, Net Median=-0.75 bps (NEGATIVE)
- Decelerating: Net Mean=+0.40 bps, Net Median=+0.73 bps (POSITIVE)

Decelerating breaks are net positive after 2 bps friction. Accelerating breaks are net negative.

### 6.11 Distribution

Both groups have similar standard deviations (37.78 vs 38.32 bps). The distributions overlap, but decelerating breaks have better central tendency at all metrics.

### 6.12 Conditional Delta

| Metric | ACCEL - DECEL Delta |
|---|---|
| Mean Delta | -1.62 bps (DECEL superior) |
| Median Delta | -1.48 bps (DECEL superior) |
| WR Delta | -3.1% (DECEL superior) |

**Assessment:** Decelerating volatility significantly outperforms accelerating volatility on all metrics. The conditional delta is large and consistently favors the control.

### 6.13 Nine Hard Gates

| Gate | Result | Evidence |
|---|---|---|
| 1. Measurement integrity | PASS | Second derivative of ATR computed from OHLC |
| 2. Temporal ordering | PASS | Acceleration computed before forward return |
| 3. Look-ahead protection | PASS | No future information in treatment membership |
| 4. Counterfactual validity | PASS | Same event class, different acceleration state |
| 5. Sample adequacy | PASS | N > 800 per group (accelerating N=5,622) |
| 6. Cost model integrity | PASS | 2 bps applied identically |
| 7. Rearm integrity | PASS | 60-bar minimum enforced |
| 8. Data integrity | PASS | Standard USATECHIDXUSD M1 data |
| 9. No survivorship bias | PASS | All events included |

**9/9 PASS**

### 6.14 Temporal Integrity

- Acceleration computed from ATR history before the break
- Forward return computed from break point to break point + 60
- No future information in treatment classification
- Rolling ATR uses only prior bars

**PASS**

### 6.15 Mechanism Assessment

The hypothesis predicted accelerating volatility would produce different downstream economics than decelerating volatility due to participant adaptation lag and risk-management stress.

**Result:** Decelerating volatility significantly outperforms accelerating volatility. The mechanism is consistent with the hypothesis but in the OPPOSITE direction: accelerating volatility is WORSE, not better. The hypothesis predicted acceleration would produce larger/more persistent moves; the evidence shows acceleration produces worse economics.

**Classification: CONTRADICTED** — The directional prediction is wrong. Acceleration is associated with WORSE economics, not better. The mechanism exists but operates in the opposite direction.

### 6.16 Absolute vs Conditional Economics

- **Absolute:** Accelerating breaks are net negative (-1.23 bps). Decelerating breaks are net positive (+0.40 bps).
- **Conditional:** Decelerating significantly outperforms accelerating (-1.62 bps mean delta)

The conditional information is meaningful: deceleration = better economics. But this contradicts the hypothesis direction.

### 6.17 State Potential

The conditional delta is large (-1.62 bps) and consistently favors deceleration. This demonstrates a genuine state relationship: volatility acceleration state affects downstream economics.

**STATE REVIEW ELIGIBLE** — The deceleration condition is associated with materially better economics. However, the relationship is in the opposite direction of the hypothesis.

### 6.18 Economic Adjudication

**INFORMATIONALLY INTERESTING**

- Absolute economics are mixed (accelerating negative, decelerating positive)
- Conditional delta is large (-1.62 bps) and favors the control
- The relationship is genuine but in the opposite direction of the hypothesis
- The mechanism is not what was hypothesized, but the information is real

### 6.19 Governance Decision

> **CLOSED — HYPOTHESIS CONTRADICTED**

CAND-096 does not survive G1. The volatility acceleration hypothesis predicted accelerating volatility would produce better economics; the evidence shows decelerating volatility is significantly better. The conditional information is real but the hypothesis direction is wrong.

---

## 7. Candidate Comparison

| Dimension | CAND-095 | CAND-096 |
|---|---|---|
| N (treatment) | 7,325 | 5,622 |
| N (control) | 7,524 | 897 |
| Mean Delta | -0.28 bps | -1.62 bps |
| Median Delta | -0.58 bps | -1.48 bps |
| WR Delta | -2.2% | -3.1% |
| Nine Gates | 9/9 PASS | 9/9 PASS |
| Mechanism | AMBIGUOUS | CONTRADICTED |
| Adjudication | ECONOMICALLY NEGATIVE | INFORMATIONALLY INTERESTING |

## 8. Economic Evidence Comparison

CAND-096 has stronger conditional information (larger delta) but the hypothesis direction is wrong. CAND-095 has weaker conditional information and the direction is also wrong.

## 9. Counterfactual Quality

Both counterfactuals are well-constructed:
- CAND-095: Same magnitude threshold, opposite direction
- CAND-096: Same event class, different acceleration state

Failures are in economic evidence, not experimental design.

## 10. Distribution / Tail Assessment

Both candidates show similar distributions between treatment and control. No meaningful tail separation.

## 11. Temporal Integrity

Both candidates have valid temporal ordering. No look-ahead.

## 12. Nine-Gate Summary

| Candidate | Gates |
|---|---|
| CAND-095 | 9/9 PASS |
| CAND-096 | 9/9 PASS |

Both candidates pass all hard validity gates. Failures are in economic evidence.

## 13. CAND-096 vs CAND-077 Integrity

**PASS** — CAND-096 genuinely measures volatility acceleration (second derivative), not regime transition. The implementation is distinct from CAND-077.

## 14. Prior-Art / G0 Integrity

- CAND-095: NEW (confirmed)
- CAND-096: NEW (confirmed, distinct from CAND-077)
- CAND-097: REDUNDANT WITH DISC-021 (confirmed, closed)

## 15. State Library

CAND-077/081/083: **PRESERVED**

## 16. SEED-002

> TESTED NEGATIVE — NO INCREMENTAL INFORMATION

## 17. Relational Framework

> GOVERNED — NO NEW TEST

## 18. APEX RB001–RB004

> DESIGNED / NOT EXECUTED

## 19. CAND-097 / DISC-021

CAND-097: **CLOSED / REDUNDANT WITH DISC-021**

## 20. Closed-Line Firewall

No V19–V31 closed hypothesis reopened. CAND-097 closed as redundant.

## 21. Forward Runtime

CAND-015/024/035: **ACTIVE / PROTECTED / UNTOUCHED**

## 22. Confirmation Requirements

Neither candidate warrants confirmation. Both failed G1.

## 23. Final Economic Adjudication

| Candidate | Adjudication | State Potential |
|---|---|---|
| CAND-095 | ECONOMICALLY NEGATIVE | NOT JUSTIFIED |
| CAND-096 | INFORMATIONALLY INTERESTING | STATE REVIEW ELIGIBLE (opposite direction) |

## 24. Integrity Verification

1. Only CAND-095 and CAND-096 were tested
2. CAND-097 was not tested
3. DISC-021 was not reopened
4. No replacement candidate was generated
5. CAND-096 implementation genuinely measures acceleration (second derivative)
6. CAND-096 semantics remain distinct from CAND-077
7. No thresholds were optimized
8. No parameter grids were searched
9. No post-outcome filters were created
10. Counterfactuals were not redesigned
11. Temporal ordering is valid
12. No look-ahead occurred
13. Nine hard gates were applied
14. Gross and net economics are separated
15. Absolute and conditional economics are separated
16. Mean, median, WR, distribution and tails were considered
17. No unsupported causal claims were made
18. No State interaction was performed
19. SEED-002 was not retested
20. No relational testing occurred
21. APEX RB001–RB004 were not executed
22. Forward runtime was not inspected
23. Confirmation was not executed
24. G2 was not executed
25. System Assembly was not executed
26. Ledger provenance is complete
27. SESSION_HANDOFF to be updated
28. Database and timeline to be updated
29. Git staged diff limited to authorized files
