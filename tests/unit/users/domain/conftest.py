from datetime import datetime
from unittest.mock import AsyncMock, Mock
from uuid import UUID

import pytest

from users.domain.ports import AuthenticatorPort, JWTServicePort
from users.domain.schemas import UserRead


@pytest.fixture
def authenticator() -> AuthenticatorPort:
    return AsyncMock(spec=AuthenticatorPort)


@pytest.fixture
def jwt_service() -> JWTServicePort:
    return Mock(spec=JWTServicePort)


@pytest.fixture
def user() -> UserRead:
    return UserRead(
        id=UUID("11111111-1111-1111-1111-111111111111"),
        created_date=datetime(2000, 1, 1),
        updated_date=datetime(2000, 1, 2),
        first_name="Test",
        last_name="test",
        email="test@example.test",
        password="hashed-password",
    )
