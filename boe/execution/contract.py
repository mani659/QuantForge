from abc import ABC, abstractmethod
from dataclasses import dataclass
from types import MappingProxyType
from typing import Any

from boe.risk.specification import PositionSpecification

@dataclass(frozen=True)
class ExecutionConfig:
    """
    Immutable configuration for an ExecutionEngine.
    """
    engine_name: str
    metadata: MappingProxyType[str, Any]

    def __hash__(self):
        return hash((
            self.engine_name,
            frozenset(self.metadata.items())
        ))

class ExecutionEngineContract(ABC):
    """
    The boundary contract defining how execution engines process PositionSpecifications.
    Implementations must be broker-specific but consume this generic interface.
    """
    
    @property
    @abstractmethod
    def config(self) -> ExecutionConfig:
        """Return the immutable configuration for this engine."""
        pass

    @abstractmethod
    def execute(self, specification: PositionSpecification) -> Any:
        """
        Execute the broker-independent PositionSpecification.
        Returns a Future ExecutionResult (represented as Any for now).
        """
        pass
