from dataclasses import dataclass
from typing import Iterable, List
import math

from boe.execution.result import ExecutionResult
from research.analytics.trade_reconstructor import TradeReconstructor, CompletedTrade


@dataclass(frozen=True)
class ResearchResult:
    """
    Immutable representation of derived research analytics.
    """
    start_timestamp: str
    end_timestamp: str
    initial_capital: float
    final_capital: float
    net_pnl: float
    gross_profit: float
    gross_loss: float
    number_of_trades: int
    winning_trades: int
    losing_trades: int
    win_rate: float
    average_win: float
    average_loss: float
    profit_factor: float
    maximum_drawdown: float
    maximum_drawdown_percentage: float
    largest_win: float
    largest_loss: float


class MetricsCalculator:
    """
    Deterministically computes ResearchResult metrics from a sequence of raw ExecutionResults.
    """
    
    @staticmethod
    def calculate(execution_results: Iterable[ExecutionResult], initial_capital: float = 100000.0) -> ResearchResult:
        sorted_results = sorted(execution_results, key=lambda r: r.timestamp)
        
        if not sorted_results:
            return MetricsCalculator._empty_result(initial_capital)
            
        trades = TradeReconstructor.reconstruct(sorted_results)
        
        # Drawdown calculation
        peak_equity = initial_capital
        max_drawdown = 0.0
        max_drawdown_percentage = 0.0
        
        # To strictly use realized equity, we track the balance at each execution step.
        # This handles the fact that ExecutionResult metadata stores 'account_balance' 
        # at the moment of the trade.
        for res in sorted_results:
            balance = res.metadata.get("account_balance", initial_capital)
            peak_equity = max(peak_equity, balance)
            current_drawdown = peak_equity - balance
            max_drawdown = max(max_drawdown, current_drawdown)
            if peak_equity > 0:
                max_drawdown_percentage = max(max_drawdown_percentage, max_drawdown / peak_equity)
                
        final_capital = sorted_results[-1].metadata.get("account_balance", initial_capital)
        net_pnl = final_capital - initial_capital
        
        gross_profit = sum(t.realized_pnl for t in trades if t.realized_pnl > 0)
        gross_loss = sum(abs(t.realized_pnl) for t in trades if t.realized_pnl < 0)
        
        winning_trades = [t for t in trades if t.realized_pnl > 0]
        losing_trades = [t for t in trades if t.realized_pnl < 0]
        
        num_wins = len(winning_trades)
        num_losses = len(losing_trades)
        num_trades = len(trades)
        
        win_rate = num_wins / num_trades if num_trades > 0 else 0.0
        average_win = gross_profit / num_wins if num_wins > 0 else 0.0
        average_loss = gross_loss / num_losses if num_losses > 0 else 0.0
        
        if gross_loss == 0.0:
            profit_factor = float('inf') if gross_profit > 0 else 0.0
        else:
            profit_factor = gross_profit / gross_loss
            
        largest_win = max([t.realized_pnl for t in winning_trades], default=0.0)
        largest_loss = min([t.realized_pnl for t in losing_trades], default=0.0)

        return ResearchResult(
            start_timestamp=sorted_results[0].timestamp.isoformat(),
            end_timestamp=sorted_results[-1].timestamp.isoformat(),
            initial_capital=initial_capital,
            final_capital=final_capital,
            net_pnl=net_pnl,
            gross_profit=gross_profit,
            gross_loss=gross_loss,
            number_of_trades=num_trades,
            winning_trades=num_wins,
            losing_trades=num_losses,
            win_rate=win_rate,
            average_win=average_win,
            average_loss=average_loss,
            profit_factor=profit_factor,
            maximum_drawdown=max_drawdown,
            maximum_drawdown_percentage=max_drawdown_percentage,
            largest_win=largest_win,
            largest_loss=largest_loss
        )
        
    @staticmethod
    def _empty_result(initial_capital: float) -> ResearchResult:
        return ResearchResult(
            start_timestamp="",
            end_timestamp="",
            initial_capital=initial_capital,
            final_capital=initial_capital,
            net_pnl=0.0,
            gross_profit=0.0,
            gross_loss=0.0,
            number_of_trades=0,
            winning_trades=0,
            losing_trades=0,
            win_rate=0.0,
            average_win=0.0,
            average_loss=0.0,
            profit_factor=0.0,
            maximum_drawdown=0.0,
            maximum_drawdown_percentage=0.0,
            largest_win=0.0,
            largest_loss=0.0
        )
