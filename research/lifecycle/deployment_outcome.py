from dataclasses import dataclass
from datetime import datetime
from types import MappingProxyType
from typing import Any
from research.lifecycle.provenance import Provenance
from research.lifecycle.research_errors import InvalidDeploymentOutcomeData

@dataclass(frozen=True)
class DeploymentOutcome:
    """Immutable deployment evidence artifact for QuantForge research lifecycle.

    DeploymentOutcome captures execution results as immutable scientific evidence.
    It contains only references and metadata - no business logic, no runtime state,
    no machine interpretation. Scientific judgement remains exclusively with
    human researchers.

    Sprint 8.2 introduces this domain object to close the research lifecycle.
    """

    outcome_id: str
    strategy_manifest_id: str
    provenance: Provenance
    execution_reference: str
    execution_metadata: MappingProxyType[str, Any]
    deployment_metadata: MappingProxyType[str, Any]
    recorded_timestamp: datetime
    schema_version: str

    def __post_init__(self) -> None:
        """Validate all fields at construction time."""
        required_strings = {
            "outcome_id": self.outcome_id,
            "strategy_manifest_id": self.strategy_manifest_id,
            "execution_reference": self.execution_reference,
            "schema_version": self.schema_version,
        }
        for field_name, value in required_strings.items():
            if not isinstance(value, str) or not value.strip():
                raise InvalidDeploymentOutcomeData(
                    f"DeploymentOutcome {field_name} must be a non-empty string."
                )

        if not isinstance(self.provenance, Provenance):
            raise InvalidDeploymentOutcomeData(
                "DeploymentOutcome provenance must be a Provenance instance."
            )

        if not isinstance(self.execution_metadata, MappingProxyType):
            raise InvalidDeploymentOutcomeData(
                "DeploymentOutcome execution_metadata must be a MappingProxyType."
            )

        if not isinstance(self.deployment_metadata, MappingProxyType):
            raise InvalidDeploymentOutcomeData(
                "DeploymentOutcome deployment_metadata must be a MappingProxyType."
            )

        if not isinstance(self.recorded_timestamp, datetime):
            raise InvalidDeploymentOutcomeData(
                "DeploymentOutcome recorded_timestamp must be a datetime."
            )

        if not self.schema_version or not isinstance(self.schema_version, str):
            raise InvalidDeploymentOutcomeData(
                "DeploymentOutcome schema_version must be a non-empty string."
            )

        self._validate_consumption_rules()

    def _validate_consumption_rules(self) -> None:
        """Ensure DeploymentOutcome adheres to constitutional consumption rules."""

        execution_metadata = dict(self.execution_metadata)

        if execution_metadata:
            warnings = []

            if "supports_hypothesis" in execution_metadata:
                warnings.append(
                    "DeploymentOutcome execution_metadata contains hypothesis evaluation"
                )
            if "challenges_hypothesis" in execution_metadata:
                warnings.append(
                    "DeploymentOutcome execution_metadata contains hypothesis evaluation"
                )
            if "inconclusive" in execution_metadata:
                warnings.append(
                    "DeploymentOutcome execution_metadata contains hypothesis classification"
                )
            if "insufficient_data" in execution_metadata:
                warnings.append(
                    "DeploymentOutcome execution_metadata contains hypothesis classification"
                )
            if "behaviour_correctness" in execution_metadata:
                warnings.append(
                    "DeploymentOutcome execution_metadata contains behavioural judgement"
                )
            if "strategy_quality" in execution_metadata:
                warnings.append(
                    "DeploymentOutcome execution_metadata contains strategy quality assessment"
                )
            if "validation_result" in execution_metadata:
                warnings.append(
                    "DeploymentOutcome execution_metadata contains scientific validation"
                )
            if "scientific_significance" in execution_metadata:
                warnings.append(
                    "DeploymentOutcome execution_metadata contains scientific interpretation"
                )

            if warnings:
                raise InvalidDeploymentOutcomeData(
                    "DeploymentOutcome execution_metadata violates constitutional boundaries: "
                    + "; ".join(warnings)
                )

    def __hash__(self) -> int:
        return hash((
            self.outcome_id,
            self.strategy_manifest_id,
            self.provenance,
            self.execution_reference,
            frozenset(self.execution_metadata.items()),
            frozenset(self.deployment_metadata.items()),
            self.recorded_timestamp,
            self.schema_version,
        ))
