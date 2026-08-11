from typing import Dict, Any

from boe.deployment.bootstrap import DeploymentDependencies
from boe.risk.position_sizer import DefaultPositionSizer, PositionSizerConfig
from boe.risk.models import DefaultRiskModel
from boe.profile.engine import BehaviourProfileEngine
from boe.execution.engine import DefaultExecutionEngine
from boe.execution.contract import ExecutionConfig

from assembly.admission.admission_errors import ConfigurationAdmissionError, DependencyAdmissionError


class DependencyFactory:
    """
    Strict factory that explicitly maps research parameters to genuine BOE dependencies.
    """
    
    @classmethod
    def validate_parameters(cls, parameters: Dict[str, Any]) -> None:
        """
        Validates the research parameters strictly against the known BOE runtime schema.
        Raises ConfigurationAdmissionError for missing, invalid, or unmapped parameters.
        """
        params = dict(parameters)
        
        # Position Sizer Configuration
        base_risk_fraction = params.pop("base_risk_fraction", None)
        max_position_multiplier = params.pop("max_position_multiplier", None)
        
        if base_risk_fraction is None:
            raise ConfigurationAdmissionError("Missing required parameter: base_risk_fraction")
        if max_position_multiplier is None:
            raise ConfigurationAdmissionError("Missing required parameter: max_position_multiplier")
            
        if not isinstance(base_risk_fraction, (int, float)):
            raise ConfigurationAdmissionError("Parameter base_risk_fraction must be numeric.")
        if not isinstance(max_position_multiplier, (int, float)):
            raise ConfigurationAdmissionError("Parameter max_position_multiplier must be numeric.")
            
        if base_risk_fraction < 0 or base_risk_fraction > 1:
            raise ConfigurationAdmissionError("Parameter base_risk_fraction must be between 0 and 1.")
        if max_position_multiplier < 0:
            raise ConfigurationAdmissionError("Parameter max_position_multiplier must be positive.")
            
        # If any parameters remain, they are unrecognized by BOE
        if params:
            raise ConfigurationAdmissionError(f"Unmapped or unknown runtime parameters: {list(params.keys())}")
            
    @classmethod
    def build(cls, parameters: Dict[str, Any]) -> DeploymentDependencies:
        """
        Constructs the deployment dependencies using the validated parameters.
        """
        # Always run validation first
        cls.validate_parameters(parameters)
        
        # Build genuine BOE components that exist
        sizer_config = PositionSizerConfig(
            base_risk_fraction=float(parameters["base_risk_fraction"]),
            max_position_multiplier=float(parameters["max_position_multiplier"])
        )
        position_sizer = DefaultPositionSizer(config=sizer_config)
        risk_model = DefaultRiskModel()
        profile_engine = BehaviourProfileEngine()
        
        # We explicitly throw DependencyAdmissionError because BOE lacks a genuine BehaviorDetectorContract 
        # and we are strictly prohibited from creating a fake one.
        raise DependencyAdmissionError(
            "Deployment admission blocked: No genuine implementation of BehaviorDetectorContract "
            "exists in the BOE layer. Cannot construct DeploymentDependencies."
        )
