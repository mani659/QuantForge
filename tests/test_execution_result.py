import unittest
from types import MappingProxyType
from dataclasses import FrozenInstanceError
from datetime import datetime

from boe.execution import (
    ExecutionResult,
    ExecutionStatus,
    ExecutionResultValidationError
)

class TestExecutionResult(unittest.TestCase):

    def setUp(self):
        self.dt = datetime(2026, 1, 1, 12, 0, 0)
        self.metadata = MappingProxyType({"env": "test"})
        
        self.valid_result = ExecutionResult(
            candidate_id="c_1",
            timeline_id="t_1",
            observation_id="o_1",
            schema_version="1.0",
            status=ExecutionStatus.SUCCESS,
            metadata=self.metadata,
            timestamp=self.dt
        )

    def test_immutable_construction(self):
        with self.assertRaises(FrozenInstanceError):
            self.valid_result.status = ExecutionStatus.FAILED # type: ignore

    def test_deterministic_outputs(self):
        result2 = ExecutionResult(
            candidate_id="c_1",
            timeline_id="t_1",
            observation_id="o_1",
            schema_version="1.0",
            status=ExecutionStatus.SUCCESS,
            metadata=self.metadata,
            timestamp=self.dt
        )
        
        self.assertEqual(self.valid_result, result2)
        self.assertEqual(hash(self.valid_result), hash(result2))

    def test_schema_validation_and_errors(self):
        with self.assertRaisesRegex(ExecutionResultValidationError, "status must be an ExecutionStatus enum"):
            ExecutionResult(
                candidate_id="c_1",
                timeline_id="t_1",
                observation_id="o_1",
                schema_version="1.0",
                status="SUCCESS", # Invalid, must be enum
                metadata=self.metadata,
                timestamp=self.dt
            )
            
        with self.assertRaisesRegex(ExecutionResultValidationError, "metadata must be a MappingProxyType"):
            ExecutionResult(
                candidate_id="c_1",
                timeline_id="t_1",
                observation_id="o_1",
                schema_version="1.0",
                status=ExecutionStatus.SUCCESS,
                metadata={"env": "test"}, # Invalid, must be MappingProxyType
                timestamp=self.dt
            )
            
        with self.assertRaisesRegex(ExecutionResultValidationError, "candidate_id must be a non-empty string"):
            ExecutionResult(
                candidate_id="",
                timeline_id="t_1",
                observation_id="o_1",
                schema_version="1.0",
                status=ExecutionStatus.SUCCESS,
                metadata=self.metadata,
                timestamp=self.dt
            )

if __name__ == '__main__':
    unittest.main()
