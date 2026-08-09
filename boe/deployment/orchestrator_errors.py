class DeploymentOrchestratorError(Exception):
    """Base exception for all DeploymentOrchestrator failures."""
    pass

class PipelineExecutionError(DeploymentOrchestratorError):
    """Raised when a component in the BOE pipeline fails during execution."""
    pass
