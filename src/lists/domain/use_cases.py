from uuid import UUID

from core.domain.errors import ForbiddenError, NotFoundError

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
    list_id: UUID,
) -> ListRead:
    list_obj = await repository.read(list_id)

    if not list_obj:
        raise NotFoundError("List", str(list_id))

    return list_obj


async def read_lists(
    repository: ListRepositoryPort,
    filters: ListFilters,
) -> list[ListRead]:
    lists = await repository.read_all(filters)

    return lists


async def delete_list(
    repository: ListRepositoryPort,
    list_id: UUID,
    user_id: UUID,
) -> ListRead:
    list: ListRead = await read_list(repository, list_id)

    if user_id != list.created_by_id:
        raise ForbiddenError()

    deleted = await repository.delete(list_id)

    if not deleted:
        raise NotFoundError("List", str(list_id))

    return deleted
