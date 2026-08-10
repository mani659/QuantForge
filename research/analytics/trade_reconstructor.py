from dataclasses import dataclass
from datetime import datetime
from typing import Iterable, List

from boe.execution.result import ExecutionResult, ExecutionStatus

@dataclass(frozen=True)
class CompletedTrade:
    """
    Represents a fully or partially closed trade, reconstructed from raw execution evidence.
    """
    entry_timestamp: datetime
    exit_timestamp: datetime
    direction: str
    volume: float
    realized_pnl: float


class TradeReconstructor:
    """
    Reconstructs a sequence of CompletedTrade objects from a raw stream of ExecutionResults.
    
    A trade is formed when a position is reduced or closed. 
    Entry timestamp is approximated to the earliest active open position timestamp.
    """

    @staticmethod
    def reconstruct(execution_results: Iterable[ExecutionResult]) -> List[CompletedTrade]:
        trades = []
        
        # State trackers
        current_direction = "NONE"
        current_volume = 0.0
        entry_timestamp = None
        
        for res in sorted(execution_results, key=lambda r: r.timestamp):
            if res.status != ExecutionStatus.SUCCESS:
                continue
                
            metadata = res.metadata
            leg_count = metadata.get("leg_count", 0)
            
            for i in range(leg_count):
                action = metadata.get(f"leg_{i}_action", "NONE")
                direction = metadata.get(f"leg_{i}_direction", "NONE")
                volume = metadata.get(f"leg_{i}_volume", 0.0)
                pnl = metadata.get(f"leg_{i}_realized_pnl", 0.0)
                
                if action in ("BUY", "SELL") and action == direction:
                    # New position or increase
                    if current_volume == 0.0:
                        entry_timestamp = res.timestamp
                        current_direction = direction
                    current_volume += volume
                    
                elif action in ("CLOSE", "REDUCE"):
                    if entry_timestamp is not None:
                        trades.append(CompletedTrade(
                            entry_timestamp=entry_timestamp,
                            exit_timestamp=res.timestamp,
                            direction=direction,
                            volume=volume,
                            realized_pnl=pnl
                        ))
                    current_volume -= volume
                    if current_volume <= 1e-9:
                        current_volume = 0.0
                        current_direction = "NONE"
                        entry_timestamp = None

        return trades
