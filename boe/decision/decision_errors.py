class DecisionError(Exception):
    """Base exception for decision errors."""
    pass

class InvalidDecision(DecisionError):
    pass

class MissingInterpretation(DecisionError):
    pass

class DecisionConflict(DecisionError):
    pass

class UnsupportedInterpretation(DecisionError):
    pass

class DecisionConstructionError(DecisionError):
    pass

class DecisionPolicyNotFound(DecisionError):
    pass

class DuplicateDecisionPolicy(DecisionError):
    pass

class InvalidDecisionPolicy(DecisionError):
    pass

class RegistryConfigurationError(DecisionError):
    pass
