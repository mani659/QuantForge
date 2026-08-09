"""Research Lifecycle domain — Phase 8.1 Research Industrialization.

Public API for the immutable objects that represent research hypotheses
transitioning through the QuantForge scientific lifecycle:

    Research Idea → ResearchCandidate → StrategyManifest

This package lives outside the frozen BOE tree. It consumes the frozen
platform but does not modify it.
"""

from research.lifecycle.research_errors import (
    ResearchLifecycleError,
    InvalidResearchCandidateData,
    InvalidProvenanceData,
    InvalidStrategyManifestData,
    InvalidDeploymentOutcomeData,
    ManifestBuildError,
)
from research.lifecycle.research_candidate import ResearchCandidate
from research.lifecycle.provenance import Provenance
from research.lifecycle.strategy_manifest import StrategyManifest
from research.lifecycle.strategy_manifest_builder import StrategyManifestBuilder
from research.lifecycle.deployment_outcome import DeploymentOutcome
from research.lifecycle.outcome_appender import OutcomeAppender
from research.lifecycle.outcome_reader import OutcomeReader

__all__ = [
    "ResearchLifecycleError",
    "InvalidResearchCandidateData",
    "InvalidProvenanceData",
    "InvalidStrategyManifestData",
    "InvalidDeploymentOutcomeData",
    "ManifestBuildError",
    "ResearchCandidate",
    "Provenance",
    "StrategyManifest",
    "StrategyManifestBuilder",
    "DeploymentOutcome",
    "OutcomeAppender",
    "OutcomeReader",
]
