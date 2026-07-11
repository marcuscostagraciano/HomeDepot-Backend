from typing import Protocol
from uuid import UUID

from db.domain.ports import RepositoryPort

from ..domain.filters import ListFilters
from .schemas import ListCreate, ListRead


class ListRepositoryPort(
    RepositoryPort[
        ListCreate,
        ListRead,
        UUID,
        UUID,
    ],
    Protocol,
):
    """Repository protocol for managing list persistence."""

    async def read_all(self, filters: ListFilters) -> list[ListRead]: ...

    async def read_all_accessible(
        self,
        filters: ListFilters,
        user_id: UUID,
    ) -> list[ListRead]: ...
