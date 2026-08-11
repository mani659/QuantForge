from typing import Tuple, Dict
from types import MappingProxyType

from boe.deployment.runtime import DeploymentRuntime
from boe.temporal.environment_snapshot import EnvironmentSnapshot
from boe.observation_environment import ObservationEnvironment
from boe.behavior_detector_contract import BehaviorDetectorContract
from boe.candidate import Candidate
from boe.candidate_state import CandidateState
from boe.observation.bow import BehaviorObservationWindow
from boe.observation.observation_contract import ObservationPolicyContract
from boe.observation.observation_result import ObservationDecision
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
    Maintains active observation windows across snapshots to produce genuine
    multi-frame temporal timelines.
    
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
        position_sizer: PositionSizerContract,
        observation_policy: ObservationPolicyContract
    ):
        self._runtime = runtime
        self._detector = detector
        self._observers = observers
        self._profile_engine = profile_engine
        self._risk_model = risk_model
        self._position_sizer = position_sizer
        self._observation_policy = observation_policy
        
        # Stateful Observation Lifecycle
        self._active_candidates: Dict[str, Candidate] = {}
        self._active_windows: Dict[str, BehaviorObservationWindow] = {}
        self._candidate_decisions: Dict[str, ObservationDecision] = {}

    def process_snapshot(self, snapshot: EnvironmentSnapshot) -> PositionSpecification | None:
        """
        Executes the BOE pipeline for a single EnvironmentSnapshot.
        
        Lifecycle:
        1. Appends snapshot to existing active observation windows.
        2. Evaluates the observation policy for each active window.
        3. Freezes windows that terminate, producing FrozenBehaviorTimelines.
        4. Evaluates the behavior detector to trigger new candidates.
        
        Returns the FIRST successfully generated PositionSpecification, if any.
        """
        try:
            position_spec: PositionSpecification | None = None
            terminated_candidates = []

            # 1. Phase 1 - Existing active observations
            for candidate_id in list(self._active_candidates.keys()):
                candidate = self._active_candidates[candidate_id]
                bow = self._active_windows[candidate_id]
                
                # Append current snapshot
                bow.append_snapshot(
                    snapshot=snapshot,
                    frame_id=f"frame_{snapshot.snapshot_id}_{candidate_id}",
                    behavior_state=candidate.observation.behavior_type,
                    behavior_strength="1.0",
                    metadata={}
                )
                
                # Evaluate Policy
                decision = bow.evaluate_policy(snapshot.timestamp, self._observation_policy)
                
                # Retain decision per-candidate
                self._candidate_decisions[candidate_id] = decision
                
                if decision.terminate_observation:
                    terminated_candidates.append(candidate_id)

            # 2. Process Terminated Observations
            for candidate_id in terminated_candidates:
                candidate = self._active_candidates[candidate_id]
                bow = self._active_windows[candidate_id]
                decision = self._candidate_decisions[candidate_id]
                
                try:
                    # Freeze BOW with candidate-specific termination reason
                    bow_result = bow.freeze(
                        closed_timestamp=snapshot.timestamp,
                        termination_reason=decision.termination_reason
                    )
                    
                    # Continue through downstream pipeline
                    spec = self._process_frozen_timeline(candidate, bow_result, snapshot)
                    if spec is not None and position_spec is None:
                        position_spec = spec
                finally:
                    # Clean up memory deterministically
                    del self._active_candidates[candidate_id]
                    del self._active_windows[candidate_id]
                    del self._candidate_decisions[candidate_id]

            # 3. Phase 2 - New detector triggers
            obs_env = ObservationEnvironment(
                schema_version="1.0.0",
                environment_id=snapshot.snapshot_id,
                instrument=snapshot.instrument,
                timeframe=snapshot.timeframe,
                observed_at=snapshot.timestamp,
                market_snapshot=(snapshot.market_state,)
            )
            
            behavior_observation = self._detector.observe(obs_env)
            if behavior_observation:
                # Deterministic candidate ID based on snapshot and observation
                candidate_id = f"cand_{snapshot.snapshot_id}"
                
                candidate = Candidate(
                    schema_version="1.0.0",
                    candidate_id=candidate_id,
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
                
                # Append trigger snapshot as the first frame
                bow.append_snapshot(
                    snapshot=snapshot,
                    frame_id=f"frame_{snapshot.snapshot_id}_{candidate_id}",
                    behavior_state=behavior_observation.behavior_type,
                    behavior_strength="1.0",
                    metadata={}
                )
                
                # Retain in active state
                self._active_candidates[candidate_id] = candidate
                self._active_windows[candidate_id] = bow
                
            return position_spec

        except Exception as e:
            raise PipelineExecutionError(f"Pipeline execution failed: {str(e)}") from e

    def _process_frozen_timeline(
        self, 
        candidate: Candidate, 
        bow_result, 
        snapshot: EnvironmentSnapshot
    ) -> PositionSpecification | None:
        """Processes a frozen timeline through the remainder of the BOE pipeline."""
        # Evidence
        evidence_list = []
        for observer in self._observers:
            evidence = observer.observe(bow_result.timeline)
            evidence_list.append(evidence)
            
        evidence_package = EvidencePackage(
            candidate_id=candidate.candidate_id,
            timeline_id=bow_result.timeline.timeline_id,
            observation_id=candidate.observation.observation_id,
            evidence_version="1.0.0",
            collection_timestamp=snapshot.timestamp,
            evidence=tuple(evidence_list),
            schema_version="1.0.0",
            metadata=MappingProxyType({})
        )
        
        # Behaviour Profile
        behaviour_profile = self._profile_engine.build_profile(evidence_package)
        
        # Interpretation
        interpretation = self._runtime.interpretation_model.interpret(behaviour_profile)
        
        # Decision
        decision = self._runtime.decision_policy.evaluate(interpretation, snapshot.timestamp)
        
        # Risk
        risk_profile = self._risk_model.evaluate(decision, snapshot.timestamp)
        risk_evaluation = self._runtime.risk_policy.evaluate(decision, risk_profile, snapshot.timestamp)
        risk_assessment = RiskAssessment.from_policy_evaluation(risk_evaluation, snapshot.timestamp)
        
        # PositionSpecification
        sizing_result = self._position_sizer.size_position(risk_assessment, snapshot.timestamp)
        position_specification = PositionSpecification.from_sizing_result(sizing_result, snapshot.timestamp)
        
        return position_specification
