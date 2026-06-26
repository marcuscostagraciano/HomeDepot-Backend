from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import DecodeError, ExpiredSignatureError

from security.utils import decode_jwt_token
from users.domain import CredentialsError, ExpiredTokenError, UserRepositoryPort
from users.repositories import get_user_repository
from users.schemas import UserRead


async def get_current_user(
    token: str = Depends(OAuth2PasswordBearer(tokenUrl="token")),
    repository: UserRepositoryPort = Depends(get_user_repository),
) -> UserRead | None:
    """Get the current user based in the provided token.

    Args:
        token (str, optional): Token used to fetch the current user. Defaults to Depends(oauth2_scheme).
        repository (UserRepositoryPort, optional): Repository responsible for the database fetch. Defaults to Depends(get_user_repository).

    Raises:
        CredentialsError: Error raised when any of these situations occur:
            - It is not possible to `decode` the token;
            - The token has expired;
            - The `email` claim is missing.

    Returns:
        UserRead | None: UserRead object with the current user informations.
    """

    try:
        payload = decode_jwt_token(token)
    except DecodeError:
        raise CredentialsError()
    except ExpiredSignatureError:
        raise ExpiredTokenError()

    if not (email := payload.get("email")):
        raise CredentialsError()

    return await repository.get_user_by_email(email)
