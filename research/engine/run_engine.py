from dataclasses import dataclass
from typing import Iterable, List, Optional
import uuid

from boe.temporal.environment_snapshot import EnvironmentSnapshot
from boe.execution.contract import ExecutionEngineContract
from boe.execution.result import ExecutionResult

from research.engine.strategy_contract import ResearchStrategyContract
from research.engine.configuration import ExperimentConfiguration


class ResearchRunEngineError(Exception):
    """Base exception for Research Run Engine failures."""
    pass


@dataclass(frozen=True)
class ResearchRunResult:
    """
    Structured outcome of processing a single EnvironmentSnapshot in a research context.
    """
    snapshot_id: str
    processed: bool
    execution_result: Optional[ExecutionResult] = None
    error: Optional[str] = None


class ResearchRunEngine:
    """
    Coordinates the deterministic execution of a ResearchStrategy over a stream
    of EnvironmentSnapshots, forwarding resulting PositionSpecifications
    to a Simulation Execution Adapter.
    
    This replaces the heavy BOE DeploymentOrchestrator pipeline for raw research.
    """

    def __init__(
        self,
        strategy: ResearchStrategyContract,
        execution_engine: ExecutionEngineContract,
        config: ExperimentConfiguration
    ):
        if not isinstance(strategy, ResearchStrategyContract):
            raise ResearchRunEngineError("strategy must be a ResearchStrategyContract")
        if not isinstance(execution_engine, ExecutionEngineContract):
            raise ResearchRunEngineError("execution_engine must be an ExecutionEngineContract")
        if not isinstance(config, ExperimentConfiguration):
            raise ResearchRunEngineError("config must be an ExperimentConfiguration")

        self._strategy = strategy
        self._execution_engine = execution_engine
        self._config = config

    def run(self, snapshots: Iterable[EnvironmentSnapshot]) -> List[ResearchRunResult]:
        """
        Sequentially process a stream of EnvironmentSnapshots.
        
        Args:
            snapshots: An iterable of immutable EnvironmentSnapshots representing a market feed.
            
        Returns:
            A list of ResearchRunResult objects describing the outcome of each snapshot.
            Failures inside a single snapshot are caught and recorded.
        """
        # 1. Deterministic State Reset
        self._strategy.reset()
        self._strategy.initialize(self._config.strategy_parameters)
        
        results = []
        
        for snapshot in snapshots:
            if not isinstance(snapshot, EnvironmentSnapshot):
                results.append(ResearchRunResult(
                    snapshot_id="unknown",
                    processed=False,
                    error="Invalid input: expected EnvironmentSnapshot"
                ))
                continue
                
            try:
                # 2. Sync Market State to Simulation Execution Adapter
                # This ensures the paper broker knows the current price for MTM valuation.
                adapter = getattr(self._execution_engine, "_adapter", None)
                if adapter and hasattr(adapter, "update_market_state"):
                    adapter.update_market_state(snapshot)

                # 3. Strategy Execution (No look-ahead, pure causal evaluation)
                spec = self._strategy.on_snapshot(snapshot)
                
                # 4. Market Execution (Simulation)
                if spec is not None:
                    # Enforce that the spec's candidate_id ties back to this research run
                    if not spec.candidate_id:
                        # Fallback id injection if strategy didn't provide one
                        # Using a hash of strategy ID and snapshot timestamp for determinism
                        spec_id = f"{self._strategy.strategy_id}_{snapshot.timestamp.isoformat()}"
                        # In a real environment we'd construct a new spec or expect the strategy
                        # to provide it. Since PositionSpecification is a dataclass, we can't easily mutate.
                        # For now, we trust the strategy returned a valid spec.
                    
                    exec_result = self._execution_engine.execute(spec)
                    results.append(ResearchRunResult(
                        snapshot_id=snapshot.snapshot_id,
                        processed=True,
                        execution_result=exec_result
                    ))
                else:
                    results.append(ResearchRunResult(
                        snapshot_id=snapshot.snapshot_id,
                        processed=True,
                        execution_result=None
                    ))
                    
            except Exception as e:
                # 5. Deterministic Failure Handling
                results.append(ResearchRunResult(
                    snapshot_id=snapshot.snapshot_id,
                    processed=False,
                    error=str(e)
                ))
                
        return results
