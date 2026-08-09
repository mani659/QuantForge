"""Immutable provenance record for scientific reproducibility.

Phase 8.1 — Research Industrialization.
Every deployed strategy must answer: 'Where did this strategy come from?'
Provenance tracks the originating ResearchCandidate, ValidationResult,
ExperimentRecord, and StrategyManifest — nothing more.

This is a scientific reproducibility object. It contains no runtime state,
deployment logic, or business decisions.
"""

from dataclasses import dataclass
from datetime import datetime

from research.lifecycle.research_errors import InvalidProvenanceData


@dataclass(frozen=True)
class Provenance:
    """Immutable scientific provenance chain for a deployed strategy.

    Answers: Where did this strategy come from?
    Tracks the originating research artefacts required for complete
    scientific reproducibility.
    """

    research_candidate_id: str
    validation_id: str
    experiment_id: str
    strategy_manifest_id: str
    created_timestamp: datetime

    def __post_init__(self) -> None:
        """Validate all fields at construction time."""
        required_strings = {
            "research_candidate_id": self.research_candidate_id,
            "validation_id": self.validation_id,
            "experiment_id": self.experiment_id,
            "strategy_manifest_id": self.strategy_manifest_id,
        }
        for field_name, value in required_strings.items():
            if not isinstance(value, str) or not value.strip():
                raise InvalidProvenanceData(
                    f"Provenance {field_name} must be a non-empty string."
                )

        if not isinstance(self.created_timestamp, datetime):
            raise InvalidProvenanceData(
                "Provenance created_timestamp must be a datetime."
            )
