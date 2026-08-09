import unittest
from types import MappingProxyType
from datetime import datetime

from boe.execution import (
    PythonSimulationAdapter,
    PythonSimulationAdapterConfig,
    ExecutionResult,
    ExecutionStatus,
    SimulationExecutionError,
    UnsupportedSimulationRequest,
    SimulationConfigurationError
)
from boe.risk.specification import PositionSpecification

class TestSimulationAdapter(unittest.TestCase):

    def setUp(self):
        self.dt = datetime(2026, 1, 1, 12, 0, 0)
        self.metadata = MappingProxyType({"env": "test"})
        self.config = PythonSimulationAdapterConfig(
            broker_name="MockSim",
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
            candidate_id="c_2",
            timeline_id="t_1",
            observation_id="o_1",
            schema_version="1.0",
            position_size_multiplier=1.0,
            exposure_fraction=-0.01,
            risk_units=1.0,
            metadata=self.metadata,
            timestamp=self.dt
        )

    def test_successful_simulated_execution(self):
        adapter = PythonSimulationAdapter(self.config)
        
        result = adapter.dispatch(self.spec_buy)
        
        self.assertIsInstance(result, ExecutionResult)
        self.assertEqual(result.status, ExecutionStatus.SUCCESS)
        self.assertEqual(result.metadata["action"], "BUY")
        self.assertEqual(result.metadata["volume"], 0.01)
        self.assertEqual(result.metadata["simulated_fill_price"], 1.0)
        
    def test_successful_simulated_execution_sell(self):
        adapter = PythonSimulationAdapter(self.config)
        
        result = adapter.dispatch(self.spec_sell)
        self.assertEqual(result.metadata["action"], "SELL")

    def test_invalid_requests(self):
        adapter = PythonSimulationAdapter(self.config)
        
        with self.assertRaises(SimulationExecutionError):
            adapter.dispatch({"invalid": "request"}) # type: ignore
            
        spec_zero = PositionSpecification(
            candidate_id="c_3",
            timeline_id="t_1",
            observation_id="o_1",
            schema_version="1.0",
            position_size_multiplier=1.0,
            exposure_fraction=0.0,
            risk_units=1.0,
            metadata=self.metadata,
            timestamp=self.dt
        )
        with self.assertRaises(UnsupportedSimulationRequest):
            adapter.dispatch(spec_zero)

    def test_immutable_outputs_and_repeatability(self):
        adapter = PythonSimulationAdapter(self.config)
        
        result1 = adapter.dispatch(self.spec_buy)
        result2 = adapter.dispatch(self.spec_buy)
        
        self.assertEqual(result1, result2)
        self.assertEqual(hash(result1), hash(result2))

    def test_configuration_validation(self):
        with self.assertRaises(SimulationConfigurationError):
            PythonSimulationAdapter("BadConfig") # type: ignore

if __name__ == '__main__':
    unittest.main()
