import time
from datetime import datetime, timezone
from types import MappingProxyType

# 1. Imports
from research.lifecycle.strategy_manifest import StrategyManifest
from research.lifecycle.provenance import Provenance
from research.experiment_recorder import ExperimentRecorder
from research.lifecycle.outcome_appender import OutcomeAppender

from boe.deployment.bootstrap import (
    DeploymentRegistries,
    DeploymentDependencies,
    DeploymentConfiguration,
    DeploymentBootstrap
)

from boe.interpretation.registry import InterpretationRegistry
from boe.decision.registry import DecisionRegistry
from boe.risk.registry import RiskPolicyRegistry

from boe.interpretation.models import DefaultInterpretationModel
from boe.decision.policy import DefaultDecisionPolicy
from boe.risk.policy import DefaultRiskPolicy
from boe.risk.models import DefaultRiskModel
from boe.risk.position_sizer import PositionSizerContract, PositionSizingResult
from boe.profile.engine import BehaviourProfileEngine
from boe.behavior_detector_contract import BehaviorDetectorContract
from boe.strategy.strategy import Strategy
from boe.strategy.strategy_status import StrategyStatus

from boe.execution.engine import DefaultExecutionEngine
from boe.execution.contract import ExecutionConfig
from boe.execution.paper_adapter import PaperTradingAdapter, PaperTradingAdapterConfig

from operational_governance.operational_authorization import OperationalAuthorization
from operational_governance.authorizer import Authorizer
from operational_governance.deployment_registry import DeploymentRegistry

def main():
    print("QuantForge Paper Session")
    print("------------------------")

    # 1. Create a valid StrategyManifest
    provenance = Provenance(
        research_candidate_id="candidate_1",
        validation_id="val_1",
        experiment_id="exp_1",
        strategy_manifest_id="strat_1",
        created_timestamp=datetime.now(timezone.utc)
    )
    
    manifest = StrategyManifest(
        strategy_id="strat_1",
        behaviour_name="momentum_reversion",
        observer_ids=("obs_1",),
        interpretation_model_id="interp_1",
        decision_policy_id="dec_1",
        risk_policy_id="risk_1",
        deployment_profile="paper_run",
        manifest_version="1.0.0",
        provenance=provenance
    )

    # 2. Construct existing deployment dependencies
    from boe.behavior_observation import BehaviorObservation
    class StubDetector(BehaviorDetectorContract):
        @property
        def detector_id(self) -> str: return "stub_detector"
        @property
        def detector_version(self) -> str: return "1.0.0"
        
        def observe(self, env):
            return BehaviorObservation(
                schema_version="1.0.0",
                observation_id="obs_001",
                environment_id=env.environment_id,
                behavior_type="momentum_reversion",
                instrument=env.instrument,
                timeframe=env.timeframe,
                observed_at=env.observed_at,
                detector_id=self.detector_id,
                detector_version=self.detector_version
            )

    interp_model = DefaultInterpretationModel()
    interp_reg = InterpretationRegistry()
    interp_reg.register(interp_model)
    
    dec_policy = DefaultDecisionPolicy()
    dec_reg = DecisionRegistry()
    dec_reg.register(dec_policy)
    
    risk_policy = DefaultRiskPolicy()
    risk_reg = RiskPolicyRegistry()
    risk_reg.register(risk_policy)
    
    strategy = Strategy(
        _strategy_id="strat_1",
        _name="momentum_reversion",
        _version="1.0.0",
        _validation_id="val_1",
        _interpretation_model_id=interp_model.model_name,
        _decision_policy_id=dec_policy.policy_name,
        _risk_policy_id=risk_policy.policy_name,
        _supported_markets=frozenset(["EURUSD"]),
        _status=StrategyStatus.READY,
        _created_at=time.time()
    )
    
    registries = DeploymentRegistries(
        interpretation=interp_reg,
        decision=dec_reg,
        risk=risk_reg,
        strategies={"strat_1": strategy}
    )

    from boe.evidence.observer_contract import ObserverContract
    from boe.evidence.evidence import Evidence
    class StubObserver(ObserverContract):
        @property
        def name(self): return "obs_1"
        @property
        def version(self): return "1.0.0"
        def observe(self, timeline):
            return Evidence(
                evidence_id="ev_1",
                candidate_id=timeline.candidate_id,
                timeline_id=timeline.timeline_id,
                observer_name=self.name,
                observer_version=self.version,
                evidence_type="RECOIL",
                confidence=0.9,
                observed=True,
                evidence_labels=("Label_RECOIL",),
                metadata=MappingProxyType({}),
                timestamp=timeline.closed_timestamp
            )

    class StubPositionSizer(PositionSizerContract):
        def __init__(self):
            self.tick_count = 0
            # Sequence: Buy, Increase, Reduce, Reversal, Close
            self.exposures = [0.02, 0.04, 0.01, -0.02, 0.0]

        @property
        def sizer_name(self) -> str: return "StubSequenceSizer"

        def size_position(self, assessment, timestamp):
            exposure = self.exposures[self.tick_count] if self.tick_count < len(self.exposures) else 0.0
            self.tick_count += 1
            return PositionSizingResult(
                candidate_id="c_1",
                timeline_id=assessment.timeline_id,
                observation_id=assessment.observation_id,
                schema_version="1.0",
                risk_units=abs(exposure),
                exposure_fraction=exposure,
                position_size_multiplier=1.0,
                metadata=MappingProxyType({"sizer": self.sizer_name}),
                timestamp=timestamp
            )

    paper_adapter = PaperTradingAdapter(PaperTradingAdapterConfig(broker_name="paper_broker", metadata=MappingProxyType({})))

    dependencies = DeploymentDependencies(
        detector=StubDetector(),
        observers=(StubObserver(),),
        profile_engine=BehaviourProfileEngine(),
        risk_model=DefaultRiskModel(),
        position_sizer=StubPositionSizer(),
        execution_engine=DefaultExecutionEngine(
            config=ExecutionConfig(engine_name="default", metadata=MappingProxyType({})),
            adapter=paper_adapter
        )
    )

    config = DeploymentConfiguration(
        schema_version="1.0.0",
        market_adapter_source="paper_feed"
    )

    # 3. Authorize the deployment
    import os; temp_dir = "./test_outputs"; os.makedirs(temp_dir, exist_ok=True)
    registry = DeploymentRegistry(temp_dir)
    authorizer = Authorizer(registry)
    
    auth_record = OperationalAuthorization(
        strategy_manifest_id=manifest.strategy_id,
        deployment_identity=manifest.deployment_profile,
        operator_identity="admin_user",
        authorized_at=datetime.now(timezone.utc)
    )
    authorizer.authorize(auth_record)

    # 4. Bootstrap the pipeline
    pipeline = DeploymentBootstrap.create(
        strategy_id=manifest.strategy_id,
        config=config,
        registries=registries,
        dependencies=dependencies
    )

    # 5. Generate synthetic market input
    raw_ticks = [
        {"id": "t1", "instrument": "EURUSD", "timeframe": "M1", "timestamp": datetime(2026, 1, 1, 10, 0, tzinfo=timezone.utc), "close": 1.1000},
        {"id": "t2", "instrument": "EURUSD", "timeframe": "M1", "timestamp": datetime(2026, 1, 1, 10, 1, tzinfo=timezone.utc), "close": 1.1010},
        {"id": "t3", "instrument": "EURUSD", "timeframe": "M1", "timestamp": datetime(2026, 1, 1, 10, 2, tzinfo=timezone.utc), "close": 1.1020},
        {"id": "t4", "instrument": "EURUSD", "timeframe": "M1", "timestamp": datetime(2026, 1, 1, 10, 3, tzinfo=timezone.utc), "close": 1.1030},
        {"id": "t5", "instrument": "EURUSD", "timeframe": "M1", "timestamp": datetime(2026, 1, 1, 10, 4, tzinfo=timezone.utc), "close": 1.1040},
    ]

    # 6. Translate market data
    snapshots = [pipeline.market_adapter.translate(tick) for tick in raw_ticks]

    # 7. Run the existing PaperTradingRunner
    results = pipeline.runner.run(snapshots)

    # 8. Persist outcomes
    recorder = ExperimentRecorder(temp_dir)
    appender = OutcomeAppender(manifest, recorder)
    
    outcome_ids = []
    executions = 0
    
    for res in results:
        if res.error:
            print(f"Error on {res.snapshot_id}: {res.error}")
        if res.execution_result is not None:
            executions += 1
            outcome_id = appender.append(res.execution_result)
            outcome_ids.append(outcome_id)

    # Print summary
    print(f"Snapshots processed: {len(results)}")
    print(f"Executions: {executions}")
    print(f"Deployment outcomes: {len(outcome_ids)}")
    print(f"Final Balance: {paper_adapter.account.balance:.2f}")
    print(f"Final Equity: {paper_adapter.account.equity:.2f}")
    print(f"Final Realised PnL: {paper_adapter.account.realised_pnl:.2f}")
    print(f"Closed Positions: {len(paper_adapter.account.closed_positions)}")
    print(f"Open Positions: {len(paper_adapter.account.open_positions)}")
    
    print("\nOutcome IDs:")
    for oid in outcome_ids:
        print(f"- {oid}")

if __name__ == "__main__":
    main()
