class ObserverError(Exception):
    """Base class for all exceptions raised by the Observer and Evidence framework."""
    pass

class EvidenceError(ObserverError):
    """Raised when there is an issue with constructing or validating Evidence."""
    pass

class TimelineCompatibilityError(ObserverError):
    """Raised when an Observer encounters an incompatible FrozenBehaviorTimeline."""
    pass

class PackageConstructionError(EvidenceError):
    """Base error for EvidencePackage construction failures."""
    pass

class DuplicateEvidenceTypeError(PackageConstructionError):
    """Raised when an EvidencePackage is provided with multiple Evidence of the same type."""
    pass

class MissingEvidenceError(PackageConstructionError):
    """Raised when an EvidencePackage is missing required evidence."""
    pass

class InvalidEvidenceError(PackageConstructionError):
    """Raised when an EvidencePackage receives improperly formatted or mismatched Evidence."""
    pass
