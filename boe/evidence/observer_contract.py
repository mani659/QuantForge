from abc import ABC, abstractmethod

from boe.temporal.frozen_behavior_timeline import FrozenBehaviorTimeline
from boe.evidence.evidence import Evidence


class ObserverContract(ABC):
    """
    Abstract Base Class for all future Observers.
    
    Observers act as independent scientific instruments. They consume an 
    immutable FrozenBehaviorTimeline and produce immutable Evidence.
    They never know other observers exist and must not communicate outside 
    of their Evidence output.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the observer."""
        pass

    @property
    @abstractmethod
    def version(self) -> str:
        """Version of the observer (e.g. '1.0.0')."""
        pass

    @abstractmethod
    def observe(self, timeline: FrozenBehaviorTimeline) -> Evidence:
        """
        Analyze the given timeline and return an immutable Evidence object.
        """
        pass
