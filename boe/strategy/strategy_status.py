from enum import Enum, auto

class StrategyStatus(Enum):
    DRAFT = auto()
    READY = auto()
    PAPER = auto()
    DEMO = auto()
    LIVE = auto()
    RETIRED = auto()
