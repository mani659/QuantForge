"""Tests for the HistoricalMarketAdapter."""

import pytest
from datetime import datetime, timezone
from types import MappingProxyType
from unittest.mock import MagicMock

from boe.deployment.historical_adapter import HistoricalMarketAdapter, HistoricalAdapterError
from boe.temporal.environment_snapshot import EnvironmentSnapshot
from boe.deployment.paper_runner import PaperTradingRunner
from boe.execution.engine import DefaultExecutionEngine
from boe.execution.paper_adapter import PaperTradingAdapter, PaperTradingAdapterConfig
from boe.execution.contract import ExecutionConfig
from boe.deployment.orchestrator import DeploymentOrchestrator
from boe.risk.specification import PositionSpecification

@pytest.fixture
def adapter():
    return HistoricalMarketAdapter(instrument="EURUSD", timeframe="M1")

@pytest.fixture
def base_time():
    return datetime(2026, 1, 1, 12, 0, tzinfo=timezone.utc)

def test_valid_raw_record_to_snapshot(adapter, base_time):
    raw_data = {
        "timestamp": base_time,
        "open": 1.1000,
        "close": 1.1010
    }
    
    snapshot = adapter.translate(raw_data)
    
    assert isinstance(snapshot, EnvironmentSnapshot)
    assert snapshot.instrument == "EURUSD"
    assert snapshot.timeframe == "M1"
    assert snapshot.timestamp == base_time
    assert snapshot.source == "historical_feed"
    assert snapshot.market_state["open"] == 1.1000
    assert snapshot.market_state["close"] == 1.1010
    # Deterministic ID
    expected_id = f"EURUSD_M1_{int(base_time.timestamp())}"
    assert snapshot.snapshot_id == expected_id

def test_multiple_records_preserve_source_order(adapter, base_time):
    t1 = base_time
    from datetime import timedelta
    t2 = base_time + timedelta(minutes=1)
    
    snap1 = adapter.translate({"timestamp": t1, "close": 1.1})
    snap2 = adapter.translate({"timestamp": t2, "close": 1.2})
    
    assert snap1.timestamp == t1
    assert snap2.timestamp == t2

def test_duplicate_timestamps_preserve_order(adapter, base_time):
    # E.g. multiple ticks in the same second
    raw1 = {"timestamp": base_time, "tick": 1}
    raw2 = {"timestamp": base_time, "tick": 2}
    
    snap1 = adapter.translate(raw1)
    snap2 = adapter.translate(raw2)
    
    assert snap1.timestamp == base_time
    assert snap2.timestamp == base_time
    assert snap1.market_state["tick"] == 1
    assert snap2.market_state["tick"] == 2

def test_missing_timestamp_rejected(adapter):
    with pytest.raises(HistoricalAdapterError, match="missing 'timestamp'"):
        adapter.translate({"close": 1.1})

def test_invalid_timestamp_rejected(adapter):
    with pytest.raises(HistoricalAdapterError, match="Must be a datetime instance"):
        adapter.translate({"timestamp": "2026-01-01", "close": 1.1})

def test_timezone_naive_timestamp_rejected(adapter):
    from datetime import datetime
    # naive timestamp
    naive_dt = datetime(2026, 1, 1, 12, 0, 0)
    with pytest.raises(HistoricalAdapterError, match="Timezone-naive timestamps are not permitted"):
        adapter.translate({"timestamp": naive_dt, "close": 1.1})

def test_timestamp_regression_rejected(adapter, base_time):
    from datetime import timedelta
    t1 = base_time
    t2 = base_time - timedelta(minutes=1)
    
    adapter.translate({"timestamp": t1, "close": 1.1})
    with pytest.raises(HistoricalAdapterError, match="Timestamp regression detected"):
        adapter.translate({"timestamp": t2, "close": 1.2})

def test_required_fields_preserved(adapter, base_time):
    # Ensure any extra fields are preserved in the market state
    raw_data = {
        "timestamp": base_time,
        "custom_field": "value",
        "nested": {"a": 1}
    }
    
    snapshot = adapter.translate(raw_data)
    assert snapshot.market_state["custom_field"] == "value"
    assert snapshot.market_state["nested"] == {"a": 1}

def test_replaying_identical_input_produces_identical_snapshots(base_time):
    adapter1 = HistoricalMarketAdapter(instrument="XAUUSD", timeframe="M5")
    adapter2 = HistoricalMarketAdapter(instrument="XAUUSD", timeframe="M5")
    
    raw = {"timestamp": base_time, "close": 1500.0}
    
    snap1 = adapter1.translate(raw)
    snap2 = adapter2.translate(raw)
    
    assert snap1 == snap2

def test_no_future_record_exposed(base_time):
    # Test that the adapter processes record N purely from record N, not N+1
    adapter = HistoricalMarketAdapter(instrument="EURUSD", timeframe="M1")
    from datetime import timedelta
    
    t1 = base_time
    t2 = base_time + timedelta(minutes=1)
    
    record1 = {"timestamp": t1, "close": 1.1}
    record2 = {"timestamp": t2, "close": 1.2}
    
    # Process record 1
    snap1 = adapter.translate(record1)
    
    # Process record 2
    snap2 = adapter.translate(record2)
    
    # If the adapter was correctly designed, snap1 didn't change and doesn't know about snap2
    assert snap1.market_state["close"] == 1.1
    assert "future" not in snap1.market_state

def test_historical_adapter_integration_with_paper_runner(base_time):
    """
    INTEGRATION TEST
    Proves that HistoricalMarketAdapter feeds correctly into the existing frozen PaperTradingRunner
    and the historical market state actually reaches the frozen paper execution path.
    """
    from boe.deployment.runtime import DeploymentRuntime
    from boe.behavior_detector_contract import BehaviorDetectorContract
    from boe.evidence.observer_contract import ObserverContract
    from boe.profile.engine import BehaviourProfileEngine
    from boe.risk.models import RiskModelContract
    from boe.risk.position_sizer import PositionSizerContract, PositionSizingResult
    from boe.decision.decision import Decision
    from boe.interpretation.interpretation import Interpretation
    from boe.risk.models import RiskProfile
    from boe.risk.policy import RiskPolicyEvaluation, RiskPolicyAction
    from boe.behavior_observation import BehaviorObservation
    
    # 1. Mock Orchestrator Dependencies
    mock_runtime = MagicMock(spec=DeploymentRuntime)
    mock_detector = MagicMock(spec=BehaviorDetectorContract)
    mock_observer = MagicMock(spec=ObserverContract)
    mock_profile_engine = MagicMock(spec=BehaviourProfileEngine)
    mock_risk_model = MagicMock(spec=RiskModelContract)
    mock_position_sizer = MagicMock(spec=PositionSizerContract)
    
    expected_snapshot_id = f"EURUSD_M1_{int(base_time.timestamp())}"
    expected_timeline_id = f"timeline_{expected_snapshot_id}"
    expected_candidate_id = f"cand_{expected_snapshot_id}"

    mock_obs = BehaviorObservation(
        schema_version="1.0.0",
        observation_id="obs_123",
        environment_id=expected_snapshot_id,
        behavior_type="TEST_BEHAVIOR",
        instrument="EURUSD",
        timeframe="M1",
        observed_at=base_time,
        detector_id="det_1",
        detector_version="1.0.0"
    )
    mock_detector.observe.return_value = mock_obs
    
    from boe.evidence.evidence import Evidence
    mock_ev = Evidence(
        evidence_id="ev_123",
        candidate_id=expected_candidate_id,
        timeline_id=expected_timeline_id,
        observer_name="mock_observer",
        observer_version="1.0.0",
        evidence_type="MOCK_EVIDENCE",
        confidence=0.9,
        observed=True,
        evidence_labels=("test",),
        metadata=MappingProxyType({}),
        timestamp=base_time
    )
    mock_observer.observe.return_value = mock_ev
    mock_profile_engine.build_profile.return_value = MagicMock()
    mock_runtime.interpretation_model.interpret.return_value = MagicMock(spec=Interpretation)
    mock_runtime.decision_policy.evaluate.return_value = MagicMock(spec=Decision)
    mock_risk_model.evaluate.return_value = MagicMock(spec=RiskProfile)

    risk_eval = MagicMock(spec=RiskPolicyEvaluation)
    risk_eval.action = RiskPolicyAction.APPROVE
    risk_eval.candidate_id = expected_candidate_id
    risk_eval.timeline_id = expected_timeline_id
    risk_eval.observation_id = "obs_123"
    risk_eval.rationale = "Test"
    risk_eval.metadata = {}
    mock_runtime.risk_policy.evaluate.return_value = risk_eval

    sizing_result = MagicMock(spec=PositionSizingResult)
    sizing_result.candidate_id = expected_candidate_id
    sizing_result.timeline_id = expected_timeline_id
    sizing_result.observation_id = "obs_123"
    sizing_result.position_size_multiplier = 1.0
    sizing_result.exposure_fraction = 0.1  # BUY intent
    sizing_result.risk_units = 1.0
    sizing_result.metadata = {}
    mock_position_sizer.size_position.return_value = sizing_result
    
    # 2. Real Orchestrator
    orchestrator = DeploymentOrchestrator(
        runtime=mock_runtime,
        detector=mock_detector,
        observers=(mock_observer,),
        profile_engine=mock_profile_engine,
        risk_model=mock_risk_model,
        position_sizer=mock_position_sizer
    )
    
    # 3. Real Adapter and Engine
    paper_adapter = PaperTradingAdapter(PaperTradingAdapterConfig(broker_name="paper", metadata=MappingProxyType({})))
    engine = DefaultExecutionEngine(ExecutionConfig(engine_name="default", metadata=MappingProxyType({})), paper_adapter)
    
    # 4. Real Runner
    runner = PaperTradingRunner(orchestrator, engine)
    
    # 5. Real Historical Adapter
    hist_adapter = HistoricalMarketAdapter(instrument="EURUSD", timeframe="M1")
    
    distinctive_price = 1.2345
    
    # Translate historical row to snapshot
    snapshot = hist_adapter.translate({
        "timestamp": base_time,
        "close": distinctive_price
    })
    
    # Feed to runner
    results = runner.run([snapshot])
    
    assert len(results) == 1
    assert results[0].processed is True
    assert results[0].error is None
    
    # The runner injected the snapshot market state into the paper adapter
    exec_result = results[0].execution_result
    assert exec_result is not None
    
    # Proof that the historical snapshot successfully traversed the pipeline
    assert exec_result.metadata["leg_0_price"] == distinctive_price
