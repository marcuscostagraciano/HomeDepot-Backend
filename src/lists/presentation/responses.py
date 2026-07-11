from uuid import UUID

from pydantic import Field

from core.presentation import (
    BasePresentation,
    BaseRequestPresentation,
    BaseResponsePresentation,
)


class List(BasePresentation):
    name: str
    observation: str | None = Field(
        default=None,
        description="Observation about the list",
    )


class ListCreate(List, BaseRequestPresentation): ...


class ListReadResponsePresentation(ListCreate, BaseResponsePresentation):
    created_by_id: UUID = Field(
        description="User id who created the list",
    )
    updated_by_id: UUID | None = Field(
        default=None,
        description="User id who last updated the list",
    )
    bought: bool | None = Field(
        default=None,
        description="Indicates if the list is bought",
    )


class ListUpdate(List, BasePresentation):
    bought: bool | None = Field(
        default=None,
        description="Indicates if the list is bought",
    )
