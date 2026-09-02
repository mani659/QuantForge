# QUANTFORGE — V34 G1 ECONOMIC PLAUSIBILITY SCREEN

## CAND-101 + CAND-102

**Date:** 2026-09-02
**Status:** COMPLETE — BOTH CANDIDATES CLOSED
**Market:** USATECHIDXUSD M1
**Data range:** 2023-09-01 to 2026-07-10 (~2.9 years, 906,815 bars)
**Cost assumption:** 2 bps round-trip friction

---

## 1. Mission

Execute V34 G1 Economic Plausibility Screen for CAND-101 (Path-Dependent Sequence Asymmetry) and CAND-102 (Directional Momentum Persistence).

This is the first G1 execution under the refined G0 process with Mechanism-Observable Challenge.

---

## 2. Authoritative Inputs

- V34 G0: `output/research_discovery/TRADEABLE_EDGE_DISCOVERY_SCREENING_V34.md`
- V34 G0 Integrity Audit: `output/research_discovery/QUANTFORGE_V34_G0_INTEGRITY_AUDIT_V1.md`
- G1 V3 Framework: `output/research_discovery/QUANTFORGE_G1_ECONOMIC_QUALIFICATION_FRAMEWORK_V3_RATIFICATION_V1.md`
- G0 Process Refinement: `output/research_discovery/QUANTFORGE_G0_MECHANISM_OBSERVABLE_CHALLENGE_V1.md`

---

## 3. Frozen Candidate Definitions

### CAND-101 — Path-Dependent Sequence Asymmetry

- **Research question:** Does the ORDER of two structural events (break-then-retest vs retest-then-break) produce different subsequent economics?
- **Expression class:** STATE / CONDITION
- **Mechanism family:** Path-Dependent Sequencing
- **Treatment:** B→R sequence (break followed by retest)
- **Control:** R→B sequence (retest followed by break)
- **Expected effect:** B→R produces tighter distributions; R→B produces wider distributions
- **Outcome horizon:** 60 bars on M1

### CAND-102 — Directional Momentum Persistence

- **Research question:** Do repeated same-direction structural breaks create a subsequent directional bias consistent with persistence/reinforcement?
- **Expression class:** STATE / CONDITION
- **Mechanism family:** Directional Dynamics
- **Observable:** Run length of consecutive same-direction structural breaks
- **Expected effect:** Higher run lengths produce stronger directional persistence
- **Outcome horizon:** 60 bars on M1
- **Trend-control requirement:** Must distinguish structural-event persistence from ordinary trend persistence

---

## 4. Experiment/Data Identity

- **Dataset:** USATECHIDXUSD M1
- **Date range:** 2023-09-01 to 2026-07-10
- **Bars:** 906,815
- **Break detection:** ATR-based (1.5x ATR, 100-bar ATR lookback)
- **Retest detection:** Price returns within 0.3x ATR of break level within 30 bars
- **Cost model:** 2 bps round-trip
- **Script:** `research/v34_g1_experiment.py`
- **Execution environment:** Python 3.11, pandas, numpy

---

## 5. Nine Hard Validity Gates

### CAND-101

| Gate | PASS/FAIL | Evidence |
|---|---|---|
| 1. Deterministic definition | PASS | Break and retest detection are deterministic from OHLC |
| 2. Executable entry | PASS | Sequence classification occurs at second event completion |
| 3. No hindsight contamination | PASS | No post-entry signal definition |
| 4. Correct cost normalization | PASS | 2 bps round-trip applied consistently |
| 5. Data integrity | PASS | M1 OHLC data sufficient for break/retest detection |
| 6. Legitimate counterfactual | PASS | Same event class, different sequence order |
| 7. Causal claims limited to observables | PASS | Hypothesis stated in observable event-order terms |
| 8. No future-bar dependency | PASS | Computable from historical events only |
| 9. Reproducible | PASS | Deterministic from OHLC data |

### CAND-102

| Gate | PASS/FAIL | Evidence |
|---|---|---|
| 1. Deterministic definition | PASS | Break detection and run-length computation are deterministic |
| 2. Executable entry | PASS | Run length computed from past breaks only |
| 3. No hindsight contamination | PASS | No post-entry signal definition |
| 4. Correct cost normalization | PASS | 2 bps round-trip applied consistently |
| 5. Data integrity | PASS | M1 OHLC data sufficient for break detection |
| 6. Legitimate counterfactual | PASS | Same event class, different run lengths |
| 7. Causal claims limited to observables | PASS | Hypothesis stated in observable run-length terms |
| 8. No future-bar dependency | PASS | Computable from historical breaks only |
| 9. Reproducible | PASS | Deterministic from OHLC data |

**All 9 hard gates PASS for both candidates.**

---

## 6. CAND-101 Implementation Verification

### Event Definition

- **Structural break:** Bar range > 1.5x ATR(100)
- **Retest:** Price returns within 0.3x ATR of break level within 30 bars of break
- **Sequence classification:**
  - B→R: break event followed by retest event (within 30 bars)
  - R→B: retest event followed by new break event (within 30 bars)
- **Minimum spacing:** 5 bars between sequence events

### Semantic Freeze Verification

| Element | G0 Definition | G1 Implementation | Match |
|---|---|---|---|
| Event A | Structural break | Bar range > 1.5x ATR | YES |
| Event B | Retest | Price returns within 0.3x ATR | YES |
| Sequence ordering | B→R vs R→B | Classified from event timestamps | YES |
| Outcome window | H bars after second event | 60 bars after second event | YES |

**Semantic integrity:** PASS — G0 definition = G1 implementation.

---

## 7. CAND-101 Sample Construction

- **Structural breaks detected:** 124,807 (60,246 up, 64,561 down)
- **Retests detected:** 118,682
- **Total sequences classified:** 35,194
- **B→R sequences:** 556
- **R→B sequences:** 34,635

### Critical Observation

**Massive sample imbalance:** R→B sequences are 62x more common than B→R sequences. This is because:
- R→B: any retest followed by any break (very common — most breaks follow some prior retest)
- B→R: break followed by retest within 30 bars (less common — requires specific timing)

This imbalance is a **structural property of the event definitions**, not an artifact. It means:
- B→R is a rare, specific pattern
- R→B is a common, generic pattern
- The two groups may differ in ways beyond sequence order (frequency, market context)

---

## 8. CAND-101 Economic Results

| Metric | B→R (Treatment) | R→B (Control) | Delta |
|---|---|---|---|
| N | 556 | 34,635 | — |
| Gross Mean | +0.58 bps | +0.60 bps | -0.02 bps |
| Gross Median | +0.44 bps | +0.97 bps | -0.53 bps |
| Net Mean | -1.42 bps | -1.40 bps | -0.02 bps |
| Net Median | -1.56 bps | -1.03 bps | -0.53 bps |
| Win Rate | 52.3% | 53.2% | -0.9% |
| Std Dev | 22.20 bps | 28.38 bps | -6.18 bps |

### Interpretation

- **Mean delta is essentially zero** (-0.02 bps). The two sequence types produce virtually identical central tendency.
- **Median delta is negative** (-0.53 bps). R→B actually has a slightly better median.
- **Win rate delta is negative** (-0.9%). R→B has a slightly higher win rate.
- **Std dev is lower for B→R** (22.20 vs 28.38 bps). B→R has tighter distributions, consistent with the expected effect.
- **However:** The distribution width difference may simply reflect that B→R is a rarer, more specific pattern (smaller N, less variance) rather than a genuine economic mechanism.

### Hypothesis Assessment

The hypothesis predicted:
- B→R produces tighter distributions ✅ (confirmed: 22.20 vs 28.38 bps std)
- B→R produces better economics ❌ (contradicted: -0.02 bps mean delta)

The distribution width hypothesis is partially supported, but the economic hypothesis is contradicted. The tighter distributions of B→R do not translate into better economics.

---

## 9. CAND-101 Adjudication

### Evidence Profile

- Mean delta: -0.02 bps (essentially zero)
- Median delta: -0.53 bps (control superior)
- WR delta: -0.9% (control superior)
- Distribution width: B→R tighter (consistent with hypothesis)
- Sample imbalance: R→B 62x more common than B→R

### Classification

> **CLOSED — ECONOMICALLY NEGATIVE**

**Rationale:** The sequence order produces virtually no economic separation. The mean delta is -0.02 bps (essentially zero). The median and win rate slightly favor the control (R→B). The distribution width difference (B→R tighter) is consistent with the hypothesis but does not translate into economic value. The massive sample imbalance (62:1) suggests the two groups differ in market context beyond sequence order, making clean interpretation difficult.

**Mechanism interpretation:** The sequence order does not produce economically meaningful differences in central tendency. The distribution width difference may be a sample-size artifact rather than a genuine economic mechanism.

---

## 10. CAND-102 Implementation Verification

### Event Definition

- **Structural break:** Bar range > 1.5x ATR(100)
- **Run length:** Consecutive same-direction breaks
- **Signal:** End-of-run observation (after N same-direction breaks)
- **Outcome horizon:** 60 bars after signal

### Trend-Control Verification

The G0 integrity audit identified trend confound risk. The G1 implementation computes a basic trend measure (200-bar return) for context but does NOT implement a formal trend-control filter (as none was predeclared in the frozen protocol).

**Trend-control limitation:** The frozen G0/G0-audit protocol did not predeclare a specific trend-control methodology. The G1 experiment reports the trend measure for context but cannot definitively distinguish structural-event persistence from ordinary trend persistence.

---

## 11. CAND-102 Trend-Control Verification

### Trend Measure

200-bar return (simple price change over 200 bars).

### Trend by Run Length

| Run Length | Trend Mean (200-bar return) |
|---|---|
| 3 | -1.71 bps |
| 4 | -1.26 bps |
| 5 | -3.16 bps |
| 6 | -2.84 bps |
| 7 | -5.87 bps |
| 8 | -7.89 bps |
| 9 | -3.96 bps |
| 10 | +1.54 bps |

**Observation:** The trend measure shows that longer runs tend to occur in more negatively trending periods. This is consistent with the idea that same-direction breaks cluster in trending markets, but the relationship is noisy and non-monotonic.

### Trend-Control Assessment

Without a predeclared trend-control methodology, the G1 experiment cannot definitively separate:
- Structural-event persistence (the hypothesized mechanism)
- Ordinary trend persistence (the alternative explanation)

This is a **methodology limitation**, not a measurement failure. The frozen protocol did not predeclare a trend-control filter.

---

## 12. CAND-102 Sample Construction

- **Total breaks:** 124,807
- **End-of-run observations:** 61,302
- **Run length distribution:**

| Run Length | N |
|---|---|
| 3 | 7,735 |
| 4 | 3,849 |
| 5 | 1,969 |
| 6 | 1,048 |
| 7 | 527 |
| 8 | 288 |
| 9 | 154 |
| 10 | 67 |

**Sample adequacy:** Run lengths 3–5 have adequate sample sizes. Run lengths 6+ have smaller samples but are still usable for directional analysis.

---

## 13. CAND-102 Economic Results

| Run Length | N | Gross Mean | Net Mean | WR | Std | Trend |
|---|---|---|---|---|---|---|
| 3 | 7,735 | +0.42 | -1.58 | 52.8% | 33.31 | -1.71 |
| 4 | 3,849 | +0.87 | -1.13 | 53.1% | 39.92 | -1.26 |
| 5 | 1,969 | +3.21 | +1.21 | 53.5% | 52.84 | -3.16 |
| 6 | 1,048 | -0.62 | -2.62 | 51.6% | 34.39 | -2.84 |
| 7 | 527 | -0.64 | -2.64 | 54.6% | 33.53 | -5.87 |
| 8 | 288 | -1.24 | -3.24 | 50.3% | 30.74 | -7.89 |
| 9 | 154 | +4.74 | +2.74 | 59.1% | 33.99 | -3.96 |
| 10 | 67 | -0.24 | -2.24 | 49.3% | 25.27 | +1.54 |

### Interpretation

- **No monotonic relationship:** Returns do not increase monotonically with run length. Run length 5 shows the strongest positive result (+3.21 bps gross, +1.21 bps net), but run lengths 6–8 are negative.
- **Run length 9 is positive** (+4.74 bps) but N=154 is marginal.
- **The pattern is non-monotonic and noisy.** This is not consistent with a clean persistence mechanism.
- **Trend context:** Longer runs occur in more negatively trending periods (trend mean becomes more negative), which may explain why longer runs produce worse returns — they are occurring in unfavorable trend environments.

### Hypothesis Assessment

The hypothesis predicted:
- Higher run lengths produce stronger directional persistence ❌ (contradicted: no monotonic relationship)

The evidence does NOT support the persistence hypothesis. The relationship between run length and forward returns is non-monotonic and noisy.

---

## 14. CAND-102 Adjudication

### Evidence Profile

- No monotonic relationship between run length and forward returns
- Run length 5 shows strongest positive result (+3.21 bps gross) but this is isolated
- Run lengths 6–8 are negative
- Trend context shows longer runs occur in more negatively trending periods
- No predeclared trend-control filter to isolate structural-event persistence

### Classification

> **CLOSED — HYPOTHESIS CONTRADICTED**

**Rationale:** The persistence hypothesis predicted that higher run lengths would produce stronger directional persistence. The evidence shows no monotonic relationship — returns peak at run length 5 and decline afterward. The pattern is non-monotonic and noisy.

**Mechanism interpretation:** The observed pattern is more consistent with ordinary trend dynamics (longer runs occur in trending markets, which may be unfavorable) than with structural-event persistence. Without a predeclared trend-control filter, the structural-event mechanism cannot be isolated.

**Observable information:** The non-monotonic pattern (peak at run length 5) is interesting but not consistent with the registered hypothesis. It may reflect sample composition effects rather than a genuine economic mechanism.

---

## 15. Cross-Candidate Interpretation

Both candidates failed to produce economically meaningful conditional separation:

- **CAND-101:** Sequence order produces virtually no economic difference (mean delta -0.02 bps)
- **CAND-102:** Run length shows no monotonic relationship with forward returns

The evidence does not represent useful information for either candidate.

---

## 16. Mechanism vs Observable Information

### CAND-101

- **Mechanism (sequence interpretation):** CONTRADICTED — sequence order does not produce economic differences
- **Observable (distribution width):** PARTIALLY SUPPORTED — B→R has tighter distributions, but this does not translate to economics
- **Overall:** The observable contains some distributional information but no economic information

### CAND-102

- **Mechanism (participant capitulation):** NOT ISOLATED — cannot distinguish from ordinary trend dynamics
- **Observable (run-length pattern):** NON-MONOTONIC — peak at run length 5 is isolated, not a clean pattern
- **Overall:** The observable does not contain clean information consistent with the registered hypothesis

---

## 17. Limitations

1. **CAND-101 sample imbalance:** B→R sequences are 62x rarer than R→B, making clean comparison difficult
2. **CAND-102 trend confound:** No predeclared trend-control filter to isolate structural-event persistence from ordinary trend dynamics
3. **Single instrument/timeframe:** Results specific to USATECHIDXUSD M1
4. **Cost assumption:** 2 bps round-trip — effects smaller than 2 bps cannot survive costs

---

## 18. Governance Disposition

| Candidate | N (T/C) | Hard Gates | Net Mean | Net Median | WR | Mean Delta | Final Classification |
|---|---|---|---|---|---|---|---|
| CAND-101 | 556 / 34,635 | 9/9 PASS | -1.42 / -1.40 bps | -1.56 / -1.03 bps | 52.3% / 53.2% | -0.02 bps | ECONOMICALLY NEGATIVE |
| CAND-102 | 7,735 (run=3) to 67 (run=10) | 9/9 PASS | varies by run length | varies by run length | varies | non-monotonic | HYPOTHESIS CONTRADICTED |

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

## 19. Reproducibility

- **Dataset:** USATECHIDXUSD M1 (`data/m1/USATECHIDXUSD_M1.csv`)
- **Date range:** 2023-09-01 to 2026-07-10
- **Bars:** 906,815
- **Cost assumption:** 2 bps round-trip
- **Script:** `research/v34_g1_experiment.py`
- **Frozen parameters:**
  - Break threshold: 1.5x ATR(100)
  - Retest tolerance: 0.3x ATR
  - Max retest window: 30 bars
  - Min sequence separation: 5 bars
  - Outcome horizon: 60 bars
  - Trend lookback: 200 bars
- **Execution environment:** Python 3.11, pandas, numpy

---

*V34 G1 complete. Both candidates closed. No G2 promotions. V34 permanently closed.*
