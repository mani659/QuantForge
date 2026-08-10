"""
Historical Market Data Adapter Module
Translates external historical market data into immutable EnvironmentSnapshots
while guaranteeing strict temporal ordering and preventing look-ahead.

Snapshot identity is a dataset-relative record identity derived from a
deterministic SHA-256 hash of the canonical record content:

    snapshot_id = f"{dataset_id}:{sha256(canonical(record))[:16]}"

The identity is reproducible outside the original process, is independent of
how the dataset is ordered, and identical records within the same dataset
intentionally share the same identifier.
"""

import hashlib
import json
from typing import Mapping, Any, Optional
from datetime import datetime, timezone

from boe.temporal.environment_snapshot import EnvironmentSnapshot
from boe.temporal.timeline_errors import TimelineError
from boe.deployment.market_adapter import MarketDataAdapterContract, MarketDataAdapterError


class HistoricalAdapterError(MarketDataAdapterError):
    """Exception for historical market adapter validation failures."""
    pass


def _canonicalize(value: Any) -> Any:
    """
    Convert a raw value into a deterministic, JSON-serializable canonical form
    that feeds the snapshot content hash.

    Rules:
    - Mapping keys are sorted deterministically (recursively).
    - Timestamps use their ISO-8601 UTC representation.
    - Floats use Python's shortest deterministic round-trip representation,
      produced by the JSON encoder for the canonical input.
    - No Python hash(), UUID, runtime clock, process, or sequence values.
    """
    if isinstance(value, datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc).isoformat()
    if isinstance(value, Mapping):
        return {
            str(key): _canonicalize(item)
            for key, item in sorted(value.items(), key=lambda pair: str(pair[0]))
        }
    if isinstance(value, (list, tuple)):
        return [_canonicalize(item) for item in value]
    if value is None or isinstance(value, bool):
        return value
    if isinstance(value, (str, int, float)):
        return value
    raise HistoricalAdapterError(
        "Cannot canonicalize value of type "
        f"{type(value).__name__} for deterministic snapshot identity."
    )


def _canonical_json(raw_data: Mapping[str, Any]) -> str:
    """Produce deterministic canonical bytes for a raw record."""
    return json.dumps(
        _canonicalize(raw_data),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    )


class HistoricalMarketAdapter(MarketDataAdapterContract):
    """
    Translates historical market data records into EnvironmentSnapshots.

    Snapshot identity:
    - snapshot_id is a dataset-relative record identity.
    - identity is derived from deterministic canonical record content.
    - identity is not wall-clock identity.
    - identity is not runtime sequence identity.
    - identity is reproducible outside the original process.
    - identical records within the same dataset intentionally share an ID.

    Temporal ordering:
    - equal timestamps are allowed.
    - increasing timestamps are allowed.
    - timestamp regression raises HistoricalAdapterError (fail fast).
    - ordering is evaluated against the timestamp of the last successfully
      translated record; a failed record never mutates adapter state.
    """

    def __init__(
        self,
        dataset_id: str,
        instrument: str,
        timeframe: str,
        schema_version: str = "1.0.0",
        source: str = "historical_feed"
    ) -> None:
        """
        Initialize the adapter with fixed properties and an empty temporal state.

        Args:
            dataset_id: Research dataset identity used to scope snapshot identity.
            instrument: The instrument identifier (e.g., 'EURUSD').
            timeframe: The timeframe identifier (e.g., 'M1').
            schema_version: The snapshot schema version.
            source: The provenance identifier for the historical data.
        """
        self.dataset_id = dataset_id
        self.instrument = instrument
        self.timeframe = timeframe
        self.schema_version = schema_version
        self.source = source
        self._last_timestamp: Optional[datetime] = None

    def _generate_snapshot_id(self, raw_data: Mapping[str, Any]) -> str:
        """Deterministic dataset-relative content identity for a raw record."""
        digest = hashlib.sha256(_canonical_json(raw_data).encode("utf-8")).hexdigest()
        return f"{self.dataset_id}:{digest[:16]}"

    def translate(self, raw_data: Mapping[str, Any]) -> EnvironmentSnapshot:
        """
        Translate one raw mapping record into an immutable EnvironmentSnapshot.

        Raises:
            HistoricalAdapterError: If input is not a mapping, the timestamp is
                missing, invalid, timezone-naive, or regresses against the last
                successfully translated timestamp, or the state payload is not
                a mapping.
        """
        if not isinstance(raw_data, Mapping):
            raise HistoricalAdapterError("Raw data must be a Mapping (e.g., dict).")

        timestamp = raw_data.get("timestamp")
        if not isinstance(timestamp, datetime):
            raise HistoricalAdapterError(
                "Invalid or missing 'timestamp'. Must be a datetime instance."
            )

        if timestamp.tzinfo is None:
            raise HistoricalAdapterError(
                "Timezone-naive timestamps are not permitted."
            )

        if self._last_timestamp is not None and timestamp < self._last_timestamp:
            raise HistoricalAdapterError(
                f"Timestamp regression detected: {timestamp} is earlier than "
                f"previous {self._last_timestamp}"
            )

        market_state = raw_data.get("state")
        if market_state is None:
            market_state = {
                k: v for k, v in raw_data.items()
                if k not in {"timestamp"}
            }

        if not isinstance(market_state, Mapping):
            raise HistoricalAdapterError("'state' payload must be a mapping.")

        snapshot_id = self._generate_snapshot_id(raw_data)

        try:
            snapshot = EnvironmentSnapshot(
                schema_version=self.schema_version,
                snapshot_id=snapshot_id,
                instrument=self.instrument,
                timeframe=self.timeframe,
                timestamp=timestamp,
                source=self.source,
                market_state=market_state
            )
        except TimelineError as e:
            raise HistoricalAdapterError(
                f"Validation failed during snapshot construction: {e}"
            ) from e

        self._last_timestamp = timestamp
        return snapshot