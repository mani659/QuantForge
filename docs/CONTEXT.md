# QuantForge Context
Version: 1.0
Status: Active Development
Last Updated: 2026-07-15

# QuantForge Context
Version: 1.0
Status: Active Development
Last Updated: 2026-07-15

===========================================================
PROJECT VISION
===========================================================

QuantForge is a research-driven quantitative trading platform.

The objective is NOT to build another indicator-based EA.

Its purpose is to repeatedly convert validated market behaviour into profitable 
automated trading systems through a disciplined, reproducible research-to-deployment pipeline.

Over time, QuantForge becomes a compounding body of scientific market knowledge — 
not merely a collection of trading strategies.

Final Deliverables

• Deployed Validated Trading Systems (MT5/Python)
• Continuous Market Feedback Loop
• Cross-market behavioural research database

===========================================================
PRIMARY DEVELOPMENT PRINCIPLE
===========================================================

Every module must increase the probability of building a better Adaptive EA.

If a feature does not directly contribute toward the Adaptive EA,
it is postponed.

Avoid over-engineering.

Research supports development.

Documentation supports development.

Development is always the priority.

===========================================================
CURRENT PROJECT STATUS
===========================================================

QuantForge Core is complete.

The Scientific Operating System is frozen.

Phases 1–7 — Observation, Evidence, Behaviour Profile, Interpretation,
Decision, Risk, Execution, Scientific Validation, Strategy Assembly, and the
Deployment Layer — are permanently frozen. The Behavioral Observation Engine
(BOE) is the only canonical architecture, with information flowing downward
only.

Current effort focuses on transforming validated behavioural research into
continuously deployable strategies.

Phase 8 (Research Industrialization) is COMPLETE. Sprints 8.1, 8.2, and 8.3
extend the platform operationally rather than architecturally: they close the
Research → Validation → Deployment → Feedback loop without modifying any frozen
scientific domain. The automated pipeline now terminates at the read-only
`OutcomeReader` service; Human Research Review is outside QuantForge software.

Future work extends the platform operationally rather than architecturally.

===========================================================
NOTES
===========================================================

QuantForge is not intended to become another indicator collection.

The project exists to transform statistically validated market behaviour
into an adaptive quantitative trading engine.

Every architectural decision must support that objective.

===========================================================
END OF CONTEXT
===========================================================

===========================================================
ARCHITECTURE FREEZE UPDATE — JULY 2026
===========================================================

The project is now officially described as a **Scientific Operating System for
Market Research and Behavioral Trading**. The earlier “research-driven
quantitative trading platform” language is retained as historical project
context; it is superseded by the frozen four-layer architecture in
`ARCHITECTURE.md`.

The current architectural direction is Market Reality → Behavioral Reality →
Scientific Reality → Operational Reality, with information flowing downward
only. Temporal observation, scientific replay, and durable experiment provenance
are first-class future capabilities.

===========================================================
SPRINT 2.2 UPDATE — OBSERVATION POLICY
===========================================================

Sprint 2.2 delivered the Observation Policy architecture within the Behavior
Domain. The Observation Policy answers one question: "Should observation
continue?" It does not interpret behavior, evaluate evidence, or produce
trading decisions.

Delivered components:

✔ ObservationPolicyContract (abstract boundary)
✔ DefaultObservationPolicy (deterministic lifecycle control)
✔ ObservationConfig (immutable external configuration)
✔ ObservationDecision (immutable result contract)
✔ ObservationPolicyFactory (deterministic named construction)
✔ Observation error hierarchy
✔ 33 deterministic unit tests

The Behavior Observation Window (Sprint 2.3) will consume
ObservationPolicyContract without knowing which policy implementation
is active. Future adaptive policies (Market DNA–driven) can implement
the contract without modifying existing components.

===========================================================
SPRINT 2.2.5 UPDATE — INFRASTRUCTURE COMPLETION
===========================================================

Sprint 2.2.5 is frozen.

Sprint 2.3 completed.

Current active milestone:
Sprint 2.4
Replay Engine

Sprint 2.4 completed.

Replay subsystem frozen.

Replay is now the canonical deterministic playback engine.

Future observers will consume replay output.

Replay never performs:
* Observation
* Validation
* Decision
* Risk
* Execution

===========================================================
CURRENT ARCHITECTURE BASELINE
===========================================================

**Version:**
Phase 2 Frozen

**State:**
Approved after independent architecture review.

Future development begins from this baseline.

Current Project State

Phase 2 Frozen

The scientific observation foundation is complete.
Future development begins at Phase 3.
The architecture is now considered stable.

Current Development Status
Phase 3A completed.
Observation Layer frozen.
Next development target
Evidence Package
Behaviour Profile
Interpretation
Decision Policy

===========================================================
SPRINT 3.1 UPDATE — EVIDENCE FRAMEWORK
===========================================================

Sprint 3.1 established the Evidence Framework.
We now possess the language of scientific evidence. 
Observers can now be implemented in future sprints using the `ObserverContract` to produce `Evidence` independently, preserving the absolute requirement that QuantForge remains a Scientific Operating System.

===========================================================
PROJECT STATUS
===========================================================

Current completion
Phase 1
COMPLETE
Phase 2
COMPLETE
Phase 3A
COMPLETE
Phase 3B
IN PROGRESS

Overall project completion
Approximately 55%


=========================================================
ARCHITECTURAL EVOLUTION: SCIENTIFIC OPERATING SYSTEM
=========================================================

The long-term objective is not a single profitable EA.
The long-term objective is a reusable behavioural research platform capable of validating and deploying scientific market hypotheses across multiple asset classes.

Trading engines are products generated from validated research.


=========================================================
SPRINT 3.8 FREEZE: BEHAVIOUR PROFILE ENGINE
=========================================================

**Sprint 3.8 Freeze Notice:**
The Behaviour Profile Engine (v1.0) has passed independent architecture audit and is now FROZEN.

**Architectural Decisions & Frozen Boundaries:**
- The Behaviour Profile domain operates purely as a descriptive aggregation layer. 
- All forms of prediction, probability, interpretation, scoring, and decision-making logic are explicitly banned from this layer. 
- The profile uses a stateless, deterministic builder function design, making it indefinitely extensible without mutating existing contracts.


=========================================================
SPRINT 3.8 FREEZE NOTICE
=========================================================

Sprint 3.8 (Behaviour Profile Engine) has officially PASSED the Independent Architecture Audit and is now FROZEN.

**Architectural Decisions & Frozen Boundaries:**
- Responsibilities: Behaviour Profile purely aggregates descriptive evidence traits without adding meaning or interpretation.
- Rule #26 Sprint Lifecycle Adoption: All sprints must rigorously follow the pipeline: Development -> Independent Audit -> Documentation Sync -> Architecture Freeze -> Next Sprint.


=========================================================
SPRINT 3.9 FREEZE NOTICE
=========================================================

Sprint 3.9 (Interpretation Registry & Interpretation Model) has officially PASSED the Independent Architecture Audit and is now FROZEN.

**Architectural Decisions & Frozen Boundaries:**
- Interpretation Registry introduced to exclusively manage model composition.
- Interpretation Models introduced to strictly map profiles to scientific conclusions.
- Registry/Model separation is permanently frozen.
- Open/Closed Principle rigorously enforced for future model injection.
- Scientific interpretation remains completely isolated from decision making.
- This architecture explicitly supports multiple interpretation models for future cross-market behavioural research.


=========================================================
SPRINT 3.10 FREEZE NOTICE
=========================================================

Sprint 3.10 (Decision Policy) has officially PASSED the Independent Architecture Audit and is now FROZEN.

**Architectural Decisions & Frozen Boundaries:**
- Decision boundary frozen: It evaluates actionability but never executes.
- Science ends here: The interpretation and decision generation concludes the scientific analysis phases of the pipeline.
- Risk begins next phase: No positional sizing or stop-loss variables exist within the Decision phase.


=========================================================
SPRINT 3.11 FREEZE NOTICE
=========================================================

Sprint 3.11 (Decision Registry) has officially PASSED the Independent Architecture Audit and is now FROZEN.

**Architectural Decisions & Frozen Boundaries:**
- Decision Registry introduced for strict lifecycle mapping of policies.
- Registry/Policy separation frozen: The orchestration layer never performs evaluation.
- Pluggable decision architecture is now completed.


=========================================================
PHASE 3 FREEZE NOTICE
=========================================================

The Scientific Reasoning Layer (Phase 3) has officially passed the final independent architecture review and is now FROZEN.

**Architectural Decisions & Scientific Boundaries:**
- The Registry architecture is formalized, isolating the composition logic from the analytical logic.
- The Decision boundary firmly establishes that scientific reasoning concludes upon the issuance of a Decision.
- Formal transition to Phase 4 (Risk Architecture) is APPROVED.


=========================================================
SPRINT 4.1 FREEZE NOTICE
=========================================================

Sprint 4.1 (Risk Model) has officially PASSED the Independent Architecture Audit and is now FROZEN.

**Architectural Decisions & Frozen Boundaries:**
- Risk begins: The pipeline transitions from scientific reasoning to structural exposure description.
- Execution still prohibited: No broker or trading logic exists.
- Scientific reasoning remains frozen and entirely isolated from risk definitions.


=========================================================
SPRINT 4.2 FREEZE NOTICE
=========================================================

Sprint 4.2 (Risk Policy) has officially PASSED the Independent Architecture Audit and is now FROZEN.

**Architectural Decisions & Frozen Boundaries:**
- Risk Policy introduced to evaluate policy acceptance of structural exposure.
- Capital allocation evaluation begins here.
- Position sizing explicitly remains future work.


=========================================================
SPRINT 4.3 FREEZE NOTICE
=========================================================

Sprint 4.3 (Risk Policy Registry) has officially PASSED the Independent Architecture Audit and is now FROZEN.

**Architectural Decisions & Frozen Boundaries:**
- Registry/Policy separation completed for the Risk Domain.
- Risk architecture remains entirely deterministic and immutable.
- Position sizing is explicitly not yet implemented and remains deferred.


=========================================================
SPRINT 4.4 FREEZE NOTICE
=========================================================

Sprint 4.4 (Risk Assessment) has officially PASSED the Independent Architecture Audit and is now FROZEN.

**Architectural Decisions & Frozen Boundaries:**
- RiskAssessment formally introduced to the pipeline.
- Capital allocation evaluation remains strictly descriptive.
- The separation between risk evaluation and mathematical position sizing is perfectly maintained.


=========================================================
SPRINT 4.5 FREEZE NOTICE
=========================================================

Sprint 4.5 (PositionSizer) has officially PASSED the Independent Architecture Audit and is now FROZEN.

**Architectural Decisions & Frozen Boundaries:**
- PositionSizer introduced to formalize mathematical exposure allocations.
- Deterministic sizing mechanics have been structurally established.
- Execution boundaries and broker interactions strictly remain outside of Phase 4 boundaries.


=========================================================
SPRINT 4.6 FREEZE NOTICE
=========================================================

Sprint 4.6 (PositionSpecification) has officially PASSED the Independent Architecture Audit and is now FROZEN.

**Architectural Decisions & Frozen Boundaries:**
- PositionSpecification formally introduced.
- Broker-independent execution contract established. Phase 4 successfully terminates with a pure data specification that subsequent deployment engines (MT5, FIX, Backtester) can consume safely.


=========================================================
PHASE 4 FREEZE NOTICE
=========================================================

Phase 4 (Capital Allocation Layer) has officially PASSED its comprehensive system-level Independent Architecture Review and is now FROZEN.

**Architectural Decisions & Frozen Boundaries:**
- Abstraction between scientific evaluation and capital assignment is fully established.
- The entire capital boundary terminates on `PositionSpecification`.
- Execution layers will inherit these data packets without violating previous pipeline strictures.


=========================================================
SPRINT 5.1 FREEZE NOTICE
=========================================================

Sprint 5.1 (Execution Engine Contract) has officially PASSED the Independent Architecture Audit and is now FROZEN.

**Architectural Decisions & Frozen Boundaries:**
- Execution boundary formally introduced.
- Broker independence perfectly preserved at the system ingress layer.
- Specific adapter implementations (MT5, Backtester) are structurally deferred.


=========================================================
SPRINT 5.2 FREEZE NOTICE
=========================================================

Sprint 5.2 (Broker Adapter Contract) has officially PASSED the Independent Architecture Audit and is now FROZEN.

**Architectural Decisions & Frozen Boundaries:**
- The broker abstraction layer has been officially introduced.
- Core execution logic remains permanently isolated from vendor-specific deployment code.
- Concrete adapter implementations have been deferred downstream.


=========================================================
SPRINT 5.3 FREEZE NOTICE
=========================================================

Sprint 5.3 (ExecutionResult) has officially PASSED the Independent Architecture Audit and is now FROZEN.

**Architectural Decisions & Frozen Boundaries:**
- The immutable execution outcome (`ExecutionResult`) has been fully established.
- Absolute broker independence has been secured at the return boundary, preventing SDK leakage during state transitions.


=========================================================
SPRINT 5.4 FREEZE NOTICE
=========================================================

Sprint 5.4 (Execution Engine) has officially PASSED the Independent Architecture Audit and is now FROZEN.

**Architectural Decisions & Frozen Boundaries:**
- Execution orchestration is strictly completed.
- Concrete broker implementations (MT5, FIX, Simulation) remain definitively deferred to their isolated plugins.


=========================================================
SPRINT 5.5 FREEZE NOTICE
=========================================================

Sprint 5.5 (MT5 Transport) has officially PASSED the Independent Architecture Audit and is now FROZEN.

**Architectural Decisions & Frozen Boundaries:**
- MT5 SDK has been completely isolated from the rest of the application.
- A pure transport layer has been introduced to intercept and cleanse network interactions.
- Future adapter implementations (Sprint 5.6) will remain insulated from raw SDK volatility.


=========================================================
SPRINT 5.6 FREEZE NOTICE
=========================================================

Sprint 5.6 (MT5 Adapter) has officially PASSED the Independent Architecture Audit and is now FROZEN.

**Architectural Decisions & Frozen Boundaries:**
- The first live-market adapter (MT5) has been fully introduced.
- The translation layer mapping abstract vectors to physical broker instructions is completed.
- Complete SDK isolation has been thoroughly preserved.


=========================================================
SPRINT 5.7 FREEZE NOTICE
=========================================================

Sprint 5.7 (Python Simulation Adapter) has officially PASSED the Independent Architecture Audit and is now FROZEN.

**Architectural Decisions & Frozen Boundaries:**
- A fully offline, mathematically deterministic simulation framework has been established.
- Replay and research architectures can now safely trigger executions without bleeding into live broker implementations.


=========================================================
SPRINT 5.8 FREEZE NOTICE
=========================================================

Sprint 5.8 (Paper Trading Adapter) has officially PASSED the Independent Architecture Audit and is now FROZEN.

**Architectural Decisions & Frozen Boundaries:**
- The virtual execution infrastructure is fully completed.
- A deterministic continuous paper account ledger has been established.
- The Execution Infrastructure phase is now feature-complete.


=========================================================
PHASE 5 FROZEN NOTICE
=========================================================

The complete Execution Infrastructure is now officially frozen.

**Architectural Decision:**
Future phases must not modify Phases 1–5. The core pipeline from market observation to execution outcome is now fully deterministic, immutable, and structurally locked.


=========================================================
SPRINT 6.1 FREEZE NOTICE
=========================================================

Scientific Validation domain initiated via the Hypothesis Contract.

**Architectural Enforcement:**
The runtime remains heavily isolated from research artefacts. Hypotheses act strictly as external blueprints, mathematically forbidden from tangling with the core execution logic.


=========================================================
SPRINT 6.2 FREEZE NOTICE
=========================================================

Experiment specifications have been successfully isolated as immutable scientific artefacts.

**Architectural Enforcement:**
Execution remains entirely outside the Scientific Validation domain. The Experiment defines the test but lacks any mechanical ability to run it.


=========================================================
SPRINT 6.3 FREEZE NOTICE
=========================================================

Validation is the immutable scientific outcome of an Experiment.

**Architectural Enforcement:**
Scientific conclusions remain isolated from the QuantForge runtime.


=========================================================
PHASE 6 FREEZE NOTICE
=========================================================

Phase 6 is now entirely frozen.
Scientific Validation has been formally established as a permanent architectural domain.


Scientific Validation completed.
Architecture frozen.

=========================================================
STRATEGY RESEARCH PROTOCOL
=========================================================

**Reference:** docs/STRATEGY_RESEARCH_PROTOCOL.md

Every future strategy developed within QuantForge must follow this protocol before entering Strategy Assembly.

The Strategy Research Protocol is officially frozen.
The Strategy Research Protocol is officially frozen.

=========================================================
SPRINT 7.1: STRATEGY ASSEMBLY
=========================================================

Strategy Assembly bridges Scientific Validation and the QuantForge runtime.

=========================================================
SPRINT 7.2 & 7.3: DEPLOYMENT LAYER (FROZEN)
=========================================================

**The Deployment Era Begins**
Sprints 7.2 and 7.3 established the `DeploymentContext`, `DeploymentAssembler`, `DeploymentRuntime`, and `DeploymentOrchestrator`. These components wire frozen scientific pipelines (Interpretation, Decision, Risk) into an orchestrated runtime.

**Architectural Enforcement:**
The deployment layer DOES NOT execute trades. It simply assembles validated scientific research into a deployable runtime, concluding the pipeline logic required to execute a strategy up to the `PositionSpecification`. Execution logic remains exclusively in the Execution Domain. This represents the beginning of the Deployment Era defined by MISSION_FREEZE.

=========================================================
SPRINT 7.4: LIVE MARKET ADAPTER (FROZEN)
=========================================================

**The Translation Boundary**
Sprint 7.4 established the `MarketDataAdapter`, defining the exclusive boundary between external market feeds and QuantForge. 

**Architectural Enforcement:**
The Market Adapter translates raw, vendor-specific external data into immutable `EnvironmentSnapshots`. It contains NO trading logic, NO scientific reasoning, and NO execution logic. It solely serves as the translation boundary, ensuring the BOE pipeline remains strictly isolated from raw vendor APIs.

=========================================================
SPRINT 7.5: PAPER TRADING RUNNER (FROZEN)
=========================================================

**The Pipeline Execution Loop**
Sprint 7.5 established the `PaperTradingRunner`.

**Architectural Enforcement:**
The Paper Trading Runner owns execution flow only, routing `EnvironmentSnapshots` through the `DeploymentOrchestrator` and pushing resulting `PositionSpecifications` into the Simulation Execution Adapter. It contains NO market logic, NO broker retry logic, and NO scientific reasoning. Failures inside a single snapshot are contained within a deterministic `RunnerResult` and do not crash the runner session.

=========================================================
SPRINT 7.6: DEPLOYMENT BOOTSTRAP (FROZEN)
=========================================================

**The Assembly Layer**
Sprint 7.6 introduced the `DeploymentBootstrap`.

**Architectural Enforcement:**
The Deployment Bootstrap serves strictly as the application entry point. It performs dependency injection and struct assembly to build a `DeployedPipeline`. It owns NO runtime, market, or scientific logic.

=========================================================
PHASE 7 FROZEN
=========================================================
The Deployment Layer is completely assembled and frozen. It successfully bridges Validated Research to Paper Trading execution without violating the BOE downward-only rules.
