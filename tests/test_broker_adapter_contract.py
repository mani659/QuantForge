import unittest
from types import MappingProxyType
from dataclasses import FrozenInstanceError
from datetime import datetime

from boe.execution import (
    BrokerAdapterContract,
    BrokerAdapterConfig,
    ExecutionError,
    InvalidBrokerAdapter,
    UnsupportedBroker,
    AdapterConfigurationError,
    BrokerContractViolation
)
from boe.risk.specification import PositionSpecification

class DummyBrokerAdapter(BrokerAdapterContract):
    def __init__(self, config: BrokerAdapterConfig):
        self._config = config
        
    @property
    def config(self) -> BrokerAdapterConfig:
        return self._config
        
    def dispatch(self, specification: PositionSpecification):
        if not isinstance(specification, PositionSpecification):
            raise BrokerContractViolation("Input must be a PositionSpecification.")
        return "DummyAdapterResult"

class TestBrokerAdapterContract(unittest.TestCase):

    def setUp(self):
        self.dt = datetime(2026, 1, 1, 12, 0, 0)
        self.metadata = MappingProxyType({"env": "test"})
        self.config = BrokerAdapterConfig(
            broker_name="TestBroker",
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
        
        self.adapter = DummyBrokerAdapter(self.config)

    def test_contract_compliance(self):
        self.assertEqual(self.adapter.config.broker_name, "TestBroker")
        result = self.adapter.dispatch(self.spec)
        self.assertEqual(result, "DummyAdapterResult")
        
    def test_configuration_immutability(self):
        with self.assertRaises(FrozenInstanceError):
            self.config.broker_name = "HackedBroker" # type: ignore

    def test_deterministic_construction_and_hashing(self):
        config2 = BrokerAdapterConfig(
            broker_name="TestBroker",
            metadata=self.metadata
        )
        
        self.assertEqual(self.config, config2)
        self.assertEqual(hash(self.config), hash(config2))

    def test_contract_violation_rejection(self):
        with self.assertRaises(BrokerContractViolation):
            self.adapter.dispatch("NOT_A_SPEC") # type: ignore

    def test_error_hierarchy(self):
        # Verify all adapter errors subclass ExecutionError
        self.assertTrue(issubclass(InvalidBrokerAdapter, ExecutionError))
        self.assertTrue(issubclass(UnsupportedBroker, ExecutionError))
        self.assertTrue(issubclass(AdapterConfigurationError, ExecutionError))
        self.assertTrue(issubclass(BrokerContractViolation, ExecutionError))

if __name__ == '__main__':
    unittest.main()
