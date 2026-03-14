from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    """Base schema used by the other `schemas` in the project.

    Inherently supports conversion from SQLAlchemy ORM models to Pydantic models, making it easier to work with
    database records in endpoints.

    Also provides immutability to ensure that once an instance is created, it cannot be modified.
    """

    model_config = ConfigDict(
        from_attributes=True,
        frozen=True,
    )


class BaseCreateSchema(BaseSchema):
    """
    Schema used as a base for all `create` operations.
    """

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
