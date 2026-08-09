from boe.deployment.context import DeploymentContext, DeploymentConfigurationError

class DeploymentRuntime:
    """
    Represents one deployable research runtime.
    Contains references only. Exposes the assembled scientific pipeline.
    Must not own portfolio, broker, MT5, event loop, scheduler, or market history.
    """
    def __init__(self, context: DeploymentContext):
        if not isinstance(context, DeploymentContext):
            raise DeploymentConfigurationError("context must be a DeploymentContext")
        self._context = context
        
    @property
    def context(self) -> DeploymentContext:
        """Returns the immutable DeploymentContext representing the configured pipeline."""
        return self._context

    @property
    def strategy_id(self) -> str:
        return self._context.strategy_manifest.strategy_id
        
    @property
    def interpretation_model(self):
        return self._context.interpretation_model
        
    @property
    def decision_policy(self):
        return self._context.decision_policy
        
    @property
    def risk_policy(self):
        return self._context.risk_policy
