import pytest
import tempfile
from pathlib import Path
from datetime import datetime

from operational_governance.operational_authorization import OperationalAuthorization
from operational_governance.deployment_registry import DeploymentRegistry


@pytest.fixture
def temp_storage():
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield Path(tmpdirname)


def create_mock_authorization(manifest_id="manifest_123"):
    return OperationalAuthorization(
        strategy_manifest_id=manifest_id,
        deployment_identity="deploy_prod_1",
        operator_identity="admin_ops",
        authorized_at=datetime.now(),
    )


def test_registry_append_and_read(temp_storage):
    """Verify a valid OperationalAuthorization can be appended and read back."""
    registry = DeploymentRegistry(temp_storage)
    auth = create_mock_authorization()
    
    registry.append(auth)
    
    records = registry.read_all()
    assert len(records) == 1
    
    retrieved = records[0]
    assert retrieved.strategy_manifest_id == auth.strategy_manifest_id
    assert retrieved.deployment_identity == auth.deployment_identity
    assert retrieved.operator_identity == auth.operator_identity
    assert retrieved.authorized_at == auth.authorized_at


def test_registry_multiple_records(temp_storage):
    """Verify multiple authorization records can coexist."""
    registry = DeploymentRegistry(temp_storage)
    
    auth1 = create_mock_authorization("manifest_1")
    auth2 = create_mock_authorization("manifest_2")
    
    registry.append(auth1)
    registry.append(auth2)
    
    records = registry.read_all()
    assert len(records) == 2
    
    manifest_ids = [r.strategy_manifest_id for r in records]
    assert "manifest_1" in manifest_ids
    assert "manifest_2" in manifest_ids


def test_registry_process_restart_persistence(temp_storage):
    """Verify records survive repository re-instantiation (simulating process reload)."""
    # Instance 1: write records
    registry1 = DeploymentRegistry(temp_storage)
    auth = create_mock_authorization("manifest_persistent")
    registry1.append(auth)
    
    # Instance 2: read records (re-instantiated on same directory)
    registry2 = DeploymentRegistry(temp_storage)
    records = registry2.read_all()
    
    assert len(records) == 1
    assert records[0].strategy_manifest_id == "manifest_persistent"


def test_registry_no_update_delete(temp_storage):
    """Verify there are no update or delete operations on the repository."""
    registry = DeploymentRegistry(temp_storage)
    
    assert not hasattr(registry, "update"), "Repository must not have an update operation"
    assert not hasattr(registry, "delete"), "Repository must not have a delete operation"
    assert not hasattr(registry, "remove"), "Repository must not have a remove operation"


def test_registry_rejects_invalid_records(temp_storage):
    """Verify invalid records are rejected."""
    registry = DeploymentRegistry(temp_storage)
    
    invalid_data = {
        "strategy_manifest_id": "manifest_123",
        "deployment_identity": "deploy_1",
    }
    
    with pytest.raises(ValueError, match="only append OperationalAuthorization"):
        registry.append(invalid_data)


def test_registry_immutability_of_returned_collection(temp_storage):
    """Verify the returned collection of records cannot be mutated to affect the repository."""
    registry = DeploymentRegistry(temp_storage)
    auth = create_mock_authorization()
    registry.append(auth)
    
    records = registry.read_all()
    assert isinstance(records, tuple), "Read result should be an immutable tuple"

