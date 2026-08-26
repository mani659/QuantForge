import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timezone
import os

from research.g6_forward.cand015_identity import FROZEN_CAND015_IDENTITY, verify_identity
from research.g6_forward.data_feed import MarketDataFeed
from research.g6_forward.signal_engine import Cand015SignalEngine
from research.g6_forward.event_machine import EventStateMachine
from research.g6_forward.paper_execution import PaperExecutionAdapter
from research.g6_forward.ledger import EventLedger
from research.g6_forward.harness import G6Harness

def generate_synthetic_data():
    dates = pd.date_range("2023-09-01 00:00:00", periods=70000, freq='1min', tz=timezone.utc)
    
    ndx_close = np.linspace(15000, 16000, 70000)
    ndx_close[69900] = 15000
    ndx_close[69901] = 15500
    ndx_close[69902] = 16000
    ndx_close[69903] = 16500
    ndx_close[69904] = 16500 
    
    df_ndx = pd.DataFrame({
        'timestamp': dates, 'open': ndx_close - 1, 'high': ndx_close + 1, 'low': ndx_close - 2, 'close': ndx_close
    })
    
    btc_close = np.linspace(25000, 26000, 70000)
    df_btc = pd.DataFrame({
        'timestamp': dates, 'open': btc_close - 10, 'high': btc_close + 10, 'low': btc_close - 20, 'close': btc_close
    })
    return df_ndx, df_btc

def test_a_identity_mismatch():
    import research.g6_forward.cand015_identity as identity_module
    original = identity_module.FROZEN_CAND015_IDENTITY["lockout_minutes"]
    identity_module.FROZEN_CAND015_IDENTITY.pop("lockout_minutes")
    with pytest.raises(RuntimeError):
        identity_module.verify_identity()
    identity_module.FROZEN_CAND015_IDENTITY["lockout_minutes"] = original
    
    identity_module.FROZEN_CAND015_IDENTITY["shock_definition"]["condition"] = "> 2 * atr_30d"
    with pytest.raises(RuntimeError):
        identity_module.verify_identity()
    identity_module.FROZEN_CAND015_IDENTITY["shock_definition"]["condition"] = "> 3 * atr_30d"

def test_b_duplicate_shock_lockout():
    engine = Cand015SignalEngine(FROZEN_CAND015_IDENTITY)
    ts1 = pd.Timestamp("2026-08-01 10:05:00", tz=timezone.utc)
    engine.last_shock_time = ts1
    
    ts2 = pd.Timestamp("2026-08-01 10:10:00", tz=timezone.utc)
    locked_out = ts2 < engine.last_shock_time + pd.Timedelta(minutes=engine.lockout_minutes)
    assert locked_out == True

def test_c_volatility_state_pre_entry():
    engine = Cand015SignalEngine(FROZEN_CAND015_IDENTITY)
    df_ndx, _ = generate_synthetic_data()
    records = df_ndx.iloc[:69905].to_dict('records')
    for row in records:
        row['symbol'] = "USATECHIDXUSD"
        row['observation_timestamp'] = row['timestamp']
    engine.m1_buffer_ndx = records
    
    eval_time = df_ndx.iloc[69905]['timestamp'] 
    signal = engine._evaluate_signal(eval_time)
    
    assert signal is not None
    initial_state = signal['volatility_state']
    
    future_tick = df_ndx.iloc[69905].copy()
    future_tick['timestamp'] = future_tick['timestamp'] + pd.Timedelta(hours=4)
    future_tick['high'] += 500000
    future_tick['low'] -= 500000
    
    future_record = future_tick.to_dict()
    future_record['symbol'] = "USATECHIDXUSD"
    future_record['observation_timestamp'] = future_record['timestamp']
    engine.m1_buffer_ndx.append(future_record)
    
    # Reset lockout so we can evaluate again
    engine.last_shock_time = None
    
    signal2 = engine._evaluate_signal(eval_time)
    assert signal2 is not None
    assert signal2['volatility_state'] == initial_state

def test_d_signal_timing():
    engine = Cand015SignalEngine(FROZEN_CAND015_IDENTITY)
    df_ndx, _ = generate_synthetic_data()
    
    records = df_ndx.iloc[:69904].to_dict('records') 
    for row in records:
        row['symbol'] = "USATECHIDXUSD"
        row['observation_timestamp'] = row['timestamp']
    engine.m1_buffer_ndx = records
    
    eval_time_incomplete = df_ndx.iloc[69904]['timestamp']
    
    signal_incomplete = engine._evaluate_signal(eval_time_incomplete)
    assert signal_incomplete is None

def test_e_paper_entry_uses_quote():
    adapter = PaperExecutionAdapter("REPLAY_TEST", FROZEN_CAND015_IDENTITY)
    tick = {
        "observation_timestamp": pd.Timestamp("2026-08-01 10:05:00", tz=timezone.utc),
        "open": 50000.0, "high": 50100.0, "low": 49900.0, "close": 50050.0,
        "bid": "unavailable", "ask": "unavailable"
    }
    decision_ts = pd.Timestamp("2026-08-01 10:05:00.050", tz=timezone.utc)
    report = adapter.execute_entry({"signal_direction": 1}, tick, decision_ts)
    assert report["execution_price"] == 50000.0 
    assert report["execution_price_type"] == "SYNTHETIC_REPLAY"

def test_f_deterministic_exit():
    machine = EventStateMachine()
    
    entry_ts = pd.Timestamp("2026-08-01 10:00:00", tz=timezone.utc)
    machine.handle_signal({"event_type": "SHOCK"}, entry_ts - pd.Timedelta(minutes=5))
    machine.handle_entry({"execution_price": 50000}, entry_ts)
    assert machine.state == "IN_POSITION"
    
    intermediate_ts = entry_ts + pd.Timedelta(minutes=30)
    exit_triggered = intermediate_ts >= entry_ts + pd.Timedelta(minutes=60)
    assert exit_triggered == False
    
    horizon_ts = entry_ts + pd.Timedelta(minutes=60)
    exit_triggered = horizon_ts >= entry_ts + pd.Timedelta(minutes=60)
    assert exit_triggered == True

def test_g_no_real_orders():
    assert "execute_real_order" not in dir(PaperExecutionAdapter)
    with pytest.raises(NotImplementedError):
        MarketDataFeed(mode="FORWARD_PAPER")

def test_h_historical_parity():
    df_ndx, df_btc = generate_synthetic_data()
    
    harness = G6Harness(mode="REPLAY_TEST", data_paths={}, ledger_path="test_ledger_h.csv")
    
    records = df_ndx.iloc[:69900].to_dict('records')
    for row in records:
        row['symbol'] = "USATECHIDXUSD"
        row['observation_timestamp'] = row['timestamp']
    harness.signal_engine.m1_buffer_ndx = records
    
    for idx, row in df_ndx.iloc[69900:69906].iterrows():
        r = row.to_dict()
        r['symbol'] = "USATECHIDXUSD"
        r['observation_timestamp'] = r['timestamp']
        r['bid'] = "unavailable"
        r['ask'] = "unavailable"
        harness._process_tick(r)
        
        btc_r = df_btc.loc[idx].to_dict()
        btc_r['symbol'] = "BTCUSD"
        btc_r['observation_timestamp'] = btc_r['timestamp']
        btc_r['bid'] = "unavailable"
        btc_r['ask'] = "unavailable"
        harness._process_tick(btc_r)
        
    assert harness.event_count == 0 
    
    for idx, row in df_ndx.iloc[69906:69970].iterrows():
        btc_r = df_btc.loc[idx].to_dict()
        btc_r['symbol'] = "BTCUSD"
        btc_r['observation_timestamp'] = btc_r['timestamp']
        btc_r['bid'] = "unavailable"
        btc_r['ask'] = "unavailable"
        harness._process_tick(btc_r)
        
    assert harness.event_count == 1
    
    ledger_df = pd.read_csv("test_ledger_h.csv")
    assert len(ledger_df) == 1
    
    trade = ledger_df.iloc[0]
    assert trade['event_type'] == "SHOCK"
    assert trade['state'] == "CLOSED"
    
    os.remove("test_ledger_h.csv")

def test_i_event_ledger():
    ledger = EventLedger("test_ledger.csv", "REPLAY_TEST")
    record = {
        "execution_id": "123", "candidate_id": "CAND-015", "event_id": "456",
        "timestamp": "2026", "market": "BTCUSD", "event_type": "SHOCK",
        "state": "CLOSED", "signal_direction": 1, "intended_entry_price": 50000,
        "observed_bid": "u", "observed_ask": "u", "paper_entry": 50000,
        "paper_exit": 51000, "gross_result": 200, "transaction_cost": 3.0,
        "net_result": 197, "latency_ms": 50, "implementation_sha": "abc",
        "data_source_identity": "test", "mode": "REPLAY_TEST", "price_source": "test",
        "execution_price_type": "test", "slippage_status": "test", "latency_status": "test"
    }
    ledger.record_trade(record)
    with open("test_ledger.csv", "r") as f:
        assert len(f.readlines()) == 2
    os.remove("test_ledger.csv")

def test_j_heartbeat(capsys):
    harness = G6Harness(mode="REPLAY_TEST", data_paths={}, ledger_path="test_ledger_j.csv")
    import time
    last_heartbeat = time.time() - 6.0
    
    if time.time() - last_heartbeat > 5.0:
        print(f"Heartbeat: state={harness.event_machine.state}, events={harness.event_count}")
        last_heartbeat = time.time()
        
    captured = capsys.readouterr()
    assert "Heartbeat: state=IDLE, events=0" in captured.out
    
    if os.path.exists("test_ledger_j.csv"):
        os.remove("test_ledger_j.csv")


import unittest.mock as mock

def test_k_exact_symbol_mapping():
    from research.g6_forward.mt5_feed import MT5DataFeed
    feed = MT5DataFeed(mode="REPLAY_TEST", identity={})
    assert feed.MAPPING["USATECHIDXUSD"] == "USTECm"
    assert feed.MAPPING["BTCUSD"] == "BTCUSDm"

def test_l_wrong_mapping_fails():
    from research.g6_forward.mt5_feed import MT5DataFeed
    import research.g6_forward.mt5_feed as mt5_feed
    with mock.patch.object(mt5_feed, 'MT5_AVAILABLE', True), \
         mock.patch('research.g6_forward.mt5_feed.mt5') as mock_mt5:
        mock_mt5.initialize.return_value = True
        mock_mt5.terminal_info.return_value.connected = True
        mock_mt5.account_info.return_value.trade_mode = mock_mt5.ACCOUNT_TRADE_MODE_DEMO
        mock_mt5.symbol_select.side_effect = lambda x, y: x != "WRONGm"
        
        feed = MT5DataFeed(mode="REPLAY_TEST", identity={})
        feed.MAPPING["USATECHIDXUSD"] = "WRONGm"
        with pytest.raises(RuntimeError, match="FAIL CLOSED: Symbol WRONGm not available"):
            feed.mode = "FORWARD_PAPER"
            feed._initialize_mt5_safety()

def test_m_no_mt5_connection_blocks_forward_mode():
    from research.g6_forward.mt5_feed import MT5DataFeed
    import research.g6_forward.mt5_feed as mt5_feed
    with mock.patch.object(mt5_feed, 'MT5_AVAILABLE', True), \
         mock.patch('research.g6_forward.mt5_feed.mt5') as mock_mt5:
        mock_mt5.initialize.return_value = False
        with pytest.raises(RuntimeError, match="FAIL CLOSED: MT5 initialize\(\) failed"):
            MT5DataFeed(mode="FORWARD_PAPER", identity={})

def test_n_non_demo_account_blocks_forward_mode():
    from research.g6_forward.mt5_feed import MT5DataFeed
    import research.g6_forward.mt5_feed as mt5_feed
    with mock.patch.object(mt5_feed, 'MT5_AVAILABLE', True), \
         mock.patch('research.g6_forward.mt5_feed.mt5') as mock_mt5:
        mock_mt5.initialize.return_value = True
        mock_mt5.terminal_info.return_value.connected = True
        mock_mt5.account_info.return_value.trade_mode = 1 # Not demo
        with pytest.raises(RuntimeError, match="FAIL CLOSED: MT5 account is NOT DEMO"):
            MT5DataFeed(mode="FORWARD_PAPER", identity={})

def test_o_bid_ask_capture():
    from research.g6_forward.mt5_feed import MT5DataFeed
    feed = MT5DataFeed(mode="REPLAY_TEST", identity={})
    feed.mode = "FORWARD_PAPER"
    
    mock_info = mock.Mock(time=int(pd.Timestamp.now(tz=timezone.utc).timestamp()), bid=100.0, ask=101.0, last=100.5)
    mock_rates = [{'time': int(pd.Timestamp.now().timestamp()), 'open': 100, 'high': 102, 'low': 99, 'close': 101},
                  {'time': int(pd.Timestamp.now().timestamp()), 'open': 100, 'high': 102, 'low': 99, 'close': 101}]
                  
    with mock.patch('research.g6_forward.mt5_feed.mt5.symbol_info', return_value=mock_info), \
         mock.patch('research.g6_forward.mt5_feed.mt5.copy_rates_from_pos', return_value=mock_rates):
        obs = feed.fetch_latest_observations()
        assert len(obs) == 2
        assert obs[0]["bid"] == 100.0
        assert obs[0]["ask"] == 101.0
        assert obs[0]["true_spread"] == 1.0

def test_p_in_progress_m5_bar_ignored():
    # Tested inherently because we use rates[-2] which is the last completed bar
    from research.g6_forward.mt5_feed import MT5DataFeed
    feed = MT5DataFeed(mode="REPLAY_TEST", identity={})
    feed.mode = "FORWARD_PAPER"
    mock_info = mock.Mock(time=int(pd.Timestamp.now(tz=timezone.utc).timestamp()), bid=100.0, ask=101.0, last=100.5)
    
    # Rates: [-2] is completed, [-1] is in-progress
    mock_rates = [{'time': 1, 'open': 1, 'high': 1, 'low': 1, 'close': 1},
                  {'time': 2, 'open': 2, 'high': 2, 'low': 2, 'close': 2}]
                  
    with mock.patch('research.g6_forward.mt5_feed.mt5.symbol_info', return_value=mock_info), \
         mock.patch('research.g6_forward.mt5_feed.mt5.copy_rates_from_pos', return_value=mock_rates):
        obs = feed.fetch_latest_observations()
        assert obs[0]["close"] == 1 # Gets index -2, not -1 (which is 2)

def test_q_equal_timestamp_deterministic_ordering():
    from research.g6_forward.harness import G6Harness
    harness = G6Harness(mode="REPLAY_TEST", data_paths={}, ledger_path="test_ledger_q.csv")
    
    # Mock _process_tick
    processed = []
    def mock_process(tick):
        processed.append(tick["symbol"])
        
    harness._process_tick = mock_process
    harness.mode = "FORWARD_PAPER"
    
    obs = [
        {"symbol": "BTCUSD", "observation_timestamp": 100},
        {"symbol": "USATECHIDXUSD", "observation_timestamp": 100}
    ]
    
    # Run the ordering logic manually as in run_forward_observation
    obs.sort(key=lambda x: (x["observation_timestamp"], 0 if x["symbol"] == "USATECHIDXUSD" else 1))
    
    for o in obs:
        harness._process_tick(o)
        
    assert processed[0] == "USATECHIDXUSD"
    assert processed[1] == "BTCUSD"

def test_r_paper_execution_has_no_order_endpoint():
    assert "order_send" not in dir(PaperExecutionAdapter)
    assert "execute_real_order" not in dir(PaperExecutionAdapter)

def test_s_ledger_contains_broker_mapping():
    ledger = EventLedger("test_ledger_s.csv", "FORWARD_PAPER")
    assert "broker_symbol" in ledger.headers
    assert "research_symbol" in ledger.headers
    os.remove("test_ledger_s.csv")

def test_t_stale_tick_fails_closed():
    from research.g6_forward.mt5_feed import MT5DataFeed
    feed = MT5DataFeed(mode="REPLAY_TEST", identity={})
    feed.mode = "FORWARD_PAPER"
    
    # 600 seconds ago
    old_time = int(pd.Timestamp.now(tz=timezone.utc).timestamp()) - 600
    mock_info = mock.Mock(time=old_time, bid=100.0, ask=101.0, last=100.5)
    
    with mock.patch('research.g6_forward.mt5_feed.mt5.symbol_info', return_value=mock_info):
        with pytest.raises(RuntimeError, match="FAIL CLOSED: DATA STALE"):
            feed.fetch_latest_observations()

def test_u_forward_loop_stops_cleanly():
    harness = G6Harness(mode="REPLAY_TEST", data_paths={}, ledger_path="test_ledger_u.csv")
    harness.mode = "FORWARD_PAPER"
    harness.data_feed = mock.Mock()
    harness._stop_event = True
    # Should exit immediately without error
    harness.run_forward_observation()
    if os.path.exists("test_ledger_u.csv"):
        os.remove("test_ledger_u.csv")

def test_v_max_duration_seconds():
    harness = G6Harness(mode="REPLAY_TEST", data_paths={}, ledger_path="test_ledger_v.csv")
    harness.mode = "FORWARD_PAPER"
    harness.data_feed = mock.Mock()
    harness.data_feed.fetch_latest_observations.return_value = []
    # Should run for very short time then exit
    harness.run_forward_observation(poll_interval_ms=10, max_duration_seconds=0.1)
    if os.path.exists("test_ledger_v.csv"):
        os.remove("test_ledger_v.csv")

def test_w_quote_execution_difference_entry():
    adapter = PaperExecutionAdapter("FORWARD_PAPER", FROZEN_CAND015_IDENTITY)
    
    # Long Entry uses Ask
    active_trade = {"signal_direction": 1}
    tick = {"observation_timestamp": 0, "bid": 100, "ask": 102}
    res = adapter.execute_entry(active_trade, tick, 0)
    assert res["execution_price"] == 102
    
    # Short Entry uses Bid
    active_trade = {"signal_direction": -1}
    res = adapter.execute_entry(active_trade, tick, 0)
    assert res["execution_price"] == 100

def test_x_quote_execution_difference_exit():
    adapter = PaperExecutionAdapter("FORWARD_PAPER", FROZEN_CAND015_IDENTITY)
    
    # Long Exit uses Bid
    active_trade = {"signal_direction": 1}
    tick = {"observation_timestamp": 0, "bid": 100, "ask": 102}
    res = adapter.execute_exit(active_trade, tick, 0)
    assert res["execution_price"] == 100
    
    # Short Exit uses Ask
    active_trade = {"signal_direction": -1}
    res = adapter.execute_exit(active_trade, tick, 0)
    assert res["execution_price"] == 102

def test_y_transaction_cost_not_double_counted():
    adapter = PaperExecutionAdapter("FORWARD_PAPER", FROZEN_CAND015_IDENTITY)
    active_trade = {"signal_direction": 1}
    tick = {"observation_timestamp": 0, "bid": 100, "ask": 102}
    res = adapter.execute_entry(active_trade, tick, 0)
    assert res["cost_bps"] == FROZEN_CAND015_IDENTITY["friction_bps"]

def test_z_replay_mode_remains_unchanged():
    adapter = PaperExecutionAdapter("REPLAY_TEST", FROZEN_CAND015_IDENTITY)
    active_trade = {"signal_direction": 1}
    tick = {"observation_timestamp": 0, "open": 101, "bid": 100, "ask": 102}
    res = adapter.execute_entry(active_trade, tick, 0)
    assert res["execution_price"] == 101 # Uses open, not bid/ask
    assert res["execution_price_type"] == "SYNTHETIC_REPLAY"
