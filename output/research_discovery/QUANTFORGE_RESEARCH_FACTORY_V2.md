# QUANTFORGE — RESEARCH FACTORY V2
# ECONOMIC-FIRST DISCOVERY PIPELINE

## 1. Objective

The objective of QuantForge is not to maximize the number of executed experiments or to build an academically complete catalog of market behaviors. The objective is:

> Discover genuine market edge → prove it scientifically → prove it economically → prove it under realistic execution conditions → formulate a deterministic strategy → validate the strategy/bot → eventually deploy a robust trading system.

This operating doctrine (V2) reorganizes the research factory to maximize the probability of finding a robust tradeable edge per unit of research time, engineering effort, and data cost.

## 2. Research Philosophy

QuantForge operates as an **Economic-First / Cost-Aware Research Funnel**. 
We retain our world-class scientific governance, strict provenance, reproducibility, and closure discipline. However, we no longer treat scientific support as a reliable precursor to economic viability.

**Research effort must scale with evidence quality:**
* Low evidence → cheap screen.
* Moderate evidence → moderate validation.
* Strong evidence → expensive production infrastructure.

## 3. Pipeline

The canonical decision table for future candidates is as follows:

| Gate | Phase | Question | Cost | Outcome |
|---|---|---|---|---|
| **G0** | **PHASE 0: Candidate Generation** | Is mechanism novel/plausible? | Very low | reject / proceed |
| **G1** | **PHASE 1: Economic Plausibility** | Does economic headroom exist? | Very low | reject / proceed |
| **G2** | **PHASE 2: Cheap Empirical Pilot** | Does cheap pilot reproduce the behavior? | Low | reject / proceed |
| **G3** | **PHASE 3: Scientific Validation** | Does scientific validation support it? | Medium | close / proceed |
| **G4** | **PHASE 4: Economic Validation** | Does economic validation survive costs? | Medium-high | close / proceed |
| **G5** | **PHASE 5: Production Execution Gate** | Does realistic execution survive? | High | close / proceed |
| **G6** | **PHASE 6: Strategy Construction** | Can it become a deterministic strategy? | High | close / proceed |
| **G7** | **PHASE 7: Bot Validation** | Can bot validation survive OOS/demo/live? | Very high | close / deploy |

## 4. Candidate Generation (PHASE 0)

To qualify as a candidate, a proposal must provide:
* A clear market mechanism;
* A falsifiable hypothesis;
* A plausible causal path;
* A proposed trade expression;
* An intended market/timeframe;
* A structural reason the mechanism could survive execution costs.

We strongly discourage cosmetic indicator combinations, arbitrary threshold searches, repeated variants of already-failed mechanism families, or candidates whose only justification is that a chart pattern "looks good." Every candidate requires a novelty review against closed research lines.

## 5. Economic Plausibility Gate (PHASE 1)

**This is a mandatory gate BEFORE any expensive scientific infrastructure is built.**

The screen must estimate:
* Expected signal frequency;
* Expected turnover;
* Approximate holding period;
* Likely gross return opportunity;
* Likely spread/slippage sensitivity;
* Expected transaction-cost burden;
* Whether the mechanism has enough **ECONOMIC HEADROOM**;
* Whether the signal is structurally compatible with the target execution environment.

**ECONOMIC HEADROOM:** A candidate must demonstrate enough plausible gross edge, turnover profile, holding-period behavior, and economic mechanism to justify the realistic friction expected for the intended instrument/timeframe. This is NOT an arbitrary universal rule (e.g., "kill everything < 15 bp"). The exact threshold remains context-dependent and must be defined by deterministic screening rules rather than retrospective tuning.

The goal is to determine whether it is rational to spend more research/infrastructure resources, NOT to prove profitability.

**Outcomes:**
* **ECONOMICALLY PROMISING:** Candidate proceeds.
* **ECONOMICALLY MARGINAL:** Candidate may proceed only with explicit justification.
* **ECONOMICALLY INSUFFICIENT:** Candidate closes before expensive research infrastructure.
* **INSUFFICIENT DATA:** Candidate remains blocked pending data necessary to assess plausibility.

*Note: Phase 1 must remain outcome-blind. Do not tune thresholds, select favorable markets, change cost assumptions, or drop bad regimes after seeing results.*

### G1 EXECUTABLE-CAPTURE CONTRACT

Every G1 economic-plausibility screen MUST explicitly specify:

**1. Trigger:** What observable event/state causes the signal.
**2. Executable Entry:** The earliest realistic entry point available from the allowed data. Entry price MUST be explicitly defined. The screen MUST NOT assume entry at a future extreme or at an unobservable price.
**3. Post-Entry Measurement Window:** The measurement window begins strictly AFTER executable entry. No price movement occurring before entry may contribute to the reported gross opportunity.
**4. Deterministic Exit:** The exit rule MUST be explicitly frozen before evaluation. Permitted G1 exits may include:
- fixed horizon;
- deterministic stop;
- deterministic target;
- deterministic session boundary;
- deterministic state reversal.
Maximum Favorable Excursion MUST NOT be used as the primary economic endpoint unless MFE itself is the registered scientific/economic object.
**5. Gross Opportunity:** Gross opportunity MUST be calculated from: `executable entry → deterministic exit`, not `signal/reference point → best future price`.
**6. Friction:** Friction must be explicitly stated and applied to the executable transaction.
**7. Turnover/Frequency:** Event count, expected trades, and overlapping exposures must be recorded.
**8. No Free Breakout Capture:** A breakout screen MUST NOT enter at the pre-breakout close and then count the breakout movement as captured. If the strategy requires confirmation, the entry must occur at or after the confirmation event.

### G1 DEFINITION-LOCK RULE

G1 MUST consume the candidate definition exactly as frozen at G0. The G1 implementation MUST NOT: substitute proxy indicators; replace mathematical definitions; change thresholds; add undocumented filters; down-sample event streams; remove observations; alter market scope; alter timing; alter entry/exit logic. Any discrepancy results in: **G1 INVALID** and execution stops.

### NO UNDOCUMENTED PROXIES

A G1 implementation may not substitute an alternative statistical or technical construct for a registered candidate definition. Example: `R-squared` cannot become `Efficiency Ratio`. Any such substitution invalidates the G1 screen.

### NO UNDOCUMENTED DOWNSAMPLING

Explicitly prohibit constructs such as `events[::10]` or any equivalent event thinning unless it is part of the registered object, documented before execution, or justified independently of the result. Otherwise: **G1 INVALID**.

### G1 PRE-RUN STATIC ASSERTION CONTRACT

A mandatory pre-run inspection requires the G1 implementation to assert: candidate definition identity; trigger identity; entry identity; exit identity; holding period; market universe; friction assumption; no proxy substitution; no undocumented down-sampling; no MFE endpoint; no future data dependency. This is a STATIC CONTRACT CHECK. It must occur before G1 data evaluation.

### G1 OUTPUT CONTRACT

Require each G1 output to contain: Candidate, Trigger, Entry price rule, Entry timestamp rule, Exit rule, Measurement window, Gross post-entry return, Friction, Net headroom, Event count, Holding period, Turnover estimate, Data source, Frozen definition identity. This prevents a generic "gross opportunity" number from obscuring how the number was created.

### G1 VALIDITY CHECK

- **VALID:** All executable-capture and definition-lock requirements pass.
- **CONDITIONAL:** Only minor documentation ambiguity exists, with no effect on economic measurement.
- **INVALID:** Any of the following occurs: pre-entry movement included; non-deterministic exit; MFE used as a proxy for tradeable outcome; parameter substitution; undocumented proxy; undocumented down-sampling; market/period alteration; future-data leakage. INVALID means: Do not interpret the result.

### NEW G1 IMPLEMENTATION AUDIT CHECKLIST

Before execution:
- [ ] Trigger frozen
- [ ] Entry executable
- [ ] Entry price frozen
- [ ] Exit deterministic
- [ ] Post-entry window only
- [ ] Friction declared
- [ ] Frequency declared
- [ ] No MFE endpoint substitution
- [ ] No proxy substitution
- [ ] No undocumented down-sampling
- [ ] No hidden filters
- [ ] Candidate definition hash/identity matches
- [ ] Market scope matches
- [ ] Time window matches

Any failed checkbox: **G1 INVALID — STOP**

## 6. Cheap Pilot (PHASE 2)

Before building production tick infrastructure or staging complex environments, require a low-cost pilot where feasible. 

**Permitted inputs:** M1, daily bars, already-existing repository datasets, existing frozen market representations.

The pilot should answer:
* Does the signal actually manifest?
* Is the direction sensible?
* Is the effect sufficiently large?
* Is turnover plausible?
* Is the behavior stable enough to justify scientific validation?

The pilot is not a final scientific result; its role is resource allocation.

## 7. Scientific Validation (PHASE 3)

Only candidates that pass G0, G1, and G2 receive full scientific validation.
QuantForge preserves all existing scientific strengths: pre-registration, frozen protocols, multiple-testing discipline, sample eligibility, outcome neutrality, reproducibility, and independent adjudication. Do not weaken these.

## 8. Economic Validation (PHASE 4)

A scientific SUPPORT result does NOT automatically earn production tick processing. The candidate must still demonstrate economic plausibility. Economic testing must verify a realistic cost model, turnover, execution timing, drawdown, forward/OOS behavior, robustness across relevant regimes, sensitivity to plausible friction, and economic significance.

## 9. Production Execution Gate (PHASE 5)

**Production Parquet/tick/staged execution is an EARNED RESOURCE.**
A candidate only reaches this phase after passing economic plausibility, cheap pilot, scientific validation, and economic validation. 

*Exception: A candidate may bypass an intermediate step only through explicit governance justification recorded before execution.*

**Reuse existing infrastructure:** Existing verified infrastructure (provenance systems, execution identity systems, EventStudyRecorder) is an asset and should be reused. Do not recreate Parquet pipelines, tick readers, or generic bootstrap infrastructure for each candidate unless justified by passing the upstream gates.

## 10. Strategy Construction (PHASE 6)

Only after economic validation should QuantForge begin to define a deterministic entry, deterministic exit, sizing, risk controls, regime behavior, execution assumptions, position management, and failure handling. Do not build the final bot merely because a behavioral hypothesis is supported.

## 11. Bot Validation (PHASE 7)

The eventual progression is:
Scientific edge → Economic edge → Strategy specification → Historical validation → Walk-forward / OOS → Demo execution → Live-small validation → Production bot.

No strategy should reach production merely because a historical backtest is positive.

## 12. Candidate Diversification

Future screening must deliberately rotate across mechanism families to prevent repeating variants of the same "event → direction → fixed horizon" family. Examples of diverse families include:
* Cross-market / relative-value;
* Volatility-state transitions;
* Multi-timescale effects;
* Microstructure / order-flow;
* Liquidity / impact;
* Regime-conditioned behavior;
* Cross-sectional effects;
* Session / auction behavior;
* Event-conditioned mechanisms;
* Other structurally distinct mechanisms.

## 13. Resource Allocation

**Research effort must scale with evidence quality.** This simple concept prevents million-row/tick-scale processing for weak ideas. A new expensive production-data pipeline MUST be justified by a candidate that has passed the upstream gates.

## 14. Stop Rules

Define explicit closure conditions for candidates that:
* Repeatedly fail economic plausibility;
* Produce sub-friction effects;
* Require repeated post-hoc tuning;
* Depend on unrealistic execution;
* Cannot survive OOS;
* Require increasingly complex exceptions;
* Consume disproportionate engineering time relative to evidence.

## 15. Governance

The research factory remains firmly governed by the strict rules of provenance, identity, freezing, and closure. Reverting to outcome-driven engineering, undocumented experimentation, or optimization without preregistration is prohibited.

## 16. Success Metrics

The goal is to maximize the probability of finding a robust tradeable edge per unit of research time, engineering effort, and data cost. Success metrics include:
* Candidate-to-economic-test conversion rate;
* Proportion of candidates killed cheaply;
* Research cost per adjudicated candidate;
* Number of distinct mechanism families screened;
* Fraction reaching realistic execution;
* Number of economically supported candidates;
* Number reaching strategy specification.

## 17. Closed-Line Firewall

Future research documents must explicitly prevent the rescue of any closed line. Specifically:
* NO H01 rescue;
* NO ORD/XAGUSD rescue;
* NO DISC-024 rescue;
* NO DISC-025 alternate translation rescue;
* NO TSMOM rescue;
* NO Mean Reversion rescue.

A new candidate must be genuinely distinct or have a new mechanism justified before reopening anything historically related.

## 18. Researcher Checklist

Before authorizing an experiment:
- [ ] Is the candidate novel and diversified from recently tested mechanism families?
- [ ] Has the candidate passed Phase 1 (Economic Plausibility Gate)?
- [ ] Has the candidate passed Phase 2 (Cheap Empirical Pilot)?
- [ ] Has the scientific protocol been pre-registered?
- [ ] Are we reusing existing infrastructure where possible?
