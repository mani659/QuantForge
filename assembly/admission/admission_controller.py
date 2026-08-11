from dataclasses import replace

from research.packaging.validated_package import ValidatedStrategyPackage
from research.analytics.verdict import Verdict
from research.orchestration.matrix import generate_experiment_id

from boe.strategy.strategy import Strategy
from boe.strategy.strategy_status import StrategyStatus
from boe.deployment.bootstrap import DeploymentBootstrap, DeploymentConfiguration, DeploymentRegistries, DeployedPipeline

from assembly.admission.admission_errors import (
    PackageIntegrityError,
    ScientificAdmissionError,
    ConfigurationAdmissionError,
    ManifestAdmissionError
)
from assembly.admission.dependency_factory import DependencyFactory


class AdmissionController:
    """
    Strict architectural boundary ensuring that only scientifically accepted,
    cryptographically intact ValidatedStrategyPackages can be deployed.
    """

    @staticmethod
    def admit(
        package: ValidatedStrategyPackage,
        config: DeploymentConfiguration,
        registries: DeploymentRegistries
    ) -> DeployedPipeline:
        
        # GATE 1: Package Integrity
        if not package.verify_fingerprint():
            raise PackageIntegrityError("Package cryptographic fingerprint verification failed.")
            
        # GATE 2: Scientific Acceptance
        if getattr(package.scientific_verdict, "verdict", None) != Verdict.ACCEPTED:
            raise ScientificAdmissionError(
                f"Scientific verdict must be ACCEPTED, got: {getattr(package.scientific_verdict, 'verdict', 'None')}"
            )
            
        # GATE 3: Validated Configuration Identity
        # Normalize partition to VALIDATION as per V1 research identity rules
        validation_config = replace(package.configuration, dataset_partition="VALIDATION")
        canonical_id = generate_experiment_id(validation_config)
        
        if canonical_id != package.scientific_verdict.validation_experiment_id:
            raise ConfigurationAdmissionError("Validated configuration identity mismatch. The package configuration does not match the scientific verdict.")
            
        # GATE 4: Parameter Validation
        DependencyFactory.validate_parameters(package.configuration.strategy_parameters)
        
        # GATE 5: Manifest Translation
        manifest = package.strategy_manifest
        
        # Verify registries explicitly to prevent ManifestAdmissionError bypassing BOE
        try:
            interp_model = registries.interpretation.get_model(manifest.interpretation_model_id)
            if not interp_model:
                raise ManifestAdmissionError(f"Interpretation model {manifest.interpretation_model_id} not found in registry.")
                
            dec_policy = registries.decision.get_policy(manifest.decision_policy_id)
            if not dec_policy:
                raise ManifestAdmissionError(f"Decision policy {manifest.decision_policy_id} not found in registry.")
                
            risk_policy = registries.risk.get_policy(manifest.risk_policy_id)
            if not risk_policy:
                raise ManifestAdmissionError(f"Risk policy {manifest.risk_policy_id} not found in registry.")
                
            # Note: observer validation would go here if BOE registries had an observer registry,
            # but observers are passed via DeploymentDependencies. We check the tuple length later.
            if not manifest.observer_ids:
                raise ManifestAdmissionError("Manifest must specify at least one observer.")
        except Exception as e:
            if isinstance(e, ManifestAdmissionError):
                raise
            raise ManifestAdmissionError(f"Manifest references missing registry components: {str(e)}") from e

        try:
            strategy_contract = Strategy(
                _strategy_id=manifest.strategy_id,
                _name=manifest.behaviour_name,
                _version=manifest.manifest_version,
                _validation_id=manifest.provenance.validation_id,
                _interpretation_model_id=manifest.interpretation_model_id,
                _decision_policy_id=manifest.decision_policy_id,
                _risk_policy_id=manifest.risk_policy_id,
                _supported_markets=frozenset([package.configuration.instrument]),
                _status=StrategyStatus.READY,
                _created_at=0.0  # Deterministic timestamp for translation
            )
        except Exception as e:
            raise ManifestAdmissionError(f"Failed to translate StrategyManifest to StrategyContract: {str(e)}") from e

        # Ensure the Strategy is injected into the strategies registry for Bootstrap to find
        # We create a new registry container to preserve determinism and immutability
        new_registries = DeploymentRegistries(
            interpretation=registries.interpretation,
            decision=registries.decision,
            risk=registries.risk,
            strategies={manifest.strategy_id: strategy_contract}
        )

        # GATE 6: Dependency Construction
        dependencies = DependencyFactory.build(package.configuration.strategy_parameters)
        
        # BOOTSTRAP
        return DeploymentBootstrap.create(
            strategy_id=manifest.strategy_id,
            config=config,
            registries=new_registries,
            dependencies=dependencies
        )
