from uuid import UUID

from core.domain.errors import ForbiddenError, NotFoundError
from lists.domain.ports import ListRepositoryPort
from lists.domain.schemas import ListRead
from users.domain.ports import UserRepositoryPort

from ...domain.types import AssociationIdVO
from ..domain.ports import ListShareRepositoryPort
from ..domain.schemas import UserListCreate, UserListRead


async def share_list(
    repository: ListShareRepositoryPort,
    list_repository: ListRepositoryPort,
    user_repository: UserRepositoryPort,
    payload: UserListCreate,
    actor_user_id: UUID,
) -> UserListRead:
    list_obj = await list_repository.read(payload.list_id)
    if not list_obj:
        raise NotFoundError("List", str(payload.list_id))

    # Apenas o dono da lista pode compartilhá-la
    if list_obj.created_by_id != actor_user_id:
        raise ForbiddenError()

    user = await user_repository.read(payload.user_id)
    if not user:
        raise NotFoundError("User", str(payload.user_id))

    existing = await repository.read_by_user_and_list(
        payload.user_id,
        payload.list_id,
    )

    if existing:
        return existing

    return await repository.create(payload)


async def read_shared_lists(
    repository: ListShareRepositoryPort,
    user_id: UUID,
) -> list[UserListRead]:
    return await repository.read_all_by_user(user_id)


async def validate_user_access_to_list(
    repository: ListShareRepositoryPort,
    list_repository: ListRepositoryPort,
    list_id: UUID,
    user_id: UUID,
) -> ListRead:
    list_obj = await list_repository.read(list_id)
    if not list_obj:
        raise NotFoundError("List", str(list_id))

    if list_obj.created_by_id == user_id:
        return list_obj

    share = await repository.read_by_user_and_list(user_id, list_id)
    if not share:
        raise ForbiddenError()

    return list_obj


async def remove_share(
    repository: ListShareRepositoryPort,
    list_repository: ListRepositoryPort,
    actor_user_id: UUID,
    association_id: AssociationIdVO,
) -> UserListRead:
    user_id = association_id.first_id
    list_id = association_id.second_id

    list_obj = await list_repository.read(list_id)
    if not list_obj:
        raise NotFoundError("List", str(list_id))

    # owner can remove any invited user, invited user can remove themselves
    is_owner = list_obj.created_by_id == actor_user_id
    is_self = actor_user_id == user_id

    if not (is_owner or is_self):
        raise ForbiddenError()

    existing = await repository.read_by_user_and_list(user_id, list_id)
    if not existing:
        raise NotFoundError("ListShare", f"{user_id}/{list_id}")

    deleted = await repository.delete(association_id)
    if not deleted:
        raise NotFoundError("ListShare", f"{user_id}/{list_id}")

    return deleted
