from typing import Protocol
from uuid import UUID

from db.domain.ports import RepositoryPort

from ...domain.types import AssociationIdVO
from .schemas import UserListCreate, UserListRead


class ListShareRepositoryPort(
    RepositoryPort[UserListCreate, UserListRead, AssociationIdVO, None],
    Protocol,
):
    async def read(
        self,
        id: AssociationIdVO,
    ) -> UserListRead | None: ...

    async def read_by_user_and_list(
        self,
        user_id: UUID,
        list_id: UUID,
    ) -> UserListRead | None: ...

    async def read_all_by_user(
        self,
        user_id: UUID,
    ) -> list[UserListRead]: ...

    async def delete(
        self,
        id: AssociationIdVO,
    ) -> UserListRead | None: ...
