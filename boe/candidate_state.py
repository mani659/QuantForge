"""Frozen lifecycle states for Behavioral Observation Engine candidates."""

from enum import Enum


class CandidateState(str, Enum):
    """The complete and closed lifecycle of a behavioral hypothesis."""

    NEW = "NEW"
    OBSERVING = "OBSERVING"
    VALIDATING = "VALIDATING"
    QUALIFIED = "QUALIFIED"
    EXECUTED = "EXECUTED"
    REJECTED = "REJECTED"
    EXPIRED = "EXPIRED"
