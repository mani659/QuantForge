"""
Market Data Adapter Module
Translates external market data into immutable EnvironmentSnapshots.
"""

from abc import ABC, abstractmethod
from typing import Mapping, Any
from datetime import datetime

from boe.temporal.environment_snapshot import EnvironmentSnapshot
from boe.temporal.timeline_errors import TimelineError


class MarketDataAdapterError(Exception):
    """Base exception for market adapter validation failures."""
    pass


class MarketDataAdapterContract(ABC):
    """
    Abstract contract for translating raw broker market data into immutable
    EnvironmentSnapshots.
    """

    @abstractmethod
    def translate(self, raw_data: Mapping[str, Any]) -> EnvironmentSnapshot:
        """
        Translate external market data into a deterministic, immutable EnvironmentSnapshot.
        
        Args:
            raw_data: A mapping representing raw tick or bar data from a broker.
            
        Returns:
            EnvironmentSnapshot: A fully populated, immutable snapshot of the market.
            
        Raises:
            MarketDataAdapterError: If the input data is malformed or invalid.
        """
        pass


class GenericMarketDataAdapter(MarketDataAdapterContract):
    """
    A generic market data adapter that translates standard dictionary representations
    of market ticks or bars into EnvironmentSnapshots.
    """

    def __init__(self, schema_version: str = "1.0.0", source: str = "generic_feed") -> None:
        """
        Initialize the adapter with fixed source and schema version properties.
        """
        self.schema_version = schema_version
        self.source = source

    def translate(self, raw_data: Mapping[str, Any]) -> EnvironmentSnapshot:
        """
        Translates raw mapping data into an EnvironmentSnapshot.
        
        Requires the following keys in raw_data:
        - 'id': str
        - 'instrument': str
        - 'timeframe': str
        - 'timestamp': datetime
        
        All other keys (or the 'state' key if provided as a mapping) will be placed
        into the market_state payload.
        """
        if not isinstance(raw_data, Mapping):
            raise MarketDataAdapterError("Raw data must be a Mapping (e.g., dict).")

        snapshot_id = raw_data.get("id")
        instrument = raw_data.get("instrument")
        timeframe = raw_data.get("timeframe")
        timestamp = raw_data.get("timestamp")

        if not isinstance(snapshot_id, str) or not snapshot_id:
            raise MarketDataAdapterError("Invalid or missing 'id'. Must be a non-empty string.")
        
        if not isinstance(instrument, str) or not instrument:
            raise MarketDataAdapterError("Invalid or missing 'instrument'. Must be a non-empty string.")
            
        if not isinstance(timeframe, str) or not timeframe:
            raise MarketDataAdapterError("Invalid or missing 'timeframe'. Must be a non-empty string.")
            
        if not isinstance(timestamp, datetime):
            raise MarketDataAdapterError("Invalid or missing 'timestamp'. Must be a datetime instance.")

        # If there's an explicit 'state' key containing a mapping, use it.
        # Otherwise, bundle the remaining fields into the state.
        market_state = raw_data.get("state")
        if market_state is None:
            market_state = {
                k: v for k, v in raw_data.items()
                if k not in {"id", "instrument", "timeframe", "timestamp"}
            }

        if not isinstance(market_state, Mapping):
            raise MarketDataAdapterError("'state' payload must be a mapping.")

        try:
            return EnvironmentSnapshot(
                schema_version=self.schema_version,
                snapshot_id=snapshot_id,
                instrument=instrument,
                timeframe=timeframe,
                timestamp=timestamp,
                source=self.source,
                market_state=market_state
            )
        except TimelineError as e:
            raise MarketDataAdapterError(f"Validation failed during snapshot construction: {e}") from e
