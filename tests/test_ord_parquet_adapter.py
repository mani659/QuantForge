import pytest
from pathlib import Path
import os
import sys
import tempfile
import pyarrow.parquet as pq
import pyarrow as pa
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from research.staged_execution.stage1 import CsvTickSource, ParquetTickSource, _StreamTracker

@pytest.fixture
def dummy_data(tmp_path):
    # Create CSV
    csv_path = tmp_path / "dummy.csv"
    with open(csv_path, "w") as f:
        f.write("20210701,00:00:00,10.0,10.1\n")
        f.write("20210701,00:00:01,10.1,10.2\n")
        f.write("20210701,00:00:01,10.2,10.3\n") # duplicate time
        f.write("20210701,00:00:02,10.3,10.4\n")
        f.write("20210801,00:00:00,11.0,11.1\n") # partition boundary
        
    # Create Parquet
    pq_dir = tmp_path / "parquet_dir"
    pq_dir.mkdir()
    
    schema = pa.schema([
        ("source_row_ordinal", pa.int64()),
        ("date", pa.string()),
        ("time", pa.string()),
        ("bid", pa.float64()),
        ("ask", pa.float64()),
        ("last", pa.float64()),
        ("vol", pa.float64())
    ])
    
    # Partition 1: 202107
    p1 = {
        "source_row_ordinal": [0, 1, 2, 3],
        "date": ["20210701", "20210701", "20210701", "20210701"],
        "time": ["00:00:00", "00:00:01", "00:00:01", "00:00:02"],
        "bid": [10.0, 10.1, 10.2, 10.3],
        "ask": [10.1, 10.2, 10.3, 10.4],
        "last": [None, None, None, None],
        "vol": [1.0, 1.0, 1.0, 1.0]
    }
    pq.write_table(pa.Table.from_pydict(p1, schema=schema), pq_dir / "202107.parquet")

    # Partition 2: 202108
    p2 = {
        "source_row_ordinal": [4],
        "date": ["20210801"],
        "time": ["00:00:00"],
        "bid": [11.0],
        "ask": [11.1],
        "last": [None],
        "vol": [1.0]
    }
    pq.write_table(pa.Table.from_pydict(p2, schema=schema), pq_dir / "202108.parquet")
    
    return csv_path, pq_dir

def test_stage1_adapter_equivalence(dummy_data):
    csv_path, pq_dir = dummy_data
    
    csv_source = CsvTickSource(csv_path)
    csv_ticks = list(csv_source.iter_ticks())
    
    pq_source = ParquetTickSource(pq_dir)
    pq_ticks = list(pq_source.iter_ticks())
    
    # Test A: CSV and Parquet normalized tick streams identical.
    # Test B: Duplicate timestamps identical.
    # Test C: Source ordinals identical (implied by ordering and count).
    # Test D: Float64 values identical.
    # Test F: Partition boundary transition produces no missing/duplicate rows.
    
    assert len(csv_ticks) == len(pq_ticks)
    assert len(csv_ticks) == 5
    
    for i in range(len(csv_ticks)):
        c_valid, c_tick = csv_ticks[i]
        p_valid, p_tick = pq_ticks[i]
        
        assert c_valid == p_valid == True
        assert c_tick == p_tick
