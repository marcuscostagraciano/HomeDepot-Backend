from typing import Any, Dict

import pytest

from tests.config import Settings
from users.adapters.jwt_service import JWTService
from users.adapters.password_hasher import PasswordHasher
from users.domain.ports import JWTServicePort, PasswordHasherPort


@pytest.fixture
def jwt_service() -> JWTServicePort:
    return JWTService(Settings())


@pytest.fixture
def password_hasher() -> PasswordHasherPort:
    return PasswordHasher()


@pytest.fixture
def payload() -> Dict[str, Any]:
    return {"email": "test@example.test"}
