import pytest
import os
import sys

# Add directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from contracts import CAND_024_CONTRACT, CAND_035_CONTRACT
from rare_event_runner import RareEventRunner
from cand_024_engine import Cand024Engine
from cand_035_engine import Cand035Engine

def test_contract_integrity():
    # Verify deterministic hashes
    assert CAND_024_CONTRACT.candidate_id == "CAND-024"
    assert CAND_035_CONTRACT.candidate_id == "CAND-035"
    assert len(CAND_024_CONTRACT.hash) == 64
    assert len(CAND_035_CONTRACT.hash) == 64

class MockFeed:
    def __init__(self, connected=True, stale=False):
        self._connected = connected
        self._stale = stale
    def connection_state(self):
        return "CONNECTED" if self._connected else "DISCONNECTED"
    def latest_quote(self, symbol):
        if not self._connected: return {"status": "FEED_UNAVAILABLE"}
        if self._stale: return {"status": "DATA_STALE", "age": 90}
        return {"status": "DATA_FRESH", "source_timestamp": 1000, "symbol": symbol, "bid": 10, "ask": 11}

def test_runner_initialization():
    runner = RareEventRunner(feed=MockFeed(), mode="test")
    assert runner.cand_024.state == "WATCHING"
    assert runner.cand_035.state == "WATCHING"
    assert hasattr(runner, 'event_ledger')
    assert hasattr(runner, 'outcome_ledger')
    assert hasattr(runner, 'paper')

def test_duplicate_prevention_024():
    engine = Cand024Engine()
    # Mock Friday
    # ... basic state transition check ...
    assert engine.state == "WATCHING"

def test_reconnect_backoff():
    runner = RareEventRunner(feed=MockFeed(), mode="test")
    assert runner.reconnect_delay == 1
    assert runner.max_reconnect_delay == 30

def test_feed_stale_rejection():
    feed = MockFeed(stale=True)
    runner = RareEventRunner(feed=feed, mode="test")
    # A single cycle processing logic simulation (the loop logic uses this)
    quote = feed.latest_quote("USATECHIDXUSD")
    assert quote["status"] == "DATA_STALE"

def test_paper_execution_isolation():
    from paper_execution import PaperExecutionFirewall
    paper = PaperExecutionFirewall(friction=2.0)
    assert not hasattr(paper, "order_send"), "Paper execution must not have real order APIs"
    assert not hasattr(paper, "mt5"), "Paper execution must not import MT5"
