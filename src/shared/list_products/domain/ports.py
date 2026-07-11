from typing import Protocol
from uuid import UUID

from db.domain.ports import RepositoryPort

from ...domain.types import AssociationIdVO
from .schemas import ListProductCreate, ListProductRead, ListProductUpdate


class ListProductRepositoryPort(
    RepositoryPort[ListProductCreate, ListProductRead, AssociationIdVO, None],
    Protocol,
):
    async def read(
        self,
        id: AssociationIdVO,
    ) -> ListProductRead | None: ...

    async def read_all_by_list(
        self,
        list_id: UUID,
    ) -> list[ListProductRead]: ...

    async def update(
        self,
        id: AssociationIdVO,
        payload: ListProductUpdate,
    ) -> ListProductRead | None: ...

    async def delete(
        self,
        id: AssociationIdVO,
    ) -> ListProductRead | None: ...
