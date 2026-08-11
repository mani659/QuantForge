import os

class AdmissionError(Exception):
    """Base class for all Deployment Admission errors."""
    pass

class PackageIntegrityError(AdmissionError):
    """Raised when the ValidatedStrategyPackage fails cryptographic fingerprint validation."""
    pass

class ScientificAdmissionError(AdmissionError):
    """Raised when the package's ScientificVerdict is not ACCEPTED."""
    pass

class ConfigurationAdmissionError(AdmissionError):
    """Raised when the validated configuration identity is tampered with, or when explicit parameter mappings fail due to missing/unknown/invalid keys."""
    pass

class ManifestAdmissionError(AdmissionError):
    """Raised when the StrategyManifest fails translation to a StrategyContract."""
    pass

class DependencyAdmissionError(AdmissionError):
    """Raised when a required BOE runtime dependency does not have a genuine implementation or cannot be constructed."""
    pass
