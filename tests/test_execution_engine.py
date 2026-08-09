import unittest
from types import MappingProxyType
from datetime import datetime

from boe.execution import (
    DefaultExecutionEngine,
    ExecutionConfig,
    BrokerAdapterContract,
    BrokerAdapterConfig,
    ExecutionResult,
    ExecutionStatus,
    InvalidExecutionRequest,
    ExecutionFailure,
    ExecutionContractViolation,
    ExecutionEngineConfigurationError
)
from boe.risk.specification import PositionSpecification

class MockValidAdapter(BrokerAdapterContract):
    def __init__(self):
        self._config = BrokerAdapterConfig("MockBroker", MappingProxyType({}))
        self.dt = datetime(2026, 1, 1, 12, 0, 0)
        
    @property
    def config(self) -> BrokerAdapterConfig:
        return self._config
        
    def dispatch(self, specification: PositionSpecification):
        return ExecutionResult(
            candidate_id=specification.candidate_id,
            timeline_id=specification.timeline_id,
            observation_id=specification.observation_id,
            schema_version="1.0",
            status=ExecutionStatus.SUCCESS,
            metadata=MappingProxyType({"ticket": "123"}),
            timestamp=self.dt
        )

class MockFailingAdapter(BrokerAdapterContract):
    def __init__(self):
        self._config = BrokerAdapterConfig("MockFailing", MappingProxyType({}))
        
    @property
    def config(self) -> BrokerAdapterConfig:
        return self._config
        
    def dispatch(self, specification: PositionSpecification):
        raise RuntimeError("Broker connection timeout")

class MockViolatingAdapter(BrokerAdapterContract):
    def __init__(self):
        self._config = BrokerAdapterConfig("MockViolating", MappingProxyType({}))
        
    @property
    def config(self) -> BrokerAdapterConfig:
        return self._config
        
    def dispatch(self, specification: PositionSpecification):
        return {"status": "SUCCESS"} # Not an ExecutionResult

class TestExecutionEngine(unittest.TestCase):

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

    def test_successful_delegation_and_immutable_output(self):
        adapter = MockValidAdapter()
        engine = DefaultExecutionEngine(self.config, adapter)
        
        result = engine.execute(self.spec)
        self.assertIsInstance(result, ExecutionResult)
        self.assertEqual(result.status, ExecutionStatus.SUCCESS)
        self.assertEqual(result.metadata["ticket"], "123")
        self.assertEqual(result.candidate_id, "c_1")

    def test_invalid_position_specification(self):
        adapter = MockValidAdapter()
        engine = DefaultExecutionEngine(self.config, adapter)
        
        with self.assertRaises(InvalidExecutionRequest):
            engine.execute({"position": "long"}) # type: ignore

    def test_adapter_failure_error_propagation(self):
        adapter = MockFailingAdapter()
        engine = DefaultExecutionEngine(self.config, adapter)
        
        with self.assertRaisesRegex(ExecutionFailure, "Broker connection timeout"):
            engine.execute(self.spec)

    def test_adapter_contract_violation_rejection(self):
        adapter = MockViolatingAdapter()
        engine = DefaultExecutionEngine(self.config, adapter)
        
        with self.assertRaises(ExecutionContractViolation):
            engine.execute(self.spec)

    def test_configuration_validation(self):
        adapter = MockValidAdapter()
        with self.assertRaises(ExecutionEngineConfigurationError):
            DefaultExecutionEngine("BadConfig", adapter) # type: ignore
            
        with self.assertRaises(ExecutionEngineConfigurationError):
            DefaultExecutionEngine(self.config, "BadAdapter") # type: ignore

if __name__ == '__main__':
    unittest.main()
