from abc import ABC, abstractmethod
from typing import FrozenSet
from boe.strategy.strategy_status import StrategyStatus

class StrategyContract(ABC):
    """
    Contract defining an executable scientific model assembled from validated components.
    
    A Strategy MUST NEVER:
    - generate signals
    - execute trades
    - replay markets
    - calculate indicators
    - perform optimisation
    - perform validation
    """
    
    @property
    @abstractmethod
    def strategy_id(self) -> str:
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def version(self) -> str:
        pass
        
    @property
    @abstractmethod
    def validation_id(self) -> str:
        pass

    @property
    @abstractmethod
    def interpretation_model_id(self) -> str:
        pass

    @property
    @abstractmethod
    def decision_policy_id(self) -> str:
        pass
        
    @property
    @abstractmethod
    def risk_policy_id(self) -> str:
        pass
        
    @property
    @abstractmethod
    def supported_markets(self) -> FrozenSet[str]:
        pass

    @property
    @abstractmethod
    def status(self) -> StrategyStatus:
        pass

    @property
    @abstractmethod
    def created_at(self) -> float:
        pass
