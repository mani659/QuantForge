
from boe.execution.contract import ExecutionEngineContract, ExecutionConfig
from boe.execution.execution_errors import (
    ExecutionError,
    InvalidPositionSpecification,
    ExecutionConfigurationError,
    UnsupportedExecutionEngine,
    ExecutionContractViolation
)

__all__ = [
    'ExecutionEngineContract',
    'ExecutionConfig',
    'ExecutionError',
    'InvalidPositionSpecification',
    'ExecutionConfigurationError',
    'UnsupportedExecutionEngine',
    'ExecutionContractViolation'
]

from boe.execution.broker_adapter_contract import BrokerAdapterContract, BrokerAdapterConfig
from boe.execution.execution_errors import (
    InvalidBrokerAdapter,
    UnsupportedBroker,
    AdapterConfigurationError,
    BrokerContractViolation
)

__all__.extend([
    'BrokerAdapterContract',
    'BrokerAdapterConfig',
    'InvalidBrokerAdapter',
    'UnsupportedBroker',
    'AdapterConfigurationError',
    'BrokerContractViolation'
])

from boe.execution.result import ExecutionResult, ExecutionStatus
from boe.execution.execution_errors import (
    InvalidExecutionResult,
    InvalidExecutionStatus,
    ExecutionResultValidationError
)

__all__.extend([
    'ExecutionResult',
    'ExecutionStatus',
    'InvalidExecutionResult',
    'InvalidExecutionStatus',
    'ExecutionResultValidationError'
])

from boe.execution.engine import DefaultExecutionEngine
from boe.execution.execution_errors import (
    ExecutionFailure,
    AdapterUnavailable,
    InvalidExecutionRequest,
    ExecutionEngineConfigurationError
)

__all__.extend([
    'DefaultExecutionEngine',
    'ExecutionFailure',
    'AdapterUnavailable',
    'InvalidExecutionRequest',
    'ExecutionEngineConfigurationError'
])

from boe.execution.mt5_transport import MT5TransportContract, DefaultMT5Transport, MT5TransportConfig
from boe.execution.execution_errors import (
    MT5TransportError,
    MT5ConnectionError,
    MT5InitializationError,
    MT5CommunicationError
)

__all__.extend([
    'MT5TransportContract',
    'DefaultMT5Transport',
    'MT5TransportConfig',
    'MT5TransportError',
    'MT5ConnectionError',
    'MT5InitializationError',
    'MT5CommunicationError'
])

from boe.execution.mt5_adapter import MT5Adapter, MT5AdapterConfig
from boe.execution.execution_errors import (
    MT5AdapterError,
    InvalidMT5Adapter,
    UnsupportedOrderType,
    TranslationError,
    MT5AdapterConfigurationError
)

__all__.extend([
    'MT5Adapter',
    'MT5AdapterConfig',
    'MT5AdapterError',
    'InvalidMT5Adapter',
    'UnsupportedOrderType',
    'TranslationError',
    'MT5AdapterConfigurationError'
])

from boe.execution.simulation_adapter import PythonSimulationAdapter, PythonSimulationAdapterConfig
from boe.execution.execution_errors import (
    SimulationExecutionError,
    UnsupportedSimulationRequest,
    SimulationConfigurationError
)

__all__.extend([
    'PythonSimulationAdapter',
    'PythonSimulationAdapterConfig',
    'SimulationExecutionError',
    'UnsupportedSimulationRequest',
    'SimulationConfigurationError'
])

from boe.execution.paper_adapter import PaperTradingAdapter, PaperTradingAdapterConfig, PaperTradingAccount
from boe.execution.execution_errors import (
    PaperTradingError,
    PaperAccountError,
    InvalidPaperExecution,
    PaperConfigurationError
)

__all__.extend([
    'PaperTradingAdapter',
    'PaperTradingAdapterConfig',
    'PaperTradingAccount',
    'PaperTradingError',
    'PaperAccountError',
    'InvalidPaperExecution',
    'PaperConfigurationError'
])
