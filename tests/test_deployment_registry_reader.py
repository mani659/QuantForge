import pytest
import tempfile
from pathlib import Path
from datetime import datetime

from operational_governance.operational_authorization import OperationalAuthorization
from operational_governance.deployment_registry import DeploymentRegistry
from operational_governance.deployment_registry_reader import DeploymentRegistryReader


@pytest.fixture
def temp_storage():
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield Path(tmpdirname)


def create_mock_authorization(manifest_id="manifest_reader_1"):
    return OperationalAuthorization(
        strategy_manifest_id=manifest_id,
        deployment_identity="deploy_reader_1",
        operator_identity="reader_admin",
        authorized_at=datetime.now(),
    )


def test_reader_observes_existing_record(temp_storage):
    """Verify an existing OperationalAuthorization can be observed."""
    registry = DeploymentRegistry(temp_storage)
    auth = create_mock_authorization()
    registry.append(auth)
    
    reader = DeploymentRegistryReader(registry)
    records = reader.read_all()
    
    assert len(records) == 1
    assert records[0].strategy_manifest_id == "manifest_reader_1"


def test_reader_observes_multiple_records(temp_storage):
    """Verify multiple authorization records can be observed."""
    registry = DeploymentRegistry(temp_storage)
    registry.append(create_mock_authorization("manifest_A"))
    registry.append(create_mock_authorization("manifest_B"))
    
    reader = DeploymentRegistryReader(registry)
    records = reader.read_all()
    
    assert len(records) == 2
    manifest_ids = [r.strategy_manifest_id for r in records]
    assert "manifest_A" in manifest_ids
    assert "manifest_B" in manifest_ids


def test_reader_is_strictly_read_only(temp_storage):
    """Verify the reader does not expose append, update, delete, or remove methods."""
    registry = DeploymentRegistry(temp_storage)
    reader = DeploymentRegistryReader(registry)
    
    assert not hasattr(reader, "append"), "Reader must not have an append operation"
    assert not hasattr(reader, "update"), "Reader must not have an update operation"
    assert not hasattr(reader, "delete"), "Reader must not have a delete operation"
    assert not hasattr(reader, "remove"), "Reader must not have a remove operation"


def test_reader_returned_records_are_immutable(temp_storage):
    """Verify records returned by the reader are immutable tuples."""
    registry = DeploymentRegistry(temp_storage)
    registry.append(create_mock_authorization())
    
    reader = DeploymentRegistryReader(registry)
    records = reader.read_all()
    
    assert isinstance(records, tuple), "Returned records must be an immutable tuple"


def test_reader_does_not_modify_repository_state(temp_storage):
    """Verify persistence remains intact after reading and reading does not modify state."""
    registry = DeploymentRegistry(temp_storage)
    registry.append(create_mock_authorization())
    
    reader = DeploymentRegistryReader(registry)
    
    # Read once
    records_1 = reader.read_all()
    assert len(records_1) == 1
    
    # Read twice, should be exactly the same
    records_2 = reader.read_all()
    assert len(records_2) == 1
    
    # Verify underlying registry files are intact
    assert len(list(temp_storage.glob("auth_*.json"))) == 1

