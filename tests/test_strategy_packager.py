import unittest
from datetime import datetime, timezone
import json
import hashlib
from dataclasses import replace

from research.analytics.verdict import ScientificVerdict, Verdict
from research.engine.configuration import ExperimentConfiguration
from research.lifecycle.research_candidate import ResearchCandidate
from research.orchestration.matrix import generate_experiment_id

from research.packaging.strategy_packager import (
    StrategyPackager,
    RejectedHypothesisError,
    ProvenanceMismatchError,
    InvalidPackagingDataError
)
from research.packaging.validated_package import ValidatedStrategyPackage


def _make_candidate(**overrides) -> ResearchCandidate:
    defaults = dict(
        candidate_id="RC-001",
        hypothesis_id="HYP-001",
        research_name="Mean Reversion Recoil",
        behaviour_name="recoil_after_displacement",
        description="Test hypothesis",
        creation_timestamp=datetime(2026, 8, 1, 12, 0, 0),
        research_version="1.0.0",
        assumptions=("Assumption 1",),
        success_criteria=("Success 1",),
        metadata=(("author", "Researcher A"),),
    )
    defaults.update(overrides)
    return ResearchCandidate(**defaults)

def _make_config(**overrides) -> ExperimentConfiguration:
    defaults = dict(
        dataset_id="ds_001",
        dataset_partition="TRAIN",
        instrument="XAUUSD",
        timeframe="M5",
        date_range_start=datetime(2020, 1, 1, tzinfo=timezone.utc),
        date_range_end=datetime(2021, 1, 1, tzinfo=timezone.utc),
        strategy_id="strat_001",
        strategy_version="1.0.0",
        strategy_parameters={"fast_ma": 10, "slow_ma": 50},
        initial_capital=100000.0,
        transaction_costs={"spread": 0.0001}
    )
    defaults.update(overrides)
    return ExperimentConfiguration(**defaults)

def _make_verdict(config: ExperimentConfiguration, **overrides) -> ScientificVerdict:
    val_config = replace(config, dataset_partition="VALIDATION")
    val_id = generate_experiment_id(val_config)
    train_id = generate_experiment_id(config)
    
    defaults = dict(
        hypothesis_id="HYP-001",
        dataset_fingerprint="fp_123",
        train_partition_id="TRAIN",
        validation_partition_id="VALIDATION",
        selected_experiment_id=train_id,
        validation_experiment_id=val_id,
        train_metrics={"profit_factor": 1.5},
        validation_metrics={"profit_factor": 1.4},
        degradation_calculations={},
        verdict=Verdict.ACCEPTED,
        rejection_reasons=(),
        evaluator_version="1.0.0"
    )
    defaults.update(overrides)
    return ScientificVerdict(**defaults)


class TestStrategyPackager(unittest.TestCase):

    def setUp(self):
        self.packager = StrategyPackager()
        self.candidate = _make_candidate()
        self.config = _make_config()
        self.verdict = _make_verdict(self.config)
        
        self.package_args = dict(
            verdict=self.verdict,
            configuration=self.config,
            candidate=self.candidate,
            observer_ids=["obs_1"],
            interpretation_model_id="interp_1",
            decision_policy_id="dec_1",
            risk_policy_id="risk_1",
            deployment_profile="paper",
            strategy_id="final_strat_001",
            manifest_version="1.0.0",
            provenance_timestamp=datetime(2026, 8, 1, 12, 0, 0)
        )

    # Test 1 — Happy path
    def test_happy_path(self):
        package = self.packager.package(**self.package_args)
        
        self.assertIsInstance(package, ValidatedStrategyPackage)
        self.assertIsNotNone(package.package_fingerprint)
        self.assertEqual(package.strategy_manifest.strategy_id, "final_strat_001")
        self.assertEqual(package.strategy_manifest.manifest_version, "1.0.0")
        
        # Verify the underlying configuration identity was preserved
        self.assertEqual(
            package.configuration.strategy_parameters["fast_ma"], 
            10
        )
        # Deep freeze test
        with self.assertRaises(TypeError):
            package.configuration.strategy_parameters["fast_ma"] = 20

        self.assertTrue(package.verify_fingerprint())

    # Test 2 — Rejected hypothesis
    def test_rejected_hypothesis_fails(self):
        rejected_verdict = replace(self.verdict, verdict=Verdict.REJECTED)
        self.package_args["verdict"] = rejected_verdict
        
        with self.assertRaises(RejectedHypothesisError):
            self.packager.package(**self.package_args)

    # Test 3 — Configuration tampering
    def test_configuration_tampering_fails(self):
        # Tamper with the parameter
        tampered_config = replace(
            self.config, 
            strategy_parameters={"fast_ma": 20, "slow_ma": 50}
        )
        self.package_args["configuration"] = tampered_config
        
        with self.assertRaises(ProvenanceMismatchError):
            self.packager.package(**self.package_args)

    # Test 4 — Validation identity mismatch
    def test_validation_identity_mismatch_fails(self):
        # Supply a verdict with a mismatched validation_experiment_id
        tampered_verdict = replace(self.verdict, validation_experiment_id="exp_forged")
        self.package_args["verdict"] = tampered_verdict
        
        with self.assertRaises(ProvenanceMismatchError):
            self.packager.package(**self.package_args)

    # Test 5 — Strategy identity mismatch
    def test_strategy_identity_mismatch_fails(self):
        # Configuration has one strategy_id, but the verdict assumes another?
        # Well, verdict just takes validation_experiment_id. If the config strategy_id changes,
        # it alters the generated validation_experiment_id, which fails Test 3.
        # Let's test that directly:
        tampered_config = replace(self.config, strategy_id="strat_002")
        self.package_args["configuration"] = tampered_config
        
        with self.assertRaises(ProvenanceMismatchError):
            self.packager.package(**self.package_args)

    # Test 6 — Dataset identity mismatch
    def test_dataset_identity_mismatch_fails(self):
        tampered_config = replace(self.config, dataset_id="ds_002")
        self.package_args["configuration"] = tampered_config
        
        with self.assertRaises(ProvenanceMismatchError):
            self.packager.package(**self.package_args)

    # Test 7 — Determinism
    def test_determinism(self):
        package1 = self.packager.package(**self.package_args)
        package2 = self.packager.package(**self.package_args)
        
        self.assertEqual(package1.package_fingerprint, package2.package_fingerprint)
        self.assertEqual(
            package1.strategy_manifest.provenance.strategy_manifest_id, 
            package2.strategy_manifest.provenance.strategy_manifest_id
        )

    # Test 8 — Dictionary ordering
    def test_dictionary_ordering_determinism(self):
        # Create a config with differently ordered dict
        params_ordered_1 = {"fast_ma": 10, "slow_ma": 50}
        params_ordered_2 = {"slow_ma": 50, "fast_ma": 10}
        
        config1 = replace(self.config, strategy_parameters=params_ordered_1)
        config2 = replace(self.config, strategy_parameters=params_ordered_2)
        
        args1 = dict(self.package_args, configuration=config1)
        args2 = dict(self.package_args, configuration=config2)
        
        pack1 = self.packager.package(**args1)
        pack2 = self.packager.package(**args2)
        
        self.assertEqual(pack1.package_fingerprint, pack2.package_fingerprint)

    # Test 9 — Mutation resistance
    def test_mutation_resistance(self):
        package = self.packager.package(**self.package_args)
        
        with self.assertRaises(TypeError):
            package.configuration.strategy_parameters["fast_ma"] = 99
            
        with self.assertRaises(TypeError):
            package.scientific_verdict.train_metrics["profit_factor"] = 99.0
            
        with self.assertRaises(AttributeError):
            # Tuples don't have append
            package.scientific_verdict.rejection_reasons.append("x")

    # Test 10 — Fingerprint tampering
    def test_fingerprint_tampering_detection(self):
        package = self.packager.package(**self.package_args)
        self.assertTrue(package.verify_fingerprint())
        
        # Tamper the fingerprint
        object.__setattr__(package, 'package_fingerprint', "deadbeef")
        self.assertFalse(package.verify_fingerprint())

    # Test 11 — Candidate mismatch
    def test_candidate_mismatch(self):
        tampered_candidate = replace(self.candidate, hypothesis_id="HYP-999")
        self.package_args["candidate"] = tampered_candidate
        
        with self.assertRaises(ProvenanceMismatchError):
            self.packager.package(**self.package_args)

    # Test 12 — Missing provenance
    def test_missing_provenance(self):
        tampered_verdict = replace(self.verdict, validation_experiment_id="")
        self.package_args["verdict"] = tampered_verdict
        
        with self.assertRaises(InvalidPackagingDataError):
            self.packager.package(**self.package_args)

        tampered_verdict2 = replace(self.verdict, selected_experiment_id="")
        self.package_args["verdict"] = tampered_verdict2
        
        with self.assertRaises(InvalidPackagingDataError):
            self.packager.package(**self.package_args)


if __name__ == '__main__':
    unittest.main()
