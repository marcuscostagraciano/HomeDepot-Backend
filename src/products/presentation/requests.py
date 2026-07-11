from pydantic import Field

from core.presentation.requests import BaseRequestPresentation


class ProductCreateRequestPresentation(BaseRequestPresentation):
    name: str
    brand: str | None = Field(
        default=None,
        description="Brand of the product",
    )
    description: str | None = Field(
        default=None,
        description="Description of the product",
    )
