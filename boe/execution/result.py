from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from types import MappingProxyType
from typing import Any

from boe.execution.execution_errors import ExecutionResultValidationError

class ExecutionStatus(Enum):
    """
    Immutable enumeration representing the abstract outcome of an execution attempt.
    """
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    PARTIALLY_EXECUTED = "PARTIALLY_EXECUTED"
    REJECTED = "REJECTED"
    CANCELLED = "CANCELLED"
    TIMEOUT = "TIMEOUT"


@dataclass(frozen=True)
class ExecutionResult:
    """
    Immutable broker-independent execution result.
    Represents the final physical outcome of a PositionSpecification.
    """
    candidate_id: str
    timeline_id: str
    observation_id: str
    schema_version: str
    status: ExecutionStatus
    metadata: MappingProxyType[str, Any]
    timestamp: datetime
    
    def __post_init__(self):
        if not isinstance(self.status, ExecutionStatus):
            raise ExecutionResultValidationError(
                f"status must be an ExecutionStatus enum, got {type(self.status)}"
            )
        if not isinstance(self.metadata, MappingProxyType):
            raise ExecutionResultValidationError(
                f"metadata must be a MappingProxyType, got {type(self.metadata)}"
            )
        if not self.candidate_id or not isinstance(self.candidate_id, str):
            raise ExecutionResultValidationError("candidate_id must be a non-empty string")
        if not self.timeline_id or not isinstance(self.timeline_id, str):
            raise ExecutionResultValidationError("timeline_id must be a non-empty string")
        if not self.observation_id or not isinstance(self.observation_id, str):
            raise ExecutionResultValidationError("observation_id must be a non-empty string")
        if not isinstance(self.timestamp, datetime):
            raise ExecutionResultValidationError("timestamp must be a datetime object")

    def __hash__(self):
        return hash((
            self.candidate_id,
            self.timeline_id,
            self.observation_id,
            self.schema_version,
            self.status,
            frozenset(self.metadata.items()),
            self.timestamp
        ))
