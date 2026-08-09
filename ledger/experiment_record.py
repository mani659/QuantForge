"""Immutable scientific record for one completed behavioral experiment."""

from dataclasses import dataclass
from datetime import datetime
import re

from boe.hypothesis.hypothesis_result import HypothesisResult
from boe.validators.validation_result import ValidationResult

from .ledger_errors import LedgerSchemaError


SEMANTIC_VERSION_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")
SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")


@dataclass(frozen=True)
class ExperimentRecord:
    """Immutable facts required to replay a policy against historical evidence.

    Validator results are retained as their original immutable contracts. No
    detector calculation, threshold, metric, private state, or explanation is
    admitted into this public scientific record.
    """

    schema_version: str
    experiment_id: str
    candidate_id: str
    observation_id: str
    behavior_type: str
    detector_id: str
    detector_version: str
    validation_results: tuple[ValidationResult, ...]
    policy_name: str
    policy_version: str
    policy_parameters_hash: str
    hypothesis_result: HypothesisResult
    overall_confidence: float
    created_timestamp: datetime
    risk_plan_id: str | None = None
    risk_approved: bool | None = None
    execution_id: str | None = None
    executed: bool | None = None
    pnl: float | None = None
    mae: float | None = None
    mfe: float | None = None
    holding_time: float | None = None

    def __post_init__(self) -> None:
        """Validate stable provenance and replayable, abstract evidence only."""
        if not SEMANTIC_VERSION_PATTERN.fullmatch(self.schema_version):
            raise LedgerSchemaError("ExperimentRecord schema_version must be semantic versioning.")
        if not all(
            isinstance(value, str) and value
            for value in (
                self.experiment_id,
                self.candidate_id,
                self.observation_id,
                self.behavior_type,
                self.detector_id,
                self.policy_name,
            )
        ):
            raise LedgerSchemaError("ExperimentRecord identity and provenance fields are required.")
        if not SEMANTIC_VERSION_PATTERN.fullmatch(self.detector_version):
            raise LedgerSchemaError("ExperimentRecord detector_version must be semantic versioning.")
        if not SEMANTIC_VERSION_PATTERN.fullmatch(self.policy_version):
            raise LedgerSchemaError("ExperimentRecord policy_version must be semantic versioning.")
        if not SHA256_PATTERN.fullmatch(self.policy_parameters_hash):
            raise LedgerSchemaError("ExperimentRecord policy_parameters_hash must be a SHA-256 hex digest.")
        if not isinstance(self.validation_results, tuple) or not self.validation_results:
            raise LedgerSchemaError("ExperimentRecord validation_results must be a non-empty tuple.")
        if not all(isinstance(result, ValidationResult) for result in self.validation_results):
            raise LedgerSchemaError("ExperimentRecord validation_results must contain ValidationResult values.")
        if any(result.candidate_id != self.candidate_id for result in self.validation_results):
            raise LedgerSchemaError("ValidationResult candidate_id must match ExperimentRecord candidate_id.")
        if not isinstance(self.hypothesis_result, HypothesisResult):
            raise LedgerSchemaError("ExperimentRecord hypothesis_result must be a HypothesisResult.")
        if self.hypothesis_result.candidate_id != self.candidate_id:
            raise LedgerSchemaError("HypothesisResult candidate_id must match ExperimentRecord candidate_id.")
        if (
            not isinstance(self.overall_confidence, float)
            or not 0.0 <= self.overall_confidence <= 1.0
            or self.overall_confidence != self.hypothesis_result.overall_confidence
        ):
            raise LedgerSchemaError("ExperimentRecord confidence must match HypothesisResult confidence.")
        if not isinstance(self.created_timestamp, datetime):
            raise LedgerSchemaError("ExperimentRecord created_timestamp must be a datetime.")
        for value, name in ((self.risk_approved, "risk_approved"), (self.executed, "executed")):
            if value is not None and not isinstance(value, bool):
                raise LedgerSchemaError(f"ExperimentRecord {name} must be bool or None.")
        for value, name in (
            (self.pnl, "pnl"), (self.mae, "mae"), (self.mfe, "mfe"),
            (self.holding_time, "holding_time"),
        ):
            if value is not None and (not isinstance(value, float) or isinstance(value, bool)):
                raise LedgerSchemaError(f"ExperimentRecord {name} must be float or None.")
