import hashlib
import json
import itertools
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, Any, List, Iterator, Callable, Optional

from research.engine.configuration import ExperimentConfiguration


@dataclass(frozen=True)
class HypothesisRecord:
    """
    Encapsulates the textual hypothesis, dataset scope, and the ExperimentMatrix definition.
    """
    hypothesis_id: str
    description: str
    dataset_id: str
    dataset_partition: str
    instrument: str
    timeframe: str
    date_range_start: datetime
    date_range_end: datetime
    strategy_id: str
    strategy_version: str
    
    # Base execution parameters that apply to all configs
    initial_capital: float = 100000.0
    transaction_costs: Dict[str, float] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.hypothesis_id or not isinstance(self.hypothesis_id, str):
            raise ValueError("hypothesis_id must be a non-empty string.")


class ExperimentMatrix:
    """
    Generates a deterministic list of ExperimentConfigurations based on a parameter matrix.
    """
    
    def __init__(self, parameter_space: Dict[str, List[Any]], filter_func: Optional[Callable[[Dict[str, Any]], bool]] = None):
        """
        Args:
            parameter_space: A dictionary mapping parameter names to lists of discrete values.
            filter_func: An optional function that takes a parameter dict and returns True if valid.
        """
        self.parameter_space = parameter_space
        self.filter_func = filter_func
        
    def generate(self, hypothesis: HypothesisRecord) -> Iterator[ExperimentConfiguration]:
        """
        Yields all valid configurations derived from the Cartesian product of the parameter space.
        """
        keys = sorted(self.parameter_space.keys())
        value_lists = [self.parameter_space[k] for k in keys]
        
        for combination in itertools.product(*value_lists):
            params = dict(zip(keys, combination))
            
            if self.filter_func and not self.filter_func(params):
                continue
                
            config = ExperimentConfiguration(
                dataset_id=hypothesis.dataset_id,
                dataset_partition=hypothesis.dataset_partition,
                instrument=hypothesis.instrument,
                timeframe=hypothesis.timeframe,
                date_range_start=hypothesis.date_range_start,
                date_range_end=hypothesis.date_range_end,
                strategy_id=hypothesis.strategy_id,
                strategy_version=hypothesis.strategy_version,
                strategy_parameters=params,
                initial_capital=hypothesis.initial_capital,
                transaction_costs=dict(hypothesis.transaction_costs),
                random_seed=self._generate_seed(params)
            )
            yield config

    @staticmethod
    def _generate_seed(params: Dict[str, Any]) -> int:
        """
        Generates a deterministic random seed based on the parameter dictionary.
        """
        param_str = json.dumps(params, sort_keys=True)
        digest = hashlib.sha256(param_str.encode("utf-8")).hexdigest()
        # Convert first 8 bytes of hex digest to an integer
        return int(digest[:16], 16)


def generate_experiment_id(config: ExperimentConfiguration) -> str:
    """
    Produces a deterministic experiment_id by content-hashing the configuration.
    """
    # Create a canonical representation
    canonical = {
        "dataset_id": config.dataset_id,
        "dataset_partition": config.dataset_partition,
        "instrument": config.instrument,
        "timeframe": config.timeframe,
        "date_range_start": config.date_range_start.astimezone(timezone.utc).isoformat(),
        "date_range_end": config.date_range_end.astimezone(timezone.utc).isoformat(),
        "strategy_id": config.strategy_id,
        "strategy_version": config.strategy_version,
        "strategy_parameters": config.strategy_parameters,
        "initial_capital": config.initial_capital,
        "transaction_costs": config.transaction_costs
    }
    
    try:
        canonical_json = json.dumps(canonical, sort_keys=True)
    except TypeError as e:
        raise ValueError(f"ExperimentConfiguration strategy_parameters contains non-serializable type. {e}")
        
    digest = hashlib.sha256(canonical_json.encode("utf-8")).hexdigest()
    return f"exp_{digest[:16]}"
