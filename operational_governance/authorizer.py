from operational_governance.operational_authorization import OperationalAuthorization
from operational_governance.deployment_registry import DeploymentRegistry


class Authorizer:
    """Service to append OperationalAuthorization records to the DeploymentRegistry.
    
    This service is the strictly defined append-only write path for Phase 9 
    Operational Governance. It performs no analysis, validation, scoring, or 
    lifecycle transitions.
    """
    
    def __init__(self, registry: DeploymentRegistry):
        """Initializes the Authorizer with a DeploymentRegistry.
        
        Args:
            registry: The immutable repository for operational authorizations.
        """
        self._registry = registry
        
    def authorize(self, authorization: OperationalAuthorization) -> str:
        """Appends the authorization fact to the registry.
        
        Args:
            authorization: The immutable operational authorization fact.
            
        Returns:
            str: The unique record identifier returned by the registry.
            
        Raises:
            ValueError: If the input is not an OperationalAuthorization.
        """
        if not isinstance(authorization, OperationalAuthorization):
            raise ValueError("Authorizer can only process OperationalAuthorization records.")
            
        return self._registry.append(authorization)

