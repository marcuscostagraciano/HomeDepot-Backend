from unittest.mock import AsyncMock, Mock
from uuid import UUID

import pytest

from core.domain.errors import NotFoundError
from users.domain.errors import UniqueEmailError
from users.domain.schemas import UserCreate, UserRead
from users.domain.use_cases import create_user, read_user


async def test_create_user_successful() -> None:
    repository = AsyncMock()
    repository.check_email_exists.return_value = False
    repository.create.return_value = UserRead(
        id=UUID("11111111-1111-1111-1111-111111111111"),
        created_date="2000-01-01",  # type: ignore
        updated_date=None,
        first_name="John",
        last_name="Doe",
        email="john@test.com",
        password="hashed",
    )
    password_hasher = Mock()
    password_hasher.hash.return_value = "hashed123"

    payload = UserCreate(
        first_name="John",
        last_name="Doe",
        email="john@test.com",
        password="12345678",
    )

    result = await create_user(repository, payload, password_hasher)

    assert result.email == "john@test.com"
    repository.check_email_exists.assert_awaited_once_with("john@test.com")
    password_hasher.hash.assert_called_once_with("12345678")


async def test_create_user_raises_on_duplicate_email() -> None:
    repository = AsyncMock()
    repository.check_email_exists.return_value = True
    password_hasher = Mock()

    payload = UserCreate(
        first_name="John",
        last_name="Doe",
        email="john@test.com",
        password="12345678",
    )

    with pytest.raises(UniqueEmailError):
        await create_user(repository, payload, password_hasher)

    repository.create.assert_not_called()


async def test_read_user_successful() -> None:
    user_id = UUID("11111111-1111-1111-1111-111111111111")
    repository = AsyncMock()
    repository.read.return_value = UserRead(
        id=user_id,
        created_date="2000-01-01",  # type: ignore
        updated_date=None,
        first_name="John",
        last_name="Doe",
        email="john@test.com",
        password="hashed",
    )

    result = await read_user(repository, user_id)

    assert result.id == user_id
    repository.read.assert_awaited_once_with(user_id)


async def test_read_user_raises_not_found() -> None:
    user_id = UUID("11111111-1111-1111-1111-111111111111")
    repository = AsyncMock()
    repository.read.return_value = None

    with pytest.raises(NotFoundError, match="User"):
        await read_user(repository, user_id)


async def test_get_token_successful(
    user: UserRead,
    authenticator: AsyncMock,
    jwt_service: AsyncMock,
) -> None:
    from users.domain.schemas import TokenSchema
    from users.domain.use_cases import get_token

    authenticator.authenticate.return_value = user

    jwt_service.generate.return_value = TokenSchema(
        access_token="token",
        token_type="Bearer",
    )

    token = await get_token(
        "john@example.com",
        "123456",
        authenticator,
        jwt_service,
    )

    authenticator.authenticate.assert_awaited_once_with(
        "john@example.com",
        "123456",
    )

    jwt_service.generate.assert_called_once_with({"email": user.email})

    assert token.access_token == "token"


async def test_get_token_raises_unauthorized_error(
    authenticator: AsyncMock,
    jwt_service: AsyncMock,
) -> None:
    from core.domain.errors import UnauthorizedError
    from users.domain.use_cases import get_token

    authenticator.authenticate.return_value = None

    with pytest.raises(UnauthorizedError):
        await get_token(
            "john@example.com",
            "wrong",
            authenticator,
            jwt_service,
        )

    jwt_service.generate.assert_not_called()
