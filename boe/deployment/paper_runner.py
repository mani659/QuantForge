"""
Paper Trading Runner
Executes the Deployment Orchestrator against a stream of EnvironmentSnapshots.
"""

from dataclasses import dataclass
from typing import Iterable, List, Optional

from boe.temporal.environment_snapshot import EnvironmentSnapshot
from boe.deployment.orchestrator import DeploymentOrchestrator
from boe.execution.contract import ExecutionEngineContract
from boe.execution.result import ExecutionResult


class PaperTradingRunnerError(Exception):
    """Base exception for Paper Trading Runner failures."""
    pass


@dataclass(frozen=True)
class RunnerResult:
    """
    Structured outcome of processing a single EnvironmentSnapshot.
    Contains the final ExecutionResult if a trade was executed, or an error if processing failed.
    """
    snapshot_id: str
    processed: bool
    execution_result: Optional[ExecutionResult] = None
    error: Optional[str] = None


class PaperTradingRunner:
    """
    Coordinates the execution of the Deployment Orchestrator over a stream
    of EnvironmentSnapshots, forwarding resulting PositionSpecifications
    to a Simulation Execution Adapter.
    """

    def __init__(
        self,
        orchestrator: DeploymentOrchestrator,
        execution_engine: ExecutionEngineContract
    ):
        if not isinstance(orchestrator, DeploymentOrchestrator):
            raise PaperTradingRunnerError("orchestrator must be a DeploymentOrchestrator")
        if not isinstance(execution_engine, ExecutionEngineContract):
            raise PaperTradingRunnerError("execution_engine must be an ExecutionEngineContract")

        self._orchestrator = orchestrator
        self._execution_engine = execution_engine

    def run(self, snapshots: Iterable[EnvironmentSnapshot]) -> List[RunnerResult]:
        """
        Sequentially process a stream of EnvironmentSnapshots.
        
        Args:
            snapshots: An iterable of immutable EnvironmentSnapshots representing a market feed.
            
        Returns:
            A list of RunnerResult objects describing the outcome of each snapshot.
            Failures inside a single snapshot are caught and recorded, preventing session crash.
        """
        results = []
        
        for snapshot in snapshots:
            if not isinstance(snapshot, EnvironmentSnapshot):
                results.append(RunnerResult(
                    snapshot_id="unknown",
                    processed=False,
                    error="Invalid input: expected EnvironmentSnapshot"
                ))
                continue
                
            try:
                # 0. Sync Market State to Simulation Execution Adapter
                adapter = getattr(self._execution_engine, "_adapter", None)
                if adapter and hasattr(adapter, "update_market_state"):
                    adapter.update_market_state(snapshot)

                # 1. Pipeline Execution
                spec = self._orchestrator.process_snapshot(snapshot)
                
                # 2. Market Execution (Simulation)
                if spec is not None:
                    exec_result = self._execution_engine.execute(spec)
                    results.append(RunnerResult(
                        snapshot_id=snapshot.snapshot_id,
                        processed=True,
                        execution_result=exec_result
                    ))
                else:
                    results.append(RunnerResult(
                        snapshot_id=snapshot.snapshot_id,
                        processed=True,
                        execution_result=None
                    ))
            except Exception as e:
                # 3. Deterministic Failure Handling
                results.append(RunnerResult(
                    snapshot_id=snapshot.snapshot_id,
                    processed=False,
                    error=str(e)
                ))
                
        return results
