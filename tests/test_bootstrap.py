"""Tests for the Deployment Bootstrap."""

import pytest
from unittest.mock import MagicMock

from boe.deployment.bootstrap import (
    DeploymentBootstrap,
    DeploymentBootstrapError,
    DeploymentConfiguration,
    DeploymentRegistries,
    DeploymentDependencies,
    DeployedPipeline
)
from boe.deployment.paper_runner import PaperTradingRunner
from boe.deployment.market_adapter import GenericMarketDataAdapter
from boe.strategy.strategy_contract import StrategyContract
from boe.interpretation.registry import InterpretationRegistry
from boe.decision.registry import DecisionRegistry
from boe.risk.registry import RiskPolicyRegistry
from boe.behavior_detector_contract import BehaviorDetectorContract
from boe.profile.engine import BehaviourProfileEngine
from boe.risk.models import RiskModelContract
from boe.risk.position_sizer import PositionSizerContract
from boe.execution.contract import ExecutionEngineContract
from boe.observation.observation_policy import DefaultObservationPolicy
from boe.observation.observation_config import ObservationConfig


@pytest.fixture
def mock_strategy():
    strategy = MagicMock(spec=StrategyContract)
    strategy.interpretation_model_id = "interp_1"
    strategy.decision_policy_id = "dec_1"
    strategy.risk_policy_id = "risk_1"
    return strategy


from boe.interpretation.models import InterpretationModelContract
from boe.decision.policy import DecisionPolicyContract
from boe.risk.policy import RiskPolicyContract

@pytest.fixture
def registries(mock_strategy):
    interp_model = MagicMock(spec=InterpretationModelContract)
    interp_reg = MagicMock(spec=InterpretationRegistry)
    interp_reg.get_model.return_value = interp_model
    
    dec_policy = MagicMock(spec=DecisionPolicyContract)
    dec_reg = MagicMock(spec=DecisionRegistry)
    dec_reg.get_policy.return_value = dec_policy
    
    risk_policy = MagicMock(spec=RiskPolicyContract)
    risk_reg = MagicMock(spec=RiskPolicyRegistry)
    risk_reg.get_policy.return_value = risk_policy
    
    return DeploymentRegistries(
        interpretation=interp_reg,
        decision=dec_reg,
        risk=risk_reg,
        strategies={"strat_1": mock_strategy}
    )


@pytest.fixture
def dependencies():
    return DeploymentDependencies(
        detector=MagicMock(spec=BehaviorDetectorContract),
        observers=(),
        profile_engine=MagicMock(spec=BehaviourProfileEngine),
        risk_model=MagicMock(spec=RiskModelContract),
        position_sizer=MagicMock(spec=PositionSizerContract),
        execution_engine=MagicMock(spec=ExecutionEngineContract),
        observation_policy=DefaultObservationPolicy(ObservationConfig("1.0.0", 5, 3600.0))
    )


def test_successful_bootstrap(registries, dependencies):
    """Test fully initializing a deployment pipeline."""
    config = DeploymentConfiguration(schema_version="1.0.0", market_adapter_source="feed_a")
    
    pipeline = DeploymentBootstrap.create(
        strategy_id="strat_1",
        config=config,
        registries=registries,
        dependencies=dependencies
    )
    
    assert isinstance(pipeline, DeployedPipeline)
    assert isinstance(pipeline.market_adapter, GenericMarketDataAdapter)
    assert isinstance(pipeline.runner, PaperTradingRunner)
    
    # Assert configuration was applied correctly to the adapter
    assert pipeline.market_adapter.schema_version == "1.0.0"
    assert pipeline.market_adapter.source == "feed_a"


def test_missing_strategy(registries, dependencies):
    """Test bootstrap fails gracefully when the strategy is missing."""
    config = DeploymentConfiguration()
    
    with pytest.raises(DeploymentBootstrapError, match="not found in provided strategies registry"):
        DeploymentBootstrap.create(
            strategy_id="unknown_strat",
            config=config,
            registries=registries,
            dependencies=dependencies
        )


def test_invalid_types_rejected(registries, dependencies):
    """Test bootstrap enforces strict input types."""
    config = DeploymentConfiguration()
    
    with pytest.raises(DeploymentBootstrapError, match="strategy_id must be a string"):
        DeploymentBootstrap.create(
            strategy_id=123,  # type: ignore
            config=config,
            registries=registries,
            dependencies=dependencies
        )
        
    with pytest.raises(DeploymentBootstrapError, match="config must be a DeploymentConfiguration"):
        DeploymentBootstrap.create(
            strategy_id="strat_1",
            config="bad config",  # type: ignore
            registries=registries,
            dependencies=dependencies
        )
        
    with pytest.raises(DeploymentBootstrapError, match="registries must be a DeploymentRegistries"):
        DeploymentBootstrap.create(
            strategy_id="strat_1",
            config=config,
            registries={"missing": "types"},  # type: ignore
            dependencies=dependencies
        )
        
    with pytest.raises(DeploymentBootstrapError, match="dependencies must be a DeploymentDependencies"):
        DeploymentBootstrap.create(
            strategy_id="strat_1",
            config=config,
            registries=registries,
            dependencies=None  # type: ignore
        )


def test_assembly_failure_handling(registries, dependencies):
    """Test bootstrap wraps inner assembly failures cleanly."""
    config = DeploymentConfiguration()
    
    # Force the assembler to fail by making the interpretation registry throw
    registries.interpretation.get_model.side_effect = Exception("Registry offline")
    
    with pytest.raises(DeploymentBootstrapError, match="Bootstrap assembly failed"):
        DeploymentBootstrap.create(
            strategy_id="strat_1",
            config=config,
            registries=registries,
            dependencies=dependencies
        )
