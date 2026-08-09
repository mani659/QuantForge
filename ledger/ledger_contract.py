"""Abstract persistence boundary for immutable Experiment Ledger records."""

from abc import ABC, abstractmethod

from .experiment_record import ExperimentRecord


class LedgerContract(ABC):
    """Defines retrieval and append behavior for future ledger persistence stores."""

    @abstractmethod
    def append(self, record: ExperimentRecord) -> ExperimentRecord:
        """Persist one immutable experiment without overwriting prior facts."""

    @abstractmethod
    def get(self, experiment_id: str) -> ExperimentRecord:
        """Return exactly one experiment by its stable identifier."""

    @abstractmethod
    def get_by_candidate(self, candidate_id: str) -> tuple[ExperimentRecord, ...]:
        """Return experiments for one candidate in deterministic append order."""

    @abstractmethod
    def get_by_policy(self, policy_name: str) -> tuple[ExperimentRecord, ...]:
        """Return experiments for one policy in deterministic append order."""

    @abstractmethod
    def get_by_behavior(self, behavior_type: str) -> tuple[ExperimentRecord, ...]:
        """Return experiments for one observed behavior in deterministic append order."""

    @abstractmethod
    def all(self) -> tuple[ExperimentRecord, ...]:
        """Return every experiment in deterministic append order."""
