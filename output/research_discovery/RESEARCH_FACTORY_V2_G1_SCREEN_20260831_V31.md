# RESEARCH FACTORY V2 — V31 G1 ECONOMIC PLAUSIBILITY SCREEN

**Date:** 2026-08-31
**Status:** COMPLETE
**Candidates:** CAND-092, CAND-093 (2 authorized)

---

## 1. G1 Status

> **COMPLETE**

## 2. V31 G0 Integrity Result

- CAND-092: NEW — ELIGIBLE
- CAND-093: NEW — ELIGIBLE
- CAND-094: REDUNDANT WITH CAND-093 — CLOSED (rejected at G0 audit)

## 3. Authorized Candidate Set

| ID | Name | Mechanism Family | Type |
|---|---|---|---|
| CAND-092 | Event-Information Decay | Information Persistence Dynamics | STATE / CONDITION |
| CAND-093 | Price-Discovery Friction Gradient | Microstructure Information Dynamics | STATE / CONDITION |

## 4. CAND-094 Exclusion

> CLOSED / REDUNDANT WITH CAND-093 — NOT TESTED

## 5. CAND-092 — Event-Information Decay

### 5.1 Frozen Definition

- **Market:** USATECHIDXUSD
- **Timeframe:** M1
- **Date range:** 2023-09-01 to 2026-07-10 (2.9 years)
- **Structural level:** 20-bar rolling high/low (from PRIOR bars)
- **Breakout threshold:** 3 bps
- **Treatment:** Events with time-since-prior-event < median (high information remaining)
- **Control:** Events with time-since-prior-event >= median (low information remaining)
- **Median time-since:** 89 bars
- **Holding period:** 60 bars (60 min)
- **Cost model:** 2 bps friction
- **Direction:** WITH the event
- **Rearm:** 60-bar minimum

### 5.2 Data and Coverage

- Source: `data/m1/USATECHIDXUSD_M1.csv`
- Rows: 906,815
- Coverage: 2023-09-01 to 2026-07-10
- Volume: UNAVAILABLE

### 5.3 Event Universe

- Raw breaks: 20,092 (9,323 up + 10,769 down)
- After rearm: 6,519
- After forward-return filter: 6,519

### 5.4 Treatment

High-information-remaining: events where time since prior structural event < 89 bars (median). N = 3,195.

### 5.5 Counterfactual

Low-information-remaining: events where time since prior event >= 89 bars. N = 3,324. Same event class, same market, same timeframe, same cost model. Only difference: time elapsed since prior event.

### 5.6 Sample Counts

| Group | N | % |
|---|---|---|
| High info remaining (treatment) | 3,195 | 49.0% |
| Low info remaining (control) | 3,324 | 51.0% |
| **Total** | **6,519** | |

### 5.7 Frequency

| Metric | Value |
|---|---|
| High info events/year | 1,119 |
| Low info events/year | 1,164 |
| Total events/year | 2,283 |

### 5.8 Gross Economics

| Metric | High Info (Treatment) | Low Info (Control) |
|---|---|---|
| Gross Mean | -1.42 bps | +0.69 bps |
| Gross Median | -0.51 bps | -0.71 bps |

### 5.9 Net Economics

| Metric | High Info (Treatment) | Low Info (Control) |
|---|---|---|
| Net Mean | **-3.42 bps** | **-1.31 bps** |
| Net Median | **-2.51 bps** | **-2.71 bps** |
| Win Rate | 46.3% | 42.9% |
| Std Dev | 46.26 bps | 27.47 bps |

### 5.10 Distribution

| Percentile | High Info | Low Info |
|---|---|---|
| P10 | -42.64 bps | -28.14 bps |
| P25 | -20.71 bps | -13.54 bps |
| P50 | -2.51 bps | -2.71 bps |
| P75 | +16.01 bps | +9.15 bps |
| P90 | +37.93 bps | +26.46 bps |

**Distribution assessment:** The high-info group has wider dispersion (46.26 vs 27.47 bps std) and fatter tails in both directions. The P10 is much worse for high-info (-42.64 vs -28.14 bps), which hurts net mean despite the better median. The distributions show partial separation in the tails but overlap in the center.

### 5.11 Conditional Delta

| Metric | Value |
|---|---|
| Mean Delta | **-2.11 bps** (control superior) |
| Median Delta | **+0.21 bps** (treatment better) |
| WR Delta | **+3.3%** (treatment better) |

**Interpretation:** Contradictory evidence. Mean says control is better (treatment worse by 2.11 bps). Median says treatment is slightly better (+0.21 bps). Win rate says treatment is better (+3.3%). The mean is dragged down by wider dispersion and worse tail in the high-info group.

### 5.12 Nine Hard Gates

| # | Gate | Result | Evidence |
|---|---|---|---|
| 1 | Deterministic definition | **PASS** | 20-bar structural level, 3 bps breakout, median time-split. Fully reproducible. |
| 2 | Executable entry | **PASS** | Time-since-event computed before entry. Entry at break. |
| 3 | No hindsight contamination | **PASS** | No post-entry filtering. Time-since measured from historical data only. |
| 4 | Correct cost normalization | **PASS** | 2 bps applied identically to both groups. |
| 5 | Data integrity | **PASS** | OHLC present. Volume unavailable but not required. |
| 6 | Legitimate counterfactual | **PASS** | Same event class, different time-since. Mechanism-specific. |
| 7 | Causal claims limited to observables | **PASS** | Hypothesis in time/event terms. "Information decay" is the mechanism label, not a causal proof. |
| 8 | No future-bar dependency | **PASS** | Time-since computed from prior events only. |
| 9 | Reproducible | **PASS** | Same data + same code = same result. |

**9/9 gates PASS**

### 5.13 Temporal Integrity

- Time-since-event is computed from the PREVIOUS structural event to the CURRENT event
- No future information enters the treatment classification
- Forward returns computed AFTER classification
- No contamination from later events
- **PASS**

### 5.14 Mechanism Assessment

**Hypothesis:** Recent events (high information remaining) produce different downstream economics than older events (low information remaining).

**Observed:** Treatment (recent) has WORSE mean (-2.11 bps delta) but BETTER median (+0.21 bps) and higher win rate (+3.3%). The wider dispersion in the treatment group drives the negative mean.

**Assessment: AMBIGUOUS.** The mean contradicts the hypothesis (treatment worse). The median and win rate support it (treatment better). The mechanism may exist but be dominated by tail risk in the high-info group. The extreme dispersion difference (46.26 vs 27.47 bps std) suggests the high-info condition adds volatility without consistent directional benefit.

### 5.15 Absolute vs Conditional Economics

| Dimension | Value |
|---|---|
| Treatment absolute (net mean) | -3.42 bps |
| Control absolute (net mean) | -1.31 bps |
| Conditional delta (mean) | -2.11 bps (control superior) |
| Conditional delta (median) | +0.21 bps (treatment better) |

Both absolute and conditional mean economics are negative. The conditional median is trivially positive. Neither dimension supports standalone Alpha.

### 5.16 State Potential

> **NOT JUSTIFIED**

The conditional evidence is contradictory (mean negative, median trivially positive). The wider dispersion in the treatment group suggests the "high information remaining" condition adds risk without consistent return benefit. No State classification warranted.

### 5.17 Economic Adjudication

> **ECONOMICALLY NEGATIVE / MIXED EVIDENCE**

**Rationale:**
- Net mean is -3.42 bps (negative absolute economics)
- Mean delta is -2.11 bps (control superior — contradicts hypothesis)
- Median delta is +0.21 bps (trivially positive)
- WR delta is +3.3% (treatment better)
- The contradictory evidence across metrics prevents a clean classification
- The wide dispersion in the treatment group suggests the mechanism adds volatility, not consistent return
- No meaningful incremental information demonstrated

### 5.18 Governance Decision

> **CLOSED — MIXED EVIDENCE / NO MEANINGFUL INCREMENTAL INFORMATION**

CAND-092 does not survive G1. The event-information decay mechanism produces contradictory evidence: the treatment group has worse mean but better median and win rate. The wider dispersion suggests the mechanism adds risk without consistent directional benefit.

---

## 6. CAND-093 — Price-Discovery Friction Gradient

### 6.1 Frozen Definition

- **Market:** USATECHIDXUSD
- **Timeframe:** M1
- **Date range:** 2023-09-01 to 2026-07-10
- **Structural level:** 20-bar rolling high/low
- **Breakout threshold:** 3 bps
- **Treatment:** Low friction (monotonicity >= median = 0.55)
- **Control:** High friction (monotonicity < median)
- **Holding period:** 60 bars
- **Cost model:** 2 bps friction
- **Direction:** WITH the break
- **Rearm:** 60-bar minimum

### 6.2 Data and Coverage

Same as CAND-092.

### 6.3 Event Universe

- After rearm: 8,421 (4,069 up + 4,352 down)

### 6.4 Treatment

Low friction: approach monotonicity >= 0.55 (median). N = 5,601.

### 6.5 Counterfactual

High friction: approach monotonicity < 0.55. N = 2,820.

### 6.6 Sample Counts

| Group | N | % |
|---|---|---|
| Low friction (treatment) | 5,601 | 66.5% |
| High friction (control) | 2,820 | 33.5% |
| **Total** | **8,421** | |

### 6.7 Frequency

| Metric | Value |
|---|---|
| Low friction events/year | 1,961 |
| High friction events/year | 988 |

### 6.8 Gross Economics

| Metric | Low Friction (Treatment) | High Friction (Control) |
|---|---|---|
| Gross Mean | -0.67 bps | +0.34 bps |
| Gross Median | -0.61 bps | -1.39 bps |

### 6.9 Net Economics

| Metric | Low Friction (Treatment) | High Friction (Control) |
|---|---|---|
| Net Mean | **-2.67 bps** | **-1.66 bps** |
| Net Median | **-2.61 bps** | **-3.39 bps** |
| Win Rate | 44.5% | 43.9% |
| Std Dev | 37.57 bps | 45.14 bps |

### 6.10 Distribution

| Percentile | Low Friction | High Friction |
|---|---|---|
| P10 | -34.85 bps | -40.95 bps |
| P25 | -16.88 bps | -19.73 bps |
| P50 | -2.61 bps | -3.39 bps |
| P75 | +11.81 bps | +13.77 bps |
| P90 | +32.05 bps | +38.03 bps |

**Distribution assessment:** The distributions overlap substantially at all percentiles. The low-friction group has narrower dispersion (37.57 vs 45.14 bps std). The P10 is better for low-friction (-34.85 vs -40.95 bps), supporting better downside. But the P90 is worse for low-friction (32.05 vs 38.03 bps), suggesting less upside.

### 6.11 Conditional Delta

| Metric | Value |
|---|---|
| Mean Delta | **-1.00 bps** (control superior) |
| Median Delta | **+0.77 bps** (treatment better) |
| WR Delta | **+0.6%** (nearly identical) |

**Interpretation:** Contradictory evidence. Mean says control is better. Median says treatment is better. Win rate is nearly identical. The mean is driven by the control group's higher gross mean (+0.34 vs -0.67 bps).

### 6.12 Nine Hard Gates

| # | Gate | Result | Evidence |
|---|---|---|---|
| 1 | Deterministic definition | **PASS** | 20-bar structural level, 3 bps breakout, monotonicity threshold. Reproducible. |
| 2 | Executable entry | **PASS** | Approach smoothness computed before break. Entry at break. |
| 3 | No hindsight contamination | **PASS** | No post-entry filtering. Approach measured from pre-break bars. |
| 4 | Correct cost normalization | **PASS** | 2 bps identical. |
| 5 | Data integrity | **PASS** | OHLC present. |
| 6 | Legitimate counterfactual | **PASS** | Same event class, different approach quality. |
| 7 | Causal claims limited to observables | **PASS** | "Consensus" is labeled as inferred mechanism, not proven. |
| 8 | No future-bar dependency | **PASS** | Approach measured before break. |
| 9 | Reproducible | **PASS** | Same code + same data = same result. |

**9/9 gates PASS**

### 6.13 Temporal Integrity

- Approach smoothness computed from bars BEFORE the break
- No future information enters treatment classification
- Forward returns computed after classification
- **PASS**

### 6.14 Mechanism Assessment

**Hypothesis:** Low-friction (clean) approach produces larger directional moves.

**Observed:** Treatment (low friction) has WORSE mean (-1.00 bps delta) but BETTER median (+0.77 bps). Win rate nearly identical. The control group has higher gross mean but worse median.

**Assessment: AMBIGUOUS.** The median supports the hypothesis (+0.77 bps treatment better). The mean contradicts it (-1.00 bps control better). The mechanism may exist but be dominated by the control group's better gross performance. The narrower dispersion in the treatment group (37.57 vs 45.14 bps) is consistent with the mechanism (cleaner approach = less noise), but the economic benefit is not consistently positive.

### 6.15 Absolute vs Conditional Economics

| Dimension | Value |
|---|---|
| Treatment absolute (net mean) | -2.67 bps |
| Control absolute (net mean) | -1.66 bps |
| Conditional delta (mean) | -1.00 bps (control superior) |
| Conditional delta (median) | +0.77 bps (treatment better) |

Both groups are negative in absolute terms. The conditional evidence is contradictory.

### 6.16 State Potential

> **NOT JUSTIFIED**

The conditional evidence is contradictory. The median supports the mechanism but the mean contradicts it. The narrower dispersion in the treatment group is consistent with the mechanism but does not demonstrate sufficient economic information for State classification.

### 6.17 Economic Adjudication

> **ECONOMICALLY NEGATIVE / MIXED EVIDENCE**

**Rationale:**
- Net mean is -2.67 bps (negative absolute economics)
- Mean delta is -1.00 bps (control superior)
- Median delta is +0.77 bps (treatment better)
- Win rate delta is +0.6% (nearly identical)
- The contradictory evidence prevents a clean classification
- The mechanism may exist but does not produce consistent economic information

### 6.18 Governance Decision

> **CLOSED — MIXED EVIDENCE / NO MEANINGFUL INCREMENTAL INFORMATION**

CAND-093 does not survive G1. The price-discovery friction mechanism produces contradictory evidence: the treatment group has better median but worse mean. The economic information is not consistently positive across metrics.

---

## 7. Candidate Comparison

| Dimension | CAND-092 | CAND-093 |
|---|---|---|
| Treatment N | 3,195 | 5,601 |
| Control N | 3,324 | 2,820 |
| Treatment Net Mean | -3.42 bps | -2.67 bps |
| Control Net Mean | -1.31 bps | -1.66 bps |
| Mean Delta | -2.11 bps | -1.00 bps |
| Median Delta | +0.21 bps | +0.77 bps |
| WR Delta | +3.3% | +0.6% |
| Mechanism | AMBIGUOUS | AMBIGUOUS |
| Decision | CLOSED | CLOSED |

## 8. Economic Evidence Comparison

Both candidates show negative absolute economics and contradictory conditional evidence. Neither demonstrates consistent incremental information. CAND-092 has more extreme contradictory evidence (larger mean delta but also larger WR delta). CAND-093 has more moderate contradictions.

## 9. Counterfactual Quality

Both candidates have well-constructed counterfactuals:
- Same event class, same market, same timeframe, same cost model
- Only difference: the proposed mechanism (time-since-event / approach quality)
- Counterfactuals are legitimate and discriminating

The failures are in the economic evidence, not the experimental design.

## 10. Distribution / Tail Assessment

Both candidates show wider dispersion in the treatment group (CAND-092: 46.26 vs 27.47 bps; CAND-093: treatment has narrower dispersion 37.57 vs 45.14 bps). The tail behavior is inconsistent with a clean directional mechanism.

## 11. Temporal Integrity

Both candidates have valid temporal ordering. No look-ahead. No future contamination.

## 12. Nine-Gate Summary

| Gate | CAND-092 | CAND-093 |
|---|---|---|
| 1. Deterministic | PASS | PASS |
| 2. Executable entry | PASS | PASS |
| 3. No hindsight | PASS | PASS |
| 4. Cost normalization | PASS | PASS |
| 5. Data integrity | PASS | PASS |
| 6. Counterfactual | PASS | PASS |
| 7. Observable claims | PASS | PASS |
| 8. No future-bar | PASS | PASS |
| 9. Reproducible | PASS | PASS |
| **Total** | **9/9** | **9/9** |

## 13. Prior-Art Integrity

- CAND-092: NEW (confirmed by V31 G0 audit)
- CAND-093: NEW (confirmed by V31 G0 audit)
- CAND-094: CLOSED / REDUNDANT (not tested)

## 14. State Library

**NO CHANGE**

## 15. SEED-002

> TESTED NEGATIVE — NO INCREMENTAL INFORMATION

## 16. APEX RB001–RB004

> DESIGNED / NOT EXECUTED

## 17. CAND-090 / CAND-087

> CLOSED / NOT REOPENED

## 18. Closed-Line Firewall

> PASS

## 19. Forward Runtime

CAND-015/024/035: **ACTIVE / PROTECTED / UNTOUCHED**

## 20. Confirmation Requirements

Neither candidate warrants confirmation. Both are closed at G1.

## 21. Final Economic Adjudication

### CAND-092

> **CLOSED — ECONOMICALLY NEGATIVE / MIXED EVIDENCE**

Event-information decay produces contradictory evidence: worse mean but better median and win rate. The wider dispersion in the treatment group suggests the mechanism adds risk without consistent directional benefit. No meaningful incremental information demonstrated.

### CAND-093

> **CLOSED — ECONOMICALLY NEGATIVE / MIXED EVIDENCE**

Price-discovery friction produces contradictory evidence: better median but worse mean. Win rate nearly identical. The mechanism may exist but does not produce consistent economic information under the frozen definitions.

## 22. Integrity Verification

| Check | Status |
|---|---|
| Only CAND-092 and CAND-093 tested | ✓ |
| CAND-094 not tested | ✓ |
| No replacement candidate generated | ✓ |
| No thresholds optimized | ✓ |
| No relational test performed | ✓ |
| SEED-002 not retested | ✓ |
| No State combined | ✓ |
| APEX RB not executed | ✓ |
| Forward runtime not inspected | ✓ |
| Nine hard gates applied | ✓ |
| Treatment frozen before evaluation | ✓ |
| Counterfactuals not redesigned | ✓ |
| Temporal ordering valid | ✓ |
| No look-ahead | ✓ |
| Gross/net separated | ✓ |
| Absolute/conditional separated | ✓ |
| Distribution assessed | ✓ |
| No unsupported causal claim | ✓ |
| Confirmation not performed | ✓ |
| G2 not performed | ✓ |
| SESSION_HANDOFF updated | ✓ |

---

**Artifact:** `output/research_discovery/RESEARCH_FACTORY_V2_G1_SCREEN_20260831_V31.md`
**Script:** `research/v31_g1_experiment.py`
