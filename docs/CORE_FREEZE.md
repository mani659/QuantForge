# QuantForge Core Freeze (CAF-1)

Phases 1–5 constitute the frozen QuantForge Core.

Future development extends the platform. 
Future development does NOT redesign the platform.

---

## Core Mission

QuantForge is a deterministic quantitative research and execution platform.

Its purpose is to transform market observations into reproducible, scientifically validated execution while remaining broker-independent and strategy-agnostic.

---

## Architectural Invariants

The following represent non-negotiable rules for the QuantForge Core platform:

- Deterministic execution
- Replay reproducibility
- Immutable domain objects
- Downward-only dependency graph
- Contract-first development
- Strict separation of Observation, Interpretation, Decision, Risk, and Execution
- Execution begins ONLY after PositionSpecification
- No strategy logic inside execution
- No risk logic inside interpretation
- No broker SDK leakage outside transports
- No implementation leakage across domains

These are permanent architectural invariants.

---

## Frozen Dependency Graph

The canonical pipeline of the QuantForge Core is immutable.

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
Execution

No future phase may violate this dependency direction without an explicit architectural redesign.

---

## Extension Policy

Future work is permitted exclusively via extension. 

Every future sprint should reduce the distance between Validated Research -> Paper Trading -> Demo -> Live.
New architectural domains should only be introduced if they directly enable deployment.

Future phases may:
- add new observers
- add new interpretation models
- add new decision policies
- add new risk policies
- add new broker adapters
- add new transports
- add portfolio management
- add optimisation
- add orchestration
- add monitoring

Future phases must extend existing contracts. 
They must not modify the frozen scientific runtime without formal architectural approval.

---

## Architectural Decision Policy

Any change affecting the foundational nature of the platform requires a formal architecture review before implementation.

This includes modifications to:
- dependency direction
- immutable contracts
- deterministic replay
- pipeline ordering
- architectural boundaries

---

## Scientific Principles

QuantForge does not optimise for profitable trades first.
QuantForge optimises for reproducible scientific truth.

Trading strategies are consumers of scientific evidence. 
They are not embedded into the platform.

---

## Product Philosophy

QuantForge Core is now a platform.

Individual trading systems (such as Mean Reversion, Momentum, Statistical Arbitrage, Cross-Market Rotation, and Portfolio Allocation) are products built on top of the platform.

They are not part of the platform itself.

---

## Completion Statement

Phases 1–5 are officially frozen.

Future development begins with Phase 6.

All future work extends the QuantForge Core.

=========================================================
PHASE 6 FREEZE
=========================================================

Phase 6 (Scientific Validation) has been completed and formally frozen.
Future phases may extend the domain, but they do NOT redesign it.

Phase 6 is now part of the frozen QuantForge platform.

Future phases may consume Scientific Validation.
They may not redesign it without a formal architecture review.

=========================================================
PHASE 7 FREEZE
=========================================================

Phase 7 (Deployment Layer) has been completed and formally frozen.
Future phases may extend the domain, but they do NOT redesign it.

Phase 7 is now part of the frozen QuantForge platform.

Future phases may consume the Deployment Layer.
They may not redesign it without a formal architecture review.

=========================================================
PHASE 8 FREEZE
=========================================================

Phase 8 extends the system operationally.
It does not alter any frozen scientific domains.
No sprint in Phase 8 may introduce business logic into BOE.

Phase 8 (Research Industrialization) industrializes the scientific lifecycle:
Research → Validation → Validated Behaviour → Strategy Manifest → Deployment
Runtime → Execution → Deployment Evidence Capture → OutcomeReader → END OF
SOFTWARE → Human Research Review → Operational Governance (Phase 9).

Note: Earlier planning documents described the final pipeline step as "Research
Feedback". That is a superseded historical term; the frozen pipeline terminates
at the read-only `OutcomeReader` service, with Human Research Review residing
outside QuantForge software.

Future phases may consume the frozen platform and Phase 8 research
industrialization. They may not redesign the frozen scientific runtime,
domain objects, or public contracts without a formal architectural review.
