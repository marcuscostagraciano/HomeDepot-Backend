from uuid import UUID

from pydantic import Field

from core.presentation import BaseResponsePresentation


class ListProductReadResponsePresentation(BaseResponsePresentation):
    list_id: UUID
    product_id: UUID
    quantity: int
    bought: bool | None = Field(
        default=None,
        description="Indicates if the product is bought in this list",
    )
    notes: str | None = Field(
        default=None,
        description="Notes about the product in this list",
    )
