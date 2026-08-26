"""Failure-classification tests (V2.0.1 §4.5, W3)."""

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from research.staged_execution._failure import (  # noqa: E402
    ECONOMIC_EXCLUSION_CODES,
    INFRASTRUCTURE_FAILURE_CATEGORIES,
    INFRASTRUCTURE_FAILURE_LABEL,
    ExecutionInfrastructureFailure,
    assert_no_infrastructure_in_economic_channel,
    classify_infrastructure_failure,
    is_economic_exclusion,
)


def test_label_is_exact_string():
    assert INFRASTRUCTURE_FAILURE_LABEL == "EXECUTION-INFRASTRUCTURE FAILURE"


def test_nine_registered_categories():
    assert INFRASTRUCTURE_FAILURE_CATEGORIES == [
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


def test_economic_exclusions_are_only_four_registered():
    assert ECONOMIC_EXCLUSION_CODES == [
        "EXCLUDED_NO_QUOTE_COVERAGE",
        "EXCLUDED_HORIZON_INCOMPLETE",
        "EXCLUDED_RANGE_RECONSTRUCTION",
        "EXCLUDED_RANGE_MISMATCH",
    ]
    assert all(is_economic_exclusion(c) for c in ECONOMIC_EXCLUSION_CODES)
    assert not is_economic_exclusion("EXECUTION-INFRASTRUCTURE FAILURE")


def test_no_overlap_between_classes():
    assert not (set(INFRASTRUCTURE_FAILURE_CATEGORIES) & set(ECONOMIC_EXCLUSION_CODES))


def test_classify_oom():
    assert classify_infrastructure_failure(MemoryError("out")) == "OOM_RESOURCE_EXHAUSTION"


def test_classify_disk():
    assert classify_infrastructure_failure(FileNotFoundError("x")) == "DISK_FILESYSTEM_FAILURE"
    assert classify_infrastructure_failure(PermissionError("x")) == "DISK_FILESYSTEM_FAILURE"


def test_classify_parser():
    assert classify_infrastructure_failure(ValueError("bad value")) == "PARSER_PROCESS_FAILURE"
    assert classify_infrastructure_failure(SyntaxError("bad")) == "PARSER_PROCESS_FAILURE"


def test_classify_default_infra_exception():
    assert classify_infrastructure_failure(RuntimeError("boom")) == "INFRASTRUCTURE_EXCEPTION"


def test_classify_hash_mismatch_keyword():
    assert classify_infrastructure_failure(RuntimeError("sha mismatch")) == "HASH_MISMATCH"


def test_execution_failure_roundtrip_category():
    exc = ExecutionInfrastructureFailure("CORRUPTED_PREPARATION", "bad prep")
    assert exc.category == "CORRUPTED_PREPARATION"
    assert INFRASTRUCTURE_FAILURE_LABEL in str(exc)
    assert classify_infrastructure_failure(exc) == "CORRUPTED_PREPARATION"


def test_unregistered_category_rejected():
    with pytest.raises(ValueError):
        ExecutionInfrastructureFailure("NOT_A_REAL_CATEGORY")


def test_economic_channel_guard_rejects_infra_label():
    with pytest.raises(AssertionError):
        assert_no_infrastructure_in_economic_channel(
            {"exit_reason": INFRASTRUCTURE_FAILURE_LABEL}
        )


def test_economic_channel_guard_accepts_clean():
    assert_no_infrastructure_in_economic_channel(
        {"exit_reason": "EXCLUDED_RANGE_MISMATCH", "n": 3}
    )