import unittest
from unittest.mock import patch, PropertyMock
import math
from datetime import datetime, timezone
import copy
from typing import List

from research.analytics.policies import SelectionPolicy, ValidationPolicy
from research.analytics.verdict import ScientificVerdict, Verdict
from research.analytics.evaluator import HypothesisEvaluator, NoEligibleExperimentError, InvalidEvaluationDataError
from research.analytics.report import ValidationReport
from research.analytics.metrics import ResearchResult
from research.engine.configuration import ExperimentConfiguration
from research.dataset.manifest import DatasetManifest
from research.dataset.partition import DatasetPartition, PartitionName
from research.orchestration.matrix import generate_experiment_id

def create_dummy_report(
    _dummy_id: str,
    partition: str,
    trades: int,
    pf: float,
    mdd: float = 0.10,
    wr: float = 0.50,
) -> ValidationReport:
    metrics = ResearchResult(
        start_timestamp="2020-01-01T00:00:00Z",
        end_timestamp="2020-02-01T00:00:00Z",
        initial_capital=100000.0,
        final_capital=105000.0,
        net_pnl=5000.0,
        gross_profit=10000.0,
        gross_loss=5000.0,
        number_of_trades=trades,
        winning_trades=trades // 2,
        losing_trades=trades // 2,
        win_rate=wr,
        average_win=100.0,
        average_loss=100.0,
        profit_factor=pf,
        maximum_drawdown=5000.0,
        maximum_drawdown_percentage=mdd,
        largest_win=500.0,
        largest_loss=500.0
    )
    
    config = ExperimentConfiguration(
        dataset_id="test_dataset",
        dataset_partition=partition,
        instrument="XAUUSD",
        timeframe="M1",
        date_range_start=datetime(2020, 1, 1, tzinfo=timezone.utc),
        date_range_end=datetime(2020, 2, 1, tzinfo=timezone.utc),
        strategy_id="test_strategy",
        strategy_version="1.0.0",
        strategy_parameters={"dummy_id": _dummy_id}
    )
    exp_id = generate_experiment_id(config)
    
    return ValidationReport(
        experiment_id=exp_id,
        dataset_id=config.dataset_id,
        dataset_partition=config.dataset_partition,
        instrument=config.instrument,
        timeframe=config.timeframe,
        date_range_start=config.date_range_start.isoformat(),
        date_range_end=config.date_range_end.isoformat(),
        strategy_id=config.strategy_id,
        strategy_version=config.strategy_version,
        strategy_parameters=config.strategy_parameters,
        execution_assumptions={"hypothesis_id": "hyp_test"},
        results=metrics
    )


class TestHypothesisEvaluator(unittest.TestCase):
    
    def setUp(self):
        self.selection_policy = SelectionPolicy(min_train_trades=30)
        self.validation_policy = ValidationPolicy(
            min_validation_trades=30,
            max_pf_degradation=0.30,
            max_win_rate_degradation=0.10,
            max_drawdown_degradation=0.10,
            min_validation_pf_when_train_inf=1.5
        )
        self.evaluator = HypothesisEvaluator(self.selection_policy, self.validation_policy)
        
        part_train = DatasetPartition(
            partition_name=PartitionName.TRAIN,
            start_timestamp=datetime(2020, 1, 1, tzinfo=timezone.utc),
            end_timestamp=datetime(2020, 2, 1, tzinfo=timezone.utc),
            source_uri="file1.csv"
        )
        part_val = DatasetPartition(
            partition_name=PartitionName.VALIDATION,
            start_timestamp=datetime(2020, 2, 1, tzinfo=timezone.utc),
            end_timestamp=datetime(2020, 3, 1, tzinfo=timezone.utc),
            source_uri="file2.csv"
        )
        self.manifest = DatasetManifest(
            dataset_id="test_dataset",
            instrument="XAUUSD",
            timeframe="M1",
            timezone="UTC",
            schema_version="1.0.0",
            partitions=[part_train, part_val]
        )
        # Fix F-3: Use properly scoped mock instead of permanently mutating the class
        patcher = patch.object(DatasetManifest, 'fingerprint', new_callable=PropertyMock, return_value="mock_fingerprint")
        self.addCleanup(patcher.stop)
        self.mock_fingerprint = patcher.start()

    # 1. Highest PF selected
    def test_selection_highest_pf(self):
        r1 = create_dummy_report("exp_1", "TRAIN", 50, 1.5)
        r2 = create_dummy_report("exp_2", "TRAIN", 50, 2.5)
        r3 = create_dummy_report("exp_3", "TRAIN", 50, 2.0)
        
        champion = self.evaluator.select_champion([r1, r2, r3])
        self.assertEqual(champion.strategy_parameters["dummy_id"], "exp_2")

    # 2. Minimum trade threshold enforced
    def test_selection_min_trades(self):
        r1 = create_dummy_report("exp_1", "TRAIN", 10, 3.0) # Too few trades, highest PF
        r2 = create_dummy_report("exp_2", "TRAIN", 50, 1.5) # Valid
        
        champion = self.evaluator.select_champion([r1, r2])
        self.assertEqual(champion.strategy_parameters["dummy_id"], "exp_2")

    # 3. MDD tie-breaker works
    def test_selection_mdd_tie_breaker(self):
        r1 = create_dummy_report("exp_1", "TRAIN", 50, 2.0, mdd=0.15)
        r2 = create_dummy_report("exp_2", "TRAIN", 50, 2.0, mdd=0.10) # Lower MDD wins
        r3 = create_dummy_report("exp_3", "TRAIN", 50, 2.0, mdd=0.20)
        
        champion = self.evaluator.select_champion([r1, r2, r3])
        self.assertEqual(champion.strategy_parameters["dummy_id"], "exp_2")

    # 4. Experiment ID tie-breaker works
    def test_selection_id_tie_breaker(self):
        # Equal PF and MDD
        r1 = create_dummy_report("exp_B", "TRAIN", 50, 2.0, mdd=0.10)
        r2 = create_dummy_report("exp_A", "TRAIN", 50, 2.0, mdd=0.10)
        
        expected_winner = r1 if r1.experiment_id < r2.experiment_id else r2
        champion = self.evaluator.select_champion([r1, r2])
        self.assertEqual(champion.strategy_parameters["dummy_id"], expected_winner.strategy_parameters["dummy_id"])

    # 5. No eligible configurations fails deterministically
    def test_selection_no_eligible(self):
        r1 = create_dummy_report("exp_1", "TRAIN", 10, 3.0)
        with self.assertRaisesRegex(NoEligibleExperimentError, "minimum requirement"):
            self.evaluator.select_champion([r1])
            
        with self.assertRaisesRegex(NoEligibleExperimentError, "Empty"):
            self.evaluator.select_champion([])

    # 6. NaN PF cannot win
    def test_selection_nan_pf(self):
        r1 = create_dummy_report("exp_1", "TRAIN", 50, float('nan'))
        r2 = create_dummy_report("exp_2", "TRAIN", 50, 1.2)
        
        champion = self.evaluator.select_champion([r1, r2])
        self.assertEqual(champion.strategy_parameters["dummy_id"], "exp_2")

    # 7. Inf PF behaves deterministically
    def test_selection_inf_pf(self):
        r1 = create_dummy_report("exp_1", "TRAIN", 50, 2.0)
        r2 = create_dummy_report("exp_2", "TRAIN", 50, float('inf')) # Should win
        
        champion = self.evaluator.select_champion([r1, r2])
        self.assertEqual(champion.strategy_parameters["dummy_id"], "exp_2")

    # 8. ACCEPT when all metrics are within bounds
    def test_oos_accept(self):
        t1 = create_dummy_report("exp_1", "TRAIN", 50, 2.0, mdd=0.10, wr=0.50)
        v1 = create_dummy_report("exp_1", "VALIDATION", 40, 1.8, mdd=0.15, wr=0.45)
        # PF deg = (2.0-1.8)/2.0 = 0.10 < 0.30
        # MDD deg = 0.15-0.10 = 0.05 < 0.10
        # WR deg = 0.50-0.45 = 0.05 < 0.10
        
        champion = self.evaluator.select_champion([t1])
        verdict = self.evaluator.evaluate_oos(champion, [t1], v1, self.manifest)
        self.assertEqual(verdict.verdict, Verdict.ACCEPTED)
        self.assertEqual(len(verdict.rejection_reasons), 0)

    # 9. REJECT when PF degradation exceeds threshold
    def test_oos_reject_pf(self):
        t1 = create_dummy_report("exp_1", "TRAIN", 50, 2.0, mdd=0.10, wr=0.50)
        v1 = create_dummy_report("exp_1", "VALIDATION", 40, 1.2, mdd=0.15, wr=0.45)
        # PF deg = (2.0-1.2)/2.0 = 0.40 > 0.30
        
        champion = self.evaluator.select_champion([t1])
        verdict = self.evaluator.evaluate_oos(champion, [t1], v1, self.manifest)
        self.assertEqual(verdict.verdict, Verdict.REJECTED)
        self.assertTrue(any("Profit Factor degradation" in r for r in verdict.rejection_reasons))

    # 10. REJECT when WR degradation exceeds threshold
    def test_oos_reject_wr(self):
        t1 = create_dummy_report("exp_1", "TRAIN", 50, 2.0, mdd=0.10, wr=0.50)
        v1 = create_dummy_report("exp_1", "VALIDATION", 40, 1.8, mdd=0.15, wr=0.35)
        # WR deg = 0.50-0.35 = 0.15 > 0.10
        
        champion = self.evaluator.select_champion([t1])
        verdict = self.evaluator.evaluate_oos(champion, [t1], v1, self.manifest)
        self.assertEqual(verdict.verdict, Verdict.REJECTED)
        self.assertTrue(any("Win Rate degradation" in r for r in verdict.rejection_reasons))

    # 11. REJECT when MDD exceeds threshold
    def test_oos_reject_mdd(self):
        t1 = create_dummy_report("exp_1", "TRAIN", 50, 2.0, mdd=0.10, wr=0.50)
        v1 = create_dummy_report("exp_1", "VALIDATION", 40, 1.8, mdd=0.25, wr=0.45)
        # MDD deg = 0.25-0.10 = 0.15 > 0.10
        
        champion = self.evaluator.select_champion([t1])
        verdict = self.evaluator.evaluate_oos(champion, [t1], v1, self.manifest)
        self.assertEqual(verdict.verdict, Verdict.REJECTED)
        self.assertTrue(any("Drawdown degradation" in r for r in verdict.rejection_reasons))

    # 12. REJECT when validation trade count is insufficient
    def test_oos_reject_val_trades(self):
        t1 = create_dummy_report("exp_1", "TRAIN", 50, 2.0)
        v1 = create_dummy_report("exp_1", "VALIDATION", 10, 2.0) # < 30
        
        champion = self.evaluator.select_champion([t1])
        verdict = self.evaluator.evaluate_oos(champion, [t1], v1, self.manifest)
        self.assertEqual(verdict.verdict, Verdict.REJECTED)
        self.assertTrue(any("Insufficient VALIDATION trades" in r for r in verdict.rejection_reasons))

    # 13. REJECT when validation has zero trades
    def test_oos_reject_zero_trades(self):
        t1 = create_dummy_report("exp_1", "TRAIN", 50, 2.0)
        v1 = create_dummy_report("exp_1", "VALIDATION", 0, float('nan'), mdd=float('nan'), wr=float('nan'))
        
        champion = self.evaluator.select_champion([t1])
        verdict = self.evaluator.evaluate_oos(champion, [t1], v1, self.manifest)
        self.assertEqual(verdict.verdict, Verdict.REJECTED)
        self.assertTrue(any("VALIDATION has zero trades" in r for r in verdict.rejection_reasons))

    # 14. ACCEPT when VALIDATION outperforms TRAIN
    def test_oos_accept_outperform(self):
        t1 = create_dummy_report("exp_1", "TRAIN", 50, 2.0, mdd=0.15, wr=0.50)
        v1 = create_dummy_report("exp_1", "VALIDATION", 50, 3.0, mdd=0.05, wr=0.70)
        
        champion = self.evaluator.select_champion([t1])
        verdict = self.evaluator.evaluate_oos(champion, [t1], v1, self.manifest)
        self.assertEqual(verdict.verdict, Verdict.ACCEPTED)

    # 15. TRAIN PF = Inf + VALIDATION PF = Inf → ACCEPT
    def test_oos_inf_inf(self):
        t1 = create_dummy_report("exp_1", "TRAIN", 50, float('inf'))
        v1 = create_dummy_report("exp_1", "VALIDATION", 50, float('inf'))
        
        champion = self.evaluator.select_champion([t1])
        verdict = self.evaluator.evaluate_oos(champion, [t1], v1, self.manifest)
        self.assertEqual(verdict.verdict, Verdict.ACCEPTED)

    # 16. TRAIN PF = Inf + VALIDATION PF >= fallback threshold → ACCEPT
    def test_oos_inf_valid(self):
        t1 = create_dummy_report("exp_1", "TRAIN", 50, float('inf'))
        v1 = create_dummy_report("exp_1", "VALIDATION", 50, 1.8) # >= 1.5
        
        champion = self.evaluator.select_champion([t1])
        verdict = self.evaluator.evaluate_oos(champion, [t1], v1, self.manifest)
        self.assertEqual(verdict.verdict, Verdict.ACCEPTED)

    # 17. TRAIN PF = Inf + VALIDATION PF below fallback → REJECT
    def test_oos_inf_reject(self):
        t1 = create_dummy_report("exp_1", "TRAIN", 50, float('inf'))
        v1 = create_dummy_report("exp_1", "VALIDATION", 50, 1.2) # < 1.5
        
        champion = self.evaluator.select_champion([t1])
        verdict = self.evaluator.evaluate_oos(champion, [t1], v1, self.manifest)
        self.assertEqual(verdict.verdict, Verdict.REJECTED)

    # 18. NaN validation metrics are handled explicitly
    def test_oos_val_nan(self):
        t1 = create_dummy_report("exp_1", "TRAIN", 50, 2.0)
        v1 = create_dummy_report("exp_1", "VALIDATION", 50, float('nan'))
        
        champion = self.evaluator.select_champion([t1])
        verdict = self.evaluator.evaluate_oos(champion, [t1], v1, self.manifest)
        self.assertEqual(verdict.verdict, Verdict.REJECTED)
        self.assertTrue(any("VALIDATION PF is NaN" in r for r in verdict.rejection_reasons))

    # 19. Identical inputs produce identical ScientificVerdict
    def test_determinism(self):
        t1 = create_dummy_report("exp_1", "TRAIN", 50, 2.0)
        v1 = create_dummy_report("exp_1", "VALIDATION", 50, 1.8)
        
        champion1 = self.evaluator.select_champion([t1])
        verdict1 = self.evaluator.evaluate_oos(champion1, [t1], v1, self.manifest)
        
        champion2 = self.evaluator.select_champion([t1])
        verdict2 = self.evaluator.evaluate_oos(champion2, [t1], v1, self.manifest)
        
        self.assertEqual(verdict1, verdict2)

    # 20. Report ordering does not affect champion selection
    def test_order_independence(self):
        r1 = create_dummy_report("exp_1", "TRAIN", 50, 1.5)
        r2 = create_dummy_report("exp_2", "TRAIN", 50, 2.5)
        
        champ_a = self.evaluator.select_champion([r1, r2])
        champ_b = self.evaluator.select_champion([r2, r1])
        self.assertEqual(champ_a.strategy_parameters["dummy_id"], "exp_2")
        self.assertEqual(champ_b.strategy_parameters["dummy_id"], "exp_2")

    # 21. select_champion() operates only on TRAIN reports.
    def test_select_only_train(self):
        v1 = create_dummy_report("exp_1", "VALIDATION", 50, 2.5)
        with self.assertRaisesRegex(InvalidEvaluationDataError, "TRAIN"):
            self.evaluator.select_champion([v1])

    # 23. Champion configuration passed to OOS execution is unchanged
    def test_champion_reconstruction(self):
        t1 = create_dummy_report("exp_1", "TRAIN", 50, 2.0)
        champion = self.evaluator.select_champion([t1])
        
        self.assertEqual(champion.strategy_parameters["dummy_id"], "exp_1")
        self.assertEqual(champion.strategy_id, "test_strategy")
        self.assertEqual(champion.dataset_partition, "TRAIN")
        # Ensure parameters are identical
        self.assertEqual(champion.strategy_parameters, t1.strategy_parameters)
        
    # 24. Resulting VALIDATION report is evaluated against the selected TRAIN champion
    def test_oos_requires_validation_partition(self):
        t1 = create_dummy_report("exp_1", "TRAIN", 50, 2.0)
        v_invalid = create_dummy_report("exp_1", "TEST", 50, 2.0)
        
        champion = self.evaluator.select_champion([t1])
        with self.assertRaisesRegex(InvalidEvaluationDataError, "VALIDATION partition"):
            self.evaluator.evaluate_oos(champion, [t1], v_invalid, self.manifest)
            
    def test_oos_requires_matching_train_champion(self):
        t1 = create_dummy_report("exp_1", "TRAIN", 50, 2.0)
        v1 = create_dummy_report("exp_2", "VALIDATION", 50, 2.0)
        
        # Mismatched experiment config
        fake_champ = ExperimentConfiguration(
            dataset_id="d1", dataset_partition="TRAIN", instrument="X", timeframe="M1",
            date_range_start=datetime(2020,1,1,tzinfo=timezone.utc), date_range_end=datetime(2020,2,1,tzinfo=timezone.utc),
            strategy_id="s1", strategy_version="1", strategy_parameters={}
        )
        with self.assertRaisesRegex(InvalidEvaluationDataError, "VALIDATION configuration does not match TRAIN champion configuration"):
            self.evaluator.evaluate_oos(fake_champ, [t1], v1, self.manifest)

    # F-1: Different strategy parameters
    def test_oos_reject_diff_params(self):
        t1 = create_dummy_report("exp_1", "TRAIN", 50, 2.0)
        v1 = create_dummy_report("exp_2", "VALIDATION", 50, 2.0)
        champion = self.evaluator.select_champion([t1])
        with self.assertRaisesRegex(InvalidEvaluationDataError, "VALIDATION configuration does not match"):
            self.evaluator.evaluate_oos(champion, [t1], v1, self.manifest)

    # F-1: Forged identity
    def test_oos_reject_forged_identity(self):
        t1 = create_dummy_report("exp_1", "TRAIN", 50, 2.0)
        v1 = create_dummy_report("exp_1", "VALIDATION", 50, 2.0)
        # Manually alter the experiment_id to forge it
        v1 = ValidationReport(
            experiment_id="forged_id",
            dataset_id=v1.dataset_id, dataset_partition=v1.dataset_partition,
            instrument=v1.instrument, timeframe=v1.timeframe,
            date_range_start=v1.date_range_start, date_range_end=v1.date_range_end,
            strategy_id=v1.strategy_id, strategy_version=v1.strategy_version,
            strategy_parameters=v1.strategy_parameters,
            execution_assumptions=v1.execution_assumptions,
            results=v1.results
        )
        champion = self.evaluator.select_champion([t1])
        with self.assertRaisesRegex(InvalidEvaluationDataError, "Forged VALIDATION identity"):
            self.evaluator.evaluate_oos(champion, [t1], v1, self.manifest)

    # F-2: FAILED validation execution
    def test_oos_reject_failed_execution(self):
        t1 = create_dummy_report("exp_1", "TRAIN", 50, 2.0)
        v1 = create_dummy_report("exp_1", "VALIDATION", 50, 2.0)
        # Modify execution assumptions
        v1.execution_assumptions["orchestration_status"] = "FAILED"
        champion = self.evaluator.select_champion([t1])
        verdict = self.evaluator.evaluate_oos(champion, [t1], v1, self.manifest)
        self.assertEqual(verdict.verdict, Verdict.REJECTED)
        self.assertTrue(any("execution failed" in r for r in verdict.rejection_reasons))

    # F-4: Verdict immutability
    def test_verdict_immutability(self):
        t1 = create_dummy_report("exp_1", "TRAIN", 50, 2.0)
        v1 = create_dummy_report("exp_1", "VALIDATION", 50, 2.0)
        champion = self.evaluator.select_champion([t1])
        verdict = self.evaluator.evaluate_oos(champion, [t1], v1, self.manifest)
        with self.assertRaises(TypeError):
            verdict.train_metrics["profit_factor"] = 999.0
        with self.assertRaises(AttributeError):
            verdict.rejection_reasons.append("TAMPERED")

    # F-5: Duplicate identities in TRAIN
    def test_selection_duplicate_identities(self):
        t1 = create_dummy_report("exp_1", "TRAIN", 50, 2.0)
        t2 = create_dummy_report("exp_1", "TRAIN", 50, 3.0) # Same ID!
        with self.assertRaisesRegex(InvalidEvaluationDataError, "Duplicate experiment identity"):
            self.evaluator.select_champion([t1, t2])
            
    def test_selection_duplicate_order_independence(self):
        t1 = create_dummy_report("exp_1", "TRAIN", 50, 2.0)
        t2 = create_dummy_report("exp_1", "TRAIN", 50, 3.0) # Same ID!
        with self.assertRaisesRegex(InvalidEvaluationDataError, "Duplicate experiment identity"):
            self.evaluator.select_champion([t2, t1])

    # F-6: Negative Profit Factor
    def test_oos_negative_pf(self):
        t1 = create_dummy_report("exp_1", "TRAIN", 50, 2.0)
        v1 = create_dummy_report("exp_1", "VALIDATION", 50, -1.0)
        champion = self.evaluator.select_champion([t1])
        verdict = self.evaluator.evaluate_oos(champion, [t1], v1, self.manifest)
        self.assertEqual(verdict.verdict, Verdict.REJECTED)
        self.assertTrue(any("negative" in r for r in verdict.rejection_reasons))

    # F-7: NaN Rejection reasons explicit
    def test_oos_nan_rejection_reasons(self):
        t1 = create_dummy_report("exp_1", "TRAIN", 50, 2.0)
        v1 = create_dummy_report("exp_1", "VALIDATION", 50, 2.0, wr=float('nan'))
        champion = self.evaluator.select_champion([t1])
        verdict = self.evaluator.evaluate_oos(champion, [t1], v1, self.manifest)
        self.assertEqual(verdict.verdict, Verdict.REJECTED)
        self.assertTrue(any("Win Rate is NaN" in r for r in verdict.rejection_reasons))
