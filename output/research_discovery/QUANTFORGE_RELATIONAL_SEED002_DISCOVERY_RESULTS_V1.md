# QUANTFORGE — SEED-002 RELATIONAL DISCOVERY RESULTS

## 1. Experiment Status

> **COMPLETE**

First formally registered QuantForge relational experiment executed.
Frozen hypothesis. No optimization. No additional relationships tested.

## 2. Registered Hypothesis

> Does a structural failure preceded by the CAND-083 accumulated rejection
> condition produce materially different downstream economics when the
> CAND-081 post-failure trapped-participant condition occurs, compared with
> comparable structural failures lacking the CAND-083 precondition?

Classification: **CONDITIONAL ASSOCIATION / INCREMENTAL INFORMATION**
Not causal proof.

## 3. Frozen Inputs

### Input A — CAND-083

- Status: STATE REVIEW ELIGIBLE
- Concept: Pre-failure accumulated rejection pressure
- Parameters: STRUCTURAL_LOOKBACK=20, REJECTION_WINDOW=50, REJECTION_TOLERANCE=1bp,
  REJECTION_CONFIRM_BARS=5, TREATMENT threshold=3+ rejections
- No numerical threshold ratified as production parameter

### Input B — CAND-081

- Status: STATE REVIEW ELIGIBLE
- Concept: Post-failure trapped participant condition
- Parameters: STRUCTURAL_LOOKBACK=20, BREAKOUT_THRESHOLD=3bps, FAILURE_WINDOW=5 bars
- No threshold optimized

## 4. Data / Time Range

- Market: USATECHIDXUSD
- Timeframe: M1
- Data: 906,815 bars
- Date range: 2023-09-01 00:00:00 to 2026-07-10 20:14:00
- Holding period: 60 bars (60 minutes)
- Friction: 2.0 bps round-trip

## 5. Event and Temporal Integrity

- CAND-081 events detected: 65,520 raw
- After deduplication (60-bar minimum gap): **6,701**
- All events classified as treatment or control
- No event double-counted
- Treatment membership determined without future information

## 6. Population Construction

### CAND-081 Baseline (all events with returns)

- N = 6,701

### CAND-081 WITHOUT CAND-083 (control)

- N = 1,784 (26.6%)

### CAND-081 WITH CAND-083 (treatment)

- N = 4,917 (73.4%)

Note: Treatment fraction is large because most CAND-081 structural failures
are preceded by some rejection activity at the structural level within the
50-bar window. This is expected given the nature of structural-level tests.

## 7. Treatment Definition

CAND-081-type post-failure events where the structural level had ≥3
rejection attempts (touch + close-back-through) within the 50-bar window
preceding the structural failure.

## 8. Control Definition

CAND-081-type post-failure events where the structural level had 0-2
rejection attempts in the same window.

## 9. Economic Metrics

### Treatment (CAND-081 WITH CAND-083)

| Metric | Value |
|---|---|
| N | 4,917 |
| Net Mean | **-1.96 bps** |
| Net Median | **-1.61 bps** |
| Gross Mean | 0.04 bps |
| Gross Median | 0.39 bps |
| Win Rate | 46.1% |
| Std Dev | 31.82 bps |
| Worst | -392.56 bps |
| Best | +411.52 bps |

### Control (CAND-081 WITHOUT CAND-083)

| Metric | Value |
|---|---|
| N | 1,784 |
| Net Mean | **-0.19 bps** |
| Net Median | **-0.90 bps** |
| Gross Mean | 1.81 bps |
| Gross Median | 1.10 bps |
| Win Rate | 48.7% |
| Std Dev | 51.56 bps |
| Worst | -274.09 bps |
| Best | +1,026.03 bps |

### Baseline (all CAND-081)

| Metric | Value |
|---|---|
| N | 6,701 |
| Net Mean | -1.49 bps |
| Net Median | -1.41 bps |
| Win Rate | 46.8% |

## 10. Treatment vs Control Delta

| Metric | Value |
|---|---|
| **Delta Mean** | **-1.78 bps** |
| **Delta Median** | **-0.72 bps** |

Treatment vs Baseline:
- Delta Mean: -0.47 bps
- Delta Median: -0.20 bps

**Classification: CONTROL SUPERIOR** — CAND-081 events WITHOUT CAND-083
precondition outperform CAND-081 events WITH CAND-083 on both mean and
median.

## 11. Distribution Assessment

### Treatment quartiles

Q25 = -14.53, Q50 = -1.61, Q75 = +10.99

### Control quartiles

Q25 = -19.21, Q50 = -0.90, Q75 = +17.94

Treatment excluding best event: Mean = -2.05, Median = -1.62
Control excluding best event: Mean = -0.76, Median = -0.92

The control group shows wider dispersion (higher std, wider quartiles) but
better central tendency. The treatment group's narrower dispersion does not
compensate for its worse mean/median.

## 12. Rejection Count Distribution (Treatment)

| Metric | Value |
|---|---|
| Mean rejection count | 18.1 |
| Median rejection count | 14.0 |
| Min | 3 |
| Max | 49 |

The treatment group has substantial rejection activity, confirming the
CAND-083 precondition is capturing meaningful structural-level interaction.

## 13. Direction Breakdown

| Direction | Group | N | Mean | Median |
|---|---|---|---|---|
| long_failure | Treatment | 2,381 | -2.58 | -2.80 |
| long_failure | Control | 766 | -1.77 | -3.76 |
| short_failure | Treatment | 2,536 | -1.38 | -0.34 |
| short_failure | Control | 1,018 | +1.00 | +1.02 |

Notable: Short-failure control events are actually slightly positive
(+1.00 mean, +1.02 median), while short-failure treatment events remain
negative (-1.38 mean). The CAND-083 precondition appears to make
short-failure events worse.

## 14. Incremental Information Assessment

### CASE 4 — REDUNDANCY / NO INCREMENTAL INFORMATION

The CAND-083 precondition does NOT add positive incremental information
to CAND-081. The treatment group (with CAND-083) performs WORSE than the
control group (without CAND-083) on all primary metrics:

- Mean: -1.96 vs -0.19 (delta: -1.78 bps)
- Median: -1.61 vs -0.90 (delta: -0.72 bps)
- Win rate: 46.1% vs 48.7%

The direction of the effect is the OPPOSITE of the hypothesis. Instead
of CAND-083 adding positive information to CAND-081, the presence of
accumulated rejection pressure is associated with WORSE downstream
economics for CAND-081 events.

## 15. Counterfactual Quality

The counterfactual is well-constructed:
- Same event class (CAND-081 structural failure)
- Same market, timeframe, holding period
- Same cost model applied consistently
- Treatment/control split determined by pre-existing structural conditions
- No future information leakage

However, the large treatment fraction (73.4%) suggests that some
structural-level rejection activity is very common before failures.
The control group (0-2 rejections) may represent a fundamentally
different type of failure — one where the break occurs without prior
tests — which could explain its better performance through a different
mechanism (less trapped-participant population overall).

## 16. Statistical Evidence

- N: treatment=4,917, control=1,784 (substantial)
- Effect direction: consistent (treatment worse on mean, median, win rate)
- No inferential test required by protocol; effect is economically small
  (-1.78 bps) and directionally contrary to hypothesis
- The result is not driven by outliers (excluding best event does not
  change the classification)

## 17. Cost Model

Friction: 2.0 bps round-trip, applied consistently to both groups.

Gross means: treatment = 0.04 bps, control = 1.81 bps.
The friction cost disproportionately affects the treatment group because
its gross edge is smaller.

## 18. Mechanism Assessment

### OBSERVED

CAND-081 events preceded by CAND-083-type rejection activity produce
worse downstream economics than CAND-081 events without such preconditions.

### CONSISTENT WITH HYPOTHESIS

Partially: the rejection activity does alter downstream economics — just
not in the hypothesized direction.

### NOT ESTABLISHED

- Actual participant positioning
- Actual forced-exit flow
- Causality (the association may be driven by structural-level
  characteristics that correlate with both rejection activity and
  poor failure economics)
- Whether the control group represents a fundamentally different
  event class
- Persistence or regime stability of this pattern

## 19. Alternative Explanations

1. **Structural-level severity**: Levels that attract many rejections
   may be less "fresh" structural boundaries, reducing the economic
   impact of the subsequent failure.

2. **Event class composition**: The control group (0-2 rejections) may
   represent "surprise" failures with stronger directional implications,
   while the treatment group represents "tested" levels where participants
   have had time to adjust positioning.

3. **Selection within CAND-081**: The CAND-081 definition may already
   capture trapped-participant dynamics, and adding CAND-083 merely
   selects a subset where the trap has been partially unwound.

4. **Asymmetric short-failure effect**: The most notable separation
   appears in short failures, where control events are positive but
   treatment events are negative. This deserves investigation in a
   future governed milestone if desired.

## 20. Absolute vs Conditional Economics

**Absolute economics**: Both treatment and control are negative (after friction).
Neither group is independently profitable.

**Conditional economics**: The CAND-083 condition is associated with WORSE
absolute economics, not better. This is the opposite of a positive
incremental finding.

**Conclusion**: CAND-083 does not rescue CAND-081 from negative economics.
It makes things marginally worse.

## 21. Relational Decision

### **A — NO INCREMENTAL INFORMATION**

**Rationale**: The CAND-083 precondition adds NO positive incremental
information to CAND-081. The treatment group performs worse than the
control on mean, median, and win rate. The effect direction is contrary
to the hypothesis. While the association is statistically detectable
(large N, consistent direction), it is economically small (-1.78 bps
mean delta) and runs in the wrong direction.

This is a genuine negative relational finding.

## 22. Confirmation Requirements

Not applicable. The relationship is classified as NO INCREMENTAL
INFORMATION. No confirmation protocol is warranted.

## 23. State Impact

### CAND-083

> STATE REVIEW ELIGIBLE — PRESERVED

The negative SEED-002 result does NOT close CAND-083 as a State object.
CAND-083's independent conditional delta (+4.60 bps mean) remains valid
as standalone State evidence. The finding that it fails to add incremental
information to CAND-081 is a separate question from its standalone
behavioural properties.

### CAND-081

> STATE REVIEW ELIGIBLE — PRESERVED

CAND-081's independent conditional evidence (+1.23 bps mean, +2.33 bps
median) remains valid. The SEED-002 result tells us that CAND-083 does
not improve CAND-081, not that CAND-081 itself lacks information.

### CAND-077

> STATE REVIEW ELIGIBLE — PRESERVED

Not involved in SEED-002.

## 24. CAND-077

> STATE REVIEW ELIGIBLE — PRESERVED

## 25. CAND-081

> STATE REVIEW ELIGIBLE — PRESERVED

## 26. CAND-083

> STATE REVIEW ELIGIBLE — PRESERVED

## 27. CAND-088

> CLOSED / HYPOTHESIS CONTRADICTED
> Aligned-break observation remains exploratory.
> Not involved in SEED-002.

## 28. Forward Runtime Protection

CAND-015/024/035:

> ACTIVE / PROTECTED / UNTOUCHED

No forward runtime was inspected during this experiment.

## 29. G2

> NOT EXECUTED

## 30. System Assembly

> NOT EXECUTED

## 31. V30

> NOT EXECUTED

## 32. Integrity Verification

| Check | Status |
|---|---|
| Only SEED-002 was tested | ✓ |
| No additional combination tested | ✓ |
| No parameter optimized | ✓ |
| No threshold changed | ✓ |
| CAND-083 definition unchanged | ✓ |
| CAND-081 definition unchanged | ✓ |
| Treatment membership without future info | ✓ |
| Treatment/control use compatible event semantics | ✓ |
| No event double-counted | ✓ |
| Costs applied consistently | ✓ |
| Mean and median both evaluated | ✓ |
| Absolute and conditional economics separated | ✓ |
| No causality claimed | ✓ |
| No confirmation performed | ✓ |
| No G2 performed | ✓ |
| No forward runtime inspected | ✓ |
| State classifications unchanged | ✓ |
| Relationship ledger updated | ✓ |
| SESSION_HANDOFF updated | ✓ |

## 33. Final Interpretation

SEED-002's registered hypothesis is **REFUTED** by the evidence.

CAND-083 accumulated rejection pressure does NOT produce better
downstream economics for CAND-081 post-failure events. Instead, the
treatment group performs slightly worse than the control.

This is a valid negative finding that contributes to QuantForge's
relational knowledge base:

> The combination of two independently validated State objects
> (CAND-083 + CAND-081) does not produce incremental economic
> information under the registered relationship.

The result does NOT diminish the standalone value of either State object.
It tells us that these two specific behavioural phenomena do not interact
in the hypothesized way.

**Key insight for future relational research**: Not all conceptually
plausible relationships between State objects will produce positive
incremental information. Rigorous registration and controlled testing
are essential to distinguish genuine complementarity from coincidental
co-occurrence.

---

**Artifact:** `output/research_discovery/QUANTFORGE_RELATIONAL_SEED002_DISCOVERY_RESULTS_V1.md`
**Experiment script:** `research/seed002_relational_experiment.py`
**Date:** 2026-08-31
