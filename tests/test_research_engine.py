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
from research.engine.run_engine import ResearchRunEngine
from research.engine.outcome_appender import ResearchOutcomeAppender
from research.experiment_recorder import ExperimentRecorder


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

    # 4. Strategy & Engine
    strategy = MovingAverageCrossoverStrategy()
    run_engine = ResearchRunEngine(
        strategy=strategy,
        execution_engine=exec_engine,
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
