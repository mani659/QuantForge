import sys
import unittest
from dataclasses import FrozenInstanceError
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from boe.behavior_observation import BehaviorObservation
from boe.candidate_manager import CandidateManager
from boe.validators.validation_context import ValidationContext
from boe.validators.validation_result import ValidationResult
from boe.validators.validator_contract import BehaviorValidatorContract
from boe.validators.validator_errors import (
    PipelineConfigurationError,
    ValidationContextError,
    ValidatorError,
    ValidatorVersionMismatchError,
)
from boe.validators.validator_pipeline import ValidatorPipeline


class OrderedValidator(BehaviorValidatorContract):
    def __init__(self, validator_id: str, order: list[str], passed: bool) -> None:
        self._validator_id = validator_id
        self._order = order
        self._passed = passed

    @property
    def validator_id(self) -> str:
        return self._validator_id

    @property
    def validator_name(self) -> str:
        return self._validator_id

    @property
    def validator_version(self) -> str:
        return "1.0.0"

    def validate(self, candidate, context) -> ValidationResult:
        self._order.append(self.validator_id)
        return ValidationResult(
            schema_version="1.0.0",
            candidate_id=candidate.candidate_id,
            validator_id=self.validator_id,
            validator_version=self.validator_version,
            passed=self._passed,
            confidence=1.0 if self._passed else 0.0,
            evidence=("abstract_evidence",),
            timestamp=context.observed_at,
        )


class TestValidatorFramework(unittest.TestCase):
    def setUp(self) -> None:
        self.timestamp = datetime(2026, 7, 19, 13, 0, tzinfo=timezone.utc)
        observation = BehaviorObservation(
            schema_version="1.0.0",
            observation_id="observation_000001",
            environment_id="environment_000001",
            behavior_type="behavioral_mean_reversion",
            instrument="EURUSD",
            timeframe="M1",
            observed_at=self.timestamp,
            detector_id="test_detector",
            detector_version="1.0.0",
        )
        self.candidate = CandidateManager().create_candidate(
            "candidate_000001", observation, self.timestamp
        )
        self.context = ValidationContext(
            schema_version="1.0.0",
            context_id="context_000001",
            candidate_id=self.candidate.candidate_id,
            observed_at=self.timestamp,
            context_data={"snapshot_reference": "market_000001"},
        )

    def test_context_and_result_are_immutable(self) -> None:
        result = ValidationResult(
            schema_version="1.0.0",
            candidate_id=self.candidate.candidate_id,
            validator_id="validator_a",
            validator_version="1.0.0",
            passed=True,
            confidence=1.0,
            evidence=("abstract_evidence",),
            timestamp=self.timestamp,
        )
        with self.assertRaises(FrozenInstanceError):
            self.context.context_id = "changed"
        with self.assertRaises(TypeError):
            self.context.context_data["snapshot_reference"] = "changed"
        with self.assertRaises(FrozenInstanceError):
            result.passed = False

    def test_contract_enforcement(self) -> None:
        with self.assertRaises(TypeError):
            BehaviorValidatorContract()
        self.assertEqual(OrderedValidator("validator_a", [], True).CONTRACT_VERSION, "1.0.0")

    def test_pipeline_runs_multiple_validators_in_order_and_aggregates_results(self) -> None:
        order = []
        pipeline = ValidatorPipeline(
            (OrderedValidator("validator_a", order, True), OrderedValidator("validator_b", order, False))
        )
        results = pipeline.validate(self.candidate, self.context)
        self.assertEqual(order, ["validator_a", "validator_b"])
        self.assertEqual(tuple(result.validator_id for result in results), ("validator_a", "validator_b"))
        self.assertEqual(tuple(result.passed for result in results), (True, False))
        self.assertIsInstance(results, tuple)

    def test_empty_pipeline_returns_empty_immutable_results(self) -> None:
        self.assertEqual(ValidatorPipeline().validate(self.candidate, self.context), ())

    def test_pipeline_output_is_deterministic(self) -> None:
        first = ValidatorPipeline((OrderedValidator("validator_a", [], True),)).validate(
            self.candidate, self.context
        )
        second = ValidatorPipeline((OrderedValidator("validator_a", [], True),)).validate(
            self.candidate, self.context
        )
        self.assertEqual(first, second)

    def test_exception_hierarchy_and_validation_errors(self) -> None:
        self.assertTrue(issubclass(ValidationContextError, ValidatorError))
        self.assertTrue(issubclass(PipelineConfigurationError, ValidatorError))
        self.assertTrue(issubclass(ValidatorVersionMismatchError, ValidatorError))
        with self.assertRaises(PipelineConfigurationError):
            ValidatorPipeline((object(),))
        with self.assertRaises(ValidatorVersionMismatchError):
            ValidationContext(
                schema_version="1.0",
                context_id="context_000001",
                candidate_id=self.candidate.candidate_id,
                observed_at=self.timestamp,
                context_data={},
            )


if __name__ == "__main__":
    unittest.main()
