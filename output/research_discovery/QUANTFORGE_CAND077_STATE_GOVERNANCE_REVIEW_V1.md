# QUANTFORGE — CAND-077 STATE GOVERNANCE REVIEW
# DATE: 2026-08-30
# STATUS: GOVERNANCE REVIEW COMPLETE
# NO EXPERIMENT / NO G1 / NO G2 / NO RESCUE

---

## 1. Purpose

Perform a formal governance review of CAND-077 to determine how the post-closure exploratory filter findings should be treated under the ratified G1 V3 framework.

This is NOT:
- A research execution task
- A new G1
- An optimization task
- A reopening of CAND-077 as an Alpha
- A rescue of the closed candidate

The purpose is to decide whether the observed CAND-077 findings justify:
> STATE REVIEW ELIGIBILITY / FORMAL STATE HYPOTHESIS REGISTRATION

or should remain:
> EXPLORATORY RESEARCH OBSERVATION

---

## 2. Original CAND-077 Status

**Frozen hypothesis:** Compression → Expansion volatility transition

**G1 V3 result:**
- N = 2,084
- Frequency = ~700/year
- Gross mean = +1.15 bps, Gross median = +0.86 bps
- Net mean = -0.85 bps, Net median = -1.14 bps
- Counterfactual mean = -2.52 bps, Counterfactual median = -1.90 bps
- Conditional delta = **+1.67 bps** (TREATMENT SUPERIOR)
- All 9 hard validity gates: PASS
- Transition integrity: PASS

**Original adjudication:** INFORMATIONALLY INTERESTING

**State potential:** HIGH

**Current status:** STATE REVIEW ELIGIBLE — OWNER REVIEW REQUIRED

---

## 3. Post-Closure Exploratory Findings

After V26 closure, an exploratory analysis tested whether selectivity filters could improve win rate while preserving useful frequency.

**Classification:** POST-CLOSURE EXPLORATORY OBSERVATIONS — NOT VALIDATED

These results were discovered AFTER observing the baseline data. They are subject to selection bias and must not be treated as confirmatory evidence.

---

## 4. Breakout-Magnitude Observation

| Filter | N | Win Rate | Gross Mean | Gross Median |
|---|---|---|---|---|
| Baseline (no filter) | 2,084 | 54.5% | +1.15 bps | +0.86 bps |
| Breakout > 2 bps | 1,454 | 54.7% | +1.42 bps | +1.07 bps |
| Breakout > 5 bps | 846 | 55.0% | +1.48 bps | +1.50 bps |
| Breakout > 10 bps | 415 | 57.8% | +2.74 bps | +3.30 bps |
| **Breakout > 15 bps** | **219** | **64.8%** | **+8.41 bps** | **+6.97 bps** |
| Breakout > 20 bps | 133 | 64.7% | +8.45 bps | +10.14 bps |

The observed relationship is monotonic: larger breakout magnitude from the compressed state is associated with higher win rate and higher gross expectancy.

Estimated frequency at >15 bps: ~77 events/year.

**Critical note:** The >15 bps threshold was NOT pre-registered. It was selected after observing the same historical outcomes. This is selection bias, not validation.

---

## 5. Distribution Evidence

At >15 bps breakout:
- Mean = +8.41 bps
- Median = +6.97 bps

The fact that median is positive and close to mean indicates the effect is:
- **Broad-based** (not driven by a single outlier)
- **Distributionally credible** (not mean-dependent skew)

This is stronger evidence than a high mean with negative median would be.

However, the distribution was observed AFTER filter selection. The apparent distribution quality is part of the same exploratory finding.

---

## 6. Frequency Tradeoff

| Threshold | N | Est. Frequency | Interpretation |
|---|---|---|---|
| Baseline | 2,084 | ~700/year | Too frequent for rare-event, too weak for standalone |
| >10 bps | 415 | ~144/year | Moderate frequency |
| >15 bps | 219 | ~77/year | Practical rare-event frequency |
| >20 bps | 133 | ~47/year | Low frequency, high selectivity |

The frequency reduction from filtering creates a practical opportunity rate that could be consistent with:
- A standalone rare-event strategy (~47–77/year)
- A component filter for another strategy
- A State condition for a downstream Alpha

However, frequency alone does not determine the correct classification.

---

## 7. Selection-Bias Risk

The following selection-bias concerns apply:

1. **Post-outcome filter selection:** The breakout-magnitude filter was tested AFTER observing that CAND-077's baseline had positive conditional delta. The filter was not pre-registered.

2. **Multiple thresholds tested:** Six threshold levels were examined (baseline, >2, >5, >10, >15, >20 bps). The >15 bps result appears strongest, but testing multiple thresholds increases the chance of finding a favorable result by chance.

3. **Same-sample validation:** All filter results use the same historical data as the baseline G1 screen. There is no independent holdout sample.

4. **Monotonic relationship:** The observed monotonicity (larger breakout → higher WR/mean) is intriguing but could be sample-specific. A monotonic relationship in one sample does not guarantee it will persist in future data.

5. **Time-of-day and day-of-week findings:** These were also discovered post-closure and are subject to the same selection-bias concerns. Their sample sizes are smaller and the evidence is weaker.

---

## 8. Multiple-Comparison / Threshold-Mining Risk

Six threshold levels were tested:
- Baseline
- >2 bps
- >5 bps
- >10 bps
- >15 bps
- >20 bps

Plus four time-of-day buckets and two day-of-week buckets.

Total exploratory tests: approximately 12.

At a nominal 5% false-positive rate, approximately 0.6 false positives would be expected by chance across 12 tests. The >15 bps result (64.8% WR, +8.41 bps) is strong enough that it is unlikely to be purely a false positive — but the exact magnitude and threshold may not replicate.

**Conclusion:** The exploratory findings are real enough to warrant further investigation, but they are NOT confirmatory evidence for any specific threshold.

---

## 9. State vs Alpha Classification

### A. EXPLORATORY OBSERVATION
The findings could remain purely exploratory — interesting but not actionable.

### B. STATE REVIEW ELIGIBLE
The findings could justify formal State hypothesis registration, because:
- The baseline state (compression → expansion transition) is objectively defined
- The baseline already showed +1.67 bps conditional delta (largest in RF history)
- The breakout-magnitude relationship is monotonic and distributionally credible
- The concept "expansion magnitude after compression contains information" is a genuine State concept

### C. ALPHA REVIEW ELIGIBLE
The findings could justify Alpha review, because:
- At >15 bps, the observed gross mean (+8.41 bps) exceeds friction
- The win rate (64.8%) is high
- The frequency (~77/year) is practical

However, the original CAND-077 standalone economics are negative (-0.85 bps). The Alpha case depends entirely on the post-closure filter observation, which is subject to selection bias.

### D. BOTH
Both State and Alpha review could be pursued.

### Decision

**The correct classification is B: STATE REVIEW ELIGIBLE.**

Reasoning:
1. The original standalone economics are negative. Alpha review would require the filter observation to be the entire basis, which is selection-biased.
2. The State concept ("expansion magnitude after compression contains information") is genuine and independently meaningful.
3. The State path is the correct governance path: it separates the informational finding from the economic validation, allowing proper future testing.
4. Alpha review would imply the candidate could be traded standalone, which is not supported by the unfiltered evidence.

---

## 10. State Review Decision

> CAND-077 REMAINS STATE REVIEW ELIGIBLE — OWNER REVIEW REQUIRED

The post-closure exploratory findings STRENGTHEN the case for State Review Eligibility but do NOT:
- Promote CAND-077 to STATE-ARTIFACT
- Authorize an interaction study
- Ratify any specific numerical threshold
- Validate the >15 bps breakout filter

The exploratory findings are classified as:
> SUPPORTING EVIDENCE FOR STATE REVIEW ELIGIBILITY

not:
> VALIDATED STATE HYPOTHESIS

---

## 11. Future State Qualification Path

If the owner chooses to pursue CAND-077 State qualification, the correct path is:

```
Observed CAND-077 transition + post-closure filter observation
        ↓
Formal State hypothesis registration (NEW hypothesis, NOT CAND-077 reopening)
        ↓
Hypothesis must define:
  - exact state concept (expansion magnitude after compression)
  - exact pre-entry observable
  - exact threshold (frozen BEFORE testing)
  - exact treatment
  - exact counterfactual
  - qualified downstream Alpha target
        ↓
Interaction study (separately authorized)
        ↓
State qualification
```

**Critical requirement:** The new hypothesis must be independently governed. It must NOT:
- Simply select "breakout >15 bps" because it had the best historical result
- Use the same data without a holdout
- Be treated as a continuation of CAND-077

The new hypothesis is a SEPARATE research object that was INSPIRED BY CAND-077 but is independently defined and tested.

---

## 12. Numerical Threshold Status

> NO NUMERICAL FILTER THRESHOLD IS RATIFIED.

The observed breakout-size results:
- >15 bps: 64.8% WR, +8.41 bps, ~77/year
- >20 bps: 64.7% WR, +8.45 bps, ~47/year

These are:
- EXPLORATORY EVIDENCE ONLY
- NOT validated thresholds
- NOT approved for any future hypothesis

Any future threshold must be:
- Frozen BEFORE confirmatory testing
- Pre-registered with exact treatment/counterfactual
- Tested on independent data or with proper holdout

The observed >15 bps result may INFORM hypothesis generation but must NOT be treated as the correct threshold.

---

## 13. CAND-079

> STATE OBSERVATION — PRESERVED

Original delta: +0.78 bps (weak but real).

Post-closure exploratory: Gold UP + >20 bps → 52.8% WR, +1.32 bps.

This is insufficient to elevate to STATE REVIEW ELIGIBILITY. The conditional information is small and the exploratory filter improvement is weak.

---

## 14. CAND-078

> CLOSED — ECONOMICALLY NEGATIVE / COUNTERFACTUAL INFERIORITY

No inverse hypothesis authorized. No state potential.

---

## 15. Current State Library

| Candidate | Mechanism | Classification | Evidence |
|---|---|---|---|
| CAND-059 | First Touch > Subsequent Touch | STATE-ARTIFACT | Informationally supported |
| CAND-065 | Deep Sweep > Shallow Sweep | STATE OBSERVATION | Evidence-limited |
| CAND-069 | Mid-session > Morning | STATE OBSERVATION | Small information |
| **CAND-077** | **Vol compression → expansion** | **STATE REVIEW ELIGIBLE** | **+1.67 bps delta, N=2084, monotonic filter relationship** |
| CAND-079 | Gold vol transition → Tech | STATE OBSERVATION | Weak +0.78 bps delta |

---

## 16. Forward Runtime Protection

### CAND-015
> ACTIVE / PROTECTED / UNTOUCHED

### CAND-024
> ACTIVE / PROTECTED / UNTOUCHED

### CAND-035
> ACTIVE / PROTECTED / UNTOUCHED

No forward runtime was touched during this review.

---

## 17. V27 Implications

The completion of this governance review means:

> V27 G0 MAY PROCEED

CAND-077's State review status is now clarified. It remains STATE REVIEW ELIGIBLE. This does not block V27 G0. The two paths are independent:

- CAND-077 State qualification: requires a separately authorized interaction study
- V27 G0: new discovery cycle, independent of CAND-077

Both may proceed in parallel or sequentially, at owner discretion.

---

## 18. Governance Decision

**Classification:** STATE REVIEW ELIGIBLE — PRESERVED

**Exploratory filter findings:** SUPPORTING EVIDENCE — NOT VALIDATED

**Numerical threshold:** NOT RATIFIED

**State hypothesis:** NOT YET REGISTERED (requires separate governance)

**V27 readiness:** READY

**Interaction study:** NOT AUTHORIZED

**Rescue:** NOT PERFORMED

---

## 19. Integrity

- No candidate was rescued
- No historical results were modified
- No forward runtime was touched
- No interaction study was performed
- No new candidates were generated
- No numerical threshold was ratified
- No filter was validated
- CAND-077 is classified as STATE REVIEW ELIGIBLE, not STATE-ARTIFACT
- The exploratory findings are recorded as evidence, not validation
- The correct future path is clearly defined
- SESSION_HANDOFF.md will be updated as mandatory
