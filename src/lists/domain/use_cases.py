from uuid import UUID

from core.errors import NotFoundError
from lists.schemas.list import ListCreate, ListRead

from .ports import ListRepositoryPort


async def create_list(
    list_payload: ListCreate, repository: ListRepositoryPort
) -> ListRead:
    created = await repository.create(list_payload)

    return ListRead.model_validate(created)


async def read_list(list_id: UUID, repository: ListRepositoryPort) -> ListRead:
    list_obj = await repository.read(list_id)

    if not list_obj:
        raise NotFoundError("List", str(list_id))

    return ListRead.model_validate(list_obj)


async def read_lists(repository: ListRepositoryPort) -> list[ListRead]:
    lists = await repository.read_all()

    return [ListRead.model_validate(list_obj) for list_obj in lists]


async def delete_list(list_id: UUID, repository: ListRepositoryPort) -> ListRead:
    deleted = await repository.delete(list_id)

    if not deleted:
        raise NotFoundError("List", str(list_id))

    return ListRead.model_validate(deleted)
