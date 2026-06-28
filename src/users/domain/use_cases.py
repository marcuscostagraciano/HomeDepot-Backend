from uuid import UUID

from core.domain import NotFoundError, RequiredFieldMissingError
from security.domain import PasswordHasherPort

from ..domain import UniqueEmailError, UserRepositoryPort
from ..schemas import UserCreate, UserRead


async def create_user(
    user: UserCreate,
    repository: UserRepositoryPort,
    password_hasher: PasswordHasherPort,
) -> UserRead:
    if not user.first_name:
        raise RequiredFieldMissingError("first_name")
    if not user.last_name:
        raise RequiredFieldMissingError("last_name")
    if not user.email:
        raise RequiredFieldMissingError("email")
    if not user.password:
        raise RequiredFieldMissingError("password")

    if await repository.check_email_exists(user.email):
        raise UniqueEmailError()

    hashed_user = user.model_copy(
        update={"password": password_hasher.hash(user.password)}
    )

    return await repository.create(hashed_user)


async def read_user(user_id: UUID, repository: UserRepositoryPort) -> UserRead:
    user = await repository.read(user_id)

    if not user:
        raise NotFoundError("User", str(user_id))

    return user
