# QuantForge Interface Specification
Version: 1.0
Status: Frozen
Last Updated: 2026-07-16

===========================================================
PURPOSE
===========================================================

This document defines the official data contracts between
QuantForge modules.

Every module must consume and produce data according to
these interfaces.

Interfaces are versioned.

Changing an interface requires a Major Version update.

===========================================================
SYSTEM PIPELINE
===========================================================

Tick Data

↓

Tick Validator

↓

Validated Tick Data

↓

Tick → M1 Converter

↓

Validated M1 Data

↓

Market DNA Profiler

↓

DNA Profile

↓

Adaptive Strategy Engine

↓

Adaptive Strategy

↓

Signal Generator

↓

Signal

↓

Risk Engine

↓

TradePlan

↓

Execution Engine

↓

Trade Result

↓

Experiment Recorder

↓

Research Database

===========================================================
INTERFACE 1
VALIDATED TICK DATA
===========================================================

Producer

Tick Validator

Consumer

Tick → M1 Converter

Contract

Validated CSV

Required Fields

timestamp

bid

ask

spread

Validation

No invalid timestamps

No Ask < Bid

No negative prices

===========================================================
INTERFACE 2
M1 CANDLE DATA
===========================================================

Producer

Tick → M1 Converter

Consumer

DNA Profiler

Contract

CSV

Required Fields

datetime

open

high

low

close

volume

===========================================================
INTERFACE 3
DNA PROFILE
===========================================================

Producer

Market DNA Profiler

Consumer

Adaptive Strategy

Contract

JSON

Contains

Trend Statistics

ATR

Expansion

Pullback

Volatility

Volume

Trading Hours

===========================================================
INTERFACE 4
ADAPTIVE STRATEGY
===========================================================

Producer

Adaptive Strategy Engine

Consumer

Signal Generator

Contract

JSON

Structure

{
    "strategy_class":"",
    "holding_style":"",
    "risk_profile":"",
    "confidence":0.00,
    "reason":[]
}

Purpose

Select the trading methodology.

===========================================================
INTERFACE 5
SIGNAL
===========================================================

Producer

Signal Generator

Consumer

Risk Engine

Contract

JSON

Structure

{
    "signal":"BUY",
    "signal_strength":0.00,
    "confidence":0.00,
    "reason":[]
}

Possible Values

BUY

SELL

NO_TRADE

Purpose

Represents a trading opportunity.

===========================================================
INTERFACE 6
TRADEPLAN
===========================================================
Producer

Risk Engine

Consumer

Execution Engine

Contract

TradePlan v1.0

Reference

TRADEPLAN.md (Historical Reference - Superseded)

Purpose

Complete approved trading decision.


Risk

Producer

Risk Engine

Consumer

Execution Engine

Contract

TradePlan v1.0

Reference

TRADEPLAN.md (Historical Reference - Superseded)

Purpose

Complete approved trading decision.

Contains

Strategy

Signal

Execution Parameters

Validation

Metadata

===========================================================
INTERFACE 7
TRADE RESULT
===========================================================

MT5Connection

↓

ConnectionStatus

Producer

MT5 Connection Manager

Consumer

MT5 Adapter

ConnectionStatus contains terminal path, broker, verified account, company,
currency, balance, equity, trade permission, terminal build, and adapter version.

TradeOrder

↓

MT5 Adapter

↓

TradeResult

Producer

MT5 Adapter

Consumer

Experiment Recorder

TradeResult v1.0

{
    "schema_version":"1.0",
    "trade_id":"",
    "order_id":"",
    "timestamp":"ISO8601",
    "instrument":"EURUSD",
    "direction":"BUY",
    "status":"FILLED",
    "requested_volume":0.10,
    "filled_volume":0.10,
    "entry_price":0.0,
    "stop_loss":null,
    "take_profit":null,
    "commission":0.0,
    "swap":0.0,
    "comment":"",
    "broker":"MetaTrader5",
    "metadata":{"adapter_version":"1.0.0"}
}

Producer

Execution Engine

Consumer

Experiment Recorder

Contract

JSON

Contains

Entry Price

Exit Price

Lot Size

PnL

Commission

Swap

Duration

Exit Reason

Trade Status

===========================================================
INTERFACE 8
EXPERIMENT RECORD
===========================================================

Producer

Experiment Recorder

Consumer

Feature Matrix Builder

Contract

Run Folder

run.json

metadata.json

dna_snapshot.json

robustness.json

trades.csv

equity.csv

manifest.json

===========================================================
INTERFACE RULES
===========================================================

Every interface

Must be deterministic

Must be versioned

Must be serializable

Must be testable

Must be documented

===========================================================
BACKWARD COMPATIBILITY
===========================================================

Minor Version

May add optional fields.

Major Version

May change required fields.

Removing required fields requires

Major Version update.

===========================================================
MODULE RESPONSIBILITY
===========================================================

Each module owns only its output.

Examples

Adaptive Strategy

Owns

Adaptive Strategy JSON

Signal Generator

Owns

Signal JSON

Risk Engine

Owns

TradePlan

Execution Engine

Owns

Trade Result

Experiment Recorder

Owns

Experiment Record

No module may modify another module's output.

===========================================================
VALIDATION
===========================================================

Every interface should have

Schema Validation

Regression Test

Compatibility Test

Any interface change must update

Tests

Documentation

Version

===========================================================
DESIGN PRINCIPLE
===========================================================

Modules communicate only through
well-defined interfaces.

No hidden state.

No implicit assumptions.

No undocumented fields.

===========================================================
END OF INTERFACES
===========================================================

===========================================================
BOE INTERFACE v1.0
===========================================================

Producer

BehaviorDetectorContract implementation

Consumer

Future Candidate Ledger / behavioral workflow

Dependency graph

ObservationEnvironment → BehaviorDetectorContract → BehaviorObservation

ObservationEnvironment supplies stable instrument, timeframe, observation time,
opaque raw market snapshot, and identity context. BehaviorObservation publishes
only observation identity, behavior type, context identity, detector provenance,
and semantic versions. It is not a trade signal.

===========================================================
CANDIDATE LIFECYCLE INTERFACE v1.0
===========================================================

Dependency graph

BehaviorObservation → CandidateManager → Candidate + CandidateEvent

Candidate contains observation provenance, frozen lifecycle state, timestamps,
revision, and immutable event history. CandidateEvent contains only event
identity, candidate identity, previous/new state, timestamp, and event type.
No detector metrics, candidate validation evidence, order information, or risk
information crosses this boundary.

===========================================================
VALIDATION INTERFACE v1.0
===========================================================

BehaviorValidatorContract consumes immutable Candidate and ValidationContext and
returns immutable ValidationResult. ValidationContext carries opaque external
reference data only. ValidationResult carries validator provenance, pass/fail,
abstract confidence, abstract evidence labels, and timestamp only.

Future insertion points include RecoilValidator, PersistenceValidator, and
ContextValidator. Each can be added to ValidatorPipeline without modifying the
pipeline, Candidate, BehaviorObservation, or existing validators.

===========================================================
HYPOTHESIS INTERPRETATION INTERFACE v1.0
===========================================================

HypothesisEngine consumes immutable Candidate and tuple[ValidationResult] and
returns immutable HypothesisResult. DecisionPolicyContract is the only evidence
interpretation boundary. HypothesisResult contains stable identity, candidate
identity, accepted state, abstract confidence, abstract supporting/rejected
evidence labels, and timestamp only.

No detector values, validator calculations, thresholds, trade instructions, or
risk/execution information crosses this interface.

## Recoil Validator v1.0

**Implementation status:** First research-derived validator implemented.

| Component | Responsibility | Dependencies | Prohibited content |
|---|---|---|---|
| `RecoilConfig` | Immutable external recoil threshold configuration | Standard library JSON | Detector access, trading decisions, embedded research parameters |
| `RecoilValidator` | Determine whether supplied contextual movement satisfies the configured recoil rule | Candidate, ValidationContext, RecoilConfig | Hypothesis, risk, execution, or broker decisions |

### Evidence definitions

`RECOIL_OBSERVED` means the supplied context satisfied the configured recoil
rule. `RECOIL_NOT_OBSERVED` means it did not. Neither label exports a distance,
threshold, indicator, or detector calculation.

### Dependency graph

`Candidate` + `ValidationContext` + `RecoilConfig` â†’ `RecoilValidator` â†’
`ValidationResult`

The context supplies raw reference/current values and an expected direction only
at the validator boundary. They are not copied to the public result contract.

## Interchangeable Decision Policies v1.0

| Component | Responsibility | Dependencies | Prohibited content |
|---|---|---|---|
| `DecisionPolicyContract` | Interpret immutable validation evidence for a stable hypothesis | Hypothesis, ValidationResult | Detector access, broker, risk, execution, mutation |
| `StrictPolicy` | Historical all-results-pass interpretation | Abstract evidence only | Weighting, probability, market calculations |
| `BalancedPolicy` | Future research insertion point; presently strict-equivalent | Strict policy behavior | Unapproved weighting research |
| `ExploratoryPolicy` | Future research insertion point; presently strict-equivalent | Strict policy behavior | Probabilities or decision research |
| `PolicyFactory` | Deterministic named policy construction | Explicit supported names | Reflection, plugins, registry loading |

`DefaultPolicy` is an alias of `StrictPolicy`. This preserves the previous
all-validator-pass behavior while allowing future policies to change only the
evidence interpretation boundary.

## Experiment Ledger v1.0

| Component | Responsibility | Dependencies | Prohibited content |
|---|---|---|---|
| `ExperimentRecord` | Immutable experiment provenance, exact validation evidence, policy provenance, abstract decision and optional outcome facts | ValidationResult, HypothesisResult | Indicators, thresholds, detector internals, private validator state, opinions |
| `LedgerContract` | Stable append and retrieval boundary | ExperimentRecord | Database-specific behavior |
| `LedgerRepository` | Deterministic append-order in-memory implementation | LedgerContract | Mutation of stored records, persistence dependencies |

`ExperimentRecord.validation_results` retains the original immutable tuple
unchanged. Policy name, semantic version, and SHA-256 parameter hash allow a
future policy implementation to evaluate historical evidence without rerunning
the detector. Rule #15 defines this replay requirement.

## Frozen Ontology and Layer Direction

QuantForge is a **Scientific Operating System for Market Research and Behavioral
Trading**. The following terms are architectural ontology; temporal-domain terms
are documented for their intended responsibilities and do not assert a current
implementation.

| Layer | Stable responsibilities | Direction rule |
|---|---|---|
| Market Reality | `EnvironmentSnapshot` | May not depend on a higher layer. |
| Behavioral Reality | `BehaviorObservation`, `BehaviorFrame`, `FrozenBehaviorTimeline` | Receives market facts only. |
| Scientific Reality | `ValidationResult`, `HypothesisDecision`, `ExperimentRecord` | Interprets behavioral facts only. |
| Operational Reality | `RiskPlan`, `TradeOrder`, `TradeResult` | Consumes scientific conclusions; never feeds them upward. |

`ActiveObservationTimeline` is private to the Behavior Observation Window;
`freeze()` produces `FrozenBehaviorTimeline`. Observation Policy governs window
duration and termination only; Decision Policy interprets evidence only; Risk
Policy governs capital only. Rule #16 requires persistence at observation
creation. Rule #17 freezes downward-only information flow.

## Temporal Ontology — Sprint 2.1

| Component | Responsibility | Mutability | Prohibited content |
|---|---|---|---|
| `EnvironmentSnapshot` | Opaque immutable Market Reality provenance | Immutable | Indicators, detector logic, behavior logic |
| `BehaviorFrame` | One categorical behavioral fact and snapshot reference | Immutable | Z-score, ATR, momentum, thresholds, detector scores |
| `ActiveObservationTimeline` | Caller-ordered frame builder and one-time `freeze()` boundary | Mutable builder only | Observation policy, decisions, replay, ledger behavior |
| `FrozenBehaviorTimeline` | Canonical immutable temporal aggregate | Immutable | Mutation, policy decision, risk, execution |
| `TimelineRepositoryContract` | Future persistence boundary | Abstract | Storage implementation |

`BehaviorTimeline` refers to `FrozenBehaviorTimeline` at module boundaries.
The active form never leaves the future Behavior Observation Window. All IDs and
timestamps are caller-supplied; temporal objects generate neither clocks nor
random identifiers.

## Observation Policy Interface v1.0

**Implementation status:** Observation lifecycle contract implemented.

| Component | Responsibility | Dependencies | Prohibited content |
|---|---|---|---|
| `ObservationPolicyContract` | Abstract observation lifecycle boundary | `ObservationConfig`, `ObservationDecision` | Behavioral interpretation, evidence, risk, execution |
| `DefaultObservationPolicy` | Deterministic frame-count and duration termination | `ObservationPolicyContract`, `ObservationConfig` | Market intelligence, heuristics, adaptive logic |
| `ObservationConfig` | Immutable external configuration (max_frames, max_duration) | Standard library JSON | Hardcoded business rules, detector parameters |
| `ObservationDecision` | Immutable lifecycle decision with termination reason | Standard library only | Indicators, thresholds, evidence, trade instructions |
| `ObservationPolicyFactory` | Deterministic named policy construction | Explicit supported names | Reflection, plugins, registry loading |

### Dependency graph

The Observation Policy is strictly independent from Decision Policy (evidence
interpretation) and Risk Policy (capital allocation). Future adaptive policies
(Market DNA–driven) can implement `ObservationPolicyContract` without modifying
the BOW or any other component.

## Infrastructure Completion — Sprint 2.2.5

**Status:** FROZEN

| Component | Responsibility |
|---|---|
| `EnvironmentRepositoryContract` | Abstract boundary for EnvironmentSnapshot persistence |
| `TimelineRepository` | Abstract boundary for FrozenBehaviorTimeline persistence |
| `TerminationReason` | Shared canonical definitions for observation termination |
| `ObservationPolicy` | Deterministic timestamp injection for exact replay |

No implementation details are exposed through these interfaces.

## Behavior Observation Window — Sprint 2.3

**Status:** FROZEN

| Component | Responsibility |
|---|---|
| `BehaviorObservationWindowContract` | Canonical runtime contract for temporal collection |
| `BOWResult` | Immutable output containing the FrozenBehaviorTimeline and statistics |
| `BOWError` hierarchy | Deterministic domain errors (e.g. `DoubleFreezeError`, `AppendAfterFreezeError`) |

**Window Lifecycle & Policy Interaction:**
The BOW coordinates the lifecycle from `open()` to `freeze()`. During `append_snapshot()`, it consults the `ObservationPolicyContract` deterministically. Upon termination, it freezes the `ActiveObservationTimeline` into a `FrozenBehaviorTimeline`, returning a fully immutable `BOWResult` without leaking runtime details.
## Replay Engine — Sprint 2.4

**Status:** FROZEN

| Component | Responsibility |
|---|---|
| `ReplayEngineContract` | Abstract canonical contract for deterministic scientific playback |
| `ReplayEngine` | Core deterministic implementation |
| `ReplayCursor` | Immutable output snapshot yielding the current index, `BehaviorFrame`, and `EnvironmentSnapshot` |
| `ReplayResult` | Immutable final statistics of the replay execution |
| `ReplayState` | Immutable enumeration of playback state (LOADED, PLAYING, COMPLETE) |
| `ReplayError` hierarchy | Domain-specific deterministic errors (e.g. `MissingTimelineError`) |

**Repository Usage & Boundaries:**
The engine exclusively consumes `FrozenBehaviorTimeline` outputs and relies strictly upon `TimelineRepositoryContract` and `EnvironmentRepositoryContract` to resolve dependencies. The boundary ensures completely deterministic replay without side effects, preventing any execution, risk, or behaviour validation logic from leaking into the playback stream.

===========================================================
EVIDENCE INTERFACE v1.0 (Sprint 3.1)
===========================================================

**Producer:**
ObserverContract implementation

**Consumer:**
Future Hypothesis Engine / Evidence Modules

**Dependency Graph:**
FrozenBehaviorTimeline → ObserverContract → Evidence

`Evidence` contains only:
- evidence_id, candidate_id, timeline_id
- observer_name, observer_version
- evidence_type, confidence (0.0-1.0), observed (bool)
- evidence_labels, metadata, timestamp

- evidence_labels, metadata, timestamp

No indicator values, trading decisions, risk logic, or execution directives are allowed across this boundary.

===========================================================
SCIENTIFIC OBSERVATION LAYER v1.0
===========================================================

**Observer Responsibilities:**
- Measure isolated behavioral phenomena mathematically.
- Expose abstract properties as metadata.

**Observer Boundaries:**
- Observers operate purely on the Replay Engine output.
- Observers NEVER interpret the evidence.

**Replay Dependencies:**
- `ReplayEngineContract`
- `ReplayCursor`
- `BehaviorFrame`
- `EnvironmentSnapshot`

**Evidence Output:**
- Singular, immutable `Evidence` object per run.

**Forbidden Dependencies:**
- Other Observers (e.g., Velocity cannot import Recoil).
- Interpretation Engine, Risk, Execution, or DNA metrics.

**State explicitly:**
Observation Layer is complete.
Aggregation begins in Sprint 3.7.


=========================================================
SPRINT 3.8 FREEZE: BEHAVIOUR PROFILE ENGINE
=========================================================

### BehaviourProfile Contract

**Public Contracts:**
- BehaviourProfile: Immutable container. Holds schema versions, provenance vectors, metadata, and a sorted tuple of descriptors.
- BehaviourDescriptor: Immutable tuple mapping a string 
ame to a generic 
alue. It ONLY describes behaviour.
- BehaviourProfileEngine: A completely stateless factory mapping an EvidencePackage to a BehaviourProfile. 
  - Extensible via DescriptorBuilderFunc injection.

**Construction Rules:**
- Profiles and Descriptors must be instantiated with all required fields.
- Provenance lists and descriptors are deterministically sorted upon initialization to ensure replay consistency.
- Mutable collections are strictly forbidden.

**Error Hierarchy:**
- ProfileError
  - InvalidBehaviourProfile
  - MissingBehaviourDescriptor
  - DuplicateBehaviourDescriptor
  - BehaviourProfileConstructionError

**Dependency Boundaries:**
- May only depend on oe.evidence.evidence.EvidencePackage.


=========================================================
SPRINT 3.8 — BEHAVIOUR PROFILE ENGINE
=========================================================

### Public API & Contracts

**BehaviourProfile Contract:**
- BehaviourProfile: Immutable container representing described behaviour. Contains schema versions, metadata, and provenance.
- BehaviourDescriptor: Immutable tuple mapping string names to values (describing traits).

**Dependency Rules:**
- Profiles may only depend upon oe.evidence.evidence.EvidencePackage.

**Error Hierarchy:**
- ProfileError (Base)
  - InvalidBehaviourProfile
  - MissingBehaviourDescriptor
  - DuplicateBehaviourDescriptor
  - BehaviourProfileConstructionError


=========================================================
SPRINT 3.9 — INTERPRETATION REGISTRY
=========================================================

### Interpretation Registry & Contracts

**InterpretationModelContract:**
- Abstract contract ensuring models define a model_name and an interpret method.
- **Model Responsibilities:** Transform BehaviourProfile into an Interpretation. Models interpret Behaviour Profiles.

**InterpretationRegistry:**
- **Registry Responsibilities:** Exclusively manages the lifecycle, lookup, and selection of models. Registry selects models.

*(Note: Decision making begins in a future phase. The registry and model absolutely do not authorize trades.)*

**Public APIs:**
- 
egister(model: InterpretationModelContract)
- get_model(model_name: str)
- has_model(model_name: str)
- 
egistered_models (Returns a sorted, immutable tuple of model names)

**Error Hierarchy:**
- InterpretationModelNotFound
- DuplicateInterpretationModel
- InvalidInterpretationModel
- RegistryConfigurationError

**Dependency Rules:**
- The Interpretation layer may only depend on the Behaviour Profile layer and core types.


=========================================================
SPRINT 3.10 — DECISION POLICY
=========================================================

### Public APIs & Contracts

**DecisionPolicyContract & DecisionConfig:**
- Abstract contract ensuring policies strictly map `Interpretation` -> `Decision`. Implicitly encapsulates policy-specific configuration variables cleanly away from the data structures.

**Decision:**
- Immutable scientific outcome container specifying an explicit `DecisionAction` and `rationale`.

**Dependency Rules:**
- Decision Policy may only depend upon `Interpretation` and basic typing. It must NEVER depend on Risk, Execution, or MT5 logic.

**Error Hierarchy:**
- `DecisionError` (Base)
  - `InvalidDecision`
  - `MissingInterpretation`
  - `DecisionConflict`
  - `UnsupportedInterpretation`
  - `DecisionConstructionError`


=========================================================
SPRINT 3.11 — DECISION REGISTRY
=========================================================

### Public APIs & Contracts

**DecisionRegistry:**
- **Registry Responsibilities:** Handles registration, lookup, duplicate rejection, and strict lifecycle orchestration of `DecisionPolicyContract`s.

**Public APIs:**
- `register(policy: DecisionPolicyContract)`
- `get_policy(policy_name: str)`
- `has_policy(policy_name: str)`
- `registered_policies` (Returns a sorted, immutable tuple of active policies)

**Dependency Rules:**
- The registry operates purely horizontally within the Decision layer and strictly downward. Absolutely zero interaction with Risk or Execution.

**Registry Errors:**
- `DecisionPolicyNotFound`
- `DuplicateDecisionPolicy`
- `InvalidDecisionPolicy`
- `RegistryConfigurationError`


=========================================================
PHASE 3 FREEZE — PUBLIC CONTRACTS
=========================================================

The following public contracts and their strict responsibilities are now permanently frozen:

- **EvidencePackage:** Holds the raw temporal and observational aggregates.
- **BehaviourProfile:** Holds descriptive `BehaviourDescriptor` facts.
- **InterpretationModelContract / InterpretationRegistry:** Manages the mapping of Profile to Interpretation without generating trade logic.
- **Interpretation:** The immutable outcome of scientific hypothesis assignment.
- **DecisionPolicyContract / DecisionRegistry:** Manages the mapping of Interpretation to Decision without risk calculations.
- **Decision:** The immutable determination of hypothesis actionability.


=========================================================
SPRINT 4.1 — RISK MODEL
=========================================================

### Public APIs & Contracts

**RiskModelContract:**
- Core abstract contract responsible for transforming `Decision` -> `RiskProfile`. 

**RiskProfile & RiskDescriptor:**
- `RiskProfile` serves as the immutable description of capital exposure containing multiple `RiskDescriptor`s. 
- Descriptors are strictly typed string-tuples describing abstract properties (e.g., "Standard Exposure", "Independent").

**Error Hierarchy:**
- `RiskError` (Base)
  - `InvalidRiskModel`
  - `MissingDecision`
  - `UnsupportedDecision`
  - `RiskModelConstructionError`


=========================================================
SPRINT 4.2 — RISK POLICY
=========================================================

### Public APIs & Contracts

**RiskPolicyContract & RiskPolicyConfig:**
- Abstract contract ensuring policies map `Decision` + `RiskProfile` -> `RiskPolicyEvaluation`. Configuration parameters (e.g., `strict_mode`) are isolated inside immutable configs to modify policy behavior without mutating public interfaces.

**Risk Policy Errors:**
- Extends the `RiskError` base with `MissingRiskModel`, `UnsupportedRiskModel`, and `RiskPolicyConstructionError`.

**Dependency Rules:**
- The Risk Policy strictly evaluates inputs. It must NEVER depend on `PositionSizer`, `RiskAssessment`, `Execution`, or `Broker` definitions.


=========================================================
SPRINT 4.3 — RISK POLICY REGISTRY
=========================================================

### Public APIs & Contracts

**RiskPolicyRegistry:**
- **Registry Responsibilities:** Handles registration, lookup, duplicate rejection, and strict lifecycle orchestration of `RiskPolicyContract`s.

**Public APIs:**
- `register(policy: RiskPolicyContract)`
- `get_policy(policy_name: str)`
- `has_policy(policy_name: str)`
- `registered_policies` (Returns a sorted, immutable tuple of active policies)

**Dependency Rules:**
- The registry operates purely horizontally. Absolutely zero interaction with `PositionSizer`, `RiskAssessment`, or Execution.

**Registry Errors:**
- `RiskPolicyNotFound`
- `DuplicateRiskPolicy`
- `InvalidRiskPolicy`
- `RiskRegistryConfigurationError`


=========================================================
SPRINT 4.4 — RISK ASSESSMENT
=========================================================

### Public APIs & Contracts

**RiskAssessment:**
- Immutable value object providing structural mapping from `RiskPolicyEvaluation` outputs. Defines properties such as `AssessmentStatus`, candidate identifiers, and descriptive rationales.

**Public API:**
- `RiskAssessment.from_policy_evaluation(evaluation: RiskPolicyEvaluation, timestamp: datetime) -> RiskAssessment`

**Error Hierarchy:**
- Extends the `RiskError` base with `InvalidRiskAssessment`, `MissingRiskDecision`, and `InvalidAssessmentState`.


=========================================================
SPRINT 4.5 — POSITION SIZER
=========================================================

### Public APIs & Contracts

**PositionSizerContract & PositionSizerConfig:**
- Core abstract boundaries for PositionSizer algorithms. Configurations determine base fractions and scalar limits. 

**Public APIs:**
- `size_position(assessment: RiskAssessment, timestamp: datetime) -> PositionSizingResult`

**Error Hierarchy:**
- `PositionSizingError`
- `UnsupportedSizingMethod`
- `InvalidPositionSizer`


=========================================================
SPRINT 4.6 — POSITION SPECIFICATION
=========================================================

### Public APIs & Contracts

**PositionSpecification:**
- Immutable transport object declaring exposure arrays (`position_size_multiplier`, `exposure_fraction`, `risk_units`). 

**Public APIs:**
- `PositionSpecification.from_sizing_result(sizing_result: PositionSizingResult, timestamp: datetime) -> PositionSpecification`

**Error Hierarchy:**
- `InvalidPositionSpecification`
- `InvalidSizingOutput`
- `PositionSpecificationConstructionError`


=========================================================
PHASE 4 FREEZE: CAPITAL ALLOCATION LAYER
=========================================================

**All Phase 4 Public Contracts Are Frozen:**
- `RiskModelContract`
- `RiskPolicyContract`
- `RiskPolicyRegistryContract`
- `PositionSizerContract`

Value Objects:
- `RiskProfile`
- `RiskPolicyEvaluation`
- `RiskAssessment`
- `PositionSizingResult`
- `PositionSpecification`

**No modifications are permitted to these interfaces without triggering a full architectural boundary review.**


=========================================================
SPRINT 5.1 — EXECUTION ENGINE CONTRACT
=========================================================

### Public APIs & Contracts

**ExecutionEngineContract & ExecutionConfig:**
- Core interfaces defining the immutable blueprint processors. 

**Error Hierarchy:**
- Base: `ExecutionError`
- Branches: `InvalidPositionSpecification`, `ExecutionConfigurationError`, `UnsupportedExecutionEngine`, `ExecutionContractViolation`


=========================================================
SPRINT 5.2 — BROKER ADAPTER CONTRACT
=========================================================

### Public APIs & Contracts

**BrokerAdapterContract & BrokerAdapterConfig:**
- Universal abstraction defining how specifications are dispatched to broker endpoints.

**Error Hierarchy:**
- Base: `ExecutionError`
- Branches: `InvalidBrokerAdapter`, `UnsupportedBroker`, `AdapterConfigurationError`, `BrokerContractViolation`


=========================================================
SPRINT 5.3 — EXECUTION RESULT
=========================================================

### Public APIs & Contracts

**ExecutionResult:**
- Immutable dataclass structure encapsulating metadata and deterministic timestamps.

**ExecutionStatus:**
- Standardized enumeration (`SUCCESS`, `FAILED`, `PARTIALLY_EXECUTED`, `REJECTED`, `CANCELLED`, `TIMEOUT`).

**Error Hierarchy:**
- Base: `ExecutionError`
- Branches: `InvalidExecutionResult`, `InvalidExecutionStatus`, `ExecutionResultValidationError`


=========================================================
SPRINT 5.4 — EXECUTION ENGINE
=========================================================

### Public APIs & Contracts

**DefaultExecutionEngine:**
- Concrete orchestrator implementing the `ExecutionEngineContract`.

**Public APIs:**
- `DefaultExecutionEngine(config: ExecutionConfig, adapter: BrokerAdapterContract)`
- `.execute(specification: PositionSpecification) -> ExecutionResult`

**Error Hierarchy:**
- Base: `ExecutionError`
- Branches: `ExecutionFailure`, `AdapterUnavailable`, `InvalidExecutionRequest`, `ExecutionEngineConfigurationError`


=========================================================
SPRINT 5.5 — MT5 TRANSPORT
=========================================================

### Public APIs & Contracts

**MT5TransportContract & MT5TransportConfig:**
- Universal, deterministic interface for routing physical requests down to the SDK layer.

**Error Hierarchy:**
- Base: `ExecutionError` -> `MT5TransportError`
- Branches: `MT5ConnectionError`, `MT5InitializationError`, `MT5CommunicationError`


=========================================================
SPRINT 5.6 — MT5 ADAPTER
=========================================================

### Public APIs & Contracts

**MT5Adapter & MT5AdapterConfig:**
- Core translator between execution logic and transport packets.

**Error Hierarchy:**
- Base: `ExecutionError` -> `MT5AdapterError`
- Branches: `InvalidMT5Adapter`, `UnsupportedOrderType`, `TranslationError`, `MT5AdapterConfigurationError`


=========================================================
SPRINT 5.7 — PYTHON SIMULATION ADAPTER
=========================================================

### Public APIs & Contracts

**PythonSimulationAdapter & Configuration:**
- `PythonSimulationAdapterConfig`: Immutable environment descriptor.
- `.dispatch(specification)`: Models execution mathematically.

**Error Hierarchy:**
- Base: `ExecutionError` -> `SimulationExecutionError`
- Branches: `UnsupportedSimulationRequest`, `SimulationConfigurationError`


=========================================================
SPRINT 5.8 — PAPER TRADING ADAPTER
=========================================================

### Public APIs & Contracts

**PaperTradingAdapter & PaperTradingAccount:**
- `PaperTradingAccount`: Immutable virtual ledger for open positions and simulated equity.
- `PaperTradingAdapterConfig`: Immutable environment descriptor.

**Error Hierarchy:**
- Base: `ExecutionError` -> `PaperTradingError`
- Branches: `PaperAccountError`, `InvalidPaperExecution`, `PaperConfigurationError`


=========================================================
SPRINT 6.1 — HYPOTHESIS CONTRACT
=========================================================

### Public APIs & Contracts

**Hypothesis Validation:**
- `HypothesisContract`: Boundary interface for retrieving a `Hypothesis`.
- `Hypothesis`: Immutable domain object housing metadata and author identifiers.
- `HypothesisStatus`: Enum defining lifecycle states (DRAFT, ACTIVE, VALIDATED, REJECTED, ARCHIVED).

**Error Hierarchy:**
- Base: `ScienceError` -> `HypothesisError`
- Branches: `InvalidHypothesisData`, `InvalidHypothesisStatus`


=========================================================
SPRINT 6.2 — EXPERIMENT CONTRACT
=========================================================

### Public APIs & Contracts

**Experiment Specification:**
- `ExperimentContract`: Boundary interface for retrieving an `Experiment`.
- `Experiment`: Immutable domain specification outlining testing bounds.
- `ExperimentStatus`: Enum defining lifecycle states (DRAFT, READY, RUNNING, COMPLETED, CANCELLED).

**Error Hierarchy:**
- Base: `ScienceError` -> `ExperimentError`
- Branches: `InvalidExperimentData`, `InvalidExperimentStatus`


=========================================================
SPRINT 6.3 — VALIDATION CONTRACT
=========================================================

### Public APIs & Contracts

**Validation Conclusion:**
- `ValidationContract`: Boundary interface for retrieving a `Validation`.
- `Validation`: Immutable domain object recording the experimental outcome.
- `ValidationStatus`: Enum defining outcome states (VALIDATED, REJECTED, PARTIALLY_VALIDATED, INCONCLUSIVE).

**Error Hierarchy:**
- Base: `ScienceError` -> `ValidationError`
- Branches: `InvalidValidationData`, `InvalidValidationStatus`


=========================================================
SPRINT 6.4 — VALIDATION SERVICE
=========================================================

### Public APIs & Contracts

**Orchestration Services:**
- `ValidationServiceContract`: Boundary interface orchestrating the transition from Experiment to Validation.
- `ValidationService`: Stateless service enforcing object lineage (`Hypothesis` to `Experiment`) before constructing an immutable `Validation`.

=========================================================
SPRINT 7.1: STRATEGY ASSEMBLY CONTRACTS
=========================================================

- **StrategyContract:** Defines the immutable properties of an executable scientific model.
- **Strategy:** The frozen dataclass implementation of the StrategyContract.
- **StrategyStatus:** Enum defining the lifecycle states (DRAFT, READY, PAPER, DEMO, LIVE, RETIRED).
- **Error Hierarchy:**
  - StrategyError: Base exception.
  - InvalidStrategyComponentError: Raised on invalid missing components.
  - InvalidStrategyLifecycleError: Raised on invalid status transitions.