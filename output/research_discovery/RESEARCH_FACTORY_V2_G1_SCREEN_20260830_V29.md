# RESEARCH FACTORY V2 — G1 ECONOMIC PLAUSIBILITY SCREEN — V29
# DATE: 2026-08-30
# STATUS: V29 G1 COMPLETE — 0 G2 PROMOTIONS — 3 CANDIDATES CLOSED
# NO G2 / NO V30 / NO OPTIMIZATION

---

## 1. G1 Status

> V29 G1 COMPLETE

All three V29 candidates evaluated under G1 V3 framework. No G2 promotions. No State Review Eligible candidates. All three closed.

---

## 2. V29 G0 Recap

V29 G0 generated three genuinely new candidates:
- CAND-086: Information Absorption Failure Cascade
- CAND-087: Recovery Quality Differential
- CAND-088: Session Sequence Asymmetry

All three were NEW (no overlap with V19–V28). All three used USATECHIDXUSD M1 OHLC data.

---

## 3. G1 V3 Framework

Ratified. Two-layer architecture:
- **Layer 1:** 9 binary hard validity gates (measurement integrity)
- **Layer 2:** Economic evidence adjudication (holistic, not scorecard)

No universal hard economic thresholds.

---

## 4. Candidate Evaluation Summary

| Candidate | N | Freq | Net Mean | Net Median | CF N | CF Net | Delta Mean | Delta Median | CF Verdict | Adjudication |
|---|---|---|---|---|---|---|---|---|---|---|
| CAND-086 | 10,198 | 3,571/yr | -2.06 | -2.13 | 21,738 | -2.12 | +0.07 | -0.03 | MIXED | ECONOMICALLY NEGATIVE |
| CAND-087 | 9,930 | 3,477/yr | -1.91 | -2.03 | 6,638 | -2.14 | +0.23 | -0.03 | MIXED | INFORMATIONALLY INTERESTING |
| CAND-088 | 222 | 79/yr | -15.51 | -10.62 | 556 | +4.07 | -19.59 | -11.39 | COUNTERFACTUAL SUPERIOR | ECONOMICALLY NEGATIVE |

---

## 5. CAND-086 — Information Absorption Failure Cascade

### Definition
Repeated failed directional moves (>1.5× ATR that reverse >50% within 5 bars) create trapped-participant state. When count ≥3 in 20-bar lookback, next sustained directional move (>50% sustained for 5+ bars) has larger continuation.

### Mechanism
Information Absorption / Failure family. Cumulative failed directional conviction traps participants across multiple sides.

### Frozen Parameters
- Lookback: 20 M1 bars
- ATR period: 20 bars
- Large move threshold: 1.5× ATR
- Reversal threshold: 50% within 5 bars
- Absorption failure count: ≥3
- Confirmation: sustained >50% for 5+ bars
- Holding period: 20 bars

### Hard Gates
| Gate | Result |
|---|---|
| 1. Event objectively definable | PASS |
| 2. Treatment precisely defined | PASS |
| 3. Counterfactual defined | PASS |
| 4. No hindsight in definition | PASS |
| 5. Sufficient sample size | PASS (N=10,198) |
| 6. Time coverage adequate | PASS |
| 7. No survivorship bias | PASS |
| 8. Execution feasible | PASS |
| 9. Counterfactual valid | PASS |

**Result: 9/9 PASS**

### Economic Evidence
- N=10,198, Freq=3,571/yr
- Gross Mean: -0.06 bps, Gross Median: -0.13 bps
- Net Mean: **-2.06 bps**, Net Median: **-2.13 bps**
- WR: 49.2%
- Std: 16.78 bps
- Worst: -433.11 bps, Best: +236.56 bps

### Counterfactual
- CF N=21,738
- CF Net Mean: -2.12 bps, CF Net Median: -2.09 bps
- CF WR: 49.4%

### Conditional Delta
- Mean: **+0.07 bps** (TREATMENT +0.07 vs CF -2.12)
- Median: **-0.03 bps** (TREATMENT -2.13 vs CF -2.09)
- Verdict: **MIXED** — negligible mean, slightly negative median

### Distribution Evidence
Mean and median deltas are both negligible. The conditional relationship is economically meaningless. The treatment is essentially identical to the counterfactual.

### Absolute Economics
Negative (-2.06 bps net mean). NOT a standalone Alpha.

### Economic Headroom
No headroom. The conditional delta is +0.07 bps mean — negligible. The mechanism does not produce meaningful economic separation.

### Dynamic-vs-Static
The transition was preserved in the frozen definition. The G1 result shows that the transition does not produce meaningful economic separation.

### Mechanism Integrity
The mechanism is logically coherent but empirically unsupported. The count of absorption failures does not predict subsequent move economics.

### Prior-Art
NEW — no V19–V28 candidate counts failed directional moves.

### State Potential
No. The conditional delta is negligible (+0.07 bps mean). No distinct market condition is demonstrated.

### Alpha Potential
No. Absolute economics negative and conditional delta negligible.

### Rare-Event Potential
No. High frequency (3,571/yr) is not a rare event.

### Failure Mode
The absorption failure count does not create a meaningful trapped-participant state, or the state does not produce measurable economic consequences.

### G1 Decision
> **ECONOMICALLY NEGATIVE — CLOSED**

The conditional delta is negligible (+0.07 bps mean, -0.03 bps median). No economic mechanism is demonstrated.

### Next-Stage Eligibility
Not eligible for any next stage.

---

## 6. CAND-087 — Recovery Quality Differential

### Definition
After large disturbance (>2× ATR), measure recovery quality over 10 bars. Weak recovery (<25% recovered) indicates trapped participants remain. Strong recovery (>75%) indicates resolution. Treatment: weak recovery → continue in disturbance direction. Counterfactual: strong recovery → continue in disturbance direction.

### Mechanism
Recovery / Failure of Recovery family. Recovery quality reveals participant constraint state.

### Frozen Parameters
- ATR period: 20 bars
- Disturbance threshold: >2× ATR
- Recovery measurement: 10 bars
- Weak recovery: <25% recovered
- Strong recovery: >75% recovered
- Entry: bar 10 after disturbance
- Holding period: 20 bars
- Direction: disturbance direction

### Hard Gates
| Gate | Result |
|---|---|
| 1. Event objectively definable | PASS |
| 2. Treatment precisely defined | PASS |
| 3. Counterfactual defined | PASS |
| 4. No hindsight in definition | PASS |
| 5. Sufficient sample size | PASS (N=9,930) |
| 6. Time coverage adequate | PASS |
| 7. No survivorship bias | PASS |
| 8. Execution feasible | PASS |
| 9. Counterfactual valid | PASS |

**Result: 9/9 PASS**

### Economic Evidence
- N=9,930, Freq=3,477/yr
- Gross Mean: +0.09 bps, Gross Median: -0.03 bps
- Net Mean: **-1.91 bps**, Net Median: **-2.03 bps**
- WR: 49.7%
- Std: 16.87 bps
- Worst: -438.73 bps, Best: +425.21 bps

### Counterfactual
- CF N=6,638
- CF Net Mean: -2.14 bps, CF Net Median: -2.01 bps
- CF WR: 49.9%

### Conditional Delta
- Mean: **+0.23 bps** (TREATMENT -1.91 vs CF -2.14)
- Median: **-0.03 bps** (TREATMENT -2.03 vs CF -2.01)
- Verdict: **MIXED** — weak positive mean, slightly negative median

### Distribution Evidence
The mean delta (+0.23 bps) is weakly positive. The median delta (-0.03 bps) is essentially zero. The conditional relationship is economically weak and not robust across the distribution.

### Absolute Economics
Negative (-1.91 bps net mean). NOT a standalone Alpha.

### Economic Headroom
Limited. The conditional delta is +0.23 bps mean — weak. The median is negative. The mechanism produces marginal informational separation at best.

### Dynamic-vs-Static
The transition was preserved. The G1 result shows weak conditional separation.

### Mechanism Integrity
The mechanism is logically coherent. Recovery quality may reveal information about participant constraint. However, the empirical evidence shows only marginal separation.

### Prior-Art
NEW — no V19–V28 candidate measures post-disturbance recovery quality.

### State Potential
Weak. The conditional delta (+0.23 bps mean, -0.03 bps median) is too weak for State Review Eligibility. The mechanism is interesting but the evidence does not support formal State classification.

### Alpha Potential
No. Absolute economics negative.

### Rare-Event Potential
No. High frequency (3,477/yr).

### Failure Mode
Recovery quality may not create a meaningful participant-constraint distinction, or the 10-bar measurement window may be insufficient.

### G1 Decision
> **INFORMATIONALLY INTERESTING — CLOSED**

The conditional delta is weak (+0.23 bps mean, -0.03 bps median). The mechanism is interesting but the evidence does not justify State Review Eligibility or Alpha promotion.

### Next-Stage Eligibility
Not eligible for any next stage. The weak conditional evidence does not meet the State Review Eligibility threshold.

---

## 7. CAND-088 — Session Sequence Asymmetry

### Definition
Opening directional bias (first 30 bars) followed by opposite-direction structural break (20-bar rolling high/low). Treatment: opposite-direction break (break opposes opening bias). Counterfactual: aligned-direction break (break matches opening bias). Entry at confirmed break, exit after 30 bars.

### Mechanism
Path Dependence / Event Sequence family. Opening-bias participants trapped when structural break opposes their exposure.

### Frozen Parameters
- Opening bias: first 30 M1 bars
- Structural level: 20-bar rolling high/low from prior session
- Break threshold: close beyond level by >2 bps
- Sequence: opposite vs aligned
- Holding period: 30 bars

### Hard Gates
| Gate | Result |
|---|---|
| 1. Event objectively definable | PASS |
| 2. Treatment precisely defined | PASS |
| 3. Counterfactual defined | PASS |
| 4. No hindsight in definition | PASS |
| 5. Sufficient sample size | PASS (N=222) |
| 6. Time coverage adequate | PASS |
| 7. No survivorship bias | PASS |
| 8. Execution feasible | PASS |
| 9. Counterfactual valid | PASS |

**Result: 9/9 PASS**

### Economic Evidence
- N=222, Freq=79/yr
- Gross Mean: -13.51 bps, Gross Median: -8.62 bps
- Net Mean: **-15.51 bps**, Net Median: **-10.62 bps**
- WR: 20.3%
- Std: 26.18 bps
- Worst: -252.57 bps, Best: +32.76 bps

### Counterfactual
- CF N=556
- CF Net Mean: **+4.07 bps**, CF Net Median: +0.78 bps
- CF WR: 58.3%

### Conditional Delta
- Mean: **-19.59 bps** (TREATMENT -15.51 vs CF +4.07)
- Median: **-11.39 bps** (TREATMENT -10.62 vs CF +0.78)
- Verdict: **COUNTERFACTUAL SUPERIOR** — aligned breaks outperform opposite breaks

### Distribution Evidence
The counterfactual (aligned breaks) is genuinely superior to the treatment (opposite breaks). This is the OPPOSITE of the hypothesized mechanism. The path-dependence hypothesis is contradicted by the evidence.

### Absolute Economics
Very negative for treatment (-15.51 bps net mean). The counterfactual is actually positive (+4.07 bps net mean).

### Economic Headroom
None for the treatment. The counterfactual has positive economics but the treatment (opposite breaks) is strongly negative.

### Dynamic-vs-Static
The path-dependence transition was preserved. The G1 result shows that the sequence is economically meaningful — but in the OPPOSITE direction from the hypothesis. Aligned breaks outperform opposite breaks.

### Mechanism Integrity
The mechanism is logically coherent but empirically contradicted. The hypothesis was that opposite-direction breaks trap opening-bias participants and produce larger continuation. The evidence shows the opposite: aligned breaks produce better economics.

### Prior-Art
NEW — no V19–V28 candidate examines session-opening direction relative to structural break direction.

### State Potential
No. The evidence contradicts the mechanism. The path-dependence exists but operates in the opposite direction from the hypothesis.

### Alpha Potential
No. The treatment (opposite breaks) is strongly negative. The counterfactual (aligned breaks) is positive but was not the hypothesis.

### Rare-Event Potential
No. Frequency is moderate (79/yr).

### Failure Mode
The hypothesis was wrong. Opening-bias participants may not be trapped by opposite-direction breaks, or the trapped-participant mechanism may not operate at the session level.

### G1 Decision
> **ECONOMICALLY NEGATIVE — COUNTERFACTUAL SUPERIOR — CLOSED**

The evidence contradicts the hypothesized mechanism. Aligned breaks outperform opposite breaks. The path-dependence exists but operates in the opposite direction.

### Next-Stage Eligibility
Not eligible for any next stage. The mechanism is contradicted.

---

## 8. Cross-Candidate Economic Comparison

| Candidate | Net Mean | CF Net | Delta Mean | Delta Median | Adjudication |
|---|---|---|---|---|---|
| CAND-086 | -2.06 | -2.12 | +0.07 | -0.03 | ECONOMICALLY NEGATIVE |
| CAND-087 | -1.91 | -2.14 | +0.23 | -0.03 | INFORMATIONALLY INTERESTING |
| CAND-088 | -15.51 | +4.07 | -19.59 | -11.39 | ECONOMICALLY NEGATIVE |

All three have negative absolute economics. CAND-087 has the strongest conditional delta (+0.23 bps mean) but it is weak and the median is negative. CAND-086 has negligible conditional delta. CAND-088's evidence contradicts the hypothesis.

---

## 9. Counterfactual Comparison

| Candidate | CF N | CF Net | Treatment Net | CF Verdict | Quality |
|---|---|---|---|---|---|
| CAND-086 | 21,738 | -2.12 | -2.06 | MIXED | Valid but negligible separation |
| CAND-087 | 6,638 | -2.14 | -1.91 | MIXED | Valid but weak separation |
| CAND-088 | 556 | +4.07 | -15.51 | COUNTERFACTUAL SUPERIOR | Valid — contradicts hypothesis |

All three counterfactuals are valid and populated. CAND-088's counterfactual is the strongest (positive economics) but it contradicts the treatment hypothesis.

---

## 10. Mechanism Quality Comparison

1. **CAND-087 (Recovery Quality):** Mechanism is logically coherent. Recovery quality as information signal is plausible. Empirical evidence shows weak but real separation (+0.23 bps mean). The mechanism is not contradicted — just weak.

2. **CAND-086 (Absorption Failure):** Mechanism is logically coherent. Cumulative failed conviction is intuitive. But empirical evidence shows negligible separation (+0.07 bps mean). The mechanism may not operate at the M1 timeframe.

3. **CAND-088 (Session Sequence):** Mechanism is logically coherent. Path dependence is intuitive. But empirical evidence contradicts the hypothesis. Aligned breaks outperform opposite breaks.

---

## 11. Distribution Quality

| Candidate | Mean | Median | WR | Std | Distribution |
|---|---|---|---|---|---|
| CAND-086 | -2.06 | -2.13 | 49.2% | 16.78 | Broad-based negative |
| CAND-087 | -1.91 | -2.03 | 49.7% | 16.87 | Broad-based negative |
| CAND-088 | -15.51 | -10.62 | 20.3% | 26.18 | Concentrated negative |

CAND-088's distribution is notably different: very low win rate (20.3%), large negative mean, concentrated losses. This is the worst distribution of the three.

---

## 12. Prior-Art / Redundancy Audit

| Candidate | Classification | Reason |
|---|---|---|
| CAND-086 | NEW | No V19–V28 candidate counts failed directional moves |
| CAND-087 | NEW | No V19–V28 candidate measures post-disturbance recovery quality |
| CAND-088 | NEW | No V19–V28 candidate examines session-opening direction vs structural break |

All three are genuinely new. No redundancy with historical candidates.

---

## 13. State Library Impact

No new State Review Eligible candidates. The conditional deltas are too weak (CAND-086: +0.07, CAND-087: +0.23) or contradicted (CAND-088: -19.59).

---

## 14. CAND-077

> STATE REVIEW ELIGIBLE — PRESERVED / NOT REOPENED

---

## 15. CAND-081

> STATE REVIEW ELIGIBLE — PRESERVED / NOT REOPENED

---

## 16. CAND-083

> STATE REVIEW ELIGIBLE — PRESERVED / NOT REOPENED

---

## 17. CAND-079

> STATE OBSERVATION

---

## 18. CAND-078

> CLOSED

---

## 19. Closed-Line Firewall

> PASS

No closed candidate was reopened. No closed mechanism was used.

---

## 20. Governed State Firewall

> CAND-077 / CAND-081 / CAND-083 preserved and untouched.

---

## 21. Protected Forward Runtime

CAND-015/024/035:
> ACTIVE / PROTECTED / UNTOUCHED

---

## 22. G2

> NOT EXECUTED

---

## 23. System Assembly

> NOT EXECUTED

---

## 24. Future Relational / Composition Research — NOT EXECUTED

Recorded as a future research direction only:

### CAND-077 + CAND-083
Volatility-character transition × accumulated rejection pressure. Does rejection pressure during/after volatility-character transition produce a distinct economic state?

### CAND-083 + CAND-081
Pre-failure rejection accumulation × post-failure trapped participant condition. Does structural failure preceded by accumulated rejection pressure produce stronger subsequent economics?

### CAND-077 + CAND-083 + CAND-081
Regime transition → rejection accumulation → structural failure → trapped participants. Does this sequence represent a coherent market-state/event chain?

These are hypotheses only. No relationship has been established. No interaction has been validated. No trading signal has been created. No threshold has been ratified.

---

## 25. Final G1 Decisions

| Candidate | G1 Decision | Next Status |
|---|---|---|
| CAND-086 | ECONOMICALLY NEGATIVE | CLOSED |
| CAND-087 | INFORMATIONALLY INTERESTING (weak) | CLOSED |
| CAND-088 | ECONOMICALLY NEGATIVE / COUNTERFACTUAL SUPERIOR | CLOSED |

No candidates promoted. No State Review Eligible. No G2.

---

## 26. Next Permitted Task

> V30 G0 — NEW DISCOVERY

---

## 27. Research Impact Assessment

V29 G1 produced no State objects and no Alpha candidates. However, the research is valuable:

1. **CAND-088's counterfactual finding is significant:** Aligned breaks (opening bias matches structural break direction) produce +4.07 bps net mean with 58.3% win rate. This is a genuine positive economic finding — but it was not the hypothesis. The aligned-break economics deserve separate governance consideration in a future cycle.

2. **The recovery-quality mechanism (CAND-087) shows weak but real separation.** The +0.23 bps mean delta suggests the mechanism may have some informational value, but not enough for State classification.

3. **The absorption-failure mechanism (CAND-086) shows negligible separation.** The count of failed directional moves does not predict subsequent economics at the M1 timeframe.

4. **V29 confirms the project's research trajectory:** mechanism-first discovery produces cleaner results than indicator/threshold discovery. Even negative results are interpretable.

---

*End of V29 G1 Economic Plausibility Screen.*
