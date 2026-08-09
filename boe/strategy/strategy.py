from dataclasses import dataclass
from typing import FrozenSet
from boe.strategy.strategy_contract import StrategyContract
from boe.strategy.strategy_status import StrategyStatus
from boe.strategy.strategy_errors import InvalidStrategyComponentError

@dataclass(frozen=True)
class Strategy(StrategyContract):
    _strategy_id: str
    _name: str
    _version: str
    _validation_id: str
    _interpretation_model_id: str
    _decision_policy_id: str
    _risk_policy_id: str
    _supported_markets: FrozenSet[str]
    _status: StrategyStatus
    _created_at: float

    def __post_init__(self):
        if not self._strategy_id:
            raise InvalidStrategyComponentError("Strategy ID cannot be empty.")
        if not self._name:
            raise InvalidStrategyComponentError("Name cannot be empty.")
        if not self._version:
            raise InvalidStrategyComponentError("Version cannot be empty.")
        if not self._validation_id:
            raise InvalidStrategyComponentError("Validation ID cannot be empty.")
        if not self._interpretation_model_id:
            raise InvalidStrategyComponentError("Interpretation Model ID cannot be empty.")
        if not self._decision_policy_id:
            raise InvalidStrategyComponentError("Decision Policy ID cannot be empty.")
        if not self._risk_policy_id:
            raise InvalidStrategyComponentError("Risk Policy ID cannot be empty.")
        if not self._supported_markets:
            raise InvalidStrategyComponentError("Supported markets cannot be empty.")
        
        # Enforce frozenset for immutability
        if not isinstance(self._supported_markets, frozenset):
            object.__setattr__(self, '_supported_markets', frozenset(self._supported_markets))
            
        if not isinstance(self._status, StrategyStatus):
            raise InvalidStrategyComponentError("Status must be a StrategyStatus enum.")

    @property
    def strategy_id(self) -> str:
        return self._strategy_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def version(self) -> str:
        return self._version

    @property
    def validation_id(self) -> str:
        return self._validation_id

    @property
    def interpretation_model_id(self) -> str:
        return self._interpretation_model_id

    @property
    def decision_policy_id(self) -> str:
        return self._decision_policy_id

    @property
    def risk_policy_id(self) -> str:
        return self._risk_policy_id

    @property
    def supported_markets(self) -> FrozenSet[str]:
        return self._supported_markets

    @property
    def status(self) -> StrategyStatus:
        return self._status

    @property
    def created_at(self) -> float:
        return self._created_at
