import pytest
from datetime import datetime, timezone
import json
import pandas as pd

from boe.temporal.environment_snapshot import EnvironmentSnapshot
from boe.execution.engine import DefaultExecutionEngine
from boe.execution.contract import ExecutionConfig, ExecutionEngineContract
from boe.execution.paper_adapter import PaperTradingAdapter, PaperTradingAdapterConfig
from boe.execution.result import ExecutionStatus, ExecutionResult
from types import MappingProxyType

from research.engine.strategy_contract import ResearchStrategyContract
from research.engine.configuration import ExperimentConfiguration

from research.orchestration.matrix import HypothesisRecord, ExperimentMatrix, generate_experiment_id
from research.orchestration.engine import OrchestrationEngine
from research.orchestration.reporter import AggregationReporter
from research.engine.synchronization import AdapterMarketStateSynchronizer


def test_experiment_id_determinism():
    config1 = ExperimentConfiguration(
        dataset_id="test", instrument="EURUSD", timeframe="M1",
        dataset_partition="TRAIN",
        date_range_start=datetime(2026, 1, 1, tzinfo=timezone.utc),
        date_range_end=datetime(2026, 1, 2, tzinfo=timezone.utc),
        strategy_id="ma_crossover", strategy_version="1.0",
        strategy_parameters={"fast": 5, "slow": 10},
        random_seed=42
    )
    
    config2 = ExperimentConfiguration(
        dataset_id="test", instrument="EURUSD", timeframe="M1",
        dataset_partition="TRAIN",
        date_range_start=datetime(2026, 1, 1, tzinfo=timezone.utc),
        date_range_end=datetime(2026, 1, 2, tzinfo=timezone.utc),
        strategy_id="ma_crossover", strategy_version="1.0",
        strategy_parameters={"fast": 5, "slow": 10},
        random_seed=42
    )
    
    config3 = ExperimentConfiguration(
        dataset_id="test", instrument="EURUSD", timeframe="M1",
        dataset_partition="TRAIN",
        date_range_start=datetime(2026, 1, 1, tzinfo=timezone.utc),
        date_range_end=datetime(2026, 1, 2, tzinfo=timezone.utc),
        strategy_id="ma_crossover", strategy_version="1.0",
        strategy_parameters={"fast": 5, "slow": 11}, # Difference
        random_seed=42
    )

    assert generate_experiment_id(config1) == generate_experiment_id(config2)
    assert generate_experiment_id(config1) != generate_experiment_id(config3)


def test_experiment_matrix_generation():
    hypothesis = HypothesisRecord(
        hypothesis_id="test_hyp",
        description="Testing MA Crossover",
        dataset_id="test",
        dataset_partition="TRAIN",
        instrument="EURUSD",
        timeframe="M1",
        date_range_start=datetime(2026, 1, 1, tzinfo=timezone.utc),
        date_range_end=datetime(2026, 1, 2, tzinfo=timezone.utc),
        strategy_id="ma",
        strategy_version="1.0"
    )
    
    # 3x3 = 9 combinations
    matrix = ExperimentMatrix({
        "fast": [5, 10, 20],
        "slow": [20, 50, 100]
    })
    
    configs = list(matrix.generate(hypothesis))
    assert len(configs) == 9
    
    # Test filter function
    matrix_filtered = ExperimentMatrix({
        "fast": [5, 50],
        "slow": [20, 100]
    }, filter_func=lambda p: p["fast"] < p["slow"])
    
    configs_filtered = list(matrix_filtered.generate(hypothesis))
    assert len(configs_filtered) == 3 # (5,20), (5,100), (50,100). (50,20) is excluded.


# Stub components for Orchestration
class DummyExceptionStrategy(ResearchStrategyContract):
    @property
    def strategy_id(self) -> str: return "fail_strat"
    @property
    def version(self) -> str: return "1.0"
    def initialize(self, parameters): pass
    def reset(self): pass
    def on_snapshot(self, snapshot):
        raise ValueError("Simulated Strategy Crash")

class DummyNoOpStrategy(ResearchStrategyContract):
    @property
    def strategy_id(self) -> str: return "noop_strat"
    @property
    def version(self) -> str: return "1.0"
    def initialize(self, parameters): pass
    def reset(self): pass
    def on_snapshot(self, snapshot): return None


def test_orchestration_failure_isolation():
    hypothesis = HypothesisRecord(
        hypothesis_id="test_hyp",
        description="Testing",
        dataset_id="test",
        dataset_partition="TRAIN",
        instrument="EURUSD",
        timeframe="M1",
        date_range_start=datetime(2026, 1, 1, tzinfo=timezone.utc),
        date_range_end=datetime(2026, 1, 2, tzinfo=timezone.utc),
        strategy_id="dummy",
        strategy_version="1.0"
    )
    
    matrix = ExperimentMatrix({"trigger_fail": [True, False]})
    
    def snapshot_factory(config):
        return [EnvironmentSnapshot(
            snapshot_id="1", timestamp=datetime(2026,1,1,tzinfo=timezone.utc), market_state={"close":100},
            schema_version="1.0.0", instrument="EURUSD", timeframe="M1", source="test"
        )]
        
    def strategy_factory(strat_id):
        return DummyExceptionStrategy() # Always fails
        
    def research_context_factory():
        config = PaperTradingAdapterConfig(broker_name="paper", metadata=MappingProxyType({}))
        adapter = PaperTradingAdapter(config)
        engine = DefaultExecutionEngine(config=ExecutionConfig(engine_name="default", metadata=MappingProxyType({})), adapter=adapter)
        return __import__('research.engine.run_engine', fromlist=['ResearchExecutionContext']).ResearchExecutionContext(
            execution_engine=engine,
            market_state_synchronizer=AdapterMarketStateSynchronizer(adapter)
        )

    engine = OrchestrationEngine(snapshot_factory, strategy_factory, research_context_factory)
    
    reports = engine.run_hypothesis(hypothesis, matrix)
    
    assert len(reports) == 2
    assert all(r.execution_assumptions["orchestration_status"] == "FAILED" for r in reports)
    assert all("Simulated Strategy Crash" in r.execution_assumptions["orchestration_error"] for r in reports)
    # Ensure isolation means the loop finished despite exceptions.


def test_aggregation_reporter():
    hypothesis = HypothesisRecord(
        hypothesis_id="test_hyp",
        description="Testing",
        dataset_id="test",
        dataset_partition="TRAIN",
        instrument="EURUSD",
        timeframe="M1",
        date_range_start=datetime(2026, 1, 1, tzinfo=timezone.utc),
        date_range_end=datetime(2026, 1, 2, tzinfo=timezone.utc),
        strategy_id="noop",
        strategy_version="1.0"
    )
    matrix = ExperimentMatrix({"param": [1, 2, 3]})
    
    def snapshot_factory(c): return []
    def strategy_factory(s): return DummyNoOpStrategy()
    def research_context_factory():
        config = PaperTradingAdapterConfig(broker_name="paper", metadata=MappingProxyType({}))
        adapter = PaperTradingAdapter(config)
        engine = DefaultExecutionEngine(config=ExecutionConfig(engine_name="default", metadata=MappingProxyType({})), adapter=adapter)
        return __import__('research.engine.run_engine', fromlist=['ResearchExecutionContext']).ResearchExecutionContext(
            execution_engine=engine,
            market_state_synchronizer=AdapterMarketStateSynchronizer(adapter)
        )
        
    engine = OrchestrationEngine(snapshot_factory, strategy_factory, research_context_factory)
    reports = engine.run_hypothesis(hypothesis, matrix)
    
    df = AggregationReporter.aggregate_to_dataframe(reports)
    
    assert len(df) == 3
    assert "param_param" in df.columns
    assert "status" in df.columns
    assert "net_pnl" in df.columns
    assert "experiment_id" in df.columns
    assert all(df["status"] == "SUCCESS")
    
    sensitivity = AggregationReporter.analyze_parameter_sensitivity(df, "param")
    assert len(sensitivity) == 3
    assert "median_pnl" in sensitivity.columns


def test_identity_survives_persistence_and_aggregation(tmp_path):
    hypothesis = HypothesisRecord(
        hypothesis_id="test_hyp", description="Testing ID", dataset_id="test",
        dataset_partition="TRAIN", instrument="EURUSD", timeframe="M1",
        date_range_start=datetime(2026, 1, 1, tzinfo=timezone.utc), date_range_end=datetime(2026, 1, 2, tzinfo=timezone.utc),
        strategy_id="noop", strategy_version="1.0"
    )
    matrix = ExperimentMatrix({"param": [1, 2]})
    
    def snapshot_factory(c): return []
    def strategy_factory(s): return DummyNoOpStrategy()
    def research_context_factory():
        config = PaperTradingAdapterConfig(broker_name="paper", metadata=MappingProxyType({}))
        adapter = PaperTradingAdapter(config)
        engine = DefaultExecutionEngine(config=ExecutionConfig(engine_name="default", metadata=MappingProxyType({})), adapter=adapter)
        return __import__('research.engine.run_engine', fromlist=['ResearchExecutionContext']).ResearchExecutionContext(
            execution_engine=engine,
            market_state_synchronizer=AdapterMarketStateSynchronizer(adapter)
        )
        
    engine = OrchestrationEngine(snapshot_factory, strategy_factory, research_context_factory)
    reports = engine.run_hypothesis(hypothesis, matrix)
    
    from research.experiment_recorder import ExperimentRecorder
    from research.analytics.report import AnalyticsPersister
    import os, json
    
    recorder = ExperimentRecorder(str(tmp_path))
    persister = AnalyticsPersister(recorder)
        # 1. ValidationReport ID must match the configuration's generated ID
    configs = list(matrix.generate(hypothesis))
    for i in range(2):
        expected_id = generate_experiment_id(configs[i])
        assert reports[i].experiment_id == expected_id
        
        # Fake the run_id folder in ExperimentRecorder
        run_folder = tmp_path / "research" / "experiments" / f"run_{i}"
        os.makedirs(run_folder, exist_ok=True)
        with open(run_folder / "manifest.json", "w") as f:
            json.dump({"run_id": f"run_{i}", "files": []}, f)
            
        # 2. AnalyticsPersister must preserve the ID in the json file
        report_file = persister.save_report(f"run_{i}", reports[i])
        with open(report_file, "r") as f:
            data = json.load(f)
            assert data["experiment_id"] == expected_id
            
    # 3. Aggregation output must include the canonical ID
    df = AggregationReporter.aggregate_to_dataframe(reports)
    assert "experiment_id" in df.columns
    assert df["experiment_id"].iloc[0] == reports[0].experiment_id
    assert df["experiment_id"].iloc[1] == reports[1].experiment_id

def test_oos_enforcement():
    hypothesis = HypothesisRecord(
        hypothesis_id="test_hyp",
        description="Testing OOS",
        dataset_id="test",
        dataset_partition="TEST",
        instrument="EURUSD",
        timeframe="M1",
        date_range_start=datetime(2026, 1, 1, tzinfo=timezone.utc),
        date_range_end=datetime(2026, 1, 2, tzinfo=timezone.utc),
        strategy_id="dummy",
        strategy_version="1.0"
    )
    matrix = ExperimentMatrix({"param": [1]})
    
    engine = OrchestrationEngine(lambda c: [], lambda s: DummyNoOpStrategy(), lambda: None)
    
    with pytest.raises(ValueError, match="Orchestration sweeps are strictly isolated to the TRAIN partition"):
        engine.run_hypothesis(hypothesis, matrix)
        
    config = list(matrix.generate(hypothesis))[0]
    
    # We need a proper exec engine for run_out_of_sample since it calls run_single_config
    def research_context_factory():
        config = PaperTradingAdapterConfig(broker_name="paper", metadata=MappingProxyType({}))
        adapter = PaperTradingAdapter(config)
        engine = DefaultExecutionEngine(config=ExecutionConfig(engine_name="default", metadata=MappingProxyType({})), adapter=adapter)
        return __import__('research.engine.run_engine', fromlist=['ResearchExecutionContext']).ResearchExecutionContext(
            execution_engine=engine,
            market_state_synchronizer=AdapterMarketStateSynchronizer(adapter)
        )
        
    engine = OrchestrationEngine(lambda c: [], lambda s: DummyNoOpStrategy(), research_context_factory)
    report = engine.run_out_of_sample(config)
    assert report.execution_assumptions["orchestration_status"] == "SUCCESS"


def test_partition_validation():
    with pytest.raises(ValueError, match="dataset_partition must be one of"):
        ExperimentConfiguration(
            dataset_id="test", instrument="EURUSD", timeframe="M1",
            dataset_partition="INVALID",
            date_range_start=datetime(2026, 1, 1, tzinfo=timezone.utc),
            date_range_end=datetime(2026, 1, 2, tzinfo=timezone.utc),
            strategy_id="ma", strategy_version="1.0"
        )


def test_identity_ignores_seed():
    config1 = ExperimentConfiguration(
        dataset_id="test", instrument="EURUSD", timeframe="M1",
        dataset_partition="TRAIN",
        date_range_start=datetime(2026, 1, 1, tzinfo=timezone.utc),
        date_range_end=datetime(2026, 1, 2, tzinfo=timezone.utc),
        strategy_id="ma", strategy_version="1.0",
        random_seed=42
    )
    config2 = ExperimentConfiguration(
        dataset_id="test", instrument="EURUSD", timeframe="M1",
        dataset_partition="TRAIN",
        date_range_start=datetime(2026, 1, 1, tzinfo=timezone.utc),
        date_range_end=datetime(2026, 1, 2, tzinfo=timezone.utc),
        strategy_id="ma", strategy_version="1.0",
        random_seed=99
    )
    assert generate_experiment_id(config1) == generate_experiment_id(config2)


def test_non_serializable_parameters():
    config = ExperimentConfiguration(
        dataset_id="test", instrument="EURUSD", timeframe="M1",
        dataset_partition="TRAIN",
        date_range_start=datetime(2026, 1, 1, tzinfo=timezone.utc),
        date_range_end=datetime(2026, 1, 2, tzinfo=timezone.utc),
        strategy_id="ma", strategy_version="1.0",
        strategy_parameters={"obj": object()}
    )
    with pytest.raises(ValueError, match="ExperimentConfiguration strategy_parameters contains non-serializable type"):
        generate_experiment_id(config)


class DummyPartialFailureStrategy(ResearchStrategyContract):
    def __init__(self):
        self.count = 0
    @property
    def strategy_id(self) -> str: return "fail_strat"
    @property
    def version(self) -> str: return "1.0"
    def initialize(self, parameters): pass
    def reset(self): pass
    def on_snapshot(self, snapshot):
        self.count += 1
        if self.count == 3:
            raise ValueError("Crash on 3rd snapshot")
        
        # Return a dummy spec that translates to an ExecutionResult
        # We need a proper PositionSpecification for it to be processed
        from boe.risk.specification import PositionSpecification
        from types import MappingProxyType
        return PositionSpecification(
            candidate_id=f"cand_{self.count}", timeline_id="t", observation_id="o", schema_version="1.0",
            position_size_multiplier=1.0, exposure_fraction=1.0, risk_units=1.0, metadata=MappingProxyType({}),
            timestamp=snapshot.timestamp
        )


def test_partial_snapshot_failure():
    hypothesis = HypothesisRecord(
        hypothesis_id="test_hyp", description="Testing Partial",
        dataset_id="test", dataset_partition="TRAIN", instrument="EURUSD", timeframe="M1",
        date_range_start=datetime(2026, 1, 1, tzinfo=timezone.utc),
        date_range_end=datetime(2026, 1, 2, tzinfo=timezone.utc),
        strategy_id="dummy", strategy_version="1.0"
    )
    matrix = ExperimentMatrix({"param": [1]})
    
    def snapshot_factory(config):
        return [
            EnvironmentSnapshot(schema_version="1.0.0", snapshot_id="1", instrument="EURUSD", timeframe="M1", timestamp=datetime(2026,1,1,tzinfo=timezone.utc), source="test", market_state={"close":100}),
            EnvironmentSnapshot(schema_version="1.0.0", snapshot_id="2", instrument="EURUSD", timeframe="M1", timestamp=datetime(2026,1,2,tzinfo=timezone.utc), source="test", market_state={"close":100}),
            EnvironmentSnapshot(schema_version="1.0.0", snapshot_id="3", instrument="EURUSD", timeframe="M1", timestamp=datetime(2026,1,3,tzinfo=timezone.utc), source="test", market_state={"close":100}),
            EnvironmentSnapshot(schema_version="1.0.0", snapshot_id="4", instrument="EURUSD", timeframe="M1", timestamp=datetime(2026,1,4,tzinfo=timezone.utc), source="test", market_state={"close":100})
        ]
        
    def strategy_factory(strat_id): return DummyPartialFailureStrategy()
        
    class DummyExecutionEngine(ExecutionEngineContract):
        def __init__(self):
            self.calls = 0
        @property
        def config(self):
            return ExecutionConfig(engine_name="dummy", metadata=MappingProxyType({}))

        def execute(self, spec):
            self.calls += 1
            action = "BUY" if self.calls == 1 else "CLOSE"
            return ExecutionResult(
                candidate_id="cand_1", timeline_id="t", observation_id="o", schema_version="1.0.0",
                status=ExecutionStatus.SUCCESS, timestamp=spec.timestamp,
                metadata=MappingProxyType({
                    "leg_count": 1,
                    "leg_0_action": action,
                    "leg_0_direction": "BUY",
                    "leg_0_volume": 1.0,
                    "leg_0_price": 100.0,
                    "leg_0_realized_pnl": 10.0 if action == "CLOSE" else 0.0,
                    "account_balance": 100010.0
                })
            )
    def research_context_factory():
        from research.engine.synchronization import MarketStateSynchronizerContract
        class DummySynchronizer(MarketStateSynchronizerContract):
            def sync_market_state(self, snapshot): pass
        engine = DummyExecutionEngine()
        return __import__('research.engine.run_engine', fromlist=['ResearchExecutionContext']).ResearchExecutionContext(
            execution_engine=engine,
            market_state_synchronizer=DummySynchronizer()
        )
            
    engine = OrchestrationEngine(snapshot_factory, strategy_factory, research_context_factory)
    reports = engine.run_hypothesis(hypothesis, matrix)
    
    report = reports[0]
    assert report.execution_assumptions["orchestration_status"] == "FAILED"
    assert "Crash on 3rd snapshot" in report.execution_assumptions["orchestration_error"]
    
    # It should have collected the first 2 executions, which forms 1 trade (BUY then CLOSE)
    assert report.results.number_of_trades == 1
    
    # 3. Aggregation output must include the canonical ID even for FAILED reports
    df = AggregationReporter.aggregate_to_dataframe(reports)
    assert "experiment_id" in df.columns
    assert df["experiment_id"].iloc[0] == report.experiment_id
    assert df["status"].iloc[0] == "FAILED"

def test_naive_datetime_rejection():
    with pytest.raises(ValueError, match="Date ranges must be timezone-aware datetimes"):
        ExperimentConfiguration(
            dataset_id="test", instrument="EURUSD", timeframe="M1",
            dataset_partition="TRAIN",
            date_range_start=datetime(2026, 1, 1), # Naive
            date_range_end=datetime(2026, 1, 2, tzinfo=timezone.utc),
            strategy_id="ma", strategy_version="1.0"
        )
        
    with pytest.raises(ValueError, match="Date ranges must be timezone-aware datetimes"):
        ExperimentConfiguration(
            dataset_id="test", instrument="EURUSD", timeframe="M1",
            dataset_partition="TRAIN",
            date_range_start=datetime(2026, 1, 1, tzinfo=timezone.utc),
            date_range_end=datetime(2026, 1, 2), # Naive
            strategy_id="ma", strategy_version="1.0"
        )

def test_timezone_aware_determinism():
    from datetime import timedelta
    # 2026-01-01 00:00 UTC
    dt_utc = datetime(2026, 1, 1, tzinfo=timezone.utc)
    # 2026-01-01 02:00 +02:00 (which is exactly the same instant as 00:00 UTC)
    tz_plus_2 = timezone(timedelta(hours=2))
    dt_local = datetime(2026, 1, 1, 2, 0, tzinfo=tz_plus_2)
    
    config1 = ExperimentConfiguration(
        dataset_id="test", instrument="EURUSD", timeframe="M1",
        dataset_partition="TRAIN",
        date_range_start=dt_utc,
        date_range_end=datetime(2026, 1, 2, tzinfo=timezone.utc),
        strategy_id="ma", strategy_version="1.0"
    )
    
    config2 = ExperimentConfiguration(
        dataset_id="test", instrument="EURUSD", timeframe="M1",
        dataset_partition="TRAIN",
        date_range_start=dt_local,
        date_range_end=datetime(2026, 1, 2, tzinfo=timezone.utc),
        strategy_id="ma", strategy_version="1.0"
    )
    
    assert generate_experiment_id(config1) == generate_experiment_id(config2)


def test_experiment_factory_isolation():
    hypothesis = HypothesisRecord(
        hypothesis_id="test_hyp",
        description="Testing factory isolation",
        dataset_id="test",
        dataset_partition="TRAIN",
        instrument="EURUSD",
        timeframe="M1",
        date_range_start=datetime(2026, 1, 1, tzinfo=timezone.utc),
        date_range_end=datetime(2026, 1, 2, tzinfo=timezone.utc),
        strategy_id="dummy",
        strategy_version="1.0"
    )
    # 2 configs in matrix
    matrix = ExperimentMatrix({"param": [1, 2]})
    
    contexts = []
    
    def snapshot_factory(c): return []
    def strategy_factory(s): return DummyNoOpStrategy()
    def research_context_factory():
        config = PaperTradingAdapterConfig(broker_name="paper", metadata=MappingProxyType({}))
        adapter = PaperTradingAdapter(config)
        engine = DefaultExecutionEngine(config=ExecutionConfig(engine_name="default", metadata=MappingProxyType({})), adapter=adapter)
        
        from research.engine.synchronization import AdapterMarketStateSynchronizer
        from research.engine.run_engine import ResearchExecutionContext
        
        ctx = ResearchExecutionContext(
            execution_engine=engine,
            market_state_synchronizer=AdapterMarketStateSynchronizer(adapter)
        )
        contexts.append(ctx)
        return ctx
        
    engine = OrchestrationEngine(snapshot_factory, strategy_factory, research_context_factory)
    engine.run_hypothesis(hypothesis, matrix)
    
    assert len(contexts) == 2
    ctx1, ctx2 = contexts[0], contexts[1]
    
    # Assert completely distinct memory identities
    assert id(ctx1) != id(ctx2)
    assert id(ctx1.execution_engine) != id(ctx2.execution_engine)
    assert id(ctx1.market_state_synchronizer) != id(ctx2.market_state_synchronizer)
    
    # Assert internal adapters are distinct
    adapter1 = ctx1.execution_engine._adapter
    adapter2 = ctx2.execution_engine._adapter
    assert id(adapter1) != id(adapter2)
