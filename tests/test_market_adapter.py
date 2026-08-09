"""Tests for the live market adapter."""

from datetime import datetime, timezone
import pytest

from boe.deployment.market_adapter import GenericMarketDataAdapter, MarketDataAdapterError
from boe.temporal.environment_snapshot import EnvironmentSnapshot


@pytest.fixture
def adapter():
    return GenericMarketDataAdapter(schema_version="1.0.0", source="test_broker")


def test_valid_tick_conversion(adapter):
    """Test translating a valid market tick."""
    tick_time = datetime(2026, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
    raw_tick = {
        "id": "tick_001",
        "instrument": "EURUSD",
        "timeframe": "TICK",
        "timestamp": tick_time,
        "bid": 1.1000,
        "ask": 1.1002,
        "volume": 15
    }
    
    snapshot = adapter.translate(raw_tick)
    
    assert isinstance(snapshot, EnvironmentSnapshot)
    assert snapshot.snapshot_id == "tick_001"
    assert snapshot.instrument == "EURUSD"
    assert snapshot.timeframe == "TICK"
    assert snapshot.timestamp == tick_time
    assert snapshot.source == "test_broker"
    assert snapshot.schema_version == "1.0.0"
    
    assert snapshot.market_state["bid"] == 1.1000
    assert snapshot.market_state["ask"] == 1.1002
    assert snapshot.market_state["volume"] == 15
    assert "id" not in snapshot.market_state
    assert "instrument" not in snapshot.market_state


def test_valid_bar_conversion(adapter):
    """Test translating a valid OHLC bar with an explicit state dict."""
    bar_time = datetime(2026, 1, 1, 10, 5, 0, tzinfo=timezone.utc)
    raw_bar = {
        "id": "bar_001",
        "instrument": "XAUUSD",
        "timeframe": "M5",
        "timestamp": bar_time,
        "state": {
            "open": 2000.0,
            "high": 2005.0,
            "low": 1999.0,
            "close": 2003.5,
            "tick_volume": 1500
        }
    }
    
    snapshot = adapter.translate(raw_bar)
    
    assert snapshot.instrument == "XAUUSD"
    assert snapshot.timeframe == "M5"
    assert snapshot.market_state["open"] == 2000.0
    assert snapshot.market_state["close"] == 2003.5


def test_malformed_input_rejection(adapter):
    """Test that invalid or missing fields raise MarketDataAdapterError."""
    # Not a mapping
    with pytest.raises(MarketDataAdapterError, match="must be a Mapping"):
        adapter.translate(["not", "a", "dict"])
        
    base_raw = {
        "id": "1",
        "instrument": "EURUSD",
        "timeframe": "M1",
        "timestamp": datetime(2026, 1, 1, 10, 0, tzinfo=timezone.utc)
    }
    
    # Missing ID
    bad_id = base_raw.copy()
    bad_id["id"] = ""
    with pytest.raises(MarketDataAdapterError, match="Invalid or missing 'id'"):
        adapter.translate(bad_id)
        
    # Missing Instrument
    bad_inst = base_raw.copy()
    del bad_inst["instrument"]
    with pytest.raises(MarketDataAdapterError, match="Invalid or missing 'instrument'"):
        adapter.translate(bad_inst)
        
    # Missing Timestamp
    bad_ts = base_raw.copy()
    bad_ts["timestamp"] = "2026-01-01"
    with pytest.raises(MarketDataAdapterError, match="Must be a datetime instance"):
        adapter.translate(bad_ts)
        
    # Bad explicit state
    bad_state = base_raw.copy()
    bad_state["state"] = "not a dict"
    with pytest.raises(MarketDataAdapterError, match="'state' payload must be a mapping"):
        adapter.translate(bad_state)


def test_deterministic_snapshot_creation(adapter):
    """Test that identical inputs produce identical deterministic snapshots."""
    tick_time = datetime(2026, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
    raw_tick_1 = {
        "id": "tick_1",
        "instrument": "BTCUSD",
        "timeframe": "TICK",
        "timestamp": tick_time,
        "price": 50000.0
    }
    
    raw_tick_2 = {
        "id": "tick_1",
        "instrument": "BTCUSD",
        "timeframe": "TICK",
        "timestamp": tick_time,
        "price": 50000.0
    }
    
    snapshot_1 = adapter.translate(raw_tick_1)
    snapshot_2 = adapter.translate(raw_tick_2)
    
    assert snapshot_1 == snapshot_2


def test_immutable_snapshots(adapter):
    """Test that the resulting snapshot is immutable."""
    raw_tick = {
        "id": "tick_1",
        "instrument": "EURUSD",
        "timeframe": "TICK",
        "timestamp": datetime(2026, 1, 1, 10, 0, tzinfo=timezone.utc),
        "price": 1.1
    }
    
    snapshot = adapter.translate(raw_tick)
    
    # Dataclass frozen check
    with pytest.raises(Exception):
        snapshot.snapshot_id = "tick_2"
        
    # MappingProxyType immutability check
    with pytest.raises(TypeError):
        snapshot.market_state["price"] = 1.2
