from dataclasses import dataclass
from datetime import datetime
from types import MappingProxyType
from typing import Any, Dict

from boe.execution.broker_adapter_contract import BrokerAdapterContract, BrokerAdapterConfig
from boe.execution.mt5_transport import MT5TransportContract
from boe.execution.result import ExecutionResult, ExecutionStatus
from boe.risk.specification import PositionSpecification
from boe.execution.execution_errors import (
    TranslationError,
    MT5AdapterConfigurationError,
    UnsupportedOrderType
)

@dataclass(frozen=True)
class MT5AdapterConfig(BrokerAdapterConfig):
    """Immutable MT5 Adapter specific configuration."""
    pass

class MT5Adapter(BrokerAdapterContract):
    """
    Translates abstract PositionSpecifications into MT5 transport requests.
    Translates transport responses back into abstract ExecutionResults.
    """
    def __init__(self, config: MT5AdapterConfig, transport: MT5TransportContract):
        if not isinstance(config, MT5AdapterConfig):
            raise MT5AdapterConfigurationError("config must be an MT5AdapterConfig")
        if not isinstance(transport, MT5TransportContract):
            raise MT5AdapterConfigurationError("transport must be an MT5TransportContract")
            
        self._config = config
        self._transport = transport

    @property
    def config(self) -> MT5AdapterConfig:
        return self._config

    def dispatch(self, specification: PositionSpecification) -> ExecutionResult:
        if not isinstance(specification, PositionSpecification):
            raise TranslationError("MT5Adapter can only translate PositionSpecifications")
            
        # Translation Step 1: QuantForge concepts -> MT5Transport requests
        # We assume positive exposure fraction means BUY, negative means SELL
        if specification.exposure_fraction == 0:
            raise UnsupportedOrderType("Exposure fraction of 0 is not supported for dispatch")
            
        action = "BUY" if specification.exposure_fraction > 0 else "SELL"
        volume = float(abs(specification.exposure_fraction)) # Use abstract volume for translation
        
        request: Dict[str, Any] = {
            "action": action,
            "volume": volume,
            "magic": hash(specification.candidate_id) % 4294967295,
            "comment": f"{specification.candidate_id}|{specification.timeline_id}"
        }
        
        # Dispatch to Transport
        try:
            transport_response = self._transport.send_request(request)
        except Exception as e:
            # Handle Transport failures (MT5CommunicationError, etc.)
            return ExecutionResult(
                candidate_id=specification.candidate_id,
                timeline_id=specification.timeline_id,
                observation_id=specification.observation_id,
                schema_version=specification.schema_version,
                status=ExecutionStatus.FAILED,
                metadata=MappingProxyType({"error": str(e)}),
                timestamp=specification.timestamp
            )
            
        # Translation Step 2: Transport responses -> ExecutionResult
        retcode = transport_response.get("retcode")
        
        # Define success status based on MT5 retcode (10009 is TRADE_RETCODE_DONE)
        status = ExecutionStatus.SUCCESS if retcode == 10009 else ExecutionStatus.FAILED
        
        return ExecutionResult(
            candidate_id=specification.candidate_id,
            timeline_id=specification.timeline_id,
            observation_id=specification.observation_id,
            schema_version=specification.schema_version,
            status=status,
            metadata=MappingProxyType(transport_response),
            timestamp=specification.timestamp
        )
