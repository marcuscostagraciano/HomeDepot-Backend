from uuid import UUID

from core.domain.errors import NotFoundError, UnauthorizedError

from .errors import UniqueEmailError
from .ports import (
    AuthenticatorPort,
    JWTServicePort,
    PasswordHasherPort,
    UserRepositoryPort,
)
from .schemas import TokenSchema, UserCreate, UserRead


async def create_user(
    repository: UserRepositoryPort,
    user: UserCreate,
    password_hasher: PasswordHasherPort,
) -> UserRead:

    if await repository.check_email_exists(user.email):
        raise UniqueEmailError()

    hashed_user = user.copy(update={"password": password_hasher.hash(user.password)})

    return await repository.create(hashed_user)


async def read_user(
    repository: UserRepositoryPort,
    user_id: UUID,
) -> UserRead:
    user = await repository.read(user_id)

    if not user:
        raise NotFoundError("User", str(user_id))

    return user


async def get_token(
    username: str,
    password: str,
    authenticator: AuthenticatorPort,
    jwt_service: JWTServicePort,
) -> TokenSchema:
    user = await authenticator.authenticate(username, password)

    if not user:
        raise UnauthorizedError("invalid credentials")

    return jwt_service.generate({"email": user.email})
