"""Immutable external context contract for Behavioral Observation validation."""

from dataclasses import dataclass
from datetime import datetime
import re
from types import MappingProxyType
from typing import Mapping

from .validator_errors import ValidationContextError, ValidatorVersionMismatchError


SEMANTIC_VERSION_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")


@dataclass(frozen=True)
class ValidationContext:
    """Stable external context supplied to validators without detector internals.

    ``context_data`` is an immutable opaque container. Future validators may use
    supplied snapshots or reference data internally, but derived measures and
    implementation-specific values must not appear in ValidationResult.
    """

    schema_version: str
    context_id: str
    candidate_id: str
    observed_at: datetime
    context_data: Mapping[str, object]

    def __post_init__(self) -> None:
        """Validate stable context fields and protect context mapping mutation."""
        if not SEMANTIC_VERSION_PATTERN.fullmatch(self.schema_version):
            raise ValidatorVersionMismatchError(
                "ValidationContext schema_version must be semantic versioning."
            )
        if not self.context_id or not self.candidate_id:
            raise ValidationContextError("ValidationContext context_id and candidate_id are required.")
        if not isinstance(self.observed_at, datetime):
            raise ValidationContextError("ValidationContext observed_at must be a datetime.")
        if not isinstance(self.context_data, Mapping):
            raise ValidationContextError("ValidationContext context_data must be a mapping.")
        object.__setattr__(self, "context_data", MappingProxyType(dict(self.context_data)))
