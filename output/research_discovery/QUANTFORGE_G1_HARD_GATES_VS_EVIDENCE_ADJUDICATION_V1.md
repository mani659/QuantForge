# QUANTFORGE — G1 V3 METHODOLOGY REFINEMENT
# HARD GATES VS EVIDENCE-BASED ECONOMIC ADJUDICATION
# DATE: 2026-08-29
# STATUS: DESIGN REVIEW — REFINING G1 V3 PROPOSAL

---

## 1. Problem

The G1 V3 proposal (QUANTFORGE_G1_ECONOMIC_QUALIFICATION_FRAMEWORK_V3_PROPOSAL.md) correctly identified the need for artifact-specific qualification paths. However, it carried forward the same structural flaw it was designed to fix: converting economic measurements into rigid numeric thresholds.

The V3 proposal specified:
- Mean Net > 5 bps (hard gate)
- Median Net > 0 bps (hard gate)
- Per-Event Mean > 20 bps (hard gate)
- N ≥ 10 / N ≥ 3 (hard gates)
- Δ > 2 bps (hard gate)

This creates a system where:
- +4.8 bps mean **fails** while +5.2 bps mean **passes** — despite the 4.8 bps candidate having broader evidence, better distribution, and higher robustness;
- N=9 **fails** while N=10 **passes** — despite N=9 having identical economic properties;
- a candidate at exactly the threshold is treated categorically differently from one one unit below.

This is not governance. This is a scoring system pretending to be governance.

---

## 2. R-Value Analogy

In risk management, R (reward-to-risk) is a **measurement unit**, not a qualification commandment. A trader does not reject a +2R trade merely because it is less than +3R. The decision to take a trade depends on the total evidence: setup quality, context, risk, and opportunity cost.

Similarly:

> bps, expectancy, median, N, delta, and frequency are **measurements of evidence**, not automatically universal qualification commandments.

A candidate at +4.8 bps with N=800, broad distribution, strong counterfactual, and clean execution may be **more worthy of G2** than a candidate at +5.2 bps with N=10, concentrated tail, and marginal counterfactual.

The framework must support this judgment. A rigid threshold system cannot.

---

## 3. Hard Validity Gates

Hard gates protect research integrity. They answer:

> "Is this experiment measuring a valid economic object?"

Failing a hard validity gate means the candidate is **not an evaluable economic object** — not that it is economically weak.

### 3.1 Validity Gate List

| Gate | Why It Is Hard |
|---|---|
| **Deterministic definition** | If the setup cannot be implemented identically by two independent researchers, it is not a testable hypothesis. |
| **Executable entry** | Entry must exist at or before the information being tested becomes known. No future extrema. |
| **No hindsight contamination** | No post-entry signal definition. No MFE/MAE-influenced entry. No future-bar filtering. |
| **Correct cost normalization** | Friction must be explicit, in bps, instrument-specified, and applied consistently. Mixed units produce invalid economics. |
| **Data integrity** | Required data must exist, be aligned in time, and be causally relevant to the hypothesis. |
| **Legitimate counterfactual** | The control must isolate the specific mechanism being tested. Treatment vs. random is not a valid counterfactual. |
| **Causal claim limited to observables** | The hypothesis must be stated in terms of observable price/time/volume behavior. Institutional intent, dealer positioning, or other unobservable claims are prohibited. |
| **No future-bar dependency** | The candidate must be computable from information available at execution time. Lookahead = invalid. |
| **Reproducible** | Given the same data, the same definition must produce the same event set. |

### 3.2 Design Principle

These gates are binary. A candidate either passes or it does not. There is no "mostly deterministic" or "approximately executable." The reason is not economic judgment — it is measurement validity.

---

## 4. Economic Evidence

All economic statistics are **evidence**, not **verdicts**.

An economic statistic answers: "What does the data suggest about the economic properties of this object?"

It does NOT answer: "Does this object automatically qualify?"

### 4.1 Evidence Metrics

| Metric | What It Measures | Role |
|---|---|---|
| Mean net | Central tendency of economic outcome | Primary evidence |
| Median net | Typical event outcome | Distributional evidence |
| Dispersion (std dev, IQR) | Outcome variability | Risk evidence |
| Worst-event loss | Downside extreme | Tail evidence |
| Payoff concentration | % of returns from top N% of events | Outlier dependence evidence |
| Exclude-best-event mean | Sensitivity to single observations | Robustness evidence |
| Counterfactual delta (Δ) | Incremental condition value | Mechanism evidence |
| N | Evidence sample size | Evidence quality marker |
| Frequency | Opportunity rate | Practical deployment evidence |
| Per-event expectancy | Per-occurrence economic value | Rare-event evidence |
| Per-unit-time contribution | Annualized economic value | Capital efficiency evidence |

### 4.2 Design Principle

None of these metrics automatically gate promotion. They are **inputs to an evidence-based adjudication**. The adjudication considers the total evidence profile, not any single number.

---

## 5. Mean

### 5.1 Role

Mean net is the **primary economic measurement**. It represents the expected value per event.

### 5.2 Treatment

Mean net is NOT a hard threshold.

Instead, the G1 report presents:
- Mean net in bps;
- The friction cost used;
- The gross mean before friction;
- The instrument and price level.

The adjudication asks:

> "Is the mean net large enough, given the evidence quality and distributional properties, to suggest genuine economic potential?"

A mean of +4.8 bps with N=800 and broad distribution is **stronger evidence** than +5.2 bps with N=10 and concentrated tail. The framework must accommodate this.

### 5.3 Reference Point

The 5 bps figure serves as a **governance reference point** — a rough indicator of "how much above friction." It is not a universal law.

> **5 bps = GOVERNANCE REFERENCE / NOT UNIVERSAL LAW**

---

## 6. Median

### 6.1 Role

Median net measures the **typical event outcome**. It answers: "What happens on a normal event?"

### 6.2 Mean Positive / Median Negative

A positive mean with negative median means:
- Most events lose money;
- A few large winners pull the mean positive.

This is not automatically invalid. It IS a warning sign requiring investigation.

### 6.3 Distinguishing Valuable Skew from Fragile Skew

**Valuable skew:**
- Mean: +8 bps; Median: -2 bps; N=200; worst event: -15 bps; top 10% contribute 40% of returns;
- Broad enough winner pool; manageable downside; the right tail is a genuine structural property.

**Fragile skew:**
- Mean: +12 bps; Median: -5 bps; N=15; worst event: -80 bps; top 1 event contributes 120% of returns;
- One event dominates; removing it flips the sign; the result is a statistical accident.

### 6.4 Treatment

Median is **evidence**, not a hard gate.

The G1 report presents:
- Median net;
- Median vs mean comparison;
- Payoff concentration;
- Exclude-best-event sensitivity.

The adjudication considers these jointly. A negative median does not automatically fail a candidate. It triggers deeper investigation.

---

## 7. Sample Size

### 7.1 Role

N measures **evidence quality**. Higher N means more reliable estimates.

### 7.2 Evidence Quality vs Economic Gate

| N | Economics | Classification |
|---|---|---|
| N=4, +60 bps/event | Large per-event | ECONOMICALLY PROMISING / EVIDENCE-LIMITED |
| N=800, +0.3 bps/event | Small per-event | ROBUSTLY ESTIMATED / ECONOMICALLY WEAK |
| N=800, +8 bps/event | Large per-event | STRONG EVIDENCE / ECONOMICALLY PROMISING |
| N=4, +0.5 bps/event | Small per-event | WEAK EVIDENCE / ECONOMICALLY NEGLIGIBLE |

### 7.3 Treatment

N is **evidence quality**, not an automatic pass/fail economic gate.

Low N with strong economics: "evidence-limited but economically promising — deserves dedicated evidence accumulation."

High N with weak economics: "robustly measured but insufficient — the economy is genuinely flat."

### 7.4 Reference Points

- N < 5: Evidence severely limited. Any result is preliminary.
- N = 5–20: Evidence limited. Distributional claims unreliable.
- N = 20–100: Moderate evidence. Mean and median informative.
- N > 100: Strong evidence. Distributional analysis meaningful.

These are **interpretation guides**, not gates.

---

## 8. Rare Events

### 8.1 Design Principle

A rare event should be eligible for dedicated forward qualification when:

> The evidence is economically compelling enough to justify waiting for more independent events.

### 8.2 Evaluation Dimensions

| Dimension | Question |
|---|---|
| Per-event economics | Is the per-event value large enough to justify waiting? |
| Event integrity | Are events independently defined and non-overlapping? |
| Independence | Are events statistically independent? |
| Outcome distribution | Is the per-event value consistent, or driven by one event? |
| Plausible waiting time | How long between events on average? |
| Opportunity cost | What else could the capital do while waiting? |
| Evidence accumulation | Is the event count sufficient for any distributional inference? |

### 8.3 No Universal Minimum Expectancy

The 20 bps figure from the V3 proposal is a **reference point**, not a law.

A rare event at +10 bps/event with clean definition, strong counterfactual, and N=8 may be more valuable than a frequent event at +3 bps with N=1000. The framework must support this judgment.

### 8.4 Evidence Classification for Rare Events

| Profile | Classification |
|---|---|
| Large per-event, strong counterfactual, N ≥ 3 | ECONOMICALLY PROMISING / EVIDENCE-LIMITED |
| Large per-event, marginal counterfactual | INCONCLUSIVE — more evidence needed |
| Large per-event, N < 3 | PRELIMINARY — insufficient events |
| Small per-event, any N | ECONOMICALLY WEAK |
| Negative per-event | ECONOMICALLY NEGATIVE |

---

## 9. State / Condition

### 9.1 Design Principle

A State/Condition artifact is evaluated on its **incremental usefulness to a legitimate downstream Alpha**, not on standalone PnL.

### 9.2 Evaluation Dimensions

| Dimension | Question |
|---|---|
| Expectancy improvement | Does the state increase the target Alpha's mean net? |
| Median improvement | Does the state improve the typical event? |
| Left-tail reduction | Does the state reduce worst-case outcomes? |
| Drawdown reduction | Does the state improve peak-to-trough behavior? |
| Hit-rate improvement | Does the state increase win rate? |
| Payoff asymmetry | Does the state shift the payoff distribution favorably? |
| Regime selectivity | Does the state activate during favorable regimes? |
| Reproducibility | Does the delta hold across time periods? |

### 9.3 No Standalone Gate

A State does NOT need positive standalone PnL. A State with negative absolute economics but +5 bps incremental delta over a qualified Alpha is informationally valuable.

### 9.4 State Evidence Classification

| Profile | Classification |
|---|---|
| Positive delta, qualified target exists, reproducible | STATE-QUALIFICATION CANDIDATE |
| Positive delta, target not yet qualified | INFORMATIONALLY PROMISING / TARGET PENDING |
| Positive delta, not reproducible | EVIDENCE-UNSTABLE |
| Zero/negative delta | NOT USEFUL AS STATE |
| Delta exists but below friction of target Alpha | MARGINAL — investigate further |

---

## 10. Regime / Specialist

### 10.1 Design Principle

A Regime Specialist is evaluated **within its operating regime**. Unconditional economics are reported but not gated.

### 10.2 Evaluation Dimensions

| Dimension | Question |
|---|---|
| In-regime economics | Does the module produce strong returns inside the regime? |
| Regime definition quality | Is the regime objective, testable, and pre-registered? |
| Consistency inside regime | Are returns stable across regime instances? |
| Behavior outside regime | Is the module appropriately inactive? |
| Transition handling | Does the module handle regime transitions cleanly? |
| Capital utilization | How much capital is idle during non-regime periods? |

### 10.3 Unconditional Economics

A regime specialist active 20% of the time with +15 bps in-regime will have ~+3 bps unconditional. This is not failure — it is specialization. The framework evaluates in-regime performance.

---

## 11. Counterfactual

### 11.1 Hard Gate

Counterfactual validity is a **hard gate**. The control must isolate the mechanism being tested.

### 11.2 Separate Reporting

Every G1 report states both:
1. **Absolute economics:** Treatment mean net, median, distribution;
2. **Incremental condition value:** Treatment minus Counterfactual (mean and median).

### 11.3 No Misreporting

Treatment Superior + Negative Absolute = "CONDITIONAL INFORMATION VALUE / ABSOLUTE ALPHA FAILED."

This is NOT:
- "validated"
- "promoted"
- "component-qualified"

---

## 12. Economic Headroom

### 12.1 Replace Binary Gates with Evidence Profiles

Instead of PASS/FAIL based on a single number, classify the total evidence:

### ECONOMICALLY NEGATIVE
No credible net economics. Negative mean net after friction. Counterfactual similar or superior. No path to monetization.

### INFORMATIONALLY INTERESTING
Meaningful conditional structure (treatment > counterfactual). Real microstructural information. But insufficient absolute movement to survive friction. Potential state/component value.

### ECONOMICALLY PROMISING
Positive economics with incomplete robustness. Evidence suggests genuine economic potential but is limited by N, distributional concerns, or counterfactual ambiguity. Deserves G2 investment.

### QUALIFICATION-WORTHY
Strong economics. Strong validity. Sufficient evidence quality. Broad-based distribution. Counterfactual favorable. Ready for rigorous G2 pilot.

### RARE-EVENT QUALIFICATION-WORTHY
Large per-event economics. Clean event definition. Strong counterfactual. Evidence-limited by event count but economically compelling enough to justify dedicated event-count forward validation.

### 12.2 Design Principle

These classifications are **holistic evidence judgments**, not score totals. They require reading the complete evidence profile, not comparing a single number to a threshold.

---

## 13. Tail Risk

### 13.1 Required Diagnostic Metrics

| Metric | Purpose |
|---|---|
| Median net | Typical event outcome |
| Payoff concentration | % of returns from top 10% of events |
| Exclude-best-event mean | Sensitivity to single observations |
| Worst-event loss | Maximum downside |
| Interquartile range | Middle-50% spread |
| Contribution concentration | Whether returns depend on a few events |

### 13.2 Treatment

These are **diagnostic inputs** to the evidence profile. They inform the adjudication.

A candidate with broad, symmetric distribution and positive mean is classified differently from one with identical mean but concentrated, fragile distribution — even if both have the same mean net.

### 13.3 Simplicity

G1 diagnostic requirements are kept to the minimum set needed to distinguish robust from fragile evidence. Not every possible statistic is required.

---

## 14. Adjudication Classes

### 14.1 G1 Decision Model

The G1 decision is one of:

| Decision | Meaning |
|---|---|
| **CONTINUE TO G2** | Evidence profile suggests genuine economic potential. Invest more research capital. |
| **HOLD — MORE EVIDENCE NEEDED** | Economically promising but evidence-limited. Recommend targeted evidence accumulation before G2. |
| **RARE-EVENT FORWARD QUALIFICATION** | Large per-event economics with insufficient event count. Recommend event-count-based forward validation. |
| **STATE INTERACTION ELIGIBLE** | Incremental information demonstrated. Awaits qualified downstream Alpha target for interaction study. |
| **REJECT** | Evidence profile does not justify further investment. Economics negative, counterfactual unfavorable, or validity failed. |

### 14.2 No Score Totals

Decisions are NOT based on numerical scores such as "7/10." They are based on reading the complete evidence profile and exercising economic judgment.

### 14.3 No Weighted Composites

There is no formula like `0.3 × mean + 0.2 × median + 0.5 × counterfactual_delta`. Each dimension is considered in context.

---

## 15. Hard Gates vs Evidence Table

| Criterion | Hard Gate? | Evidence/Diagnostic? | Why |
|---|---|---|---|
| Deterministic definition | **HARD** | — | Without reproducibility, no valid experiment exists. |
| Executable entry | **HARD** | — | Without executable integrity, economics are fabricated. |
| No hindsight contamination | **HARD** | — | Post-entry definition invalidates the measurement. |
| Correct cost normalization | **HARD** | — | Mixed units produce false economics. |
| Data integrity | **HARD** | — | Missing/wrong data = invalid experiment. |
| Legitimate counterfactual | **HARD** | — | Invalid control = uninterpretable result. |
| Causal claims limited to observables | **HARD** | — | Unobservable claims cannot be empirically tested. |
| Mean net | — | **PRIMARY EVIDENCE** | Economic measurement, not a threshold. |
| Median net | — | **DISTRIBUTIONAL EVIDENCE** | Typical outcome, informs skew analysis. |
| N | — | **EVIDENCE QUALITY MARKER** | Higher N = more reliable, but not automatically a gate. |
| Frequency | — | **PRACTICAL EVIDENCE** | Describes deployment characteristics. |
| Counterfactual delta | — | **MECHANISM EVIDENCE** | Measures condition value. |
| Payoff concentration | — | **TAIL EVIDENCE** | Detects outlier dependence. |
| Exclude-best-event mean | — | **ROBUSTNESS EVIDENCE** | Detects fragility. |
| Worst-event loss | — | **DOWNSIDE EVIDENCE** | Documents extreme risk. |
| Per-event expectancy | — | **RARE-EVENT EVIDENCE** | Primary for rare events. |
| Per-unit-time contribution | — | **CAPITAL EFFICIENCY EVIDENCE** | Practical deployment value. |
| In-regime economics | — | **REGIME EVIDENCE** | Primary for regime specialists. |

---

## 16. Numeric Threshold Review

### 16.1 — 5 bps (Mean Net)

| Dimension | Assessment |
|---|---|
| Current status | V3 proposed as hard gate |
| Revised status | **REFERENCE POINT — NOT UNIVERSAL LAW** |
| Justification | 5 bps represents ~2.5x friction coverage. Useful for rough calibration. But +4.8 bps with strong evidence may be more valuable than +5.2 bps with weak evidence. The number should inform, not decide. |

### 16.2 — 20 bps (Per-Event Rare-Event)

| Dimension | Assessment |
|---|---|
| Current status | V3 proposed as hard gate |
| Revised status | **REFERENCE POINT — NOT UNIVERSAL LAW** |
| Justification | 20 bps represents ~10x friction, compensating for small N. Reasonable as a rough indicator of "economically large enough to justify rare-event treatment." But a rare event at +12 bps with very clean definition and strong mechanism may also qualify. |

### 16.3 — 2 bps (State Delta)

| Dimension | Assessment |
|---|---|
| Current status | V3 proposed as hard gate |
| Revised status | **REMOVE AS UNIVERSAL RULE** |
| Justification | State usefulness depends entirely on the target Alpha's economics. A 1 bps delta on a +50 bps Alpha is more valuable than a 3 bps delta on a +2 bps Alpha. The delta must be evaluated relative to the target, not as an absolute threshold. |

### 16.4 — N=3 (Rare-Event Minimum)

| Dimension | Assessment |
|---|---|
| Current status | V3 proposed as hard gate |
| Revised status | **EVIDENCE-QUALITY MARKER — NOT AUTOMATIC GATE** |
| Justification | N=3 is the practical minimum for any distributional inference. Below N=3, results are highly preliminary. But N=2 with +100 bps/event and clean definition is not worthless — it is "very early evidence." The classification should reflect this, not reject it. |

### 16.5 — N=10 (Standalone Minimum)

| Dimension | Assessment |
|---|---|
| Current status | V3 proposed as hard gate |
| Revised status | **EVIDENCE-QUALITY MARKER — NOT AUTOMATIC GATE** |
| Justification | N=10 allows rudimentary distributional assessment. Below N=10, mean is highly sensitive to individual events. But N=8 with +8 bps and broad distribution is stronger evidence than N=12 with +0.5 bps and concentrated tail. |

### 16.6 Summary

| Threshold | Revised Classification |
|---|---|
| 5 bps | Reference Point |
| 20 bps | Reference Point |
| 2 bps State delta | Remove as universal rule |
| N=3 | Evidence-Quality Marker |
| N=10 | Evidence-Quality Marker |

**None remain as universal hard gates.**

---

## 17. Hypothetical Examples

### Example A vs B — Why Rigid Gates Fail

**Candidate A:**
- Mean Net: +4.8 bps
- Median Net: +2.5 bps
- N: 800
- Distribution: Broad, symmetric
- Counterfactual: Treatment Superior (+4.8 vs +1.2 bps)
- Exclude-best-event mean: +4.6 bps
- Payoff concentration: Top 10% contribute 25% of returns
- Classification: **QUALIFICATION-WORTHY** (under V3: FAILS at 4.8 < 5)

**Candidate B:**
- Mean Net: +5.2 bps
- Median Net: +0.1 bps
- N: 10
- Distribution: Right-skewed, one event contributes +40 bps
- Counterfactual: Treatment Superior (+5.2 vs +3.8 bps)
- Exclude-best-event mean: +1.2 bps
- Payoff concentration: Top 1 event contributes 77% of returns
- Classification: **ECONOMICALLY PROMISING / EVIDENCE-LIMITED** (under V3: PASSES at 5.2 > 5)

**Under rigid V3 gates:** B passes, A fails.
**Under evidence-based adjudication:** A is clearly stronger than B.

This demonstrates why thresholds are dangerous. The total evidence — distribution, robustness, counterfactual strength, sample size — matters more than any single number.

### Example C — Rare Event

**Candidate C:**
- N: 4
- Per-Event Mean Net: +60 bps
- Per-Event Median Net: +55 bps
- Counterfactual: Treatment Superior (+60 vs -5 bps)
- Event definition: Clean, deterministic, independently verifiable
- Mechanism: Plausible forced-flow / settlement pressure
- Exclude-best-event mean: +42 bps

**Under rigid V3 gates:** FAILS (N=4 < N=10 minimum, or borderline at N≥3).
**Under evidence-based adjudication:** ECONOMICALLY PROMISING / EVIDENCE-LIMITED. The per-event economics are massive, the counterfactual is strong, the definition is clean, and even excluding the best event, the mean is +42 bps. This deserves dedicated event-count forward qualification, not rejection.

---

## 18. Rescue Firewall

### 18.1 Principle

> Changing the G1 framework does not retroactively rescue V19–V24.

### 18.2 Application

- V24 remains CLOSED;
- CAND-071, CAND-072, CAND-073 remain CLOSED;
- CAND-059 remains STATE-ARTIFACT — NOT STANDALONE PROFITABLE;
- CAND-065 remains EVIDENCE-LIMITED;
- CAND-069 remains CLOSED / INSUFFICIENT;
- Any future reclassification requires explicit owner-authorized review.

### 18.3 Prospective Only

G1 V3 (as refined) applies to new candidates only. The new framework would not rescue any V19–V24 Alpha candidate because their absolute economics are genuinely negative.

---

## 19. V24 Status

> V24 CLOSED — NO G2 CANDIDATE

CAND-071: CLOSED — NEGATIVE ABSOLUTE EXPECTANCY
CAND-072: CLOSED — NEGATIVE ABSOLUTE EXPECTANCY
CAND-073: CLOSED — NEGATIVE ABSOLUTE EXPECTANCY

Not reopened.

---

## 20. Protected Forward Runtime

### CAND-015
> ACTIVE / PROTECTED / UNTOUCHED

### CAND-024
> ACTIVE / PROTECTED / UNTOUCHED
> Canonical: `CAND-024:CANONICAL:925495a8`

### CAND-035
> ACTIVE / PROTECTED / UNTOUCHED
> Canonical: `CAND-035:CANONICAL:ddc5d0e9`

Do not modify runner, launcher, contracts, ledgers, or feed.

---

## 21. Proposed G1 V3 Revision

### 21.1 Two-Layer Architecture

**Layer 1: Hard Validity Gates** (binary — pass/fail)
- Deterministic definition
- Executable entry
- No hindsight contamination
- Correct cost normalization
- Data integrity
- Legitimate counterfactual
- Causal claims limited to observables
- Reproducible

**Layer 2: Economic Evidence + Adjudication** (holistic — evidence profile)
- Mean net, median net, dispersion, tail diagnostics
- Counterfactual delta
- N as evidence quality marker
- Frequency as practical evidence
- Per-event expectancy (rare events)
- Regime consistency (regime specialists)

### 21.2 G1 Decision

Based on total evidence profile, NOT a numeric score:

| Decision | Condition |
|---|---|
| CONTINUE TO G2 | Evidence profile suggests genuine economic potential |
| HOLD — MORE EVIDENCE | Economically promising but evidence-limited |
| RARE-EVENT FORWARD QUALIFICATION | Large per-event economics, insufficient event count |
| STATE INTERACTION ELIGIBLE | Incremental information demonstrated, target pending |
| REJECT | Evidence profile does not justify further investment |

### 21.3 Evidence Profile Classification

| Classification | Description |
|---|---|
| ECONOMICALLY NEGATIVE | No credible net economics |
| INFORMATIONALLY INTERESTING | Real conditional structure, insufficient monetizable economics |
| ECONOMICALLY PROMISING | Positive economics, incomplete robustness/evidence |
| QUALIFICATION-WORTHY | Strong economics + strong validity + sufficient evidence |
| RARE-EVENT QUALIFICATION-WORTHY | Large per-event economics justify dedicated validation |

### 21.4 Numeric Thresholds — Revised

| Metric | Role in V3 |
|---|---|
| 5 bps | Reference point — calibrates "how far above friction" |
| 20 bps | Reference point — calibrates "how large per-event for rare events" |
| 2 bps delta | Removed as universal rule — evaluated relative to target Alpha |
| N=3 | Evidence-quality marker — below this, results are very preliminary |
| N=10 | Evidence-quality marker — below this, distributional claims unreliable |

---

## 22. Required Owner Decisions

The following decisions require explicit owner ratification:

### Decision 1: Two-Layer Architecture
> **RATIFY** the separation into Hard Validity Gates + Economic Evidence Adjudication.

### Decision 2: Hard Validity Gates
> **RATIFY** the nine hard gates listed in Section 3.1.

### Decision 3: No Numeric Hard Gates for Economics
> **RATIFY** that economic metrics (mean, median, N, delta, frequency) are evidence inputs, not hard thresholds.

### Decision 4: Evidence Profile Classification
> **RATIFY** the five-level evidence classification (Economically Negative → Rare-Event Qualification-Worthy).

### Decision 5: G1 Decision Model
> **RATIFY** the five-decision model (Continue / Hold / Rare-Event FQ / State Interaction Eligible / Reject).

### Decision 6: Numeric Threshold Roles
> **RATIFY** that 5 bps and 20 bps are reference points, N=3 and N=10 are evidence-quality markers, and 2 bps State delta is removed as a universal rule.

### Decision 7: Median Treatment
> **RATIFY** that median is evidence, not a hard gate — negative median triggers investigation, not automatic rejection.

### Decision 8: Friction Unit Standard
> **RATIFY** that all economic results use bps as primary unit with explicit instrument documentation.

### Decision 9: Prospective Application
> **RATIFY** that G1 V3 applies prospectively only.

### Decision 10: Counterfactual Hard Gate
> **RATIFY** that counterfactual validity remains a hard gate, but counterfactual superiority is evidence, not a gate.

---

## 23. Integrity

- No candidates were rescued;
- No parameters were changed in existing systems;
- No experiments were run;
- No forward results were inspected;
- No research was executed;
- V24 remains closed;
- All proposed thresholds are classified by evidence quality;
- No value is claimed as ratified without explicit owner decision;
- The refinement is a design review, not an implementation.
