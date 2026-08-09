from typing import TYPE_CHECKING
from types import MappingProxyType
from research.lifecycle.deployment_outcome import DeploymentOutcome
from research.lifecycle.strategy_manifest import StrategyManifest
from research.lifecycle.research_candidate import ResearchCandidate
from boe.execution.result import ExecutionResult
from research.experiment_recorder import ExperimentRecorder

if TYPE_CHECKING:
    pass


class OutcomeAppender:
    """Stateless service for capturing deployment evidence as immutable scientific artifacts.

    Sprint 8.2 introduces this stateless service to bridge frozen execution output
    into the experiment ledger as immutable scientific evidence. It performs no analysis,
    no classification, no scoring, and no scientific reasoning. The automated system
    captures deployment evidence and stops. Scientific interpretation belongs exclusively
    to the human researcher.

    Termination rules:
    OutcomeAppender SHALL NOT:
    - publish downstream events
    - invoke research services
    - trigger lifecycle transitions
    - perform analysis
    - perform optimisation
    - perform promotion
    - perform scientific reasoning

    Its responsibility ends after appending DeploymentOutcome to the ExperimentRecorder.
    """

    def __init__(self, strategy_manifest: StrategyManifest, experiment_recorder: ExperimentRecorder):
        """Initialize OutcomeAppender with required dependencies.

        Args:
            strategy_manifest: The active StrategyManifest (must not be mutated).
            experiment_recorder: The ExperimentRecorder for appending deployment evidence.
        """
        self.strategy_manifest = strategy_manifest
        self.experiment_recorder = experiment_recorder

    def append(self, execution_result: ExecutionResult) -> str:
        """Capture deployment evidence and append it to the experiment ledger.

        Sprint 8.2 captures deployment results as immutable scientific evidence.
        This method constructs a DeploymentOutcome from the frozen ExecutionResult
        and passes it to the ExperimentRecorder. The automated system ends at the
        recorder; scientific interpretation remains with human researchers.

        Args:
            execution_result: The frozen execution result to capture.

        Returns:
            str: The unique identifier for the appended deployment outcome.

        Raises:
            ValueError: If the execution_result is invalid or the outcome violates
                       constitutional boundaries.
        """

        deployment_outcome = self._build_deployment_outcome(execution_result)

        outcome_id = self.experiment_recorder.append_deployment_outcome(deployment_outcome)

        return outcome_id

    def _build_deployment_outcome(self, execution_result: ExecutionResult) -> DeploymentOutcome:
        """Construct a DeploymentOutcome from ExecutionResult and StrategyManifest.

        Args:
            execution_result: The frozen execution result.

        Returns:
            DeploymentOutcome: The immutable deployment evidence artifact.

        Raises:
            ValueError: If construction violates constitutional boundaries.
        """

        from research.lifecycle.research_candidate import ResearchCandidate

        execution_metadata = dict(execution_result.metadata)

        deployment_metadata = {
            "strategy_id": self.strategy_manifest.strategy_id,
            "behaviour_name": self.strategy_manifest.behaviour_name,
            "deployment_timestamp": execution_result.timestamp.isoformat(),
        }

        provenance = self.strategy_manifest.provenance

        recorded_timestamp = execution_result.timestamp

        deployment_outcome = DeploymentOutcome(
            outcome_id=f"outcome_{execution_result.candidate_id}_{execution_result.timestamp.isoformat()}",
            strategy_manifest_id=self.strategy_manifest.strategy_id,
            provenance=provenance,
            execution_reference=execution_result.candidate_id,
            execution_metadata=MappingProxyType(execution_metadata),
            deployment_metadata=MappingProxyType(deployment_metadata),
            recorded_timestamp=recorded_timestamp,
            schema_version="1.0.0",
        )

        return deployment_outcome
