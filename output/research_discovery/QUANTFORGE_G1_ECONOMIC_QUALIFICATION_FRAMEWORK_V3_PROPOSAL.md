# QUANTFORGE — G1 ECONOMIC QUALIFICATION FRAMEWORK V3
# GOVERNANCE RATIFICATION PROPOSAL
# DATE: 2026-08-29
# STATUS: PENDING OWNER RATIFICATION

---

## 1. Purpose

This document proposes a replacement for the current single-gate G1 Economic Plausibility Screen. The new framework introduces four artifact-class-specific qualification paths, explicit friction-unit governance, distributional robustness requirements, and a clear separation between absolute economics and conditional information value.

This proposal does NOT:
- rescue any failed candidate;
- reopen V24;
- generate V25;
- modify forward runtime;
- alter any existing candidate definition.

This proposal IS:
- a governance specification pending owner ratification;
- prospective in application;
- grounded in the completed audit (QUANTFORGE_G1_ECONOMIC_QUALIFICATION_CRITERIA_AUDIT_V1.md).

---

## 2. Problem With Current G1

### 2.1 Single-Gate Design

The current G1 applies one absolute-economic gate (Mean Net > 5 bps) to all candidates regardless of artifact class. This is incorrect for:

- **State/Condition** artifacts, which do not generate standalone trades;
- **Rare-Event Alpha**, which cannot accumulate sufficient N within standard G2 chronological holdouts;
- **Regime Specialists**, which intentionally suppress activity outside their operating regime.

### 2.2 Unit Ambiguity

The friction constant (2.0 bps) is applied consistently in code but ambiguously documented in governance. "2 bps" could be confused with "2 index points" by future implementers. No explicit unit convention exists.

### 2.3 Mean-Only Gating

The absolute gate uses mean net expectancy alone. A candidate with mean +6 bps but median -3 bps would pass despite being outlier-dependent. No distributional robustness check exists at G1.

### 2.4 No Information Delta Distinction

The framework does not separately report absolute economics and incremental condition value. A treatment that beats its control while remaining economically negative is correctly classified as "INSUFFICIENT" but the informational value is not formally captured.

### 2.5 Implicit Frequency Bias

Although governance doctrine states "low frequency is not automatically a kill condition," the framework's structure implicitly favors high-frequency candidates because G2 chronological holdouts require accumulated events.

---

## 3. Design Principles

1. **Artifact-specific qualification.** Each class has its own gate, metrics, and evidence requirements.
2. **Separate absolute economics from conditional information.** Every G1 report states both independently.
3. **Explicit friction units.** All economic results use basis points. No silent mixing of units.
4. **Distributional awareness.** Mean is necessary but not sufficient. Median and tail diagnostics are required.
5. **Minimum complexity.** Simple, interpretable gates preferred over dozens of interacting statistical conditions.
6. **Prospective application.** V3 applies to new candidates only. Historical verdicts are not retroactively changed.
7. **Research capital efficiency.** The framework exists to allocate research investment wisely, not to maximize rejection count.

---

## 4. Four Artifact Classes

### CLASS A — STANDALONE ALPHA

> An event or condition that could operate as an independent executable trading strategy.

**Primary question:** Does this event produce friction-surviving positive expectancy with sufficient evidence?

### CLASS B — RARE-EVENT ALPHA

> A low-frequency event with strong per-event economics that justifies a specialized module.

**Primary question:** Is the per-event economic value large enough to justify waiting, and is the event objectively defined and independently occurring?

### CLASS C — STATE / CONDITION

> A reproducible market condition that provides incremental information for a legitimate downstream Alpha.

**Primary question:** Does the state materially improve the conditional distribution of a properly defined Alpha target?

### CLASS D — REGIME / SPECIALIST

> A module that intentionally operates only within a specific, objectively defined market regime.

**Primary question:** Does the module produce strong economics inside its defined regime, and is the regime definition objective and testable?

---

## 5. Standalone Alpha Gate

### 5.1 Primary Question

Does this event produce friction-surviving positive expectancy with sufficient evidence and executable integrity?

### 5.2 Hard Gates (Must Pass All)

| Metric | Threshold | Status |
|---|---|---|
| Mean Net | > 5 bps | GOVERNANCE HEURISTIC — REQUIRES OWNER RATIFICATION |
| Median Net | > 0 bps | GOVERNANCE HEURISTIC — REQUIRES OWNER RATIFICATION |
| Counterfactual | Treatment Superior | EVIDENCE-SUPPORTED |
| Minimum N | ≥ 10 independent events | GOVERNANCE HEURISTIC — REQUIRES OWNER RATIFICATION |
| Executable Capture | Verified — no future-bar contamination | EVIDENCE-SUPPORTED |
| Friction Unit | Explicit bps, instrument-specified | NEW STANDARD |

### 5.3 Diagnostic Metrics (Reported, Not Gating at G1)

| Metric | Purpose |
|---|---|
| Payoff Concentration | % of total returns from top 10% of events — outlier detection |
| Exclude-Best-Event Mean | Mean excluding the single best event — fragility check |
| Worst-Event Loss | Maximum single-event loss — downside documentation |
| Win Rate | Descriptive, not gating |
| Frequency | Opportunities per year — descriptive |

### 5.4 Rationale

The >5 bps mean net threshold provides approximately 2.5x friction coverage for the governed 2.0 bps round-trip cost. Adding median > 0 prevents outlier-driven promotion. N ≥ 10 ensures basic evidence sufficiency without requiring the high N needed for bootstrap robustness (which belongs at G2).

---

## 6. Rare-Event Alpha Gate

### 6.1 Primary Question

Is the per-event economic value large enough to justify waiting, and is the event objectively defined and independently occurring?

### 6.2 Hard Gates (Must Pass All)

| Metric | Threshold | Status |
|---|---|---|
| Per-Event Mean Net | > 20 bps | GOVERNANCE HEURISTIC — REQUIRES OWNER RATIFICATION |
| Per-Event Median Net | > 0 bps | GOVERNANCE HEURISTIC — REQUIRES OWNER RATIFICATION |
| Minimum Historical Events | ≥ 3 independent, non-overlapping events | GOVERNANCE HEURISTIC — REQUIRES OWNER RATIFICATION |
| Event Integrity | Events independently defined and non-overlapping | EVIDENCE-SUPPORTED |
| Counterfactual | Treatment Superior | EVIDENCE-SUPPORTED |
| Economic Mechanism | Plausible displacement source documented | EVIDENCE-SUPPORTED |
| Executable Capture | Verified | EVIDENCE-SUPPORTED |

### 6.3 Diagnostic Metrics

| Metric | Purpose |
|---|---|
| Annual Frequency | Opportunities per year — practical planning |
| Per-Event Median | Distributional center |
| Maximum Waiting Period | Estimated longest gap between events |
| Event Size Distribution | Consistency of per-event magnitude |

### 6.4 Frequency Treatment

Frequency is NOT a hard gate at G1. Low frequency alone is not a rejection criterion. The question is:

> Is the per-event economics strong enough to justify the waiting period?

Forward validation for rare events uses event-count accumulation, not calendar-duration holdouts.

### 6.5 Rationale

The 20 bps per-event threshold represents approximately 10x friction coverage. This high bar compensates for the small sample sizes inherent in rare events — with N ≥ 3, each event must carry substantial weight. The threshold ensures that even if observed economics overstate true economics by 50%, the event still survives friction.

---

## 7. State / Condition Gate

### 7.1 Primary Question

Does the state provide reproducible incremental information for a legitimate downstream Alpha?

### 7.2 Hard Gates (Must Pass All)

| Metric | Threshold | Status |
|---|---|---|
| Incremental Δ | > 0 bps (Treatment mean net minus Counterfactual mean net) | MINIMUM GATE — threshold value REQUIRES OWNER RATIFICATION |
| Qualified Downstream Alpha | Identified and documented | EVIDENCE-SUPPORTED |
| Causal Observability | State measurable with available data | EVIDENCE-SUPPORTED |
| Counterfactual | Discriminating (not vs random) | EVIDENCE-SUPPORTED |
| Standalone Profitability | NOT REQUIRED | DESIGN PRINCIPLE |

### 7.3 Diagnostic Metrics

| Metric | Purpose |
|---|---|
| Incremental Median Δ | Distributional information |
| Right-Tail Change | Does the state improve extreme outcomes? |
| Left-Tail Reduction | Does the state reduce worst-case outcomes? |
| Interaction Stability | Does the delta hold across time periods? |

### 7.4 Future Interaction Testing

State qualification at G1 establishes informational value. Actual production deployment requires:

1. A formally qualified downstream Alpha target;
2. Interaction study demonstrating the state improves the Alpha's distribution;
3. Stability across time periods;
4. No rescue of a failed Alpha through state attachment.

### 7.5 Non-Independence Warning

A State/Condition artifact is NOT independently tradeable. It gains value only through interaction with a qualified Alpha. This must be explicitly stated in every State G1 report.

### 7.6 Rationale

States should not be evaluated on standalone PnL because they do not generate standalone trades. The incremental delta (Treatment minus Counterfactual) measures the informational contribution directly. A positive delta indicates the state carries real information, regardless of whether the underlying Alpha is profitable in isolation.

---

## 8. Regime / Specialist Gate

### 8.1 Primary Question

Does the module produce strong economics inside its defined regime, and is the regime definition objective and testable?

### 8.2 Hard Gates (Must Pass All)

| Metric | Threshold | Status |
|---|---|---|
| In-Regime Mean Net | > 5 bps | GOVERNANCE HEURISTIC — REQUIRES OWNER RATIFICATION |
| In-Regime Median Net | > 0 bps | GOVERNANCE HEURISTIC — REQUIRES OWNER RATIFICATION |
| Regime Definition | Objective, testable, pre-registered | EVIDENCE-SUPPORTED |
| In-Regime N | ≥ 5 events | GOVERNANCE HEURISTIC — REQUIRES OWNER RATIFICATION |
| Counterfactual (in regime) | Treatment Superior | EVIDENCE-SUPPORTED |
| Out-of-Regime Behavior | Documented (inactive is acceptable) | DIAGNOSTIC |

### 8.3 Unconditional Economics

Unconditional economics are reported but NOT gated. A regime specialist that is intentionally inactive 80% of the time will have diluted unconditional returns. This is by design, not a defect.

### 8.4 Regime Transition Stability

The regime definition must be testable across regime transitions. A regime that produces contradictory signals at its own boundaries requires investigation before G2.

### 8.5 Rationale

Regime specialists are legitimate modular components. Their economics are evaluated only within their valid operating environment. The objective regime definition requirement prevents post-hoc regime construction.

---

## 9. Friction Standard

### 9.1 Governance Rule

> ALL ECONOMIC RESULTS IN G1 AND BEYOND MUST USE BASIS POINTS (bps) AS THE PRIMARY UNIT.
>
> 1 basis point = 0.01% of instrument price.

### 9.2 Instrument Documentation

Every G1 artifact must state the instrument, approximate price level, and friction in bps with the equivalent price-point cost.

**Example for USATECHIDXUSD:**

| Parameter | Value |
|---|---|
| Instrument | USATECHIDXUSD (USTECm) |
| Approximate Price | ~30,000 |
| Friction (bps) | 2.0 bps round-trip |
| Friction (points) | ~6 index points |
| Friction Source | Spread + estimated slippage + commission |
| Execution Quality | Retail CFD |

### 9.3 Universal Convention

Returns, thresholds, deltas, and friction are ALL expressed in bps unless explicitly stated otherwise. No mixing of bps and price points in the same calculation.

### 9.4 Status

> **NEW STANDARD — REQUIRES OWNER RATIFICATION**

This convention is consistent with existing V19–V24 code but adds explicit documentation requirements.

---

## 10. Mean / Median Treatment

### 10.1 Current State

Mean net is the primary gate. Median is reported but not gating.

### 10.2 Proposed Treatment

For **Standalone Alpha** and **Regime Specialist**:
- Mean Net > threshold: HARD GATE;
- Median Net > 0: HARD GATE.

For **Rare-Event Alpha**:
- Per-Event Mean Net > threshold: HARD GATE;
- Per-Event Median Net > 0: HARD GATE.

For **State/Condition**:
- Mean Δ > 0: HARD GATE;
- Median Δ reported as diagnostic.

### 10.3 Mean Positive / Median Negative

A candidate with positive mean and negative median is NOT automatically rejected. It is flagged for:

- Payoff concentration analysis;
- Exclude-best-event sensitivity;
- G2 robustness testing.

The median gate prevents promoting strategies where the typical event loses money.

### 10.4 Status

> **MEDIAN REQUIREMENT — GOVERNANCE HEURISTIC — REQUIRES OWNER RATIFICATION**

---

## 11. Tail / Robustness Treatment

### 11.1 G1 Role

G1 is an economic plausibility screen. Full robustness testing (bootstrap, confidence intervals) belongs at G2 or Scientific Qualification.

### 11.2 G1 Requirements

| Metric | Role | Status |
|---|---|---|
| Payoff Concentration | Diagnostic — outlier detection | REPORTED |
| Exclude-Best-Event Mean | Diagnostic — fragility check | REPORTED |
| Worst-Event Loss | Diagnostic — downside documentation | REPORTED |
| Win Rate | Diagnostic — descriptive | REPORTED |

### 11.3 G2 Requirements

| Metric | Role | Status |
|---|---|---|
| Bootstrap 95% CI Lower Bound | MANDATORY GATE | EVIDENCE-SUPPORTED |
| Exclude-Best-Event Mean | MANDATORY GATE | EVIDENCE-SUPPORTED |

### 11.4 Rationale

Adding bootstrap to G1 would increase complexity without proportional benefit at the plausibility-screen stage. A simple exclude-best-event diagnostic at G1 catches the worst outlier cases. Full robustness testing is reserved for G2 where the research investment is justified.

---

## 12. Counterfactual Treatment

### 12.1 Preserved Principle

> CONDITION VALUE ≠ ABSOLUTE ALPHA

Every G1 report must separately state:

1. **Absolute Economics:** Treatment mean net, median net, friction;
2. **Incremental Condition Value:** Treatment minus Counterfactual (both mean and median).

### 12.2 Gate Logic

| Absolute Economics | Condition Value | Classification |
|---|---|---|
| Positive (> threshold) | Treatment Superior | PROMOTE |
| Positive (> threshold) | Similar/Inconclusive | PROMOTE (flag condition uncertainty) |
| Positive (> threshold) | Counterfactual Superior | INVESTIGATE (mechanism concern) |
| Negative | Treatment Superior | CONDITIONAL VALUE — NOT ALPHA |
| Negative | Similar/Inconclusive | INSUFFICIENT |
| Negative | Counterfactual Superior | INSUFFICIENT |

### 12.3 No Misreporting

A candidate with Treatment Superior but negative absolute economics is classified as:

> CONDITIONAL INFORMATION VALUE OBSERVED / ABSOLUTE ALPHA FAILED

It is NOT classified as:
- "validated";
- "promoted";
- "component-qualified."

### 12.4 Status

> **EVIDENCE-SUPPORTED — PRESERVED FROM CURRENT FRAMEWORK**

---

## 13. Information Delta

### 13.1 Definition

```
Δ_mean = Treatment Mean Net − Counterfactual Mean Net
Δ_median = Treatment Median Net − Counterfactual Median Net
```

### 13.2 Role at G1

Delta is a **required diagnostic** for all artifact classes. It is a **hard gate** only for State/Condition artifacts.

### 13.3 Threshold for State/Condition

The minimum meaningful delta for State qualification:

> Δ_mean > 0 bps (minimum) — REQUIRES OWNER RATIFICATION for specific threshold.

A delta must demonstrate that the state adds information beyond the control. The exact minimum threshold depends on:
- The target Alpha's economics;
- The friction of the target Alpha;
- The stability of the delta across time.

**Recommendation:** Do not hard-code a universal state delta threshold at this stage. Instead, require that the delta is:
1. Positive;
2. Stable across time periods (diagnostic);
3. Associated with a qualified downstream Alpha.

> **STATUS: PROVISIONAL — REQUIRES OWNER RATIFICATION**

---

## 14. Frequency

### 14.1 Principle

Frequency is **contextual**, not universal. Its role varies by artifact class.

### 14.2 By Class

| Class | Frequency Role | Hard Gate? |
|---|---|---|
| Standalone Alpha | Diagnostic — reported, not gating | NO |
| Rare-Event Alpha | Handled by event-count forward validation, not G1 | NO |
| State/Condition | State occurrence frequency — reported | NO |
| Regime Specialist | In-regime frequency — diagnostic | NO |

### 14.3 No Minimum Opportunities/Year

The framework does NOT impose a minimum frequency requirement at G1. The question for rare events is economic magnitude per event, not calendar frequency.

### 14.4 Status

> **DESIGN PRINCIPLE — EVIDENCE-SUPPORTED**

---

## 15. Capital / Time Efficiency

### 15.1 Three Metrics

1. **Per-Event Expectancy:** Mean net per event (primary for rare events);
2. **Per-Unit-Time Contribution:** Mean net × frequency per year (primary for standalone Alpha);
3. **Capital/Eportunity Efficiency:** Expectancy per unit of capital at risk (G2+ requirement).

### 15.2 G1 Requirements

| Metric | Required at G1? | Class |
|---|---|---|
| Per-Event Expectancy | YES — primary for Rare-Event | Rare-Event |
| Per-Unit-Time Contribution | REPORTED — diagnostic for Standalone | Standalone |
| Capital Efficiency | NO — belongs at G2+ | All |

### 15.3 Rationale

G1 prevents over-investment in candidates that cannot survive friction. Detailed capital efficiency modeling belongs at G2 where the research investment is justified.

---

## 16. Stage Boundaries

### 16.1 G1 — Economic Plausibility Screen

**Purpose:** Determine whether the hypothesis has enough economic potential to justify a cheap empirical pilot.

**Input:** Candidate definition from G0.

**Output:** PROMOTE / INSUFFICIENT / ZERO-EVENT / BLOCKED.

**What it does NOT do:** Prove robustness, prove reproducibility, prove execution viability, prove component value.

### 16.2 G2 — Cheap Empirical Pilot

**Purpose:** Verify that the economic signal survives basic robustness testing with actual data.

**Input:** G1-promoted candidate.

**Output:** PROMOTE / FAIL / EVIDENCE-LIMITED.

**Key additions:** Bootstrap lower bound, exclude-best-event, time-split stability.

### 16.3 Scientific Qualification

**Purpose:** Confirm reproducibility, robustness, and mechanism integrity.

**Input:** G2 survivor.

**Output:** QUALIFIED / NOT QUALIFIED.

### 16.4 Economic Qualification

**Purpose:** Verify economics survive execution-realistic conditions.

**Input:** Scientifically qualified candidate.

**Output:** ECONOMICALLY QUALIFIED / NOT QUALIFIED.

### 16.5 Component Qualification

**Purpose:** Verify that the artifact adds value when combined with a qualified target.

**Input:** Independently qualified artifact + target Alpha.

**Output:** SYSTEM-QUALIFIED / NOT QUALIFIED.

### 16.6 System Qualification

**Purpose:** Verify portfolio-level properties.

**Input:** Qualified components.

**Output:** SYSTEM APPROVED / NOT APPROVED.

### 16.7 Principle

> Each stage has a distinct purpose. Do not collapse stages. Do not skip stages. Do not use one stage to substitute for another.

---

## 17. Numeric Threshold Audit

### 17.1 — 5 bps (Standalone Alpha Mean Net)

| Dimension | Assessment |
|---|---|
| Origin | Governance heuristic; first explicitly stated in V23 G1 artifact |
| Empirical basis | None identified in repository |
| Statistical basis | None — not derived from data |
| Execution-driven | Partially — covers ~2.5x the 2.0 bps friction |
| Justification | Reasonable margin above friction for standalone Alpha |
| Classification | **GOVERNANCE HEURISTIC — REQUIRES OWNER RATIFICATION** |

### 17.2 — 20 bps (Rare-Event Per-Event Mean Net)

| Dimension | Assessment |
|---|---|
| Origin | Proposed in G1 Framework V3 audit |
| Empirical basis | None — new proposal |
| Statistical basis | Designed as ~10x friction, compensating for small N |
| Execution-driven | Yes — high per-event bar compensates for evidence uncertainty |
| Justification | Ensures rare events survive even if observed economics overstate truth by 50% |
| Classification | **GOVERNANCE HEURISTIC — REQUIRES OWNER RATIFICATION** |

### 17.3 — 2 bps (State Incremental Delta)

| Dimension | Assessment |
|---|---|
| Origin | Proposed in audit |
| Empirical basis | None — new proposal |
| Statistical basis | None |
| Execution-driven | Partially — 2 bps exceeds friction, ensuring the state adds more than cost |
| Justification | A state that improves an Alpha by less than friction may not survive |
| Classification | **PROVISIONAL — REQUIRES OWNER RATIFICATION** |

### 17.4 — N=3 (Rare-Event Minimum Events)

| Dimension | Assessment |
|---|---|
| Origin | Proposed in audit |
| Empirical basis | CAND-024 has ~4.5/yr, CAND-035 has ~4.0/yr; 3 events ≈ 9 months of observation |
| Statistical basis | Minimum for any distributional assessment |
| Execution-driven | Practical minimum for forward event-count validation |
| Justification | Below 3, no meaningful distributional inference is possible |
| Classification | **GOVERNANCE HEURISTIC — REQUIRES OWNER RATIFICATION** |

### 17.5 — N=10 (Standalone Alpha Minimum Events)

| Dimension | Assessment |
|---|---|
| Origin | Proposed in audit |
| Empirical basis | Common rule-of-thumb for basic statistical assessment |
| Statistical basis | Minimum for rudimentary central-limit-based inference |
| Execution-driven | Ensures result is not driven by 1–2 events |
| Justification | Below 10, the mean is highly sensitive to individual events |
| Classification | **GOVERNANCE HEURISTIC — REQUIRES OWNER RATIFICATION** |

---

## 18. Threshold Ratification Status

| Threshold | Value | Classification | Owner Decision Needed |
|---|---|---|---|
| Standalone Alpha Mean Net | > 5 bps | Governance Heuristic | YES — Ratify or Reject |
| Standalone Alpha Median Net | > 0 bps | Governance Heuristic | YES — Ratify or Reject |
| Standalone Alpha N | ≥ 10 | Governance Heuristic | YES — Ratify or Reject |
| Rare-Event Per-Event Mean Net | > 20 bps | Governance Heuristic | YES — Ratify or Reject |
| Rare-Event Per-Event Median Net | > 0 bps | Governance Heuristic | YES — Ratify or Reject |
| Rare-Event N | ≥ 3 | Governance Heuristic | YES — Ratify or Reject |
| State Incremental Δ | > 0 bps (minimum) | Provisional | YES — Ratify, Reject, or Specify |
| Regime In-Regime Mean Net | > 5 bps | Governance Heuristic | YES — Ratify or Reject |
| Regime In-Regime Median Net | > 0 bps | Governance Heuristic | YES — Ratify or Reject |
| Regime In-Regime N | ≥ 5 | Governance Heuristic | YES — Ratify or Reject |
| Friction Unit Standard | bps, instrument-specified | New Standard | YES — Ratify or Reject |
| Median as Hard Gate | Yes (Alpha, Rare-Event, Regime) | Design Choice | YES — Ratify or Reject |

---

## 19. V24 Non-Retroactivity

### 19.1 Rule

> G1 Framework V3 applies PROSPECTIVELY ONLY.

V24 remains CLOSED. CAND-071, CAND-072, CAND-073 are NOT reopened, reclassified, or rescued.

### 19.2 Future Historical Review

Retrospective reclassification of any candidate requires:
1. An explicit governance authorization;
2. A separate dedicated task;
3. Documentation of the reclassification rationale.

This is not performed by the framework proposal itself.

---

## 20. Rescue Firewall

### 20.1 Principle

> Framework improvement is not retroactive candidate rescue.

### 20.2 Application

The new framework would theoretically allow State/Condition evaluation for candidates like CAND-059 (which showed informational value but failed the standalone Alpha gate). However:

- CAND-059 is NOT automatically reclassified;
- Any future State qualification of CAND-059 requires a separate governance-authorized task;
- The task must identify a qualified downstream Alpha target;
- The task must demonstrate interaction stability.

### 20.3 Closed Lines

All explicitly closed research lines from V19–V24 remain closed. The new framework does not reopen them.

---

## 21. Current Register

### Rare-Event Qualification Active

| Candidate | Historical Economics | Frequency | Status |
|---|---|---|---|
| CAND-024 | +40.59 bps net/event | ~4.55/yr | RARE-EVENT QUALIFICATION ACTIVE |
| CAND-035 | +62.36 bps net/event | ~4.09/yr | RARE-EVENT QUALIFICATION ACTIVE |

### Component Candidates

| Candidate | Type | Status |
|---|---|---|
| CAND-042 | Event Opportunist | NOT SCIENTIFICALLY QUALIFIED |

### State Artifacts

| Candidate | Type | Status |
|---|---|---|
| CAND-059 | Freshness / First-Touch | INFORMATIONALLY SUPPORTED / NOT STANDALONE PROFITABLE |
| CAND-065 | Deep Sweep Depth | EVIDENCE-LIMITED / NOT VALIDATED |
| CAND-069 | Mid-Session Anchor | CLOSED / INSUFFICIENT ECONOMIC MAGNITUDE |

### Closed (V24)

| Candidate | Type | Status |
|---|---|---|
| CAND-071 | Gold→Tech Transmission | CLOSED — NEGATIVE ABSOLUTE EXPECTANCY |
| CAND-072 | Friday Compression | CLOSED — NEGATIVE ABSOLUTE EXPECTANCY |
| CAND-073 | Lunch Reversal | CLOSED — NEGATIVE ABSOLUTE EXPECTANCY |

### Protected Forward Observation

| Candidate | Status |
|---|---|
| CAND-015 | ACTIVE / PROTECTED / UNTOUCHED |

---

## 22. Protected Forward Runtime

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

## 23. Proposed G1 Framework V3 Table

| Dimension | Standalone Alpha | Rare-Event Alpha | State / Condition | Regime / Specialist |
|---|---|---|---|---|
| **Primary Question** | Friction-surviving positive expectancy? | Per-event value justifies waiting? | Incremental info for downstream Alpha? | Strong in-regime economics? |
| **Hard Gate: Mean** | > 5 bps | > 20 bps/event | Δ > 0 bps | > 5 bps (in-regime) |
| **Hard Gate: Median** | > 0 bps | > 0 bps/event | Diagnostic | > 0 bps (in-regime) |
| **Hard Gate: Counterfactual** | Treatment Superior | Treatment Superior | Discriminating | Treatment Superior (in-regime) |
| **Hard Gate: N** | ≥ 10 | ≥ 3 events | — | ≥ 5 (in-regime) |
| **Hard Gate: Executable** | Yes | Yes | N/A (no standalone trade) | Yes |
| **Hard Gate: Regime Def** | N/A | N/A | N/A | Objective, testable, pre-registered |
| **Hard Gate: Target Alpha** | N/A | N/A | Qualified target identified | N/A |
| **Diagnostic: Payoff Concentration** | Yes | Yes | N/A | Yes |
| **Diagnostic: Exclude-Best** | Yes | Yes | N/A | Yes |
| **Diagnostic: Frequency** | Yes | Yes | State occurrence rate | In-regime rate |
| **Diagnostic: Δ** | Yes | Yes | PRIMARY | Yes |
| **Frequency as Gate** | NO | NO | NO | NO |
| **Forward Validation** | Chronological holdout | Event-count accumulation | Interaction study with target | In-regime chronological holdout |

---

## 24. Required Governance Decisions

The following decisions require explicit owner ratification before G1 Framework V3 becomes operational:

### Decision 1: Four-Class Framework
> **RATIFY** the separation of G1 into four artifact-class-specific qualification paths (Standalone Alpha, Rare-Event Alpha, State/Condition, Regime/Specialist).

### Decision 2: Standalone Alpha Mean Net Threshold
> **RATIFY or REJECT** the >5 bps mean net threshold for standalone Alpha promotion.

### Decision 3: Standalone Alpha Median Requirement
> **RATIFY or REJECT** the requirement that median net > 0 bps for standalone Alpha promotion.

### Decision 4: Standalone Alpha N Minimum
> **RATIFY or REJECT** N ≥ 10 as the minimum event count for standalone Alpha.

### Decision 5: Rare-Event Per-Event Threshold
> **RATIFY or REJECT** the >20 bps per-event mean net threshold for rare-event Alpha promotion.

### Decision 6: Rare-Event N Minimum
> **RATIFY or REJECT** N ≥ 3 as the minimum historical event count for rare-event Alpha.

### Decision 7: State Delta Threshold
> **RATIFY, REJECT, or SPECIFY** a minimum incremental delta for State/Condition artifacts.

### Decision 8: Regime In-Regime Threshold
> **RATIFY or REJECT** the >5 bps in-regime mean net threshold for regime specialists.

### Decision 9: Friction Unit Standard
> **RATIFY or REJECT** the requirement that all economic results use bps as the primary unit with explicit instrument documentation.

### Decision 10: Median as Hard Gate
> **RATIFY or REJECT** median net > 0 as a mandatory hard gate for Alpha, Rare-Event, and Regime classes.

### Decision 11: Prospective Application
> **RATIFY** that G1 Framework V3 applies prospectively only. Historical verdicts are not retroactively changed without explicit owner authorization.

---

## 25. Recommended Next Step

After owner ratification of the required decisions:

1. Codify the ratified thresholds into the G1 execution scripts;
2. Update all governance artifacts to reference Framework V3;
3. Begin V25 G0 under the new framework with explicit artifact-class classification;
4. Continue forward observation of CAND-015/024/035 independently.

---

## 26. Integrity

- No candidates were rescued;
- No parameters were changed in existing systems;
- No experiments were run;
- No forward results were inspected;
- No research was executed;
- V24 remains closed;
- All thresholds are classified by evidence quality;
- No value is claimed as ratified without explicit owner decision;
- The proposal is a governance specification, not an implementation.
