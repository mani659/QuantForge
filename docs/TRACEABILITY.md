# QuantForge Traceability

> **Note:** The Behavioral Observation Engine (BOE) and the pipeline described below represent the canonical architecture. Legacy modules remain as historical artifacts that contributed to the underlying research.
## Behavioral Observation Engine v1.0

**Implementation status:** Contract foundation complete; no detector implementation exists.

| Contract component | Responsibility | Dependencies | Prohibited content |
|---|---|---|---|
| `ObservationEnvironment` | Immutable detector input context | Standard library only | Indicators, scores, thresholds, trading decisions |
| `BehaviorDetectorContract` | Abstract detector boundary | Environment and observation contracts | Detection algorithm or broker code |
| `BehaviorObservation` | Immutable observed-behavior record | Standard library only | Signals, direction, risk, orders, internal calculations |
| `detector_errors` | Deterministic contract failures | Standard library only | Generic exception handling |

### Dependency graph

`ObservationEnvironment` → `BehaviorDetectorContract` → `BehaviorObservation`

### Public-contract rule

The public contract contains identity, provenance, market context, behavior
classification, and semantic versions. Candidate lifecycle, derived measures,
thresholds, indicators, scores, and detector state are internal or belong to a
future Candidate Ledger.

## Candidate Manager v1.0

**Implementation status:** Frozen state-machine foundation complete; no behavioral
validation, persistence decision, trade signal, risk calculation, or order action exists.

| Component | Responsibility | Dependencies | Prohibited content |
|---|---|---|---|
| `CandidateState` | Closed lifecycle vocabulary | Standard library only | Behavioral metrics or trade state |
| `CandidateEvent` | Immutable replayable state transition | Candidate state | Detector calculations or event payload metrics |
| `Candidate` | Immutable behavioral-hypothesis snapshot | BehaviorObservation, CandidateEvent | Risk, orders, indicators, execution |
| `CandidateManager` | Enforce permitted transitions and append events | Candidate contracts | Detector, validator, broker, or trading logic |

### Dependency graph

`BehaviorObservation` → `CandidateManager` → `Candidate` + `CandidateEvent`

The manager receives timestamps from callers; it never reads a clock or generates
identifiers. This preserves deterministic replay from the future Candidate Ledger.

## Behavior Validator Framework v1.0

**Implementation status:** Contract and pipeline foundation complete; no validation
algorithm or hypothesis decision is implemented.

| Component | Responsibility | Dependencies | Prohibited content |
|---|---|---|---|
| `ValidationContext` | Immutable opaque external validation context | Standard library only | Detector calculations or interpreted market metrics |
| `BehaviorValidatorContract` | Pure validator boundary | Candidate, context, result contracts | Mutation, trading, or hypothesis decisions |
| `ValidationResult` | Immutable abstract validator evidence | Standard library only | ATR, Z-score, thresholds, distances, durations, indicators |
| `ValidatorPipeline` | Sequential result collection | Validator contracts | Parallelism, short-circuiting, aggregation, decisions |

### Dependency graph

`Candidate` + `ValidationContext` → `BehaviorValidatorContract` →
`ValidationResult` → future Hypothesis Evaluation

Future validators are insertion points only: RecoilValidator, PersistenceValidator,
and ContextValidator can implement the contract independently.

## Hypothesis Engine v1.0

**Implementation status:** Evidence interpretation foundation complete; no research
policy, detector logic, trading decision, risk, or execution action is implemented.

| Component | Responsibility | Dependencies | Prohibited content |
|---|---|---|---|
| `Hypothesis` | Immutable candidate-derived hypothesis identity | Candidate identity | Detector or validator internals |
| `DecisionPolicyContract` | Interchangeable evidence interpretation boundary | Hypothesis, ValidationResult | Candidate mutation or trading logic |
| `DeterministicDecisionPolicy` | Baseline all-results-pass policy | Abstract validator results | Weighting, research scoring, calculations |
| `HypothesisResult` | Immutable abstract hypothesis outcome | Standard library only | Thresholds, metrics, orders, risk, execution |
| `HypothesisEngine` | Policy orchestration and result contract enforcement | Candidate, result tuple, policy | Detector/validator implementation knowledge |

### Dependency graph

`Candidate` + `tuple[ValidationResult]` → `HypothesisEngine` →
`DecisionPolicyContract` → `HypothesisResult`

The engine derives identity and timestamp deterministically from the immutable
candidate. Future policies can be inserted without modifying validators.

## Recoil Validator v1.0

| Research source | Derived contract behavior | Implementation artifact | Verification |
|---|---|---|---|
| DISC-004: strong trades exhibited immediate recoil after behavioral displacement | Determine whether recoil was observed, without deciding whether to trade | `boe.validators.RecoilValidator` | `tests.test_recoil_validator` |
| DISC-019: weak trades frequently failed to recoil | Publish only abstract positive/negative recoil evidence | `ValidationResult.evidence` | `RECOIL_OBSERVED` / `RECOIL_NOT_OBSERVED` assertions |

The recoil threshold is externalized in `config/recoil_rules.json` and loaded
into immutable `RecoilConfig`. The public evidence contract contains no numeric
threshold, recoil distance, or detector implementation detail.

## Interchangeable Decision Policies v1.0

| Architectural rule | Contract behavior | Implementation artifact | Verification |
|---|---|---|---|
| Rule #13: evidence modules observe independently | Evidence sufficiency is interpreted after validation, not inside a validator | `boe.hypothesis.policies.DecisionPolicyContract` | `tests.test_decision_policies` |
| Backward compatibility | Default policy preserves prior all-results-pass outcome | `StrictPolicy`, `DefaultPolicy`, legacy `DeterministicDecisionPolicy` alias | strict and legacy policy equivalence assertions |
| Future research insertion | Named policies are selected deterministically with no dynamic loading | `PolicyFactory` | factory and invalid selection assertions |

BalancedPolicy and ExploratoryPolicy intentionally remain strict-equivalent
placeholders. They reserve the policy boundary without introducing weighting or
probability research before it is independently validated.

## Experiment Ledger v1.0

| Architectural rule | Contract behavior | Implementation artifact | Verification |
|---|---|---|---|
| Rule #15: long-term replay | Immutable evidence, policy version, and SHA-256 parameter provenance are recorded together | `ledger.ExperimentRecord` | replay compatibility assertions |
| Rule #8: no implementation leakage | Ledger permits only public ValidationResult/HypothesisResult contracts and abstract provenance | `ExperimentRecord.__post_init__` | schema validation assertions |
| Persistence independence | Repository operations are specified behind an abstract contract | `LedgerContract`, `LedgerRepository` | append, lookup, ordering, and duplicate tests |

The Experiment Ledger records behavioral experiments, not trade, broker, or
execution logs. Execution and outcome fields are optional factual placeholders;
they do not alter its role as the scientific source of truth.

## Architecture Freeze and Future Placement

| Research timeline concern | Frozen architectural placement | Current module or future milestone |
|---|---|---|
| Supplied market context | Market Reality / `EnvironmentSnapshot` | Sprint 2.1: Environment Snapshot and Repository |
| Behavioral event over time | Behavioral Reality / observation and timeline ontology | Existing BehaviorObservation; Sprints 2.1–2.3: frames, timelines, BOW |
| Recoil, persistence, context, and environment evidence | Scientific Reality / Behavioral Evidence Modules | Recoil Validator exists; Phase 3 observers remain planned |
| Evidence sufficiency | Scientific Reality / Decision Policy | Existing Hypothesis Engine and policies |
| Replayable experimental provenance | Scientific Reality / Experiment Ledger | Existing Experiment Ledger; Sprint 2.4 replay tools planned |
| Capital allocation and order action | Operational Reality / Risk Policy and Execution | Existing risk/execution foundations; later evolution phases |

Rules #16 and #17 connect the research timeline to durable observation facts and
downward-only layer flow. Future modules must enter the layer named here rather
than bypassing the observation, evidence, or policy boundaries.

## Temporal Ontology — Sprint 2.1

| Research-to-architecture need | Temporal contract | Current status |
|---|---|---|
| Immutable supplied market reality | `EnvironmentSnapshot` | Implemented |
| Ordered behavioral facts over an observation period | `BehaviorFrame` → `ActiveObservationTimeline` | Implemented builder boundary |
| Durable, replay-ready temporal behavior | `FrozenBehaviorTimeline` | Implemented immutable aggregate |
| Persistent temporal source of truth | `TimelineRepositoryContract` | Contract only; repository is a future milestone |

The timeline is frozen before future behavioral evidence modules consume it.
This preserves Rule #8, Rule #16, and Rule #17: implementation details do not
cross boundaries, observations require persistence architecture, and information
flows downward through the four realities.

## Observation Policy — Sprint 2.2

**Implementation status:** Observation lifecycle contract implemented. No Behavior
Observation Window, observer, replay, evidence, or decision behavior exists in
this component.

| Component | Responsibility | Dependencies | Prohibited content |
|---|---|---|---|
| `ObservationPolicyContract` | Abstract observation lifecycle boundary | `ObservationConfig`, `ObservationDecision` | Behavioral interpretation, evidence evaluation, risk, execution |
| `DefaultObservationPolicy` | Deterministic frame-count and duration termination | `ObservationPolicyContract`, `ObservationConfig` | Market intelligence, heuristics, adaptive logic |
| `ObservationConfig` | Immutable external configuration | Standard library JSON | Hardcoded business rules, detector parameters |
| `ObservationDecision` | Immutable lifecycle decision and termination reason | Standard library only | Indicators, thresholds, evidence labels, trade instructions |
| `ObservationPolicyFactory` | Deterministic named policy construction | Explicit supported names | Reflection, plugins, registry loading |

### Dependency graph

`ObservationConfig` (external JSON) → `ObservationPolicyContract` →
`DefaultObservationPolicy` → `ObservationDecision`

### Architectural placement

| Research-to-architecture need | Observation Policy contract | Current status |
|---|---|---|
| Observation lifecycle control | `ObservationPolicyContract` → `ObservationDecision` | Implemented abstract contract and default policy |
| Pluggable policy boundary | Future policies implement `ObservationPolicyContract` | Contract ready; BOW will consume the contract only |
| External configuration | `ObservationConfig.from_json()` | Implemented immutable JSON loading |
| Deterministic termination | `DefaultObservationPolicy.evaluate()` | Frame count and duration limits with deterministic priority |

The Observation Policy is strictly independent from Decision Policy (evidence
interpretation) and Risk Policy (capital allocation). Future adaptive policies
(Market DNA–driven) can implement `ObservationPolicyContract` without modifying
the BOW or any other component.

## Infrastructure Completion — Sprint 2.2.5

Rule #16 is now fully implemented through persistent repositories.

### Research Mapping

Research
↓
Temporal Observation
↓
Behavior Observation Window
↓
FrozenBehaviorTimeline
↓
Evidence Modules
↓
Hypothesis Engine
### Replay Engine Mapping (Sprint 2.4)

Rule #18 compliance verified: 100% deterministic, no singletons, no cache drift.

Research
↓
Replay architecture
↓
Replay contracts
↓
Replay implementation
↓
Replay tests
↓
Replay documentation

### Official Scientific Pipeline Mapping

Research
↓
Temporal Observation
↓
Environment Snapshot
↓
Timeline
↓
Replay
↓
Evidence
↓
Hypothesis
↓
Decision

This officially records the scientific pipeline.

### Replay Engine Canonical Flow

Research
↓
Behavior Observation Engine
↓
Temporal Ontology
↓
Replay Engine
↓
Scientific Memory
↓
Future Evidence Modules
↓
Future Market DNA

Replay Engine is now the canonical replay interface for all future research modules.

### Scientific Evidence Mapping (Sprint 3.1)

Research
↓
Independent Observer Rule (Rule #23)
↓
Observer Contract
↓
Immutable Evidence
↓
Evidence Package

This ensures Observers act perfectly as isolated scientific instruments.

### Scientific Observation Layer Mapping (Phase 3A)

Research
↓
Replay Engine
↓
Five Scientific Observers
↓
Evidence

*(Interpretation layer is explicitly excluded at this stage.)*


=========================================================
ARCHITECTURAL EVOLUTION: SCIENTIFIC OPERATING SYSTEM
=========================================================

Traceability update for behavioural hypotheses flow:

Research
↓
Observation
↓
Evidence
↓
Behaviour Profile
↓
Interpretation
↓
Experiment Ledger
↓
Cross-Market Validation
↓
Strategy Intelligence
↓
Deployment


=========================================================
SPRINT 3.8 FREEZE: BEHAVIOUR PROFILE ENGINE
=========================================================

Updated Scientific Pipeline Flow:

Research
↓
Observation
↓
Evidence
↓
Behaviour Profile
↓
Interpretation (future)
↓
Decision (future)
↓
Risk (future)
↓
Execution (future)


=========================================================
SPRINT 3.8 PIPELINE UPDATE
=========================================================

Updated Scientific Pipeline:

Market
↓
Observation
↓
Evidence
↓
Behaviour Profile
↓
Interpretation (future)
↓
Interpretation Registry (future)
↓
Decision Policy (future)
↓
Risk (future)
↓
Execution (future)

*(Note: Interpretation Registry / Interpretation Model is a newly approved future sprint between Behaviour Profile and Decision Policy.)*


=========================================================
SPRINT 3.9 PIPELINE UPDATE
=========================================================

Updated Scientific Pipeline:

Market Reality
↓
Observation
↓
Behaviour Timeline
↓
Evidence
↓
Behaviour Profile
↓
Interpretation Registry
↓
Interpretation Model
↓
Interpretation
↓
Decision Policy (future)
↓
Decision Registry (future)
↓
Risk Policy (future)
↓
Execution (future)

*(Note: The Interpretation Registry is the first pluggable scientific reasoning layer, serving as the bridge between the descriptive profile and the upcoming decision logic.)*


=========================================================
SPRINT 3.10 PIPELINE UPDATE
=========================================================

Updated Scientific Pipeline:

Market
↓
Observation
↓
Evidence
↓
Behaviour Profile
↓
Interpretation Registry
↓
Interpretation
↓
Decision Policy
↓
Decision Registry (future)
↓
Risk (future)
↓
Execution (future)


=========================================================
SPRINT 3.11 PIPELINE UPDATE
=========================================================

Updated Scientific Pipeline:

Market
↓
Observation
↓
Evidence
↓
Behaviour Profile
↓
Interpretation Registry
↓
Interpretation
↓
Decision Registry
↓
Decision Policy
↓
Decision
↓
Risk (future)
↓
Execution (future)


=========================================================
PHASE 3 FREEZE — SCIENTIFIC PIPELINE & VALIDATION
=========================================================

**FROZEN PIPELINE:**
Market
↓
Observation
↓
Evidence
↓
Behaviour Profile
↓
Interpretation Registry
↓
Interpretation Model
↓
Interpretation
↓
Decision Registry
↓
Decision Policy
↓
Decision
↓
Risk (future)
↓
Execution (future)

**Research Validation Milestone:**
The QuantForge architecture directly supports iterative cross-market behavioural research. Validated behavioural hypotheses seamlessly plug into the pipeline by becoming new `Interpretation Models` and `Decision Policies`. This critical validation loop is mathematically quarantined and fully completed *before* any risk or execution logic is introduced to the system.


=========================================================
SPRINT 4.1 PIPELINE UPDATE
=========================================================

Updated Scientific & Risk Pipeline:

Market
↓
Observation
↓
Evidence
↓
Behaviour Profile
↓
Interpretation Registry
↓
Interpretation
↓
Decision Registry
↓
Decision
↓
Risk Model
↓
Risk Registry (future)
↓
Risk Policy (future)
↓
Position Sizing (future)
↓
Execution (future)


=========================================================
SPRINT 4.2 PIPELINE UPDATE
=========================================================

Updated Scientific & Risk Pipeline:

Market
↓
Observation
↓
Evidence
↓
Behaviour Profile
↓
Interpretation Registry
↓
Interpretation
↓
Decision Registry
↓
Decision
↓
RiskModel
↓
RiskPolicy
↓
RiskAssessment (future)
↓
PositionSizer (future)
↓
Execution (future)


=========================================================
SPRINT 4.3 PIPELINE UPDATE
=========================================================

Updated Scientific & Risk Pipeline:

Market
↓
Observation
↓
Evidence
↓
Behaviour Profile
↓
Interpretation Registry
↓
Interpretation
↓
Decision Registry
↓
Decision
↓
RiskModel
↓
RiskPolicyRegistry
↓
RiskPolicy
↓
RiskAssessment (future)
↓
PositionSizer (future)
↓
Execution (future)


=========================================================
SPRINT 4.4 PIPELINE UPDATE
=========================================================

Updated Scientific & Risk Pipeline:

Market
↓
Observation
↓
Evidence
↓
Behaviour Profile
↓
Interpretation Registry
↓
Interpretation
↓
Decision Registry
↓
Decision
↓
RiskModel
↓
RiskPolicyRegistry
↓
RiskPolicy
↓
RiskAssessment
↓
PositionSizer (future)
↓
Execution (future)


=========================================================
SPRINT 4.5 PIPELINE UPDATE
=========================================================

Updated Scientific & Risk Pipeline:

Market
↓
Observation
↓
Evidence
↓
Behaviour Profile
↓
Interpretation Registry
↓
Interpretation
↓
Decision Registry
↓
Decision
↓
RiskModel
↓
RiskPolicyRegistry
↓
RiskPolicy
↓
RiskAssessment
↓
PositionSizer
↓
PositionPlan (future)
↓
Execution (future)


=========================================================
SPRINT 4.6 PIPELINE UPDATE
=========================================================

Updated Scientific & Risk Pipeline:

Market
↓
Observation
↓
Evidence
↓
Behaviour Profile
↓
Interpretation Registry
↓
Interpretation
↓
Decision Registry
↓
Decision
↓
RiskModel
↓
RiskPolicyRegistry
↓
RiskPolicy
↓
RiskAssessment
↓
PositionSizer
↓
PositionSpecification
↓
Execution (future)


=========================================================
PHASE 4 FREEZE: PIPELINE
=========================================================

Updated Scientific & Risk Pipeline:

Market
↓
Observation
↓
Evidence
↓
Behaviour Profile
↓
Interpretation Registry
↓
Interpretation
↓
Decision Registry
↓
Decision
↓
Risk (Model -> Policy -> Assessment -> Sizer)
↓
Position Specification
↓
Execution (Phase 5)


=========================================================
SPRINT 5.1 PIPELINE UPDATE
=========================================================

Execution Pipeline:

PositionSpecification
↓
ExecutionEngine
↓
ExecutionResult (future)


=========================================================
SPRINT 5.2 PIPELINE UPDATE
=========================================================

Execution Pipeline:

PositionSpecification
↓
ExecutionEngine
↓
BrokerAdapterContract
↓
ExecutionResult (future)


=========================================================
SPRINT 5.3 PIPELINE UPDATE
=========================================================

Execution Pipeline:

PositionSpecification
↓
ExecutionEngine
↓
Broker Adapter Contract
↓
ExecutionResult


=========================================================
SPRINT 5.4 PIPELINE UPDATE
=========================================================

Execution Pipeline:

PositionSpecification
↓
ExecutionEngine
↓
BrokerAdapterContract
↓
ExecutionResult


=========================================================
SPRINT 5.5 PIPELINE UPDATE
=========================================================

Execution Pipeline:

ExecutionEngine
↓
MT5Adapter (future)
↓
MT5Transport
↓
MetaTrader5 SDK


=========================================================
SPRINT 5.6 PIPELINE UPDATE
=========================================================

Execution Pipeline:

ExecutionEngine
↓
MT5Adapter
↓
MT5Transport
↓
MetaTrader5 SDK


=========================================================
SPRINT 5.7 PIPELINE UPDATE
=========================================================

Execution Pipeline (Simulation Branch):

ExecutionEngine
↓
PythonSimulationAdapter
↓
ExecutionResult


=========================================================
SPRINT 5.8 PIPELINE UPDATE
=========================================================

Execution Pipeline (Paper Trading Branch):

ExecutionEngine
↓
PaperTradingAdapter
↓
ExecutionResult


=========================================================
PHASE 5 COMPLETE RUNTIME PIPELINE
=========================================================

Market
↓
Observation
↓
Evidence
↓
Behaviour Profile
↓
Interpretation
↓
Decision
↓
Risk
↓
PositionSpecification
↓
ExecutionEngine
↓
BrokerAdapter
↓
ExecutionResult


=========================================================
SCIENTIFIC VALIDATION LIFECYCLE
=========================================================

Hypothesis
↓
Experiment
↓
Validation
↓
Approved Interpretation Model


=========================================================
SCIENTIFIC VALIDATION LIFECYCLE (Updated)
=========================================================

Hypothesis
↓
Experiment
↓
Validation
↓
Approved Interpretation Model


=========================================================
SCIENTIFIC VALIDATION LIFECYCLE (Finalized)
=========================================================

Hypothesis
↓
Experiment
↓
Validation
↓
Approved Interpretation Model


=========================================================
COMPLETED SCIENTIFIC VALIDATION LIFECYCLE
=========================================================

Hypothesis
↓
Experiment
↓
Validation

*(This completes the macro-lifecycle of scientific testing, enabling downstream consumption by the Interpretation phase).*


=========================================================
END-TO-END RESEARCH LIFECYCLE
=========================================================

Research
↓
Hypothesis
↓
Experiment
↓
Validation
↓
Approved Interpretation Model
↓
QuantForge Runtime

=========================================================
STRATEGY TRACEABILITY
=========================================================

Validation
↓
Strategy
↓
QuantForge Runtime

=========================================================
CANONICAL DEPLOYMENT PIPELINE
=========================================================

DeploymentBootstrap
↓
MarketDataAdapter
↓
PaperTradingRunner
↓
DeploymentOrchestrator
↓
Scientific BOE Pipeline
↓
PositionSpecification
↓
Simulation Execution

=========================================================
PHASE 8 RESEARCH LIFECYCLE (TRACEABILITY)
=========================================================

The canonical Phase 8 lifecycle of a behavioural edge in QuantForge is
permanently frozen as:

Research Candidate
↓
Scientific Validation
↓
Validated Behaviour
↓
Strategy Manifest
↓
Deployment Runtime
↓
Execution
↓
Deployment Evidence Capture
↓
OutcomeReader
↓
END OF SOFTWARE
↓
Human Research Review
(planning-era label for the closing stage: "Research Feedback")

- **Research Candidate:** The formal, immutable declaration of a behavioural
hypothesis and its required observational components.
- **Scientific Validation:** The deterministic replay of the Research Candidate
against historical market data to produce immutable Evidence and Validation
outcomes.
- **Validated Behaviour:** A validated scientific truth that has met the statistical and
reproducibility criteria of the Research Protocol.
- **Strategy Manifest:** The deterministic wiring configuration binding the
Validated Behaviour to the frozen BOE registries.
- **Deployment Runtime:** The frozen Phase 7 operational shell that executes the
Strategy Manifest.
- **Execution:** The physical or simulated market interaction resulting in an
immutable outcome.
- **Deployment Evidence Capture (planning-era label: "Research Feedback"):** The capture of execution outcomes and market
observations as new immutable scientific evidence appended to the permanent
Experiment Ledger as new scientific evidence. The automated system terminates at
the read-only `OutcomeReader` service; Human Research Review is outside
QuantForge software.

Phase 8.1 completes the Research Candidate and Strategy Manifest contracts,
formalizing the boundary between validated research and the frozen Deployment
Runtime. The repository is constitutionally synchronized. Phase 8.2 may begin
without architectural risk.

=========================================================
PHASE 8.1 LINEAGE (SPRINT 8.1)
=========================================================

Research Idea
↓
ResearchCandidate (Phase 8.1)
↓
Scientific Validation
↓
Validated Behaviour
↓
Strategy Manifest (Phase 8.1)
↓
Deployment Runtime
↓
Execution
↓
Research Feedback

> Historical terminology note: "Research Feedback" is the planning-era label for the closing lifecycle stage. The frozen name is **Deployment Evidence Capture**, terminating at the read-only `OutcomeReader` service (see `PHASE8_PERMANENT_FREEZE.md`).

**Phase 8.1 Responsibility:** Establish deterministic frozen contracts for
Research Candidate and Strategy Manifest without modifying any frozen scientific
domain or BOE layer.

**Next Phase:** Phase 8.2 (Deployment Evidence Capture; planning-era label "Research Feedback Loop") will industrialize the research lifecycle feedback stage.

**Freeze Status:** Phase 8.1 permanently frozen. No changes permitted without formal constitutional review.

## Phase 8.1 — Research Candidate & Strategy Manifest v1.0

**Implementation status:** Complete; immutable lifecycle objects and
deterministic builder delivered with full regression coverage (82 tests).

| Component | Responsibility | Dependencies | Prohibited content |
|---|---|---|---|
| `ResearchCandidate` | Immutable behavioural hypothesis declaration | Standard library only | Runtime state, execution, results, statistics, broker info |
| `Provenance` | Immutable scientific reproducibility chain | Standard library only | Business logic, deployment decisions, runtime state |
| `StrategyManifest` | Immutable deployment wiring configuration (references only) | Provenance | Instantiated classes, business logic, execution state |
| `StrategyManifestBuilder` | Deterministic transition: ResearchCandidate → StrategyManifest | ResearchCandidate, Provenance, StrategyManifest | Scientific decisions, evidence interpretation, validation logic |
| `research_errors` | Deterministic construction failures | Standard library only | Generic exception handling |

### Dependency graph

`ResearchCandidate` → `StrategyManifestBuilder` → `Provenance` + `StrategyManifest`

### Domain boundaries

- **ResearchCandidate** is a *scientific* object. It declares what behaviour is
  hypothesized. It does not know how to test, deploy, or execute.
- **StrategyManifest** is an *operational* object. It declares how a validated
  behaviour should be wired for deployment. It contains only identifiers.
- **Provenance** is a *scientific reproducibility* object. It answers:
  "Where did this strategy come from?"
- **StrategyManifestBuilder** is a *structural assembly* tool. It validates
  completeness and produces immutable outputs. It never creates scientific
  decisions.

### Traceability to Phase 8 Constitutional Lifecycle

| Phase 8 Lifecycle Stage | Sprint 8.1 Implementation |
|---|---|
| Research Candidate | `ResearchCandidate` frozen dataclass |
| Scientific Validation | Referenced via `Provenance.validation_id` (not implemented in 8.1) |
| Validated Behaviour | Represented by the validated references accepted by the builder |
| Strategy Manifest | `StrategyManifest` frozen dataclass |
| Deployment Runtime | Consumer (frozen Phase 7 — not modified) |

=========================================================
PHASE 8.2 LINEAGE (SPRINT 8.2)
=========================================================

Research Idea
↓
ResearchCandidate (Phase 8.1)
↓
Strategy Manifest (Phase 8.1)
↓
Deployment Runtime
↓
Execution
↓
ExecutionResult
↓
OutcomeAppender (Phase 8.2)
↓
DeploymentOutcome (Phase 8.2)
↓
ExperimentRecorder (append)

**Phase 8.2 Responsibility:** Capture immutable deployment evidence.
`OutcomeAppender` transforms a frozen `ExecutionResult` (and the originating
`StrategyManifest` + `Provenance`) into an immutable `DeploymentOutcome` and
appends it to the existing `ExperimentRecorder`. This closes the capture side of
the research feedback loop without modifying any frozen scientific domain.

**Freeze Status:** Phase 8.2 permanently frozen. No changes permitted without formal constitutional review.

=========================================================
PHASE 8.3 LINEAGE (SPRINT 8.3)
=========================================================

Research Idea
↓
ResearchCandidate (Phase 8.1)
↓
Strategy Manifest (Phase 8.1)
↓
Deployment Runtime
↓
Execution
↓
ExecutionResult
↓
OutcomeAppender (Phase 8.2)
↓
DeploymentOutcome (Phase 8.2)
↓
ExperimentRecorder (append)
↓
OutcomeReader (Phase 8.3)
↓
HUMAN RESEARCH REVIEW (outside QuantForge software)

**Phase 8.3 Responsibility:** Sprint 8.3 consumes deployment evidence.
`OutcomeReader` is a stateless, deterministic, read-only application service that
locates, retrieves, deserializes, validates, and returns immutable
`DeploymentOutcome` artifacts persisted by `ExperimentRecorder`.

**Boundary:** The automated system terminates at `OutcomeReader`. Human Research
Review exists completely outside QuantForge software and is not represented as a
software service.

**Freeze Status:** Phase 8.3 permanently frozen. No changes permitted without formal constitutional review.

