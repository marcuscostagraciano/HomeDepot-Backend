from uuid import UUID

from core.errors import NotFoundError, RequiredFieldMissingError
from users.domain import UserRepositoryPort
from users.schemas.user import UserCreate, UserRead


async def create_user(user: UserCreate, repository: UserRepositoryPort) -> UserRead:
    if not user.first_name:
        raise RequiredFieldMissingError("first_name")
    if not user.last_name:
        raise RequiredFieldMissingError("last_name")
    if not user.email:
        raise RequiredFieldMissingError("email")
    if not user.password:
        raise RequiredFieldMissingError("password")

    created = await repository.create(user)

    return UserRead.model_validate(created)


async def read_user(user_id: UUID, repository: UserRepositoryPort) -> UserRead:
    user = await repository.read(user_id)

    if not user:
        raise NotFoundError("User", str(user_id))

    return UserRead.model_validate(user)
