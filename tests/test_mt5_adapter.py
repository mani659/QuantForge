import unittest
from types import MappingProxyType
from datetime import datetime

from boe.execution import (
    MT5Adapter,
    MT5AdapterConfig,
    MT5TransportConfig,
    MT5TransportContract,
    ExecutionResult,
    ExecutionStatus,
    TranslationError,
    UnsupportedOrderType,
    MT5CommunicationError,
    MT5AdapterConfigurationError
)
from boe.risk.specification import PositionSpecification

class MockMT5Transport(MT5TransportContract):
    def __init__(self, failure=False):
        self._config = MT5TransportConfig("mock/path", MappingProxyType({}))
        self.failure = failure
        
    @property
    def config(self) -> MT5TransportConfig:
        return self._config
        
    def initialize(self) -> bool:
        return True
        
    def shutdown(self) -> None:
        pass
        
    def send_request(self, request: dict) -> dict:
        if self.failure:
            raise MT5CommunicationError("Mock transport failure")
            
        return {
            "retcode": 10009,
            "deal": 123,
            "order": 456,
            "volume": request.get("volume"),
            "action": request.get("action"),
            "comment": request.get("comment")
        }

class MockMT5TransportRejection(MockMT5Transport):
    def send_request(self, request: dict) -> dict:
        return {
            "retcode": 10004, # REQUOTE
            "comment": "Requote error"
        }

class TestMT5Adapter(unittest.TestCase):

    def setUp(self):
        self.dt = datetime(2026, 1, 1, 12, 0, 0)
        self.metadata = MappingProxyType({"env": "test"})
        self.config = MT5AdapterConfig(
            broker_name="MockMT5",
            metadata=self.metadata
        )
        self.spec_buy = PositionSpecification(
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
        self.spec_sell = PositionSpecification(
            candidate_id="c_1",
            timeline_id="t_1",
            observation_id="o_1",
            schema_version="1.0",
            position_size_multiplier=1.0,
            exposure_fraction=-0.01,
            risk_units=1.0,
            metadata=self.metadata,
            timestamp=self.dt
        )

    def test_translation_logic_buy(self):
        transport = MockMT5Transport()
        adapter = MT5Adapter(self.config, transport)
        
        result = adapter.dispatch(self.spec_buy)
        
        self.assertIsInstance(result, ExecutionResult)
        self.assertEqual(result.status, ExecutionStatus.SUCCESS)
        self.assertEqual(result.metadata["action"], "BUY")
        self.assertEqual(result.metadata["volume"], 0.01)

    def test_translation_logic_sell(self):
        transport = MockMT5Transport()
        adapter = MT5Adapter(self.config, transport)
        
        result = adapter.dispatch(self.spec_sell)
        
        self.assertEqual(result.status, ExecutionStatus.SUCCESS)
        self.assertEqual(result.metadata["action"], "SELL")
        self.assertEqual(result.metadata["volume"], 0.01)

    def test_translation_logic_zero_exposure(self):
        transport = MockMT5Transport()
        adapter = MT5Adapter(self.config, transport)
        
        spec_zero = PositionSpecification(
            candidate_id="c_1",
            timeline_id="t_1",
            observation_id="o_1",
            schema_version="1.0",
            position_size_multiplier=1.0,
            exposure_fraction=0.0,
            risk_units=1.0,
            metadata=self.metadata,
            timestamp=self.dt
        )
        with self.assertRaises(UnsupportedOrderType):
            adapter.dispatch(spec_zero)

    def test_adapter_failure_propagation(self):
        transport = MockMT5Transport(failure=True)
        adapter = MT5Adapter(self.config, transport)
        
        result = adapter.dispatch(self.spec_buy)
        self.assertEqual(result.status, ExecutionStatus.FAILED)
        self.assertIn("Mock transport failure", result.metadata["error"])

    def test_mt5_rejection_translation(self):
        transport = MockMT5TransportRejection()
        adapter = MT5Adapter(self.config, transport)
        
        result = adapter.dispatch(self.spec_buy)
        self.assertEqual(result.status, ExecutionStatus.FAILED)
        self.assertEqual(result.metadata["retcode"], 10004)

    def test_immutable_inputs(self):
        transport = MockMT5Transport()
        adapter = MT5Adapter(self.config, transport)
        
        with self.assertRaises(TranslationError):
            adapter.dispatch({"invalid": "type"}) # type: ignore

    def test_deterministic_behaviour(self):
        transport = MockMT5Transport()
        adapter1 = MT5Adapter(self.config, transport)
        adapter2 = MT5Adapter(self.config, transport)
        
        res1 = adapter1.dispatch(self.spec_buy)
        res2 = adapter2.dispatch(self.spec_buy)
        
        self.assertEqual(res1, res2)

    def test_configuration_validation(self):
        transport = MockMT5Transport()
        with self.assertRaises(MT5AdapterConfigurationError):
            MT5Adapter("BadConfig", transport) # type: ignore
            
        with self.assertRaises(MT5AdapterConfigurationError):
            MT5Adapter(self.config, "BadTransport") # type: ignore

if __name__ == '__main__':
    unittest.main()
