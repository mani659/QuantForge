import pytest
import os
import shutil
from datetime import datetime, timezone
from types import MappingProxyType

from boe.deployment.historical_adapter import HistoricalMarketAdapter
from boe.execution.engine import DefaultExecutionEngine
from boe.execution.contract import ExecutionConfig
from boe.execution.paper_adapter import PaperTradingAdapter, PaperTradingAdapterConfig
from boe.execution.result import ExecutionStatus

from research.engine.configuration import ExperimentConfiguration
from research.engine.stub_strategy import MovingAverageCrossoverStrategy
from research.engine.synchronization import AdapterMarketStateSynchronizer, SynchronizedExecutionEngine
from research.engine.run_engine import ResearchRunEngine, ResearchExecutionContext, ResearchRunEngineError
from research.engine.outcome_appender import ResearchOutcomeAppender
from research.experiment_recorder import ExperimentRecorder
from research.engine.synchronization import NullMarketStateSynchronizer, MarketStateSynchronizerContract

def test_research_run_pipeline_end_to_end():
    # 1. Config
    config = ExperimentConfiguration(
        dataset_id="test_dataset",
        dataset_partition="TRAIN",
        instrument="EURUSD",
        timeframe="M1",
        date_range_start=datetime(2026, 1, 1, tzinfo=timezone.utc),
        date_range_end=datetime(2026, 1, 2, tzinfo=timezone.utc),
        strategy_id="ma_crossover_stub",
        strategy_version="1.0.0",
        strategy_parameters={"short_window": 2, "long_window": 4}
    )

    # 2. Historical Market Adapter (Frozen Contract)
    adapter = HistoricalMarketAdapter(
        dataset_id=config.dataset_id,
        instrument=config.instrument,
        timeframe=config.timeframe,
    )
    
    # Synthetic Data
    raw_ticks = [
        {"timestamp": datetime(2026, 1, 1, 10, 0, tzinfo=timezone.utc), "close": 1.1000},
        {"timestamp": datetime(2026, 1, 1, 10, 1, tzinfo=timezone.utc), "close": 1.1010},
        {"timestamp": datetime(2026, 1, 1, 10, 2, tzinfo=timezone.utc), "close": 1.1020},
        {"timestamp": datetime(2026, 1, 1, 10, 3, tzinfo=timezone.utc), "close": 1.1030}, # short MA > long MA -> Buy
        {"timestamp": datetime(2026, 1, 1, 10, 4, tzinfo=timezone.utc), "close": 1.1040}, # Still Buy
        {"timestamp": datetime(2026, 1, 1, 10, 5, tzinfo=timezone.utc), "close": 1.0900}, # short MA < long MA -> Sell
    ]
    snapshots = [adapter.translate(tick) for tick in raw_ticks]

    # 3. Execution Stack
    paper_config = PaperTradingAdapterConfig(broker_name="paper", metadata=MappingProxyType({}))
    paper_adapter = PaperTradingAdapter(config=paper_config)
    exec_engine = DefaultExecutionEngine(
        config=ExecutionConfig(engine_name="default", metadata=MappingProxyType({})),
        adapter=paper_adapter
    )
    
    context = ResearchExecutionContext(
        execution_engine=exec_engine,
        market_state_synchronizer=AdapterMarketStateSynchronizer(paper_adapter)
    )

    # 4. Strategy & Engine
    strategy = MovingAverageCrossoverStrategy()
    run_engine = ResearchRunEngine(
        strategy=strategy,
        execution_context=context,
        config=config
    )

    # 5. Execute Run
    results = run_engine.run(snapshots)
    
    # Assert execution logic works (we expect 2 executions based on the data)
    assert len(results) == len(snapshots)
    
    executions = [r for r in results if r.execution_result is not None]
    assert len(executions) > 0
    assert all(e.execution_result.status == ExecutionStatus.SUCCESS for e in executions)
    
    # 6. Save Outcomes
    temp_dir = "./test_research_outcomes"
    os.makedirs(temp_dir, exist_ok=True)
    try:
        recorder = ExperimentRecorder(temp_dir)
        appender = ResearchOutcomeAppender(recorder)
        
        outcome_ids = []
        for res in executions:
            outcome_id = appender.append(res.execution_result, strategy, config, "test_exp_id")
            outcome_ids.append(outcome_id)
            
        assert len(outcome_ids) == len(executions)
        
        # Verify ExperimentRecorder wrote files
        recorded_runs = recorder.list_deployment_outcomes()
        assert len(recorded_runs) == len(executions)
        
    finally:
        shutil.rmtree(temp_dir)

def test_explicit_synchronization():
    """Test 1: Explicit synchronization verification."""
    config = ExperimentConfiguration(
        dataset_id="t", dataset_partition="TRAIN", instrument="EURUSD", timeframe="M1",
        date_range_start=datetime(2026, 1, 1, tzinfo=timezone.utc), date_range_end=datetime(2026, 1, 2, tzinfo=timezone.utc),
        strategy_id="stub", strategy_version="1.0.0", strategy_parameters={}
    )
    
    class SpySynchronizer(MarketStateSynchronizerContract):
        def __init__(self):
            self.synced = []
        def sync_market_state(self, snapshot):
            self.synced.append(snapshot.market_state["close"])
            
    spy_sync = SpySynchronizer()
    exec_engine = DefaultExecutionEngine(
        config=ExecutionConfig(engine_name="d", metadata=MappingProxyType({})),
        adapter=PaperTradingAdapter(config=PaperTradingAdapterConfig(broker_name="paper", metadata=MappingProxyType({})))
    )
    
    context = ResearchExecutionContext(execution_engine=exec_engine, market_state_synchronizer=spy_sync)
    run_engine = ResearchRunEngine(strategy=MovingAverageCrossoverStrategy(), execution_context=context, config=config)
    
    adapter = HistoricalMarketAdapter(dataset_id="test", instrument="EURUSD", timeframe="M1")
    snapshots = [
        adapter.translate({"timestamp": datetime(2026, 1, 1, 10, 0, tzinfo=timezone.utc), "close": 1.11}),
        adapter.translate({"timestamp": datetime(2026, 1, 1, 10, 1, tzinfo=timezone.utc), "close": 1.12}),
        adapter.translate({"timestamp": datetime(2026, 1, 1, 10, 2, tzinfo=timezone.utc), "close": 1.13})
    ]
    
    run_engine.run(snapshots)
    
    assert spy_sync.synced == [1.11, 1.12, 1.13]


def test_no_implicit_fallback():
    """Test 2: Verify ResearchRunEngine fails without an explicit context."""
    config = ExperimentConfiguration(
        dataset_id="t", dataset_partition="TRAIN", instrument="EURUSD", timeframe="M1",
        date_range_start=datetime(2026, 1, 1, tzinfo=timezone.utc), date_range_end=datetime(2026, 1, 2, tzinfo=timezone.utc),
        strategy_id="stub", strategy_version="1.0.0", strategy_parameters={}
    )
    exec_engine = DefaultExecutionEngine(
        config=ExecutionConfig(engine_name="d", metadata=MappingProxyType({})),
        adapter=PaperTradingAdapter(config=PaperTradingAdapterConfig(broker_name="paper", metadata=MappingProxyType({})))
    )
    
    with pytest.raises(ResearchRunEngineError, match="execution_context must be a ResearchExecutionContext"):
        ResearchRunEngine(
            strategy=MovingAverageCrossoverStrategy(),
            execution_context=exec_engine,  # Invalid! Must be ResearchExecutionContext
            config=config
        )


def test_market_state_synchronization_regression():
    """Test 3: Real paper-adapter MTM regression."""
    config = ExperimentConfiguration(
        dataset_id="test_dataset", dataset_partition="TRAIN", instrument="EURUSD", timeframe="M1",
        date_range_start=datetime(2026, 1, 1, tzinfo=timezone.utc),
        date_range_end=datetime(2026, 1, 2, tzinfo=timezone.utc),
        strategy_id="stub", strategy_version="1.0.0",
        strategy_parameters={}
    )

    paper_config = PaperTradingAdapterConfig(broker_name="paper", metadata=MappingProxyType({}))
    paper_adapter = PaperTradingAdapter(config=paper_config)
    exec_engine = DefaultExecutionEngine(
        config=ExecutionConfig(engine_name="default", metadata=MappingProxyType({})),
        adapter=paper_adapter
    )
    
    context = ResearchExecutionContext(
        execution_engine=exec_engine,
        market_state_synchronizer=AdapterMarketStateSynchronizer(paper_adapter)
    )

    class DummyStrategy(MovingAverageCrossoverStrategy):
        def on_snapshot(self, snapshot):
            if snapshot.market_state["close"] == 1.1030:
                from boe.risk.specification import PositionSpecification
                return PositionSpecification(
                    candidate_id="c1", timeline_id="t1", observation_id="o1", schema_version="1.0",
                    position_size_multiplier=1.0, exposure_fraction=0.1, risk_units=1.0,
                    metadata=MappingProxyType({}), timestamp=snapshot.timestamp
                )
            return None

    run_engine = ResearchRunEngine(strategy=DummyStrategy(), execution_context=context, config=config)

    adapter = HistoricalMarketAdapter(dataset_id="test", instrument="EURUSD", timeframe="M1")
    raw_ticks = [
        {"timestamp": datetime(2026, 1, 1, 10, 0, tzinfo=timezone.utc), "close": 1.1000},
        {"timestamp": datetime(2026, 1, 1, 10, 1, tzinfo=timezone.utc), "close": 1.1030}, # Triggers Buy
    ]
    snapshots = [adapter.translate(tick) for tick in raw_ticks]

    results = run_engine.run(snapshots)
    
    executions = [r for r in results if r.execution_result is not None]
    assert len(executions) == 1
    
    # If synchronization was a no-op, the price would remain 100.0 (the default initialized value)
    # With correct synchronization, the price at execution time for 1.1030 snapshot should be 1.1030
    metadata = executions[0].execution_result.metadata
    assert metadata["leg_0_price"] == 1.1030, f"Execution price was {metadata['leg_0_price']}, expected 1.1030. Synchronization regression!"


def test_standard_execution_engine_remains_valid():
    """Test 5: Standard execution engine remains valid under frozen contract."""
    from boe.execution.contract import ExecutionEngineContract
    
    paper_adapter = PaperTradingAdapter(config=PaperTradingAdapterConfig(broker_name="paper", metadata=MappingProxyType({})))
    exec_engine = DefaultExecutionEngine(
        config=ExecutionConfig(engine_name="default", metadata=MappingProxyType({})),
        adapter=paper_adapter
    )
    
    assert isinstance(exec_engine, ExecutionEngineContract)
    assert not hasattr(exec_engine, "sync_market_state")
    assert not hasattr(exec_engine, "_market_synchronizer")

