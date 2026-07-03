from typing import Protocol, Tuple
from uuid import UUID

from db.domain.ports import RepositoryPort

from .schemas import ListProductCreate, ListProductRead, ListProductUpdate


class ListProductRepositoryPort(
    RepositoryPort[
        ListProductCreate,
        ListProductRead,
        Tuple[UUID, UUID],
    ],
    Protocol,
):
    async def read(
        self,
        id: Tuple[UUID, UUID],
    ) -> ListProductRead | None: ...

    async def read_all_by_list(
        self,
        list_id: UUID,
    ) -> list[ListProductRead]: ...

    async def update(
        self,
        id: Tuple[UUID, UUID],
        payload: ListProductUpdate,
    ) -> ListProductRead | None: ...

    async def delete(
        self,
        id: Tuple[UUID, UUID],
    ) -> ListProductRead | None: ...
