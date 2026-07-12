from unittest.mock import AsyncMock, Mock
from uuid import UUID

import pytest

from users.adapters.authenticator import Authenticator


@pytest.fixture
def repository() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def password_hasher() -> Mock:
    return Mock()


@pytest.fixture
def authenticator(
    repository: AsyncMock,
    password_hasher: AsyncMock,
) -> Authenticator:
    return Authenticator(
        repository=repository,
        password_hasher=password_hasher,
    )


async def test_authenticate_returns_user_when_valid(
    authenticator: Authenticator,
    repository: AsyncMock,
    password_hasher: AsyncMock,
) -> None:
    from users.domain.schemas import UserRead

    user = UserRead(
        id=UUID("11111111-1111-1111-1111-111111111111"),
        created_date="2000-01-01",  # type: ignore
        updated_date=None,
        first_name="John",
        last_name="Doe",
        email="john@test.com",
        password="hashed",
    )
    repository.get_user_by_email.return_value = user
    password_hasher.verify.return_value = True

    result = await authenticator.authenticate("john@test.com", "12345678")

    assert result is not None
    assert result.email == "john@test.com"
    repository.get_user_by_email.assert_awaited_once_with("john@test.com")
    password_hasher.verify.assert_called_once_with("12345678", "hashed")


async def test_authenticate_returns_none_when_user_not_found(
    authenticator: Authenticator,
    repository: AsyncMock,
    password_hasher: AsyncMock,
) -> None:
    repository.get_user_by_email.return_value = None

    result = await authenticator.authenticate("john@test.com", "12345678")

    assert result is None
    password_hasher.verify.assert_not_called()


async def test_authenticate_returns_none_when_wrong_password(
    authenticator: Authenticator,
    repository: AsyncMock,
    password_hasher: AsyncMock,
) -> None:
    from users.domain.schemas import UserRead

    user = UserRead(
        id=UUID("11111111-1111-1111-1111-111111111111"),
        created_date="2000-01-01",  # type: ignore
        updated_date=None,
        first_name="John",
        last_name="Doe",
        email="john@test.com",
        password="hashed",
    )
    repository.get_user_by_email.return_value = user
    password_hasher.verify.return_value = False

    result = await authenticator.authenticate("john@test.com", "wrong")

    assert result is None
    password_hasher.verify.assert_called_once_with("wrong", "hashed")
