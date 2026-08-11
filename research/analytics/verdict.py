from dataclasses import dataclass
from enum import Enum
from typing import Tuple, Mapping, Any
from types import MappingProxyType

class Verdict(Enum):
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"


@dataclass(frozen=True)
class MetricDegradation:
    """
    Immutable record of a single metric's degradation calculation.
    """
    train_value: float
    validation_value: float
    degradation: float
    threshold: float
    passed: bool


@dataclass(frozen=True)
class ScientificVerdict:
    """
    Deterministic, immutable outcome of a scientific hypothesis out-of-sample evaluation.
    """
    hypothesis_id: str
    dataset_fingerprint: str
    train_partition_id: str
    validation_partition_id: str
    selected_experiment_id: str
    validation_experiment_id: str
    
    train_metrics: Mapping[str, float]
    validation_metrics: Mapping[str, float]
    
    degradation_calculations: Mapping[str, MetricDegradation]
    
    verdict: Verdict
    rejection_reasons: Tuple[str, ...]
    
    evaluator_version: str

    def __post_init__(self):
        # Enforce deep immutability
        if not isinstance(self.train_metrics, MappingProxyType):
            object.__setattr__(self, 'train_metrics', MappingProxyType(dict(self.train_metrics)))
        if not isinstance(self.validation_metrics, MappingProxyType):
            object.__setattr__(self, 'validation_metrics', MappingProxyType(dict(self.validation_metrics)))
        if not isinstance(self.degradation_calculations, MappingProxyType):
            object.__setattr__(self, 'degradation_calculations', MappingProxyType(dict(self.degradation_calculations)))
        if not isinstance(self.rejection_reasons, tuple):
            object.__setattr__(self, 'rejection_reasons', tuple(self.rejection_reasons))
