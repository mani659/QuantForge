"""Deterministic in-memory implementation of the Experiment Ledger contract."""

from .experiment_record import ExperimentRecord
from .ledger_contract import LedgerContract
from .ledger_errors import DuplicateExperimentError, ExperimentNotFoundError, LedgerError


class LedgerRepository(LedgerContract):
    """Append-only in-memory scientific record, replaceable by future persistence."""

    def __init__(self) -> None:
        self._records: tuple[ExperimentRecord, ...] = ()

    def append(self, record: ExperimentRecord) -> ExperimentRecord:
        """Append a unique immutable record and return the exact stored object."""
        if not isinstance(record, ExperimentRecord):
            raise LedgerError("LedgerRepository accepts only ExperimentRecord values.")
        if any(existing.experiment_id == record.experiment_id for existing in self._records):
            raise DuplicateExperimentError(f"Experiment already exists: {record.experiment_id}")
        self._records = (*self._records, record)
        return record

    def get(self, experiment_id: str) -> ExperimentRecord:
        """Return one record or raise a deterministic not-found error."""
        for record in self._records:
            if record.experiment_id == experiment_id:
                return record
        raise ExperimentNotFoundError(f"Experiment was not found: {experiment_id}")

    def get_by_candidate(self, candidate_id: str) -> tuple[ExperimentRecord, ...]:
        """Return candidate records in append order."""
        return tuple(record for record in self._records if record.candidate_id == candidate_id)

    def get_by_policy(self, policy_name: str) -> tuple[ExperimentRecord, ...]:
        """Return policy records in append order."""
        return tuple(record for record in self._records if record.policy_name == policy_name)

    def get_by_behavior(self, behavior_type: str) -> tuple[ExperimentRecord, ...]:
        """Return behavior records in append order."""
        return tuple(record for record in self._records if record.behavior_type == behavior_type)

    def all(self) -> tuple[ExperimentRecord, ...]:
        """Return all records in append order as an immutable tuple."""
        return self._records
