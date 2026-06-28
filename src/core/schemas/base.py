from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from ..domain import SortField, SortOrder


class BaseSchema(BaseModel):
    """Base schema used by the other `schemas` in the project.

    Inherently supports conversion from SQLAlchemy ORM models to Pydantic models, making it easier to work with
    database records in endpoints.

    Also provides immutability to ensure that once an instance is created, it cannot be modified.
    """

    model_config = ConfigDict(
        from_attributes=True,
        frozen=True,
        use_enum_values=True,
    )


class BaseCreateSchema(BaseSchema):
    """Schema used as a base for all `create` operations."""

    ...


class BaseReadSchema(BaseSchema):
    """
    Schema used as a base for all `read` operations, ensuring that every read schema includes:
        - A unique identifier (`id`) of type `UUID`.
        - Timestamps for when the record was created (`created_date`) and last updated (`updated_date`).
    """

    id: UUID
    created_date: datetime
    updated_date: datetime | None


class BaseQueryParamsSchema(BaseSchema):
    """Schema used as a base for all query parameters."""

    page: int = Field(
        default=1,
        description="Page number for paginated results. Starts at 1.",
    )
    limit: int = Field(
        default=20,
        description="Maximum number of items to return per page.",
    )
    sort: SortField = Field(
        default=SortField.ID,
        description="Field used to sort the returned results.",
    )
    order: SortOrder = Field(
        default=SortOrder.ASC,
        description="Sort order for the returned results (ascending or descending).",
    )
