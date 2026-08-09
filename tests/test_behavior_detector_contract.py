import sys
import unittest
from dataclasses import FrozenInstanceError
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from boe.behavior_detector_contract import BehaviorDetectorContract
from boe.behavior_observation import BehaviorObservation
from boe.detector_errors import (
    ConfigurationError,
    DataIntegrityError,
    DetectorError,
    VersionMismatchError,
)
from boe.observation_environment import ObservationEnvironment


class ConcreteDetector(BehaviorDetectorContract):
    @property
    def detector_id(self) -> str:
        return "test_detector"

    @property
    def detector_version(self) -> str:
        return "1.0.0"

    def observe(self, environment: ObservationEnvironment) -> BehaviorObservation | None:
        return None


class TestBehaviorDetectorContract(unittest.TestCase):
    def setUp(self) -> None:
        self.timestamp = datetime(2026, 7, 19, 10, 0, tzinfo=timezone.utc)
        self.environment = ObservationEnvironment(
            schema_version="1.0.0",
            environment_id="environment_000001",
            instrument="EURUSD",
            timeframe="M1",
            observed_at=self.timestamp,
            market_snapshot=({"timestamp": "2026-07-19T10:00:00Z"},),
        )
        self.observation = BehaviorObservation(
            schema_version="1.0.0",
            observation_id="observation_000001",
            environment_id=self.environment.environment_id,
            behavior_type="behavioral_mean_reversion",
            instrument="EURUSD",
            timeframe="M1",
            observed_at=self.timestamp,
            detector_id="test_detector",
            detector_version="1.0.0",
        )

    def test_environment_and_observation_are_immutable(self) -> None:
        with self.assertRaises(FrozenInstanceError):
            self.environment.instrument = "XAUUSD"
        with self.assertRaises(FrozenInstanceError):
            self.observation.behavior_type = "other"
        with self.assertRaises(TypeError):
            self.environment.market_snapshot[0]["timestamp"] = "changed"

    def test_contract_is_abstract_and_complete_subclass_can_be_created(self) -> None:
        with self.assertRaises(TypeError):
            BehaviorDetectorContract()
        detector = ConcreteDetector()
        self.assertEqual(detector.CONTRACT_VERSION, "1.0.0")
        self.assertIsNone(detector.observe(self.environment))

    def test_valid_contract_objects_are_created(self) -> None:
        self.assertEqual(self.environment.instrument, "EURUSD")
        self.assertEqual(self.observation.environment_id, "environment_000001")
        self.assertEqual(self.observation.detector_version, "1.0.0")

    def test_contract_validation_is_deterministic(self) -> None:
        with self.assertRaises(VersionMismatchError):
            ObservationEnvironment(
                schema_version="1.0",
                environment_id="environment_000001",
                instrument="EURUSD",
                timeframe="M1",
                observed_at=self.timestamp,
                market_snapshot=({"timestamp": "2026-07-19T10:00:00Z"},),
            )
        with self.assertRaises(DataIntegrityError):
            BehaviorObservation(
                schema_version="1.0.0",
                observation_id="",
                environment_id="environment_000001",
                behavior_type="behavioral_mean_reversion",
                instrument="EURUSD",
                timeframe="M1",
                observed_at=self.timestamp,
                detector_id="test_detector",
                detector_version="1.0.0",
            )

    def test_exception_hierarchy_is_stable(self) -> None:
        self.assertTrue(issubclass(DataIntegrityError, DetectorError))
        self.assertTrue(issubclass(ConfigurationError, DetectorError))
        self.assertTrue(issubclass(VersionMismatchError, DetectorError))


if __name__ == "__main__":
    unittest.main()
