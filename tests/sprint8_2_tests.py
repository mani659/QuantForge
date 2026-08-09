"""Unit tests for Sprint 8.2 (Deployment Outcome Capture)."""
import pytest
from datetime import datetime
from types import MappingProxyType
from research.lifecycle.deployment_outcome import DeploymentOutcome
from research.lifecycle.provenance import Provenance
from research.lifecycle.strategy_manifest import StrategyManifest
from research.lifecycle.outcome_appender import OutcomeAppender
from research.experiment_recorder import ExperimentRecorder
from boe.execution.result import ExecutionResult, ExecutionStatus
from boe.execution.execution_errors import ExecutionResultValidationError
import tempfile
import os
from pathlib import Path


class TestDeploymentOutcome:
    """Tests for the DeploymentOutcome domain object."""

    def test_creation(self):
        """Test that a DeploymentOutcome can be created with valid data."""
        provenance = Provenance(
            research_candidate_id="candidate_001",
            validation_id="validation_001",
            experiment_id="experiment_001",
            strategy_manifest_id="manifest_001",
            created_timestamp=datetime(2026, 1, 1, 12, 0, 0),
        )

        execution_metadata = MappingProxyType({
            "status": "SUCCESS",
            "trades_executed": 10,
            "total_return": 0.05,
        })

        deployment_metadata = MappingProxyType({
            "strategy_name": "TestStrategy",
            "deployment_time": "2026-01-01T12:00:00",
        })

        outcome = DeploymentOutcome(
            outcome_id="outcome_001",
            strategy_manifest_id="manifest_001",
            provenance=provenance,
            execution_reference="execution_001",
            execution_metadata=execution_metadata,
            deployment_metadata=deployment_metadata,
            recorded_timestamp=datetime(2026, 1, 1, 12, 0, 0),
            schema_version="1.0.0",
        )

        assert outcome.outcome_id == "outcome_001"
        assert outcome.strategy_manifest_id == "manifest_001"
        assert outcome.provenance.research_candidate_id == "candidate_001"
        assert outcome.execution_reference == "execution_001"
        assert outcome.execution_metadata["status"] == "SUCCESS"
        assert outcome.deployment_metadata["strategy_name"] == "TestStrategy"
        assert outcome.recorded_timestamp == datetime(2026, 1, 1, 12, 0, 0)
        assert outcome.schema_version == "1.0.0"

    def test_immutability(self):
        """Test that DeploymentOutcome is immutable."""
        provenance = Provenance(
            research_candidate_id="candidate_001",
            validation_id="validation_001",
            experiment_id="experiment_001",
            strategy_manifest_id="manifest_001",
            created_timestamp=datetime(2026, 1, 1, 12, 0, 0),
        )

        execution_metadata = MappingProxyType({})
        deployment_metadata = MappingProxyType({})

        outcome = DeploymentOutcome(
            outcome_id="outcome_001",
            strategy_manifest_id="manifest_001",
            provenance=provenance,
            execution_reference="execution_001",
            execution_metadata=execution_metadata,
            deployment_metadata=deployment_metadata,
            recorded_timestamp=datetime(2026, 1, 1, 12, 0, 0),
            schema_version="1.0.0",
        )

        # Attempting to modify should raise an exception
        try:
            outcome.outcome_id = "new_id"
            assert False, "Should not be able to modify immutable dataclass"
        except (AttributeError, TypeError):
            pass

    def test_hash(self):
        """Test that DeploymentOutcome is hashable."""
        provenance = Provenance(
            research_candidate_id="candidate_001",
            validation_id="validation_001",
            experiment_id="experiment_001",
            strategy_manifest_id="manifest_001",
            created_timestamp=datetime(2026, 1, 1, 12, 0, 0),
        )

        execution_metadata = MappingProxyType({})
        deployment_metadata = MappingProxyType({})

        outcome1 = DeploymentOutcome(
            outcome_id="outcome_001",
            strategy_manifest_id="manifest_001",
            provenance=provenance,
            execution_reference="execution_001",
            execution_metadata=execution_metadata,
            deployment_metadata=deployment_metadata,
            recorded_timestamp=datetime(2026, 1, 1, 12, 0, 0),
            schema_version="1.0.0",
        )

        outcome2 = DeploymentOutcome(
            outcome_id="outcome_001",
            strategy_manifest_id="manifest_001",
            provenance=provenance,
            execution_reference="execution_001",
            execution_metadata=execution_metadata,
            deployment_metadata=deployment_metadata,
            recorded_timestamp=datetime(2026, 1, 1, 12, 0, 0),
            schema_version="1.0.0",
        )

        # Equal outcomes should have same hash
        assert outcome1 == outcome2
        assert hash(outcome1) == hash(outcome2)

    def test_validation_rules(self):
        """Test that invalid inputs are rejected."""
        provenance = Provenance(
            research_candidate_id="candidate_001",
            validation_id="validation_001",
            experiment_id="experiment_001",
            strategy_manifest_id="manifest_001",
            created_timestamp=datetime(2026, 1, 1, 12, 0, 0),
        )

        execution_metadata = MappingProxyType({})
        deployment_metadata = MappingProxyType({})

        # Test invalid outcome_id
        with pytest.raises(Exception):
            DeploymentOutcome(
                outcome_id="",
                strategy_manifest_id="manifest_001",
                provenance=provenance,
                execution_reference="execution_001",
                execution_metadata=execution_metadata,
                deployment_metadata=deployment_metadata,
                recorded_timestamp=datetime(2026, 1, 1, 12, 0, 0),
                schema_version="1.0.0",
            )

        # Test invalid provenance
        with pytest.raises(Exception):
            DeploymentOutcome(
                outcome_id="outcome_001",
                strategy_manifest_id="manifest_001",
                provenance="invalid",
                execution_reference="execution_001",
                execution_metadata=execution_metadata,
                deployment_metadata=deployment_metadata,
                recorded_timestamp=datetime(2026, 1, 1, 12, 0, 0),
                schema_version="1.0.0",
            )

        # Test invalid execution_metadata
        with pytest.raises(Exception):
            DeploymentOutcome(
                outcome_id="outcome_001",
                strategy_manifest_id="manifest_001",
                provenance=provenance,
                execution_reference="execution_001",
                execution_metadata="invalid",
                deployment_metadata=deployment_metadata,
                recorded_timestamp=datetime(2026, 1, 1, 12, 0, 0),
                schema_version="1.0.0",
            )

    def test_constitutional_boundaries(self):
        """Test that execution_metadata cannot contain hypothesis evaluation."""
        provenance = Provenance(
            research_candidate_id="candidate_001",
            validation_id="validation_001",
            experiment_id="experiment_001",
            strategy_manifest_id="manifest_001",
            created_timestamp=datetime(2026, 1, 1, 12, 0, 0),
        )

        # Test with hypothesis evaluation (should raise exception)
        execution_metadata = MappingProxyType({
            "supports_hypothesis": True,
            "challenges_hypothesis": False,
        })

        deployment_metadata = MappingProxyType({})

        with pytest.raises(Exception):
            DeploymentOutcome(
                outcome_id="outcome_001",
                strategy_manifest_id="manifest_001",
                provenance=provenance,
                execution_reference="execution_001",
                execution_metadata=execution_metadata,
                deployment_metadata=deployment_metadata,
                recorded_timestamp=datetime(2026, 1, 1, 12, 0, 0),
                schema_version="1.0.0",
            )

        # Test with classification (should raise exception)
        execution_metadata = MappingProxyType({
            "behaviour_correctness": True,
            "strategy_quality": "good",
        })

        with pytest.raises(Exception):
            DeploymentOutcome(
                outcome_id="outcome_001",
                strategy_manifest_id="manifest_001",
                provenance=provenance,
                execution_reference="execution_001",
                execution_metadata=execution_metadata,
                deployment_metadata=deployment_metadata,
                recorded_timestamp=datetime(2026, 1, 1, 12, 0, 0),
                schema_version="1.0.0",
            )

        # Test with validation (should raise exception)
        execution_metadata = MappingProxyType({
            "validation_result": "VALIDATED",
        })

        with pytest.raises(Exception):
            DeploymentOutcome(
                outcome_id="outcome_001",
                strategy_manifest_id="manifest_001",
                provenance=provenance,
                execution_reference="execution_001",
                execution_metadata=execution_metadata,
                deployment_metadata=deployment_metadata,
                recorded_timestamp=datetime(2026, 1, 1, 12, 0, 0),
                schema_version="1.0.0",
            )

    def test_valid_execution_metadata(self):
        """Test that valid operational facts are allowed in execution_metadata."""
        provenance = Provenance(
            research_candidate_id="candidate_001",
            validation_id="validation_001",
            experiment_id="experiment_001",
            strategy_manifest_id="manifest_001",
            created_timestamp=datetime(2026, 1, 1, 12, 0, 0),
        )

        # Test with valid operational facts only
        execution_metadata = MappingProxyType({
            "status": "SUCCESS",
            "trades_executed": 10,
            "total_return": 0.05,
            "execution_time_ms": 1500,
            "position_size": 1000.0,
        })

        deployment_metadata = MappingProxyType({})

        outcome = DeploymentOutcome(
            outcome_id="outcome_001",
            strategy_manifest_id="manifest_001",
            provenance=provenance,
            execution_reference="execution_001",
            execution_metadata=execution_metadata,
            deployment_metadata=deployment_metadata,
            recorded_timestamp=datetime(2026, 1, 1, 12, 0, 0),
            schema_version="1.0.0",
        )

        assert outcome.execution_metadata["status"] == "SUCCESS"
        assert outcome.execution_metadata["trades_executed"] == 10
        assert outcome.execution_metadata["total_return"] == 0.05


class TestOutcomeAppender:
    """Tests for the OutcomeAppender service."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        # Create a temporary directory for the experiment recorder
        self.temp_dir = tempfile.mkdtemp()
        self.experiment_recorder = ExperimentRecorder(self.temp_dir)

        # Create a mock StrategyManifest
        provenance = Provenance(
            research_candidate_id="candidate_001",
            validation_id="validation_001",
            experiment_id="experiment_001",
            strategy_manifest_id="manifest_001",
            created_timestamp=datetime(2026, 1, 1, 12, 0, 0),
        )

        self.strategy_manifest = StrategyManifest(
            strategy_id="strategy_001",
            behaviour_name="test_strategy",
            observer_ids=("observer_001",),
            interpretation_model_id="model_001",
            decision_policy_id="policy_001",
            risk_policy_id="risk_001",
            deployment_profile="production",
            manifest_version="1.0.0",
            provenance=provenance,
        )

        self.outcome_appender = OutcomeAppender(
            strategy_manifest=self.strategy_manifest,
            experiment_recorder=self.experiment_recorder,
        )

    def teardown_method(self):
        """Clean up after each test method."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_append_deployment_outcome(self):
        """Test that OutcomeAppender can append a deployment outcome."""
        execution_result = ExecutionResult(
            candidate_id="candidate_001",
            timeline_id="timeline_001",
            observation_id="observation_001",
            schema_version="1.0.0",
            status=ExecutionStatus.SUCCESS,
            metadata=MappingProxyType({
                "trades_executed": 10,
                "total_return": 0.05,
                "status": "SUCCESS",
            }),
            timestamp=datetime(2026, 1, 1, 12, 0, 0),
        )

        outcome_id = self.outcome_appender.append(execution_result)

        assert outcome_id.startswith("run_")

        # Verify the outcome was appended
        outcome_file = Path(self.temp_dir) / "research" / "experiments" / outcome_id / "deployment_outcome.json"
        assert outcome_file.exists()

        import json
        with open(outcome_file, "r") as f:
            deployment_data = json.load(f)

        assert deployment_data["outcome_id"] == f"outcome_candidate_001_{datetime(2026, 1, 1, 12, 0, 0).isoformat()}"
        assert deployment_data["strategy_manifest_id"] == "strategy_001"
        assert deployment_data["execution_reference"] == "candidate_001"
        assert deployment_data["execution_metadata"]["status"] == "SUCCESS"

    def test_stateless_behaviour(self):
        """Test that OutcomeAppender is stateless."""
        execution_result = ExecutionResult(
            candidate_id="candidate_001",
            timeline_id="timeline_001",
            observation_id="observation_001",
            schema_version="1.0.0",
            status=ExecutionStatus.SUCCESS,
            metadata=MappingProxyType({
                "trades_executed": 10,
                "status": "SUCCESS",
            }),
            timestamp=datetime(2026, 1, 1, 12, 0, 0),
        )

        # Append the same result twice
        outcome_id1 = self.outcome_appender.append(execution_result)
        outcome_id2 = self.outcome_appender.append(execution_result)

        # Both should be processed independently (different run IDs)
        assert outcome_id1 != outcome_id2
        assert outcome_id1.startswith("run_")
        assert outcome_id2.startswith("run_")

    def test_deterministic_output(self):
        """Test that OutcomeAppender produces deterministic output given same dependencies."""
        execution_result = ExecutionResult(
            candidate_id="candidate_001",
            timeline_id="timeline_001",
            observation_id="observation_001",
            schema_version="1.0.0",
            status=ExecutionStatus.SUCCESS,
            metadata=MappingProxyType({
                "trades_executed": 10,
                "status": "SUCCESS",
            }),
            timestamp=datetime(2026, 1, 1, 12, 0, 0),
        )

        # Use the same dependencies to append the same execution result
        outcome_id1 = self.outcome_appender.append(execution_result)

        # Create a fresh OutcomeAppender with the same dependencies
        new_appender = OutcomeAppender(
            strategy_manifest=self.strategy_manifest,
            experiment_recorder=self.experiment_recorder,
        )

        outcome_id2 = new_appender.append(execution_result)

        # The system should generate sequential run IDs deterministically
        # Both should be valid run IDs
        assert outcome_id1.startswith("run_")
        assert outcome_id2.startswith("run_")

        # The IDs should be different (different runs) but algorithmically deterministic
        # i.e., if we were to rewind time, the same sequence would occur
        import re
        run_num1 = int(re.search(r"run_(\d+)", outcome_id1).group(1))
        run_num2 = int(re.search(r"run_(\d+)", outcome_id2).group(1))
        assert run_num2 == run_num1 + 1

    def test_termination_rules(self):
        """Test that OutcomeAppender terminates correctly."""
        execution_result = ExecutionResult(
            candidate_id="candidate_001",
            timeline_id="timeline_001",
            observation_id="observation_001",
            schema_version="1.0.0",
            status=ExecutionStatus.SUCCESS,
            metadata=MappingProxyType({
                "trades_executed": 10,
                "status": "SUCCESS",
            }),
            timestamp=datetime(2026, 1, 1, 12, 0, 0),
        )

        # OutcomeAppender should not have any analysis/promotion methods
        assert not hasattr(self.outcome_appender, "analyze")
        assert not hasattr(self.outcome_appender, "promote")
        assert not hasattr(self.outcome_appender, "optimize")

        # Should only have append method
        assert hasattr(self.outcome_appender, "append")

    def test_no_scientific_reasoning(self):
        """Test that OutcomeAppender does not perform scientific reasoning."""
        execution_result = ExecutionResult(
            candidate_id="candidate_001",
            timeline_id="timeline_001",
            observation_id="observation_001",
            schema_version="1.0.0",
            status=ExecutionStatus.SUCCESS,
            metadata=MappingProxyType({
                "trades_executed": 10,
                "status": "SUCCESS",
            }),
            timestamp=datetime(2026, 1, 1, 12, 0, 0),
        )

        # Append should not have any hypothesis evaluation/classification
        outcome_id = self.outcome_appender.append(execution_result)

        # The outcome file should not contain scientific reasoning
        outcome_file = Path(self.temp_dir) / "research" / "experiments" / outcome_id / "deployment_outcome.json"
        assert outcome_file.exists()

        import json
        with open(outcome_file, "r") as f:
            deployment_data = json.load(f)

        # Should not contain scientific reasoning fields
        assert "supports_hypothesis" not in deployment_data
        assert "challenges_hypothesis" not in deployment_data
        assert "validation_result" not in deployment_data
        assert "behaviour_correctness" not in deployment_data


class TestExperimentRecorder:
    """Tests for the ExperimentRecorder append_deployment_outcome method."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.temp_dir = tempfile.mkdtemp()
        self.experiment_recorder = ExperimentRecorder(self.temp_dir)

    def teardown_method(self):
        """Clean up after each test method."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_append_deployment_outcome(self):
        """Test that ExperimentRecorder can append a deployment outcome."""
        from research.lifecycle.deployment_outcome import DeploymentOutcome
        from research.lifecycle.provenance import Provenance

        provenance = Provenance(
            research_candidate_id="candidate_001",
            validation_id="validation_001",
            experiment_id="experiment_001",
            strategy_manifest_id="manifest_001",
            created_timestamp=datetime(2026, 1, 1, 12, 0, 0),
        )

        execution_metadata = MappingProxyType({
            "status": "SUCCESS",
            "trades_executed": 10,
        })

        deployment_metadata = MappingProxyType({
            "strategy_name": "TestStrategy",
        })

        deployment_outcome = DeploymentOutcome(
            outcome_id="outcome_001",
            strategy_manifest_id="manifest_001",
            provenance=provenance,
            execution_reference="execution_001",
            execution_metadata=execution_metadata,
            deployment_metadata=deployment_metadata,
            recorded_timestamp=datetime(2026, 1, 1, 12, 0, 0),
            schema_version="1.0.0",
        )

        outcome_id = self.experiment_recorder.append_deployment_outcome(deployment_outcome)

        assert outcome_id.startswith("run_")

        # Verify the outcome was saved
        outcome_file = Path(self.temp_dir) / "research" / "experiments" / outcome_id / "deployment_outcome.json"
        assert outcome_file.exists()

        import json
        with open(outcome_file, "r") as f:
            deployment_data = json.load(f)

        assert deployment_data["outcome_id"] == "outcome_001"
        assert deployment_data["strategy_manifest_id"] == "manifest_001"
        assert deployment_data["execution_reference"] == "execution_001"

    def test_append_only(self):
        """Test that ExperimentRecorder is append-only."""
        from research.lifecycle.deployment_outcome import DeploymentOutcome
        from research.lifecycle.provenance import Provenance

        provenance = Provenance(
            research_candidate_id="candidate_001",
            validation_id="validation_001",
            experiment_id="experiment_001",
            strategy_manifest_id="manifest_001",
            created_timestamp=datetime(2026, 1, 1, 12, 0, 0),
        )

        execution_metadata = MappingProxyType({})
        deployment_metadata = MappingProxyType({})

        deployment_outcome = DeploymentOutcome(
            outcome_id="outcome_001",
            strategy_manifest_id="manifest_001",
            provenance=provenance,
            execution_reference="execution_001",
            execution_metadata=execution_metadata,
            deployment_metadata=deployment_metadata,
            recorded_timestamp=datetime(2026, 1, 1, 12, 0, 0),
            schema_version="1.0.0",
        )

        # Append first outcome
        outcome_id1 = self.experiment_recorder.append_deployment_outcome(deployment_outcome)

        # Append second outcome (should have different run ID)
        deployment_outcome2 = DeploymentOutcome(
            outcome_id="outcome_002",
            strategy_manifest_id="manifest_002",
            provenance=provenance,
            execution_reference="execution_002",
            execution_metadata=execution_metadata,
            deployment_metadata=deployment_metadata,
            recorded_timestamp=datetime(2026, 1, 1, 12, 0, 0),
            schema_version="1.0.0",
        )

        outcome_id2 = self.experiment_recorder.append_deployment_outcome(deployment_outcome2)

        # Run IDs should be different
        assert outcome_id1 != outcome_id2

        # Both should exist
        outcome_file1 = Path(self.temp_dir) / "research" / "experiments" / outcome_id1 / "deployment_outcome.json"
        outcome_file2 = Path(self.temp_dir) / "research" / "experiments" / outcome_id2 / "deployment_outcome.json"

        assert outcome_file1.exists()
        assert outcome_file2.exists()

    def test_deterministic_persistence(self):
        """Test that ExperimentRecorder produces deterministic persistence."""
        from research.lifecycle.deployment_outcome import DeploymentOutcome
        from research.lifecycle.provenance import Provenance

        provenance = Provenance(
            research_candidate_id="candidate_001",
            validation_id="validation_001",
            experiment_id="experiment_001",
            strategy_manifest_id="manifest_001",
            created_timestamp=datetime(2026, 1, 1, 12, 0, 0),
        )

        execution_metadata = MappingProxyType({})
        deployment_metadata = MappingProxyType({})

        deployment_outcome = DeploymentOutcome(
            outcome_id="outcome_001",
            strategy_manifest_id="manifest_001",
            provenance=provenance,
            execution_reference="execution_001",
            execution_metadata=execution_metadata,
            deployment_metadata=deployment_metadata,
            recorded_timestamp=datetime(2026, 1, 1, 12, 0, 0),
            schema_version="1.0.0",
        )

        # Append with first recorder
        outcome_id1 = self.experiment_recorder.append_deployment_outcome(deployment_outcome)

        # Create a new recorder and append with same data
        new_recorder = ExperimentRecorder(self.temp_dir)
        outcome_id2 = new_recorder.append_deployment_outcome(deployment_outcome)

        # The system should generate sequential run IDs deterministically
        # Both should be valid run IDs
        assert outcome_id1.startswith("run_")
        assert outcome_id2.startswith("run_")

        # The IDs should be different (different runs) but algorithmically deterministic
        # i.e., if we were to rewind time, the same sequence would occur
        import re
        run_num1 = int(re.search(r"run_(\d+)", outcome_id1).group(1))
        run_num2 = int(re.search(r"run_(\d+)", outcome_id2).group(1))
        assert run_num2 == run_num1 + 1

    def test_append_only_ledger(self):
        """Test that ExperimentRecorder maintains an append-only ledger."""
        from research.lifecycle.deployment_outcome import DeploymentOutcome
        from research.lifecycle.provenance import Provenance

        provenance = Provenance(
            research_candidate_id="candidate_001",
            validation_id="validation_001",
            experiment_id="experiment_001",
            strategy_manifest_id="manifest_001",
            created_timestamp=datetime(2026, 1, 1, 12, 0, 0),
        )

        execution_metadata = MappingProxyType({})
        deployment_metadata = MappingProxyType({})

        deployment_outcome = DeploymentOutcome(
            outcome_id="outcome_001",
            strategy_manifest_id="manifest_001",
            provenance=provenance,
            execution_reference="execution_001",
            execution_metadata=execution_metadata,
            deployment_metadata=deployment_metadata,
            recorded_timestamp=datetime(2026, 1, 1, 12, 0, 0),
            schema_version="1.0.0",
        )

        # Append multiple outcomes
        outcome_id1 = self.experiment_recorder.append_deployment_outcome(deployment_outcome)

        deployment_outcome2 = DeploymentOutcome(
            outcome_id="outcome_002",
            strategy_manifest_id="manifest_002",
            provenance=provenance,
            execution_reference="execution_002",
            execution_metadata=execution_metadata,
            deployment_metadata=deployment_metadata,
            recorded_timestamp=datetime(2026, 1, 1, 12, 0, 0),
            schema_version="1.0.0",
        )

        outcome_id2 = self.experiment_recorder.append_deployment_outcome(deployment_outcome2)

        # All outcomes should be preserved
        assert outcome_id1 != outcome_id2

        outcome_file1 = Path(self.temp_dir) / "research" / "experiments" / outcome_id1 / "deployment_outcome.json"
        outcome_file2 = Path(self.temp_dir) / "research" / "experiments" / outcome_id2 / "deployment_outcome.json"

        assert outcome_file1.exists()
        assert outcome_file2.exists()


class TestIntegration:
    """Integration tests for Sprint 8.2."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.temp_dir = tempfile.mkdtemp()
        self.experiment_recorder = ExperimentRecorder(self.temp_dir)

        # Create a mock StrategyManifest
        provenance = Provenance(
            research_candidate_id="candidate_001",
            validation_id="validation_001",
            experiment_id="experiment_001",
            strategy_manifest_id="manifest_001",
            created_timestamp=datetime(2026, 1, 1, 12, 0, 0),
        )

        self.strategy_manifest = StrategyManifest(
            strategy_id="strategy_001",
            behaviour_name="test_strategy",
            observer_ids=("observer_001",),
            interpretation_model_id="model_001",
            decision_policy_id="policy_001",
            risk_policy_id="risk_001",
            deployment_profile="production",
            manifest_version="1.0.0",
            provenance=provenance,
        )

        self.outcome_appender = OutcomeAppender(
            strategy_manifest=self.strategy_manifest,
            experiment_recorder=self.experiment_recorder,
        )

    def teardown_method(self):
        """Clean up after each test method."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_full_integration(self):
        """Test the full Sprint 8.2 integration: ExecutionResult → OutcomeAppender → DeploymentOutcome → ExperimentRecorder."""
        # Create a valid ExecutionResult
        execution_result = ExecutionResult(
            candidate_id="candidate_001",
            timeline_id="timeline_001",
            observation_id="observation_001",
            schema_version="1.0.0",
            status=ExecutionStatus.SUCCESS,
            metadata=MappingProxyType({
                "trades_executed": 10,
                "total_return": 0.05,
                "status": "SUCCESS",
            }),
            timestamp=datetime(2026, 1, 1, 12, 0, 0),
        )

        # Use OutcomeAppender to capture the execution result
        outcome_id = self.outcome_appender.append(execution_result)

        # Verify the outcome was appended
        assert outcome_id.startswith("run_")

        outcome_file = Path(self.temp_dir) / "research" / "experiments" / outcome_id / "deployment_outcome.json"
        assert outcome_file.exists()

        import json
        with open(outcome_file, "r") as f:
            deployment_data = json.load(f)

        # Verify the deployment outcome contains the expected data
        assert deployment_data["outcome_id"].startswith("outcome_candidate_001_")
        assert deployment_data["strategy_manifest_id"] == "strategy_001"
        assert deployment_data["execution_reference"] == "candidate_001"
        assert deployment_data["execution_metadata"]["status"] == "SUCCESS"
        assert deployment_data["execution_metadata"]["trades_executed"] == 10
        assert deployment_data["execution_metadata"]["total_return"] == 0.05

    def test_constitutional_boundaries_integration(self):
        """Test that the full integration respects constitutional boundaries."""
        execution_result = ExecutionResult(
            candidate_id="candidate_001",
            timeline_id="timeline_001",
            observation_id="observation_001",
            schema_version="1.0.0",
            status=ExecutionStatus.SUCCESS,
            metadata=MappingProxyType({
                "trades_executed": 10,
                "status": "SUCCESS",
            }),
            timestamp=datetime(2026, 1, 1, 12, 0, 0),
        )

        # Append the execution result
        outcome_id = self.outcome_appender.append(execution_result)

        # Verify the outcome does not contain scientific reasoning
        outcome_file = Path(self.temp_dir) / "research" / "experiments" / outcome_id / "deployment_outcome.json"
        assert outcome_file.exists()

        import json
        with open(outcome_file, "r") as f:
            deployment_data = json.load(f)

        # Should not contain scientific reasoning fields
        assert "supports_hypothesis" not in deployment_data
        assert "challenges_hypothesis" not in deployment_data
        assert "validation_result" not in deployment_data
        assert "behaviour_correctness" not in deployment_data
        assert "strategy_quality" not in deployment_data
        assert "scientific_significance" not in deployment_data

        # Should contain only operational facts
        assert "outcome_id" in deployment_data
        assert "strategy_manifest_id" in deployment_data
        assert "execution_reference" in deployment_data
        assert "execution_metadata" in deployment_data
        assert "deployment_metadata" in deployment_data
        assert "recorded_timestamp" in deployment_data

    def test_deterministic_integration(self):
        """Test that the full integration is deterministic."""
        execution_result = ExecutionResult(
            candidate_id="candidate_001",
            timeline_id="timeline_001",
            observation_id="observation_001",
            schema_version="1.0.0",
            status=ExecutionStatus.SUCCESS,
            metadata=MappingProxyType({
                "trades_executed": 10,
                "status": "SUCCESS",
            }),
            timestamp=datetime(2026, 1, 1, 12, 0, 0),
        )

        # Append with first OutcomeAppender
        outcome_id1 = self.outcome_appender.append(execution_result)

        # Create a new OutcomeAppender with same dependencies
        new_outcome_appender = OutcomeAppender(
            strategy_manifest=self.strategy_manifest,
            experiment_recorder=self.experiment_recorder,
        )

        outcome_id2 = new_outcome_appender.append(execution_result)

        # The system should generate sequential run IDs deterministically
        # Both should be valid run IDs
        assert outcome_id1.startswith("run_")
        assert outcome_id2.startswith("run_")

        # The IDs should be different (different runs) but algorithmically deterministic
        # i.e., if we were to rewind time, the same sequence would occur
        import re
        run_num1 = int(re.search(r"run_(\d+)", outcome_id1).group(1))
        run_num2 = int(re.search(r"run_(\d+)", outcome_id2).group(1))
        assert run_num2 == run_num1 + 1

    def test_append_only_ledger_integration(self):
        """Test that the experiment ledger remains append-only."""
        execution_result1 = ExecutionResult(
            candidate_id="candidate_001",
            timeline_id="timeline_001",
            observation_id="observation_001",
            schema_version="1.0.0",
            status=ExecutionStatus.SUCCESS,
            metadata=MappingProxyType({
                "trades_executed": 10,
                "status": "SUCCESS",
            }),
            timestamp=datetime(2026, 1, 1, 12, 0, 0),
        )

        execution_result2 = ExecutionResult(
            candidate_id="candidate_002",
            timeline_id="timeline_002",
            observation_id="observation_002",
            schema_version="1.0.0",
            status=ExecutionStatus.SUCCESS,
            metadata=MappingProxyType({
                "trades_executed": 15,
                "status": "SUCCESS",
            }),
            timestamp=datetime(2026, 1, 1, 12, 0, 0),
        )

        # Append two different execution results
        outcome_id1 = self.outcome_appender.append(execution_result1)
        outcome_id2 = self.outcome_appender.append(execution_result2)

        # Both should be preserved
        assert outcome_id1 != outcome_id2

        outcome_file1 = Path(self.temp_dir) / "research" / "experiments" / outcome_id1 / "deployment_outcome.json"
        outcome_file2 = Path(self.temp_dir) / "research" / "experiments" / outcome_id2 / "deployment_outcome.json"

        assert outcome_file1.exists()
        assert outcome_file2.exists()

        import json
        with open(outcome_file1, "r") as f:
            deployment_data1 = json.load(f)

        with open(outcome_file2, "r") as f:
            deployment_data2 = json.load(f)

        # Both should have their own unique outcome IDs
        assert deployment_data1["outcome_id"].startswith("outcome_candidate_001_")
        assert deployment_data2["outcome_id"].startswith("outcome_candidate_002_")

        # Both should reference their own execution references
        assert deployment_data1["execution_reference"] == "candidate_001"
        assert deployment_data2["execution_reference"] == "candidate_002"