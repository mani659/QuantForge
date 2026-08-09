import pytest
from unittest.mock import Mock, MagicMock
from types import MappingProxyType

from boe.strategy.strategy_contract import StrategyContract
from boe.interpretation.models import InterpretationModelContract
from boe.decision.policy import DecisionPolicyContract
from boe.risk.policy import RiskPolicyContract
from boe.execution.contract import ExecutionEngineContract, ExecutionConfig

from boe.interpretation.registry import InterpretationRegistry
from boe.decision.registry import DecisionRegistry
from boe.risk.registry import RiskPolicyRegistry
from boe.execution.registry import ExecutionRegistry
from boe.execution.execution_errors import ExecutionEngineNotFound, DuplicateExecutionEngine, ExecutionEngineConfigurationError

from boe.deployment.context import DeploymentContext, DeploymentConfigurationError
from boe.deployment.runtime import DeploymentRuntime
from boe.deployment.assembler import DeploymentAssembler


def test_execution_registry_registration():
    config = ExecutionConfig(engine_name="paper", metadata=MappingProxyType({}))
    mock_engine = MagicMock(spec=ExecutionEngineContract)
    mock_engine.config = config
    
    registry = ExecutionRegistry()
    registry.register(mock_engine)
    
    assert registry.has_engine("paper")
    assert registry.get_engine("paper") == mock_engine
    
    with pytest.raises(DuplicateExecutionEngine):
        registry.register(mock_engine)

def test_execution_registry_get_missing():
    registry = ExecutionRegistry()
    with pytest.raises(ExecutionEngineNotFound):
        registry.get_engine("missing")

def test_deployment_context_immutability_and_validation():
    mock_strategy = MagicMock(spec=StrategyContract)
    mock_interp = MagicMock(spec=InterpretationModelContract)
    mock_decision = MagicMock(spec=DecisionPolicyContract)
    mock_risk = MagicMock(spec=RiskPolicyContract)
    mock_exec = MagicMock(spec=ExecutionEngineContract)
    
    context = DeploymentContext(
        strategy_manifest=mock_strategy,
        interpretation_model=mock_interp,
        decision_policy=mock_decision,
        risk_policy=mock_risk
    )
    
    assert context.strategy_manifest == mock_strategy
    
    with pytest.raises(DeploymentConfigurationError):
        DeploymentContext(
            strategy_manifest=None,
            interpretation_model=mock_interp,
            decision_policy=mock_decision,
            risk_policy=mock_risk
        )

def test_deployment_assembler_deterministic_resolution():
    # Setup Mocks
    mock_strategy = MagicMock(spec=StrategyContract)
    mock_strategy.interpretation_model_id = "interp_1"
    mock_strategy.decision_policy_id = "dec_1"
    mock_strategy.risk_policy_id = "risk_1"
    mock_strategy.strategy_id = "strat_1"
    
    mock_interp = MagicMock(spec=InterpretationModelContract)
    mock_interp.model_name = "interp_1"
    
    mock_decision = MagicMock(spec=DecisionPolicyContract)
    mock_decision.policy_name = "dec_1"
    
    mock_risk = MagicMock(spec=RiskPolicyContract)
    mock_risk.policy_name = "risk_1"
    
    mock_exec = MagicMock(spec=ExecutionEngineContract)
    mock_exec.config = ExecutionConfig(engine_name="paper", metadata=MappingProxyType({}))
    
    # Setup Registries
    i_reg = InterpretationRegistry((mock_interp,))
    d_reg = DecisionRegistry((mock_decision,))
    r_reg = RiskPolicyRegistry((mock_risk,))
    
    assembler = DeploymentAssembler(i_reg, d_reg, r_reg)
    runtime = assembler.assemble(mock_strategy)
    
    assert isinstance(runtime, DeploymentRuntime)
    assert runtime.strategy_id == "strat_1"
    assert runtime.interpretation_model == mock_interp
    assert runtime.decision_policy == mock_decision
    assert runtime.risk_policy == mock_risk

def test_deployment_assembler_missing_registry_throws():
    mock_strategy = MagicMock(spec=StrategyContract)
    mock_strategy.interpretation_model_id = "interp_missing"
    mock_strategy.decision_policy_id = "dec_1"
    mock_strategy.risk_policy_id = "risk_1"
    
    i_reg = InterpretationRegistry()
    d_reg = DecisionRegistry()
    r_reg = RiskPolicyRegistry()
    
    assembler = DeploymentAssembler(i_reg, d_reg, r_reg)
    
    with pytest.raises(Exception):
        assembler.assemble(mock_strategy)
