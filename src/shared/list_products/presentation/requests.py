from uuid import UUID

from pydantic import Field

from core.presentation import BaseRequestPresentation


class ListProductCreateRequestPresentation(BaseRequestPresentation):
    product_id: UUID
    quantity: int = Field(
        default=1,
        ge=1,
        description="Quantity of the product in the list",
    )
    bought: bool | None = Field(
        default=False,
        description="Indicates if the product is bought in this list",
    )
    notes: str | None = Field(
        default=None,
        description="Notes about the product in this list",
    )


class ListProductUpdateRequestPresentation(BaseRequestPresentation):
    quantity: int | None = Field(
        default=None,
        ge=1,
        description="Updated quantity of the product in the list",
    )
    bought: bool | None = Field(
        default=None,
        description="Indicates if the product is bought in this list",
    )
    notes: str | None = Field(
        default=None,
        description="Notes about the product in this list",
    )
