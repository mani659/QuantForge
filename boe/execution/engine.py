from boe.execution.contract import ExecutionEngineContract, ExecutionConfig
from boe.execution.broker_adapter_contract import BrokerAdapterContract
from boe.execution.result import ExecutionResult, ExecutionStatus
from boe.execution.execution_errors import (
    ExecutionFailure,
    AdapterUnavailable,
    InvalidExecutionRequest,
    ExecutionEngineConfigurationError,
    ExecutionContractViolation
)
from boe.risk.specification import PositionSpecification

class DefaultExecutionEngine(ExecutionEngineContract):
    """
    Default broker-independent execution engine.
    Orchestrates execution by delegating immutable PositionSpecifications
    to an injected BrokerAdapterContract, and validates the returned ExecutionResult.
    """
    
    def __init__(self, config: ExecutionConfig, adapter: BrokerAdapterContract):
        if not isinstance(config, ExecutionConfig):
            raise ExecutionEngineConfigurationError("config must be an ExecutionConfig")
        if not isinstance(adapter, BrokerAdapterContract):
            raise ExecutionEngineConfigurationError("adapter must be a BrokerAdapterContract")
            
        self._config = config
        self._adapter = adapter
        
    @property
    def config(self) -> ExecutionConfig:
        return self._config

    def execute(self, specification: PositionSpecification) -> ExecutionResult:
        if not isinstance(specification, PositionSpecification):
            raise InvalidExecutionRequest("ExecutionEngine must receive a PositionSpecification")
            
        try:
            result = self._adapter.dispatch(specification)
        except Exception as e:
            raise ExecutionFailure(f"Execution failed during adapter dispatch: {str(e)}") from e
            
        if not isinstance(result, ExecutionResult):
            raise ExecutionContractViolation(
                f"BrokerAdapter must return an ExecutionResult, got {type(result)}"
            )
            
        return result
