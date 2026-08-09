from typing import Tuple

from operational_governance.operational_authorization import OperationalAuthorization
from operational_governance.deployment_registry import DeploymentRegistry


class DeploymentRegistryReader:
    """Read-only service for observing OperationalAuthorization records.
    
    This service forms the strict read-only observation boundary for Phase 9 
    Operational Governance. It returns immutable records from the 
    DeploymentRegistry without exposing any mutation paths (append, update, delete).
    """
    
    def __init__(self, registry: DeploymentRegistry):
        """Initializes the DeploymentRegistryReader.
        
        Args:
            registry: The immutable repository to read from.
        """
        self._registry = registry
        
    def read_all(self) -> Tuple[OperationalAuthorization, ...]:
        """Reads all persisted authorization records.
        
        Returns:
            Tuple[OperationalAuthorization, ...]: The collection of immutable authorization facts.
        """
        # Relies entirely on the DeploymentRegistry for data retrieval, 
        # avoiding any direct file storage bypass.
        return self._registry.read_all()

