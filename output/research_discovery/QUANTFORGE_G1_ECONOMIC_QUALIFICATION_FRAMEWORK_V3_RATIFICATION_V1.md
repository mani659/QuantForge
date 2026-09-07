# QUANTFORGE — G1 ECONOMIC QUALIFICATION FRAMEWORK V3
# FORMAL OWNER RATIFICATION
# DATE: 2026-08-29
# STATUS: RATIFIED — EFFECTIVE FOR FUTURE RESEARCH CYCLES

---

## 1. Owner Decision

> APPROVED. The refined G1 Economic Qualification Framework V3 is ratified as the prospective governing framework for all future Research Factory cycles.

This framework replaces the single-gate G1 design (Mean Net > 5 bps + Counterfactual Treatment Superior applied uniformly) with a two-layer architecture separating validity gates from economic evidence adjudication.

---

## 2. Effective Date

> 2026-08-29

Scope: Future research cycles only (V25 and beyond).

Does NOT apply retroactively to V19–V24.

---

## 3. Two-Layer G1 Architecture

G1 consists of two distinct layers:

### Layer 1: Hard Validity / Integrity Gates

Binary pass/fail. These protect measurement validity.

Failing a validity gate means:

> THE CANDIDATE IS NOT A VALID ECONOMIC MEASUREMENT OBJECT.

This is not an economic performance judgment.

### Layer 2: Economic Evidence Adjudication

Holistic reading of the complete evidence profile.

Economic statistics are **inputs to judgment**, not automated pass/fail commands.

The G1 decision is made by reading the total evidence, not by comparing a single number to a threshold.

---

## 4. Hard Validity Gates

The following are binary validity requirements. All must pass.

| # | Gate | Why Hard |
|---|---|---|
| 1 | Deterministic definition | Without reproducibility, no valid experiment exists. Two independent researchers must produce the same event set. |
| 2 | Executable entry | Entry must exist at or before the information being tested. No hindsight. |
| 3 | No hindsight contamination | No post-entry signal definition. No MFE/MAE-influenced entry. No future-bar filtering. |
| 4 | Correct cost normalization | Friction must be explicit, in bps, instrument-specified, and consistent. Mixed units produce false economics. |
| 5 | Data integrity | Required data must exist, be time-aligned, and causally relevant. |
| 6 | Legitimate counterfactual | The control must isolate the specific mechanism being tested. Treatment vs. random is invalid. |
| 7 | Causal claims limited to observables | Hypotheses must be stated in observable price/time/volume terms. Institutional intent or unobservable claims are prohibited. |
| 8 | No future-bar dependency | Computable from information available at execution time. |
| 9 | Reproducible | Given the same data, the same definition produces the same event set. |

---

## 5. Economic Evidence

All economic measurements are evidence inputs. None are universal hard thresholds.

| Metric | Role |
|---|---|
| Mean net | Primary economic measurement — central tendency |
| Median net | Distributional evidence — typical event outcome |
| Dispersion | Risk evidence — outcome variability |
| Worst-event loss | Tail evidence — downside extreme |
| Payoff concentration | Outlier dependence — % of returns from top events |
| Exclude-best-event mean | Robustness evidence — sensitivity to single observations |
| Counterfactual delta | Mechanism evidence — incremental condition value |
| N | Evidence quality marker — higher N = more reliable |
| Frequency | Practical evidence — opportunity rate |
| Per-event expectancy | Rare-event evidence — per-occurrence value |
| Per-unit-time contribution | Capital efficiency — annualized value |
| In-regime economics | Regime evidence — specialist performance |

These metrics **inform the adjudication**. They do not automate it.

---

## 6. Four Artifact Classes

G1 evaluates candidates within one of four artifact-specific classes. Each class has its own primary question and evaluation focus.

| Class | Primary Question |
|---|---|
| **A — Standalone Alpha** | Does the event contain credible friction-surviving absolute economic value? |
| **B — Rare-Event Alpha** | Is the per-event economics sufficiently compelling to justify waiting for additional independent events? |
| **C — State / Condition** | Does the state provide reproducible incremental value to a legitimate downstream Alpha? |
| **D — Regime / Specialist** | Does the candidate exhibit economically useful behavior inside its explicitly defined operating regime? |

---

## 7. Standalone Alpha

### Evaluation Focus

- Absolute net economics;
- Distributional properties (mean, median, dispersion, tail);
- Counterfactual;
- Evidence quality (N, stability);
- Execution integrity.

### Key Principles

- Mean and median are both reported. Neither is an automatic gate.
- Payoff concentration and robustness diagnostics are required.
- A positive mean with negative median triggers investigation, not automatic rejection.
- The total evidence profile determines the verdict.

### Adjudication

The G1 report presents the complete evidence profile and classifies the candidate within the five-level evidence classification. The decision to continue to G2 is based on whether the **total evidence** suggests genuine economic potential.

---

## 8. Rare-Event Alpha

### Evaluation Focus

- Per-event economics;
- Event integrity (deterministic, independent, non-overlapping);
- Counterfactual;
- Outcome distribution across events;
- Independent event count;
- Practical waiting burden;
- Capital/opportunity efficiency.

### Key Principles

- Frequency is NOT a universal rejection criterion.
- Low frequency with strong per-event economics is legitimate.
- The question is: "Is the per-event value large enough to justify the waiting period?"
- Forward validation uses event-count accumulation, not calendar-duration holdouts.

### Adjudication

A rare event is eligible for dedicated forward qualification when the evidence is economically compelling enough to justify waiting for more events. The decision considers per-event economics, evidence quality, counterfactual strength, and event integrity jointly.

---

## 9. State / Condition

### Evaluation Focus

- Incremental value to a legitimate downstream Alpha;
- Reproducibility of the delta across time;
- Interaction stability.

### Key Principles

- Standalone profitability is NOT required.
- The State cannot become formally qualified without a legitimate target Alpha.
- A State that merely beats a weak control while remaining economically flat does not automatically deserve component status.

### Adjudication

A State is classified as "STATE INTERACTION ELIGIBLE" when it demonstrates reproducible incremental information. Formal qualification requires a subsequent interaction study with a qualified downstream Alpha.

---

## 10. Regime / Specialist

### Evaluation Focus

- In-regime economics;
- Regime definition quality (objective, testable, pre-registered);
- Consistency inside regime;
- Behavior outside regime (inactive is acceptable);
- Transition handling;
- Capital utilization.

### Key Principles

- Unconditional economics are informative but not automatically decisive.
- A specialist active 20% of the time with strong in-regime returns is not failing — it is specializing.
- The regime definition must be pre-registered and objective.

### Adjudication

Evaluated within the operating regime. In-regime evidence profile determines the verdict.

---

## 11. Friction Standard

### Rule

> ALL FUTURE G1 RESULTS MUST CLEARLY DECLARE: instrument, price unit, tick unit (where relevant), round-trip cost, spread treatment, slippage treatment, and normalized economic representation.

### Convention

All economic results are expressed in **basis points (bps)** as the primary unit. 1 bp = 0.01% of instrument price.

No mixing of bps, price points, ticks, or currency without explicit conversion documentation.

### USATECHIDXUSD / USTECm

| Parameter | Value |
|---|---|
| Instrument | USATECHIDXUSD (USTECm) |
| Approximate Price | ~30,000 |
| Friction (bps) | To be specified per experiment |
| Friction (points) | bps × price / 10,000 |
| Execution Quality | Retail CFD |

---

## 12. Mean / Median

### Treatment

Both mean and median are reported where meaningful.

- **Mean:** Primary economic measurement. Central tendency of outcomes.
- **Median:** Distributional evidence. Typical event outcome.

### No Automatic Gate

- A negative median does NOT automatically invalidate a positively skewed strategy.
- A positive mean does NOT automatically validate it.

### Investigation Triggers

Mean positive / median negative triggers investigation into:
- Payoff concentration;
- Right-tail dependence;
- Worst events;
- Contribution concentration;
- Exclude-best-event sensitivity.

### Distinction

The framework distinguishes:
- **Valuable skew:** Broad winner pool, manageable downside, structural right tail.
- **Fragile skew:** One event dominates, removing it flips the sign, statistical accident.

---

## 13. Tail / Downside Evidence

### Required Diagnostics

| Metric | Purpose |
|---|---|
| Median net | Typical outcome |
| Payoff concentration | Outlier dependence |
| Exclude-best-event mean | Fragility check |
| Worst-event loss | Maximum downside |
| Interquartile range | Middle-50% spread |

### Treatment

These are **diagnostic inputs** to the evidence profile. They inform the adjudication.

A candidate with broad, symmetric distribution is classified differently from one with identical mean but concentrated, fragile distribution.

### Simplicity

G1 diagnostics are kept to the minimum set needed to distinguish robust from fragile evidence.

---

## 14. Counterfactual

### Hard Gate

Counterfactual validity is a hard scientific requirement. The control must isolate the mechanism being tested.

### Separate Reporting

Every G1 report states both:
1. **Absolute economics:** Treatment mean net, median, distribution;
2. **Incremental condition value:** Treatment minus Counterfactual (mean and median).

### No Misreporting

Treatment Superior + Negative Absolute = "CONDITIONAL INFORMATION VALUE / ABSOLUTE ALPHA FAILED."

This is NOT validated, promoted, or component-qualified.

---

## 15. Sample Size

### Role

N is an **evidence-quality indicator**.

### Interpretation Guide

| N | Interpretation |
|---|---|
| < 5 | Evidence severely limited. Any result is preliminary. |
| 5–20 | Evidence limited. Distributional claims unreliable. |
| 20–100 | Moderate evidence. Mean and median informative. |
| > 100 | Strong evidence. Distributional analysis meaningful. |

### Not a Gate

Low N with strong economics = "economically promising / evidence-limited."
High N with weak economics = "robustly estimated / economically weak."

Neither is automatically rejected based on N alone.

---

## 16. Frequency

### Principle

Frequency is **contextual**, not universal. Its role varies by artifact class.

| Class | Frequency Role |
|---|---|
| Standalone Alpha | Practical evidence — reported, not gating |
| Rare-Event Alpha | Handled by event-count forward validation |
| State/Condition | State occurrence frequency — diagnostic |
| Regime Specialist | In-regime frequency — diagnostic |

### No Minimum Opportunities/Year

The framework does NOT impose a minimum frequency requirement. The question for rare events is economic magnitude per event, not calendar frequency.

---

## 17. Capital / Time Efficiency

### Three Metrics

1. **Per-Event Expectancy:** Primary for rare events.
2. **Per-Unit-Time Contribution:** Primary for standalone Alpha.
3. **Capital/Efficiency:** G2+ requirement.

### G1 Treatment

| Metric | Required at G1? |
|---|---|
| Per-Event Expectancy | YES — primary evidence for rare events |
| Per-Unit-Time Contribution | REPORTED — diagnostic for standalone |
| Capital Efficiency | NO — belongs at G2+ |

---

## 18. Economic Adjudication Classes

The G1 report classifies evidence into one of five levels:

| Classification | Description |
|---|---|
| **ECONOMICALLY NEGATIVE** | No credible net economics. Negative mean net after friction. No path to monetization. |
| **INFORMATIONALLY INTERESTING** | Meaningful conditional structure. Real microstructural information. Insufficient absolute movement to survive friction. Potential state/component value. |
| **ECONOMICALLY PROMISING** | Positive economics with incomplete robustness. Evidence suggests genuine potential. Deserves G2 investment. |
| **QUALIFICATION-WORTHY** | Strong economics. Strong validity. Sufficient evidence. Broad distribution. Counterfactual favorable. Ready for G2. |
| **RARE-EVENT QUALIFICATION-WORTHY** | Large per-event economics. Clean definition. Strong counterfactual. Evidence-limited by event count but economically compelling. |

These are **holistic evidence judgments**, not score totals.

---

## 19. Numeric Threshold Policy

### Ratified Status

| Metric | Status | Role |
|---|---|---|
| 5 bps (mean net) | **REFERENCE POINT** | Calibrates "how far above friction." Not a universal law. |
| 20 bps (per-event) | **REFERENCE POINT** | Calibrates "how large per-event for rare events." Not a universal law. |
| 2 bps (State delta) | **REMOVED AS UNIVERSAL RULE** | State usefulness evaluated relative to target Alpha, not as absolute threshold. |
| N=3 | **EVIDENCE-QUALITY MARKER** | Below this, results are very preliminary. Not an automatic gate. |
| N=10 | **EVIDENCE-QUALITY MARKER** | Below this, distributional claims unreliable. Not an automatic gate. |

### Rule

> No economic metric is automatically applied as a mechanical gate. Future governance may introduce artifact-specific thresholds only through explicit owner ratification supported by evidence.

---

## 20. G1 → G2 Boundary

### G1 Question

> Is this economic object worth additional research capital?

### G2 Question

> Does the observed signal survive a controlled empirical pilot?

### Principle

Do not collapse the stages. G1 is a plausibility screen. G2 is an empirical pilot. Each has a distinct purpose.

---

## 21. Rescue Firewall

### Principle

> Ratification does NOT reopen previous research.

### Application

- V19–V24 remain closed under their original governance decisions;
- Historical candidates retain their original classifications;
- Any future reclassification requires a separate explicit owner-approved governance task;
- The new framework does not retroactively rescue any candidate.

---

## 22. V24 Closure

> V24 CLOSED — NO G2 CANDIDATE

| Candidate | Status |
|---|---|
| CAND-071 | CLOSED — NEGATIVE ABSOLUTE EXPECTANCY |
| CAND-072 | CLOSED — NEGATIVE ABSOLUTE EXPECTANCY |
| CAND-073 | CLOSED — NEGATIVE ABSOLUTE EXPECTANCY |

Not reopened.

---

## 23. Current Forward Runtime

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

## 24. V25 Status

> NOT STARTED

Do not generate V25 within this task.

---

## 25. Governance Authority

This framework is ratified by the owner and becomes the governing standard for G1 evaluation in all future Research Factory cycles.

Changes to this framework require:
1. Explicit owner authorization;
2. Documented rationale based on repository evidence;
3. A formal ratification task.

The framework may not be modified implicitly through G1 execution or candidate adjudication.

---

## 26. Integrity

- No candidates were rescued;
- No parameters were changed in existing systems;
- No experiments were run;
- No forward results were inspected;
- No research was executed;
- V24 remains closed;
- V19–V23 remain closed;
- All thresholds are classified by evidence quality;
- The ratification is prospective only;
- The forward runtime is untouched.
