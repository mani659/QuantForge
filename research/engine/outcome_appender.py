from datetime import datetime, timezone
from types import MappingProxyType

from research.experiment_recorder import ExperimentRecorder
from research.lifecycle.deployment_outcome import DeploymentOutcome
from research.lifecycle.provenance import Provenance
from boe.execution.result import ExecutionResult

from research.engine.configuration import ExperimentConfiguration
from research.engine.strategy_contract import ResearchStrategyContract


class ResearchOutcomeAppender:
    """
    Bridges the Research Run execution results into the frozen ExperimentRecorder.
    Translates Research entities (ExperimentConfiguration) into the legacy
    DeploymentOutcome format required by the recorder.
    """
    def __init__(self, recorder: ExperimentRecorder):
        self.recorder = recorder

    def append(
        self, 
        execution_result: ExecutionResult, 
        strategy: ResearchStrategyContract,
        config: ExperimentConfiguration,
        experiment_id: str
    ) -> str:
        """
        Translates and appends a single execution result to the experiment ledger.
        """
        # Create a synthetic provenance to satisfy frozen legacy contracts.
        # This maps the Research Engine identity into the BOE identity space.
        provenance = Provenance(
            research_candidate_id=f"candidate_{experiment_id}",
            validation_id="research_run_validation",
            experiment_id=experiment_id,
            strategy_manifest_id=strategy.strategy_id,
            created_timestamp=execution_result.timestamp
        )

        execution_metadata = dict(execution_result.metadata)

        deployment_metadata = {
            "strategy_id": strategy.strategy_id,
            "strategy_version": strategy.version,
            "dataset_id": config.dataset_id,
            "instrument": config.instrument,
            "timeframe": config.timeframe,
            "deployment_timestamp": execution_result.timestamp.isoformat(),
        }

        outcome = DeploymentOutcome(
            outcome_id=f"outcome_{experiment_id}_{execution_result.timestamp.isoformat()}",
            strategy_manifest_id=strategy.strategy_id,
            provenance=provenance,
            execution_reference=execution_result.candidate_id,
            execution_metadata=MappingProxyType(execution_metadata),
            deployment_metadata=MappingProxyType(deployment_metadata),
            recorded_timestamp=execution_result.timestamp,
            schema_version="1.0.0",
        )

        return self.recorder.append_deployment_outcome(outcome)
