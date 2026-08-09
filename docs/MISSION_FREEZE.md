# QuantForge Mission Freeze

**Status:** PERMANENT  
**Authority:** Highest-level document in the QuantForge repository  
**Established:** August 2026  
**Supersedes:** All prior mission, vision, and directional statements

> Every future architectural decision, sprint, implementation, audit, and
> research effort must remain aligned with this document. If a conflict arises
> between this document and any other, this document prevails.

---

## 1. Mission Statement

QuantForge exists to discover whether financial markets exhibit statistically
measurable behavioural patterns, and — where the evidence supports it — to
convert those patterns into deterministic, reproducible, automated trading
systems that generate profit from validated scientific truth rather than from
assumptions, optimisation, or belief. The project treats every market
interaction as a scientific experiment and every deployed strategy as a
continuing source of evidence.

---

## 2. Vision

QuantForge is a scientific operating system. Its purpose is to repeatedly
convert validated market behaviour into profitable automated trading systems
through a disciplined, reproducible research-to-deployment pipeline.

The operating system does not begin with a strategy and work backward to find
data that supports it. It begins with raw market reality, observes behaviour
without interpretation, collects evidence independently, subjects that evidence
to scientific reasoning, and only then permits a deterministic decision to flow
toward capital allocation and execution.

Every strategy that survives this pipeline and reaches live deployment becomes
a new experiment. Its real-world performance generates fresh market evidence,
which feeds back into the research process and produces new hypotheses. The
system therefore grows more scientifically informed with every deployment cycle,
regardless of whether individual trades win or lose.

Over time, QuantForge becomes a compounding body of scientific market knowledge
— not merely a collection of trading strategies.

---

## 3. Scientific Philosophy

QuantForge is built on the following scientific principles. These are not
aspirational guidelines. They are operational constraints.

**Observation before interpretation.**  
Market data is recorded and described before any meaning is assigned. Observers
measure. They never explain.

**Behaviour before prediction.**  
QuantForge identifies what markets *do*, not what they *will do*. Prediction is
a consequence of understanding behaviour, not a substitute for it.

**Validation before deployment.**  
No strategy enters paper trading, demo trading, or live trading until its
underlying hypothesis has survived scientific validation — including
cross-market testing, walk-forward analysis, stress testing, and Monte Carlo
simulation.

**Deployment generates new research.**  
A deployed strategy is not the end of the scientific process. It is the
beginning of a new observation cycle. Live performance produces evidence that
either strengthens or challenges the original hypothesis.

**Determinism over optimisation.**  
Every pipeline stage must produce identical outputs given identical inputs.
Curve-fitted parameters, non-reproducible randomness, and opaque optimisation
loops are prohibited. If a result cannot be replayed, it is not scientific.

**Scientific reproducibility over curve fitting.**  
A strategy that performs well on historical data but cannot explain *why* in
behavioural terms has not been validated. It has been overfit. QuantForge
rejects it.

**Independence of evidence.**  
Scientific observers operate in isolation. They analyse the same immutable data
independently and produce evidence independently. No observer may read, depend
on, or react to another observer's output.

---

## 4. Canonical Architecture

The Behavioral Observation Engine (BOE) is the only canonical architecture of
QuantForge.

The BOE implements the project's scientific philosophy as a deterministic
pipeline with strict downward-only information flow across four immutable
domains:

```
Market Reality          →  EnvironmentSnapshot
        ↓
Behavioral Reality      →  BehaviorObservation, BehaviorFrame, FrozenBehaviorTimeline
        ↓
Scientific Reality      →  Evidence, BehaviourProfile, Interpretation, Decision,
                           ValidationResult, HypothesisResult, ExperimentRecord
        ↓
Operational Reality     →  RiskModel, RiskAssessment, PositionSpecification,
                           ExecutionResult
```

Higher domains never depend on lower domains. Operational Reality never feeds
information upward into Scientific Reality. Scientific Reality never feeds
information upward into Behavioral Reality. This separation is permanent.

Legacy modules — including the original Tick Validator, Market DNA Profiler,
Adaptive Strategy Engine, and Signal Generator — remain as historical
artifacts. They contributed to the research discoveries that shaped the BOE.
They are not part of the canonical runtime pipeline. Future development targets
the BOE exclusively.

---

## 5. Core Invariants

The following invariants are immutable. They exist not as arbitrary rules but
because the scientific philosophy demands them.

**Downward-only information flow.**  
Exists because mixing operational outcomes (trade results, profit/loss) into
scientific observation would contaminate the evidence and destroy
reproducibility. The research must never be influenced by the execution.

**Immutable domain objects.**  
Exists because mutation introduces hidden state, breaks replay, and makes
scientific experiments non-reproducible. Every domain object is frozen at
creation.

**Deterministic replay.**  
Exists because science requires reproducibility. Any experiment, observation
window, or decision must produce identical results when replayed with identical
inputs, regardless of when or where the replay occurs.

**Contract-first design.**  
Exists because the contract *is* the architecture. Implementations are
replaceable; contracts are permanent. New observers, interpretation models,
decision policies, risk policies, and broker adapters enter the system by
implementing existing contracts — never by modifying them.

**Separation of Observation, Interpretation, Decision, Risk, and Execution.**  
Exists because conflating these responsibilities is the root cause of
curve-fitting, overfitting, and untestable trading systems. Each domain has a
single responsibility. Observers observe. Interpreters interpret. Decision
policies decide. Risk policies allocate. Execution engines execute. No domain
performs the work of another.

**Execution begins only after PositionSpecification.**  
Exists because the scientific pipeline must complete its work — observation,
evidence collection, interpretation, decision, risk assessment, and position
sizing — before any capital is committed. Execution is the final consumer, not
a participant in the scientific process.

**No broker SDK leakage outside transports.**  
Exists because coupling the scientific pipeline to a specific broker's API
would destroy portability, testability, and the ability to run deterministic
simulations.

These invariants are documented in detail in CORE_FREEZE.md. This section
explains *why* they exist. CORE_FREEZE.md specifies *what* they prohibit.

---

## 6. Current Strategic Objective

The next objective is not building more architecture.

The architecture is sufficiently complete. Seven phases have been designed,
implemented, independently audited, and frozen. The Behavioral Observation
Engine provides the complete pipeline from market observation to broker
execution. Scientific Validation provides the framework for hypothesis testing.
Strategy Assembly provides the composition layer.

The next objective is deploying the scientifically validated Mean Reversion
research through the QuantForge pipeline.

The validated research (DISC-001 through DISC-020) has established that
extreme behavioural displacement, followed by measurable recoil and persistence
confirmation, constitutes a statistically repeatable pattern across multiple
asset classes. This pattern has survived walk-forward testing, Monte Carlo
simulation, spread stress testing, and latency stress testing.

All future work must reduce the distance between:

```
Validated Research
        ↓
Paper Trading
        ↓
Demo Trading
        ↓
Live Trading
```

Any work that does not reduce this distance must justify its existence against
the Decision Filter in Section 11. Architecture refinement, documentation
improvement, and infrastructure enhancement are permitted only when they
directly enable the deployment of validated research.

---

## 7. Research Factory

QuantForge is not a system that produces one strategy and stops. It is a
factory that repeats the following loop indefinitely:

```
Idea
  ↓
Hypothesis
  ↓
Experiment Design
  ↓
Scientific Validation
  ↓
Strategy Assembly
  ↓
Paper Trading
  ↓
Demo Trading
  ↓
Live Trading
  ↓
Market Feedback
  ↓
New Observations
  ↓
New Hypothesis
```

Each complete rotation of this loop produces three outcomes:

1. **A deployed strategy** — if the hypothesis survived validation.
2. **A rejected hypothesis** — if the evidence did not support the claim. This
   is equally valuable. It permanently narrows the search space.
3. **New scientific knowledge** — regardless of outcome. Every experiment
   teaches something about market behaviour that informs the next hypothesis.

QuantForge ultimately exists to repeat this loop forever. The first rotation
is Mean Reversion. The second rotation may be a refinement of Mean Reversion
informed by live performance data, or an entirely new behavioural hypothesis
discovered during deployment. The system does not prescribe what comes next. It
prescribes *how* what comes next must be discovered, validated, and deployed.

The Strategy Research Protocol (docs/STRATEGY_RESEARCH_PROTOCOL.md) governs
this process. Every future strategy must follow it.

---

## 8. What QuantForge Is NOT

QuantForge will not become any of the following unless the scientific research
independently validates a need for it. These are not arbitrary exclusions. Each
represents a specific category of drift that would compromise the scientific
mission.

**Not an AI prediction platform.**  
Because prediction without behavioural understanding is curve fitting.
QuantForge observes behaviour first and infers patterns from evidence. It does
not train models to predict future prices from historical patterns.

**Not an indicator collection.**  
Because indicators are implementation details, not scientific discoveries.
Observers may internally use any calculation they require, but indicators never
cross module boundaries. The system trades behaviour, not indicator values.

**Not a generic EA builder.**  
Because a general-purpose expert advisor framework optimises for flexibility at
the expense of scientific discipline. QuantForge is opinionated: every strategy
must trace to validated research.

**Not a machine learning playground.**  
Because machine learning is a tool, not a philosophy. If ML techniques are
introduced, they must enter through the existing scientific pipeline — as
observers, interpretation models, or decision policies — and must demonstrate
statistically superior performance over deterministic baselines before
replacing them.

**Not an over-engineered framework.**  
Because complexity that does not serve the scientific mission is technical debt,
regardless of how elegant it appears. Every abstraction must justify its
existence by enabling validated research to reach deployment.

**Not architecture for architecture's sake.**  
Because the purpose of QuantForge is deployed strategies, not beautiful
diagrams. The architecture exists to serve the research. The moment
architecture becomes the product, the project has lost its way.

---

## 9. Design Philosophy Going Forward

**Prefer extension over redesign.**  
The frozen architecture is the foundation. New capabilities enter through new
implementations of existing contracts. The contracts themselves change only
through formal architectural review.

**Prefer composition over inheritance.**  
Strategies are compositions of validated scientific components — not subclasses
of an abstract strategy. Observers, interpretation models, decision policies,
risk policies, and broker adapters are composed at assembly time.

**Prefer simplicity over abstraction.**  
If a simpler design achieves the same scientific goal, choose simplicity. An
abstraction that exists to handle future cases that have not been validated is
premature. Build for the validated case. Extend when new evidence demands it.

**Build only what moves validated research closer to deployment.**  
Every line of code, every new module, every configuration file must answer the
question: "Does this help deploy a scientifically validated strategy?" If the
answer is uncertain, the work should wait.

**Every abstraction must justify its existence.**  
An abstraction is justified when it enables a validated research need or solves
a demonstrated production requirement. It is not justified by theoretical
future flexibility.

**Research drives architecture. Architecture never rewrites research.**  
If the research says the market behaves a certain way, the architecture adapts
to represent that behaviour. The architecture never imposes a behaviour that
the research has not validated.

---

## 10. Future Evolution

After the first Mean Reversion strategy is successfully deployed through the
complete QuantForge pipeline and generating live market evidence, the system
may evolve in the following directions:

- **Multiple strategies** — additional behavioural hypotheses validated through
  the Research Factory and deployed as independent Strategy compositions.
- **Portfolio management** — capital allocation across multiple concurrent
  strategies, informed by cross-strategy correlation evidence.
- **Multiple brokers** — additional broker adapters implementing
  BrokerAdapterContract for FIX, REST, and cryptocurrency exchanges.
- **Multiple asset classes** — extension of cross-market validation to new
  instruments as research demands.
- **Cross-market behavioural research** — systematic comparison of behavioural
  patterns across markets to identify universal versus instrument-specific
  phenomena.
- **Regime-aware deployment** — dynamic strategy parameter adaptation based on
  validated regime classification, once regime research achieves statistical
  power.
- **Automated research pipelines** — walk-forward, Monte Carlo, and robustness
  testing executed automatically as part of the deployment process.

These are consequences of success. They are not today's objective. Each will
enter the roadmap only when the preceding stage — successful live deployment of
validated research — has been achieved and its evidence has been recorded.

---

## 11. Decision Filter

Every proposed feature, module, enhancement, or refactoring must pass this
filter before implementation begins.

| # | Question | Required Answer |
|---|----------|-----------------|
| 1 | Does this support scientifically validated trading? | **Yes** |
| 2 | Does it reduce the distance between validated research and live deployment? | **Yes** |
| 3 | Does it preserve the deterministic architecture? | **Yes** |
| 4 | Does it avoid unnecessary complexity? | **Yes** |

If any answer is **No**, the feature should not be built — unless a formal
architectural review explicitly approves it with documented justification.

If all answers are **Yes**, the feature should still be evaluated against the
current strategic objective (Section 6). Work that passes the filter but does
not advance the current objective should be deferred, not abandoned.

---

## 12. Closing Statement

QuantForge is no longer in the architecture-building phase.

Seven architectural phases have been designed, implemented, independently
audited, and frozen. The Behavioral Observation Engine provides a complete,
deterministic pipeline from raw market data to broker execution. The Scientific
Validation domain provides the framework for hypothesis testing. The Strategy
Assembly layer provides the composition mechanism. The research has produced
twenty permanent discoveries, validated across five markets, stress-tested
under adverse conditions, and confirmed through walk-forward and Monte Carlo
analysis.

The foundation is sufficiently complete.

The project's success will now be measured by one criterion: scientifically
validated strategies successfully deployed through the QuantForge operating
system and generating live market evidence that feeds back into the Research
Factory.

Everything else is a means to that end.

---

*This document is intended to remain stable for years. It requires revision
only if the fundamental purpose of QuantForge itself changes — not when a new
sprint begins, a new module is added, or a new market is validated. If the
purpose remains the same, this document remains the same.*

=========================================================
STATUS: CONSTITUTIONALLY FROZEN
=========================================================
