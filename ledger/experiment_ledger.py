"""Public Experiment Ledger façade for the default in-memory repository."""

from .ledger_repository import LedgerRepository


class ExperimentLedger(LedgerRepository):
    """Canonical scientific-memory façade; persistence is intentionally in-memory in v1.0."""
