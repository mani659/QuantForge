import pytest
from datetime import datetime
from dataclasses import FrozenInstanceError

from operational_governance.operational_authorization import (
    OperationalAuthorization,
    InvalidOperationalAuthorizationData,
)


def test_operational_authorization_construction():
    """Verify construction succeeds with valid data and fields are preserved exactly."""
    now = datetime.now()
    auth = OperationalAuthorization(
        strategy_manifest_id="manifest_001",
        deployment_identity="deploy_prod_btc",
        operator_identity="alice_ops",
        authorized_at=now,
    )

    assert auth.strategy_manifest_id == "manifest_001"
    assert auth.deployment_identity == "deploy_prod_btc"
    assert auth.operator_identity == "alice_ops"
    assert auth.authorized_at == now


def test_operational_authorization_immutability():
    """Verify mutation after construction is rejected."""
    now = datetime.now()
    auth = OperationalAuthorization(
        strategy_manifest_id="manifest_001",
        deployment_identity="deploy_prod_btc",
        operator_identity="alice_ops",
        authorized_at=now,
    )

    with pytest.raises(FrozenInstanceError):
        auth.strategy_manifest_id = "manifest_002"

    with pytest.raises(FrozenInstanceError):
        auth.deployment_identity = "deploy_staging"


def test_operational_authorization_equality():
    """Verify equality semantics follow existing conventions."""
    now = datetime.now()
    auth1 = OperationalAuthorization(
        strategy_manifest_id="manifest_001",
        deployment_identity="deploy_prod_btc",
        operator_identity="alice_ops",
        authorized_at=now,
    )
    auth2 = OperationalAuthorization(
        strategy_manifest_id="manifest_001",
        deployment_identity="deploy_prod_btc",
        operator_identity="alice_ops",
        authorized_at=now,
    )

    assert auth1 == auth2
    assert hash(auth1) == hash(auth2)


def test_operational_authorization_invalid_data():
    """Verify construction fails with invalid data."""
    now = datetime.now()
    
    with pytest.raises(InvalidOperationalAuthorizationData):
        OperationalAuthorization(
            strategy_manifest_id="",
            deployment_identity="deploy_prod_btc",
            operator_identity="alice_ops",
            authorized_at=now,
        )

    with pytest.raises(InvalidOperationalAuthorizationData):
        OperationalAuthorization(
            strategy_manifest_id="manifest_001",
            deployment_identity=None,
            operator_identity="alice_ops",
            authorized_at=now,
        )

    with pytest.raises(InvalidOperationalAuthorizationData):
        OperationalAuthorization(
            strategy_manifest_id="manifest_001",
            deployment_identity="deploy_prod_btc",
            operator_identity="   ",
            authorized_at=now,
        )

    with pytest.raises(InvalidOperationalAuthorizationData):
        OperationalAuthorization(
            strategy_manifest_id="manifest_001",
            deployment_identity="deploy_prod_btc",
            operator_identity="alice_ops",
            authorized_at="2026-08-08",
        )
