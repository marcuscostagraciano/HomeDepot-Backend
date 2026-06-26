from security.domain.errors import UnauthorizedError
from security.domain.ports import AuthRepositoryPort
from security.schemas import TokenSchema
from security.utils import generate_jwt_token


async def get_token(
    username: str,
    password: str,
    repository: AuthRepositoryPort,
) -> TokenSchema:
    user = await repository.authenticate(username, password)

    if not user:
        raise UnauthorizedError("invalid credentials")

    return generate_jwt_token(
        {
            "email": user.email,
        }
    )
