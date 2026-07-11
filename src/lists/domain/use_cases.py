from uuid import UUID

from core.domain.errors import ForbiddenError, NotFoundError
from shared.list_shares.domain.ports import ListShareRepositoryPort
from shared.list_shares.domain.use_cases import validate_user_access_to_list

from .filters import ListFilters
from .ports import ListRepositoryPort
from .schemas import ListCreate, ListRead


async def create_list(
    repository: ListRepositoryPort,
    payload: ListCreate,
    user_id: UUID,
) -> ListRead:
    payload = payload.copy(update={"created_by_id": user_id})
    return await repository.create(payload)


async def read_list(
    repository: ListRepositoryPort,
    share_repository: ListShareRepositoryPort,
    list_id: UUID,
    user_id: UUID,
) -> ListRead:
    list_obj = await validate_user_access_to_list(
        share_repository,
        repository,
        list_id,
        user_id,
    )

    return list_obj


async def read_lists(
    repository: ListRepositoryPort,
    filters: ListFilters,
    user_id: UUID,
) -> list[ListRead]:
    lists = await repository.read_all_accessible(filters, user_id)

    return lists


async def delete_list(
    repository: ListRepositoryPort,
    share_repository: ListShareRepositoryPort,
    list_id: UUID,
    user_id: UUID,
) -> ListRead:
    list: ListRead = await read_list(
        repository,
        share_repository,
        list_id,
        user_id,
    )

    if user_id != list.created_by_id:
        raise ForbiddenError()

    deleted = await repository.delete(list_id)

    if not deleted:
        raise NotFoundError("List", str(list_id))

    return deleted
