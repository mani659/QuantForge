import pytest
from datetime import datetime, timedelta
from unittest.mock import MagicMock, call
from types import MappingProxyType

from boe.temporal.environment_snapshot import EnvironmentSnapshot
from boe.behavior_observation import BehaviorObservation
from boe.evidence.evidence import EvidencePackage, Evidence
from boe.profile.profile import BehaviourProfile
from boe.interpretation.interpretation import Interpretation
from boe.decision.decision import Decision, DecisionAction
from boe.risk.models import RiskProfile
from boe.risk.assessment import RiskAssessment, AssessmentStatus
from boe.risk.specification import PositionSpecification
from boe.risk.position_sizer import PositionSizingResult
from boe.risk.policy import RiskPolicyEvaluation, RiskPolicyAction

from boe.deployment.runtime import DeploymentRuntime
from boe.behavior_detector_contract import BehaviorDetectorContract
from boe.evidence.observer_contract import ObserverContract
from boe.profile.engine import BehaviourProfileEngine
from boe.risk.models import RiskModelContract
from boe.risk.position_sizer import PositionSizerContract
from boe.observation.observation_config import ObservationConfig
from boe.observation.observation_policy import DefaultObservationPolicy
from boe.observation.observation_contract import ObservationPolicyContract
from boe.observation.observation_result import ObservationDecision
from boe.observation.termination_reason import TerminationReason
from boe.observers.velocity_observer import VelocityObserver, VelocityObserverConfig
from boe.replay.replay_engine_contract import ReplayEngineContract
from boe.replay.replay_state import ReplayState

from boe.deployment.orchestrator import DeploymentOrchestrator
from boe.deployment.orchestrator_errors import PipelineExecutionError

def make_snapshot(timestamp: datetime, snapshot_id: str, close_price: float = 1.1000) -> EnvironmentSnapshot:
    return EnvironmentSnapshot(
        schema_version="1.0.0",
        snapshot_id=snapshot_id,
        instrument="EURUSD",
        timeframe="H1",
        timestamp=timestamp,
        source="MT5",
        market_state={"close": close_price}
    )

def make_observation(snapshot_id: str, timestamp: datetime) -> BehaviorObservation:
    return BehaviorObservation(
        schema_version="1.0.0",
        observation_id=f"obs_{snapshot_id}",
        environment_id=snapshot_id,
        behavior_type="TEST_BEHAVIOR",
        instrument="EURUSD",
        timeframe="H1",
        observed_at=timestamp,
        detector_id="det_1",
        detector_version="1.0.0"
    )

@pytest.fixture
def mock_snapshot():
    return make_snapshot(datetime(2026, 1, 1, 12, 0, 0), "snap_123")

@pytest.fixture
def policy_config():
    return ObservationConfig(schema_version="1.0.0", max_frames=2, max_duration=3600.0)

@pytest.fixture
def mock_dependencies(policy_config):
    mock_runtime = MagicMock(spec=DeploymentRuntime)
    mock_detector = MagicMock(spec=BehaviorDetectorContract)
    mock_observer = MagicMock(spec=ObserverContract)
    mock_profile_engine = MagicMock(spec=BehaviourProfileEngine)
    mock_risk_model = MagicMock(spec=RiskModelContract)
    mock_position_sizer = MagicMock(spec=PositionSizerContract)
    
    mock_obs = make_observation("snap_123", datetime(2026, 1, 1, 12, 0, 0))
    mock_detector.observe.return_value = mock_obs
    
    def mock_observer_side_effect(timeline):
        return Evidence(
            evidence_id="ev_123",
            candidate_id=timeline.candidate_id,
            timeline_id=timeline.timeline_id,
            observer_name="mock_observer",
            observer_version="1.0.0",
            evidence_type="MOCK_EVIDENCE",
            confidence=0.9,
            observed=True,
            evidence_labels=("test",),
            metadata=MappingProxyType({}),
            timestamp=timeline.closed_timestamp
        )
    mock_observer.observe.side_effect = mock_observer_side_effect
    
    mock_prof = MagicMock(spec=BehaviourProfile)
    mock_profile_engine.build_profile.return_value = mock_prof
    
    mock_interp = MagicMock(spec=Interpretation)
    mock_runtime.interpretation_model.interpret.return_value = mock_interp
    
    mock_dec = MagicMock(spec=Decision)
    mock_runtime.decision_policy.evaluate.return_value = mock_dec
    
    mock_risk_prof = MagicMock(spec=RiskProfile)
    mock_risk_model.evaluate.return_value = mock_risk_prof
    
    # Return a side_effect to dynamically create RiskPolicyEvaluation using the argument candidate_id
    def mock_risk_policy_side_effect(dec, rp, dt):
        eval_mock = MagicMock(spec=RiskPolicyEvaluation)
        eval_mock.action = RiskPolicyAction.APPROVE
        eval_mock.candidate_id = "mock_cand"
        eval_mock.timeline_id = "mock_timeline"
        eval_mock.observation_id = "mock_obs"
        eval_mock.rationale = "Test"
        eval_mock.metadata = {"policy": "TestPolicy"}
        return eval_mock
    mock_runtime.risk_policy.evaluate.side_effect = mock_risk_policy_side_effect
    
    # Same for sizer
    def mock_sizer_side_effect(assessment, dt):
        res = MagicMock(spec=PositionSizingResult)
        res.position_size_multiplier = 1.0
        res.candidate_id = "mock_cand"
        res.timeline_id = "mock_timeline"
        res.observation_id = "mock_obs"
        res.exposure_fraction = 0.02
        res.risk_units = 1.0
        res.metadata = {"sizer": "mock"}
        return res
    mock_position_sizer.size_position.side_effect = mock_sizer_side_effect
    
    observation_policy = DefaultObservationPolicy(policy_config)

    return {
        "runtime": mock_runtime,
        "detector": mock_detector,
        "observers": (mock_observer,),
        "profile_engine": mock_profile_engine,
        "risk_model": mock_risk_model,
        "position_sizer": mock_position_sizer,
        "observation_policy": observation_policy,
        "outputs": {
            "observation": mock_obs,
            "profile": mock_prof,
            "interpretation": mock_interp,
            "decision": mock_dec,
            "risk_profile": mock_risk_prof
        }
    }

def create_orchestrator(mock_dependencies, policy=None):
    if policy is None:
        policy = mock_dependencies["observation_policy"]
    return DeploymentOrchestrator(
        runtime=mock_dependencies["runtime"],
        detector=mock_dependencies["detector"],
        observers=mock_dependencies["observers"],
        profile_engine=mock_dependencies["profile_engine"],
        risk_model=mock_dependencies["risk_model"],
        position_sizer=mock_dependencies["position_sizer"],
        observation_policy=policy
    )

def test_deployment_orchestrator_successful_pipeline(mock_snapshot, mock_dependencies):
    orchestrator = create_orchestrator(mock_dependencies)
    
    dt1 = mock_snapshot.timestamp
    spec1 = orchestrator.process_snapshot(mock_snapshot)
    assert spec1 is None
    assert len(orchestrator._active_candidates) == 1
    
    snap2 = make_snapshot(dt1 + timedelta(minutes=1), "snap_124")
    mock_dependencies["detector"].observe.return_value = None
    
    spec2 = orchestrator.process_snapshot(snap2)
    assert spec2 is not None
    assert isinstance(spec2, PositionSpecification)
    
    from unittest.mock import ANY
    mock_dependencies["observers"][0].observe.assert_called_once_with(ANY)
    timeline_arg = mock_dependencies["observers"][0].observe.call_args[0][0]
    assert len(timeline_arg.frames) == 2
    assert timeline_arg.frames[0].environment_snapshot_id == "snap_123"
    assert timeline_arg.frames[1].environment_snapshot_id == "snap_124"
    
    assert len(orchestrator._active_candidates) == 0

def test_deployment_orchestrator_no_behavior_detected(mock_snapshot, mock_dependencies):
    mock_dependencies["detector"].observe.return_value = None
    
    orchestrator = create_orchestrator(mock_dependencies)
    spec = orchestrator.process_snapshot(mock_snapshot)
    
    assert spec is None
    assert len(orchestrator._active_candidates) == 0
    mock_dependencies["observers"][0].observe.assert_not_called()

def test_deployment_orchestrator_pipeline_failure_preserves_determinism(mock_snapshot, mock_dependencies):
    policy_config = ObservationConfig(schema_version="1.0.0", max_frames=1, max_duration=3600.0)
    policy = DefaultObservationPolicy(policy_config)
    orchestrator = create_orchestrator(mock_dependencies, policy)
    
    mock_dependencies["runtime"].risk_policy.evaluate.side_effect = ValueError("Risk Policy Error")
    
    # For a max_frames=1, snap1 will trigger AND terminate immediately?
    # No, trigger creates window and appends snap1. But freeze only happens on the NEXT process_snapshot
    # because detector triggers are processed AFTER existing active windows in `process_snapshot`.
    orchestrator.process_snapshot(mock_snapshot)
    
    snap2 = make_snapshot(mock_snapshot.timestamp + timedelta(minutes=1), "snap_fail")
    with pytest.raises(PipelineExecutionError) as exc_info:
        orchestrator.process_snapshot(snap2)
        
    assert "Pipeline execution failed: Risk Policy Error" in str(exc_info.value)
    mock_dependencies["position_sizer"].size_position.assert_not_called()

def test_first_trigger_opens_active_observation(mock_snapshot, mock_dependencies):
    orchestrator = create_orchestrator(mock_dependencies)
    spec = orchestrator.process_snapshot(mock_snapshot)
    
    assert spec is None
    assert len(orchestrator._active_candidates) == 1
    assert "cand_snap_123" in orchestrator._active_windows
    bow = orchestrator._active_windows["cand_snap_123"]
    assert bow._timeline.frame_count() == 1
    mock_dependencies["observers"][0].observe.assert_not_called()

def test_second_snapshot_appends(mock_snapshot, mock_dependencies):
    policy_config = ObservationConfig(schema_version="1.0.0", max_frames=3, max_duration=3600.0)
    policy = DefaultObservationPolicy(policy_config)
    orchestrator = create_orchestrator(mock_dependencies, policy)
    
    orchestrator.process_snapshot(mock_snapshot)
    
    snap2 = make_snapshot(mock_snapshot.timestamp + timedelta(minutes=1), "snap_124")
    mock_dependencies["detector"].observe.return_value = None
    spec2 = orchestrator.process_snapshot(snap2)
    
    assert spec2 is None
    bow = orchestrator._active_windows["cand_snap_123"]
    assert bow._timeline.frame_count() == 2
    mock_dependencies["observers"][0].observe.assert_not_called()

def test_multi_frame_freeze(mock_snapshot, mock_dependencies):
    policy_config = ObservationConfig(schema_version="1.0.0", max_frames=3, max_duration=3600.0)
    policy = DefaultObservationPolicy(policy_config)
    orchestrator = create_orchestrator(mock_dependencies, policy)
    
    orchestrator.process_snapshot(mock_snapshot)
    
    snap2 = make_snapshot(mock_snapshot.timestamp + timedelta(minutes=1), "snap_124")
    mock_dependencies["detector"].observe.return_value = None
    orchestrator.process_snapshot(snap2)
    
    snap3 = make_snapshot(mock_snapshot.timestamp + timedelta(minutes=2), "snap_125")
    orchestrator.process_snapshot(snap3)
    
    timeline_arg = mock_dependencies["observers"][0].observe.call_args[0][0]
    assert len(timeline_arg.frames) == 3

def test_genuine_observer_compatibility(mock_snapshot, mock_dependencies):
    velocity_config = VelocityObserverConfig("1.0.0", {"1.0": 1})
    mock_engine = MagicMock(spec=ReplayEngineContract)
    # mock engine behavior
    cursor_mock1 = MagicMock()
    cursor_mock1.current_frame = MagicMock(behavior_strength="1.0")
    cursor_mock1.status = ReplayState.PLAYING
    
    cursor_mock2 = MagicMock()
    cursor_mock2.current_frame = MagicMock(behavior_strength="1.0")
    cursor_mock2.status = ReplayState.COMPLETE
    
    mock_engine.step.side_effect = [cursor_mock1, cursor_mock2]
    
    velocity_observer = VelocityObserver(velocity_config, mock_engine)
    
    orchestrator = DeploymentOrchestrator(
        runtime=mock_dependencies["runtime"],
        detector=mock_dependencies["detector"],
        observers=(velocity_observer,),
        profile_engine=mock_dependencies["profile_engine"],
        risk_model=mock_dependencies["risk_model"],
        position_sizer=mock_dependencies["position_sizer"],
        observation_policy=mock_dependencies["observation_policy"] # max_frames=2
    )
    
    orchestrator.process_snapshot(mock_snapshot)
    
    snap2 = make_snapshot(mock_snapshot.timestamp + timedelta(minutes=1), "snap_124")
    mock_dependencies["detector"].observe.return_value = None
    orchestrator.process_snapshot(snap2)
    
    evidence_package = mock_dependencies["profile_engine"].build_profile.call_args[0][0]
    velocity_evidence = evidence_package.evidence[0]
    
    assert velocity_evidence.observer_name == "VelocityObserver"
    assert velocity_evidence.observed is True

def test_policy_is_actually_used(mock_snapshot, mock_dependencies):
    policy_config = ObservationConfig(schema_version="1.0.0", max_frames=5, max_duration=3600.0)
    policy = DefaultObservationPolicy(policy_config)
    orchestrator = create_orchestrator(mock_dependencies, policy)
    
    orchestrator.process_snapshot(mock_snapshot)
    mock_dependencies["detector"].observe.return_value = None
    
    for i in range(1, 4):
        snap = make_snapshot(mock_snapshot.timestamp + timedelta(minutes=i), f"snap_{i}")
        orchestrator.process_snapshot(snap)
        assert len(orchestrator._active_candidates) == 1
    
    snap5 = make_snapshot(mock_snapshot.timestamp + timedelta(minutes=4), "snap_4")
    orchestrator.process_snapshot(snap5)
    assert len(orchestrator._active_candidates) == 0

def test_multiple_candidates_and_deterministic_order(mock_snapshot, mock_dependencies):
    policy_config = ObservationConfig(schema_version="1.0.0", max_frames=3, max_duration=3600.0)
    policy = DefaultObservationPolicy(policy_config)
    orchestrator = create_orchestrator(mock_dependencies, policy)
    
    orchestrator.process_snapshot(mock_snapshot)
    
    snap2 = make_snapshot(mock_snapshot.timestamp + timedelta(minutes=1), "snap_124")
    mock_dependencies["detector"].observe.return_value = make_observation("snap_124", snap2.timestamp)
    orchestrator.process_snapshot(snap2)
    
    assert list(orchestrator._active_candidates.keys()) == ["cand_snap_123", "cand_snap_124"]
    assert orchestrator._active_windows["cand_snap_123"]._timeline.frame_count() == 2
    assert orchestrator._active_windows["cand_snap_124"]._timeline.frame_count() == 1
    
    snap3 = make_snapshot(mock_snapshot.timestamp + timedelta(minutes=2), "snap_125")
    mock_dependencies["detector"].observe.return_value = make_observation("snap_125", snap3.timestamp)
    orchestrator.process_snapshot(snap3)
    
    assert list(orchestrator._active_candidates.keys()) == ["cand_snap_124", "cand_snap_125"]
    assert orchestrator._active_windows["cand_snap_124"]._timeline.frame_count() == 2
    assert orchestrator._active_windows["cand_snap_125"]._timeline.frame_count() == 1

def test_candidate_specific_termination_reason(mock_snapshot, mock_dependencies):
    class CustomPolicy(ObservationPolicyContract):
        def __init__(self):
            self._config = ObservationConfig("1.0.0", 5, 3600.0)
        @property
        def policy_id(self): return "custom"
        @property
        def policy_version(self): return "1.0.0"
        @property
        def config(self): return self._config
        def evaluate(self, current_timestamp, frame_count, elapsed_duration):
            if elapsed_duration >= 60:
                return ObservationDecision(False, True, TerminationReason.MAX_DURATION, "c", "1", current_timestamp)
            elif frame_count == 3:
                return ObservationDecision(False, True, TerminationReason.WINDOW_COMPLETE, "c", "1", current_timestamp)
            return ObservationDecision(True, False, None, "c", "1", current_timestamp)
            
    orchestrator = create_orchestrator(mock_dependencies, CustomPolicy())
    
    dt0 = mock_snapshot.timestamp
    orchestrator.process_snapshot(mock_snapshot)
    
    snap2 = make_snapshot(dt0 + timedelta(seconds=10), "snap_124")
    mock_dependencies["detector"].observe.return_value = make_observation("snap_124", snap2.timestamp)
    orchestrator.process_snapshot(snap2)
    
    snap3 = make_snapshot(dt0 + timedelta(seconds=20), "snap_125")
    mock_dependencies["detector"].observe.return_value = None
    
    timelines_observed = []
    def mock_observer_side_effect(timeline):
        timelines_observed.append(timeline)
        return Evidence(
            evidence_id="ev_123", candidate_id=timeline.candidate_id, timeline_id=timeline.timeline_id,
            observer_name="mock", observer_version="1.0", evidence_type="MOCK", confidence=0.9,
            observed=True, evidence_labels=(), metadata=MappingProxyType({}), timestamp=dt0
        )
    mock_dependencies["observers"][0].observe.side_effect = mock_observer_side_effect
    
    # Snap 3 terminates Cand A on WINDOW_COMPLETE
    orchestrator.process_snapshot(snap3)
    
    # Snap 4 terminates Cand B on MAX_DURATION (it jumps to 80s, elapsed for Cand B is 70s)
    snap4 = make_snapshot(dt0 + timedelta(seconds=80), "snap_126")
    orchestrator.process_snapshot(snap4)
    
    assert len(orchestrator._active_candidates) == 0
    assert len(timelines_observed) == 2
    
    timeline_a = timelines_observed[0]
    timeline_b = timelines_observed[1]
    
    assert timeline_a.candidate_id == "cand_snap_123"
    assert timeline_a.termination_reason == TerminationReason.WINDOW_COMPLETE.value
    
    assert timeline_b.candidate_id == "cand_snap_124"
    assert timeline_b.termination_reason == TerminationReason.MAX_DURATION.value


def test_downstream_failure_recovery_E5(mock_snapshot, mock_dependencies):
    policy_config = ObservationConfig(schema_version="1.0.0", max_frames=3, max_duration=3600.0)
    policy = DefaultObservationPolicy(policy_config)
    orchestrator = create_orchestrator(mock_dependencies, policy)
    
    dt0 = mock_snapshot.timestamp
    # 1. Create Cand A (t=0, frame_count=1)
    orchestrator.process_snapshot(mock_snapshot)
    
    # 2. Create Cand B (t=1m)
    # Cand A appends, frame_count=2
    snap2 = make_snapshot(dt0 + timedelta(minutes=1), "snap_124")
    mock_dependencies["detector"].observe.return_value = make_observation("snap_124", snap2.timestamp)
    orchestrator.process_snapshot(snap2)
    
    # 3. Cause downstream failure during Cand A's termination
    # Cand A will hit max_frames=3 on snap3.
    snap3 = make_snapshot(dt0 + timedelta(minutes=2), "snap_125")
    mock_dependencies["detector"].observe.return_value = None
    
    # Poison the observer for Cand A
    def mock_observer_side_effect(timeline):
        if timeline.candidate_id == "cand_snap_123":
            raise ValueError("Intentional Observer Failure for Cand A")
        return Evidence(
            evidence_id="ev_123", candidate_id=timeline.candidate_id, timeline_id=timeline.timeline_id,
            observer_name="mock", observer_version="1.0", evidence_type="MOCK", confidence=0.9,
            observed=True, evidence_labels=(), metadata=MappingProxyType({}), timestamp=timeline.closed_timestamp
        )
    mock_dependencies["observers"][0].observe.side_effect = mock_observer_side_effect
    
    # 4. Assert original exception propagates
    with pytest.raises(PipelineExecutionError) as exc_info:
        orchestrator.process_snapshot(snap3)
    assert "Intentional Observer Failure for Cand A" in str(exc_info.value)
    
    # 5. Assert Cand A is removed
    assert "cand_snap_123" not in orchestrator._active_candidates
    assert "cand_snap_123" not in orchestrator._active_windows
    assert "cand_snap_123" not in orchestrator._candidate_decisions
    
    # 6. Assert Cand B remains active
    assert "cand_snap_124" in orchestrator._active_candidates
    bow_b = orchestrator._active_windows["cand_snap_124"]
    # Cand B had 1 frame at snap2. On snap3, it received the append in Phase 1 before the freeze exception in Phase 2!
    assert bow_b._timeline.frame_count() == 2
    
    # 7. Process another snapshot for Cand B
    # Cand B now has 2 frames. On snap4 it hits 3 frames and terminates successfully.
    snap4 = make_snapshot(dt0 + timedelta(minutes=3), "snap_126")
    spec = orchestrator.process_snapshot(snap4)
    
    # 8-10. Assert B continues normally and orchestrator is not wedged
    assert spec is not None
    assert "cand_snap_124" not in orchestrator._active_candidates
