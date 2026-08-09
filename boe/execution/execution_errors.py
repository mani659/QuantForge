class ExecutionError(Exception):
    """Base exception for all Execution layer errors."""
    pass

class InvalidPositionSpecification(ExecutionError):
    pass

class ExecutionConfigurationError(ExecutionError):
    pass

class UnsupportedExecutionEngine(ExecutionError):
    pass

class ExecutionEngineNotFound(ExecutionError):
    pass

class DuplicateExecutionEngine(ExecutionError):
    pass

class ExecutionContractViolation(ExecutionError):
    pass

class InvalidBrokerAdapter(ExecutionError):
    pass

class UnsupportedBroker(ExecutionError):
    pass

class AdapterConfigurationError(ExecutionError):
    pass

class BrokerContractViolation(ExecutionError):
    pass

class InvalidExecutionResult(ExecutionError):
    pass

class InvalidExecutionStatus(ExecutionError):
    pass

class ExecutionResultValidationError(ExecutionError):
    pass

class ExecutionFailure(ExecutionError):
    pass

class AdapterUnavailable(ExecutionError):
    pass

class InvalidExecutionRequest(ExecutionError):
    pass

class ExecutionEngineConfigurationError(ExecutionError):
    pass

class MT5TransportError(ExecutionError):
    pass

class MT5ConnectionError(MT5TransportError):
    pass

class MT5InitializationError(MT5TransportError):
    pass

class MT5CommunicationError(MT5TransportError):
    pass

class MT5AdapterError(ExecutionError):
    pass

class InvalidMT5Adapter(MT5AdapterError):
    pass

class UnsupportedOrderType(MT5AdapterError):
    pass

class TranslationError(MT5AdapterError):
    pass

class MT5AdapterConfigurationError(MT5AdapterError):
    pass

class SimulationExecutionError(ExecutionError):
    pass

class UnsupportedSimulationRequest(SimulationExecutionError):
    pass

class SimulationConfigurationError(SimulationExecutionError):
    pass

class PaperTradingError(ExecutionError):
    pass

class PaperAccountError(PaperTradingError):
    pass

class InvalidPaperExecution(PaperTradingError):
    pass

class PaperConfigurationError(PaperTradingError):
    pass
