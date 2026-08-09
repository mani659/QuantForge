from abc import ABC, abstractmethod
from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Dict, Optional

from boe.execution.execution_errors import (
    MT5TransportError,
    MT5ConnectionError,
    MT5InitializationError,
    MT5CommunicationError
)

@dataclass(frozen=True)
class MT5TransportConfig:
    """
    Immutable configuration for the MT5Transport layer.
    """
    terminal_path: str
    metadata: MappingProxyType[str, Any]
    
    def __hash__(self):
        return hash((
            self.terminal_path,
            frozenset(self.metadata.items())
        ))

class MT5TransportContract(ABC):
    """
    The rigid boundary contract for communicating with the MetaTrader5 Python SDK.
    """
    
    @property
    @abstractmethod
    def config(self) -> MT5TransportConfig:
        """Return the immutable configuration for this transport."""
        pass

    @abstractmethod
    def initialize(self) -> bool:
        """Initialize the MT5 terminal connection."""
        pass
        
    @abstractmethod
    def shutdown(self) -> None:
        """Shutdown the MT5 terminal connection."""
        pass

    @abstractmethod
    def send_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send a transport-neutral DTO to MT5 and retrieve a transport-neutral response.
        Absolutely no SDK objects may cross this boundary.
        """
        pass

class DefaultMT5Transport(MT5TransportContract):
    """
    Concrete wrapper for the MetaTrader5 SDK.
    Isolates all SDK imports and objects.
    """
    
    def __init__(self, config: MT5TransportConfig, mt5_module: Optional[Any] = None):
        if not isinstance(config, MT5TransportConfig):
            raise MT5TransportError("config must be an MT5TransportConfig")
        self._config = config
        self._mt5_module = mt5_module
        self._initialized = False

    @property
    def config(self) -> MT5TransportConfig:
        return self._config

    def _get_mt5_module(self) -> Any:
        if self._mt5_module is not None:
            return self._mt5_module
        try:
            import MetaTrader5 as mt5 # type: ignore
            self._mt5_module = mt5
            return mt5
        except ImportError as e:
            raise MT5InitializationError("MetaTrader5 SDK is not installed.") from e

    def initialize(self) -> bool:
        mt5 = self._get_mt5_module()
        if not mt5.initialize(path=self.config.terminal_path):
            raise MT5InitializationError(f"Failed to initialize MT5 at {self.config.terminal_path}")
            
        terminal_info = mt5.terminal_info()
        if terminal_info is None:
            raise MT5ConnectionError("MT5 terminal is not connected.")
            
        self._initialized = True
        return True

    def shutdown(self) -> None:
        if self._initialized:
            mt5 = self._get_mt5_module()
            mt5.shutdown()
            self._initialized = False

    def send_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        if not self._initialized:
            raise MT5CommunicationError("Transport is not initialized.")
            
        mt5 = self._get_mt5_module()
        
        # Example interaction: sending an order.
        # This converts a primitive dictionary into an MT5 order request and returns a primitive dict.
        result = mt5.order_send(request)
        
        if result is None:
            raise MT5CommunicationError("Order send failed, received None from MT5 SDK.")
            
        # Return a primitive dictionary representation, never the raw SDK object.
        return {
            "retcode": getattr(result, "retcode", None),
            "deal": getattr(result, "deal", None),
            "order": getattr(result, "order", None),
            "volume": getattr(result, "volume", None),
            "price": getattr(result, "price", None),
            "comment": getattr(result, "comment", "")
        }
