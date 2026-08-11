import os
import csv
import json
import pytest
from datetime import datetime, timezone

from research.dataset.errors import DatasetConfigurationError, DatasetReaderError
from research.dataset.partition import PartitionName, DatasetPartition
from research.dataset.manifest import DatasetManifest
from research.dataset.reader import CSVPartitionReader
from research.dataset.stream import create_snapshot_stream

from boe.deployment.historical_adapter import HistoricalAdapterError
from boe.execution.engine import DefaultExecutionEngine
from boe.execution.contract import ExecutionConfig
from boe.execution.paper_adapter import PaperTradingAdapter, PaperTradingAdapterConfig
from research.engine.stub_strategy import MovingAverageCrossoverStrategy
from research.engine.synchronization import AdapterMarketStateSynchronizer
from research.engine.run_engine import ResearchRunEngine, ResearchExecutionContext
from research.engine.configuration import ExperimentConfiguration
from types import MappingProxyType


@pytest.fixture
def sample_csv_path(tmp_path):
    """Creates a deterministic 10-row fixture CSV."""
    filepath = tmp_path / "xauusd_test.csv"
    
    # 10 rows: 10:00 to 10:09
    rows = []
    for i in range(10):
        rows.append({
            "timestamp": f"2026-01-01T10:0{i}:00",
            "open": 2000.0 + i,
            "high": 2005.0 + i,
            "low": 1995.0 + i,
            "close": 2002.0 + i,
            "volume": 100 + i
        })
        
    # Duplicate timestamp case at 10:10
    rows.append({
        "timestamp": "2026-01-01T10:10:00",
        "open": 2010.0, "high": 2015.0, "low": 2005.0, "close": 2012.0, "volume": 110
    })
    rows.append({
        "timestamp": "2026-01-01T10:10:00", # Duplicate timestamp
        "open": 2010.5, "high": 2015.5, "low": 2005.5, "close": 2012.5, "volume": 111
    })
        
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["timestamp", "open", "high", "low", "close", "volume"])
        writer.writeheader()
        writer.writerows(rows)
        
    return str(filepath)


def test_manifest_validation(sample_csv_path):
    """Test valid and invalid manifest configurations."""
    p_train = DatasetPartition(
        PartitionName.TRAIN,
        datetime(2026, 1, 1, 10, 0, tzinfo=timezone.utc),
        datetime(2026, 1, 1, 10, 5, tzinfo=timezone.utc),
        sample_csv_path
    )
    
    p_val = DatasetPartition(
        PartitionName.VALIDATION,
        datetime(2026, 1, 1, 10, 5, tzinfo=timezone.utc),
        datetime(2026, 1, 1, 10, 8, tzinfo=timezone.utc),
        sample_csv_path
    )
    
    # Valid manifest
    manifest = DatasetManifest(
        "test_ds", "XAUUSD", "M1", "UTC", "1.0.0",
        partitions=[p_train, p_val]
    )
    assert manifest.dataset_id == "test_ds"
    assert manifest.fingerprint.startswith("sha256:")
    
    # Invalid: Overlap
    p_overlap = DatasetPartition(
        PartitionName.TEST,
        datetime(2026, 1, 1, 10, 7, tzinfo=timezone.utc), # Overlaps with p_val
        datetime(2026, 1, 1, 10, 10, tzinfo=timezone.utc),
        sample_csv_path
    )
    
    with pytest.raises(DatasetConfigurationError, match="Overlapping partitions detected"):
        DatasetManifest("test_ds", "XAUUSD", "M1", "UTC", "1.0.0", [p_val, p_overlap])
        
    # Invalid: Not chronological
    with pytest.raises(DatasetConfigurationError, match="strict chronological order"):
        DatasetManifest("test_ds", "XAUUSD", "M1", "UTC", "1.0.0", [p_val, p_train])
        
    # Invalid: Duplicate partition name
    p_train_2 = DatasetPartition(
        PartitionName.TRAIN,
        datetime(2026, 1, 1, 10, 10, tzinfo=timezone.utc),
        datetime(2026, 1, 1, 10, 15, tzinfo=timezone.utc),
        sample_csv_path
    )
    with pytest.raises(DatasetConfigurationError, match="Duplicate partition name"):
        DatasetManifest("test_ds", "XAUUSD", "M1", "UTC", "1.0.0", [p_train, p_train_2])


def test_scientific_isolation(sample_csv_path):
    """Test that readers only emit rows within their explicit boundaries."""
    # TRAIN: [10:00, 10:03) -> 10:00, 10:01, 10:02 (3 rows)
    p_train = DatasetPartition(
        PartitionName.TRAIN,
        datetime(2026, 1, 1, 10, 0, tzinfo=timezone.utc),
        datetime(2026, 1, 1, 10, 3, tzinfo=timezone.utc),
        sample_csv_path
    )
    # VALIDATION: [10:03, 10:06) -> 10:03, 10:04, 10:05 (3 rows)
    p_val = DatasetPartition(
        PartitionName.VALIDATION,
        datetime(2026, 1, 1, 10, 3, tzinfo=timezone.utc),
        datetime(2026, 1, 1, 10, 6, tzinfo=timezone.utc),
        sample_csv_path
    )
    
    reader_train = CSVPartitionReader(p_train, "UTC")
    train_rows = list(reader_train.read())
    assert len(train_rows) == 3
    assert train_rows[0]["timestamp"].minute == 0
    assert train_rows[1]["timestamp"].minute == 1
    assert train_rows[2]["timestamp"].minute == 2
    
    reader_val = CSVPartitionReader(p_val, "UTC")
    val_rows = list(reader_val.read())
    assert len(val_rows) == 3
    assert val_rows[0]["timestamp"].minute == 3
    assert val_rows[2]["timestamp"].minute == 5


def test_duplicate_timestamps_accepted(sample_csv_path):
    """Duplicate timestamps should be yielded if they are within bounds."""
    p_test = DatasetPartition(
        PartitionName.TEST,
        datetime(2026, 1, 1, 10, 9, tzinfo=timezone.utc),
        datetime(2026, 1, 1, 10, 11, tzinfo=timezone.utc),
        sample_csv_path
    )
    reader = CSVPartitionReader(p_test, "UTC")
    rows = list(reader.read())
    # Should get 10:09, 10:10 (dup 1), 10:10 (dup 2)
    assert len(rows) == 3
    assert rows[1]["timestamp"] == rows[2]["timestamp"]
    assert rows[1]["close"] == 2012.0
    assert rows[2]["close"] == 2012.5


def test_malformed_data(tmp_path):
    """Test reading from a malformed CSV fails fast."""
    filepath = tmp_path / "bad.csv"
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["timestamp", "open", "high", "low", "close", "volume"])
        writer.writeheader()
        writer.writerow({"timestamp": "2026-01-01T10:00:00", "open": "invalid", "high": 2005.0, "low": 1995.0, "close": 2002.0, "volume": 100})
        
    p = DatasetPartition(
        PartitionName.TRAIN,
        datetime(2026, 1, 1, 10, 0, tzinfo=timezone.utc),
        datetime(2026, 1, 1, 10, 5, tzinfo=timezone.utc),
        str(filepath)
    )
    
    reader = CSVPartitionReader(p, "UTC")
    with pytest.raises(DatasetReaderError, match="Invalid numeric value"):
        list(reader.read())


def test_dataset_fingerprint_reproducibility(sample_csv_path):
    p = DatasetPartition(
        PartitionName.TRAIN,
        datetime(2026, 1, 1, 10, 0, tzinfo=timezone.utc),
        datetime(2026, 1, 1, 10, 5, tzinfo=timezone.utc),
        sample_csv_path
    )
    manifest1 = DatasetManifest("ds1", "XAUUSD", "M1", "UTC", "1.0.0", [p])
    manifest2 = DatasetManifest("ds1", "XAUUSD", "M1", "UTC", "1.0.0", [p])
    
    assert manifest1.fingerprint == manifest2.fingerprint
    
    # Change partition boundary
    p_mod = DatasetPartition(
        PartitionName.TRAIN,
        datetime(2026, 1, 1, 10, 0, tzinfo=timezone.utc),
        datetime(2026, 1, 1, 10, 6, tzinfo=timezone.utc),
        sample_csv_path
    )
    manifest3 = DatasetManifest("ds1", "XAUUSD", "M1", "UTC", "1.0.0", [p_mod])
    assert manifest1.fingerprint != manifest3.fingerprint


def test_end_to_end_research_integration(sample_csv_path):
    """
    Test the full pipeline:
    Manifest -> Stream -> ResearchRunEngine
    """
    # 1. Manifest
    p_train = DatasetPartition(
        PartitionName.TRAIN,
        datetime(2026, 1, 1, 10, 0, tzinfo=timezone.utc),
        datetime(2026, 1, 1, 10, 11, tzinfo=timezone.utc), # Covers all 12 rows
        sample_csv_path
    )
    manifest = DatasetManifest(
        dataset_id="test_ds",
        instrument="XAUUSD",
        timeframe="M1",
        timezone="UTC",
        schema_version="1.0.0",
        partitions=[p_train]
    )
    
    # 2. Config
    config = ExperimentConfiguration(
        dataset_id=manifest.dataset_id,
        dataset_partition="TRAIN",
        instrument=manifest.instrument,
        timeframe=manifest.timeframe,
        date_range_start=p_train.start_timestamp,
        date_range_end=p_train.end_timestamp,
        strategy_id="ma_crossover_stub",
        strategy_version="1.0.0",
        strategy_parameters={"short_window": 2, "long_window": 4}
    )
    
    # 3. Stream
    snapshot_stream = create_snapshot_stream(manifest, PartitionName.TRAIN)
    
    # 4. Engine context
    paper_config = PaperTradingAdapterConfig(broker_name="paper", metadata=MappingProxyType({}))
    paper_adapter = PaperTradingAdapter(config=paper_config)
    exec_engine = DefaultExecutionEngine(
        config=ExecutionConfig(engine_name="default", metadata=MappingProxyType({})),
        adapter=paper_adapter
    )
    context = ResearchExecutionContext(
        execution_engine=exec_engine,
        market_state_synchronizer=AdapterMarketStateSynchronizer(paper_adapter)
    )
    strategy = MovingAverageCrossoverStrategy()
    run_engine = ResearchRunEngine(
        strategy=strategy,
        execution_context=context,
        config=config
    )
    
    # 5. Execute
    results = run_engine.run(snapshot_stream)
    
    # All 12 rows should be processed successfully
    assert len(results) == 12
    assert all(r.processed for r in results)
    
    # Verify snapshot_id correctness (generated by HistoricalMarketAdapter)
    assert all(r.snapshot_id.startswith("test_ds:") for r in results)
