class StrategyError(Exception):
    """Base class for strategy exceptions."""
    pass

class InvalidStrategyComponentError(StrategyError):
    """Raised when a Strategy component is invalid or missing."""
    pass

class InvalidStrategyLifecycleError(StrategyError):
    """Raised when a Strategy lifecycle transition is invalid."""
    pass
