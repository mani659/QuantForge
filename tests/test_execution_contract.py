import unittest
from types import MappingProxyType
from dataclasses import FrozenInstanceError
from datetime import datetime

from boe.execution import (
    ExecutionEngineContract,
    ExecutionConfig,
    ExecutionError,
    InvalidPositionSpecification,
    ExecutionConfigurationError,
    UnsupportedExecutionEngine,
    ExecutionContractViolation
)
from boe.risk.specification import PositionSpecification

class DummyExecutionEngine(ExecutionEngineContract):
    def __init__(self, config: ExecutionConfig):
        self._config = config
        
    @property
    def config(self) -> ExecutionConfig:
        return self._config
        
    def execute(self, specification: PositionSpecification):
        if not isinstance(specification, PositionSpecification):
            raise ExecutionContractViolation("Input must be a PositionSpecification.")
        return "DummyResult"

class TestExecutionContract(unittest.TestCase):

    def setUp(self):
        self.dt = datetime(2026, 1, 1, 12, 0, 0)
        self.metadata = MappingProxyType({"env": "test"})
        self.config = ExecutionConfig(
            engine_name="TestEngine",
            metadata=self.metadata
        )
        
        self.spec = PositionSpecification(
            candidate_id="c_1",
            timeline_id="t_1",
            observation_id="o_1",
            schema_version="1.0",
            position_size_multiplier=1.0,
            exposure_fraction=0.01,
            risk_units=1.0,
            metadata=self.metadata,
            timestamp=self.dt
        )
        
        self.engine = DummyExecutionEngine(self.config)

    def test_contract_compliance(self):
        self.assertEqual(self.engine.config.engine_name, "TestEngine")
        result = self.engine.execute(self.spec)
        self.assertEqual(result, "DummyResult")
        
    def test_configuration_immutability(self):
        with self.assertRaises(FrozenInstanceError):
            self.config.engine_name = "HackedEngine" # type: ignore

    def test_deterministic_construction_and_hashing(self):
        config2 = ExecutionConfig(
            engine_name="TestEngine",
            metadata=self.metadata
        )
        
        self.assertEqual(self.config, config2)
        self.assertEqual(hash(self.config), hash(config2))

    def test_contract_violation_rejection(self):
        with self.assertRaises(ExecutionContractViolation):
            self.engine.execute("NOT_A_SPEC") # type: ignore

    def test_error_hierarchy(self):
        # Verify all execution errors subclass ExecutionError
        self.assertTrue(issubclass(InvalidPositionSpecification, ExecutionError))
        self.assertTrue(issubclass(ExecutionConfigurationError, ExecutionError))
        self.assertTrue(issubclass(UnsupportedExecutionEngine, ExecutionError))
        self.assertTrue(issubclass(ExecutionContractViolation, ExecutionError))

if __name__ == '__main__':
    unittest.main()
