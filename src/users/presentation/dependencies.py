from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import DecodeError, ExpiredSignatureError

from core.domain.errors import ExpiredTokenError, UnauthorizedError

from ..adapters.jwt_service import get_jwt_service
from ..domain.ports import JWTServicePort, UserRepositoryPort
from ..domain.schemas import UserRead
from ..repositories.user_repository import get_user_repository


async def get_current_user(
    token: str = Depends(OAuth2PasswordBearer(tokenUrl="users/login")),
    repository: UserRepositoryPort = Depends(get_user_repository),
    jwt_service: JWTServicePort = Depends(get_jwt_service),
) -> UserRead | None:
    """Get the current user based in the provided token.

    Args:
        token (str, optional): Token used to fetch the current user. Defaults to Depends(oauth2_scheme).
        repository (UserRepositoryPort, optional): Repository responsible for the database fetch. Defaults to Depends(get_user_repository).

    Raises:
        UnauthorizedError: Error raised when any of these situations occur:
            - It is not possible to `decode` the token;
            - The token has expired;
            - The `email` claim is missing.

    Returns:
        UserRead: User object with the current user informations.
    """

    try:
        payload = jwt_service.decode(token)
    except DecodeError:
        raise UnauthorizedError()
    except ExpiredSignatureError:
        raise ExpiredTokenError()

    if not (email := payload.get("email")):
        raise UnauthorizedError()

    user: UserRead | None = await repository.get_user_by_email(email)
    if not user:
        raise UnauthorizedError()

    return user
