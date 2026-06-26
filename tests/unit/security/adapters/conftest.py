from typing import Any, Dict

import pytest

from security.adapters import JWTService, PasswordHasher
from security.domain import JWTServicePort, PasswordHasherPort
from tests.config import Settings


@pytest.fixture
def jwt_service() -> JWTServicePort:
    return JWTService(Settings())


@pytest.fixture
def password_hasher() -> PasswordHasherPort:
    return PasswordHasher()


@pytest.fixture
def payload() -> Dict[str, Any]:
    return {"email": "test@example.test"}
