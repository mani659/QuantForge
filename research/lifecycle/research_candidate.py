"""Immutable research hypothesis declaration for the Research Lifecycle domain.

Phase 8.1 — Research Industrialization.
A ResearchCandidate represents a single behavioural hypothesis entering
the QuantForge scientific lifecycle. It is the constitutional entry point:
an idea formalized into a testable claim.

A ResearchCandidate is scientific. It contains no runtime state, execution
results, statistics, or broker information. It declares what is to be
tested, not how it performs.
"""

from dataclasses import dataclass
from datetime import datetime
import re

from research.lifecycle.research_errors import InvalidResearchCandidateData


SEMANTIC_VERSION_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")


@dataclass(frozen=True)
class ResearchCandidate:
    """An immutable behavioural hypothesis entering the scientific lifecycle.

    Contains identity, hypothesis provenance, behavioural classification,
    assumptions, and success criteria. Contains no runtime state, execution
    results, statistics, or broker information.
    """

    candidate_id: str
    hypothesis_id: str
    research_name: str
    behaviour_name: str
    description: str
    creation_timestamp: datetime
    research_version: str
    assumptions: tuple[str, ...]
    success_criteria: tuple[str, ...]
    metadata: tuple[tuple[str, str], ...]

    def __post_init__(self) -> None:
        """Validate all fields at construction time."""
        # Validate required string fields are non-empty
        required_strings = {
            "candidate_id": self.candidate_id,
            "hypothesis_id": self.hypothesis_id,
            "research_name": self.research_name,
            "behaviour_name": self.behaviour_name,
            "description": self.description,
        }
        for field_name, value in required_strings.items():
            if not isinstance(value, str) or not value.strip():
                raise InvalidResearchCandidateData(
                    f"ResearchCandidate {field_name} must be a non-empty string."
                )

        # Validate semantic version
        if not isinstance(self.research_version, str):
            raise InvalidResearchCandidateData(
                "ResearchCandidate research_version must be a string."
            )
        if not SEMANTIC_VERSION_PATTERN.fullmatch(self.research_version):
            raise InvalidResearchCandidateData(
                "ResearchCandidate research_version must be semantic versioning (e.g. 1.0.0)."
            )

        # Validate timestamp
        if not isinstance(self.creation_timestamp, datetime):
            raise InvalidResearchCandidateData(
                "ResearchCandidate creation_timestamp must be a datetime."
            )

        # Validate and normalize assumptions
        if isinstance(self.assumptions, list):
            object.__setattr__(self, "assumptions", tuple(self.assumptions))
        if not isinstance(self.assumptions, tuple):
            raise InvalidResearchCandidateData(
                "ResearchCandidate assumptions must be a tuple of strings."
            )
        if not all(isinstance(a, str) for a in self.assumptions):
            raise InvalidResearchCandidateData(
                "ResearchCandidate assumptions must be a tuple of strings."
            )

        # Validate and normalize success_criteria
        if isinstance(self.success_criteria, list):
            object.__setattr__(self, "success_criteria", tuple(self.success_criteria))
        if not isinstance(self.success_criteria, tuple):
            raise InvalidResearchCandidateData(
                "ResearchCandidate success_criteria must be a tuple of strings."
            )
        if not all(isinstance(c, str) for c in self.success_criteria):
            raise InvalidResearchCandidateData(
                "ResearchCandidate success_criteria must be a tuple of strings."
            )

        # Validate and normalize metadata
        if isinstance(self.metadata, dict):
            object.__setattr__(
                self, "metadata", tuple(sorted(self.metadata.items()))
            )
        if not isinstance(self.metadata, tuple):
            raise InvalidResearchCandidateData(
                "ResearchCandidate metadata must be a tuple of (str, str) pairs."
            )
        for item in self.metadata:
            if (
                not isinstance(item, tuple)
                or len(item) != 2
                or not isinstance(item[0], str)
                or not isinstance(item[1], str)
            ):
                raise InvalidResearchCandidateData(
                    "ResearchCandidate metadata must be a tuple of (str, str) pairs."
                )
