"""Staged economic execution — failure classification (W3).

V2.0.1 §4.5 separates two disjoint classes of outcomes:

* Economic exclusions  — ONLY the registered V1.1.0/V2 trade outcomes
  (`EXCLUDED_*`), governed by the frozen economic rules (V1.1.0 §10).
* Execution-infrastructure failures — a uniform `EXECUTION-INFRASTRUCTURE
  FAILURE` class with nine registered categories.

The five binding consequences (§4.5.3) are enforced structurally by the
stages themselves (Stages 0/1 persist no economic result), and this module
guarantees the *classification* contract: an infrastructure failure is never
reported through an `EXCLUDED_*` economic code.
"""

from __future__ import annotations

from typing import Dict, List

INFRASTRUCTURE_FAILURE_LABEL = "EXECUTION-INFRASTRUCTURE FAILURE"

# Registered execution-infrastructure failure categories (V2.0.1 §4.5.2).
INFRASTRUCTURE_FAILURE_CATEGORIES: List[str] = [
    "OOM_RESOURCE_EXHAUSTION",
    "DISK_FILESYSTEM_FAILURE",
    "PARSER_PROCESS_FAILURE",
    "HASH_MISMATCH",
    "CORRUPTED_PREPARATION",
    "PROCESS_CRASH",
    "STALE_HEARTBEAT",
    "INFRASTRUCTURE_EXCEPTION",
    "PREPARATION_INTEGRITY_FAILURE",
]

# Registered economic exclusion states (V1.1.0 §10 data gates).  These are the
# ONLY economic non-trade outcomes permitted in the ledger's exit_reason /
# data_quality_flag columns for exclusions.
ECONOMIC_EXCLUSION_CODES: List[str] = [
    "EXCLUDED_NO_QUOTE_COVERAGE",
    "EXCLUDED_HORIZON_INCOMPLETE",
    "EXCLUDED_RANGE_RECONSTRUCTION",
    "EXCLUDED_RANGE_MISMATCH",
]


class ExecutionInfrastructureFailure(Exception):
    """An execution-infrastructure failure per V2.0.1 §4.5.2.

    Carries a registered category code.  It is never an economic exclusion:
    the label is always `EXECUTION-INFRASTRUCTURE FAILURE` and it never appears
    in any economic ledger column.
    """

    def __init__(self, category: str, message: str = ""):
        if category not in INFRASTRUCTURE_FAILURE_CATEGORIES:
            raise ValueError(
                f"Unregistered infrastructure-failure category: {category!r}"
            )
        self.category = category
        super().__init__(f"{INFRASTRUCTURE_FAILURE_LABEL} [{category}]: {message}")


def classify_infrastructure_failure(exc: BaseException) -> str:
    """Maps an exception to its registered §4.5.2 category.

    Default (unrecognized exception) is INFRASTRUCTURE_EXCEPTION; OOM and
    disk/filesystem errors are detected explicitly.
    """
    module = type(exc).__module__
    name = type(exc).__name__
    full = f"{module}.{name}"

    if isinstance(exc, ExecutionInfrastructureFailure):
        return exc.category

    if isinstance(exc, MemoryError) or (
        "memory" in str(exc).lower() and full.startswith("numpy")
    ):
        return "OOM_RESOURCE_EXHAUSTION"

    if name in ("OSError", "FileNotFoundError", "PermissionError") or (
        isinstance(exc, OSError)
    ):
        return "DISK_FILESYSTEM_FAILURE"

    if name in ("SyntaxError", "ParseError", "ValueError", "json.JSONDecodeError"):
        return "PARSER_PROCESS_FAILURE"

    if "mismatch" in str(exc).lower():
        return "HASH_MISMATCH"

    return "INFRASTRUCTURE_EXCEPTION"


def is_economic_exclusion(code: str) -> bool:
    """True only for registered economic exclusion states (never infra)."""
    return code in ECONOMIC_EXCLUSION_CODES


def assert_no_infrastructure_in_economic_channel(channel: Dict[str, int]) -> None:
    """Guard: no registered economic channel may carry the infra label.

    Both the channel keys and their carried values are inspected; a channel
    whose key or value is (or contains) the infra label is rejected.
    """
    for key, value in channel.items():
        if INFRASTRUCTURE_FAILURE_LABEL in str(key) or (
            INFRASTRUCTURE_FAILURE_LABEL in str(value)
        ):
            raise AssertionError(
                "Infrastructure failures must never appear in an economic channel."
            )