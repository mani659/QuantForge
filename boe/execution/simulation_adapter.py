from dataclasses import dataclass
from types import MappingProxyType

from boe.execution.broker_adapter_contract import BrokerAdapterContract, BrokerAdapterConfig
from boe.execution.result import ExecutionResult, ExecutionStatus
from boe.risk.specification import PositionSpecification
from boe.execution.execution_errors import (
    SimulationExecutionError,
    SimulationConfigurationError,
    UnsupportedSimulationRequest
)

@dataclass(frozen=True)
class PythonSimulationAdapterConfig(BrokerAdapterConfig):
    """Immutable Python Simulation Adapter specific configuration."""
    pass

class PythonSimulationAdapter(BrokerAdapterContract):
    """
    Deterministic execution simulator for research, replay, and optimization.
    Does not communicate with any external broker or network.
    """
    def __init__(self, config: PythonSimulationAdapterConfig):
        if not isinstance(config, PythonSimulationAdapterConfig):
            raise SimulationConfigurationError("config must be a PythonSimulationAdapterConfig")
            
        self._config = config

    @property
    def config(self) -> PythonSimulationAdapterConfig:
        return self._config

    def dispatch(self, specification: PositionSpecification) -> ExecutionResult:
        if not isinstance(specification, PositionSpecification):
            raise SimulationExecutionError("PythonSimulationAdapter can only execute PositionSpecifications")
            
        if specification.exposure_fraction == 0:
            raise UnsupportedSimulationRequest("Exposure fraction of 0 is not supported for simulation")
            
        action = "BUY" if specification.exposure_fraction > 0 else "SELL"
        volume = float(abs(specification.exposure_fraction))
        
        # Deterministic dummy simulation metadata
        metadata = {
            "action": action,
            "volume": volume,
            "simulated_slippage": 0.0,
            "simulated_fill_price": 1.0,
            "simulated_commission": 0.0,
            "ticket": f"sim_{hash(specification.candidate_id) % 4294967295}"
        }
        
        return ExecutionResult(
            candidate_id=specification.candidate_id,
            timeline_id=specification.timeline_id,
            observation_id=specification.observation_id,
            schema_version=specification.schema_version,
            status=ExecutionStatus.SUCCESS,
            metadata=MappingProxyType(metadata),
            timestamp=specification.timestamp
        )
