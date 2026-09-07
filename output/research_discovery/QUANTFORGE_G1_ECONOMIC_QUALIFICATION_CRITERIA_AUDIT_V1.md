# QUANTFORGE — G1 ECONOMIC QUALIFICATION CRITERIA AUDIT
# READ-ONLY GOVERNANCE / METHODOLOGY AUDIT
# DATE: 2026-08-29

---

## 1. Executive Verdict

**G1 FRAMEWORK REFINEMENT REQUIRED.**

The current G1 framework is *internally consistent* and *partially correct* for standalone Alpha evaluation, but it suffers from three material defects:

1. **Unit ambiguity in friction modeling.** The friction constant (2.0 bps) is applied identically to all instruments, but the code does not distinguish between index-point units and basis-point units. For USATECHIDXUSD (~30,000), 2 bps and 2 points are mathematically different. Current G1 artifacts use "2 bps" consistently, but the friction constant in the V24 code (`FRIC = 2.0`) is subtracted from bps-denominated returns without explicit unit documentation.

2. **Single-gate design inapplicable to four artifact classes.** The `>5 bps mean net` threshold is a *standalone Alpha gate* incorrectly applied to all candidates. It is inappropriate for:
   - **State/Condition artifacts** (should not require standalone profitability);
   - **Rare-event Alpha** (should focus on per-event expectancy, not frequency-weighted annualized return);
   - **Regime specialists** (should prove value inside regime, not unconditionally).

3. **Mean-only absolute gate ignores outlier-driven results.** A candidate with mean net +6 bps but median net -3 bps would PASS the current gate while being fundamentally unreliable. The framework lacks robustness/lower-bound evidence requirements.

**Recommendation:** Implement a four-class G1 framework with artifact-specific gates. No numeric thresholds should be changed until unit ambiguity is resolved and the governance owner ratifies the new framework.

---

## 2. Current G1 Framework

### 2.1 Absolute Expectancy Gate

The current gate is:

```
Mean Net = Mean Gross − Friction
```

Classification:
- **PASS:** Mean Net > 5 bps
- **MARGINAL:** 0 < Mean Net ≤ 5 bps
- **FAIL:** Mean Net ≤ 0 bps

This is hardcoded in `research/v24_g1_screen.py`:
```python
econ = "PASS" if mn > 5 else ("MARGINAL" if mn > 0 else "FAIL")
```

### 2.2 Friction Model

Fixed at 2.0 bps round-trip. Applied identically to all instruments. No instrument-specific scaling.

### 2.3 Counterfactual Gate

Treatment vs Registered Counterfactual:
- **TREATMENT SUPERIOR:** Mean net AND median net both higher for treatment
- **COUNTERFACTUAL SUPERIOR:** Both lower for treatment
- **SIMILAR:** Mixed signals

Promotion requires TREATMENT SUPERIOR.

### 2.4 Evidence Requirements

No formal N minimum for G1. Zero-event candidates are automatically rejected. Sample size affects interpretation but does not gate promotion.

### 2.5 Payoff Distribution

Currently assessed narratively. No formal metric required. Mean-only evaluation is standard.

### 2.6 Executable Capture

Entry at exact defined timestamp. No future-bar filtering. No MFE/MAE contamination. Checked narratively.

---

## 3. Origin of the >5 BPS Gate

### 3.1 Repository Evidence

The `>5 bps` threshold first appears explicitly as a *stated requirement* in the **V23 G1 artifact** (2026-08-27):

> "Fails to clear the >5 bps absolute headroom required for Alpha validation"

The V24 G1 script codifies it as a programmatic gate.

### 3.2 No Prior Formal Derivation

No artifact in the repository explicitly:
- derives the 5 bps threshold from execution economics;
- calibrates it against historical friction or slippage;
- ratifies it as a governance standard for all artifact classes.

### 3.3 Classification

> **THE >5 BPS GATE IS A GOVERNANCE HEURISTIC WITHOUT IDENTIFIED EMPIRICAL CALIBRATION OR FORMAL DERIVATION.**

It was likely introduced as a reasonable standalone Alpha threshold — sufficient to cover friction (2 bps) plus a safety margin — but was never explicitly justified in writing.

### 3.4 Appropriate Scope

The gate is *reasonable* for standalone Alpha promotion. It is *inappropriate* for State/Condition evaluation, which should not require standalone profitability.

---

## 4. Friction Unit Audit

### 4.1 Current Assumption

All G1 artifacts state:
> "Friction: 2.0 bps (Standard Nasdaq-100 CFD spread round-trip)"

### 4.2 Mathematical Relationship

For an instrument at price P:
```
basis_points = points / P × 10,000
```

For USATECHIDXUSD at P ≈ 30,000:
```
2 bps = 2/10,000 × 30,000 = 6 index points
2 index points = 2/30,000 × 10,000 = 0.667 bps
```

### 4.3 G1 Script Analysis

The V24 G1 script calculates returns as:
```python
ret = (c - o) / o * 10000 * dr
```

This produces **basis-point-denominated returns**. The friction (`FRIC = 2.0`) is subtracted directly from these bps returns. This is **correct** — both return and friction are in the same units.

### 4.4 Inconsistency Risk

The friction description "2 bps" could be confused with "2 index points" by future implementers. The V24 code is internally consistent (both in bps), but the *governance language* does not explicitly define the unit model.

### 4.5 Classification

| Aspect | Status |
|---|---|
| V24 code internal consistency | CORRECT |
| V19–V23 narrative consistency | CORRECT |
| Governance unit documentation | AMBIGUOUS |
| Risk of future unit confusion | MATERIAL |

**Recommendation:** The governance framework must explicitly define:
> "All friction, returns, and economic thresholds are in **basis points** (1 bp = 0.01% of price)."

---

## 5. Instrument-Normalized Cost Model

### 5.1 Current State

No formal universal cost model exists. A fixed 2.0 bps is applied to all instruments.

### 5.2 Known Instruments

| Instrument | Approx Price | 2 bps = | 2 points = |
|---|---|---|---|
| USATECHIDXUSD | ~30,000 | 6 points | 0.667 bps |
| XAUUSD | ~3,300 | 66 cents | 6.06 bps |
| XAGUSD | ~38 | 7.6 cents | 526 bps |

### 5.3 Recommendation

A governance specification should explicitly state:

> Friction for each instrument is denominated in basis points (bps). For USATECHIDXUSD, the governed friction is 2.0 bps round-trip, representing approximately 6 index points at current price levels. The 2.0 bps figure includes estimated spread + slippage + commission at retail CFD execution quality.

This documentation prevents future confusion without changing the actual computation.

---

## 6. Mean vs Median

### 6.1 Current Treatment

G1 currently evaluates mean net and median net but gates exclusively on mean net.

### 6.2 Failure Mode

A candidate with:
- Mean net: +6 bps (PASSES gate)
- Median net: -3 bps

Would be promoted despite being driven by right-tail outliers.

### 6.3 Evidence from Repository

No V19–V24 candidate had mean > 5 bps AND median < 0 simultaneously, so this failure mode has not yet been triggered. But the framework does not guard against it.

### 6.4 Recommendation

The framework should require:
- **Mean net > 5 bps** (primary gate);
- **Median net > 0 bps** (secondary gate);
- **Payoff concentration analysis** (diagnostic, not gating).

A right-skewed strategy is not automatically invalid, but median-negative strategies require explicit governance override.

---

## 7. Outlier / Tail Risk

### 7.1 Current Treatment

No formal tail-risk metrics are required. Payoff structure is described narratively.

### 7.2 Dangers

- Positive mean driven by one event;
- Large right-tail dependence;
- Fat left tails masked by few large winners;
- Unstable dispersion.

### 7.3 Recommendation

At **G1**, require:
- Payoff concentration: % of total returns contributed by top 10% of events (diagnostic);
- Worst-event loss (diagnostic).

At **G2 / Scientific Qualification**, require:
- Bootstrap confidence interval;
- Lower confidence bound (mandatory gate).

---

## 8. Robustness / Lower-Bound Evidence

### 8.1 Current Treatment

Not required at G1.

### 8.2 Assessment

G1 is an *economic plausibility screen*, not a scientific qualification. Robustness testing belongs at G2 or later.

**However:** The framework should require that G1 results are not driven by a single event. A simple diagnostic (e.g., "excluding the best event, is the mean still positive?") would prevent promoting fragile strategies.

### 8.3 Recommendation

- **G1:** Diagnostic only (exclude-best-event analysis);
- **G2:** Bootstrap lower-bound required;
- **Scientific Qualification:** Full robustness required.

---

## 9. Standalone Alpha Qualification

### 9.1 Recommended G1 Gate

| Metric | Requirement | Type |
|---|---|---|
| Mean Net | > 5 bps | MANDATORY |
| Median Net | > 0 bps | MANDATORY |
| Friction | Instrument-specific, bps-denominated | GOVERNED |
| Counterfactual | Treatment Superior | MANDATORY |
| N | ≥ 10 (or rare-event override) | MANDATORY |
| Executable Capture | Verified | MANDATORY |
| Payoff Concentration | < 50% from top 10% of events | DIAGNOSTIC |
| Worst-Event Loss | Documented | DIAGNOSTIC |

### 9.2 Rationale

The current `>5 bps mean net` gate is reasonable for standalone Alpha. Adding median > 0 prevents outlier-driven promotion. The counterfactual gate remains essential.

---

## 10. Rare-Event Alpha Qualification

### 10.1 Current Treatment

Identical to standalone Alpha. Frequency is noted but does not affect gating.

### 10.2 Problem

A rare-event candidate with 3–5 events/year and +60 bps per event fails the *frequency implicit bias* in the framework — not because it fails the explicit gate, but because G1/G2 chronological holdouts require high N, and rare events cannot accumulate sufficient events.

### 10.3 Recommended G1 Gate

| Metric | Requirement | Type |
|---|---|---|
| Per-Event Mean Net | > 20 bps | MANDATORY |
| Per-Event Median Net | > 0 bps | MANDATORY |
| N | ≥ 3 independent historical events | MANDATORY |
| Event Integrity | Events independently defined | MANDATORY |
| Counterfactual | Treatment Superior | MANDATORY |
| Economic Mechanism | Plausible displacement source | MANDATORY |
| Frequency | Not gated (event-count validated later) | N/A at G1 |

### 10.4 Rationale

CAND-024 (+40.59 bps) and CAND-035 (+62.36 bps) demonstrate that rare events can have massive per-event economics. The current framework does not accommodate this class. Per-event expectancy is the correct primary metric.

---

## 11. State / Condition Qualification

### 11.1 Current Treatment

State candidates are evaluated identically to Alpha candidates — requiring standalone absolute net expectancy. This is incorrect.

### 11.2 Problem

A State/Condition artifact (e.g., CAND-059: First Touch > Second Touch) does not generate standalone trades. It adds *incremental information* to a downstream Alpha. Requiring standalone profitability is a category error.

### 11.3 Recommended G1 Gate

| Metric | Requirement | Type |
|---|---|---|
| Incremental Delta | Treatment Δ > Counterfactual Δ by > 2 bps | MANDATORY |
| Scientifically Qualified Target | Alpha target identified | MANDATORY |
| Causal Observability | State measurable with available data | MANDATORY |
| Counterfactual | Discriminating (not vs random) | MANDATORY |
| Standalone Profitability | NOT REQUIRED | N/A |

### 11.4 Rationale

CAND-059 proved FIRST TOUCH > SECOND TOUCH with a ~4.5 bps informational delta. This is valuable state information. The current framework rejected it because standalone expectancy was negative — but standalone expectancy is the wrong question for a state artifact.

---

## 12. Regime / Specialist Qualification

### 12.1 Current Treatment

No explicit regime/specialist gate exists. Regime specialists are evaluated as standalone Alphas.

### 12.2 Problem

A valid regime specialist may have:
- Strong economics inside its operating regime;
- Zero or negative results outside regime;
- Low unconditional expectancy (because regime is rare).

The current framework punishes regime specialization by measuring unconditional performance.

### 12.3 Recommended G1 Gate

| Metric | Requirement | Type |
|---|---|---|
| In-Regime Mean Net | > 5 bps (inside regime only) | MANDATORY |
| Regime Definition | Objective, testable, pre-registered | MANDATORY |
| In-Regime N | ≥ 5 | MANDATORY |
| Out-of-Regime Behavior | Documented (inactive acceptable) | DIAGNOSTIC |
| Counterfactual | Treatment Superior (in regime) | MANDATORY |

### 12.4 Rationale

A module that is silent during trending markets and active during ranges is not failing — it is specializing. The gate should evaluate it only within its valid operating regime.

---

## 13. Counterfactual Gate

### 13.1 Current Assessment

The counterfactual gate is **correctly designed** for its intended purpose: discriminating whether the treatment condition adds information beyond the control.

### 13.2 V24 Result

All three V24 candidates showed TREATMENT SUPERIOR — real informational value. This demonstrates the gate works.

### 13.3 Clarification Needed

The gate answers: *Does the condition add information?*

It does NOT answer: *Is the absolute economics sufficient?*

These are separate questions. The current framework correctly evaluates both but should be explicit that **counterfactual superiority alone is not sufficient for promotion**.

---

## 14. Incremental Information Value

### 14.1 Current Treatment

Not formally defined. Implicitly measured by Treatment − Counterfactual mean net difference.

### 14.2 Formal Definition

```
Δ = Treatment Mean Net − Counterfactual Mean Net
```

### 14.3 Assessment

V24 CAND-071: Δ = -1.99 − (-2.86) = +0.87 bps (informational value exists)
V24 CAND-072: Δ = -5.15 − (-10.98) = +5.83 bps (strong informational value)
V24 CAND-073: Δ = -1.98 − (-2.57) = +0.59 bps (small informational value)

### 14.4 Recommendation

Δ should be reported as a diagnostic metric at G1. A minimum meaningful Δ should be defined for State/Condition candidates (see Part 11). For Alpha candidates, Δ is informative but the primary gate remains absolute economics.

---

## 15. Frequency Doctrine

### 15.1 Current Treatment

Frequency is noted but not gated. High frequency is implicitly preferred because G2 chronological holdouts require sufficient events.

### 15.2 Assessment

This creates an implicit bias toward high-frequency candidates, even though the Dual-Path Governance explicitly states:

> "LOW FREQUENCY IS NOT AUTOMATICALLY A KILL CONDITION."

### 15.3 Recommendation

- **Standalone Alpha:** Frequency should be a *diagnostic*, not a *gate*. High frequency is preferred for core strategies but not mandatory.
- **Rare-Event Alpha:** Frequency is handled by event-count forward validation, not calendar-duration holdouts.
- **State/Condition:** Frequency of the state occurrence matters for practical utility but should not gate G1 promotion.

---

## 16. Capital / Opportunity Efficiency

### 16.1 Current Treatment

Not evaluated at G1. Implicitly evaluated by G2 forward validation.

### 16.2 Assessment

Three distinct metrics exist:
1. **Per-event expectancy:** bps per event (most relevant for rare events);
2. **Per-unit-time expectancy:** bps per year (relevant for capital utilization);
3. **Per-unit-capital expectancy:** bps per dollar of risk (relevant for sizing).

### 16.3 Recommendation

- **G1:** Report per-event expectancy (all classes) and per-unit-time (for Alpha candidates);
- **G2:** Full capital efficiency model required;
- **System Qualification:** Mandatory.

---

## 17. V19–V24 Empirical Pattern

### 17.1 Candidate Registry

| Cycle | Candidates | Type | Treatment Superior? | Absolute Economics | Verdict |
|---|---|---|---|---|---|
| V19 | CAND-056 | Alpha | Counterfactual Superior | Negative | INSUFFICIENT |
| V19 | CAND-057 | State | Zero-Event | N/A | ZERO-EVENT |
| V19 | CAND-058 | Alpha | Counterfactual Superior (+73 vs +46) | Negative | INSUFFICIENT |
| V20 | CAND-059 | State | Treatment Superior (+4.5 bps) | Negative standalone | INSUFFICIENT |
| V20 | CAND-060 | Alpha | Zero-Event | N/A | ZERO-EVENT |
| V20 | CAND-061 | Alpha | Negative | Negative | INSUFFICIENT |
| V21 | CAND-062 | Alpha | Counterfactual Superior | Negative | INSUFFICIENT |
| V21 | CAND-063 | State | Counterfactual Superior | N/A | INSUFFICIENT |
| V21 | CAND-064 | State | Counterfactual Superior (falsified) | N/A | FALSIFIED |
| V22 | CAND-065 | State | Evidence-limited (N=27) | Delta +11.46 bps | EVIDENCE-LIMITED |
| V22 | CAND-066 | Alpha | Counterfactual Superior | Negative | INSUFFICIENT |
| V22 | CAND-067 | State | Zero-Event | N/A | ZERO-EVENT |
| V23 | CAND-068 | Alpha | Zero-Event | N/A | ZERO-EVENT |
| V23 | CAND-069 | State | Treatment Superior (+0.75 bps) | Flat | INSUFFICIENT |
| V23 | CAND-070 | Alpha | Falsified | N/A | FALSIFIED |
| V24 | CAND-071 | Alpha | Treatment Superior (+0.87 bps Δ) | Negative | INSUFFICIENT |
| V24 | CAND-072 | Alpha | Treatment Superior (+5.83 bps Δ) | Negative | INSUFFICIENT |
| V24 | CAND-073 | Alpha | Treatment Superior (+0.59 bps Δ) | Negative | INSUFFICIENT |

### 17.2 Aggregate Pattern

- **18 candidates** across 6 cycles;
- **0 G2 promotions**;
- **3 zero-events;**
- **3 falsified/hypothesis contradicted;**
- **5 counterfactual-superior** (mechanism didn't work);
- **4 treatment-superior but economically negative** (informational value exists, economics don't survive friction);
- **3 evidence-limited** (N too small);
- **0 standalone positive expectancy** from V19–V24.

### 17.3 Pattern Classification

> **Dominant pattern: Informationally interesting conditions with insufficient absolute displacement to survive retail friction.**

This is NOT evidence of a broken G1 gate. The candidates genuinely lack friction-surviving economics. However, it IS evidence of a **candidate-generation bias** — G0 repeatedly produces conditions (price patterns, timing, structural transitions) that carry microstructural information but cannot generate large enough post-entry moves to cover even 2 bps of friction.

---

## 18. Candidate-Generation vs Qualification Bias

### 18.1 Question

Are G1 failures caused by:
- (A) G0 generating bad candidates? or
- (B) G1 using the wrong gate?

### 18.2 Evidence

**Evidence for (A) — candidate-generation bias:**
- All V19–V24 candidates tested price-pattern/structural hypotheses;
- None tested direct economic displacement mechanisms (settlement, benchmark, forced flow);
- Treatment-superior candidates show real microstructural information, but the information manifests as <1 bps deltas — too small to monetize;
- The absolute economics are genuinely negative (not just gate-calibration issues).

**Evidence for (B) — qualification-framework bias:**
- State/Condition candidates are incorrectly evaluated with the standalone Alpha gate;
- Rare-event candidates cannot use chronological holdouts;
- The >5 bps threshold was never formally calibrated;
- Mean-only gating ignores outlier risk.

### 18.3 Conclusion

> **Both biases exist simultaneously.**
>
> The *candidate-generation* bias is more impactful: generating price-pattern conditions rather than displacement mechanisms produces a fundamentally low-economic-magnitude pipeline.
>
> The *qualification-framework* bias is real but secondary: fixing the gate would rescue a few informationally valuable artifacts (CAND-059, CAND-065) as state candidates, but would NOT rescue any V19–V24 Alpha candidates, because their absolute economics are genuinely negative.

---

## 19. Four-Class G1 Framework Assessment

### 19.1 Current State

All candidates are evaluated against a single Alpha-centric gate. The framework recognizes four artifact classes (Alpha, Rare-Event, State, Regime) but applies identical gating to all.

### 19.2 Assessment

> **Separate artifact-class gates are required.**

The evidence is clear:
- CAND-059 (State) was rejected for lacking standalone profitability — a category error;
- CAND-024/CAND-035 (Rare-Event) cannot use chronological holdouts — a structural incompatibility;
- A future regime specialist would be rejected for low unconditional expectancy — a design flaw.

### 19.3 Proposed Separation

| Class | Primary Gate | Secondary Gate | Counterfactual |
|---|---|---|---|
| Standalone Alpha | Mean Net > 5 bps | Median Net > 0 bps | Treatment Superior |
| Rare-Event Alpha | Per-Event Net > 20 bps | Per-Event Median > 0 bps | Treatment Superior |
| State/Condition | Δ > 2 bps vs counterfactual | Qualified target exists | Discriminating |
| Regime/Specialist | In-Regime Mean Net > 5 bps | Regime definition objective | Treatment Superior (in regime) |

---

## 20. Rescue Firewall

### 20.1 Principle

> A new qualification framework CANNOT retroactively rescue a candidate that failed its correctly specified original gate.

### 20.2 Exception

> A candidate rejected *solely* because the wrong artifact-class gate was applied may be eligible for future governance review.

### 20.3 Application to V24

V24 candidates (CAND-071/072/073) failed the standalone Alpha gate correctly. Their absolute economics are genuinely negative. The new framework would NOT rescue them as standalone Alphas.

However:
- CAND-072's Friday compression condition (Δ = +5.83 bps) could theoretically qualify as a **State/Condition** artifact under the new framework — but only if a downstream Alpha target is identified and a formal G0 registration occurs. No rescue is performed here.

---

## 21. V24 Status

> **V24 CLOSED — NO G2 CANDIDATE**

This audit does not reopen V24. Any future reclassification requires explicit governance authorization.

---

## 22. Proposed G1 Framework V3

### 22.1 Purpose

Replace the single-gate G1 with four artifact-class-specific evaluation tracks.

### 22.2 Common Requirements (All Classes)

| Requirement | Type |
|---|---|
| Executable capture verified | MANDATORY |
| No future-bar contamination | MANDATORY |
| Friction in bps, instrument-specified | GOVERNED |
| Counterfactual registered and discriminating | MANDATORY |
| Data availability confirmed | MANDATORY |

### 22.3 Standalone Alpha Gate

| Metric | Threshold | Type |
|---|---|---|
| Mean Net | > 5 bps | MANDATORY |
| Median Net | > 0 bps | MANDATORY |
| Counterfactual | Treatment Superior | MANDATORY |
| N | ≥ 10 | MANDATORY |
| Payoff Concentration | < 50% from top 10% of events | DIAGNOSTIC |
| Exclude-Best-Event Mean | > 0 bps | DIAGNOSTIC |

### 22.4 Rare-Event Alpha Gate

| Metric | Threshold | Type |
|---|---|---|
| Per-Event Mean Net | > 20 bps | MANDATORY |
| Per-Event Median Net | > 0 bps | MANDATORY |
| N (historical events) | ≥ 3 | MANDATORY |
| Event Integrity | Independently defined, non-overlapping | MANDATORY |
| Counterfactual | Treatment Superior | MANDATORY |
| Economic Mechanism | Plausible displacement source documented | MANDATORY |
| Frequency | Not gated at G1 | N/A |

### 22.5 State / Condition Gate

| Metric | Threshold | Type |
|---|---|---|
| Incremental Δ | > 2 bps (Treatment vs Counterfactual) | MANDATORY |
| Qualified Target Alpha | Identified and documented | MANDATORY |
| Causal Observability | State measurable with available data | MANDATORY |
| Counterfactual | Discriminating (not vs random) | MANDATORY |
| Standalone Profitability | NOT REQUIRED | N/A |

### 22.6 Regime / Specialist Gate

| Metric | Threshold | Type |
|---|---|---|
| In-Regime Mean Net | > 5 bps | MANDATORY |
| Regime Definition | Objective, testable, pre-registered | MANDATORY |
| In-Regime N | ≥ 5 | MANDATORY |
| Out-of-Regime Behavior | Documented | DIAGNOSTIC |
| Counterfactual (in regime) | Treatment Superior | MANDATORY |

### 22.7 Required Governance Decisions

| Decision | Current | Proposed | Status |
|---|---|---|---|
| >5 bps standalone Alpha gate | Heuristic | Keep (with median add) | REQUIRES OWNER RATIFICATION |
| Rare-event per-event threshold | None | >20 bps | REQUIRES OWNER RATIFICATION |
| State Δ threshold | None | >2 bps | REQUIRES OWNER RATIFICATION |
| Median > 0 requirement | None | Added | REQUIRES OWNER RATIFICATION |
| Regime in-regime gate | None | >5 bps in regime | REQUIRES OWNER RATIFICATION |
| Friction unit documentation | Ambiguous | Explicitly bps | REQUIRES OWNER RATIFICATION |

---

## 23. Required Governance Decisions

The following decisions require explicit governance owner ratification before implementation:

1. **Ratify the four-class G1 framework** (Standalone Alpha, Rare-Event, State, Regime);
2. **Ratify the >5 bps standalone Alpha threshold** as a governance standard (not just a heuristic);
3. **Ratify the >20 bps per-event threshold** for rare-event candidates;
4. **Ratify the >2 bps Δ threshold** for state/condition artifacts;
5. **Ratify median > 0 as a mandatory secondary gate** for Alpha candidates;
6. **Ratify explicit bps unit documentation** in all governance artifacts;
7. **Decide whether to apply the new framework prospectively only** (recommended) or to allow retrospective reclassification of specific candidates.

---

## 24. Protected Forward Runtime

### CAND-015
> ACTIVE / PROTECTED / UNTOUCHED

### CAND-024
> ACTIVE / PROTECTED / UNTOUCHED

Canonical: `CAND-024:CANONICAL:925495a8`

### CAND-035
> ACTIVE / PROTECTED / UNTOUCHED

Canonical: `CAND-035:CANONICAL:ddc5d0e9`

Do not inspect forward performance. Do not modify runtime.

---

## 25. Next Milestone

> GOVERNANCE OWNER RATIFICATION OF G1 FRAMEWORK V3

Until ratification:
- V24 remains closed;
- No V25 generation;
- No retrospective reclassification;
- Forward observation continues independently;
- The proposed framework is a recommendation, not a rule.

---

## 26. Integrity

- No candidates were rescued;
- No parameters were changed;
- No experiments were run;
- No forward results were inspected;
- No research was executed;
- V24 closure is preserved;
- The audit is read-only governance analysis;
- All conclusions are grounded in repository evidence.
