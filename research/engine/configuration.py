from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, Optional

@dataclass(frozen=True)
class ExperimentConfiguration:
    """
    Immutable configuration capturing all variables required to reproduce a Research Run.
    """
    dataset_id: str
    dataset_partition: str # e.g., "TRAIN", "VALIDATION", "TEST"
    instrument: str
    timeframe: str
    
    date_range_start: datetime
    date_range_end: datetime
    
    strategy_id: str
    strategy_version: str
    strategy_parameters: Dict[str, Any] = field(default_factory=dict)
    
    initial_capital: float = 100000.0
    # Dictionary for transaction costs (e.g., {'spread': 0.0001, 'commission': 2.0})
    transaction_costs: Dict[str, float] = field(default_factory=dict)
    
    random_seed: Optional[int] = None
    
    def __post_init__(self):
        valid_partitions = ("TRAIN", "VALIDATION", "TEST")
        if self.dataset_partition not in valid_partitions:
            raise ValueError(f"dataset_partition must be one of {valid_partitions}")
        if not isinstance(self.date_range_start, datetime) or not isinstance(self.date_range_end, datetime):
            raise ValueError("Date ranges must be datetime instances.")
        if self.date_range_start.tzinfo is None or self.date_range_end.tzinfo is None:
            raise ValueError("Date ranges must be timezone-aware datetimes.")
        if self.date_range_end < self.date_range_start:
            raise ValueError("date_range_end cannot be before date_range_start.")
        if self.initial_capital <= 0:
            raise ValueError("initial_capital must be positive.")
