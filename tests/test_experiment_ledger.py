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
from boe.hypothesis.hypothesis_engine import HypothesisEngine
from boe.validators.validation_result import ValidationResult
from ledger.experiment_record import ExperimentRecord
from ledger.ledger_errors import DuplicateExperimentError, LedgerSchemaError
from ledger.ledger_repository import LedgerRepository


class TestExperimentLedger(unittest.TestCase):
    POLICY_HASH = "a" * 64

    def setUp(self) -> None:
        self.timestamp = datetime(2026, 7, 20, 9, 0, tzinfo=timezone.utc)
        observation = BehaviorObservation(
            schema_version="1.0.0",
            observation_id="observation_ledger_000001",
            environment_id="environment_ledger_000001",
            behavior_type="behavioral_mean_reversion",
            instrument="EURUSD",
            timeframe="M1",
            observed_at=self.timestamp,
            detector_id="test_detector",
            detector_version="1.0.0",
        )
        self.candidate = CandidateManager().create_candidate(
            "candidate_ledger_000001", observation, self.timestamp
        )
        self.repository = LedgerRepository()

    def _record(self, experiment_id: str, policy_name: str = "strict_all_pass", behavior: str | None = None) -> ExperimentRecord:
        validation_results = (
            ValidationResult(
                schema_version="1.0.0",
                candidate_id=self.candidate.candidate_id,
                validator_id="recoil_validator",
                validator_version="1.0.0",
                passed=True,
                confidence=1.0,
                evidence=("RECOIL_OBSERVED",),
                timestamp=self.timestamp,
            ),
        )
        hypothesis_result = HypothesisEngine().evaluate(self.candidate, validation_results)
        return ExperimentRecord(
            schema_version="1.0.0",
            experiment_id=experiment_id,
            candidate_id=self.candidate.candidate_id,
            observation_id=self.candidate.observation.observation_id,
            behavior_type=behavior or self.candidate.observation.behavior_type,
            detector_id=self.candidate.observation.detector_id,
            detector_version=self.candidate.observation.detector_version,
            validation_results=validation_results,
            policy_name=policy_name,
            policy_version="1.0.0",
            policy_parameters_hash=self.POLICY_HASH,
            hypothesis_result=hypothesis_result,
            overall_confidence=hypothesis_result.overall_confidence,
            created_timestamp=self.timestamp,
        )

    def test_record_is_immutable_and_has_schema_version(self) -> None:
        record = self._record("experiment_000001")
        self.assertEqual(record.schema_version, "1.0.0")
        with self.assertRaises(FrozenInstanceError):
            record.policy_name = "changed"

    def test_append_and_retrieval(self) -> None:
        record = self._record("experiment_000001")
        self.assertIs(self.repository.append(record), record)
        self.assertIs(self.repository.get(record.experiment_id), record)

    def test_candidate_policy_and_behavior_lookups(self) -> None:
        first = self._record("experiment_000001")
        second = self._record("experiment_000002", policy_name="balanced", behavior="behavioral_breakout")
        self.repository.append(first)
        self.repository.append(second)
        self.assertEqual(self.repository.get_by_candidate(self.candidate.candidate_id), (first, second))
        self.assertEqual(self.repository.get_by_policy("balanced"), (second,))
        self.assertEqual(self.repository.get_by_behavior("behavioral_mean_reversion"), (first,))

    def test_deterministic_append_order_and_duplicates(self) -> None:
        first = self._record("experiment_000001")
        second = self._record("experiment_000002")
        self.repository.append(first)
        self.repository.append(second)
        self.assertEqual(self.repository.all(), (first, second))
        with self.assertRaises(DuplicateExperimentError):
            self.repository.append(first)

    def test_replay_compatibility_preserves_exact_evidence_and_policy_provenance(self) -> None:
        record = self._record("experiment_000001")
        self.repository.append(record)
        replay = self.repository.get(record.experiment_id)
        self.assertIs(replay.validation_results, record.validation_results)
        self.assertEqual(replay.policy_name, "strict_all_pass")
        self.assertEqual(replay.policy_version, "1.0.0")
        self.assertEqual(replay.policy_parameters_hash, self.POLICY_HASH)

    def test_invalid_schema_data_is_rejected(self) -> None:
        record = self._record("experiment_000001")
        with self.assertRaises(LedgerSchemaError):
            ExperimentRecord(
                **{**record.__dict__, "policy_parameters_hash": "not-a-hash"}
            )


if __name__ == "__main__":
    unittest.main()
