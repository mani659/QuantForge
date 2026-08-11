import unittest
from datetime import datetime, timezone
from dataclasses import replace
import copy

from research.packaging.validated_package import ValidatedStrategyPackage
from research.lifecycle.strategy_manifest import StrategyManifest
from research.lifecycle.provenance import Provenance
from research.engine.configuration import ExperimentConfiguration
from research.analytics.verdict import ScientificVerdict, Verdict
from research.orchestration.matrix import generate_experiment_id

from boe.deployment.bootstrap import DeploymentConfiguration, DeploymentRegistries
from boe.interpretation.registry import InterpretationRegistry
from boe.decision.registry import DecisionRegistry
from boe.risk.registry import RiskPolicyRegistry

from boe.interpretation.models import DefaultInterpretationModel
from boe.decision.policy import DefaultDecisionPolicy
from boe.risk.policy import DefaultRiskPolicy

from assembly.admission.admission_controller import AdmissionController
from assembly.admission.admission_errors import (
    PackageIntegrityError,
    ScientificAdmissionError,
    ConfigurationAdmissionError,
    ManifestAdmissionError,
    DependencyAdmissionError
)


def create_mock_registries() -> DeploymentRegistries:
    interp_reg = InterpretationRegistry()
    interp_model = DefaultInterpretationModel()
    interp_reg.register(interp_model)
    
    dec_reg = DecisionRegistry()
    dec_policy = DefaultDecisionPolicy()
    dec_reg.register(dec_policy)
    
    risk_reg = RiskPolicyRegistry()
    risk_policy = DefaultRiskPolicy()
    risk_reg.register(risk_policy)
    
    return DeploymentRegistries(
        interpretation=interp_reg,
        decision=dec_reg,
        risk=risk_reg,
        strategies={}
    )


def create_valid_package(
    parameters=None,
    verdict=Verdict.ACCEPTED,
    modify_fingerprint=False
) -> ValidatedStrategyPackage:
    if parameters is None:
        parameters = {
            "base_risk_fraction": 0.01,
            "max_position_multiplier": 1.0
        }
        
    config = ExperimentConfiguration(
        dataset_id="ds_1",
        dataset_partition="VALIDATION",
        instrument="EURUSD",
        timeframe="H1",
        date_range_start=datetime(2020, 1, 1, tzinfo=timezone.utc),
        date_range_end=datetime(2020, 12, 31, tzinfo=timezone.utc),
        strategy_id="strat_1",
        strategy_version="1.0.0",
        strategy_parameters=parameters,
        initial_capital=10000.0,
        transaction_costs={"spread": 0.0001}
    )
    
    # We must match identity to exactly "VALIDATION"
    canonical_id = generate_experiment_id(config)
    
    provenance = Provenance(
        research_candidate_id="rc_1",
        validation_id="val_1",
        experiment_id=canonical_id,
        strategy_manifest_id="sm_1",
        created_timestamp=datetime(2020, 1, 1, tzinfo=timezone.utc)
    )
    
    manifest = StrategyManifest(
        strategy_id="strat_1",
        behaviour_name="Test Behavior",
        observer_ids=("obs_1",),
        interpretation_model_id="DefaultInterpretationModel_v1.0",
        decision_policy_id="DefaultDecisionPolicy_v1.0",
        risk_policy_id="DefaultRiskPolicy_v1.0",
        deployment_profile="PAPER",
        manifest_version="1.0.0",
        provenance=provenance
    )
    
    scientific_verdict = ScientificVerdict(
        hypothesis_id="hyp_1",
        dataset_fingerprint="ds_fp",
        train_partition_id="TRAIN",
        validation_partition_id="VALIDATION",
        selected_experiment_id="exp_train",
        validation_experiment_id=canonical_id,
        train_metrics={"profit": 100},
        validation_metrics={"profit": 90},
        degradation_calculations={},
        verdict=verdict,
        rejection_reasons=(),
        evaluator_version="1.0"
    )
    
    fingerprint = ValidatedStrategyPackage.compute_canonical_fingerprint(
        manifest, config, scientific_verdict
    )
    
    if modify_fingerprint:
        fingerprint = "00000000000000000000000000000000"
        
    return ValidatedStrategyPackage(
        strategy_manifest=manifest,
        configuration=config,
        scientific_verdict=scientific_verdict,
        package_fingerprint=fingerprint
    )


class TestDeploymentAdmission(unittest.TestCase):
    def setUp(self):
        self.registries = create_mock_registries()
        self.config = DeploymentConfiguration(schema_version="1.0.0", market_adapter_source="feed_a")
        
    def test_happy_path_ends_in_dependency_error(self):
        # Due to BOE missing a genuine BehaviorDetectorContract, this will block bootstrap
        package = create_valid_package()
        
        with self.assertRaises(DependencyAdmissionError) as context:
            AdmissionController.admit(package, self.config, self.registries)
            
        self.assertIn("No genuine implementation of BehaviorDetectorContract", str(context.exception))
        
    def test_fingerprint_tampering(self):
        package = create_valid_package(modify_fingerprint=True)
        with self.assertRaises(PackageIntegrityError):
            AdmissionController.admit(package, self.config, self.registries)

    def test_parameter_tampering(self):
        package = create_valid_package()
        
        # Manually alter the parameter dict without recomputing fingerprint
        # ValidatedStrategyPackage freezes the config deeply, so we have to bypass it
        object.__setattr__(package.configuration, 'strategy_parameters', {"base_risk_fraction": 0.05})
        
        with self.assertRaises(PackageIntegrityError):
            AdmissionController.admit(package, self.config, self.registries)
            
    def test_scientific_rejection(self):
        package = create_valid_package(verdict=Verdict.REJECTED)
        with self.assertRaises(ScientificAdmissionError):
            AdmissionController.admit(package, self.config, self.registries)

    def test_missing_required_parameter(self):
        # Missing max_position_multiplier
        package = create_valid_package(parameters={"base_risk_fraction": 0.01})
        with self.assertRaises(ConfigurationAdmissionError) as ctx:
            AdmissionController.admit(package, self.config, self.registries)
        self.assertIn("Missing required parameter: max_position_multiplier", str(ctx.exception))

    def test_unknown_parameter(self):
        params = {
            "base_risk_fraction": 0.01,
            "max_position_multiplier": 1.0,
            "unknown_metric": 5
        }
        package = create_valid_package(parameters=params)
        with self.assertRaises(ConfigurationAdmissionError) as ctx:
            AdmissionController.admit(package, self.config, self.registries)
        self.assertIn("Unmapped or unknown runtime parameters", str(ctx.exception))

    def test_invalid_parameter_type(self):
        params = {
            "base_risk_fraction": "0.01",
            "max_position_multiplier": 1.0
        }
        package = create_valid_package(parameters=params)
        with self.assertRaises(ConfigurationAdmissionError):
            AdmissionController.admit(package, self.config, self.registries)

    def test_invalid_parameter_value(self):
        params = {
            "base_risk_fraction": 1.5, # > 1
            "max_position_multiplier": 1.0
        }
        package = create_valid_package(parameters=params)
        with self.assertRaises(ConfigurationAdmissionError):
            AdmissionController.admit(package, self.config, self.registries)

    def test_manifest_reference_failure(self):
        package = create_valid_package()
        
        # Tamper with the manifest to point to an invalid policy
        new_manifest = replace(package.strategy_manifest, decision_policy_id="UnknownPolicy")
        # Fix fingerprint to get past Gate 1
        fingerprint = ValidatedStrategyPackage.compute_canonical_fingerprint(
            new_manifest, package.configuration, package.scientific_verdict
        )
        package = ValidatedStrategyPackage(
            strategy_manifest=new_manifest,
            configuration=package.configuration,
            scientific_verdict=package.scientific_verdict,
            package_fingerprint=fingerprint
        )
        
        with self.assertRaises(ManifestAdmissionError):
            AdmissionController.admit(package, self.config, self.registries)

    def test_configuration_identity_mutation(self):
        package = create_valid_package()
        
        # Change something in configuration that changes its experiment ID, but recompute fingerprint
        # so Gate 1 passes, but Gate 3 (Configuration Identity) fails.
        new_config = replace(package.configuration, instrument="GBPUSD")
        fingerprint = ValidatedStrategyPackage.compute_canonical_fingerprint(
            package.strategy_manifest, new_config, package.scientific_verdict
        )
        package = ValidatedStrategyPackage(
            strategy_manifest=package.strategy_manifest,
            configuration=new_config,
            scientific_verdict=package.scientific_verdict,
            package_fingerprint=fingerprint
        )
        
        with self.assertRaises(ConfigurationAdmissionError) as ctx:
            AdmissionController.admit(package, self.config, self.registries)
        self.assertIn("Validated configuration identity mismatch", str(ctx.exception))

    def test_partition_normalization(self):
        # Simulate a package trained on TRAIN but correctly recording the VALIDATION ID in the verdict
        package = create_valid_package()
        
        train_config = replace(package.configuration, dataset_partition="TRAIN")
        fingerprint = ValidatedStrategyPackage.compute_canonical_fingerprint(
            package.strategy_manifest, train_config, package.scientific_verdict
        )
        package = ValidatedStrategyPackage(
            strategy_manifest=package.strategy_manifest,
            configuration=train_config,
            scientific_verdict=package.scientific_verdict,
            package_fingerprint=fingerprint
        )
        
        # Should still pass Gate 3, and only fail at Dependency construction
        with self.assertRaises(DependencyAdmissionError):
            AdmissionController.admit(package, self.config, self.registries)

    def test_determinism(self):
        package1 = create_valid_package()
        package2 = create_valid_package()
        
        # Both should fail deterministically with the same exception at the exact same gate
        with self.assertRaises(DependencyAdmissionError) as ctx1:
            AdmissionController.admit(package1, self.config, self.registries)
            
        with self.assertRaises(DependencyAdmissionError) as ctx2:
            AdmissionController.admit(package2, self.config, self.registries)
            
        self.assertEqual(str(ctx1.exception), str(ctx2.exception))


if __name__ == '__main__':
    unittest.main()
