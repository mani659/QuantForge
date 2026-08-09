"""Deterministic errors for Experiment Ledger contracts."""


class LedgerError(ValueError):
    """Base error for an Experiment Ledger contract violation."""


class ExperimentNotFoundError(LedgerError):
    """Raised when an experiment identifier does not exist in the repository."""


class DuplicateExperimentError(LedgerError):
    """Raised when an append would overwrite an immutable experiment record."""


class LedgerSchemaError(LedgerError):
    """Raised when a record violates the stable Experiment Ledger schema."""
