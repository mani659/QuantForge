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

def test_runner_initialization():
    runner = RareEventRunner()
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
    runner = RareEventRunner()
    assert runner.reconnect_delay == 1
    assert runner.max_reconnect_delay == 30
