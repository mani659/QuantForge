import pytest
import os
import json
import shutil
from datetime import datetime, timezone
from types import MappingProxyType

from boe.execution.result import ExecutionResult, ExecutionStatus
from research.engine.configuration import ExperimentConfiguration
from research.analytics.trade_reconstructor import TradeReconstructor
from research.analytics.metrics import MetricsCalculator, ResearchResult
from research.analytics.report import AnalyticsPersister, ValidationReport
from research.experiment_recorder import ExperimentRecorder


def _mock_execution(timestamp: datetime, metadata: dict) -> ExecutionResult:
    return ExecutionResult(
        candidate_id="test_candidate",
        timeline_id="test_timeline",
        observation_id="test_observation",
        schema_version="1.0.0",
        status=ExecutionStatus.SUCCESS,
        metadata=MappingProxyType(metadata),
        timestamp=timestamp
    )

def test_zero_trades():
    # Only execution results with no trades
    res = MetricsCalculator.calculate([], initial_capital=100000.0)
    assert res.number_of_trades == 0
    assert res.net_pnl == 0.0
    assert res.win_rate == 0.0
    assert res.profit_factor == 0.0
    assert res.maximum_drawdown == 0.0

def test_one_winning_trade():
    executions = [
        _mock_execution(datetime(2026, 1, 1, tzinfo=timezone.utc), {
            "leg_count": 1,
            "leg_0_action": "BUY",
            "leg_0_direction": "BUY",
            "leg_0_volume": 1.0,
            "leg_0_price": 100.0,
            "leg_0_realized_pnl": 0.0,
            "account_balance": 100000.0
        }),
        _mock_execution(datetime(2026, 1, 2, tzinfo=timezone.utc), {
            "leg_count": 1,
            "leg_0_action": "CLOSE",
            "leg_0_direction": "BUY",
            "leg_0_volume": 1.0,
            "leg_0_price": 110.0,
            "leg_0_realized_pnl": 10.0,
            "account_balance": 100010.0
        })
    ]
    res = MetricsCalculator.calculate(executions, initial_capital=100000.0)
    assert res.number_of_trades == 1
    assert res.winning_trades == 1
    assert res.losing_trades == 0
    assert res.net_pnl == 10.0
    assert res.gross_profit == 10.0
    assert res.gross_loss == 0.0
    assert res.profit_factor == float('inf')
    assert res.maximum_drawdown == 0.0
    assert res.win_rate == 1.0

def test_one_losing_trade():
    executions = [
        _mock_execution(datetime(2026, 1, 1, tzinfo=timezone.utc), {
            "leg_count": 1,
            "leg_0_action": "BUY",
            "leg_0_direction": "BUY",
            "leg_0_volume": 1.0,
            "account_balance": 100000.0
        }),
        _mock_execution(datetime(2026, 1, 2, tzinfo=timezone.utc), {
            "leg_count": 1,
            "leg_0_action": "CLOSE",
            "leg_0_direction": "BUY",
            "leg_0_volume": 1.0,
            "leg_0_realized_pnl": -10.0,
            "account_balance": 99990.0
        })
    ]
    res = MetricsCalculator.calculate(executions)
    assert res.winning_trades == 0
    assert res.losing_trades == 1
    assert res.net_pnl == -10.0
    assert res.gross_loss == 10.0
    assert res.maximum_drawdown == 10.0
    assert res.profit_factor == 0.0

def test_mixed_wins_losses():
    executions = [
        # Win 20
        _mock_execution(datetime(2026, 1, 1, tzinfo=timezone.utc), {"leg_count": 1, "leg_0_action": "BUY", "leg_0_direction": "BUY", "leg_0_volume": 1.0, "account_balance": 100000.0}),
        _mock_execution(datetime(2026, 1, 2, tzinfo=timezone.utc), {"leg_count": 1, "leg_0_action": "CLOSE", "leg_0_direction": "BUY", "leg_0_volume": 1.0, "leg_0_realized_pnl": 20.0, "account_balance": 100020.0}),
        # Loss 10
        _mock_execution(datetime(2026, 1, 3, tzinfo=timezone.utc), {"leg_count": 1, "leg_0_action": "SELL", "leg_0_direction": "SELL", "leg_0_volume": 1.0, "account_balance": 100020.0}),
        _mock_execution(datetime(2026, 1, 4, tzinfo=timezone.utc), {"leg_count": 1, "leg_0_action": "CLOSE", "leg_0_direction": "SELL", "leg_0_volume": 1.0, "leg_0_realized_pnl": -10.0, "account_balance": 100010.0}),
        # Win 30
        _mock_execution(datetime(2026, 1, 5, tzinfo=timezone.utc), {"leg_count": 1, "leg_0_action": "BUY", "leg_0_direction": "BUY", "leg_0_volume": 1.0, "account_balance": 100010.0}),
        _mock_execution(datetime(2026, 1, 6, tzinfo=timezone.utc), {"leg_count": 1, "leg_0_action": "CLOSE", "leg_0_direction": "BUY", "leg_0_volume": 1.0, "leg_0_realized_pnl": 30.0, "account_balance": 100040.0}),
    ]
    res = MetricsCalculator.calculate(executions)
    assert res.number_of_trades == 3
    assert res.winning_trades == 2
    assert res.losing_trades == 1
    assert res.gross_profit == 50.0
    assert res.gross_loss == 10.0
    assert res.net_pnl == 40.0
    assert res.profit_factor == 5.0
    assert res.maximum_drawdown == 10.0
    assert res.win_rate == (2/3)

def test_break_even_trade():
    executions = [
        _mock_execution(datetime(2026, 1, 1, tzinfo=timezone.utc), {"leg_count": 1, "leg_0_action": "BUY", "leg_0_direction": "BUY", "leg_0_volume": 1.0, "account_balance": 100000.0}),
        _mock_execution(datetime(2026, 1, 2, tzinfo=timezone.utc), {"leg_count": 1, "leg_0_action": "CLOSE", "leg_0_direction": "BUY", "leg_0_volume": 1.0, "leg_0_realized_pnl": 0.0, "account_balance": 100000.0})
    ]
    res = MetricsCalculator.calculate(executions)
    assert res.number_of_trades == 1
    assert res.winning_trades == 0
    assert res.losing_trades == 0
    assert res.net_pnl == 0.0
    assert res.gross_profit == 0.0
    assert res.gross_loss == 0.0

def test_drawdown_calculation():
    # Sequence of balances: 100, 110 (Peak), 90 (DD=20), 120 (Peak), 105 (DD=15)
    executions = [
        _mock_execution(datetime(2026, 1, 1, tzinfo=timezone.utc), {"account_balance": 100.0}),
        _mock_execution(datetime(2026, 1, 2, tzinfo=timezone.utc), {"account_balance": 110.0}),
        _mock_execution(datetime(2026, 1, 3, tzinfo=timezone.utc), {"account_balance": 90.0}),
        _mock_execution(datetime(2026, 1, 4, tzinfo=timezone.utc), {"account_balance": 120.0}),
        _mock_execution(datetime(2026, 1, 5, tzinfo=timezone.utc), {"account_balance": 105.0}),
    ]
    res = MetricsCalculator.calculate(executions, initial_capital=100.0)
    assert res.maximum_drawdown == 20.0
    assert res.maximum_drawdown_percentage == (20.0 / 110.0)

def test_deterministic_repeated_calculation():
    executions = [
        _mock_execution(datetime(2026, 1, 1, tzinfo=timezone.utc), {"leg_count": 1, "leg_0_action": "BUY", "leg_0_direction": "BUY", "leg_0_volume": 1.0, "account_balance": 100000.0}),
        _mock_execution(datetime(2026, 1, 2, tzinfo=timezone.utc), {"leg_count": 1, "leg_0_action": "CLOSE", "leg_0_direction": "BUY", "leg_0_volume": 1.0, "leg_0_realized_pnl": 10.0, "account_balance": 100010.0})
    ]
    res1 = MetricsCalculator.calculate(executions)
    res2 = MetricsCalculator.calculate(executions)
    
    assert res1 == res2
    
def test_persistence_round_trip():
    temp_dir = "./test_analytics_outcomes"
    os.makedirs(temp_dir, exist_ok=True)
    try:
        # Create fake run directory to mimic ExperimentRecorder
        run_id = "run_000001"
        run_folder = os.path.join(temp_dir, "research", "experiments", run_id)
        os.makedirs(run_folder, exist_ok=True)
        
        # Write dummy manifest
        with open(os.path.join(run_folder, "manifest.json"), "w") as f:
            json.dump({"run_id": run_id, "files": []}, f)
            
        recorder = ExperimentRecorder(temp_dir)
        persister = AnalyticsPersister(recorder)
        
        config = ExperimentConfiguration(
            dataset_id="test_data",
            dataset_partition="TRAIN",
            instrument="EURUSD",
            timeframe="M1",
            date_range_start=datetime(2026, 1, 1, tzinfo=timezone.utc),
            date_range_end=datetime(2026, 1, 2, tzinfo=timezone.utc),
            strategy_id="strat_1",
            strategy_version="1.0"
        )
        
        executions = [
            _mock_execution(datetime(2026, 1, 1, tzinfo=timezone.utc), {"leg_count": 1, "leg_0_action": "BUY", "leg_0_direction": "BUY", "leg_0_volume": 1.0, "account_balance": 100000.0}),
            _mock_execution(datetime(2026, 1, 2, tzinfo=timezone.utc), {"leg_count": 1, "leg_0_action": "CLOSE", "leg_0_direction": "BUY", "leg_0_volume": 1.0, "leg_0_realized_pnl": 10.0, "account_balance": 100010.0})
        ]
        res = MetricsCalculator.calculate(executions)
        
        # Original ExecutionResult must remain unchanged
        assert executions[0].metadata["account_balance"] == 100000.0
        
        report = ValidationReport(
            experiment_id="test_exp_id", dataset_id=config.dataset_id, dataset_partition=config.dataset_partition,
            instrument=config.instrument, timeframe=config.timeframe, date_range_start=config.date_range_start.isoformat(),
            date_range_end=config.date_range_end.isoformat(), strategy_id=config.strategy_id, strategy_version=config.strategy_version,
            strategy_parameters=config.strategy_parameters, execution_assumptions={}, results=res
        )
        report_file = persister.save_report(run_id, report)
        assert os.path.exists(report_file)
        
        # Verify deterministic reconstruction
        with open(report_file, "r") as f:
            data = json.load(f)
            assert data["experiment_id"] == "test_exp_id"
            assert data["results"]["net_pnl"] == 10.0
            assert data["strategy_id"] == "strat_1"
            
    finally:
        shutil.rmtree(temp_dir)


def test_persistence_infinity_and_overwrite():
    temp_dir = "./test_analytics_outcomes2"
    os.makedirs(temp_dir, exist_ok=True)
    try:
        run_id = "run_000002"
        run_folder = os.path.join(temp_dir, "research", "experiments", run_id)
        os.makedirs(run_folder, exist_ok=True)
        
        with open(os.path.join(run_folder, "manifest.json"), "w") as f:
            json.dump({"run_id": run_id, "files": []}, f)
            
        recorder = ExperimentRecorder(temp_dir)
        persister = AnalyticsPersister(recorder)
        
        config = ExperimentConfiguration(
            dataset_id="test_data", dataset_partition="TRAIN", instrument="EURUSD", timeframe="M1",
            date_range_start=datetime(2026, 1, 1, tzinfo=timezone.utc),
            date_range_end=datetime(2026, 1, 2, tzinfo=timezone.utc),
            strategy_id="strat_2", strategy_version="1.0"
        )
        
        # Win with 0 gross loss -> infinite profit factor
        executions = [
            _mock_execution(datetime(2026, 1, 1, tzinfo=timezone.utc), {"leg_count": 1, "leg_0_action": "BUY", "leg_0_direction": "BUY", "leg_0_volume": 1.0, "account_balance": 100000.0}),
            _mock_execution(datetime(2026, 1, 2, tzinfo=timezone.utc), {"leg_count": 1, "leg_0_action": "CLOSE", "leg_0_direction": "BUY", "leg_0_volume": 1.0, "leg_0_realized_pnl": 10.0, "account_balance": 100010.0})
        ]
        res = MetricsCalculator.calculate(executions)
        assert res.profit_factor == float('inf')
        
        report = ValidationReport(
            experiment_id="test_exp_id2", dataset_id=config.dataset_id, dataset_partition=config.dataset_partition,
            instrument=config.instrument, timeframe=config.timeframe, date_range_start=config.date_range_start.isoformat(),
            date_range_end=config.date_range_end.isoformat(), strategy_id=config.strategy_id, strategy_version=config.strategy_version,
            strategy_parameters=config.strategy_parameters, execution_assumptions={}, results=res
        )
        report_file = persister.save_report(run_id, report)
        assert os.path.exists(report_file)
        
        with open(report_file, "r") as f:
            data = json.load(f)
            assert data["results"]["profit_factor"] == "Infinity"
            
        # Overwrite should raise FileExistsError
        with pytest.raises(FileExistsError, match="Overwrite rejected to preserve reproducibility"):
            persister.save_report(run_id, report)
            
    finally:
        shutil.rmtree(temp_dir)
