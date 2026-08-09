"""Deterministic error hierarchy for the Research Lifecycle domain.

Phase 8.1 — Research Industrialization.
These errors are raised only during construction validation of immutable
lifecycle objects. They contain no runtime state, execution context, or
broker information.
"""


class ResearchLifecycleError(Exception):
    """Base exception for the Research Lifecycle domain."""
    pass


class InvalidResearchCandidateData(ResearchLifecycleError):
    """Raised when a ResearchCandidate is instantiated with invalid data."""
    pass


class InvalidProvenanceData(ResearchLifecycleError):
    """Raised when a Provenance is instantiated with invalid data."""
    pass


class InvalidStrategyManifestData(ResearchLifecycleError):
    """Raised when a StrategyManifest is instantiated with invalid data."""
    pass


class InvalidDeploymentOutcomeData(ResearchLifecycleError):
    """Raised when a DeploymentOutcome is instantiated with invalid data."""
    pass


class ManifestBuildError(ResearchLifecycleError):
    """Raised when the StrategyManifestBuilder cannot produce a valid manifest."""
    pass
