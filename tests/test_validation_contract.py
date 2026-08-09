import unittest
from datetime import datetime

from boe.science import (
    Validation,
    ValidationStatus,
    InvalidValidationData
)

class TestValidationContract(unittest.TestCase):

    def setUp(self):
        self.dt = datetime(2026, 1, 1, 12, 0, 0)
        
        self.valid_data = {
            "identifier": "VAL-001",
            "experiment_identifier": "EXP-001",
            "hypothesis_identifier": "HYP-001",
            "summary": "MR was validated",
            "completed_timestamp": self.dt,
            "status": ValidationStatus.VALIDATED
        }

    def test_immutable_construction_and_equality(self):
        v1 = Validation(**self.valid_data)
        v2 = Validation(**self.valid_data)
        
        self.assertEqual(v1.identifier, "VAL-001")
        self.assertEqual(v1.status, ValidationStatus.VALIDATED)
        
        # Test equality and hashing
        self.assertEqual(v1, v2)
        self.assertEqual(hash(v1), hash(v2))
        
        # Test immutability
        with self.assertRaises(Exception): # FrozenInstanceError
            v1.identifier = "VAL-002" # type: ignore

    def test_invalid_values(self):
        # Empty identifier
        data = self.valid_data.copy()
        data["identifier"] = ""
        with self.assertRaises(InvalidValidationData):
            Validation(**data)
            
        # Empty experiment_identifier
        data = self.valid_data.copy()
        data["experiment_identifier"] = ""
        with self.assertRaises(InvalidValidationData):
            Validation(**data)
            
        # Empty hypothesis_identifier
        data = self.valid_data.copy()
        data["hypothesis_identifier"] = ""
        with self.assertRaises(InvalidValidationData):
            Validation(**data)
            
        # Empty summary
        data = self.valid_data.copy()
        data["summary"] = ""
        with self.assertRaises(InvalidValidationData):
            Validation(**data)
            
        # Invalid timestamp
        data = self.valid_data.copy()
        data["completed_timestamp"] = "Not a datetime" # type: ignore
        with self.assertRaises(InvalidValidationData):
            Validation(**data)

    def test_status_validation(self):
        data = self.valid_data.copy()
        data["status"] = "INVALID_STATUS" # type: ignore
        with self.assertRaises(InvalidValidationData):
            Validation(**data)
            
        # Valid statuses should work
        for status in ValidationStatus:
            data["status"] = status
            v = Validation(**data)
            self.assertEqual(v.status, status)

if __name__ == '__main__':
    unittest.main()
