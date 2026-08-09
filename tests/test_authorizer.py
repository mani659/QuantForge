import pytest
import tempfile
from pathlib import Path
from datetime import datetime

from operational_governance.operational_authorization import OperationalAuthorization
from operational_governance.deployment_registry import DeploymentRegistry
from operational_governance.authorizer import Authorizer


@pytest.fixture
def temp_storage():
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield Path(tmpdirname)


def create_mock_authorization():
    return OperationalAuthorization(
        strategy_manifest_id="manifest_auth",
        deployment_identity="deploy_auth_1",
        operator_identity="auth_admin",
        authorized_at=datetime.now(),
    )


def test_authorizer_appends_valid_record(temp_storage):
    """Verify a valid OperationalAuthorization is appended and retrievable."""
    registry = DeploymentRegistry(temp_storage)
    authorizer = Authorizer(registry)
    
    auth = create_mock_authorization()
    record_id = authorizer.authorize(auth)
    
    assert isinstance(record_id, str)
    
    records = registry.read_all()
    assert len(records) == 1
    assert records[0].strategy_manifest_id == "manifest_auth"


def test_authorizer_rejects_invalid_input(temp_storage):
    """Verify invalid input is rejected without appending."""
    registry = DeploymentRegistry(temp_storage)
    authorizer = Authorizer(registry)
    
    with pytest.raises(ValueError, match="can only process OperationalAuthorization records"):
        authorizer.authorize({"strategy_manifest_id": "manifest_invalid"})


def test_authorizer_does_not_expose_update_delete(temp_storage):
    """Verify Authorizer does not expose update or delete behavior."""
    registry = DeploymentRegistry(temp_storage)
    authorizer = Authorizer(registry)
    
    assert not hasattr(authorizer, "update"), "Authorizer must not have an update operation"
    assert not hasattr(authorizer, "delete"), "Authorizer must not have a delete operation"
    assert not hasattr(authorizer, "remove"), "Authorizer must not have a remove operation"


def test_authorizer_no_mutation(temp_storage):
    """Verify Authorizer does not mutate the given authorization object."""
    registry = DeploymentRegistry(temp_storage)
    authorizer = Authorizer(registry)
    
    auth = create_mock_authorization()
    
    original_manifest_id = auth.strategy_manifest_id
    original_operator = auth.operator_identity
    
    authorizer.authorize(auth)
    
    assert auth.strategy_manifest_id == original_manifest_id
    assert auth.operator_identity == original_operator
