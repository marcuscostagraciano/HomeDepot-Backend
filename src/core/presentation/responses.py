from datetime import datetime
from uuid import UUID

from .base_presentation import BasePresentation


class BaseResponsePresentation(BasePresentation):
    """
    Schema used as a base for all `read` operations, ensuring that every read schema includes:
        - A unique identifier (`id`) of type `UUID`.
        - Timestamps for when the record was created (`created_date`) and last updated (`updated_date`).
    """

    id: UUID
    created_date: datetime
    updated_date: datetime | None
