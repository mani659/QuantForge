"""Tests for the Paper Trading Runner."""

from datetime import datetime, timezone
import pytest
from unittest.mock import MagicMock

from boe.deployment.paper_runner import PaperTradingRunner, RunnerResult, PaperTradingRunnerError
from boe.deployment.orchestrator import DeploymentOrchestrator
from boe.execution.contract import ExecutionEngineContract
from boe.temporal.environment_snapshot import EnvironmentSnapshot
from boe.risk.specification import PositionSpecification
from boe.execution.result import ExecutionResult, ExecutionStatus
from types import MappingProxyType


@pytest.fixture
def mock_orchestrator():
    orchestrator = MagicMock(spec=DeploymentOrchestrator)
    return orchestrator


@pytest.fixture
def mock_engine():
    engine = MagicMock(spec=ExecutionEngineContract)
    return engine


@pytest.fixture
def runner(mock_orchestrator, mock_engine):
    return PaperTradingRunner(mock_orchestrator, mock_engine)


@pytest.fixture
def valid_snapshot():
    return EnvironmentSnapshot(
        schema_version="1.0.0",
        snapshot_id="snap_1",
        instrument="EURUSD",
        timeframe="M1",
        timestamp=datetime(2026, 1, 1, 10, 0, tzinfo=timezone.utc),
        source="test",
        market_state={"close": 1.1}
    )


@pytest.fixture
def valid_snapshot_2():
    return EnvironmentSnapshot(
        schema_version="1.0.0",
        snapshot_id="snap_2",
        instrument="EURUSD",
        timeframe="M1",
        timestamp=datetime(2026, 1, 1, 10, 1, tzinfo=timezone.utc),
        source="test",
        market_state={"close": 1.1005}
    )


def test_initialization_validation(mock_orchestrator, mock_engine):
    """Test that runner initialization enforces types."""
    with pytest.raises(PaperTradingRunnerError):
        PaperTradingRunner("not_an_orchestrator", mock_engine)
        
    with pytest.raises(PaperTradingRunnerError):
        PaperTradingRunner(mock_orchestrator, "not_an_engine")
        
    runner = PaperTradingRunner(mock_orchestrator, mock_engine)
    assert runner is not None


def test_single_snapshot_with_trade(runner, mock_orchestrator, mock_engine, valid_snapshot):
    """Test processing a single snapshot resulting in a trade execution."""
    spec = PositionSpecification(
        candidate_id="c_1",
        timeline_id="t_1",
        observation_id="o_1",
        schema_version="1.0",
        position_size_multiplier=1.0,
        exposure_fraction=0.1,
        risk_units=1.0,
        metadata=MappingProxyType({}),
        timestamp=valid_snapshot.timestamp
    )
    mock_orchestrator.process_snapshot.return_value = spec
    
    exec_result = ExecutionResult(
        candidate_id="c_1",
        timeline_id="t_1",
        observation_id="o_1",
        schema_version="1.0",
        status=ExecutionStatus.SUCCESS,
        timestamp=valid_snapshot.timestamp,
        metadata=MappingProxyType({"fill": 1.1})
    )
    mock_engine.execute.return_value = exec_result
    
    results = runner.run([valid_snapshot])
    
    assert len(results) == 1
    assert results[0].snapshot_id == "snap_1"
    assert results[0].processed is True
    assert results[0].execution_result == exec_result
    assert results[0].error is None
    
    mock_orchestrator.process_snapshot.assert_called_once_with(valid_snapshot)
    mock_engine.execute.assert_called_once_with(spec)


def test_single_snapshot_no_trade(runner, mock_orchestrator, mock_engine, valid_snapshot):
    """Test processing a single snapshot where orchestrator returns None."""
    mock_orchestrator.process_snapshot.return_value = None
    
    results = runner.run([valid_snapshot])
    
    assert len(results) == 1
    assert results[0].processed is True
    assert results[0].execution_result is None
    
    mock_orchestrator.process_snapshot.assert_called_once_with(valid_snapshot)
    mock_engine.execute.assert_not_called()


def test_multiple_snapshots(runner, mock_orchestrator, mock_engine, valid_snapshot, valid_snapshot_2):
    """Test deterministic processing of multiple snapshots sequentially."""
    mock_orchestrator.process_snapshot.side_effect = [None, None]
    
    results = runner.run([valid_snapshot, valid_snapshot_2])
    
    assert len(results) == 2
    assert results[0].snapshot_id == "snap_1"
    assert results[1].snapshot_id == "snap_2"
    assert mock_orchestrator.process_snapshot.call_count == 2
    
    # Assert deterministic ordering matching input order
    calls = mock_orchestrator.process_snapshot.call_args_list
    assert calls[0][0][0] == valid_snapshot
    assert calls[1][0][0] == valid_snapshot_2


def test_execution_failure_handling(runner, mock_orchestrator, mock_engine, valid_snapshot):
    """Test that a failure in the orchestrator is handled and doesn't crash the session."""
    mock_orchestrator.process_snapshot.side_effect = Exception("Orchestrator crashed")
    
    results = runner.run([valid_snapshot])
    
    assert len(results) == 1
    assert results[0].snapshot_id == "snap_1"
    assert results[0].processed is False
    assert results[0].execution_result is None
    assert results[0].error == "Orchestrator crashed"


def test_malformed_snapshot(runner, mock_orchestrator):
    """Test that the runner safely skips malformed (non-EnvironmentSnapshot) items."""
    results = runner.run(["not_a_snapshot"])  # type: ignore
    
    assert len(results) == 1
    assert results[0].snapshot_id == "unknown"
    assert results[0].processed is False
    assert "Invalid input" in results[0].error
    
    mock_orchestrator.process_snapshot.assert_not_called()


def test_replay_equality(runner, mock_orchestrator, mock_engine, valid_snapshot, valid_snapshot_2):
    """Test that two identical sequences of snapshots produce identically equivalent outcomes."""
    mock_orchestrator.process_snapshot.side_effect = [None, None, None, None]
    
    # First run
    run_1 = runner.run([valid_snapshot, valid_snapshot_2])
    
    # Second run (exact same input data)
    run_2 = runner.run([valid_snapshot, valid_snapshot_2])
    
    assert run_1 == run_2

def test_market_state_synchronization_regression(mock_orchestrator):
    """
    REGRESSION TEST: Proves that the PaperTradingRunner actively synchronizes
    the market state to the PaperTradingAdapter before execution.
    
    If PaperTradingRunner.run() fails to call adapter.update_market_state(snapshot),
    the adapter will silently use the default legacy price (100.0) instead of the
    actual market price (1.2345), resulting in incorrect execution metrics.
    """
    from boe.execution.engine import DefaultExecutionEngine
    from boe.execution.paper_adapter import PaperTradingAdapter, PaperTradingAdapterConfig
    from boe.execution.contract import ExecutionConfig
    from types import MappingProxyType

    # 1. Real Adapter & Engine
    adapter = PaperTradingAdapter(PaperTradingAdapterConfig(broker_name="paper", metadata=MappingProxyType({})))
    engine = DefaultExecutionEngine(ExecutionConfig(engine_name="default", metadata=MappingProxyType({})), adapter)
    runner = PaperTradingRunner(mock_orchestrator, engine)

    # 2. Distinctive Market Price
    distinctive_price = 1.2345
    snapshot = EnvironmentSnapshot(
        schema_version="1.0.0",
        snapshot_id="snap_sync_1",
        instrument="EURUSD",
        timeframe="M1",
        timestamp=datetime(2026, 1, 1, 10, 0, tzinfo=timezone.utc),
        source="test",
        market_state=MappingProxyType({"close": distinctive_price})
    )

    # 3. Simulate Orchestrator Approving a Trade
    spec = PositionSpecification(
        candidate_id="c_sync",
        timeline_id="t_sync",
        observation_id="o_sync",
        schema_version="1.0",
        position_size_multiplier=1.0,
        exposure_fraction=0.1,  # Intent to BUY
        risk_units=1.0,
        metadata=MappingProxyType({}),
        timestamp=snapshot.timestamp
    )
    mock_orchestrator.process_snapshot.return_value = spec

    # 4. Run the Pipeline
    results = runner.run([snapshot])
    
    # 5. Verify the Execution Result contains the distinctive price, not 100.0
    assert len(results) == 1
    assert results[0].processed is True
    assert results[0].error is None
    
    exec_result = results[0].execution_result
    assert exec_result is not None
    
    # Verify the physical execution leg recorded the correct distinctive price
    assert exec_result.metadata["leg_0_price"] == distinctive_price
