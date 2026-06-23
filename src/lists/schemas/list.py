from uuid import UUID

from pydantic import Field

from core.schemas import BaseCreateSchema, BaseReadSchema, BaseSchema


class ListCreate(BaseCreateSchema):
    observation: str | None = Field(
        default=None, description="Observation about the list"
    )
    created_by_id: UUID = Field(description="User id who created the list")


class ListRead(ListCreate, BaseReadSchema):
    bought: bool = Field(default=False, description="Indicates if the list is bought")
    updated_by_id: UUID | None = Field(
        default=None, description="User id who last updated the list"
    )


class ListUpdate(BaseSchema):
    observation: str | None = Field(
        default=None, description="Observation about the list"
    )
    bought: bool | None = Field(
        default=None, description="Indicates if the list is bought"
    )
