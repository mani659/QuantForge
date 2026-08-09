import pytest
from datetime import datetime
from unittest.mock import MagicMock

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
from boe.interpretation.models import InterpretationModelContract
from boe.decision.policy import DecisionPolicyContract
from boe.risk.policy import RiskPolicyContract

from boe.deployment.orchestrator import DeploymentOrchestrator
from boe.deployment.orchestrator_errors import PipelineExecutionError

@pytest.fixture
def mock_snapshot():
    return EnvironmentSnapshot(
        schema_version="1.0.0",
        snapshot_id="snap_123",
        instrument="EURUSD",
        timeframe="H1",
        timestamp=datetime(2026, 1, 1, 12, 0, 0),
        source="MT5",
        market_state={"close": 1.1000}
    )

@pytest.fixture
def mock_dependencies():
    # Setup Mocks
    mock_runtime = MagicMock(spec=DeploymentRuntime)
    mock_detector = MagicMock(spec=BehaviorDetectorContract)
    mock_observer = MagicMock(spec=ObserverContract)
    mock_profile_engine = MagicMock(spec=BehaviourProfileEngine)
    mock_risk_model = MagicMock(spec=RiskModelContract)
    mock_position_sizer = MagicMock(spec=PositionSizerContract)
    
    # 1. Detector
    mock_obs = BehaviorObservation(
        schema_version="1.0.0",
        observation_id="obs_123",
        environment_id="snap_123",
        behavior_type="TEST_BEHAVIOR",
        instrument="EURUSD",
        timeframe="H1",
        observed_at=datetime(2026, 1, 1, 12, 0, 0),
        detector_id="det_1",
        detector_version="1.0.0"
    )
    mock_detector.observe.return_value = mock_obs
    
    from types import MappingProxyType
    # 3. Evidence
    mock_ev = Evidence(
        evidence_id="ev_123",
        candidate_id="cand_snap_123",
        timeline_id="timeline_snap_123",
        observer_name="mock_observer",
        observer_version="1.0.0",
        evidence_type="MOCK_EVIDENCE",
        confidence=0.9,
        observed=True,
        evidence_labels=("test",),
        metadata=MappingProxyType({}),
        timestamp=datetime(2026, 1, 1, 12, 0, 0)
    )
    mock_observer.observe.return_value = mock_ev
    
    # 4. Profile
    mock_prof = MagicMock(spec=BehaviourProfile)
    mock_profile_engine.build_profile.return_value = mock_prof
    
    # 5. Interpretation
    mock_interp = MagicMock(spec=Interpretation)
    mock_runtime.interpretation_model.interpret.return_value = mock_interp
    
    # 6. Decision
    mock_dec = MagicMock(spec=Decision)
    mock_runtime.decision_policy.evaluate.return_value = mock_dec
    
    # 7. Risk
    mock_risk_prof = MagicMock(spec=RiskProfile)
    mock_risk_model.evaluate.return_value = mock_risk_prof
    
    mock_risk_eval = MagicMock(spec=RiskPolicyEvaluation)
    mock_risk_eval.action = RiskPolicyAction.APPROVE
    mock_risk_eval.candidate_id = "cand_123"
    mock_risk_eval.timeline_id = "timeline_123"
    mock_risk_eval.observation_id = "obs_123"
    mock_risk_eval.rationale = "Test"
    mock_risk_eval.metadata = {"policy": "TestPolicy"}
    
    mock_runtime.risk_policy.evaluate.return_value = mock_risk_eval
    # 8. Position Sizer
    mock_sizing_result = MagicMock(spec=PositionSizingResult)
    mock_sizing_result.candidate_id = "cand_123"
    mock_sizing_result.timeline_id = "timeline_123"
    mock_sizing_result.observation_id = "obs_123"
    mock_sizing_result.position_size_multiplier = 1.0
    mock_sizing_result.exposure_fraction = 0.02
    mock_sizing_result.risk_units = 1.0
    mock_sizing_result.metadata = {"sizer": "mock"}
    
    mock_position_sizer.size_position.return_value = mock_sizing_result
    
    return {
        "runtime": mock_runtime,
        "detector": mock_detector,
        "observers": (mock_observer,),
        "profile_engine": mock_profile_engine,
        "risk_model": mock_risk_model,
        "position_sizer": mock_position_sizer,
        "outputs": {
            "observation": mock_obs,
            "evidence": mock_ev,
            "profile": mock_prof,
            "interpretation": mock_interp,
            "decision": mock_dec,
            "risk_profile": mock_risk_prof,
            "risk_evaluation": mock_risk_eval,
            "sizing_result": mock_sizing_result
        }
    }

def test_deployment_orchestrator_successful_pipeline(mock_snapshot, mock_dependencies):
    orchestrator = DeploymentOrchestrator(
        runtime=mock_dependencies["runtime"],
        detector=mock_dependencies["detector"],
        observers=mock_dependencies["observers"],
        profile_engine=mock_dependencies["profile_engine"],
        risk_model=mock_dependencies["risk_model"],
        position_sizer=mock_dependencies["position_sizer"]
    )
    
    spec = orchestrator.process_snapshot(mock_snapshot)
    
    # Verify the return value
    assert isinstance(spec, PositionSpecification)
    assert spec.position_size_multiplier == 1.0
    
    # Verify the calls were made with precise arguments
    dt = mock_snapshot.timestamp
    outputs = mock_dependencies["outputs"]
    
    from unittest.mock import ANY
    mock_dependencies["detector"].observe.assert_called_once_with(ANY)
    mock_dependencies["observers"][0].observe.assert_called_once_with(ANY)
    mock_dependencies["profile_engine"].build_profile.assert_called_once_with(ANY)
    mock_dependencies["runtime"].interpretation_model.interpret.assert_called_once_with(outputs["profile"])
    mock_dependencies["runtime"].decision_policy.evaluate.assert_called_once_with(outputs["interpretation"], dt)
    mock_dependencies["risk_model"].evaluate.assert_called_once_with(outputs["decision"], dt)
    mock_dependencies["runtime"].risk_policy.evaluate.assert_called_once_with(outputs["decision"], outputs["risk_profile"], dt)
    
    # Verify the position sizer was called with a RiskAssessment, not a RiskPolicyEvaluation
    sizer_calls = mock_dependencies["position_sizer"].size_position.call_args_list
    assert len(sizer_calls) == 1
    assessment_arg, timestamp_arg = sizer_calls[0][0]
    assert isinstance(assessment_arg, RiskAssessment)
    assert assessment_arg.status == AssessmentStatus.APPROVED
    assert timestamp_arg == dt

def test_deployment_orchestrator_no_behavior_detected(mock_snapshot, mock_dependencies):
    mock_dependencies["detector"].observe.return_value = None
    
    orchestrator = DeploymentOrchestrator(
        runtime=mock_dependencies["runtime"],
        detector=mock_dependencies["detector"],
        observers=mock_dependencies["observers"],
        profile_engine=mock_dependencies["profile_engine"],
        risk_model=mock_dependencies["risk_model"],
        position_sizer=mock_dependencies["position_sizer"]
    )
    
    spec = orchestrator.process_snapshot(mock_snapshot)
    
    assert spec is None
    # Ensure nothing else was called
    mock_dependencies["observers"][0].observe.assert_not_called()

def test_deployment_orchestrator_pipeline_failure_preserves_determinism(mock_snapshot, mock_dependencies):
    # Simulate an error mid-pipeline (e.g. Risk Policy fails)
    mock_dependencies["runtime"].risk_policy.evaluate.side_effect = ValueError("Risk Policy Error")
    
    orchestrator = DeploymentOrchestrator(
        runtime=mock_dependencies["runtime"],
        detector=mock_dependencies["detector"],
        observers=mock_dependencies["observers"],
        profile_engine=mock_dependencies["profile_engine"],
        risk_model=mock_dependencies["risk_model"],
        position_sizer=mock_dependencies["position_sizer"]
    )
    
    with pytest.raises(PipelineExecutionError) as exc_info:
        orchestrator.process_snapshot(mock_snapshot)
        
    assert "Pipeline execution failed: Risk Policy Error" in str(exc_info.value)
    
    # Verify position sizer was NOT called (no partial execution)
    mock_dependencies["position_sizer"].size_position.assert_not_called()
