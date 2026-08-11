# Architecture Decision Record: Experiment Orchestration V1

## Context

QuantForge has successfully established a robust, deterministic execution engine (`ResearchRunEngine`) that evaluates a single `ResearchStrategyContract` against a historical market stream (`EnvironmentSnapshot` stream) with strict no-look-ahead and causal correctness guarantees.

However, to move from single-run diagnostics to rigorous strategy research, the system must orchestrate multiple experiments systematically (e.g., parameter sweeps) without mutating the frozen execution layer or compromising the research integrity.

We need an orchestration layer that:
1. Replays experiments deterministically.
2. Isolates state across runs.
3. Structurally enforces in-sample (TRAIN) vs. out-of-sample (VALIDATION/TEST) boundaries.
4. Generates descriptive analytics.
5. Does *not* act as a model-selection optimizer.

## Decision

We will implement **Experiment Orchestration V1** as a strict configuration-driven matrix execution loop with the following design constraints:

### 1. Deterministic Identity (`ExperimentConfiguration`)
Experiment identity is derived exclusively from a content hash of the configuration parameters (`experiment_id = sha256(canonical_json(config))[:16]`). The identity explicitly excludes runtime artifacts, random seeds, or any non-reproducible wall-clock metrics. `random_seed` is reproducibility metadata and does not participate in `experiment_id`. Identical scientific configurations with different seeds therefore share the same `experiment_id`.

### 2. Experiment Matrix
The `ExperimentMatrix` will generate configurations via a Cartesian product. It guarantees deterministic ordering and provides a `filter_func` mechanism to explicitly reject logically invalid parameter combinations before execution.

### 3. Strict Orchestration & Isolation (`OrchestrationEngine`)
The orchestration loop guarantees memory isolation by injecting factory functions for the `MarketDataAdapter`, `ResearchStrategyContract`, and `ResearchExecutionContext` (via `research_context_factory`). For every iteration, completely fresh instances of these components are created. State is never shared between configurations.

**Research Execution Context Principle**: A research simulation requires an execution engine plus an explicit market-state synchronization capability. The synchronization capability belongs to the research domain and must not be added to the generic frozen execution contract. 
- `ExecutionEngineContract` is strictly responsible for execution and order dispatch.
- `MarketStateSynchronizerContract` is strictly responsible for deterministic simulation market-state injection.

The research execution follows a strict causal sequence:
```text
EnvironmentSnapshot
        ↓
Market State Synchronization
        ↓
Strategy Evaluation
        ↓
Execution
        ↓
Evidence Collection
```
### 4. Walk-Forward / Out-of-Sample Barrier
The configuration natively includes a `dataset_partition` field (`TRAIN`, `VALIDATION`, `TEST`). The system enforces an API-level partition boundary. `run_hypothesis()` permits only `TRAIN`. `run_out_of_sample()` permits only `VALIDATION` / `TEST`. `_run_single_config()` is an internal execution primitive and is not the public OOS policy boundary.

### 5. Failure Containment
If an individual snapshot triggers a strategy crash or failure, the run remains `"FAILED"`. However, the `OrchestrationEngine` computes partial metrics from all executions that were successfully collected (including any executions that may occur despite or after the snapshot error). These partial metrics are included in the yielded `ValidationReport` along with the exception's string representation (`str(e)`). This allows the system to seamlessly proceed to the next parameter combination to preserve the integrity of the overall sweep. Partial metrics must never be interpreted as a successful validation result.

### 6. Descriptive Analytics (`AggregationReporter`)
The matrix outcomes are tabulated into a flat pandas DataFrame. Parameter sensitivity is evaluated via grouped median descriptive statistics. The engine strictly reports evidence and is architecturally barred from choosing a "winner" or recommending deployment.

### 7. Analytics Persistence Conventions
- The canonical `experiment_id` is persisted unchanged.
- The `run_id` is not substituted for the `experiment_id`.
- Analytics persistence is write-once at the report-folder level.
- A second write to an existing report folder raises `FileExistsError`, even if the content is identical.
- Positive infinity in `profit_factor` is explicitly represented as the JSON string `"Infinity"`.
- Non-finite values such as NaN must fail loudly rather than producing non-standard JSON.
- Persistence must remain machine-readable and strictly JSON compliant.

## Explicit Non-Goals (V1 Freeze Criteria)
The following are permanently excluded from V1:
- Machine Learning (ML) hyperparameter tuning.
- Genetic optimization / Simulated annealing algorithms.
- Automatic parameter selection / model recommendation.
- Asynchronous / Threaded / Parallelized execution loops.
- In-memory dataset caching mechanisms (for V1, isolated re-parsing is preferred).
- Live execution pathways.
