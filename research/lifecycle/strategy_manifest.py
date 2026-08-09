"""Immutable strategy manifest for deterministic deployment wiring.

Phase 8.1 — Research Industrialization.
A StrategyManifest represents one validated behaviour ready for deployment.
It contains references only — never logic. It declaratively maps a Validated
Behaviour to the specific, frozen Observers, Policies, and Risk Models that
comprise its operational composition.

A StrategyManifest is operational rather than scientific. It answers 'how
should this validated behaviour be wired for deployment?' — not 'what does
the behaviour mean?'
"""

from dataclasses import dataclass
import re

from research.lifecycle.provenance import Provenance
from research.lifecycle.research_errors import InvalidStrategyManifestData


SEMANTIC_VERSION_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")


@dataclass(frozen=True)
class StrategyManifest:
    """Immutable deployment wiring configuration for a validated behaviour.

    Contains only identifiers and provenance. No instantiated classes,
    no business logic, no execution state.
    """

    strategy_id: str
    behaviour_name: str
    observer_ids: tuple[str, ...]
    interpretation_model_id: str
    decision_policy_id: str
    risk_policy_id: str
    deployment_profile: str
    manifest_version: str
    provenance: Provenance

    def __post_init__(self) -> None:
        """Validate all fields at construction time."""
        required_strings = {
            "strategy_id": self.strategy_id,
            "behaviour_name": self.behaviour_name,
            "interpretation_model_id": self.interpretation_model_id,
            "decision_policy_id": self.decision_policy_id,
            "risk_policy_id": self.risk_policy_id,
            "deployment_profile": self.deployment_profile,
        }
        for field_name, value in required_strings.items():
            if not isinstance(value, str) or not value.strip():
                raise InvalidStrategyManifestData(
                    f"StrategyManifest {field_name} must be a non-empty string."
                )

        # Validate semantic version
        if not isinstance(self.manifest_version, str):
            raise InvalidStrategyManifestData(
                "StrategyManifest manifest_version must be a string."
            )
        if not SEMANTIC_VERSION_PATTERN.fullmatch(self.manifest_version):
            raise InvalidStrategyManifestData(
                "StrategyManifest manifest_version must be semantic versioning (e.g. 1.0.0)."
            )

        # Validate and normalize observer_ids
        if isinstance(self.observer_ids, list):
            object.__setattr__(self, "observer_ids", tuple(self.observer_ids))
        if not isinstance(self.observer_ids, tuple):
            raise InvalidStrategyManifestData(
                "StrategyManifest observer_ids must be a tuple of strings."
            )
        if not self.observer_ids:
            raise InvalidStrategyManifestData(
                "StrategyManifest observer_ids must not be empty."
            )
        if not all(isinstance(o, str) and o.strip() for o in self.observer_ids):
            raise InvalidStrategyManifestData(
                "StrategyManifest observer_ids must be a tuple of non-empty strings."
            )

        # Validate provenance
        if not isinstance(self.provenance, Provenance):
            raise InvalidStrategyManifestData(
                "StrategyManifest provenance must be a Provenance instance."
            )
