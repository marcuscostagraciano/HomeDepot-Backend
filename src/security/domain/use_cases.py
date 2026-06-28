from ..domain import AuthRepositoryPort, JWTServicePort, UnauthorizedError
from ..schemas import TokenSchema


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
