# QuantForge Phase 7 Deployment Freeze

The Deployment Layer is permanently frozen.

Future development extends the platform.  
Future development does NOT redesign the platform.

---

## 1. Purpose

The Deployment Layer exists to faithfully carry validated scientific conclusions into repeatable operational behaviour. It serves as the constitutional bridge between confirmed research and consistent execution, preserving the integrity of the underlying science while enabling it to be reproduced across the forms of operation the platform supports.

Deployment is operational.  
It is not scientific.

The Deployment Layer does not create science, redefine science, or assign meaning to science. Its role is to preserve what has been validated and to reproduce it faithfully in a stable and deterministic manner.

It does not own discovery.  
It does not own interpretation.  
It does not own execution physics.

---

## 2. Scope

Phase 7 owns exactly the following responsibilities:

**Strategy Assembly** — The declarative composition layer that binds validated scientific components into a deployable unit with a managed lifecycle (DRAFT → READY → PAPER → DEMO → LIVE → RETIRED).

**Deployment Runtime** — The read-only shell exposing the assembled scientific pipeline. It holds no broker integrations, no event loops, and no portfolio state.

**Deployment Context** — The immutable container storing strictly validated references to the pipeline's exact components.

**Deployment Assembler** — The deterministic resolver that binds a deployable unit against domain registries to produce the runtime configuration.

**Deployment Bootstrap** — The application entry point performing deterministic structural assembly, producing a fully initialized pipeline from configuration, registries, and injected engines.

**Deployment Orchestrator** — The stateless coordinator that routes each market observation sequentially through the complete scientific pipeline — Observation → Evidence → Behaviour → Interpretation → Decision → Risk — terminating at the position specification boundary.

**Market Data Adapter** — The exclusive ingress boundary translating raw external market feeds into structured market observations. Contains no trading logic, no scientific reasoning, no execution logic.

**Paper Trading Runner** — The execution flow coordinator that drives market observations through the orchestrator and forwards resulting position specifications to the execution layer, encapsulating per-snapshot failures in deterministic outcomes.

**Simulation Execution Integration** — The contract-level integration with the Execution Domain ensuring deterministic, broker-independent simulation of position specifications into execution outcomes.

Nothing else.

---

## 3. Canonical Deployment Pipeline

The frozen deployment pipeline is immutable and strictly ordered:

```
Market Feed
    ↓
Market Observation
    ↓
Market Data Adapter
    ↓
Deployment Orchestrator
    ↓
Observation
    ↓
Evidence
    ↓
Behaviour
    ↓
Interpretation
    ↓
Decision
    ↓
Risk
    ↓
Position Specification
    ↓
Execution
    ↓
Execution Result
```

This is the only canonical deployment pipeline.

The pipeline begins at Market Feed and terminates at Execution Result.  
No stage may be reordered, bypassed, or duplicated.  
Information flows downward only.

---

## 4. Constitutional Principles

The following principles are permanent rules for the Deployment Layer:

**Deployment owns orchestration.**  
The orchestrator sequences the scientific pipeline. It does not compute indicators, evaluate evidence, or size positions.

**Deployment owns construction.**  
The bootstrap, assembler, and runtime configuration objects construct the deployment graph. They do not execute it.

**Deployment never owns science.**  
No observation, evidence, behaviour, interpretation, decision, or validation logic exists in the Deployment Layer. Scientific reasoning is consumed, never produced.

**Deployment never owns execution physics.**  
No broker communication, order routing, fill simulation, or position tracking exists in the Deployment Layer. Execution is delegated to the Execution Domain.

**Deployment never owns market interpretation.**  
The Market Data Adapter translates structure only. It assigns no meaning to price, volume, or time.

**Deployment remains stateless.**  
All deployment components hold no mutable state between calls. State resides exclusively in the Execution Domain.

**Deployment never stores behavioural history.**  
No timeline, window, or historical accumulation exists in the Deployment Layer. Behavioural history remains exclusively in the Behavioural Reality domain.

**Deployment never modifies frozen objects.**  
All domain objects flowing through the pipeline are immutable. Deployment components treat them as read-only inputs.

**Deployment coordinates only.**  
Every Deployment component is a coordinator, translator, assembler, or factory. None is a decision-maker.

---

## 5. Frozen Public Contracts

The following responsibilities constitute the stable constitutional commitments of the Deployment Layer. They are frozen as concepts, not as implementation signatures or interface details. Implementations may vary; responsibilities must not be modified without formal architectural review.

**Strategy Assembly**  
Responsible for composing validated scientific components into a deployable unit with a managed lifecycle.

**Deployment Runtime**  
Responsible for presenting the assembled pipeline as a controlled operating context.

**Deployment Context**  
Responsible for carrying the validated references required to execute the pipeline faithfully.

**Deployment Assembler**  
Responsible for binding a deployable unit to the resources required for its operating configuration.

**Deployment Bootstrap**  
Responsible for deterministic construction of the deployment pipeline from its governing configuration and dependencies.

**Deployment Orchestrator**  
Responsible for sequentially routing observations through the complete scientific pipeline until the position specification boundary is reached.

**Market Data Adapter**  
Responsible for translating external market data into structured market observations without introducing scientific interpretation.

**Paper Trading Runner**  
Responsible for coordinating execution over a stream of observations while preserving deterministic failure isolation.

**Execution Integration**  
Responsible for connecting the deployment pipeline to execution outcomes without altering the underlying scientific logic.

**Deployment Configuration**  
Responsible for preserving immutable deployment settings that govern how the pipeline is assembled and operated.

**Deployment Registries**  
Responsible for providing the controlled resolution of components required for deployment assembly.

**Deployment Dependencies**  
Responsible for supplying the runtime dependencies required to construct and operate the deployment pipeline.

---

## 6. Extension Policy

Future work may extend the platform exclusively through the following mechanisms:

**Permitted Extensions**
- **Live MT5 Adapter** — Implementing `MarketDataAdapterContract` for MT5 market data feeds
- **Interactive Brokers Adapter** — Implementing `MarketDataAdapterContract` for IB feeds
- **Binance Adapter** — Implementing `MarketDataAdapterContract` for cryptocurrency feeds
- **FIX Adapter** — Implementing `MarketDataAdapterContract` for FIX protocol feeds
- **Additional Broker Adapters** — Implementing `ExecutionEngineContract` for live broker execution
- **Monitoring & Telemetry** — Observing pipeline metrics without modifying pipeline behaviour
- **Portfolio Layer** — Capital allocation across multiple concurrent Strategies (post-Phase 7)

**Prohibited Modifications**
The following components are constitutionally frozen and must NOT be modified unless a Constitutional Review explicitly approves it:

- `DeploymentRuntime`
- `DeploymentContext`
- `DeploymentAssembler`
- `DeploymentBootstrap`
- `DeploymentOrchestrator`
- `MarketDataAdapterContract`
- `GenericMarketDataAdapter`
- `PaperTradingRunner`
- `RunnerResult`
- `DeployedPipeline`
- `DeploymentConfiguration`
- `DeploymentRegistries`
- `DeploymentDependencies`

Future phases may consume these contracts.  
They may not redesign them.

---

## 7. Non-Goals

The Deployment Layer must NEVER become the following. These are not arbitrary exclusions. Each represents a specific category of responsibility that belongs to other constitutional domains.

**Not a scientific discovery engine.**  
The Deployment Layer does not discover opportunities, validate hypotheses, or generate new scientific knowledge. Discovery belongs to the Scientific Reality domain.

**Not a market interpreter.**  
The Deployment Layer does not interpret market behaviour, classify regimes, or assign meaning to price patterns. Interpretation belongs to the Scientific Reality domain.

**Not a portfolio manager.**  
The Deployment Layer does not allocate capital across multiple strategies, manage correlations, or optimise portfolio construction. Portfolio management is a future capability that belongs above the Deployment Layer.

**Not a strategy optimiser.**  
The Deployment Layer does not tune parameters, walk-forward optimise, or adapt strategy behaviour. Optimisation belongs to the Scientific Validation domain.

**Not a behavioural learning system.**  
The Deployment Layer does not learn from market data, adapt to new patterns, or evolve its understanding of behaviour. Learning belongs to the Scientific Reality domain.

**Not a scientific decision maker.**  
The Deployment Layer does not decide whether to trade. Decisions are made by the Scientific Reality domain and consumed by the Deployment Layer as immutable conclusions.

**Not a risk calculator.**  
The Deployment Layer does not compute risk models, assess exposure, or size positions. Risk calculation belongs to the Operational Reality domain.

---

## 8. Relationship to Future Phases

Future phases consume the Deployment Layer.

Future phases extend the platform.

Future phases shall not redefine Deployment responsibilities.

The Deployment Layer is a permanent constitutional boundary. It represents the established mechanism by which validated scientific research becomes deterministic operational behaviour. Future phases may add new adapters, new execution integrations, and new monitoring capabilities. They may not redesign the orchestration model, the assembly model, or the boundary definitions.

If a future phase identifies a deficiency in the Deployment Layer, the deficiency must be addressed through formal constitutional review — not through ad hoc modification during implementation.

---

## 9. Accepted Technical Debt

At the time of this freeze, no architectural technical debt has been accepted as part of the Deployment Layer's constitutional definition. This does not prohibit future operational improvements, capability expansion, or refinement of supporting implementations. It means only that the frozen boundary itself is not defined by compromise. Future improvements may strengthen reliability, observability, compatibility, and execution support, but they do not alter the constitutional responsibilities of the Deployment Layer.

## 10. Deployment Philosophy

Deployment faithfully executes validated science.

Deployment never creates science.

Deployment never changes science.

Deployment never interprets science.

Its sole purpose is to reproduce validated behavioural research consistently across replay, paper trading, and live execution.

---

## 11. Completion Summary

This document records the permanent constitutional boundary of the Deployment Layer. It preserves the frozen responsibilities, boundaries, and principles established for Phase 7 without introducing new architecture or redefining scope.

**Sprint 7.1 — Strategy Assembly Contracts**  
Defined the immutable Strategy composition layer binding Validation, Interpretation Model, Decision Policy, and Risk Policy into a deployable artefact with a managed lifecycle.

**Sprint 7.2 — Deployment Runtime**  
Introduced DeploymentContext, DeploymentRuntime, and DeploymentAssembler — the structural primitives for wiring scientific registries into an executable runtime.

**Sprint 7.3 — Deployment Orchestrator**  
Implemented the stateless pipeline coordinator that routes EnvironmentSnapshots through the complete BOE pipeline (Observation → Evidence → Behaviour Profile → Interpretation → Decision → Risk) terminating at PositionSpecification.

**Sprint 7.3.1 — Audit Remediation**  
Resolved independent audit findings: removed dead code (execution_profile), eliminated phantom ExecutionRegistry dependency, clarified orchestrator docstring. Zero functional changes.

**Sprint 7.4 — Live Market Adapter**  
Established the exclusive ingress boundary (MarketDataAdapterContract, GenericMarketDataAdapter) translating raw external market data into immutable EnvironmentSnapshots with full validation and deterministic construction.

**Sprint 7.5 — Paper Trading Runner**  
Implemented the execution flow coordinator (PaperTradingRunner) that drives snapshot streams through the orchestrator and into the Simulation Execution Adapter, with deterministic per-snapshot failure isolation.

**Sprint 7.6 — Deployment Bootstrap**  
Delivered the application entry point (DeploymentBootstrap) performing deterministic dependency injection and structural assembly into a DeployedPipeline, completing the Deployment Layer.

---

## 12. Constitutional Status

**PHASE 7**  
**DEPLOYMENT LAYER**  

**STATUS:**  
**CONSTITUTIONALLY FROZEN**

The Deployment Layer is considered complete.

Future development shall extend the platform rather than redesign it.

The frozen BOE boundaries established during Phases 1–6 remain unchanged.

Deployment exists solely to reduce the distance between validated scientific research and deterministic execution.

Approved:  
August 4, 2026

---

## 13. Post-Fix Stable Baseline (Execution Metadata & Market Synchronization)

This section formally records the validated baseline of the Phase 7 Deployment Layer following the resolution of the Execution Metadata defect and the implementation of Market-State Synchronization regression protection.

### Test Baseline
```text
Tests: 491
Passed: 491
Failed: 0
Errors: 0
Warnings: 0
```

### Execution Evidence
The validated five-tick synthetic paper session is:
```text
Tick 1
Price: 1.1000
Exposure: +0.02
Action: BUY
Realized PnL: 0.0000000000000000

Tick 2
Price: 1.1010
Exposure: +0.04
Action: BUY
Realized PnL: 0.0000000000000000

Tick 3
Price: 1.1020
Exposure: +0.01
Action: REDUCE
Realized PnL: +4.0896687635740303

Tick 4
Price: 1.1030
Exposure: -0.02
Actions:
  CLOSE BUY 907.4904837452596
  SELL 1813.351927456235
Realized PnL: +2.2691304477742227

Tick 5
Price: 1.1040
Exposure: 0.00
Action:
  CLOSE SELL 1813.351927456235
Realized PnL: -1.8133519274564380

Final Realized PnL:
+4.545447283891815
```
The persisted execution records, rather than internal account state alone, must be treated as the audit evidence for this result.

### Frozen Execution Contract Invariants
* `PositionSpecification → ExecutionResult` remains 1:1.
* `ExecutionEngineContract` remains unchanged.
* `BrokerAdapterContract` remains unchanged.
* `ExecutionResult` remains unchanged.
* Compound physical execution is represented inside `ExecutionResult.metadata`.
* Multiple `ExecutionResult` objects are NOT introduced for a single strategy execution intent.

### Frozen Metadata Invariants
* Every physical execution leg is persisted.
* Reversal contains both the closing and opening legs.
* Full close contains the actual physical closed volume.
* Metadata remains compatible with `ExecutionResult.__hash__`.
* Persisted metadata is sufficient for independent lifecycle reconstruction.

### Frozen Market-State Invariant
For normal paper-runner execution:
```text
EnvironmentSnapshot
→ PaperTradingRunner
→ PaperTradingAdapter.update_market_state(snapshot)
→ PaperTradingAdapter.execute_trade()
```
The execution must use the synchronized market price.
The regression test: `test_market_state_synchronization_regression` is the protection against removal of this behavior.

### Frozen Accounting Invariants
* Partial close preserves remaining position state.
* Reversal closes the previous direction before opening the new direction.
* Full close produces zero final position.
* Realized PnL is generated only from actual closures.
* Unrealized PnL is not incorrectly double-counted as realized PnL.
* Reconstructed persisted PnL matches the execution ledger.
* Five-tick final realized PnL remains `4.545447283891815`.

### Intentional Non-Blocking Assumptions

#### A. Legacy `current_price = 100.0`
Classification: `KNOWN LEGACY DEFAULT — NON-BLOCKING`
The runner synchronization path overwrites this before normal paper execution. Do NOT remove it as part of this freeze.

#### B. Duck-typed market synchronization
Current mechanism:
```text
PaperTradingRunner
→ getattr/hasattr adapter
→ update_market_state(snapshot)
```
Classification: `KNOWN IMPLEMENTATION COUPLING — NON-BLOCKING`
This is intentionally accepted for the current milestone. It must NOT be "fixed" or replaced during unrelated future work. Any future formalization of this boundary requires an explicit architectural decision and separate milestone.

#### C. Exposure-to-volume semantics
Current repository behavior is:
```text
target_volume =
    account_equity
    × abs(exposure_fraction)
    ÷ current_market_price
```
Classification: `REPOSITORY-DEFINED ASSUMPTION`
Do NOT alter it during this baseline freeze.

#### D. Equity-based sizing
The current simulator uses equity, including the relevant unrealized PnL at the synchronized market state, for sizing.
Classification: `REPOSITORY-DEFINED SIMULATION ASSUMPTION`
Do NOT change it without an explicit design decision.

#### E. Flat `leg_X_*` metadata
Classification: `VALIDATED IMPLEMENTATION CONSTRAINT`
This representation is intentionally compatible with the immutable/hashable `ExecutionResult` requirements. Do NOT replace it with nested/unhashable metadata without an explicit contract review.

### Explicit Anti-Drift Rules

**Future engineering MUST NOT silently:**
* change exposure semantics;
* change equity-vs-balance sizing;
* change PnL semantics;
* remove market-state synchronization;
* replace compound leg metadata;
* alter reversal lifecycle behavior;
* alter full-close reporting;
* modify frozen execution contracts;
* change the 1:1 strategy-intent → ExecutionResult relationship;
* redesign the execution boundary merely to make the current implementation look cleaner.

Any such change requires:
1. explicit identification of the affected invariant;
2. a new engineering decision;
3. updated tests;
4. a new audit;
5. explicit approval before implementation.