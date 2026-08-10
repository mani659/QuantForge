# QuantForge Research Engine & Historical Market Data Integration Design

**Status:** DESIGN ONLY — NOT IMPLEMENTED
**Date:** September 2026
**Authority:** Constitution v1.0; PHASE7_FREEZE_APPROVED.md; PHASE8_PERMANENT_FREEZE.md
**Verification Baseline:** 491-test regression suite green on the working tree;
`test_market_state_synchronization_regression` in `tests/test_paper_runner.py`
guards the runner→adapter market-state sync that historical replay depends on.

---

## 1. Executive Summary

This document details the design for integrating historical market data into QuantForge to enable deterministic backtesting and research execution. The core objective is to seamlessly exercise the already validated, frozen decision-to-execution pipeline (Phases 1-7) using historical data without altering a single frozen contract.

The proposed architecture introduces a strictly isolated Historical Data Adapter and a Research Runner. By complying with the existing `MarketDataAdapterContract` and `PaperTradingRunner` patterns, the research engine guarantees that historical replay uses the exact same scientific and operational boundaries as live and paper trading. This document represents a design-only milestone; no production code or tests are modified or implemented.

---

## 2. Current Architecture Relevant to Research

The existing QuantForge architecture provides a fully deterministic, immutable pipeline from market observation to execution outcome. Key components relevant to this design include:

*   `EnvironmentSnapshot`: An immutable, opaque dataclass holding market reality.
*   `MarketDataAdapterContract`: An abstract interface defining the translation of raw market data into immutable `EnvironmentSnapshot`s.
*   `GenericMarketDataAdapter`: The existing implementation of the market data adapter contract.
*   `PaperTradingRunner`: The component that drives a sequence of `EnvironmentSnapshot`s through the pipeline and into a broker adapter (simulation).
*   `PaperTradingAdapter`: Simulates broker execution and maintains virtual state.
*   `ExecutionResult`: The immutable, broker-independent output of an execution attempt.

---

## 3. Existing Components Reused

The design maximizes the reuse of existing frozen components to ensure consistency between research and operational execution.

*   `EnvironmentSnapshot`: Used without modification.
*   `MarketDataAdapterContract`: Used without modification. The new Historical Data Adapter will implement this contract.
*   `DeploymentOrchestrator`: Used without modification. It processes historical snapshots identically to live snapshots.
*   `DefaultExecutionEngine` / `PaperTradingAdapter`: Used without modification to simulate execution on historical data.
*   `RunnerResult`: Used without modification to capture the outcome of processing historical snapshots.
*   `ExecutionResult`: Used without modification to record simulated historical fills.

---

## 4. Historical Data Boundary

The boundary between raw historical data and the QuantForge pipeline is defined by the Historical Data Adapter.

### 4.1 Input

Historical market data will be supplied to the Historical Data Adapter (HDA) as a standard iterable of raw data mappings (e.g., dictionaries containing OHLC bars, ticks, or bid/ask data). This iterable represents the chronological stream of market events.

Each `HistoricalMarketAdapter` instance is **adapter-scoped** to a single
dataset/instrument/timeframe combination. `dataset_id`, `instrument`, and
`timeframe` are supplied once when constructing `HistoricalMarketAdapter` and are
**not** dynamically extracted from every raw record. If a historical dataset
contains multiple instrument/timeframe combinations, the research orchestration
layer must use separate appropriately configured adapter instances, or otherwise
partition the dataset before translation.

Required fields per raw data record (illustrative):
*   `timestamp`: `datetime` instance representing the close (or observation) time of the bar/tick.
*   `state`: A mapping containing the market state details (e.g., `open`, `high`, `low`, `close`, `volume`). If absent, the remaining non-identity raw fields are preserved as the market state.

### 4.2 Output

The HDA will output an iterable of immutable `EnvironmentSnapshot` objects. This output exactly matches the contract expected by the `PaperTradingRunner`.

*   `timestamp`: Derived from the raw record.
*   `market_state`: An opaque mapping containing the OHLC/volume data from the raw record. No interpretation or indicator calculation is performed at this boundary.
*   `instrument`: Adapter-scoped, supplied to the `HistoricalMarketAdapter` constructor; copied to each constructed snapshot.
*   `timeframe`: Adapter-scoped, supplied to the `HistoricalMarketAdapter` constructor; copied to each constructed snapshot.
*   `dataset_id`: Adapter-scoped, supplied to the `HistoricalMarketAdapter` constructor and used to scope `snapshot_id`.
*   Determinism: Identical raw input must produce an identical sequence of `EnvironmentSnapshot` objects.

---

## 5. Deterministic Replay Model

Deterministic replay is guaranteed by strict immutability and the acyclic nature of the pipeline.

*   **Dataset Identity**: Provided by the operator or derived from the file path/content hash. It is required by the `HistoricalMarketAdapter` constructor and used to scope `snapshot_id`.
*   **Source Provenance**: The `source` field in `EnvironmentSnapshot` will be set to "historical_feed".
*   **Ordering**: The Historical Data Adapter preserves the strict chronological order of the input data. No internal reordering occurs.
*   **Timezone Handling**: Timezone-awareness is a **HistoricalMarketAdapter-specific invariant**, not an inherited requirement of `EnvironmentSnapshot` or `GenericMarketDataAdapter`. Timezone-naive timestamps are rejected because silently assuming an offset can change the represented market instant and therefore compromise ordering and reproducibility.
*   **Randomness**: No random seeds are required or used. The system operates deterministically by design.

---

## 6. Research Run Model

A research/backtest run is formally modeled as the execution of a `DeploymentOrchestrator` over a sequence of historical `EnvironmentSnapshot`s.

Identity/Provenance needed to reproduce a run (stored as a Research Run Manifest, external to the frozen pipeline):
*   Run ID (e.g., UUID or timestamp-based).
*   Dataset Identity (e.g., file hash or database query hash).
*   Strategy Manifest Identity (e.g., Strategy ID).
*   Configuration Identity (e.g., hash of configuration parameters).
*   Code/Repository Version (e.g., Git commit hash).
*   Start/End Time (historical dataset bounds).

The result evidence consists of the `RunnerResult` objects generated during the run, capturing all `ExecutionResult`s and any pipeline errors.

---

## 7. Research vs. Paper Execution

The existing repository architecture cleanly supports historical research execution via Option B.

**Option B: Replay historical snapshots through the existing paper execution path.**

This is the recommended design because:
*   **Frozen boundaries respected**: Requires no modification to execution contracts.
*   **Accounting correctness**: The `PaperTradingAdapter` already handles PnL, exposure, and reversal lifecycle deterministically.
*   **Reuse**: 100% reuse of the existing execution engine and simulator.
*   **Future consistency**: Guarantees that research behavior matches paper trading behavior exactly.

Thus, the Historical Data Adapter feeds `EnvironmentSnapshot`s into the existing `PaperTradingRunner`, which drives the `DeploymentOrchestrator` and forwards `PositionSpecification`s to the `ExecutionEngine` backed by the `PaperTradingAdapter`.

---

## 8. Market Time Semantics

Time flows through historical replay strictly via the `timestamp` field of the `EnvironmentSnapshot`.

*   The `timestamp` represents the market observation time.
*   The `DeploymentOrchestrator` uses this timestamp for all pipeline processing (e.g., decision evaluation, risk assessment, position sizing).
*   The `PaperTradingAdapter` uses this timestamp via the `EnvironmentSnapshot` to update market state (`update_market_state`) before executing any resulting trades.
*   The market-state sync is performed by `PaperTradingRunner.run()` **before** the orchestrator consumes the snapshot — the same order used in live/paper mode and protected by `test_market_state_synchronization_regression`.
*   **Identical Timestamps**: If the historical data contains multiple snapshots with the exact same timestamp, they are processed sequentially in the order they appear in the dataset.

---

## 9. Data Leakage / Look-Ahead Protection

Look-ahead bias is prevented by a single architectural invariant:

**The Historical Data Adapter and the Research Runner are strictly forward-only iterators.**

*   The Historical Data Adapter reads the dataset sequentially. It cannot seek forward.
*   The `DeploymentOrchestrator` and `PaperTradingRunner` process one `EnvironmentSnapshot` at a time and never retain references to future snapshots.
*   The `PaperTradingAdapter` evaluates `PositionSpecification`s solely against the current `EnvironmentSnapshot`'s market state (e.g., `close` price).
*   No component in the decision pipeline can access information from subsequent `EnvironmentSnapshot`s.

This invariant is structurally enforced by the sequential nature of the `run()` method in `PaperTradingRunner` and the statelessness of the orchestrator.

---

## 10. Data Quality

The Historical Data Adapter is responsible for deterministic data quality handling.

*   **Missing Timestamps**: Records missing timestamps are rejected. The adapter raises a `HistoricalAdapterError`.
*   **Invalid Timestamps**: Non-datetime timestamps are rejected.
*   **Out-of-Order Records**: The adapter fails fast. A timestamp regression raises `HistoricalAdapterError`; no record is silently discarded. The comparison is against the timestamp of the last **successfully translated** record, so a failed record never advances the adapter's chronological state.
*   **Invalid Prices**: Negative or zero prices are rejected.
*   **Missing Prices**: Missing required OHLC fields result in the record being skipped.
*   **Duplicate Timestamps**: Processed sequentially as valid market updates for that specific time.
*   **No Invention**: The adapter never fabricates missing data or interpolates prices. Invalid data is rejected or skipped deterministically.

---

## 11. Experiment Evidence

The persisted evidence for a research run is recorded through the **frozen Phase 8
capture chain** — identical to how paper outcomes are recorded:

*   Each `ExecutionResult` is appended via `OutcomeAppender.append()` into an
    immutable `DeploymentOutcome` (`research/lifecycle/deployment_outcome.py`).
*   `ExperimentRecorder.append_deployment_outcome()` persists it to
    `research/experiments/run_000001/deployment_outcome.json` + `manifest.json`.
*   The immutable evidence is read back through the frozen read-only
    `OutcomeReader` / `ExperimentRecorder.get_deployment_outcome()`, terminating
    the automated system exactly as Phase 8 defines.

Each `RunnerResult` additionally carries per-snapshot provenance:
*   `snapshot_id`: A dataset-relative record identity derived from a deterministic SHA-256 hash of the canonical record content
    (`snapshot_id = f"{dataset_id}:{sha256(canonical(record))[:16]}"`). It is **not** a wall-clock identity and **not** a
    runtime sequence identity; it is reproducible outside the original process. Identical records within the same dataset
    intentionally share the same identifier, while records with different content (same or different timestamps) differ.
*   `processed`: Boolean indicating pipeline success.
*   `execution_result`: The immutable `ExecutionResult` (if a trade was executed), including metadata with realized PnL and leg details.
*   `error`: String containing pipeline failure details (if any).

This evidence allows researchers to reconstruct the exact execution history, calculate total trades, realized PnL, and equity progression. No new evidence artifact, no parallel recorder, and no parallel read path are introduced.

---

## 12. Research Outputs

The minimal required outputs for this milestone are derived by aggregating the sequence of `RunnerResult` objects:

*   **Total Trades**: Count of `RunnerResult` entries with non-null `execution_result`.
*   **Realized PnL**: Sum of `leg_X_realized_pnl` values from execution result metadata.
*   **Execution History**: The sequence of `ExecutionResult` objects.
*   **Dataset Coverage**: Number of snapshots processed vs. skipped.
*   **Run Provenance**: The Research Run Manifest (defined in Section 6).

Advanced performance analytics (win rate, max drawdown, Sharpe ratio) are explicitly deferred to future milestones.

---

## 13. Multi-Timeframe Question

The current architecture handles a single timeframe per `EnvironmentSnapshot`. Historical multi-timeframe aggregation is out of scope for this milestone.

The `timeframe` is **adapter-scoped**: it is supplied to the `HistoricalMarketAdapter` constructor, not read from the raw records. An adapter configured with "M1" produces M1 snapshots; a separate adapter configured with "H1" produces H1 snapshots. Multi-timeframe intelligence requires architectural extension and is deferred. A dataset containing multiple timeframes must therefore be partitioned so each adapter instance receives records for a single timeframe.

---

## 14. Historical XAUUSD Data

The primary research instrument is XAUUSD.

The Historical Data Adapter does not hardcode XAUUSD. The `instrument` is **adapter-scoped**: it is supplied to the `HistoricalMarketAdapter` constructor and copied into each `EnvironmentSnapshot`, rather than being read dynamically from every raw record. A separate adapter instance is required per instrument, so XAUUSD is supported as the first dataset by constructing the adapter with `instrument="XAUUSD"`.

The research framework itself remains completely market-agnostic.

---

## 15. Architectural Drift Protection

| Component | Frozen? | May change? | Reason |
|---|---|---|---|
| ExecutionEngineContract | YES | NO | Existing freeze (Phase 5) |
| BrokerAdapterContract | YES | NO | Existing freeze (Phase 5) |
| ExecutionResult | YES | NO | Existing freeze (Phase 5) |
| PositionSpecification | YES | NO | Existing freeze (Phase 4) |
| PaperTradingAdapter | YES | NO | Existing freeze (Phase 7) |
| PaperTradingRunner | YES | NO | Existing freeze (Phase 7) |
| MarketDataAdapterContract| YES | NO | Existing freeze (Phase 7) |
| Historical Data Adapter | NO | YES | New milestone |
| Research Runner | NO | YES | New milestone |
| Research persistence | NO | YES | New milestone |

Design Options:
Option 1: Implement a single `HistoricalResearchRunner` that wraps `PaperTradingRunner` and manages the dataset iterable.
Option 2: Implement only the `HistoricalMarketAdapter` and feed its output directly into the existing `PaperTradingRunner`.

**Selected Design: Option 2** is the minimal viable implementation and maximizes reuse. It requires zero new runner components. The `PaperTradingRunner` already accepts an `Iterable[EnvironmentSnapshot]`. The new `HistoricalMarketAdapter` will simply provide that iterable.

---

## 16. Minimal Next Implementation Milestone

**Milestone: Historical Deterministic Replay Execution**

1.  Load historical dataset (e.g., XAUUSD CSV).
2.  Initialize `HistoricalMarketAdapter` with the dataset.
3.  Generate the sequence of `EnvironmentSnapshot` objects.
4.  Feed the iterable into the existing `PaperTradingRunner.run()`.
5.  Collect the resulting list of `RunnerResult` objects.
6.  Persist the results as evidence.

This does NOT implement optimization, ML, parameter sweeps, walk-forward testing, live trading, spread modeling, slippage modeling, or multi-timeframe intelligence.

## 17. Explicit Non-Goals

*   Strategy optimization or parameter tuning.
*   Machine learning integration.
*   Walk-forward analysis.
*   Live trading integration.
*   Spread or slippage modeling.
*   Multi-timeframe aggregation.
*   Advanced performance analytics (Sharpe, Sortino, Drawdown).
*   GUI or dashboard development.

## 18. Required Tests for Implementation Phase

The implementation phase must include:
*   `HistoricalMarketAdapter` tests for correct translation of raw data to `EnvironmentSnapshot`.
*   `HistoricalMarketAdapter` tests for data quality rules (skipping invalid records, rejecting malformed input).
*   Integration test verifying that historical snapshots processed through the `PaperTradingRunner` produce deterministically identical `ExecutionResult`s as synthetic test data.
*   Time semantics test ensuring the adapter preserves chronological order.

## 19. Final Engineering Gate

**STATUS: PASS — RESEARCH ENGINE DESIGN READY FOR INDEPENDENT AUDIT**

The design fits entirely above the frozen baseline. It requires no modification to any frozen contract. It extends the platform operationally via a new `MarketDataAdapterContract` implementation, exactly as permitted by the Phase 7 Extension Policy.

**Frozen-boundary verification summary:**
*   `boe/`, `execution/`, `research/`, and `operational_governance/` source is not modified — zero production changes.
*   `tests/` is not modified — zero test changes; the 491-test baseline remains the regression guard.
*   Determinism and look-ahead integrity are inherited from the frozen pipeline plus the strictly forward-only Historical Data Adapter.
*   Evidence is produced and read exclusively through the frozen Phase 8 capture chain (`OutcomeAppender` → `ExperimentRecorder` → `OutcomeReader`).