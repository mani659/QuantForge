from typing import Tuple
from types import MappingProxyType

from boe.deployment.runtime import DeploymentRuntime
from boe.temporal.environment_snapshot import EnvironmentSnapshot
from boe.observation_environment import ObservationEnvironment
from boe.behavior_detector_contract import BehaviorDetectorContract
from boe.candidate import Candidate
from boe.candidate_state import CandidateState
from boe.observation.bow import BehaviorObservationWindow
from boe.observation.termination_reason import TerminationReason
from boe.evidence.observer_contract import ObserverContract
from boe.evidence.evidence import EvidencePackage
from boe.profile.engine import BehaviourProfileEngine
from boe.risk.models import RiskModelContract
from boe.risk.position_sizer import PositionSizerContract
from boe.risk.specification import PositionSpecification
from boe.risk.assessment import RiskAssessment
from boe.deployment.orchestrator_errors import PipelineExecutionError

class DeploymentOrchestrator:
    """
    Coordinates the execution of the full BOE pipeline per EnvironmentSnapshot.
    Maintains NO internal state across snapshots to guarantee determinism.
    
    DeploymentOrchestrator ends at PositionSpecification. 
    Execution belongs exclusively to the Execution Domain.
    """

    def __init__(
        self,
        runtime: DeploymentRuntime,
        detector: BehaviorDetectorContract,
        observers: Tuple[ObserverContract, ...],
        profile_engine: BehaviourProfileEngine,
        risk_model: RiskModelContract,
        position_sizer: PositionSizerContract
    ):
        self._runtime = runtime
        self._detector = detector
        self._observers = observers
        self._profile_engine = profile_engine
        self._risk_model = risk_model
        self._position_sizer = position_sizer

    def process_snapshot(self, snapshot: EnvironmentSnapshot) -> PositionSpecification | None:
        """
        Executes the BOE pipeline for a single EnvironmentSnapshot.
        Returns a PositionSpecification if the pipeline approves execution, else None.
        """
        try:
            # 1. Observation
            obs_env = ObservationEnvironment(
                schema_version="1.0.0",
                environment_id=snapshot.snapshot_id,
                instrument=snapshot.instrument,
                timeframe=snapshot.timeframe,
                observed_at=snapshot.timestamp,
                market_snapshot=(snapshot.market_state,)
            )
            
            behavior_observation = self._detector.observe(obs_env)
            if not behavior_observation:
                return None
                
            # 2. Transient Candidate & BOW
            candidate = Candidate(
                schema_version="1.0.0",
                candidate_id=f"cand_{snapshot.snapshot_id}",
                observation=behavior_observation,
                state=CandidateState.OBSERVING,
                created_at=snapshot.timestamp,
                updated_at=snapshot.timestamp,
                revision=1,
                event_history=()
            )
            
            bow = BehaviorObservationWindow()
            bow.open(
                candidate=candidate,
                timeline_id=f"timeline_{snapshot.snapshot_id}",
                current_timestamp=snapshot.timestamp
            )
            bow.append_snapshot(
                snapshot=snapshot,
                frame_id=f"frame_{snapshot.snapshot_id}",
                behavior_state=behavior_observation.behavior_type,
                behavior_strength="1.0",
                metadata={}
            )
            
            # Immediately freeze to produce a 1-frame FrozenBehaviorTimeline
            bow_result = bow.freeze(
                closed_timestamp=snapshot.timestamp,
                termination_reason=TerminationReason.WINDOW_COMPLETE
            )
            
            # 3. Evidence
            evidence_list = []
            for observer in self._observers:
                evidence = observer.observe(bow_result.timeline)
                evidence_list.append(evidence)
                
            evidence_package = EvidencePackage(
                candidate_id=candidate.candidate_id,
                timeline_id=bow_result.timeline.timeline_id,
                observation_id=behavior_observation.observation_id,
                evidence_version="1.0.0",
                collection_timestamp=snapshot.timestamp,
                evidence=tuple(evidence_list),
                schema_version="1.0.0",
                metadata=MappingProxyType({})
            )
            
            # 4. Behaviour Profile
            behaviour_profile = self._profile_engine.build_profile(evidence_package)
            
            # 5. Interpretation
            interpretation = self._runtime.interpretation_model.interpret(behaviour_profile)
            
            # 6. Decision
            decision = self._runtime.decision_policy.evaluate(interpretation, snapshot.timestamp)
            
            # 7. Risk
            risk_profile = self._risk_model.evaluate(decision, snapshot.timestamp)
            risk_evaluation = self._runtime.risk_policy.evaluate(decision, risk_profile, snapshot.timestamp)
            risk_assessment = RiskAssessment.from_policy_evaluation(risk_evaluation, snapshot.timestamp)
            
            # 8. PositionSpecification
            sizing_result = self._position_sizer.size_position(risk_assessment, snapshot.timestamp)
            position_specification = PositionSpecification.from_sizing_result(sizing_result, snapshot.timestamp)
            
            return position_specification

        except Exception as e:
            raise PipelineExecutionError(f"Pipeline execution failed: {str(e)}") from e
