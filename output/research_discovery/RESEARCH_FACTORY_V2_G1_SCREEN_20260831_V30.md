# RESEARCH FACTORY V2 — V30 G1 ECONOMIC PLAUSIBILITY SCREEN

**Date:** 2026-08-31
**Status:** COMPLETE
**Candidates:** CAND-089, CAND-091 (2 authorized)

---

## 1. G1 Status

> **COMPLETE**

## 2. V30 G0 Integrity Result

- CAND-089: NEW — ELIGIBLE
- CAND-090: REDUNDANT WITH CAND-087 — CLOSED (rejected)
- CAND-091: NEW — ELIGIBLE

G1 candidate count: 2 (not 3)

## 3. Authorized Candidates

| ID | Name | Mechanism Family | Type |
|---|---|---|---|
| CAND-089 | Acceptance Velocity Decay | Information Processing Dynamics | STANDALONE ALPHA / STATE |
| CAND-091 | Cumulative Directional Exhaustion | Directional Exhaustion Dynamics | STATE / CONDITION |

## 4. CAND-090 Exclusion

> CLOSED / REDUNDANT WITH CAND-087 — NOT TESTED

Same economic hypothesis as V29 CAND-087. Same mechanism, same observable concept, same counterfactual structure, same economic prediction. Parameter differences are implementation choices, not mechanism distinctions.

## 5. CAND-089 — Acceptance Velocity Decay

### 5.1 Frozen Definition

- **Market:** USATECHIDXUSD
- **Timeframe:** M1
- **Date range:** 2023-09-01 to 2026-07-10 (2.9 years, 1,043 days)
- **Structural level:** 20-bar rolling high/low (from PRIOR bars)
- **Breakout threshold:** 3 bps
- **Rearm:** 60-bar minimum
- **Preceding window:** 20 bars before each break
- **Velocity decay:** Late-window range vs early-window range
- **Holding period:** 60 bars (60 min)
- **Cost model:** 2 bps friction
- **Direction:** WITH the break (long if up break, short if down break)

### 5.2 Data and Coverage

- Source: `data/m1/USATECHIDXUSD_M1.csv`
- Rows: 906,815
- Coverage: 2023-09-01 00:00:00 to 2026-07-10 20:14:00
- Volume: UNAVAILABLE (all zeros)

### 5.3 Population

| Group | N | % |
|---|---|---|
| Decaying velocity (treatment) | 4,152 | 49.3% |
| Stable velocity (control) | 4,269 | 50.7% |
| **Total** | **8,421** | |

### 5.4 Frequency

| Metric | Value |
|---|---|
| Decaying events/year | 1,454 |
| Stable events/year | 1,495 |
| Total events/year | 2,949 |

### 5.5 Gross Economics

| Metric | Decaying (Treatment) | Stable (Control) |
|---|---|---|
| Gross Mean | -0.20 bps | -0.46 bps |
| Gross Median | -0.98 bps | -0.77 bps |

### 5.6 Net Economics

| Metric | Decaying (Treatment) | Stable (Control) |
|---|---|---|
| Net Mean | **-2.20 bps** | **-2.46 bps** |
| Net Median | **-2.98 bps** | **-2.77 bps** |
| Win Rate | 43.7% | 44.9% |
| Std Dev | 42.43 bps | 38.05 bps |

### 5.7 Distribution

| Percentile | Decaying | Stable |
|---|---|---|
| P10 | -36.96 bps | -37.40 bps |
| P25 | -18.17 bps | -17.34 bps |
| P50 | -2.98 bps | -2.77 bps |
| P75 | +12.75 bps | +12.33 bps |
| P90 | +34.23 bps | +33.52 bps |

**Distribution assessment:** Nearly identical distributions across all percentiles. No separation between treatment and control. The distributions are effectively indistinguishable.

**Top 10% contribution:**
- Decaying: +27,294.6 bps of -9,134.7 bps total (298.8% share)
- Stable: +26,511.2 bps of -10,492.0 bps total (252.7% share)

**Exclude-best-event mean:**
- Decaying: -2.45 bps
- Stable: -2.59 bps

**Worst event:**
- Decaying: -1,045.90 bps
- Stable: -475.92 bps

### 5.8 Counterfactual

**Treatment:** Structural breaks preceded by decaying acceptance velocity (late range wider than early range = velocity declining).

**Control:** Structural breaks preceded by stable or improving acceptance velocity (late range narrower than early range = velocity stable or increasing).

**Counterfactual quality:** Well-defined. Same event class (structural level break), same market, same timeframe, same cost model. Only difference: velocity trajectory (decaying vs stable).

### 5.9 Conditional Delta

| Metric | Value |
|---|---|
| Mean Delta | **+0.26 bps** |
| Median Delta | **-0.22 bps** |
| WR Delta | **-1.2%** |

**Interpretation:** Mean delta is positive but tiny (+0.26 bps). Median delta is negative (-0.22 bps), indicating the mean improvement is driven by outliers. Win rate is LOWER for decaying velocity (43.7% vs 44.9%). The directional evidence is contradictory: mean says decaying is better, median says decaying is worse, win rate says decaying is worse.

### 5.10 Nine Hard Gates

| # | Gate | Result | Evidence |
|---|---|---|---|
| 1 | Deterministic definition | **PASS** | 20-bar structural level + 3 bps breakout + 20-bar velocity measurement. Fully reproducible. |
| 2 | Executable entry | **PASS** | Velocity is measured BEFORE the break; entry is at the break. No hindsight. |
| 3 | No hindsight contamination | **PASS** | No post-entry filtering. No MFE/MAE dependency. |
| 4 | Correct cost normalization | **PASS** | 2 bps friction applied consistently to both groups. |
| 5 | Data integrity | **PASS** | OHLC data present and time-aligned. Volume unavailable but not required. |
| 6 | Legitimate counterfactual | **PASS** | Same event class, different velocity trajectory. Mechanism-specific comparison. |
| 7 | Causal claims limited to observables | **PASS** | Hypothesis stated in observable price/range terms. |
| 8 | No future-bar dependency | **PASS** | Velocity computed from bars before the break. |
| 9 | Reproducible | **PASS** | Same data + same definition = same event set. |

**9/9 gates PASS**

### 5.11 Mechanism Assessment

**Hypothesis:** Velocity decay → trapped participants → forced exits → directional amplification.

**Observed:** Treatment and control distributions are nearly identical. No meaningful separation on any metric.

**Assessment: AMBIGUOUS — NOT CONTRADICTED, BUT NOT SUPPORTED.** The tiny positive mean delta (+0.26 bps) is offset by negative median delta (-0.22 bps) and lower win rate (-1.2%). The mechanism may exist but is too weak to detect at this level of analysis, or the observable proxy (range convergence) does not adequately capture the proposed participant-accumulation mechanism.

### 5.12 Absolute vs Conditional Economics

| Dimension | Value |
|---|---|
| Treatment absolute (net mean) | -2.20 bps |
| Control absolute (net mean) | -2.46 bps |
| Conditional delta (mean) | +0.26 bps |
| Conditional delta (median) | -0.22 bps |

The treatment group has marginally better absolute economics (+0.26 bps mean) but marginally worse median and win rate. Neither absolute nor conditional economics are economically meaningful.

### 5.13 Economic Adjudication

> **ECONOMICALLY NEGATIVE**

**Rationale:**
- Net mean is -2.20 bps (negative absolute economics)
- Conditional mean delta is +0.26 bps (trivially small)
- Conditional median delta is -0.22 bps (opposite direction from hypothesis)
- Win rate delta is -1.2% (opposite direction from hypothesis)
- Distribution is indistinguishable between treatment and control
- Top 10% contribution is identical (~300% share, meaning the mean is entirely driven by top decile)
- Exclude-best-event mean is nearly identical (-2.45 vs -2.59 bps)
- Mechanism is ambiguous — not contradicted but not supported

**The candidate demonstrates no economically meaningful incremental information from acceptance velocity decay.**

### 5.14 State Potential

> **NOT JUSTIFIED**

The treatment does not demonstrate conditional information beyond the control. No State classification is warranted.

### 5.15 Governance Decision

> **CLOSED — NO INCREMENTAL INFORMATION**

CAND-089 does not survive G1. The acceptance velocity decay mechanism does not produce economically distinguishable outcomes from the control.

---

## 6. CAND-091 — Cumulative Directional Exhaustion

### 6.1 Frozen Definition

- **Market:** USATECHIDXUSD
- **Timeframe:** M1
- **Date range:** 2023-09-01 to 2026-07-10 (2.9 years, 1,043 days)
- **Exhaustion window:** 100 bars (cumulative directional distance)
- **Exhaustion threshold:** 70th percentile of |cumulative return| in bps
- **Structural level:** 20-bar rolling high/low
- **Breakout threshold:** 3 bps
- **Rearm:** 60-bar minimum
- **Holding period:** 60 bars (60 min)
- **Cost model:** 2 bps friction
- **Direction:** WITH the break (long if up break, short if down break)

### 6.2 Data and Coverage

- Source: `data/m1/USATECHIDXUSD_M1.csv`
- Rows: 906,815
- Coverage: 2023-09-01 00:00:00 to 2026-07-10 20:14:00
- Volume: UNAVAILABLE

### 6.3 Population

| Group | N | % |
|---|---|---|
| Exhausted (treatment) | 3,886 | 46.1% |
| Non-exhausted (control) | 4,535 | 53.9% |
| **Total** | **8,421** | |

### 6.4 Frequency

| Metric | Value |
|---|---|
| Exhausted events/year | 1,361 |
| Non-exhausted events/year | 1,588 |
| Total events/year | 2,949 |

### 6.5 Gross Economics

| Metric | Exhausted (Treatment) | Non-exhausted (Control) |
|---|---|---|
| Gross Mean | -0.69 bps | -0.02 bps |
| Gross Median | -1.13 bps | -0.75 bps |

### 6.6 Net Economics

| Metric | Exhausted (Treatment) | Non-exhausted (Control) |
|---|---|---|
| Net Mean | **-2.69 bps** | **-2.02 bps** |
| Net Median | **-3.13 bps** | **-2.75 bps** |
| Win Rate | 45.1% | 43.6% |
| Std Dev | 49.79 bps | 29.78 bps |

### 6.7 Distribution

| Percentile | Exhausted | Non-exhausted |
|---|---|---|
| P10 | -45.04 bps | -30.78 bps |
| P25 | -21.77 bps | -15.20 bps |
| P50 | -3.13 bps | -2.75 bps |
| P75 | +16.29 bps | +10.06 bps |
| P90 | +39.47 bps | +27.88 bps |

**Distribution assessment:** Exhausted group has wider dispersion (std 49.79 vs 29.78 bps) and fatter tails in both directions. The P10 and P90 values show the exhausted group has more extreme outcomes. However, the WORSE tail (P10) is much worse for exhausted (-45.04 vs -30.78 bps), which hurts net economics more than the better tail helps.

**Top 10% contribution:**
- Exhausted: +29,404.4 bps of -10,452.4 bps total
- Non-exhausted: +23,767.8 bps of -9,174.3 bps total

**Exclude-best-event mean:**
- Exhausted: -2.95 bps
- Non-exhausted: -2.07 bps

**Worst event:**
- Exhausted: -1,045.90 bps
- Non-exhausted: -422.33 bps

### 6.8 Counterfactual

**Treatment:** Structural breaks occurring during cumulative directional exhaustion (|cumulative return| > 22.2 bps over 100-bar window).

**Control:** Structural breaks occurring during non-exhausted conditions (|cumulative return| ≤ 22.2 bps).

**Counterfactual quality:** Well-defined. Same event class, same market, same timeframe, same cost model. Only difference: exhaustion condition. The mechanism specifically requires exhaustion — this comparison isolates the hypothesized effect.

### 6.9 Conditional Delta

| Metric | Value |
|---|---|
| Mean Delta | **-0.67 bps** |
| Median Delta | **-0.39 bps** |
| WR Delta | **+1.4%** |

**Interpretation:** The treatment group (exhausted) performs WORSE than the control on mean and median. The win rate is slightly higher for exhausted (+1.4%), but this is overwhelmed by the larger magnitude losses. The direction is: exhausted → WORSE economics → hypothesis contradicted.

### 6.10 Nine Hard Gates

| # | Gate | Result | Evidence |
|---|---|---|---|
| 1 | Deterministic definition | **PASS** | 100-bar cumulative distance + 70th percentile threshold + structural breaks. Fully reproducible. |
| 2 | Executable entry | **PASS** | Exhaustion is measured before/at the break; entry is at the break. |
| 3 | No hindsight contamination | **PASS** | No post-entry filtering. No MFE/MAE dependency. |
| 4 | Correct cost normalization | **PASS** | 2 bps friction applied consistently. |
| 5 | Data integrity | **PASS** | OHLC data present. Volume unavailable but not required. |
| 6 | Legitimate counterfactual | **PASS** | Same event class, different exhaustion condition. Mechanism-specific. |
| 7 | Causal claims limited to observables | **PASS** | Hypothesis stated in observable price/distance terms. |
| 8 | No future-bar dependency | **PASS** | Exhaustion computed from prior bars. |
| 9 | Reproducible | **PASS** | Same data + same definition = same event set. |

**9/9 gates PASS**

### 6.11 Mechanism Assessment

**Hypothesis:** Exhaustion → participant depletion → counter-trend amplification → larger counter-trend moves.

**Observed:** Exhausted group performs WORSE than non-exhausted. Mean delta is -0.67 bps (control superior). Median delta is -0.39 bps (control superior).

**Assessment: CONTRADICTED.** The directional hypothesis is contradicted: exhaustion produces WORSE, not better, downstream economics. The wider dispersion (std 49.79 vs 29.78 bps) and fatter negative tail (P10: -45.04 vs -30.78 bps) mean that exhaustion adds RISK without adding RETURN.

**Direction-specific analysis confirms the contradiction:**

| Group | Direction | N | Net Mean | Net Median | WR |
|---|---|---|---|---|---|
| Exhausted | Long | 1,933 | -0.17 | -0.33 | 49.2% |
| Exhausted | Short | 1,953 | -5.18 | -6.09 | 40.9% |
| Non-exhausted | Long | 2,136 | -1.70 | -1.64 | 45.9% |
| Non-exhausted | Short | 2,399 | -2.31 | -3.68 | 41.6% |

The exhausted group has better longs (-0.17 vs -1.70 bps) but much worse shorts (-5.18 vs -2.31 bps). The net effect is dominated by the short underperformance. This asymmetry suggests the exhaustion mechanism may affect longs and shorts differently, but the overall hypothesis (exhaustion → better economics) is contradicted.

### 6.12 Absolute vs Conditional Economics

| Dimension | Value |
|---|---|
| Treatment absolute (net mean) | -2.69 bps |
| Control absolute (net mean) | -2.02 bps |
| Conditional delta (mean) | -0.67 bps |
| Conditional delta (median) | -0.39 bps |

Both absolute and conditional economics are negative. The treatment is worse on both dimensions.

### 6.13 Economic Adjudication

> **ECONOMICALLY NEGATIVE — HYPOTHESIS CONTRADICTED**

**Rationale:**
- Net mean is -2.69 bps (negative absolute economics, worse than control)
- Conditional mean delta is -0.67 bps (control superior — contradicts hypothesis)
- Conditional median delta is -0.39 bps (control superior)
- Win rate is slightly higher for exhausted (+1.4%) but overwhelmed by larger losses
- Exhausted group has 67% higher dispersion (49.79 vs 29.78 bps)
- Worst event is much worse for exhausted (-1,045.90 vs -422.33 bps)
- P10 (downside tail) is much worse for exhausted (-45.04 vs -30.78 bps)
- Exclude-best-event mean is worse for exhausted (-2.95 vs -2.07 bps)
- The mechanism is contradicted: exhaustion adds risk without return

**The candidate demonstrates that cumulative directional exhaustion WORSENS downstream economics, contradicting the hypothesis.**

### 6.14 State Potential

> **NOT JUSTIFIED — NEGATIVE CONDITIONAL INFORMATION**

The treatment does not provide positive conditional information. No State classification is warranted.

### 6.15 Governance Decision

> **CLOSED — HYPOTHESIS CONTRADICTED**

CAND-091 does not survive G1. The cumulative directional exhaustion mechanism produces worse, not better, downstream economics.

---

## 7. Candidate Comparison

| Dimension | CAND-089 | CAND-091 |
|---|---|---|
| Treatment N | 4,152 | 3,886 |
| Control N | 4,269 | 4,535 |
| Treatment Net Mean | -2.20 bps | -2.69 bps |
| Control Net Mean | -2.46 bps | -2.02 bps |
| Mean Delta | +0.26 bps | -0.67 bps |
| Median Delta | -0.22 bps | -0.39 bps |
| WR Delta | -1.2% | +1.4% |
| Mechanism | AMBIGUOUS | CONTRADICTED |
| Decision | CLOSED — NO INCREMENTAL INFO | CLOSED — HYPOTHESIS CONTRADICTED |

## 8. Economic Evidence Comparison

Both candidates show negative absolute economics (net mean < -2 bps). Neither demonstrates economically meaningful incremental information from its proposed mechanism.

CAND-089 shows near-zero conditional deltas (mean +0.26, median -0.22) with contradictory evidence across metrics. The mechanism is ambiguous — not supported but not clearly contradicted.

CAND-091 shows clearly negative conditional deltas (mean -0.67, median -0.39) with the treatment performing WORSE than the control. The mechanism is contradicted.

## 9. Counterfactual Quality

Both candidates have well-constructed counterfactuals:
- Same event class (structural level break)
- Same market, timeframe, holding period
- Same cost model
- Only difference: the proposed mechanism (velocity trajectory / exhaustion condition)

The counterfactuals are legitimate and discriminating. The failure is in the mechanism, not the experimental design.

## 10. Distribution / Tail Assessment

| Metric | CAND-089 | CAND-091 |
|---|---|---|
| Treatment std dev | 42.43 bps | 49.79 bps |
| Control std dev | 38.05 bps | 29.78 bps |
| Treatment P10 | -36.96 bps | -45.04 bps |
| Control P10 | -37.40 bps | -30.78 bps |
| Treatment worst | -1,045.90 bps | -1,045.90 bps |
| Control worst | -475.92 bps | -422.33 bps |

CAND-091's exhaustion condition adds significantly to dispersion and downside tail risk without compensating return. This is the opposite of what the hypothesis predicted.

## 11. Nine-Gate Summary

| Gate | CAND-089 | CAND-091 |
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

Both candidates pass all nine hard validity gates. The failures are in economic evidence, not measurement validity.

## 12. Prior-Art Integrity

- CAND-089: NEW (confirmed by V30 G0 integrity audit)
- CAND-091: NEW (confirmed by V30 G0 integrity audit)
- CAND-090: CLOSED / REDUNDANT (not tested)

## 13. State Library Impact

**NO CHANGE**

Existing State objects preserved:
- CAND-077: STATE REVIEW ELIGIBLE
- CAND-081: STATE REVIEW ELIGIBLE
- CAND-083: STATE REVIEW ELIGIBLE
- CAND-059: STATE-ARTIFACT
- CAND-065: STATE OBSERVATION
- CAND-069: STATE OBSERVATION
- CAND-079: STATE OBSERVATION

## 14. Relational Framework Status

> RELATIONAL FRAMEWORK = GOVERNED

SEED-002: TESTED NEGATIVE — NO INCREMENTAL INFORMATION

No new relational hypothesis registered during V30 G1.

## 15. SEED-002 Negative Knowledge

Preserved:

| Metric | Treatment (CAND-081 WITH CAND-083) | Control (CAND-081 WITHOUT CAND-083) |
|---|---|---|
| N | 4,917 | 1,784 |
| Net Mean | -1.96 bps | -0.19 bps |
| Net Median | -1.61 bps | -0.90 bps |
| WR | 46.1% | 48.7% |
| Delta | -1.78 bps | |

## 16. APEX RB001–RB004 Firewall

> DESIGNED — NOT EXECUTED

APEX modular research branches were not used, evaluated, or compared during V30 G1.

## 17. CAND-090 / CAND-087 Firewall

> CAND-090: CLOSED / REDUNDANT WITH CAND-087 — NOT TESTED
> CAND-087: NOT REOPENED

## 18. Closed-Line Firewall

> PASS

No V19–V29 closed hypothesis was reopened or used as a positive input.

## 19. Forward Runtime Protection

CAND-015/024/035: **ACTIVE / PROTECTED / UNTOUCHED**

No forward performance was inspected.

## 20. G2

> **NOT EXECUTED**

Neither candidate qualifies for G2. Both are closed.

## 21. System Assembly

> **NOT EXECUTED**

## 22. Confirmation Requirements

Neither candidate warrants confirmation. Both are closed at G1.

CAND-089: NO INCREMENTAL INFORMATION — not promising enough for confirmation.
CAND-091: HYPOTHESIS CONTRADICTED — confirmation would be pointless.

## 23. Final Economic Adjudication

### CAND-089

> **CLOSED — ECONOMICALLY NEGATIVE / NO INCREMENTAL INFORMATION**

Acceptance velocity decay does not produce economically distinguishable outcomes from the control. The mechanism may exist but is too weak to detect, or the observable proxy does not capture the proposed participant-accumulation mechanism.

### CAND-091

> **CLOSED — ECONOMICALLY NEGATIVE / HYPOTHESIS CONTRADICTED**

Cumulative directional exhaustion produces WORSE downstream economics, not better. The exhaustion condition adds dispersion and downside tail risk without compensating return. The hypothesis is contradicted.

## 24. Integrity Verification

| Check | Status |
|---|---|
| Exactly two candidates tested | ✓ |
| CAND-089 tested using frozen definition | ✓ |
| CAND-091 tested using frozen definition | ✓ |
| CAND-090 was NOT tested | ✓ |
| CAND-087 was NOT reopened | ✓ |
| No replacement candidate generated | ✓ |
| No thresholds optimized | ✓ |
| No parameter search occurred | ✓ |
| No relational test occurred | ✓ |
| SEED-002 was not retested | ✓ |
| No State interaction occurred | ✓ |
| APEX RB001–RB004 were not executed | ✓ |
| No forward runtime performance inspected | ✓ |
| Nine hard gates applied | ✓ |
| Counterfactuals not redesigned post-outcome | ✓ |
| Gross/net economics kept distinct | ✓ |
| Absolute vs conditional economics separated | ✓ |
| Mean and median both evaluated | ✓ |
| Distribution/tail dependence assessed | ✓ |
| No unsupported causal claim made | ✓ |
| No confirmation executed | ✓ |
| No G2 executed | ✓ |
| No System Assembly occurred | ✓ |
| SESSION_HANDOFF is accurate and verified | ✓ |

---

**Artifact:** `output/research_discovery/RESEARCH_FACTORY_V2_G1_SCREEN_20260831_V30.md`
**Script:** `research/v30_g1_experiment.py`
