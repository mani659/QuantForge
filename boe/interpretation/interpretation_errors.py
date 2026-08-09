class InterpretationError(Exception):
    """Base exception for interpretation errors."""
    pass

class InvalidInterpretation(InterpretationError):
    pass

class MissingBehaviourProfile(InterpretationError):
    pass

class InterpretationConflict(InterpretationError):
    pass

class UnsupportedBehaviourProfile(InterpretationError):
    pass

class InterpretationConstructionError(InterpretationError):
    pass

class InterpretationModelNotFound(InterpretationError):
    pass

class DuplicateInterpretationModel(InterpretationError):
    pass

class InvalidInterpretationModel(InterpretationError):
    pass

class RegistryConfigurationError(InterpretationError):
    pass
