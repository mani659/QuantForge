class RiskError(Exception):
    """Base exception for risk errors."""
    pass

class InvalidRiskModel(RiskError):
    pass

class MissingDecision(RiskError):
    pass

class UnsupportedDecision(RiskError):
    pass

class RiskModelConstructionError(RiskError):
    pass

class MissingRiskModel(RiskError):
    pass

class UnsupportedRiskModel(RiskError):
    pass

class RiskPolicyConstructionError(RiskError):
    pass

class RiskPolicyNotFound(RiskError):
    pass

class DuplicateRiskPolicy(RiskError):
    pass

class InvalidRiskPolicy(RiskError):
    pass

class RiskRegistryConfigurationError(RiskError):
    pass

class InvalidRiskAssessment(RiskError):
    pass

class MissingRiskDecision(RiskError):
    pass

class InvalidAssessmentState(RiskError):
    pass

class PositionSizingError(RiskError):
    pass

class UnsupportedSizingMethod(RiskError):
    pass

class InvalidPositionSizer(RiskError):
    pass

class InvalidPositionSpecification(RiskError):
    pass

class InvalidSizingOutput(RiskError):
    pass

class PositionSpecificationConstructionError(RiskError):
    pass
