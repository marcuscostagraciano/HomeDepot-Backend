from uuid import UUID
from .base import BaseSchema


class ListCreate(BaseSchema):
    observation: str | None = None


class ListRead(BaseSchema):
    id: UUID
    observation: str | None = None
    bought: bool = False
    created_at: str
    updated_at: str | None = None


class ListUpdate(BaseSchema):
    observation: str | None = None
    bought: bool | None = None
