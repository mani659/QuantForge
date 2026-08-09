"""
Historical Market Data Adapter Module
Translates external historical market data into immutable EnvironmentSnapshots
while guaranteeing strict temporal ordering and preventing look-ahead.
"""

from typing import Mapping, Any, Optional
from datetime import datetime

from boe.temporal.environment_snapshot import EnvironmentSnapshot
from boe.temporal.timeline_errors import TimelineError
from boe.deployment.market_adapter import MarketDataAdapterContract, MarketDataAdapterError


class HistoricalAdapterError(MarketDataAdapterError):
    """Exception for historical market adapter validation failures."""
    pass


class HistoricalMarketAdapter(MarketDataAdapterContract):
    """
    Translates historical market data records into EnvironmentSnapshots.
    Guarantees strict chronological ordering and prevents future look-ahead.
    
    The adapter may remember the previous timestamp only for ordering validation. 
    It must never expose or derive information from future records.
    """

    def __init__(self, instrument: str, timeframe: str, schema_version: str = "1.0.0", source: str = "historical_feed") -> None:
        """
        Initialize the adapter with fixed properties and an empty temporal state.
        
        Args:
            instrument: The instrument identifier (e.g., 'EURUSD').
            timeframe: The timeframe identifier (e.g., 'M1').
            schema_version: The snapshot schema version.
            source: The provenance identifier for the historical data.
        """
        self.instrument = instrument
        self.timeframe = timeframe
        self.schema_version = schema_version
        self.source = source
        self._last_timestamp: Optional[datetime] = None

    def translate(self, raw_data: Mapping[str, Any]) -> EnvironmentSnapshot:
        """
        Translates raw mapping data into an EnvironmentSnapshot.
        
        Requires the following keys in raw_data:
        - 'timestamp': datetime (timezone-aware)
        
        All other keys (or the 'state' key if provided as a mapping) will be placed
        into the market_state payload.
        
        Raises:
            HistoricalAdapterError: If timestamps move backwards, are naive, missing, or invalid.
        """
        if not isinstance(raw_data, Mapping):
            raise HistoricalAdapterError("Raw data must be a Mapping (e.g., dict).")

        timestamp = raw_data.get("timestamp")
        if not isinstance(timestamp, datetime):
            raise HistoricalAdapterError("Invalid or missing 'timestamp'. Must be a datetime instance.")
            
        if timestamp.tzinfo is None:
            raise HistoricalAdapterError("Timezone-naive timestamps are not permitted.")

        # Temporal ordering validation (no look-ahead, no backward moving time)
        if self._last_timestamp is not None:
            if timestamp < self._last_timestamp:
                raise HistoricalAdapterError(
                    f"Timestamp regression detected: {timestamp} is earlier than previous {self._last_timestamp}"
                )
        self._last_timestamp = timestamp

        # Determine market state
        market_state = raw_data.get("state")
        if market_state is None:
            market_state = {
                k: v for k, v in raw_data.items()
                if k not in {"timestamp"}
            }

        if not isinstance(market_state, Mapping):
            raise HistoricalAdapterError("'state' payload must be a mapping.")
            
        # Generate deterministic snapshot ID
        snapshot_id = f"{self.instrument}_{self.timeframe}_{int(timestamp.timestamp())}"

        try:
            return EnvironmentSnapshot(
                schema_version=self.schema_version,
                snapshot_id=snapshot_id,
                instrument=self.instrument,
                timeframe=self.timeframe,
                timestamp=timestamp,
                source=self.source,
                market_state=market_state
            )
        except TimelineError as e:
            raise HistoricalAdapterError(f"Validation failed during snapshot construction: {e}") from e
