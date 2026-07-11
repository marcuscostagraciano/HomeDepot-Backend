from dataclasses import dataclass
from uuid import UUID

from core.domain.schemas import DomainCreateSchema, DomainReadSchema, DomainSchema


@dataclass(frozen=True)
class List(DomainSchema):
    name: str
    observation: str | None
    bought: bool = False


@dataclass(frozen=True)
class ListCreate(List, DomainCreateSchema):
    created_by_id: UUID | None = None


@dataclass(frozen=True)
class ListRead(ListCreate, DomainReadSchema):
    updated_by_id: UUID | None = None


@dataclass(frozen=True)
class ListUpdate(List): ...
