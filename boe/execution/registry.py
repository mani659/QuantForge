from typing import Tuple, Dict

from boe.execution.contract import ExecutionEngineContract
from boe.execution.execution_errors import (
    ExecutionEngineNotFound,
    DuplicateExecutionEngine,
    ExecutionEngineConfigurationError
)

class ExecutionRegistry:
    """
    Registry for managing Execution Engines.
    It selects execution engines (e.g. paper vs MT5) but DOES NOT execute trades.
    Follows Open/Closed Principle by allowing registration of new engines without modifying this class.
    Must be instantiated; no singleton/global mutable state.
    """
    
    def __init__(self, initial_engines: Tuple[ExecutionEngineContract, ...] = ()):
        self._engines: Dict[str, ExecutionEngineContract] = {}
        for engine in initial_engines:
            self.register(engine)
            
    def register(self, engine: ExecutionEngineContract) -> None:
        if not isinstance(engine, ExecutionEngineContract):
            raise ExecutionEngineConfigurationError("Engine must implement ExecutionEngineContract.")
            
        engine_name = engine.config.engine_name
        if not engine_name:
            raise ExecutionEngineConfigurationError("Engine config must provide a non-empty engine_name.")
            
        if engine_name in self._engines:
            raise DuplicateExecutionEngine(f"Engine '{engine_name}' is already registered.")
            
        self._engines[engine_name] = engine

    def get_engine(self, engine_name: str) -> ExecutionEngineContract:
        if not engine_name:
            raise ExecutionEngineNotFound("Engine name cannot be empty.")
            
        engine = self._engines.get(engine_name)
        if not engine:
            raise ExecutionEngineNotFound(f"Engine '{engine_name}' not found in registry.")
            
        return engine

    def has_engine(self, engine_name: str) -> bool:
        return engine_name in self._engines

    @property
    def registered_engines(self) -> Tuple[str, ...]:
        """Returns a deterministic, sorted tuple of registered engine names."""
        return tuple(sorted(self._engines.keys()))
