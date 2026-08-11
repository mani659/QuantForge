import math
from datetime import datetime
from typing import List, Tuple

from research.analytics.report import ValidationReport
from research.engine.configuration import ExperimentConfiguration
from research.dataset.manifest import DatasetManifest
from research.dataset.partition import PartitionName

from .policies import SelectionPolicy, ValidationPolicy
from .verdict import ScientificVerdict, Verdict, MetricDegradation


class NoEligibleExperimentError(Exception):
    pass


class InvalidEvaluationDataError(Exception):
    pass


class HypothesisEvaluator:
    """
    Deterministic out-of-sample scientific evaluator.
    Maintains a strict boundary between TRAIN selection and VALIDATION execution.
    """
    
    EVALUATOR_VERSION = "1.0.0"

    def __init__(self, selection_policy: SelectionPolicy, validation_policy: ValidationPolicy):
        self.selection_policy = selection_policy
        self.validation_policy = validation_policy

    def select_champion(self, train_reports: List[ValidationReport]) -> ExperimentConfiguration:
        """
        Phase A: Deterministically select the single champion configuration from TRAIN evidence.
        """
        if not train_reports:
            raise NoEligibleExperimentError("Empty TRAIN report collection provided.")

        eligible_reports = []
        id_to_report = {}
        for report in train_reports:
            if report.dataset_partition != "TRAIN":
                raise InvalidEvaluationDataError("select_champion must only receive TRAIN reports.")
            if report.results.number_of_trades >= self.selection_policy.min_train_trades:
                pf = report.results.profit_factor
                if math.isnan(pf):
                    continue
                if pf < 0:
                    continue
                
                eid = report.experiment_id
                if eid in id_to_report:
                    raise InvalidEvaluationDataError(f"Duplicate experiment identity detected for {eid}")
                id_to_report[eid] = report
                
                eligible_reports.append(report)
                
        if not eligible_reports:
            raise NoEligibleExperimentError(f"No TRAIN report met the minimum requirement of {self.selection_policy.min_train_trades} trades.")

        # Primary: profit_factor DESC
        # Tie-breaker 1: maximum_drawdown_percentage ASC
        # Tie-breaker 2: experiment_id ASC
        
        champion_report = sorted(
            eligible_reports, 
            key=lambda r: (-r.results.profit_factor, r.results.maximum_drawdown_percentage, r.experiment_id)
        )[0]

        return self._reconstruct_configuration(champion_report)

    def evaluate_oos(
        self, 
        champion_config: ExperimentConfiguration, 
        train_reports: List[ValidationReport], 
        validation_report: ValidationReport, 
        dataset_manifest: DatasetManifest
    ) -> ScientificVerdict:
        """
        Phase B: Compare VALIDATION execution against the originally selected TRAIN champion.
        """
        if validation_report.dataset_partition != "VALIDATION":
            raise InvalidEvaluationDataError("validation_report must be from the VALIDATION partition.")

        from research.orchestration.matrix import generate_experiment_id
        from dataclasses import replace
        
        # F-1: Cryptographic configuration identity verification
        val_config = self._reconstruct_configuration(validation_report)
        expected_val_id = generate_experiment_id(val_config)
        if expected_val_id != validation_report.experiment_id:
            raise InvalidEvaluationDataError("Forged VALIDATION identity detected.")
            
        expected_val_config = replace(champion_config, dataset_partition="VALIDATION")
        if expected_val_config != val_config:
            raise InvalidEvaluationDataError("VALIDATION configuration does not match TRAIN champion configuration.")

        champion_id = generate_experiment_id(champion_config)
        train_report = next((r for r in train_reports if r.experiment_id == champion_id), None)
        if not train_report:
            raise InvalidEvaluationDataError("Champion configuration not found in provided TRAIN reports.")
            
        verdict_status = Verdict.ACCEPTED
        rejection_reasons = []
        degradation_calculations = {}
        
        # F-2: Failed VALIDATION execution
        if validation_report.execution_assumptions.get("orchestration_status") == "FAILED":
            verdict_status = Verdict.REJECTED
            rejection_reasons.append("Validation execution failed")

        # 1. Trade count checks
        train_trades = train_report.results.number_of_trades
        val_trades = validation_report.results.number_of_trades
        
        if val_trades < self.validation_policy.min_validation_trades:
            verdict_status = Verdict.REJECTED
            rejection_reasons.append(f"Insufficient VALIDATION trades: {val_trades} < {self.validation_policy.min_validation_trades}")
        if val_trades == 0:
            verdict_status = Verdict.REJECTED
            rejection_reasons.append("VALIDATION has zero trades.")

        # 2. Profit Factor
        train_pf = train_report.results.profit_factor
        val_pf = validation_report.results.profit_factor
        pf_deg_val = float('nan')
        pf_passed = False
        
        if math.isnan(train_pf):
             pf_passed = False
             rejection_reasons.append("TRAIN PF is NaN.")
        elif train_pf < 0:
             pf_passed = False
             rejection_reasons.append("TRAIN PF is negative.")
        elif math.isnan(val_pf):
             pf_passed = False
             rejection_reasons.append("VALIDATION PF is NaN.")
        elif val_pf < 0:
             pf_passed = False
             rejection_reasons.append("VALIDATION PF is negative.")
        elif math.isinf(train_pf):
            if math.isinf(val_pf) or val_pf >= self.validation_policy.min_validation_pf_when_train_inf:
                pf_passed = True
            else:
                pf_passed = False
                rejection_reasons.append(f"VALIDATION PF ({val_pf}) fell below fallback threshold ({self.validation_policy.min_validation_pf_when_train_inf}) when TRAIN PF was Inf.")
        else:
            if train_pf > 0:
                pf_deg_val = (train_pf - val_pf) / train_pf
                if pf_deg_val <= self.validation_policy.max_pf_degradation:
                    pf_passed = True
                else:
                    rejection_reasons.append(f"Profit Factor degradation ({pf_deg_val:.2%}) exceeded {self.validation_policy.max_pf_degradation:.2%}")
            else:
                # If TRAIN_PF <= 0, we require VALIDATION to also not be worse, but relative formula fails.
                # In standard metrics, PF is never negative, but 0 happens if gross_profit = 0.
                if val_pf >= train_pf:
                    pf_passed = True
                    pf_deg_val = 0.0
                else:
                    rejection_reasons.append("Profit Factor degraded from 0.")
                    
        degradation_calculations["profit_factor"] = MetricDegradation(
            train_value=train_pf,
            validation_value=val_pf,
            degradation=pf_deg_val,
            threshold=self.validation_policy.max_pf_degradation,
            passed=pf_passed
        )
        if not pf_passed:
            verdict_status = Verdict.REJECTED

        # 3. Win Rate
        train_wr = train_report.results.win_rate
        val_wr = validation_report.results.win_rate
        wr_deg_val = train_wr - val_wr
        wr_passed = False
        
        if math.isnan(train_wr):
             rejection_reasons.append("TRAIN Win Rate is NaN.")
        elif math.isnan(val_wr):
             rejection_reasons.append("VALIDATION Win Rate is NaN.")
        elif wr_deg_val <= self.validation_policy.max_win_rate_degradation:
            wr_passed = True
        else:
            rejection_reasons.append(f"Win Rate degradation ({wr_deg_val:.2f}) exceeded {self.validation_policy.max_win_rate_degradation:.2f}")

        degradation_calculations["win_rate"] = MetricDegradation(
            train_value=train_wr,
            validation_value=val_wr,
            degradation=wr_deg_val,
            threshold=self.validation_policy.max_win_rate_degradation,
            passed=wr_passed
        )
        if not wr_passed:
            verdict_status = Verdict.REJECTED

        # 4. Max Drawdown Percentage
        train_dd = train_report.results.maximum_drawdown_percentage
        val_dd = validation_report.results.maximum_drawdown_percentage
        dd_deg_val = val_dd - train_dd
        dd_passed = False
        
        if math.isnan(train_dd):
             rejection_reasons.append("TRAIN Max Drawdown is NaN.")
        elif math.isnan(val_dd):
             rejection_reasons.append("VALIDATION Max Drawdown is NaN.")
        elif dd_deg_val <= self.validation_policy.max_drawdown_degradation:
            dd_passed = True
        else:
            rejection_reasons.append(f"Drawdown degradation ({dd_deg_val:.2f}) exceeded {self.validation_policy.max_drawdown_degradation:.2f}")

        degradation_calculations["maximum_drawdown_percentage"] = MetricDegradation(
            train_value=train_dd,
            validation_value=val_dd,
            degradation=dd_deg_val,
            threshold=self.validation_policy.max_drawdown_degradation,
            passed=dd_passed
        )
        if not dd_passed:
            verdict_status = Verdict.REJECTED
            
        train_metrics = {
            "profit_factor": train_pf,
            "win_rate": train_wr,
            "maximum_drawdown_percentage": train_dd,
            "number_of_trades": train_trades
        }
        val_metrics = {
            "profit_factor": val_pf,
            "win_rate": val_wr,
            "maximum_drawdown_percentage": val_dd,
            "number_of_trades": val_trades
        }

        # Assuming hypothesis_id is passed down or inferred, we can use the dataset_id and strategy_id to construct one if missing.
        # But for exact V1, we'll use f"{champion_config.strategy_id}_{champion_config.dataset_id}" as hypothesis_id 
        # since hypothesis_id isn't in ValidationReport directly (it is in OrchestrationEngine but lost in translation unless it's in execution_assumptions).
        hypothesis_id = train_report.execution_assumptions.get("hypothesis_id", f"hyp_{champion_config.strategy_id}")

        return ScientificVerdict(
            hypothesis_id=hypothesis_id,
            dataset_fingerprint=dataset_manifest.fingerprint,
            train_partition_id=train_report.dataset_partition,
            validation_partition_id=validation_report.dataset_partition,
            selected_experiment_id=champion_id,
            validation_experiment_id=validation_report.experiment_id,
            train_metrics=train_metrics,
            validation_metrics=val_metrics,
            degradation_calculations=degradation_calculations,
            verdict=verdict_status,
            rejection_reasons=rejection_reasons,
            evaluator_version=self.EVALUATOR_VERSION
        )

    def _reconstruct_configuration(self, report: ValidationReport) -> ExperimentConfiguration:
        """
        Safely rebuilds the deterministic experiment configuration from an immutable ValidationReport.
        """
        assumptions = report.execution_assumptions
        initial_capital = assumptions.get("initial_capital", 100000.0)
        transaction_costs = assumptions.get("transaction_costs", {})

        return ExperimentConfiguration(
            dataset_id=report.dataset_id,
            dataset_partition=report.dataset_partition,
            instrument=report.instrument,
            timeframe=report.timeframe,
            date_range_start=datetime.fromisoformat(report.date_range_start),
            date_range_end=datetime.fromisoformat(report.date_range_end),
            strategy_id=report.strategy_id,
            strategy_version=report.strategy_version,
            strategy_parameters=dict(report.strategy_parameters),
            initial_capital=initial_capital,
            transaction_costs=dict(transaction_costs)
        )
