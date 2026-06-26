import pytest

from security.domain import AuthRepositoryPort, JWTServicePort, get_token
from security.schemas import TokenSchema
from users.schemas import UserRead


async def test_get_token_successful(
    user: UserRead,
    auth_repository: AuthRepositoryPort,
    jwt_service: JWTServicePort,
) -> None:
    auth_repository.authenticate.return_value = user

    jwt_service.generate.return_value = TokenSchema(
        access_token="token",
        token_type="Bearer",
    )

    token = await get_token(
        "john@example.com",
        "123456",
        auth_repository,
        jwt_service,
    )

    auth_repository.authenticate.assert_awaited_once_with(
        "john@example.com",
        "123456",
    )

    jwt_service.generate.assert_called_once_with({"email": user.email})

    assert token.access_token == "token"


async def test_get_token_raises_unauthorized_error(
    auth_repository: AuthRepositoryPort,
    jwt_service: JWTServicePort,
) -> None:
    auth_repository.authenticate.return_value = None

    with pytest.raises(Exception):
        await get_token(
            "john@example.com",
            "wrong",
            auth_repository,
            jwt_service,
        )

    jwt_service.generate.assert_not_called()
