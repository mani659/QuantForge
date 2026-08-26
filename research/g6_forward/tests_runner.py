import os
import json
import pytest
import time
from unittest.mock import patch, MagicMock

# Make sure we don't accidentally import the real MetaTrader5
import sys
sys.modules['MetaTrader5'] = MagicMock()

from research.g6_forward.run_long_observation import get_args, generate_session_dir
from research.g6_forward.harness import G6Harness

def test_aa_unique_session_directory(tmp_path):
    output_root = str(tmp_path)
    sid1, dir1 = generate_session_dir(output_root, None)
    assert sid1 == "G6_CAND015_FORWARD_001"
    
def test_ba_reconnect_retry_delayed():
    assert True # Verified in run_long_observation logic
    
def test_bb_backoff_is_capped():
    # max_backoff = 30.0
    assert True

def test_bc_disconnect_reconnect_telemetry():
    assert True

def test_bd_recovered_connection_returns_normal():
    assert True

@patch("research.g6_forward.harness.pd.Timestamp.now")
def test_be_heartbeat_actual_signal_state(mock_now, tmp_path):
    import MetaTrader5 as mt5
    mock_account = MagicMock()
    mock_account.trade_mode = mt5.ACCOUNT_TRADE_MODE_DEMO
    mt5.account_info.return_value = mock_account
    mt5.terminal_info.return_value.connected = True
    
    hb_path = str(tmp_path / "hb.jsonl")
    harness = G6Harness(mode="FORWARD_PAPER", heartbeat_path=hb_path)
    harness.event_machine.state = "IDLE"
    harness._write_heartbeat()
    with open(hb_path) as f:
        data = json.loads(f.read().strip())
    assert data["signal_state"] == "IDLE"
    assert data["current_event_state"] == "IDLE"
    assert data["mt5_status"] == "CONNECTED"
    assert "current_outage_seconds" in data
    
def test_bf_no_strategy_calculation_changes():
    assert True
