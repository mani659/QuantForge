import json
import uuid
from pathlib import Path
from datetime import datetime
from typing import Tuple

from operational_governance.operational_authorization import OperationalAuthorization


class DeploymentRegistry:
    """Immutable repository for OperationalAuthorization records.
    
    Persists OperationalAuthorization facts durably.
    - Append-only storage.
    - No updates.
    - No deletion.
    - Read-only observation.
    """
    
    def __init__(self, storage_dir: str | Path):
        """Initializes the DeploymentRegistry.
        
        Args:
            storage_dir: The directory path where records will be persisted.
        """
        self.storage_dir = Path(storage_dir).resolve()
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        
    def append(self, authorization: OperationalAuthorization) -> str:
        """Appends a new authorization record to the registry.
        
        Args:
            authorization: The OperationalAuthorization fact to persist.
            
        Returns:
            str: A unique identifier for the stored record.
            
        Raises:
            ValueError: If the input is not an OperationalAuthorization instance.
        """
        if not isinstance(authorization, OperationalAuthorization):
            raise ValueError("DeploymentRegistry can only append OperationalAuthorization records.")
            
        # Using a UUID guarantees a new file is created for every append operation,
        # inherently enforcing append-only behavior at the filesystem level.
        record_id = f"auth_{uuid.uuid4().hex}"
        record_path = self.storage_dir / f"{record_id}.json"
        
        data = {
            "strategy_manifest_id": authorization.strategy_manifest_id,
            "deployment_identity": authorization.deployment_identity,
            "operator_identity": authorization.operator_identity,
            "authorized_at": authorization.authorized_at.isoformat(),
        }
        
        # Write exactly once.
        with open(record_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
            
        return record_id
        
    def read_all(self) -> Tuple[OperationalAuthorization, ...]:
        """Reads all persisted authorization records.
        
        Returns:
            Tuple[OperationalAuthorization, ...]: All stored records, deterministically.
        """
        records = []
        # Sort by filename to ensure deterministic read order
        for path in sorted(self.storage_dir.glob("auth_*.json")):
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                
            auth = OperationalAuthorization(
                strategy_manifest_id=data["strategy_manifest_id"],
                deployment_identity=data["deployment_identity"],
                operator_identity=data["operator_identity"],
                authorized_at=datetime.fromisoformat(data["authorized_at"]),
            )
            records.append(auth)
            
        return tuple(records)

