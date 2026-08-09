"""Unit tests for Sprint 8.3 (Deployment Evidence Consumption).

Coverage targets:
- locate: find persisted DeploymentOutcome artifacts deterministically
- retrieve: read raw artifact, error when absent
- deserialize: reconstruct immutable DeploymentOutcome, reject malformed
- validate: integrity round-trip, reject tampered artifacts
- return: immutable returns, no interpretation, no runtime state, no mutation
- repository abstraction: OutcomeReader delegates persistence to ExperimentRecorder
- determinism: repeated reads produce identical results
"""
import json
import shutil
import tempfile
from datetime import datetime
from pathlib import Path
from types import MappingProxyType

import pytest

from research.experiment_recorder import ExperimentRecorder
from research.lifecycle.deployment_outcome import DeploymentOutcome
from research.lifecycle.outcome_reader import OutcomeReader
from research.lifecycle.provenance import Provenance
from research.lifecycle.research_errors import InvalidDeploymentOutcomeData


def _make_provenance(**overrides) -> Provenance:
    """Build a valid Provenance with sensible defaults."""
    defaults = dict(
        research_candidate_id="candidate_001",
        validation_id="validation_001",
        experiment_id="experiment_001",
        strategy_manifest_id="manifest_001",
        created_timestamp=datetime(2026, 1, 1, 12, 0, 0),
    )
    defaults.update(overrides)
    return Provenance(**defaults)


def _make_outcome(**overrides) -> DeploymentOutcome:
    """Build a valid DeploymentOutcome with sensible defaults."""
    defaults = dict(
        outcome_id="outcome_001",
        strategy_manifest_id="manifest_001",
        provenance=_make_provenance(),
        execution_reference="execution_001",
        execution_metadata=MappingProxyType(
            {"status": "SUCCESS", "trades_executed": 10, "total_return": 0.05}
        ),
        deployment_metadata=MappingProxyType(
            {"strategy_name": "TestStrategy", "deployment_time": "2026-01-01T12:00:00"}
        ),
        recorded_timestamp=datetime(2026, 1, 1, 12, 30, 0),
        schema_version="1.0.0",
    )
    defaults.update(overrides)
    return DeploymentOutcome(**defaults)


class TestOutcomeReaderLocate:
    """Tests for the locate responsibility."""

    def setup_method(self):
        self.temp_dir = tempfile.mkdtemp()
        self.recorder = ExperimentRecorder(self.temp_dir)
        self.reader = OutcomeReader(self.recorder)

    def teardown_method(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_locate_returns_empty_when_no_artifacts(self):
        assert self.reader.locate() == ()

    def test_locate_returns_run_ids_in_deterministic_sorted_order(self):
        for i in range(3):
            self.recorder.append_deployment_outcome(_make_outcome(outcome_id=f"outcome_{i}"))
        located = self.reader.locate()
        assert located == tuple(sorted(located))
        assert len(located) == 3
        assert all(run_id.startswith("run_") for run_id in located)

    def test_locate_ignores_runs_without_deployment_outcome(self):
        run_id = self.recorder.append_deployment_outcome(_make_outcome())
        # Simulate a run directory without an artifact
        bare = Path(self.temp_dir) / "research" / "experiments" / "run_009999"
        bare.mkdir(parents=True, exist_ok=True)
        (bare / "manifest.json").write_text("{}", encoding="utf-8")
        assert run_id in self.reader.locate()
        assert "run_009999" not in self.reader.locate()

    def test_locate_repeated_calls_are_identical(self):
        for i in range(2):
            self.recorder.append_deployment_outcome(_make_outcome(outcome_id=f"outcome_{i}"))
        assert self.reader.locate() == self.reader.locate()


class TestOutcomeReaderRetrieve:
    """Tests for the retrieve responsibility."""

    def setup_method(self):
        self.temp_dir = tempfile.mkdtemp()
        self.recorder = ExperimentRecorder(self.temp_dir)
        self.reader = OutcomeReader(self.recorder)

    def teardown_method(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_retrieve_returns_raw_artifact(self):
        run_id = self.recorder.append_deployment_outcome(_make_outcome())
        artifact = self.reader.retrieve(run_id)
        assert isinstance(artifact, dict)
        assert artifact["outcome_id"] == "outcome_001"

    def test_retrieve_absent_run_raises(self):
        with pytest.raises(InvalidDeploymentOutcomeData):
            self.reader.retrieve("run_999999")

    def test_retrieve_does_not_modify_persisted_file(self):
        run_id = self.recorder.append_deployment_outcome(_make_outcome())
        file_path = (
            Path(self.temp_dir) / "research" / "experiments" / run_id / "deployment_outcome.json"
        )
        before = file_path.read_text(encoding="utf-8")
        self.reader.retrieve(run_id)
        after = file_path.read_text(encoding="utf-8")
        assert before == after


class TestOutcomeReaderDeserialize:
    """Tests for the deserialize responsibility."""

    def setup_method(self):
        self.temp_dir = tempfile.mkdtemp()
        self.recorder = ExperimentRecorder(self.temp_dir)
        self.reader = OutcomeReader(self.recorder)

    def teardown_method(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _artifact_for(self, run_id):
        file_path = (
            Path(self.temp_dir) / "research" / "experiments" / run_id / "deployment_outcome.json"
        )
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def test_deserialize_reconstructs_immutable_outcome(self):
        run_id = self.recorder.append_deployment_outcome(_make_outcome())
        artifact = self._artifact_for(run_id)
        outcome = self.reader.deserialize(artifact)
        assert isinstance(outcome, DeploymentOutcome)
        assert outcome.outcome_id == "outcome_001"
        assert outcome.strategy_manifest_id == "manifest_001"
        assert outcome.provenance.research_candidate_id == "candidate_001"
        assert outcome.provenance.created_timestamp == datetime(2026, 1, 1, 12, 0, 0)
        assert outcome.execution_reference == "execution_001"
        assert outcome.execution_metadata["status"] == "SUCCESS"
        assert outcome.deployment_metadata["strategy_name"] == "TestStrategy"
        assert outcome.recorded_timestamp == datetime(2026, 1, 1, 12, 30, 0)
        assert outcome.schema_version == "1.0.0"

    def test_deserialize_rejects_non_dict(self):
        with pytest.raises(InvalidDeploymentOutcomeData):
            self.reader.deserialize("not-a-dict")

    def test_deserialize_rejects_missing_provenance(self):
        run_id = self.recorder.append_deployment_outcome(_make_outcome())
        artifact = self._artifact_for(run_id)
        del artifact["provenance"]
        with pytest.raises(InvalidDeploymentOutcomeData):
            self.reader.deserialize(artifact)

    def test_deserialize_rejects_invalid_timestamp(self):
        run_id = self.recorder.append_deployment_outcome(_make_outcome())
        artifact = self._artifact_for(run_id)
        artifact["recorded_timestamp"] = "not-a-timestamp"
        with pytest.raises(InvalidDeploymentOutcomeData):
            self.reader.deserialize(artifact)

    def test_deserialize_produces_mappingproxy_metadata(self):
        run_id = self.recorder.append_deployment_outcome(_make_outcome())
        artifact = self._artifact_for(run_id)
        outcome = self.reader.deserialize(artifact)
        assert isinstance(outcome.execution_metadata, MappingProxyType)
        assert isinstance(outcome.deployment_metadata, MappingProxyType)


class TestOutcomeReaderValidate:
    """Tests for the validate responsibility."""

    def setup_method(self):
        self.temp_dir = tempfile.mkdtemp()
        self.recorder = ExperimentRecorder(self.temp_dir)
        self.reader = OutcomeReader(self.recorder)

    def teardown_method(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _artifact_for(self, run_id):
        file_path = (
            Path(self.temp_dir) / "research" / "experiments" / run_id / "deployment_outcome.json"
        )
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def test_validate_returns_true_for_valid_artifact(self):
        run_id = self.recorder.append_deployment_outcome(_make_outcome())
        assert self.reader.validate(self._artifact_for(run_id)) is True

    def test_validate_rejects_tampered_schema_version(self):
        """Tampered schema_version outside the canonical pattern is rejected."""
        run_id = self.recorder.append_deployment_outcome(_make_outcome())
        artifact = self._artifact_for(run_id)
        artifact["schema_version"] = "1.0"
        with pytest.raises(InvalidDeploymentOutcomeData):
            self.reader.validate(artifact)

    def test_validate_rejects_interpretation_field(self):
        """Reading must never accept artifacts carrying interpretation fields."""
        run_id = self.recorder.append_deployment_outcome(_make_outcome())
        artifact = self._artifact_for(run_id)
        artifact["execution_metadata"]["supports_hypothesis"] = True
        with pytest.raises(InvalidDeploymentOutcomeData):
            self.reader.validate(artifact)

    def test_validate_does_not_modify_artifact(self):
        run_id = self.recorder.append_deployment_outcome(_make_outcome())
        artifact = self._artifact_for(run_id)
        before = json.dumps(artifact, sort_keys=True)
        self.reader.validate(artifact)
        after = json.dumps(artifact, sort_keys=True)
        assert before == after


class TestOutcomeReaderReturn:
    """Tests for the return responsibility (read / read_all)."""

    def setup_method(self):
        self.temp_dir = tempfile.mkdtemp()
        self.recorder = ExperimentRecorder(self.temp_dir)
        self.reader = OutcomeReader(self.recorder)

    def teardown_method(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_read_returns_immutable_outcome(self):
        run_id = self.recorder.append_deployment_outcome(_make_outcome())
        outcome = self.reader.read(run_id)
        assert isinstance(outcome, DeploymentOutcome)
        assert outcome.outcome_id == "outcome_001"

    def test_read_all_returns_all_in_deterministic_order(self):
        for i in range(3):
            self.recorder.append_deployment_outcome(_make_outcome(outcome_id=f"outcome_{i}"))
        outcomes = self.reader.read_all()
        assert len(outcomes) == 3
        assert outcomes == self.reader.read_all()
        assert all(isinstance(o, DeploymentOutcome) for o in outcomes)

    def test_read_missing_run_raises(self):
        with pytest.raises(InvalidDeploymentOutcomeData):
            self.reader.read("run_999999")

    def test_repeated_reads_are_identical(self):
        run_id = self.recorder.append_deployment_outcome(_make_outcome())
        assert self.reader.read(run_id) == self.reader.read(run_id)


class TestOutcomeReaderReadOnly:
    """Tests for the read-only guarantees."""

    def setup_method(self):
        self.temp_dir = tempfile.mkdtemp()
        self.recorder = ExperimentRecorder(self.temp_dir)
        self.reader = OutcomeReader(self.recorder)

    def teardown_method(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_no_interpretation_fields(self):
        """OutcomeReader must never add interpretation fields to artifacts."""
        run_id = self.recorder.append_deployment_outcome(_make_outcome())
        file_path = (
            Path(self.temp_dir) / "research" / "experiments" / run_id / "deployment_outcome.json"
        )
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.reader.read(run_id)
        with open(file_path, "r", encoding="utf-8") as f:
            after = json.load(f)
        forbidden = (
            "supports_hypothesis",
            "challenges_hypothesis",
            "validation_result",
            "behaviour_correctness",
            "quality_score",
            "recommendation",
        )
        assert not any(key in data for key in forbidden)
        assert data == after

    def test_no_runtime_state_between_reads(self):
        run_id = self.recorder.append_deployment_outcome(_make_outcome())
        first = self.reader.read(run_id)
        second = self.reader.read(run_id)
        assert first == second
        assert first is not second
        assert self.reader.recorder is not None

    def test_no_mutation_of_returned_outcome(self):
        run_id = self.recorder.append_deployment_outcome(_make_outcome())
        outcome = self.reader.read(run_id)
        with pytest.raises(TypeError):
            outcome.execution_metadata["status"] = "MUTATED"
        with pytest.raises(TypeError):
            outcome.deployment_metadata["strategy_name"] = "MUTATED"


class TestOutcomeReaderRepositoryAbstraction:
    """Tests that OutcomeReader delegates persistence to ExperimentRecorder."""

    def setup_method(self):
        self.temp_dir = tempfile.mkdtemp()
        self.recorder = ExperimentRecorder(self.temp_dir)
        self.reader = OutcomeReader(self.recorder)

    def teardown_method(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_reader_uses_recorder_for_locate(self):
        for i in range(2):
            self.recorder.append_deployment_outcome(_make_outcome(outcome_id=f"outcome_{i}"))
        assert self.reader.locate() == self.recorder.list_deployment_outcomes()

    def test_reader_uses_recorder_for_retrieve(self):
        run_id = self.recorder.append_deployment_outcome(_make_outcome())
        assert self.reader.retrieve(run_id) == self.recorder.get_deployment_outcome(run_id)

    def test_reader_is_stateless_instance(self):
        assert self.reader.recorder is self.recorder
        assert not hasattr(self.reader, "_cache")
        assert not hasattr(self.reader, "outcomes")
