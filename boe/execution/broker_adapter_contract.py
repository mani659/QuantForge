from abc import ABC, abstractmethod
from dataclasses import dataclass
from types import MappingProxyType
from typing import Any

from boe.risk.specification import PositionSpecification

@dataclass(frozen=True)
class BrokerAdapterConfig:
    """
    Immutable configuration for a BrokerAdapter.
    """
    broker_name: str
    metadata: MappingProxyType[str, Any]
    
    def __hash__(self):
        return hash((
            self.broker_name,
            frozenset(self.metadata.items())
        ))

class BrokerAdapterContract(ABC):
    """
    The boundary contract defining how execution engines dispatch to broker-specific adapters.
    Implementations must be broker-specific but consume and produce generic interfaces.
    """
    
    @property
    @abstractmethod
    def config(self) -> BrokerAdapterConfig:
        """Return the immutable configuration for this adapter."""
        pass

    @abstractmethod
    def dispatch(self, specification: PositionSpecification) -> Any:
        """
        Dispatch the generic PositionSpecification to the broker.
        Returns a Future ExecutionResult (represented as Any for now).
        """
        pass
