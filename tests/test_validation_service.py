import unittest
from datetime import datetime, timedelta

from boe.science import (
    Hypothesis,
    HypothesisStatus,
    Experiment,
    ExperimentStatus,
    Validation,
    ValidationStatus,
    ValidationService,
    InvalidServiceOperation
)

class TestValidationService(unittest.TestCase):

    def setUp(self):
        self.dt = datetime(2026, 1, 1, 12, 0, 0)
        self.service = ValidationService()
        
        self.hypothesis = Hypothesis(
            identifier="HYP-001",
            title="SPX Mean Reversion",
            description="Testing MR",
            author="Researcher A",
            created_timestamp=self.dt,
            status=HypothesisStatus.ACTIVE
        )
        
        self.experiment = Experiment(
            identifier="EXP-001",
            hypothesis_identifier="HYP-001",
            title="MR on SPX",
            description="Testing MR with Lookback 20",
            markets=("SPX",),
            configuration={"lookback": 20},
            analysis_period={"start": self.dt, "end": self.dt + timedelta(days=30)},
            created_timestamp=self.dt,
            status=ExperimentStatus.COMPLETED
        )

    def test_successful_validation_creation(self):
        validation = self.service.create_validation(
            identifier="VAL-001",
            hypothesis=self.hypothesis,
            experiment=self.experiment,
            summary="MR was successful",
            completed_timestamp=self.dt + timedelta(days=31),
            status=ValidationStatus.VALIDATED
        )
        
        self.assertIsInstance(validation, Validation)
        self.assertEqual(validation.identifier, "VAL-001")
        self.assertEqual(validation.experiment_identifier, "EXP-001")
        self.assertEqual(validation.hypothesis_identifier, "HYP-001")
        self.assertEqual(validation.status, ValidationStatus.VALIDATED)

    def test_invalid_hypothesis_linkage(self):
        # Experiment belongs to HYP-002, but we pass HYP-001
        invalid_experiment = Experiment(
            identifier="EXP-002",
            hypothesis_identifier="HYP-002",
            title="MR on SPX",
            description="Testing MR",
            markets=("SPX",),
            configuration={"lookback": 20},
            analysis_period={"start": self.dt, "end": self.dt + timedelta(days=30)},
            created_timestamp=self.dt,
            status=ExperimentStatus.COMPLETED
        )
        
        with self.assertRaises(InvalidServiceOperation):
            self.service.create_validation(
                identifier="VAL-001",
                hypothesis=self.hypothesis, # HYP-001
                experiment=invalid_experiment, # Points to HYP-002
                summary="Mismatch test",
                completed_timestamp=self.dt,
                status=ValidationStatus.VALIDATED
            )
            
    def test_deterministic_and_immutable_output(self):
        v1 = self.service.create_validation(
            identifier="VAL-001",
            hypothesis=self.hypothesis,
            experiment=self.experiment,
            summary="Determinism test",
            completed_timestamp=self.dt,
            status=ValidationStatus.VALIDATED
        )
        
        v2 = self.service.create_validation(
            identifier="VAL-001",
            hypothesis=self.hypothesis,
            experiment=self.experiment,
            summary="Determinism test",
            completed_timestamp=self.dt,
            status=ValidationStatus.VALIDATED
        )
        
        self.assertEqual(v1, v2)
        self.assertEqual(hash(v1), hash(v2))
        
        with self.assertRaises(Exception): # FrozenInstanceError
            v1.identifier = "VAL-002" # type: ignore

if __name__ == '__main__':
    unittest.main()
