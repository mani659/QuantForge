from dataclasses import dataclass

@dataclass(frozen=True)
class SelectionPolicy:
    """
    Immutable deterministic policy for selecting a champion configuration from TRAIN evidence.
    """
    min_train_trades: int = 30


@dataclass(frozen=True)
class ValidationPolicy:
    """
    Immutable deterministic mathematical bounds for out-of-sample degradation.
    """
    min_validation_trades: int = 30
    max_pf_degradation: float = 0.30
    max_win_rate_degradation: float = 0.10
    max_drawdown_degradation: float = 0.30
    min_validation_pf_when_train_inf: float = 1.5

    def __post_init__(self):
        if self.min_validation_trades <= 0:
            raise ValueError("Minimum trade thresholds must be positive.")
        if self.min_validation_pf_when_train_inf <= 1.0:
            raise ValueError("min_validation_pf_when_train_inf must be greater than 1.0.")
