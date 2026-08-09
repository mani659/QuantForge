import unittest
from datetime import datetime, timedelta

from boe.science import (
    Experiment,
    ExperimentStatus,
    InvalidExperimentData
)

class TestExperimentContract(unittest.TestCase):

    def setUp(self):
        self.dt_start = datetime(2026, 1, 1, 12, 0, 0)
        self.dt_end = self.dt_start + timedelta(days=30)
        
        self.valid_data = {
            "identifier": "EXP-001",
            "hypothesis_identifier": "HYP-001",
            "title": "SPX MR Test",
            "description": "Testing MR",
            "markets": ["SPX"],
            "configuration": {"lookback": 20},
            "analysis_period": {"start": self.dt_start, "end": self.dt_end},
            "created_timestamp": self.dt_start,
            "status": ExperimentStatus.DRAFT
        }

    def test_immutable_construction_and_equality(self):
        e1 = Experiment(**self.valid_data)
        e2 = Experiment(**self.valid_data)
        
        self.assertEqual(e1.identifier, "EXP-001")
        self.assertEqual(e1.status, ExperimentStatus.DRAFT)
        
        # Test equality and hashing
        self.assertEqual(e1, e2)
        self.assertEqual(hash(e1), hash(e2))
        
        # Test immutability
        with self.assertRaises(Exception): # FrozenInstanceError
            e1.identifier = "EXP-002" # type: ignore

    def test_invalid_values(self):
        # Empty identifier
        data = self.valid_data.copy()
        data["identifier"] = ""
        with self.assertRaises(InvalidExperimentData):
            Experiment(**data)
            
        # Empty hypothesis_identifier
        data = self.valid_data.copy()
        data["hypothesis_identifier"] = ""
        with self.assertRaises(InvalidExperimentData):
            Experiment(**data)
            
        # Invalid markets
        data = self.valid_data.copy()
        data["markets"] = []
        with self.assertRaises(InvalidExperimentData):
            Experiment(**data)
            
        data["markets"] = [""]
        with self.assertRaises(InvalidExperimentData):
            Experiment(**data)
            
        data["markets"] = "SPX" # type: ignore
        with self.assertRaises(InvalidExperimentData):
            Experiment(**data)
            
        # Invalid configuration
        data = self.valid_data.copy()
        data["configuration"] = [] # type: ignore
        with self.assertRaises(InvalidExperimentData):
            Experiment(**data)
            
        # Invalid analysis period
        data = self.valid_data.copy()
        data["analysis_period"] = {"start": self.dt_start} # missing end
        with self.assertRaises(InvalidExperimentData):
            Experiment(**data)
            
        data["analysis_period"] = {"start": self.dt_end, "end": self.dt_start} # reversed
        with self.assertRaises(InvalidExperimentData):
            Experiment(**data)
            
        # Invalid timestamp
        data = self.valid_data.copy()
        data["created_timestamp"] = "Not a datetime" # type: ignore
        with self.assertRaises(InvalidExperimentData):
            Experiment(**data)

    def test_status_validation(self):
        data = self.valid_data.copy()
        data["status"] = "INVALID_STATUS" # type: ignore
        with self.assertRaises(InvalidExperimentData):
            Experiment(**data)
            
        # Valid statuses should work
        for status in ExperimentStatus:
            data["status"] = status
            e = Experiment(**data)
            self.assertEqual(e.status, status)

if __name__ == '__main__':
    unittest.main()
