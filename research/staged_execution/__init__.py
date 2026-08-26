"""Staged economic execution package (V2.0.1 protocol).

Repeatable non-scientific stages (0, 1, 3) plus the single controlled
economic execution (Stage 2).  Exposes the stage entry points and the shared
identity / failure primitives.
"""

from ._failure import (
    ECONOMIC_EXCLUSION_CODES,
    INFRASTRUCTURE_FAILURE_CATEGORIES,
    INFRASTRUCTURE_FAILURE_LABEL,
    ExecutionInfrastructureFailure,
    classify_infrastructure_failure,
    is_economic_exclusion,
)
from ._identity import (
    PREP_CODE_SCHEMA_VERSION,
    STAGE1_SCHEMA_VERSION,
    STAGE1_PARAMETER_KEYS,
    canonical_stage1_parameters,
    external_median,
    external_percentile,
    prep_identity,
    sha256_file,
)
from ._stage_recorder import StageRunRecorder
from .stage0 import run_stage0_preflight
from .stage1 import PREP_ARTIFACTS, is_valid_prep, run_stage1_prepare
from .stage2 import run_stage2_execute
from .stage3 import run_stage3_verify

__all__ = [
    "ECONOMIC_EXCLUSION_CODES",
    "INFRASTRUCTURE_FAILURE_CATEGORIES",
    "INFRASTRUCTURE_FAILURE_LABEL",
    "ExecutionInfrastructureFailure",
    "classify_infrastructure_failure",
    "is_economic_exclusion",
    "PREP_CODE_SCHEMA_VERSION",
    "STAGE1_SCHEMA_VERSION",
    "STAGE1_PARAMETER_KEYS",
    "canonical_stage1_parameters",
    "external_median",
    "external_percentile",
    "prep_identity",
    "sha256_file",
    "StageRunRecorder",
    "run_stage0_preflight",
    "PREP_ARTIFACTS",
    "is_valid_prep",
    "run_stage1_prepare",
    "run_stage2_execute",
    "run_stage3_verify",
]

__version__ = "0.1.0"