"""Deterministic builder for StrategyManifest construction.

Phase 8.1 — Research Industrialization.
The StrategyManifestBuilder transitions:

    ResearchCandidate → Validated Behaviour → StrategyManifest

The builder performs structural validation. It never creates scientific
decisions. It never interprets evidence. It never executes strategies.
It assembles references deterministically.
"""

from datetime import datetime
import re

from research.lifecycle.provenance import Provenance
from research.lifecycle.research_candidate import ResearchCandidate
from research.lifecycle.research_errors import ManifestBuildError
from research.lifecycle.strategy_manifest import StrategyManifest


SEMANTIC_VERSION_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")


class StrategyManifestBuilder:
    """Deterministic builder that assembles a StrategyManifest from validated inputs.

    Fluent API:
        manifest = (
            StrategyManifestBuilder()
            .with_candidate(candidate)
            .with_validation(validation_id, experiment_id)
            .with_observers(["obs-recoil-001", "obs-persist-001"])
            .with_interpretation_model("interp-mr-001")
            .with_decision_policy("dp-deterministic-001")
            .with_risk_policy("rp-fixed-001")
            .with_deployment_profile("paper")
            .build(strategy_id="strat-001", manifest_version="1.0.0")
        )

    The builder validates completeness at build time. It never creates
    scientific decisions — only structural assembly.
    """

    def __init__(self) -> None:
        self._candidate: ResearchCandidate | None = None
        self._validation_id: str | None = None
        self._experiment_id: str | None = None
        self._observer_ids: tuple[str, ...] | None = None
        self._interpretation_model_id: str | None = None
        self._decision_policy_id: str | None = None
        self._risk_policy_id: str | None = None
        self._deployment_profile: str | None = None

    def with_candidate(self, candidate: ResearchCandidate) -> "StrategyManifestBuilder":
        """Set the originating ResearchCandidate."""
        if not isinstance(candidate, ResearchCandidate):
            raise ManifestBuildError(
                "StrategyManifestBuilder requires a ResearchCandidate instance."
            )
        self._candidate = candidate
        return self

    def with_validation(
        self, validation_id: str, experiment_id: str
    ) -> "StrategyManifestBuilder":
        """Set the validation and experiment references proving the behaviour."""
        if not isinstance(validation_id, str) or not validation_id.strip():
            raise ManifestBuildError(
                "StrategyManifestBuilder validation_id must be a non-empty string."
            )
        if not isinstance(experiment_id, str) or not experiment_id.strip():
            raise ManifestBuildError(
                "StrategyManifestBuilder experiment_id must be a non-empty string."
            )
        self._validation_id = validation_id
        self._experiment_id = experiment_id
        return self

    def with_observers(self, observer_ids: list[str] | tuple[str, ...]) -> "StrategyManifestBuilder":
        """Set the observer identifiers required by this strategy."""
        if not observer_ids:
            raise ManifestBuildError(
                "StrategyManifestBuilder observer_ids must not be empty."
            )
        ids = tuple(observer_ids)
        if not all(isinstance(o, str) and o.strip() for o in ids):
            raise ManifestBuildError(
                "StrategyManifestBuilder observer_ids must be non-empty strings."
            )
        self._observer_ids = ids
        return self

    def with_interpretation_model(self, model_id: str) -> "StrategyManifestBuilder":
        """Set the interpretation model identifier."""
        if not isinstance(model_id, str) or not model_id.strip():
            raise ManifestBuildError(
                "StrategyManifestBuilder interpretation_model_id must be a non-empty string."
            )
        self._interpretation_model_id = model_id
        return self

    def with_decision_policy(self, policy_id: str) -> "StrategyManifestBuilder":
        """Set the decision policy identifier."""
        if not isinstance(policy_id, str) or not policy_id.strip():
            raise ManifestBuildError(
                "StrategyManifestBuilder decision_policy_id must be a non-empty string."
            )
        self._decision_policy_id = policy_id
        return self

    def with_risk_policy(self, policy_id: str) -> "StrategyManifestBuilder":
        """Set the risk policy identifier."""
        if not isinstance(policy_id, str) or not policy_id.strip():
            raise ManifestBuildError(
                "StrategyManifestBuilder risk_policy_id must be a non-empty string."
            )
        self._risk_policy_id = policy_id
        return self

    def with_deployment_profile(self, profile: str) -> "StrategyManifestBuilder":
        """Set the deployment profile (e.g. 'paper', 'demo', 'live')."""
        if not isinstance(profile, str) or not profile.strip():
            raise ManifestBuildError(
                "StrategyManifestBuilder deployment_profile must be a non-empty string."
            )
        self._deployment_profile = profile
        return self

    def build(
        self,
        strategy_id: str,
        manifest_version: str,
        provenance_timestamp: datetime | None = None,
    ) -> StrategyManifest:
        """Build an immutable StrategyManifest with full provenance.

        Args:
            strategy_id: Unique identifier for the strategy.
            manifest_version: Semantic version of the manifest (e.g. '1.0.0').
            provenance_timestamp: Timestamp for the provenance record.
                If None, uses datetime.utcnow().

        Returns:
            An immutable StrategyManifest.

        Raises:
            ManifestBuildError: If any required input is missing or invalid.
        """
        # Validate strategy_id
        if not isinstance(strategy_id, str) or not strategy_id.strip():
            raise ManifestBuildError(
                "StrategyManifestBuilder strategy_id must be a non-empty string."
            )

        # Validate manifest_version
        if not isinstance(manifest_version, str):
            raise ManifestBuildError(
                "StrategyManifestBuilder manifest_version must be a string."
            )
        if not SEMANTIC_VERSION_PATTERN.fullmatch(manifest_version):
            raise ManifestBuildError(
                "StrategyManifestBuilder manifest_version must be semantic versioning (e.g. 1.0.0)."
            )

        # Validate completeness
        if self._candidate is None:
            raise ManifestBuildError(
                "StrategyManifestBuilder requires a ResearchCandidate (call with_candidate)."
            )
        if self._validation_id is None or self._experiment_id is None:
            raise ManifestBuildError(
                "StrategyManifestBuilder requires validation and experiment references (call with_validation)."
            )
        if self._observer_ids is None:
            raise ManifestBuildError(
                "StrategyManifestBuilder requires observer_ids (call with_observers)."
            )
        if self._interpretation_model_id is None:
            raise ManifestBuildError(
                "StrategyManifestBuilder requires interpretation_model_id (call with_interpretation_model)."
            )
        if self._decision_policy_id is None:
            raise ManifestBuildError(
                "StrategyManifestBuilder requires decision_policy_id (call with_decision_policy)."
            )
        if self._risk_policy_id is None:
            raise ManifestBuildError(
                "StrategyManifestBuilder requires risk_policy_id (call with_risk_policy)."
            )
        if self._deployment_profile is None:
            raise ManifestBuildError(
                "StrategyManifestBuilder requires deployment_profile (call with_deployment_profile)."
            )

        # Determine provenance timestamp
        if provenance_timestamp is None:
            provenance_timestamp = datetime.utcnow()
        if not isinstance(provenance_timestamp, datetime):
            raise ManifestBuildError(
                "StrategyManifestBuilder provenance_timestamp must be a datetime."
            )

        # Build provenance
        provenance = Provenance(
            research_candidate_id=self._candidate.candidate_id,
            validation_id=self._validation_id,
            experiment_id=self._experiment_id,
            strategy_manifest_id=strategy_id,
            created_timestamp=provenance_timestamp,
        )

        # Build manifest
        return StrategyManifest(
            strategy_id=strategy_id,
            behaviour_name=self._candidate.behaviour_name,
            observer_ids=self._observer_ids,
            interpretation_model_id=self._interpretation_model_id,
            decision_policy_id=self._decision_policy_id,
            risk_policy_id=self._risk_policy_id,
            deployment_profile=self._deployment_profile,
            manifest_version=manifest_version,
            provenance=provenance,
        )
