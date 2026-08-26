import gc
import os
import psutil
import tempfile
from pathlib import Path
from zoneinfo import ZoneInfo
import numpy as np
import pandas as pd
import pytest

from scripts.run_ord_v1 import load_market

ET = ZoneInfo("America/New_York")

def old_load_market(path: Path) -> pd.DataFrame:
    """The original unoptimized data loader logic."""
    df = pd.read_csv(path)
    df["ts"] = pd.to_datetime(df["timestamp"], format="%Y-%m-%d %H:%M:%S", errors="coerce")
    df = df.dropna(subset=["ts"])
    df = df.sort_values("ts").drop_duplicates(subset="ts", keep="first").reset_index(drop=True)
    et = df["ts"].dt.tz_localize("UTC").dt.tz_convert(ET)
    df["et_min"] = et.dt.hour * 60 + et.dt.minute
    df["date"] = et.dt.floor("D")
    df["o"] = df["open"].astype(float)
    df["h"] = df["high"].astype(float)
    df["l"] = df["low"].astype(float)
    df["c"] = df["close"].astype(float)
    return df

@pytest.fixture
def synthetic_market_data(tmp_path):
    # Includes:
    # - valid rows
    # - duplicate timestamps with different OHLC (to verify keep='first')
    # - out of order timestamps (to verify sorting)
    # - malformed timestamps (to verify errors='coerce')
    # - timestamps in opening range and detection window
    csv_content = """timestamp,open,high,low,close,volume
2026-08-18 07:00:00,10.0,10.5,9.5,10.1,100
2026-08-18 07:01:00,10.1,10.6,9.6,10.2,200
2026-08-18 07:00:00,99.0,99.0,99.0,99.0,999
2026-08-18 06:59:00,9.9,10.4,9.4,10.0,300
invalid_date,0,0,0,0,0
2026-08-18 13:30:00,11.0,11.5,10.5,11.1,400
2026-08-18 21:00:00,12.0,12.5,11.5,12.1,500
"""
    file_path = tmp_path / "SYNTH_M1.csv"
    file_path.write_text(csv_content, encoding="utf-8")
    return file_path

def test_scientific_equivalence(synthetic_market_data, monkeypatch):
    # Mock DATA_DIR in run_ord_v1 so load_market reads our temp file
    monkeypatch.setattr("scripts.run_ord_v1.DATA_DIR", synthetic_market_data.parent)
    
    df_old = old_load_market(synthetic_market_data)
    df_new = load_market("SYNTH")
    
    # 1. Surviving rows must match
    assert len(df_old) == len(df_new)
    
    # 2. Chronological order & duplicate selection must match
    # 07:00:00 duplicate winner must be the FIRST one (open=10.0, not 99.0)
    old_ts = df_old["ts"].values
    new_ts = df_new["ts"].values
    np.testing.assert_array_equal(old_ts, new_ts)
    
    old_o = df_old["o"].values
    new_o = df_new["o"].values
    np.testing.assert_array_equal(old_o, new_o)
    
    # Assert specific winner
    assert df_new.loc[1, "o"] == 10.0 # 07:00:00 row
    
    # 3. OHLC values and data types
    assert df_new["o"].dtype == np.float64
    assert df_new["h"].dtype == np.float64
    assert df_new["l"].dtype == np.float64
    assert df_new["c"].dtype == np.float64
    
    for col in ["h", "l", "c"]:
        np.testing.assert_array_equal(df_old[col].values, df_new[col].values)
        
    # 4. Day identity and ET minute
    np.testing.assert_array_equal(df_old["et_min"].values, df_new["et_min"].values)
    np.testing.assert_array_equal(df_old["date"].values, df_new["date"].values)

class MockMarketData:
    def __init__(self, data):
        self.data = data
    def __del__(self):
        global mock_deleted
        mock_deleted = True

mock_deleted = False

def test_market_lifetime():
    global mock_deleted
    mock_deleted = False
    
    # Simulate the main loop's try/finally block
    MARKETS = {"MOCK1": {}, "MOCK2": {}}
    for mkt in MARKETS:
        df = None
        try:
            df = MockMarketData([1,2,3])
            # Process market
            assert df is not None
        finally:
            if df is not None:
                del df
            gc.collect()
            
        assert mock_deleted is True
        mock_deleted = False

def test_memory_diagnostics(synthetic_market_data, monkeypatch):
    """
    Engineering-only memory diagnostic using synthetic data.
    """
    process = psutil.Process(os.getpid())
    
    rss_before = process.memory_info().rss
    
    monkeypatch.setattr("scripts.run_ord_v1.DATA_DIR", synthetic_market_data.parent)
    df = load_market("SYNTH")
    
    rss_during = process.memory_info().rss
    
    del df
    gc.collect()
    
    rss_after = process.memory_info().rss
    
    print(f"\\nRSS Before: {rss_before / 1024**2:.2f} MB")
    print(f"RSS During: {rss_during / 1024**2:.2f} MB")
    print(f"RSS After : {rss_after / 1024**2:.2f} MB")
    
    assert True
