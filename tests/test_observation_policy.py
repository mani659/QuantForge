"""Deterministic tests for the Observation Policy architecture."""

import json
import sys
import tempfile
import unittest
from dataclasses import FrozenInstanceError
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from boe.observation import (
    DefaultObservationPolicy,
    ObservationConfig,
    ObservationDecision,
    ObservationPolicyContract,
    ObservationPolicyFactory,
)
from boe.observation.termination_reason import TerminationReason
from boe.observation.observation_errors import (
    ObservationConfigurationError,
    ObservationPolicyError,
    ObservationPolicyValidationError,
)
from boe.detector_errors import VersionMismatchError


class TestObservationConfig(unittest.TestCase):
    """Configuration loading, validation, and immutability."""

    def test_valid_config_creation(self) -> None:
        config = ObservationConfig(
            schema_version="1.0.0", max_frames=100, max_duration=60.0
        )
        self.assertEqual(config.schema_version, "1.0.0")
        self.assertEqual(config.max_frames, 100)
        self.assertEqual(config.max_duration, 60.0)

    def test_config_is_immutable(self) -> None:
        config = ObservationConfig("1.0.0", 100, 60.0)
        with self.assertRaises(FrozenInstanceError):
            config.max_frames = 200

    def test_invalid_schema_version_rejected(self) -> None:
        with self.assertRaises(VersionMismatchError):
            ObservationConfig("bad_version", 100, 60.0)
        with self.assertRaises(VersionMismatchError):
            ObservationConfig("1.0", 100, 60.0)

    def test_invalid_max_frames_rejected(self) -> None:
        with self.assertRaises(ObservationConfigurationError):
            ObservationConfig("1.0.0", 0, 60.0)
        with self.assertRaises(ObservationConfigurationError):
            ObservationConfig("1.0.0", -5, 60.0)
        with self.assertRaises(ObservationConfigurationError):
            ObservationConfig("1.0.0", True, 60.0)

    def test_invalid_max_duration_rejected(self) -> None:
        with self.assertRaises(ObservationConfigurationError):
            ObservationConfig("1.0.0", 100, 0.0)
        with self.assertRaises(ObservationConfigurationError):
            ObservationConfig("1.0.0", 100, -1.0)
        with self.assertRaises(ObservationConfigurationError):
            ObservationConfig("1.0.0", 100, True)

    def test_from_json_loads_valid_config(self) -> None:
        data = {"schema_version": "1.0.0", "max_frames": 50, "max_duration": 120.5}
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            json.dump(data, f)
            path = Path(f.name)
        try:
            config = ObservationConfig.from_json(path)
            self.assertEqual(config.max_frames, 50)
            self.assertEqual(config.max_duration, 120.5)
        finally:
            path.unlink(missing_ok=True)

    def test_from_json_missing_file_raises(self) -> None:
        with self.assertRaises(ObservationConfigurationError):
            ObservationConfig.from_json("/nonexistent/path.json")

    def test_from_json_invalid_json_raises(self) -> None:
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            f.write("{invalid json")
            path = Path(f.name)
        try:
            with self.assertRaises(ObservationConfigurationError):
                ObservationConfig.from_json(path)
        finally:
            path.unlink(missing_ok=True)

    def test_from_json_missing_fields_raises(self) -> None:
        data = {"schema_version": "1.0.0", "max_frames": 50}
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            json.dump(data, f)
            path = Path(f.name)
        try:
            with self.assertRaises(ObservationConfigurationError):
                ObservationConfig.from_json(path)
        finally:
            path.unlink(missing_ok=True)


class TestObservationDecision(unittest.TestCase):
    """Immutable decision contract validation."""

    def _ts(self) -> datetime:
        return datetime(2026, 7, 20, 12, 0, tzinfo=timezone.utc)

    def test_valid_continue_decision(self) -> None:
        decision = ObservationDecision(
            continue_observation=True,
            terminate_observation=False,
            termination_reason=None,
            policy_id="default_observation_policy",
            policy_version="1.0.0",
            timestamp=self._ts(),
        )
        self.assertTrue(decision.continue_observation)
        self.assertFalse(decision.terminate_observation)
        self.assertIsNone(decision.termination_reason)

    def test_valid_terminate_decision(self) -> None:
        decision = ObservationDecision(
            continue_observation=False,
            terminate_observation=True,
            termination_reason=TerminationReason.WINDOW_COMPLETE,
            policy_id="default_observation_policy",
            policy_version="1.0.0",
            timestamp=self._ts(),
        )
        self.assertFalse(decision.continue_observation)
        self.assertTrue(decision.terminate_observation)
        self.assertEqual(decision.termination_reason, TerminationReason.WINDOW_COMPLETE)

    def test_decision_is_immutable(self) -> None:
        decision = ObservationDecision(
            True, False, None, "pol", "1.0.0", self._ts()
        )
        with self.assertRaises(FrozenInstanceError):
            decision.continue_observation = False

    def test_conflicting_flags_rejected(self) -> None:
        with self.assertRaises(ValueError):
            ObservationDecision(True, True, None, "pol", "1.0.0", self._ts())
        with self.assertRaises(ValueError):
            ObservationDecision(False, False, None, "pol", "1.0.0", self._ts())

    def test_invalid_termination_reason_rejected(self) -> None:
        with self.assertRaises(ValueError):
            ObservationDecision(
                False, True, "INVALID_REASON", "pol", "1.0.0", self._ts()
            )

    def test_termination_reason_present_on_continue_rejected(self) -> None:
        with self.assertRaises(ValueError):
            ObservationDecision(
                True, False, TerminationReason.WINDOW_COMPLETE, "pol", "1.0.0", self._ts()
            )

    def test_empty_policy_id_rejected(self) -> None:
        with self.assertRaises(ValueError):
            ObservationDecision(True, False, None, "", "1.0.0", self._ts())

    def test_empty_policy_version_rejected(self) -> None:
        with self.assertRaises(ValueError):
            ObservationDecision(True, False, None, "pol", "", self._ts())

    def test_all_allowed_termination_reasons(self) -> None:
        for reason in TerminationReason:
            decision = ObservationDecision(
                False, True, reason, "pol", "1.0.0", self._ts()
            )
            self.assertEqual(decision.termination_reason, reason)


class TestDefaultObservationPolicy(unittest.TestCase):
    """Default policy continuation and termination logic."""

    def setUp(self) -> None:
        self.config = ObservationConfig("1.0.0", max_frames=10, max_duration=30.0)
        self.policy = DefaultObservationPolicy(self.config)
        self.ts = datetime(2026, 7, 28, 12, 0, tzinfo=timezone.utc)

    def test_policy_identity(self) -> None:
        self.assertEqual(self.policy.policy_id, "default_observation_policy")
        self.assertEqual(self.policy.policy_version, "1.0.0")
        self.assertIs(self.policy.config, self.config)

    def test_continue_when_below_limits(self) -> None:
        decision = self.policy.evaluate(current_timestamp=self.ts, frame_count=5, elapsed_duration=10.0)
        self.assertTrue(decision.continue_observation)
        self.assertFalse(decision.terminate_observation)
        self.assertIsNone(decision.termination_reason)
        self.assertEqual(decision.policy_id, "default_observation_policy")
        self.assertEqual(decision.timestamp, self.ts)

    def test_terminate_by_frame_count(self) -> None:
        decision = self.policy.evaluate(current_timestamp=self.ts, frame_count=10, elapsed_duration=5.0)
        self.assertFalse(decision.continue_observation)
        self.assertTrue(decision.terminate_observation)
        self.assertEqual(decision.termination_reason, TerminationReason.WINDOW_COMPLETE)
        self.assertEqual(decision.timestamp, self.ts)

    def test_terminate_by_frame_count_exceeded(self) -> None:
        decision = self.policy.evaluate(current_timestamp=self.ts, frame_count=15, elapsed_duration=5.0)
        self.assertTrue(decision.terminate_observation)
        self.assertEqual(decision.termination_reason, TerminationReason.WINDOW_COMPLETE)

    def test_terminate_by_duration(self) -> None:
        decision = self.policy.evaluate(current_timestamp=self.ts, frame_count=5, elapsed_duration=30.0)
        self.assertFalse(decision.continue_observation)
        self.assertTrue(decision.terminate_observation)
        self.assertEqual(decision.termination_reason, TerminationReason.MAX_DURATION)
        self.assertEqual(decision.timestamp, self.ts)

    def test_terminate_by_duration_exceeded(self) -> None:
        decision = self.policy.evaluate(current_timestamp=self.ts, frame_count=5, elapsed_duration=45.0)
        self.assertTrue(decision.terminate_observation)
        self.assertEqual(decision.termination_reason, TerminationReason.MAX_DURATION)

    def test_frame_count_priority_over_duration(self) -> None:
        """When both limits are reached, frame count wins (deterministic priority)."""
        decision = self.policy.evaluate(current_timestamp=self.ts, frame_count=10, elapsed_duration=30.0)
        self.assertTrue(decision.terminate_observation)
        self.assertEqual(decision.termination_reason, TerminationReason.WINDOW_COMPLETE)

    def test_invalid_frame_count_rejected(self) -> None:
        with self.assertRaises(ObservationPolicyValidationError):
            self.policy.evaluate(current_timestamp=self.ts, frame_count=-1, elapsed_duration=5.0)
        with self.assertRaises(ObservationPolicyValidationError):
            self.policy.evaluate(current_timestamp=self.ts, frame_count=True, elapsed_duration=5.0) # type: ignore

    def test_invalid_elapsed_duration_rejected(self) -> None:
        with self.assertRaises(ObservationPolicyValidationError):
            self.policy.evaluate(current_timestamp=self.ts, frame_count=5, elapsed_duration=-1.0)
        with self.assertRaises(ObservationPolicyValidationError):
            self.policy.evaluate(current_timestamp=self.ts, frame_count=5, elapsed_duration=True) # type: ignore

    def test_invalid_timestamp_rejected(self) -> None:
        with self.assertRaises(ObservationPolicyValidationError):
            self.policy.evaluate(current_timestamp="2026-07-28", frame_count=5, elapsed_duration=5.0) # type: ignore

    def test_invalid_config_rejected(self) -> None:
        with self.assertRaises(ObservationPolicyValidationError):
            DefaultObservationPolicy(config="not_a_config") # type: ignore

    def test_contract_compliance(self) -> None:
        """DefaultObservationPolicy implements ObservationPolicyContract."""
        self.assertIsInstance(self.policy, ObservationPolicyContract)


class TestObservationPolicyFactory(unittest.TestCase):
    """Factory creation and error handling."""

    def setUp(self) -> None:
        self.config = ObservationConfig("1.0.0", max_frames=10, max_duration=30.0)

    def test_factory_creates_default_policy(self) -> None:
        policy = ObservationPolicyFactory.create("default", self.config)
        self.assertIsInstance(policy, DefaultObservationPolicy)
        self.assertIsInstance(policy, ObservationPolicyContract)
        self.assertIs(policy.config, self.config)

    def test_factory_default_name_is_default(self) -> None:
        policy = ObservationPolicyFactory.create(config=self.config)
        self.assertIsInstance(policy, DefaultObservationPolicy)

    def test_factory_unsupported_policy_raises(self) -> None:
        with self.assertRaises(ObservationPolicyError):
            ObservationPolicyFactory.create("nonexistent", self.config)

    def test_factory_non_string_name_raises(self) -> None:
        with self.assertRaises(ObservationPolicyError):
            ObservationPolicyFactory.create(123, self.config)

    def test_factory_missing_config_raises(self) -> None:
        with self.assertRaises(ObservationPolicyError):
            ObservationPolicyFactory.create("default")


class TestObservationErrorHierarchy(unittest.TestCase):
    """Error hierarchy verification."""

    def test_error_hierarchy(self) -> None:
        from boe.detector_errors import DetectorError
        self.assertTrue(issubclass(ObservationPolicyError, DetectorError))
        self.assertTrue(issubclass(ObservationConfigurationError, ObservationPolicyError))
        self.assertTrue(issubclass(ObservationPolicyValidationError, ObservationPolicyError))


if __name__ == "__main__":
    unittest.main()

