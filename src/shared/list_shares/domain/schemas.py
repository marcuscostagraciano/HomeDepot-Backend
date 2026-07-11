from dataclasses import dataclass
from uuid import UUID

from core.domain.schemas import DomainCreateSchema, DomainReadSchema, DomainSchema


@dataclass(frozen=True)
class UserList(DomainSchema):
    user_id: UUID
    list_id: UUID


@dataclass(frozen=True)
class UserListCreate(UserList, DomainCreateSchema): ...


@dataclass(frozen=True)
class UserListRead(UserList, DomainReadSchema): ...
