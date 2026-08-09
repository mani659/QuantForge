# QuantForge System Architecture
Version: 1.0
Status: Active Development
Last Updated: 2026-07-15

===========================================================
QUANTFORGE SYSTEM ARCHITECTURE
===========================================================

PURPOSE

This document defines the complete software architecture of
QuantForge.

It describes how every module interacts with the rest of the
system and establishes the development contract for all future
components.

This document intentionally avoids implementation details.

===========================================================
DESIGN PHILOSOPHY
===========================================================

QuantForge is built as a modular pipeline.

Each module has one responsibility.

Each module produces validated outputs.

No module depends on hidden state.

Every stage can be tested independently.

Architecture Principles

• Single Responsibility

• Deterministic Behaviour

• Modular Components

• Cross-Market Compatibility

• Research First

• Data Validation Before Analysis

• Freeze Stable Modules

===========================================================
CANONICAL ARCHITECTURE (BOE)
===========================================================

The Behavioral Observation Engine (BOE) is the only canonical architecture.

Market Reality          →  EnvironmentSnapshot
        ↓
Behavioral Reality      →  BehaviorObservation, BehaviorFrame, FrozenBehaviorTimeline
        ↓
Scientific Reality      →  Evidence, BehaviourProfile, Interpretation, Decision, ValidationResult
        ↓
Operational Reality     →  RiskModel, RiskAssessment, PositionSpecification, ExecutionResult

Legacy modules (such as Tick Validator, Market DNA Profiler, etc.) remain as historical artifacts that contributed to the research discoveries. They are not part of the canonical runtime pipeline. Future development targets the BOE exclusively.

===========================================================
LEGACY ARCHITECTURE (Historical)
===========================================================

                 RAW MARKET DATA
                        │
                        ▼
              Tick Validator
                        │
                        ▼
            Tick → M1 Converter
                        │
                        ▼
               M1 Validator
                        │
                        ▼
             Market DNA Profiler
                        │
                        ▼
             DNA Comparator
                        │
                        ▼
           Experiment Recorder
                        │
                        ▼
          Feature Matrix Builder
                        │
                        ▼
        Strategy Intelligence Engine
                        │
                        ▼
       Adaptive Strategy Engine
                        │
                        ▼
            Signal Generator
                        │
                        ▼
               Risk Engine
                        │
                        ▼
            Execution Engine
                        │
                        ▼
             Python Trading Engine
                        │
                        ▼
              MT5 Expert Advisor

===========================================================
LAYER 1
DATA FOUNDATION
===========================================================

Modules

Tick Validator

Tick → M1 Converter

M1 Validator

Purpose

Guarantee clean market data before any research begins.

Outputs

Validated Tick Data

Validated M1 Data

Rule

No downstream module may process unvalidated data.

===========================================================
LAYER 2
MARKET UNDERSTANDING
===========================================================

Modules

Market DNA Profiler

DNA Comparator

Purpose

Transform price data into quantitative behavioural
characteristics.

Outputs

DNA Profile

Cross-Market DNA Comparison

Responsibilities

Measure

Trend

Volatility

Expansion

Pullback

Volume

Market Structure

===========================================================
LAYER 3
RESEARCH DATABASE
===========================================================

Modules

Experiment Recorder

Feature Matrix Builder

Purpose

Store every experiment in a standardized format.

Responsibilities

Record

Parameters

DNA Snapshot

Performance

Trades

Equity

Robustness

Outputs

JSON

CSV

Parquet

This layer represents QuantForge's permanent research memory.

===========================================================
LAYER 4
TRADING INTELLIGENCE
===========================================================

Modules

Strategy Intelligence

Adaptive Strategy Engine

Purpose

Convert statistical observations into trading decisions.

Strategy Intelligence

Finds relationships between

DNA

↓

Performance

Adaptive Strategy

Determines

How should this market be traded?

Outputs

Strategy Class

Holding Style

Risk Profile

Exit Preference

Confidence

===========================================================
LAYER 5
TRADE DECISION
===========================================================

Modules

Signal Generator

Purpose

Determine

Should a trade be taken now?

Inputs

Adaptive Strategy

Market Data

DNA

Outputs

BUY

SELL

NO TRADE

Signal Strength

Confidence

This module never manages risk.

===========================================================
LAYER 6
RISK MANAGEMENT
===========================================================

Module

Risk Engine

Purpose

Determine

How much should be traded?

Responsibilities

Position Size

Risk %

Maximum Exposure

Maximum Daily Loss

Maximum Consecutive Losses

Maximum Open Positions

Outputs

Trade Risk

Lot Size

Position Limits

===========================================================
LAYER 7
EXECUTION
===========================================================

Module

Execution Engine

Purpose

Execute approved trades.

Responsibilities

Order Placement

Trade Modification

Stop Management

Take Profit

Partial Close

Trailing Stop

Logging

Outputs

Executed Positions

Trade History

===========================================================
LAYER 8
PLATFORMS
===========================================================

Primary

Python Trading Engine

Purpose

Research

Simulation

Forward Testing

Validation

Secondary

MT5 Expert Advisor

Purpose

Live Trading

The Python implementation is always considered the
reference implementation.

MT5 mirrors Python behaviour.

===========================================================
MODULE COMMUNICATION
===========================================================

Modules communicate only through structured outputs.

Examples

Tick Validator

↓

Validated Tick CSV

---------------------------------------

DNA Profiler

↓

DNA JSON

---------------------------------------

Experiment Recorder

↓

Run Folder

---------------------------------------

Adaptive Strategy

↓

Recommendation JSON

---------------------------------------

Signal Generator

↓

Signal JSON

Hidden shared state is prohibited.

===========================================================
DATA FLOW
===========================================================

Tick Data

↓

Validated Tick

↓

M1

↓

Validated M1

↓

DNA

↓

Experiments

↓

Feature Matrix

↓

Strategy Intelligence

↓

Adaptive Strategy

↓

Signal Generator

↓

Risk Engine

↓

TradePlan

↓

Execution Engine

↓

Trade

===========================================================
CONFIGURATION
===========================================================

Configuration is external.

Examples

adaptive_rules.json

Future

risk_rules.json

signal_rules.json

execution_rules.json

No business logic should depend on hardcoded constants.

===========================================================
TESTING STRATEGY
===========================================================

Every module must provide

Independent Unit Test

Independent Validation Report

Deterministic Output

Regression Safety

A module is frozen only after all tests pass.

===========================================================
VERSIONING POLICY
===========================================================

Major Version

Architectural changes.

Minor Version

New functionality.

Patch Version

Bug fixes.

Stable modules are frozen.

Future work proceeds in new versions.

===========================================================
NON-GOALS
===========================================================

QuantForge is NOT

An indicator collection.

A discretionary trading system.

A black-box AI.

A curve-fitting framework.

A market prediction engine.

QuantForge IS

A deterministic adaptive trading platform based on
statistically validated market behaviour.

===========================================================
MT5 BROKER ADAPTER PIPELINE
===========================================================

TradeOrder

↓

MT5 Connection Manager

↓

MT5 Broker Adapter

↓

MetaTrader 5

↓

TradeResult

↓

Experiment Recorder

===========================================================
PROJECT MATURITY
===========================================================

Foundation: 100%

Research Platform: 100%

Decision Layer: 100%

Execution Layer: 20%

Live Intelligence: 0%

Overall Project Progress: Approximately 80%

Architecture Completion: 100%

Remaining Work: Implementation, not architecture.

===========================================================
FUTURE ARCHITECTURE
===========================================================

Possible additions after Python EA

Bayesian Decision Engine

Machine Learning Layer

Portfolio Intelligence

Multi-Timeframe DNA

Market Regime Detection

Dynamic Rule Optimisation

These components must never replace deterministic
logic until they demonstrate statistically superior
performance.

===========================================================
END OF ARCHITECTURE
===========================================================

===========================================================
BEHAVIORAL OBSERVATION ENGINE (BOE) v1.0
===========================================================

Status: Contract foundation implemented. No detector or trading logic exists.

Contract diagram

ObservationEnvironment

↓

BehaviorDetectorContract

↓

BehaviorObservation

The BOE exposes observed behavior only. Internal detector calculations,
indicator values, thresholds, and candidate state never cross this boundary.

===========================================================
CANDIDATE MANAGER v1.0
===========================================================

Status: Deterministic lifecycle contract implemented. No behavioral validation,
trade signal, risk action, or execution action exists in this component.

Lifecycle

NEW → OBSERVING → VALIDATING → QUALIFIED → EXECUTED

VALIDATING → REJECTED

OBSERVING or VALIDATING → EXPIRED

Candidate Manager consumes BehaviorObservation and emits immutable Candidate
snapshots plus CandidateEvent transition records. The future Candidate Ledger
persists events; it does not decide transitions.

===========================================================
BEHAVIOR VALIDATOR FRAMEWORK (BVF) v1.0
===========================================================

Status: Contract and deterministic pipeline foundation implemented. No recoil,
persistence, context, session, volatility, or regime validator exists yet.

Dependency graph

Candidate + ValidationContext

↓

BehaviorValidatorContract implementations

↓

ValidationResult tuple

↓

Future Hypothesis Evaluation

ValidatorPipeline executes every configured validator sequentially and returns
all results without aggregating, short-circuiting, or deciding a hypothesis.

===========================================================
HYPOTHESIS ENGINE (HE) v1.0
===========================================================

Status: Deterministic evidence interpretation foundation implemented. No trading,
detector, validator, risk, execution, or market logic exists in this component.

Dependency graph

Candidate + tuple[ValidationResult]

↓

HypothesisEngine

↓

DecisionPolicyContract

↓

HypothesisResult

The default DeterministicDecisionPolicy accepts only when every validator result
passed. Future policies replace this policy boundary; validators remain unchanged.

===========================================================
RECOIL VALIDATOR v1.0
===========================================================

Status: First research-derived validator implemented. RecoilValidator consumes
only Candidate and ValidationContext through the BVF contract, then returns a
ValidationResult. Its externally configured threshold is read from immutable
RecoilConfig; it does not expose a distance, threshold, or other calculation.

Dependency graph

Candidate + ValidationContext

â†“

RecoilValidator + RecoilConfig

â†“

ValidationResult (RECOIL_OBSERVED | RECOIL_NOT_OBSERVED)

Research traceability: the validator operationalizes the recoil observation
recorded in DISC-004 and DISC-019. It answers only whether recoil was observed;
it does not accept a hypothesis or make a trading, risk, or execution decision.

===========================================================
INTERCHANGEABLE DECISION POLICIES v1.0
===========================================================

Status: Implemented. Evidence modules observe independently; policies determine
how much immutable ValidationResult evidence is sufficient. The HypothesisEngine
continues to create a stable Hypothesis and delegates interpretation to one
DecisionPolicyContract implementation.

Policy hierarchy

DecisionPolicyContract
â†“
StrictPolicy (default; all validators pass)
â†“
BalancedPolicy / ExploratoryPolicy (research extension points; strict baseline)

QuantForge Rule #13: Evidence Modules observe independently. Decision Policies
determine how much evidence is sufficient. Policies may evolve; Evidence Modules
should rarely change.

===========================================================
EXPERIMENT LEDGER v1.0
===========================================================

Status: Implemented as the canonical immutable scientific memory for behavioral
experiments. Every candidate may be recorded irrespective of hypothesis outcome,
risk approval, or execution.

Replay architecture

Candidate provenance + immutable ValidationResult tuple + policy name/version/
parameter hash + HypothesisResult

â†“

ExperimentRecord

â†“

LedgerContract â†’ in-memory LedgerRepository (future CSV / SQLite / DuckDB / Parquet)

QuantForge Rule #15: every experiment must remain reproducible years later using
the Experiment Ledger, Policy Version, and Policy Parameter Hash. The ledger
stores facts and provenance only; it never stores indicators, thresholds,
detector internals, private validator state, or explanations.

===========================================================
ARCHITECTURE FREEZE: SCIENTIFIC OPERATING SYSTEM
===========================================================

Effective architecture statement: QuantForge is a **Scientific Operating System
for Market Research and Behavioral Trading**. Historical references to a
"trading framework" or "trading platform" describe earlier milestones and do
not define the frozen architecture below.

QuantForge has four immutable layers. Information flows strictly downward;
higher layers never depend on lower layers.

1. Market Reality: `EnvironmentSnapshot`
2. Behavioral Reality: `BehaviorObservation`, `BehaviorFrame`,
   `FrozenBehaviorTimeline`
3. Scientific Reality: `ValidationResult`, `HypothesisDecision`,
   `ExperimentRecord`
4. Operational Reality: `RiskPlan`, `TradeOrder`, `TradeResult`

The ontology defines architectural responsibilities, not implementation choices.
`EnvironmentSnapshot` records supplied market reality. `BehaviorObservation`
records an observed behavior. `BehaviorFrame` represents one temporal behavioral
fact. `ActiveObservationTimeline` is the bounded, mutable collection used only
inside a Behavior Observation Window. `FrozenBehaviorTimeline` is its immutable
historical form. `ExperimentRecord` is the durable scientific provenance record
for the observation, its evidence, and its policy interpretation.

Current Architecture Lifecycle:

Research
↓
Scientific Validation Framework
↓
Strategy Assembly
↓
Deployment Assembly
↓
Deployment Runtime
↓
Paper Trading
↓
Demo Trading
↓
Live Trading
↓
Deployment Evidence Capture
↓
OutcomeReader
↓
END OF SOFTWARE
↓
Human Research Review
(planning-era label: "Research Feedback")

===========================================================
TEMPORAL OBSERVATION ARCHITECTURE
===========================================================

Behavior Detector
â†“
Candidate
â†“
Behavior Observation Window
â†“
Observation Policy
â†“
ActiveObservationTimeline
â†“
freeze()
â†“
FrozenBehaviorTimeline
â†“
Behavioral Evidence Modules
â†“
Experiment Ledger
â†“
Decision Policy
â†“
Risk Policy
â†“
Execution

`ActiveObservationTimeline` never leaves the Behavior Observation Window.
`FrozenBehaviorTimeline` is immutable, and Evidence Modules never mutate either
timeline. Observation Policy manages observation duration only. Decision Policy
interprets evidence only. Risk Policy manages capital only.

Rule #16: Observations are persisted at the point of creation. Persistent
repositories—not runtime registries—are the source of truth. Runtime caches may
exist only as performance optimizations.

Rule #17: QuantForge separates Market Reality, Behavioral Reality, Scientific
Reality, and Operational Reality. Information flows downward only.

===========================================================
TEMPORAL ONTOLOGY — SPRINT 2.1
===========================================================

Status: Implemented immutable domain model only. No Observation Policy, Behavior
Observation Window, replay, evidence algorithm, decision, risk, or execution
behavior is included.

`EnvironmentSnapshot` is immutable Market Reality and retains an opaque supplied
market payload. `BehaviorFrame` is one immutable categorical behavioral fact
linked to a snapshot. `ActiveObservationTimeline` is the sole mutable temporal
object: it collects caller-ordered frames. `freeze()` converts it to the
canonical immutable `FrozenBehaviorTimeline`. `TimelineRepositoryContract`
defines future persistent storage only; it has no implementation in this sprint.

Mutable Builder
â†“
Immutable Timeline

`FrozenBehaviorTimeline` is the canonical temporal object of the Behavior
Domain. It can be supplied unchanged to future Observation Policies and replay
tools. Neither detectors nor Evidence Modules may mutate a timeline.

===========================================================
OBSERVATION POLICY — SPRINT 2.2
===========================================================

Status: Implemented. The Observation Policy answers one question: "Should
observation continue?" It does not interpret behavior, evaluate evidence,
or produce decisions. It controls the observation window lifecycle only.

Dependency graph

ObservationConfig (external JSON)
↓
ObservationPolicyContract
↓
The Behavior Observation Window (Sprint 2.3) will consume
ObservationPolicyContract without knowing which policy implementation
is active. Future adaptive policies (Market DNA–driven) can implement
the contract without modifying existing components.

===========================================================
SPRINT 2.2.5 UPDATE — INFRASTRUCTURE COMPLETION
===========================================================

Sprint 2.2.5 introduced:

• EnvironmentRepositoryContract
• InMemoryEnvironmentRepository
• TimelineRepository implementation
• Shared TerminationReason contract
• Deterministic Observation Policy

These complete the infrastructure required before the Behavior Observation Window.

DefaultObservationPolicy terminates when the configured maximum frame
count or maximum duration is reached. Frame count has deterministic
priority over duration.

ObservationDecision is an immutable result containing continue/terminate
state, termination reason, policy identity, and timestamp. Allowed
termination reasons are: WINDOW_COMPLETE, MAX_DURATION,
POLICY_TERMINATED, CANDIDATE_INVALIDATED, UNKNOWN.

ObservationConfig is loaded from external JSON and is immutable. It
contains schema_version, max_frames, and max_duration. No hardcoded
business rules.

ObservationPolicyFactory constructs policies by stable name without
reflection, plugins, or registry loading. Currently supports "default"
only.

Observation Policy is strictly independent from Decision Policy
(evidence interpretation) and Risk Policy (capital allocation).

===========================================================
SPRINT 2.3 UPDATE — BEHAVIOR OBSERVATION WINDOW
===========================================================

Sprint 2.3 is COMPLETE. The Behavior Observation Window (BOW) is now the canonical temporal runtime component.

The BOW functions strictly as a deterministic collector:
• opens observation windows
• accepts immutable EnvironmentSnapshots
• internally constructs immutable BehaviorFrames
• appends into ActiveObservationTimeline
• consults ObservationPolicy
• freezes into FrozenBehaviorTimeline
• returns immutable BOWResult

The BOW explicitly performs NO:
• detector logic
• recoil logic
• persistence logic
• hypothesis logic
• execution
• risk
• Market DNA
===========================================================
SPRINT 2.4 UPDATE — REPLAY ENGINE
===========================================================

Replay Engine v1.0 is now frozen.

The Replay Engine is the canonical deterministic playback engine. It encapsulates the `ReplayEngineContract` and provides a strict, immutable playback sequence.

**Responsibilities & Lifecycle Sequence:**
• The Replay Engine loads a `FrozenBehaviorTimeline`.
• It initializes playback via `start()`.
• It iterates chronologically (`step()`, `replay_all()`), yielding a `ReplayCursor` containing the current immutable `BehaviorFrame` and resolving the corresponding `EnvironmentSnapshot` from the `EnvironmentRepositoryContract`.
• Upon completion, `finish()` yields an immutable `ReplayResult`.
• It safely supports `restart()`.

**Boundaries & Restrictions:**
The Replay Engine guarantees deterministic replay without mutation. It exclusively relies upon `TimelineRepositoryContract` and `EnvironmentRepositoryContract` dependencies.

Replay explicitly performs NO:
• Behavior detection or observation
• Recoil validation
• Persistence logic
• Hypothesis logic
• Execution
• Risk
• Market DNA

All internal states (`ReplayState`) and structural boundary issues map to the deterministic `ReplayError` hierarchy.

===========================================================
PHASE 2 ARCHITECTURE FREEZE
===========================================================

Phase 2 is now considered COMPLETE.

**Temporal Behaviour Infrastructure Components:**
• Environment Repository
• Timeline Repository
• Behavior Observation Window
• Observation Policy
• Replay Engine
• Temporal Ontology

These six components together form the Temporal Behaviour Infrastructure.

**Official Phase 2 Data Flow:**
Market
↓
EnvironmentSnapshot
↓
BehaviorObservation
↓
Candidate
↓
Behavior Observation Window
↓
ActiveObservationTimeline
↓
FrozenBehaviorTimeline
↓
Replay Engine
↓
Evidence Modules
↓
Hypothesis Engine

Phase 2 establishes deterministic behavioural time.

===========================================================
ARCHITECTURAL RULES (19-22)
===========================================================

**Rule #19**
**Phase Freeze Rule**
After every completed architectural phase an independent architecture review is mandatory.
No development may begin on the next phase until:
• audit passes
• documentation updated
• architecture frozen

**Rule #20**
**Documentation Synchronisation Rule**
Documentation is considered part of the architecture.
Every completed sprint requires documentation updates before the next sprint begins.
Code is never considered complete until documentation is synchronised.

**Rule #21**
**Scientific Integrity Rule**
Architecture decisions may never be changed because they are easier to code.
Scientific correctness always overrides implementation convenience.

**Rule #22**
**Technical Debt Rule**
Known technical debt must always be explicitly documented.
It is never hidden.
Accepted debt is recorded together with:
• reason
• impact
• future mitigation phase

===========================================================
PHASE 2 INDEPENDENT ARCHITECTURE REVIEW
===========================================================

**Architecture Score:** 92/100
**Status:** APPROVED
**Ready for Phase 3**

**Strengths**
- deterministic replay
- immutable timelines
- policy separation
- contract-first architecture
- downward dependency flow

**Weaknesses**
- repository transactional boundary
- directory fragmentation

**Overengineering observations**
- Candidate vs BehaviorObservation remains acceptable
- no action required

**Future optimisation**
- replay batch loading
- repository transactions

===========================================================
TECHNICAL DEBT REGISTER
===========================================================

**TD-001**
**Title:** Cross Repository Transaction Boundary
**Description:** TimelineRepository and EnvironmentRepository currently persist independently.
**Risk:** Partial persistence may create orphaned timeline references.
**Current Status:** Accepted.
**Resolution Phase:** Future infrastructure phase.

---------------------------------------------------------
PHASE 2 ARCHITECTURE FREEZE (Final Audit Update)
---------------------------------------------------------

The following components are marked as Frozen:
- Behavior Detector
- Candidate Manager
- Validator Framework
- Hypothesis Engine
- Experiment Ledger
- Temporal Ontology
- Observation Policy
- Behavior Observation Window
- Replay Engine

These components are now considered stable architectural foundations.
Future work may extend them but must not change their public contracts without a major architecture revision.

---------------------------------------------------------
PHASE 2 REVIEW SUMMARY
---------------------------------------------------------

**Architecture Score:** 92/100

**Strengths**
- deterministic architecture
- immutable ontology
- replayability
- contract-driven design
- strict domain boundaries

**Approved observations**
- Repository separation remains intentional.
- Replay Engine remains read-only.
- Candidate and BehaviorObservation remain separate.

**Known architectural debt**
- transactional UnitOfWork deferred to persistence phase
- replay batch loading deferred to production optimisation
- module consolidation deferred until architecture freeze of later phases

These are accepted engineering trade-offs, not defects.

---------------------------------------------------------
RULE #19 (Amended)
---------------------------------------------------------

**Rule #19**
Every completed phase must satisfy the following gate before development proceeds.

Implementation Complete
↓
Independent Sprint Audit
↓
Documentation Synchronisation
↓
Architecture Review
↓
Architecture Freeze
↓
Next Phase

No implementation work may begin on the next phase before the previous phase is frozen.

===========================================================
PHASE 3: SCIENTIFIC EVIDENCE FRAMEWORK (Sprint 3.1)
===========================================================

Sprint 3.1 established the Evidence Framework.
We now possess the language of scientific evidence. 
Observers can now be implemented in future sprints using the `ObserverContract` to produce `Evidence` independently, preserving the absolute requirement that QuantForge remains a Scientific Operating System.

===========================================================
PHASE 3A - SCIENTIFIC OBSERVATION LAYER (FROZEN)
===========================================================

**Purpose**

QuantForge now contains a complete scientific observation layer.
The observation layer consists of five independent scientific instruments.
Each instrument analyses the same immutable replayed timeline.
Observers never communicate.
Observers never depend on each other.
Observers never consume another Observer's Evidence.
Observers never perform interpretation.
Observers never perform aggregation.
Observers never perform decision making.
Observers only produce immutable scientific evidence.

**Architecture**

FrozenBehaviorTimeline
        │
        ├──► Recoil Observer
        ├──► Persistence Observer
        ├──► Failure Observer
        ├──► Velocity Observer
        └──► Compression Observer

Each observer returns immutable Evidence.
No observer mutates the replay.
No observer owns runtime state.

Phase 3B begins with Evidence Package.

**Rule #23 (Evidence Independence Rule)**
- Observers never know other observers exist.
- Every Observer analyses ONLY the immutable FrozenBehaviorTimeline.
- Observers communicate ONLY through immutable Evidence objects.
- No Observer may read another Observer's output.

**Evidence Framework Components:**
- `EvidenceContract`: Abstract boundary for scientific evidence.
- `Evidence`: Immutable dataclass containing only abstract information (confidence, labels). It absolutely prohibits indicator values, trading decisions, risk logic, or execution directives.
- `EvidencePackage`: Immutable aggregate holding a collection of `Evidence` for a specific candidate/timeline without interpreting it.
- `ObserverContract`: Abstract base class that all future Observers must implement, guaranteeing independent analysis of `FrozenBehaviorTimeline`.


=========================================================
ARCHITECTURAL EVOLUTION: SCIENTIFIC OPERATING SYSTEM
=========================================================

QuantForge separates:

Scientific Discovery
↓
Cross-Market Validation
↓
Trading Deployment

Deployment is not considered successful until behavioural hypotheses have demonstrated robustness across multiple markets.


=========================================================
SPRINT 3.8 FREEZE: BEHAVIOUR PROFILE ENGINE
=========================================================

**Purpose & Responsibilities:**
The Behaviour Profile Engine transforms an immutable EvidencePackage into an immutable BehaviourProfile. 
It exists solely to provide descriptive insights into observed behavioural characteristics and traits.

**Explicit Constraints:**
- A Behaviour Profile DESCRIBES behaviour.
- It does NOT interpret, predict, score, rank, generate confidence, generate probability, produce signals, or generate decisions.

**Architectural Boundaries & Immutability:**
- Extensible through a stateless builder pattern allowing new BehaviourDescriptor functions.
- 100% Immutable and Deterministic: All outputs are frozen dataclasses containing strictly sorted tuples to guarantee flawless replay hashing.
- **Dependencies:** The Engine depends ONLY upon EvidencePackage, immutable contracts, and primitive python typings. It strictly forbids Replay Engine, Policy, or Interpretation imports.


=========================================================
SPRINT 3.8 — BEHAVIOUR PROFILE ENGINE
=========================================================

**Purpose & Responsibilities:**
The Behaviour Profile Engine transforms an immutable EvidencePackage into a BehaviourProfile. It serves exclusively to aggregate and describe the observed behavioural traits.

**Inputs & Outputs:**
- Input: EvidencePackage ONLY.
- Output: BehaviourProfile ONLY.

**Dependency Boundaries:**
- The engine depends strictly on EvidencePackage, identifiers, and core typings. It forbids imports from Replay Engine, Interpretation, Decision, or Risk.

**Immutability & Determinism:**
- All outputs are immutable dataclasses containing sorted tuples to guarantee flawless determinism and deterministic hashing.

**FROZEN ARCHITECTURAL RULE:**
BehaviourProfile DESCRIBES behaviour only.
It MUST NOT:
- interpret
- predict
- score
- rank
- estimate confidence
- estimate probability
- generate signals
- generate decisions


=========================================================
SPRINT 3.9 — INTERPRETATION REGISTRY & MODEL FREEZE
=========================================================

**Purpose & Responsibilities:**
The Interpretation Registry introduces a pluggable scientific interpretation layer between Behaviour Profiles and future Decision Policies. The Registry purely selects and manages models. The Models convert an immutable BehaviourProfile into an immutable Interpretation.

**Inputs & Outputs:**
- Input: BehaviourProfile (consumed by Models).
- Output: Interpretation (produced by Models).

**Dependency Boundaries:**
- The Interpretation Registry and Models depend ONLY upon BehaviourProfile, immutable contracts, identifiers, and enums.

**Registry & Model Architecture:**
- **Open/Closed Principle:** New Interpretation Models can be seamlessly added and registered without modifying existing registry logic.
- **Immutability & Determinism:** Interpretations are strictly immutable dataclasses. Registry configurations are immutable post-initialisation. Model resolution and selection is perfectly deterministic.

**FROZEN ARCHITECTURAL RULES:**
- Interpretation Registry manages interpretation models ONLY.
- Interpretation Models perform scientific interpretation ONLY.
- Neither component may:
  - generate decisions
  - generate signals
  - estimate confidence
  - estimate probability
  - interact with risk
  - interact with execution
  - interact with brokers

Sprint 3.9 is now frozen. Future modifications must preserve:
- registry/model separation
- deterministic model selection
- immutable interpretations
- pluggable interpretation models
- downward dependency flow


=========================================================
SPRINT 3.10 — DECISION POLICY
=========================================================

**Purpose & Responsibilities:**
The Decision Policy acts as the first layer allowed to answer "Should this interpretation be acted upon?". It serves as the definitive boundary where scientific interpretation stops and actionable decision-making begins.

**Inputs & Outputs:**
- Input: `Interpretation` ONLY.
- Output: `Decision` ONLY (e.g., ACCEPT, REJECT, REQUIRE_MORE_EVIDENCE).

**Dependency Boundaries:**
- The Decision Policy depends strictly upon Interpretation, immutable contracts, enums, and identifiers. It forbids any dependency on Risk, Execution, or Broker logic.

**Immutability & Determinism:**
- The `Decision` object is a perfectly immutable dataclass. Evaluation logic is perfectly deterministic and replay-safe.

**FROZEN ARCHITECTURAL RULES:**
Decision Policy determines:
Interpretation
↓
Decision

It NEVER:
- executes
- sizes positions
- interacts with brokers
- calculates risk


=========================================================
SPRINT 3.11 — DECISION REGISTRY
=========================================================

**Purpose & Responsibilities:**
The Decision Registry acts as a centralized orchestrator to manage and resolve Decision Policies. It provides a pluggable composition boundary for the decision phase.

**Dependency Boundaries:**
- The Decision Registry depends ONLY on `DecisionPolicyContract`, `Interpretation`, and native types.

**Registry Architecture & Policy Management:**
- The architecture preserves the Open/Closed Principle, allowing robust injection of new policies without mutating registry code.
- Policy lifecycles, configuration mappings, and duplicate protections are entirely handled within the registry.

**Immutability & Determinism:**
- The registry explicitly avoids singleton/global mutable states. `registered_policies` ensures deterministic resolution via strictly sorted tuples.

**FROZEN ARCHITECTURAL RULES:**
- Decision Registry manages Decision Policies ONLY.
- It NEVER performs decision logic.


=========================================================
PHASE 3 FREEZE — SCIENTIFIC REASONING LAYER
=========================================================

**Purpose:**
Phase 3 formalizes the complete Scientific Reasoning Layer, locking the progression from raw market observations to definitive, non-execution decisions.

**Responsibilities & Architectural Boundaries:**
The architecture strictly enforces separation of concerns:
- **Evidence:** Aggregation of raw observer frames.
- **Behaviour Profile:** Descriptive behavioural facts.
- **Interpretation:** Assignment of scientific meaning (e.g., Mean Reversion Candidate).
- **Decision:** Actionability evaluation (ACCEPT, REJECT, DEFER).

**Dependency Flow:**
All data flows purely downwards. Each layer explicitly depends ONLY upon the output of the preceding layer and core immutable contracts. Upward dependencies and lateral leakage of execution or risk parameters are completely banned.

**Immutability & Determinism:**
Every core output across Phase 3 is a frozen dataclass containing only deterministic structures (sorted tuples, fixed identifiers). Non-deterministic functions are eradicated, ensuring perfect replay synchronization.

**FROZEN COMPLETE REASONING PIPELINE:**
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

**CRITICAL MANDATE:**
Science ends at Decision.
Risk begins in Phase 4.
Execution begins after Risk.


=========================================================
SPRINT 4.1 — RISK MODEL
=========================================================

**Purpose & Responsibilities:**
The Risk Model represents the first component of Phase 4. Its sole responsibility is to translate a scientific `Decision` into a set of structural capital exposure intents. 

**Dependency Boundaries:**
- Depends ONLY on `Decision` and immutable contracts.
- Strictly forbidden from depending on Execution, Broker integrations, or MT5 libraries.

**Immutability & Determinism:**
- The resulting `RiskProfile` is an aggressively validated, hashed, frozen dataclass. The generation is completely deterministic and stateless.

**FROZEN ARCHITECTURAL RULES:**
- Risk Model DESCRIBES capital exposure only.
- It performs NO monetary calculations (no lots, margin, SL/TP levels).
- Execution remains completely outside Phase 4.


=========================================================
SPRINT 4.2 — RISK POLICY
=========================================================

**Purpose & Responsibilities:**
The Risk Policy is the first component that evaluates whether a scientifically valid Decision may receive capital allocation. It evaluates the combination of a `Decision` and a `RiskModel` to determine the policy outcome.

**Inputs & Outputs:**
- Inputs: `Decision` and `RiskProfile` (from RiskModel)
- Output: `RiskPolicyEvaluation` (e.g., APPROVE, REJECT, REDUCE_EXPOSURE, REQUIRE_REVIEW)

**Dependency Boundaries:**
- Depends strictly on `Decision`, `RiskModel`, and pure contracts/enums. No upward dependencies.

**Immutability & Determinism:**
- The configuration and evaluation outputs are aggressively validated frozen dataclasses with perfectly deterministic custom hashing algorithms.

**FROZEN ARCHITECTURAL RULES:**
- Risk Policy evaluates Decision and RiskModel ONLY.
- It performs NO position sizing.
- It performs NO execution.


=========================================================
SPRINT 4.3 — RISK POLICY REGISTRY
=========================================================

**Purpose & Responsibilities:**
The Risk Policy Registry acts as a centralized orchestrator to manage and resolve Risk Policies. It provides a pluggable composition boundary for the risk phase, identical to the interpretation phase.

**Dependency Boundaries:**
- The Risk Policy Registry depends ONLY on `RiskPolicyContract` and native types.

**Registry Architecture & Policy Management:**
- The architecture preserves the Open/Closed Principle, allowing robust injection of new risk policies (e.g. Retail, PropFirm) without mutating registry code.
- Policy lifecycles and duplicate protections are strictly handled within the registry.

**Immutability & Determinism:**
- The registry explicitly avoids singleton/global mutable states. `registered_policies` ensures deterministic resolution via strictly sorted tuples.

**FROZEN ARCHITECTURAL RULES:**
- Risk Policy Registry manages Risk Policies ONLY.
- It NEVER evaluates risk.


=========================================================
SPRINT 4.4 — RISK ASSESSMENT
=========================================================

**Purpose & Responsibilities:**
The Risk Assessment component captures the immutable outcome of the Risk Policy layer. It definitively records the capital allocation outcome in a purely structural format without executing numerical sizing logic.

**Dependency Boundaries:**
- RiskAssessment strictly consumes the output of Risk Policy (`RiskPolicyEvaluation`). It explicitly prohibits any linkage to broker integration or monetary computation.

**Immutability & Determinism:**
- Built as a `@dataclass(frozen=True)`, the RiskAssessment maintains rigorous referential transparency through custom mapping-proxy hashing.

**FROZEN ARCHITECTURAL RULES:**
- RiskAssessment is the immutable output of Risk Policy.
- It performs NO calculations.
- It performs NO execution.


=========================================================
SPRINT 4.5 — POSITION SIZER
=========================================================

**Purpose & Responsibilities:**
The PositionSizer converts an approved RiskAssessment into a deterministic sizing result suitable for the PositionPlan layer. It strictly evaluates sizing mechanics and abstract exposure allocations.

**Dependency Boundaries:**
- The PositionSizer exclusively consumes `RiskAssessment`. 

**Immutability & Determinism:**
- Evaluative mapping occurs via explicitly validated abstract classes and math without relying on underlying global states.

**FROZEN ARCHITECTURAL RULES:**
- PositionSizer performs deterministic sizing only.
- It performs NO execution.
- It performs NO broker interaction.


=========================================================
SPRINT 4.6 — POSITION SPECIFICATION
=========================================================

**Purpose & Responsibilities:**
PositionSpecification represents an immutable, execution-agnostic specification defining a future position. It acts as the final output boundary for Phase 4, packaging deterministic sizing results into a broker-independent payload.

**Dependency Boundaries:**
- The specification acts as a pure transport object derived entirely from the upstream `PositionSizer`. It strictly enforces zero dependencies on downstream broker execution mechanics.

**Immutability & Determinism:**
- Guaranteed to be completely replay-safe via rigid schema locking and mapping proxies.

**FROZEN ARCHITECTURAL RULES:**
- PositionSpecification is the immutable broker-independent output of PositionSizer.
- Execution natively consumes PositionSpecification.


=========================================================
PHASE 4 FREEZE: CAPITAL ALLOCATION LAYER
=========================================================

**Purpose & Responsibilities:**
The Capital Allocation Layer formalizes the abstract intent generated by the Scientific Reasoning layer into a deterministic, broker-independent physical exposure target. It manages risk profiling, policy enforcement, structural assessment, and abstract position scaling without ever linking to physical execution mechanics.

**Pipeline:**
Decision -> RiskModel -> RiskPolicyRegistry -> RiskPolicy -> RiskAssessment -> PositionSizer -> PositionSpecification

**Architectural Boundaries & Dependency Flow:**
- Strict downward dependency execution.
- Immutability and replay safety are mathematically guaranteed across all value objects.
- Broker integration remains 100% absent.

**FROZEN ARCHITECTURAL RULES:**
- Capital Allocation operates in complete abstraction from Execution logic.
- The pipeline yields only deterministic descriptions of intent (`PositionSpecification`).
- Execution mechanics (orders, fill calculations, margins) begin ONLY in Phase 5.


=========================================================
SPRINT 5.1 — EXECUTION ENGINE CONTRACT
=========================================================

**Purpose & Responsibilities:**
The Execution Engine Contract formally defines the boundary where deterministic capital allocation transitions into physical deployment. It strictly limits responsibilities to ingesting the immutable `PositionSpecification` and dispatching it to downstream execution adapters.

**Dependency Boundaries:**
- Consumes strictly `PositionSpecification` from Phase 4.
- Operates entirely ignorant of prior Scientific Reasoning or abstract Risk Profiling layers.

**Execution Boundary & Broker Independence:**
- The engine contract mandates absolute broker independence, meaning implementations for Python simulations or live MT5 deployments must utilize the identical interface structure.

**FROZEN ARCHITECTURAL RULES:**
- Execution begins here.
- Scientific reasoning and capital allocation remain complete before this boundary.


=========================================================
SPRINT 5.2 — BROKER ADAPTER CONTRACT
=========================================================

**Purpose & Responsibilities:**
The Broker Adapter Contract formalizes the abstraction layer shielding the deterministic `ExecutionEngine` from third-party broker implementations. It ensures uniform processing of `PositionSpecification` packets across vastly different execution environments (MT5, FIX, Simulation, Paper).

**Dependency Boundaries:**
- The `ExecutionEngine` strictly relies on this abstract contract rather than concrete broker API classes.

**Immutability & Determinism:**
- Adapter configurations utilize mapping proxies and frozen classes to guarantee routing metadata remains perfectly deterministic and tamper-proof.

**FROZEN ARCHITECTURAL RULES:**
- ExecutionEngine depends only on BrokerAdapterContract.
- Concrete brokers remain strictly isolated in downstream adapters.


=========================================================
SPRINT 5.3 — EXECUTION RESULT
=========================================================

**Purpose & Responsibilities:**
ExecutionResult represents the immutable outcome of an execution attempt. It formalizes the conclusion of the execution flow by logging the physical trade attempt into a deterministic, broker-agnostic abstraction.

**Dependency Boundaries:**
- Relies solely on native enumerations (`ExecutionStatus`) and generic mapping configurations.
- Operates in total isolation from vendor APIs and network mechanics.

**Immutability & Broker Independence:**
- Completely replay-safe and heavily validated during instantiation to block runtime mutability.

**FROZEN ARCHITECTURAL RULES:**
- ExecutionResult is the immutable broker-independent outcome of execution.


=========================================================
SPRINT 5.4 — EXECUTION ENGINE
=========================================================

**Purpose & Responsibilities:**
The ExecutionEngine is the central broker-independent orchestrator for Phase 5. It manages the translation of abstract capital targets into physical realities by routing immutable specifications downward into isolated broker adapters.

**Dependency Boundaries:**
- The Engine explicitly consumes only `PositionSpecification` and exclusively relies upon `BrokerAdapterContract` to perform physical tasks.

**Orchestration Role & Broker Independence:**
- The engine operates purely as a structural traffic cop. It performs zero mathematical evaluations or trade-size recalculations.

**FROZEN ARCHITECTURAL RULES:**
- ExecutionEngine orchestrates execution only.
- ExecutionEngine delegates to BrokerAdapterContract.
- ExecutionEngine never contains broker-specific logic.


=========================================================
SPRINT 5.5 — MT5 TRANSPORT
=========================================================

**Purpose & Responsibilities:**
The MT5 Transport layer is the exclusive module permitted to interact with the MetaTrader5 Python SDK. It encapsulates raw network sockets and vendor APIs behind a deterministic, predictable boundary. 

**Dependency Boundaries & SDK Isolation:**
- MetaTrader5 imports are tightly sandboxed within `DefaultMT5Transport`.
- Zero vendor objects (e.g., `OrderSendResult`) are permitted to cross the return boundary. All SDK artifacts are shredded and converted into primitive Python dictionaries.

**FROZEN ARCHITECTURAL RULES:**
- MetaTrader5 SDK interaction exists ONLY inside MT5Transport.
- No SDK objects leave the transport boundary.


=========================================================
SPRINT 5.6 — MT5 ADAPTER
=========================================================

**Purpose & Responsibilities:**
The MT5 Adapter serves purely as a translation module. It converts abstract QuantForge `PositionSpecification` vectors into basic dictionary strings, and wraps physical transport responses back into immutable `ExecutionResult` dataclasses.

**Dependency Boundaries & Transport Dependency:**
- The Adapter strictly depends upon `BrokerAdapterContract` (upstream) and `MT5TransportContract` (downstream). 
- It actively forbids any evaluation of scientific trading logic or risk recalculations.

**FROZEN ARCHITECTURAL RULES:**
- MT5Adapter translates QuantForge execution requests into MT5 transport operations.
- MT5Adapter never communicates directly with the MetaTrader5 SDK.


=========================================================
SPRINT 5.7 — PYTHON SIMULATION ADAPTER
=========================================================

**Purpose & Responsibilities:**
The PythonSimulationAdapter provides a strictly deterministic, offline execution engine for backtesting, research, and batch replay workflows. It simulates physical market conditions without invoking any network state.

**Dependency Boundaries & Deterministic Simulation:**
- Safely implements `BrokerAdapterContract`.
- Entirely broker-independent; relies on zero external SDKs, APIs, or data sockets.

**FROZEN ARCHITECTURAL RULES:**
- PythonSimulationAdapter implements BrokerAdapterContract for deterministic research and replay.


=========================================================
SPRINT 5.8 — PAPER TRADING ADAPTER
=========================================================

**Purpose & Responsibilities:**
The PaperTradingAdapter provides a deterministic, continuous virtual brokerage account. It behaves indistinguishably from a live market connection, maintaining persistent ledger state (balance, open positions) without invoking network operations.

**Dependency Boundaries & Virtual Account Management:**
- Operates entirely as a stateful ledger engine.
- Implements `BrokerAdapterContract` transparently to upstream orchestrators.
- Absolute broker independence guarantees zero physical API leakage.

**FROZEN ARCHITECTURAL RULES:**
- PaperTradingAdapter implements BrokerAdapterContract and provides deterministic virtual execution using an internal paper account.


=========================================================
PHASE 5 FROZEN
=========================================================

**Execution Infrastructure Completed:**
The Execution Infrastructure consists of:
- ExecutionEngine
- BrokerAdapterContract
- MT5Transport
- MT5Adapter
- PythonSimulationAdapter
- PaperTradingAdapter

**FROZEN ARCHITECTURAL RULES:**
- Execution begins ONLY after PositionSpecification.
- Execution remains entirely broker-independent through adapters.


=========================================================
SPRINT 6.1 — HYPOTHESIS CONTRACT
=========================================================

**Purpose & Scientific Role:**
The Hypothesis Contract initiates the Scientific Validation domain. It establishes a formal, strictly declarative structure for researchers to propose scientific claims regarding market behavior.

**Immutable Design & Runtime Isolation:**
- Implemented as a strictly frozen dataclass.
- Wholly isolated from the core trading engine; it possesses zero capability to execute logic, parse market telemetry, or adjust risk parameters.

**FROZEN ARCHITECTURAL RULES:**
- Hypothesis represents a scientific claim only and is not part of the QuantForge execution runtime.


=========================================================
SPRINT 6.2 — EXPERIMENT CONTRACT
=========================================================

**Purpose & Scientific Role:**
The Experiment Contract establishes the formal specification for testing a scientific Hypothesis. It dictates exactly what markets, configurations, and analysis periods will be evaluated.

**Immutable Design & Relationship to Hypothesis:**
- The Experiment maps to a Hypothesis strictly via a string identifier (`hypothesis_identifier`) to guarantee loose coupling.
- It intercepts mutable data structures and deep-freezes them (tuples of tuples) to ensure absolute test repeatability.

**FROZEN ARCHITECTURAL RULES:**
- Experiment defines a reproducible scientific test.
- It never executes or validates.


=========================================================
SPRINT 6.3 — VALIDATION CONTRACT
=========================================================

**Purpose & Scientific Role:**
The Validation Contract serves as the final immutable scientific conclusion of an Experiment.

**Immutable Design & Relationship to Experiment:**
- It relates directly to a prior Experiment via a loose string coupling (`experiment_identifier`).
- Designed as a strictly frozen data structure containing only the outcome state.

**FROZEN ARCHITECTURAL RULES:**
- Validation represents the immutable scientific conclusion of an Experiment.
- It contains no statistical logic and performs no calculations.


=========================================================
PHASE 6 — SCIENTIFIC VALIDATION (FROZEN)
=========================================================

**Purpose & Domain Boundaries:**
Phase 6 officially introduces the Scientific Validation domain. This acts as a pre-runtime research layer that governs how scientific claims are structured, tested, and concluded.

**Lifecycle Orchestration:**
The formal sequence orchestrated by this domain is:
Hypothesis
↓
Experiment
↓
Validation

**Architectural Integrity:**
Scientific Validation exists entirely outside the QuantForge execution runtime. It produces validated scientific artefacts that are consumed by future Interpretation Models, but it does NOT perform market execution or active statistical computations itself.


# Phase 6 Frozen

Scientific Validation consists of
- Hypothesis
- Experiment
- Validation
- Validation Service

Its purpose is to transform scientific claims into validated scientific conclusions.
It remains completely isolated from the QuantForge runtime.

=========================================================
SPRINT 7.1 — STRATEGY ASSEMBLY CONTRACTS
=========================================================

### Purpose
Strategy Assembly acts as a declarative composition layer. It binds together the validated outputs of the scientific process (Validation, Interpretation Model, Decision Policy, Risk Policy) into an executable Strategy.

### Lifecycle
A Strategy follows a strict lifecycle: DRAFT -> READY -> PAPER -> DEMO -> LIVE -> RETIRED.

### Immutable Design
A Strategy is an immutable composition of validated scientific components.
It contains no execution logic.

=========================================================
SPRINT 7.2 & 7.3 — DEPLOYMENT LAYER (FROZEN)
=========================================================

### Purpose
The Deployment Layer officially initiates the Deployment Era. It wires validated scientific research (StrategyManifest) into an orchestrated, deployable runtime pipeline without introducing state or execution logic.

### Components
- **DeploymentContext**: An immutable dataclass storing strictly validated references to the pipeline's exact components (`StrategyContract`, `InterpretationModelContract`, `DecisionPolicyContract`, `RiskPolicyContract`). Contains NO market data, runtime state, or execution profile.
- **DeploymentAssembler**: Safely resolves the abstract `StrategyManifest` against domain registries and deterministically produces the `DeploymentRuntime`.
- **DeploymentRuntime**: A read-only shell wrapping the `DeploymentContext`. It exposes the assembled scientific pipeline but explicitly owns NO broker integrations, event loops, execution orchestration, or portfolio state.
- **DeploymentOrchestrator**: Coordinates the full BOE pipeline per EnvironmentSnapshot. It maintains no internal state. It routes data perfectly sequentially from observation through to risk calculation.

### Architectural Constraint
DeploymentOrchestrator coordinates the BOE pipeline.
It terminates at PositionSpecification.
Execution remains exclusively within the Execution Domain.

=========================================================
SPRINT 7.4 — LIVE MARKET ADAPTER (FROZEN)
=========================================================

### Purpose
The MarketDataAdapter acts as the exclusive boundary between external market feeds (MT5, Interactive Brokers, CSV Replay, etc.) and QuantForge. It isolates the BOE pipeline from raw vendor APIs.

### Components
- **MarketDataAdapterContract**: An abstract contract defining the translation boundary.
- **GenericMarketDataAdapter**: Translates generic external ticks/bars into a fully populated, immutable `EnvironmentSnapshot`.

### Architectural Constraint
The Market Adapter performs translation only. It produces immutable `EnvironmentSnapshots` and explicitly contains no trading logic, no interpretation, no signals, no decisions, and no execution. Time originates strictly from incoming market data.

=========================================================
SPRINT 7.5 — PAPER TRADING RUNNER (FROZEN)
=========================================================

### Purpose
The Paper Trading Runner coordinates execution of the Deployment Orchestrator over a stream of EnvironmentSnapshots, targeting the Simulation Execution Adapter.

### Components
- **PaperTradingRunner**: Sequentially drives `EnvironmentSnapshots` into the `DeploymentOrchestrator` and forwards resulting `PositionSpecifications` to the `ExecutionEngineContract`.
- **RunnerResult**: Deterministic structured output containing execution results or errors for individual snapshots.

### Architectural Constraint
The Paper Trading Runner owns execution flow only. It contains NO market logic, NO scientific reasoning, and NO broker retry logic. Failures produce deterministic results rather than terminating the session.

=========================================================
SPRINT 7.6 — DEPLOYMENT BOOTSTRAP (FROZEN)
=========================================================

### Purpose
The Deployment Bootstrap serves as the application entry point, wiring together the fully completed deployment components into an executable pipeline.

### Components
- **DeploymentBootstrap**: Factory exposing a deterministic `create()` method that assembles the `DeployedPipeline`.
- **DeployedPipeline**: The fully initialized integration of the Market Adapter and Paper Trading Runner.

### Architectural Constraint
The Bootstrap performs construction only. It owns NO scientific logic, NO market logic, and NO runtime logic. Its sole responsibility is dependency injection and structural assembly.

=========================================================
PHASE 7 FREEZE WARNING
=========================================================
**The Deployment Layer is completely FROZEN.** 
No modifications may be made to the Deployment Layer without formal architectural review. The project has fully assembled the research deployment runtime.

=========================================================
CANONICAL DEPLOYMENT PIPELINE (PHASE 7)
=========================================================
The execution path for deployed research is strictly ordered as follows:

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

===========================================================
PHASE 8.1 — RESEARCH CANDIDATE & STRATEGY MANIFEST
===========================================================

Phase 8.1 introduces the constitutional entry point of the scientific
lifecycle. It creates the immutable objects required to represent:

    Research Idea → ResearchCandidate → StrategyManifest

This sprint does not create a strategy. It creates the immutable object
that represents a research hypothesis moving through QuantForge.

Package Location: research/lifecycle/

This package lives outside the frozen boe/ tree. Phase 8 is an operational
extension — it consumes the frozen platform but does not modify it.

Components:

ResearchCandidate (research/lifecycle/research_candidate.py)
    Immutable frozen dataclass representing one behavioural hypothesis.
    Contains: candidate_id, hypothesis_id, research_name, behaviour_name,
    description, creation_timestamp, research_version, assumptions,
    success_criteria, metadata.
    Contains NO: runtime state, execution, results, statistics, broker info.

Provenance (research/lifecycle/provenance.py)
    Immutable frozen dataclass tracking scientific reproducibility.
    Tracks: originating ResearchCandidate, ValidationResult,
    ExperimentRecord, and StrategyManifest.

StrategyManifest (research/lifecycle/strategy_manifest.py)
    Immutable frozen dataclass representing one validated behaviour ready
    for deployment. Contains references only — never logic.
    Fields: strategy_id, behaviour_name, observer_ids,
    interpretation_model_id, decision_policy_id, risk_policy_id,
    deployment_profile, manifest_version, provenance.

StrategyManifestBuilder (research/lifecycle/strategy_manifest_builder.py)
    Deterministic builder that transitions:
    ResearchCandidate → Validated Behaviour → StrategyManifest
    Performs structural validation. Never creates scientific decisions.

Dependency Graph:

ResearchCandidate
        ↓
StrategyManifestBuilder (accepts validation + component references)
        ↓
Provenance + StrategyManifest
        ↓
Frozen Phase 7 Deployment Layer (consumer)

Relationship to Frozen BOE:
Phase 8.1 objects consume the frozen platform. They do not modify the BOE,
the frozen public contracts, or the deployment layer. The StrategyManifest
is designed to be consumed by the existing DeploymentAssembler.

