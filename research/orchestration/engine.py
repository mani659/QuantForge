from typing import List, Callable, Iterable
from boe.deployment.historical_adapter import HistoricalMarketAdapter
from boe.execution.contract import ExecutionEngineContract
from boe.temporal.environment_snapshot import EnvironmentSnapshot

from research.engine.strategy_contract import ResearchStrategyContract
from research.engine.configuration import ExperimentConfiguration
from research.engine.run_engine import ResearchRunEngine
from research.analytics.metrics import MetricsCalculator, ResearchResult
from research.analytics.report import ValidationReport

from research.orchestration.matrix import HypothesisRecord, ExperimentMatrix, generate_experiment_id


class OrchestrationEngine:
    """
    Executes an ExperimentMatrix sequentially, ensuring strict state isolation 
    and failure containment between runs.
    """
    
    def __init__(
        self,
        market_adapter_factory: Callable[[ExperimentConfiguration], Iterable[EnvironmentSnapshot]],
        strategy_factory: Callable[[str], ResearchStrategyContract],
        execution_engine_factory: Callable[[], ExecutionEngineContract]
    ):
        """
        Factories are required because every run MUST have completely fresh instances
        to prevent state leakage.
        """
        self.market_adapter_factory = market_adapter_factory
        self.strategy_factory = strategy_factory
        self.execution_engine_factory = execution_engine_factory

    def run_hypothesis(self, hypothesis: HypothesisRecord, matrix: ExperimentMatrix) -> List[ValidationReport]:
        """
        Generates and executes all configurations for the given hypothesis.
        Structurally enforces that matrix sweeps can only run on TRAIN partitions.
        """
        if hypothesis.dataset_partition != "TRAIN":
            raise ValueError(f"Orchestration sweeps are strictly isolated to the TRAIN partition. Attempted: {hypothesis.dataset_partition}")
            
        reports = []
        
        for config in matrix.generate(hypothesis):
            report = self._run_single_config(config)
            reports.append(report)
            
        return reports

    def run_out_of_sample(self, config: ExperimentConfiguration) -> ValidationReport:
        """
        Executes a single explicitly provided configuration, typically for out-of-sample validation.
        This bypasses the matrix sweep to prevent parameter selection on unseen data.
        """
        if config.dataset_partition not in ("VALIDATION", "TEST"):
            raise ValueError(f"run_out_of_sample requires a VALIDATION or TEST partition. Attempted: {config.dataset_partition}")
            
        return self._run_single_config(config)

    def _run_single_config(self, config: ExperimentConfiguration) -> ValidationReport:
        experiment_id = generate_experiment_id(config)
        
        try:
            # 1. Fresh instantiation for strict isolation
            snapshots = self.market_adapter_factory(config)
            strategy = self.strategy_factory(config.strategy_id)
            exec_engine = self.execution_engine_factory()
            
            # 2. Run Engine
            run_engine = ResearchRunEngine(
                strategy=strategy,
                execution_engine=exec_engine,
                config=config
            )
            
            # 3. Execution
            results = run_engine.run(snapshots)
            
            # Extract successful executions and check for errors
            successful_executions = []
            errors = []
            for r in results:
                if r.error:
                    errors.append(r.error)
                elif r.execution_result is not None and r.processed:
                    successful_executions.append(r.execution_result)
                    
            if errors:
                # M6: Calculate partial metrics on snapshot failure
                partial_metrics = MetricsCalculator.calculate(successful_executions, config.initial_capital)
                return self._build_report(config, partial_metrics, experiment_id=experiment_id, status="FAILED", error="; ".join(errors))
            
            # 4. Metrics
            metrics = MetricsCalculator.calculate(successful_executions, config.initial_capital)
            
            return self._build_report(config, metrics, experiment_id=experiment_id)
            
        except Exception as e:
            # Isolation Policy: If a single run fails entirely, we record the failure and continue orchestration.
            # We construct a zeroed result to represent the failure mathematically.
            failure_metrics = MetricsCalculator._empty_result(config.initial_capital)
            # In a real environment, we'd log the exception `e` or attach it to the report.
            return self._build_report(config, failure_metrics, experiment_id=experiment_id, status="FAILED", error=str(e))
            
    def _build_report(self, config: ExperimentConfiguration, metrics: ResearchResult, experiment_id: str, status: str = "SUCCESS", error: str = "") -> ValidationReport:
        # We subclass or augment ValidationReport if we want to store status/error.
        # For now, we return it as is, and attach error info into execution assumptions or a similar field if needed.
        # Let's add status and error to execution_assumptions for tracking without mutating the frozen ValidationReport class contract.
        
        assumptions = {
            "initial_capital": config.initial_capital,
            "transaction_costs": config.transaction_costs,
            "orchestration_status": status
        }
        if error:
            assumptions["orchestration_error"] = error
            
        return ValidationReport(
            experiment_id=experiment_id,
            dataset_id=config.dataset_id,
            dataset_partition=config.dataset_partition,
            instrument=config.instrument,
            timeframe=config.timeframe,
            date_range_start=config.date_range_start.isoformat(),
            date_range_end=config.date_range_end.isoformat(),
            strategy_id=config.strategy_id,
            strategy_version=config.strategy_version,
            strategy_parameters=config.strategy_parameters,
            execution_assumptions=assumptions,
            results=metrics
        )
