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
from boe.validators.recoil_config import RecoilConfig
from boe.validators.recoil_validator import RecoilValidator
from boe.validators.validation_context import ValidationContext
from boe.validators.validator_errors import ValidationContextError


class TestRecoilValidator(unittest.TestCase):
    def setUp(self) -> None:
        self.timestamp = datetime(2026, 7, 19, 15, 0, tzinfo=timezone.utc)
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
        self.config = RecoilConfig.from_json(PROJECT_ROOT / "config" / "recoil_rules.json")
        self.validator = RecoilValidator(self.config)

    def _context(self, reference_value: float, current_value: float, direction: str = "UP") -> ValidationContext:
        return ValidationContext(
            schema_version="1.0.0",
            context_id="context_000001",
            candidate_id=self.candidate.candidate_id,
            observed_at=self.timestamp,
            context_data={
                "reference_value": reference_value,
                "current_value": current_value,
                "expected_recoil_direction": direction,
            },
        )

    def test_recoil_observed(self) -> None:
        result = self.validator.validate(self.candidate, self._context(100.0, 101.5))
        self.assertTrue(result.passed)
        self.assertEqual(result.evidence, ("RECOIL_OBSERVED",))

    def test_recoil_absent(self) -> None:
        result = self.validator.validate(self.candidate, self._context(100.0, 100.5))
        self.assertFalse(result.passed)
        self.assertEqual(result.evidence, ("RECOIL_NOT_OBSERVED",))

    def test_boundary_condition_is_observed(self) -> None:
        result = self.validator.validate(
            self.candidate,
            self._context(100.0, 100.0 + self.config.minimum_recoil_distance),
        )
        self.assertTrue(result.passed)

    def test_output_is_deterministic(self) -> None:
        context = self._context(100.0, 101.5)
        self.assertEqual(
            self.validator.validate(self.candidate, context),
            self.validator.validate(self.candidate, context),
        )

    def test_configuration_is_loaded_and_immutable(self) -> None:
        self.assertEqual(self.config.schema_version, "1.0.0")
        with self.assertRaises(FrozenInstanceError):
            self.config.minimum_recoil_distance = 2.0

    def test_invalid_context_is_rejected(self) -> None:
        context = ValidationContext(
            schema_version="1.0.0",
            context_id="context_000002",
            candidate_id=self.candidate.candidate_id,
            observed_at=self.timestamp,
            context_data={"reference_value": 100.0},
        )
        with self.assertRaises(ValidationContextError):
            self.validator.validate(self.candidate, context)


if __name__ == "__main__":
    unittest.main()
