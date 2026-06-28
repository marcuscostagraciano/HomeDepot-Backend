from uuid import UUID

from pydantic import Field

from core.schemas import BaseCreateSchema, BaseReadSchema, BaseSchema


class List(BaseSchema):
    name: str
    observation: str | None = Field(
        default=None,
        description="Observation about the list",
    )


class ListCreate(List, BaseCreateSchema):
    created_by_id: UUID = Field(
        description="User id who created the list",
    )


class ListRead(ListCreate, BaseReadSchema):
    updated_by_id: UUID | None = Field(
        default=None,
        description="User id who last updated the list",
    )


class ListUpdate(List, BaseSchema):
    bought: bool | None = Field(
        default=None,
        description="Indicates if the list is bought",
    )
