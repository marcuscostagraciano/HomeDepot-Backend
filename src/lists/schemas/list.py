from uuid import UUID

from pydantic import Field

from core.schemas import BaseSchema


class ListCreate(BaseSchema):
    observation: str | None = Field(
        default=None, description="Observation about the list"
    )


class ListRead(BaseSchema):
    id: UUID = Field(description="Unique identifier of the list")
    observation: str | None = Field(
        default=None, description="Observation about the list"
    )
    bought: bool = Field(default=False, description="Indicates if the list is bought")
    created_at: str = Field(description="Timestamp of when the list was created")
    updated_at: str | None = Field(
        default=None, description="Timestamp of when the list was last updated"
    )


class ListUpdate(BaseSchema):
    observation: str | None = Field(
        default=None, description="Observation about the list"
    )
    bought: bool | None = Field(
        default=None, description="Indicates if the list is bought"
    )
