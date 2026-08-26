import pytest
import pyarrow.parquet as pq
import hashlib
import json
import os
import shutil
import tracemalloc
from pathlib import Path
from research.staged_execution.tick_parquet_converter import TickParquetConverter

@pytest.fixture
def temp_dir(tmp_path):
    fixtures_dir = tmp_path / "fixtures"
    fixtures_dir.mkdir()
    yield fixtures_dir
    if fixtures_dir.exists():
        shutil.rmtree(fixtures_dir)

def create_synthetic_csv(path: Path, rows: list):
    with open(path, 'w') as f:
        for r in rows:
            f.write(','.join(str(x) for x in r) + '\n')

def test_a_b_c_d_e_f_basic_conversion(temp_dir):
    # Tests A, B, C, D, E, F
    csv_path = temp_dir / "synthetic_ticks.csv"
    out_dir = temp_dir / "output"
    
    rows = [
        # date, time, bid, ask, last, vol
        ["20210101", "09:30:00.123", "1.1000000000000001", "1.1005", "1.1002", "10"], # D: rounding edge case
        ["20210101", "09:30:00.123", "1.1002", "1.1006", "", "15"], # B: duplicate timestamp, E: nullable last
        ["20210201", "10:00:00.000", "1.1010", "1.1012", "1.1011", "20"] # F: next month
    ]
    create_synthetic_csv(csv_path, rows)
    
    converter = TickParquetConverter(output_dir=out_dir, market="SYNTHTEST")
    manifest = converter.process_file(csv_path)
    
    assert manifest["row_count"] == 3
    
    # Test F: Partitioning
    part1 = out_dir / "SYNTHTEST" / "202101.parquet"
    part2 = out_dir / "SYNTHTEST" / "202102.parquet"
    assert part1.exists()
    assert part2.exists()
    assert manifest["partitions"] == ["202101.parquet", "202102.parquet"]
    
    # Read Parquet
    table1 = pq.read_table(part1)
    
    # Test C: Row identity
    assert table1.column("source_row_ordinal").to_pylist() == [0, 1]
    
    # Test D: Numeric equivalence & rounding
    bids = table1.column("bid").to_pylist()
    assert bids[0] == float("1.1000000000000001")
    assert bids[1] == float("1.1002")
    
    # Test E: Nullable last
    lasts = table1.column("last").to_pylist()
    assert lasts[0] == float("1.1002")
    assert lasts[1] is None

def test_g_h_canonical_reproducibility(temp_dir):
    # Test G and H
    csv_path = temp_dir / "synthetic_ticks2.csv"
    rows = [
        ["20210101", "09:30:00", "1.0", "2.0", "1.5", "100"]
    ]
    create_synthetic_csv(csv_path, rows)
    
    out_dir1 = temp_dir / "out1"
    converter1 = TickParquetConverter(out_dir1, "MKT", compression="snappy")
    man1 = converter1.process_file(csv_path)
    
    out_dir2 = temp_dir / "out2"
    # Change compression to alter physical bytes
    converter2 = TickParquetConverter(out_dir2, "MKT", compression="none")
    man2 = converter2.process_file(csv_path)
    
    # Canonical hashes MUST match exactly
    assert man1["column_hashes"] == man2["column_hashes"]
    assert man1["row_count"] == man2["row_count"]
    
    # Physical files MUST differ (Test H)
    f1 = out_dir1 / "MKT" / "202101.parquet"
    f2 = out_dir2 / "MKT" / "202101.parquet"
    
    def file_hash(p):
        with open(p, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()
            
    assert file_hash(f1) != file_hash(f2)

def test_i_malformed_input(temp_dir):
    # Test I
    out_dir = temp_dir / "out3"
    converter = TickParquetConverter(out_dir, "MKT")
    
    # Invalid column count
    csv1 = temp_dir / "bad1.csv"
    create_synthetic_csv(csv1, [["20210101", "09:30", "1.0"]])
    with pytest.raises(RuntimeError, match="EXECUTION-INFRASTRUCTURE FAILURE"):
        converter.process_file(csv1)
        
    # Invalid float
    csv2 = temp_dir / "bad2.csv"
    create_synthetic_csv(csv2, [["20210101", "09:30:00", "bad", "2.0", "1.5", "100"]])
    with pytest.raises(RuntimeError, match="EXECUTION-INFRASTRUCTURE FAILURE"):
        converter.process_file(csv2)

    # Non-chronological partition
    csv3 = temp_dir / "bad3.csv"
    create_synthetic_csv(csv3, [
        ["20210201", "09:30:00", "1.0", "2.0", "1.5", "100"],
        ["20210101", "09:30:00", "1.0", "2.0", "1.5", "100"]
    ])
    with pytest.raises(RuntimeError, match="EXECUTION-INFRASTRUCTURE FAILURE: Non-chronological"):
        converter.process_file(csv3)

def test_j_memory_behavior(temp_dir):
    csv_path = temp_dir / "large.csv"
    out_dir = temp_dir / "out_mem"
    
    # Generate 500k rows
    with open(csv_path, 'w') as f:
        for i in range(500000):
            # 20210101,09:30:00,1.0,2.0,1.5,100
            f.write(f"20210101,09:30:00,{1.0 + i*0.0001},2.0,1.5,10\n")
            
    tracemalloc.start()
    converter = TickParquetConverter(out_dir, "MEMTEST", chunk_size=100000)
    converter.process_file(csv_path)
    
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    # 500k rows in memory would be over 50MB. We assert peak memory is under 35MB, proving O(1) chunks.
    assert peak < 35 * 1024 * 1024, f"Peak memory was {peak / 1024 / 1024:.2f} MB, which is too high!"
    
def test_production_firewall(tmp_path):
    prod_path = tmp_path / "data" / "production_ticks.csv"
    prod_path.parent.mkdir()
    prod_path.touch()
    
    converter = TickParquetConverter(tmp_path / "out", "PRODTEST")
    with pytest.raises(RuntimeError, match="EXECUTION-INFRASTRUCTURE FAILURE: Production data access forbidden."):
        converter.process_file(prod_path)

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
