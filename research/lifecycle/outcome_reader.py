"""Immutable deployment evidence reader for the Research Lifecycle domain.

Phase 8.3 — Research Industrialization.
OutcomeReader is a stateless, deterministic, read-only application service. It
locates, retrieves, deserializes, validates, and returns immutable
DeploymentOutcome artifacts persisted by the ExperimentRecorder. It performs
no analysis, classification, scoring, ranking, optimisation, recommendation,
inference, evaluation, or promotion. Its responsibility ends immediately after
returning immutable DeploymentOutcome objects to human researchers.

The automated system terminates at OutcomeReader. Human Research Review is
outside QuantForge software.
"""

from datetime import datetime
from types import MappingProxyType

from research.lifecycle.deployment_outcome import DeploymentOutcome
from research.lifecycle.provenance import Provenance
from research.lifecycle.research_errors import InvalidDeploymentOutcomeData


DEPLOYMENT_OUTCOME_FILENAME = "deployment_outcome.json"


class OutcomeReader:
    """Stateless read-only application service for DeploymentOutcome evidence.

    Responsibilities are limited to:
        1. locate   — find persisted DeploymentOutcome artifacts
        2. retrieve — read the raw artifact
        3. deserialize — reconstruct the immutable DeploymentOutcome
        4. validate — verify artifact integrity
        5. return   — yield immutable DeploymentOutcome objects

    The reader holds no runtime state, no caches, no background workers, no
    events, and no scheduling. Repeated reads produce identical results.
    """

    def __init__(self, recorder):
        """Initialize the OutcomeReader against a persistence backend.

        Args:
            recorder: The ExperimentRecorder instance that provides the
                      read-only retrieval API.
        """
        self.recorder = recorder

    # ------------------------------------------------------------------
    # locate
    # ------------------------------------------------------------------

    def locate(self):
        """Locate all persisted DeploymentOutcome run identifiers.

        Returns:
            tuple[str, ...]: Sorted run identifiers that contain a persisted
            deployment_outcome.json artifact.
        """
        return self.recorder.list_deployment_outcomes()

    # ------------------------------------------------------------------
    # retrieve
    # ------------------------------------------------------------------

    def retrieve(self, run_id):
        """Retrieve the raw artifact data for a given run.

        Args:
            run_id (str): The run identifier (e.g. 'run_000001').

        Returns:
            dict: The raw persisted artifact data.

        Raises:
            InvalidDeploymentOutcomeData: If the artifact cannot be located.
        """
        try:
            return self.recorder.get_deployment_outcome(run_id)
        except ValueError as exc:
            raise InvalidDeploymentOutcomeData(str(exc)) from exc

    # ------------------------------------------------------------------
    # deserialize
    # ------------------------------------------------------------------

    def deserialize(self, artifact: dict) -> DeploymentOutcome:
        """Deserialize raw artifact data into an immutable DeploymentOutcome.

        Args:
            artifact (dict): The raw persisted artifact data.

        Returns:
            DeploymentOutcome: The reconstructed immutable evidence artifact.

        Raises:
            InvalidDeploymentOutcomeData: If the artifact is malformed.
        """
        if not isinstance(artifact, dict):
            raise InvalidDeploymentOutcomeData(
                "OutcomeReader deserialize requires a dict artifact."
            )

        provenance_data = artifact.get("provenance")
        if not isinstance(provenance_data, dict):
            raise InvalidDeploymentOutcomeData(
                "OutcomeReader artifact is missing a provenance object."
            )

        try:
            created_timestamp = datetime.fromisoformat(
                provenance_data.get("created_timestamp")
            )
            recorded_timestamp = datetime.fromisoformat(
                artifact.get("recorded_timestamp")
            )
        except (TypeError, ValueError) as exc:
            raise InvalidDeploymentOutcomeData(
                "OutcomeReader artifact contains an invalid timestamp."
            ) from exc

        provenance = Provenance(
            research_candidate_id=provenance_data.get("research_candidate_id"),
            validation_id=provenance_data.get("validation_id"),
            experiment_id=provenance_data.get("experiment_id"),
            strategy_manifest_id=provenance_data.get("strategy_manifest_id"),
            created_timestamp=created_timestamp,
        )

        return DeploymentOutcome(
            outcome_id=artifact.get("outcome_id"),
            strategy_manifest_id=artifact.get("strategy_manifest_id"),
            provenance=provenance,
            execution_reference=artifact.get("execution_reference"),
            execution_metadata=MappingProxyType(
                dict(artifact.get("execution_metadata") or {})
            ),
            deployment_metadata=MappingProxyType(
                dict(artifact.get("deployment_metadata") or {})
            ),
            recorded_timestamp=recorded_timestamp,
            schema_version=artifact.get("schema_version"),
        )

    # ------------------------------------------------------------------
    # validate
    # ------------------------------------------------------------------

    def validate(self, artifact: dict) -> bool:
        """Validate the integrity of a raw artifact.

        Verification is a full round-trip: the artifact must deserialize into
        a valid immutable DeploymentOutcome and round-trip back to the exact
        same artifact data. This detects tampering, truncation, and
        non-deterministic reconstruction without performing any analysis,
        classification, or scoring.

        Args:
            artifact (dict): The raw persisted artifact data.

        Returns:
            bool: True if the artifact is valid and constitutional.

        Raises:
            InvalidDeploymentOutcomeData: If validation fails.
        """
        outcome = self.deserialize(artifact)

        # Explicit integrity checks required by the frozen specification:
        # non-empty identifiers, canonical schema_version pattern, and
        # immutable MappingProxyType metadata.
        for field_name in ("outcome_id", "strategy_manifest_id", "execution_reference"):
            value = getattr(outcome, field_name)
            if not isinstance(value, str) or not value.strip():
                raise InvalidDeploymentOutcomeData(
                    f"OutcomeReader artifact {field_name} must be a non-empty string."
                )

        schema_version = outcome.schema_version
        parts = schema_version.split(".")
        if len(parts) != 3 or not all(part.isdigit() for part in parts):
            raise InvalidDeploymentOutcomeData(
                "OutcomeReader artifact schema_version must match the pattern "
                "'major.minor.patch' (e.g. '1.0.0')."
            )

        if not isinstance(outcome.execution_metadata, MappingProxyType):
            raise InvalidDeploymentOutcomeData(
                "OutcomeReader artifact execution_metadata must be immutable."
            )
        if not isinstance(outcome.deployment_metadata, MappingProxyType):
            raise InvalidDeploymentOutcomeData(
                "OutcomeReader artifact deployment_metadata must be immutable."
            )

        # Round-trip equality against the source artifact verifies determinism,
        # integrity, and absence of tampering.
        if self._to_artifact(outcome) != self._canonical(artifact):
            raise InvalidDeploymentOutcomeData(
                "OutcomeReader artifact failed round-trip integrity validation."
            )
        return True

    # ------------------------------------------------------------------
    # return
    # ------------------------------------------------------------------

    def read(self, run_id) -> DeploymentOutcome:
        """Return a single immutable DeploymentOutcome for a given run.

        Args:
            run_id (str): The run identifier (e.g. 'run_000001').

        Returns:
            DeploymentOutcome: The immutable evidence artifact.
        """
        artifact = self.retrieve(run_id)
        self.validate(artifact)
        return self.deserialize(artifact)

    def read_all(self) -> tuple:
        """Return all immutable DeploymentOutcome artifacts.

        Returns:
            tuple[DeploymentOutcome, ...]: All immutable evidence artifacts in
            deterministic order.
        """
        outcomes = []
        for run_id in self.locate():
            outcomes.append(self.read(run_id))
        return tuple(outcomes)

    # ------------------------------------------------------------------
    # internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _canonical(artifact: dict) -> dict:
        """Normalize a raw artifact to its canonical key set.

        Used solely for integrity round-trip comparison. Unknown or extra keys
        are excluded so the comparison focuses on the scientific artifact
        fields.
        """
        return {
            "schema_version": artifact.get("schema_version"),
            "outcome_id": artifact.get("outcome_id"),
            "strategy_manifest_id": artifact.get("strategy_manifest_id"),
            "execution_reference": artifact.get("execution_reference"),
            "execution_metadata": artifact.get("execution_metadata") or {},
            "deployment_metadata": artifact.get("deployment_metadata") or {},
            "recorded_timestamp": artifact.get("recorded_timestamp"),
            "provenance": artifact.get("provenance") or {},
        }

    @staticmethod
    def _to_artifact(outcome: DeploymentOutcome) -> dict:
        """Reconstruct the canonical artifact representation of an outcome.

        This mirrors the ExperimentRecorder persistence format exactly and is
        used solely for integrity round-trip validation. It performs no
        analysis or interpretation.
        """
        return {
            "schema_version": outcome.schema_version,
            "outcome_id": outcome.outcome_id,
            "strategy_manifest_id": outcome.strategy_manifest_id,
            "execution_reference": outcome.execution_reference,
            "execution_metadata": dict(outcome.execution_metadata),
            "deployment_metadata": dict(outcome.deployment_metadata),
            "recorded_timestamp": outcome.recorded_timestamp.isoformat(),
            "provenance": {
                "research_candidate_id": outcome.provenance.research_candidate_id,
                "validation_id": outcome.provenance.validation_id,
                "experiment_id": outcome.provenance.experiment_id,
                "strategy_manifest_id": outcome.provenance.strategy_manifest_id,
                "created_timestamp": outcome.provenance.created_timestamp.isoformat(),
            },
        }
