import pytest
import os
import shutil
from datetime import datetime, timezone
from types import MappingProxyType

from boe.deployment.historical_adapter import HistoricalMarketAdapter
from boe.execution.engine import DefaultExecutionEngine
from boe.execution.contract import ExecutionConfig, ExecutionEngineContract
from boe.execution.paper_adapter import PaperTradingAdapter, PaperTradingAdapterConfig
from boe.execution.result import ExecutionStatus

from research.engine.configuration import ExperimentConfiguration
from research.engine.stub_strategy import MovingAverageCrossoverStrategy
from research.engine.strategy_contract import ResearchStrategyContract
from research.engine.synchronization import AdapterMarketStateSynchronizer, MarketStateSynchronizerContract
from research.engine.run_engine import ResearchRunEngine, ResearchExecutionContext, ResearchRunEngineError
from research.engine.outcome_appender import ResearchOutcomeAppender
from research.experiment_recorder import ExperimentRecorder
def test_research_run_pipeline_end_to_end(tmp_path):
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
    temp_dir = str(tmp_path)
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

def test_research_execution_ordering():
    """Test: Prove strict sequence: sync -> strategy -> execute."""
    config = ExperimentConfiguration(
        dataset_id="t", dataset_partition="TRAIN", instrument="EURUSD", timeframe="M1",
        date_range_start=datetime(2026, 1, 1, tzinfo=timezone.utc), date_range_end=datetime(2026, 1, 2, tzinfo=timezone.utc),
        strategy_id="stub", strategy_version="1.0.0", strategy_parameters={}
    )
    
    events = []
    
    class SpySynchronizer(MarketStateSynchronizerContract):
        def sync_market_state(self, snapshot):
            events.append("sync")
            
    class SpyStrategy(ResearchStrategyContract):
        @property
        def strategy_id(self): return "spy"
        @property
        def version(self): return "1.0"
        def reset(self): pass
        def initialize(self, params): pass
        def on_snapshot(self, snapshot):
            events.append("strategy")
            from boe.risk.specification import PositionSpecification
            return PositionSpecification(
                candidate_id="c1", timeline_id="t1", observation_id="o1", schema_version="1.0",
                position_size_multiplier=1.0, exposure_fraction=0.1, risk_units=1.0,
                metadata=MappingProxyType({}), timestamp=snapshot.timestamp
            )

    class SpyExecutionEngine(ExecutionEngineContract):
        @property
        def config(self) -> ExecutionConfig:
            return ExecutionConfig(engine_name="spy", metadata=MappingProxyType({}))
        def execute(self, specification):
            events.append("execute")
            from boe.execution.result import ExecutionResult, ExecutionStatus
            return ExecutionResult(
                candidate_id=specification.candidate_id,
                timeline_id=specification.timeline_id,
                observation_id=specification.observation_id,
                schema_version=specification.schema_version,
                status=ExecutionStatus.SUCCESS,
                metadata=MappingProxyType({}),
                timestamp=specification.timestamp
            )

    context = ResearchExecutionContext(execution_engine=SpyExecutionEngine(), market_state_synchronizer=SpySynchronizer())
    run_engine = ResearchRunEngine(strategy=SpyStrategy(), execution_context=context, config=config)
    
    historical_adapter = HistoricalMarketAdapter(dataset_id="test", instrument="EURUSD", timeframe="M1")
    snapshot = historical_adapter.translate({"timestamp": datetime(2026, 1, 1, 10, 0, tzinfo=timezone.utc), "close": 1.1000})
    
    results = run_engine.run([snapshot])
    
    # Assert exact causal ordering
    assert events == ["sync", "strategy", "execute"]
    
    # Assert successful execution processing
    assert len(results) == 1
    assert results[0].processed is True
    assert results[0].execution_result is not None
    assert results[0].error is None


def test_adapter_market_state_synchronizer_fail_fast():
    """Test: AdapterMarketStateSynchronizer fails if adapter lacks update_market_state."""
    class InvalidAdapter:
        pass
        
    with pytest.raises(ValueError, match="Adapter does not support market-state synchronization"):
        AdapterMarketStateSynchronizer(InvalidAdapter())


def test_adapter_market_state_synchronizer_valid():
    """Test: AdapterMarketStateSynchronizer successfully syncs valid adapter."""
    class ValidAdapter:
        def __init__(self):
            self.synced = False
        def update_market_state(self, snapshot):
            self.synced = True
            
    adapter = ValidAdapter()
    sync = AdapterMarketStateSynchronizer(adapter)
    
    historical_adapter = HistoricalMarketAdapter(dataset_id="test", instrument="EURUSD", timeframe="M1")
    snapshot = historical_adapter.translate({"timestamp": datetime(2026, 1, 1, 10, 0, tzinfo=timezone.utc), "close": 1.1000})
    
    sync.sync_market_state(snapshot)
    assert adapter.synced is True


def test_research_execution_context_validation():
    """Test: ResearchExecutionContext rejects invalid dependencies."""
    from boe.execution.contract import ExecutionEngineContract
    
    class DummySynchronizer(MarketStateSynchronizerContract):
        def sync_market_state(self, snapshot): pass
        
    class DummyExecutionEngine(ExecutionEngineContract):
        @property
        def config(self) -> ExecutionConfig:
            return ExecutionConfig(engine_name="dummy", metadata=MappingProxyType({}))
        def execute(self, spec): pass

    # Invalid engine
    with pytest.raises(TypeError, match="execution_engine must be an ExecutionEngineContract"):
        ResearchExecutionContext(execution_engine="not_an_engine", market_state_synchronizer=DummySynchronizer())
        
    # Invalid synchronizer
    with pytest.raises(TypeError, match="market_state_synchronizer must be a MarketStateSynchronizerContract"):
        ResearchExecutionContext(execution_engine=DummyExecutionEngine(), market_state_synchronizer="not_a_sync")
        
    # Valid
    ctx = ResearchExecutionContext(execution_engine=DummyExecutionEngine(), market_state_synchronizer=DummySynchronizer())
    assert ctx.execution_engine is not None
