from datetime import datetime
from dataclasses import replace

from research.analytics.verdict import ScientificVerdict, Verdict
from research.engine.configuration import ExperimentConfiguration
from research.lifecycle.research_candidate import ResearchCandidate
from research.lifecycle.strategy_manifest_builder import StrategyManifestBuilder
from research.orchestration.matrix import generate_experiment_id
from research.packaging.validated_package import ValidatedStrategyPackage


class RejectedHypothesisError(Exception):
    """Raised when attempting to package a rejected scientific hypothesis."""
    pass


class ProvenanceMismatchError(Exception):
    """Raised when the supplied configuration or candidate does not cryptographically match the verdict."""
    pass


class InvalidPackagingDataError(Exception):
    """Raised when packaging inputs are malformed or missing required scientific data."""
    pass


class StrategyPackager:
    """
    Gatekeeper that converts accepted scientific verdicts into immutable deployment packages.
    """

    def __init__(self, manifest_builder: StrategyManifestBuilder = None):
        self._builder = manifest_builder or StrategyManifestBuilder()

    def package(
        self,
        verdict: ScientificVerdict,
        configuration: ExperimentConfiguration,
        candidate: ResearchCandidate,
        observer_ids: list[str],
        interpretation_model_id: str,
        decision_policy_id: str,
        risk_policy_id: str,
        deployment_profile: str,
        strategy_id: str,
        manifest_version: str,
        provenance_timestamp: datetime,
    ) -> ValidatedStrategyPackage:
        """
        Validates provenance and returns a tamper-proof ValidatedStrategyPackage.
        """
        # 1. Acceptance Gate
        if verdict.verdict != Verdict.ACCEPTED:
            raise RejectedHypothesisError(
                f"Cannot package REJECTED verdict for hypothesis {verdict.hypothesis_id}"
            )

        # 2. Verdict consistency
        if not verdict.validation_experiment_id:
            raise InvalidPackagingDataError("ScientificVerdict is missing validation_experiment_id")

        if not verdict.selected_experiment_id:
            raise InvalidPackagingDataError("ScientificVerdict is missing selected_experiment_id")

        # 3. Candidate / Hypothesis alignment
        if verdict.hypothesis_id != candidate.hypothesis_id:
            raise ProvenanceMismatchError(
                f"Candidate hypothesis_id ({candidate.hypothesis_id}) does not match "
                f"Verdict hypothesis_id ({verdict.hypothesis_id})"
            )

        # 4. Validated Configuration Identity
        # Reproduce partition-normalized identity semantics (TRAIN vs VALIDATION)
        val_config = replace(configuration, dataset_partition="VALIDATION")
        expected_val_id = generate_experiment_id(val_config)

        if expected_val_id != verdict.validation_experiment_id:
            raise ProvenanceMismatchError(
                f"Supplied configuration generated validation identity {expected_val_id}, "
                f"but verdict requires {verdict.validation_experiment_id}"
            )

        # 5. Build Strategy Manifest
        try:
            manifest = (
                self._builder
                .with_candidate(candidate)
                .with_validation(
                    validation_id=verdict.validation_experiment_id, 
                    experiment_id=verdict.selected_experiment_id
                )
                .with_observers(observer_ids)
                .with_interpretation_model(interpretation_model_id)
                .with_decision_policy(decision_policy_id)
                .with_risk_policy(risk_policy_id)
                .with_deployment_profile(deployment_profile)
                .build(
                    strategy_id=strategy_id,
                    manifest_version=manifest_version,
                    provenance_timestamp=provenance_timestamp
                )
            )
        except Exception as e:
            # Wrap builder errors if needed, or just let them bubble
            raise InvalidPackagingDataError(f"Manifest construction failed: {str(e)}")

        # 6. Compute Package Fingerprint
        fingerprint = ValidatedStrategyPackage.compute_canonical_fingerprint(
            manifest=manifest,
            config=configuration,
            verdict=verdict
        )

        # 7. Construct ValidatedStrategyPackage
        return ValidatedStrategyPackage(
            strategy_manifest=manifest,
            configuration=configuration,
            scientific_verdict=verdict,
            package_fingerprint=fingerprint
        )
