from pydantic import Field

from core.presentation.responses import BaseResponsePresentation


class ProductReadResponsePresentation(BaseResponsePresentation):
    name: str
    brand: str | None = Field(
        default=None,
        description="Brand of the product",
    )
    description: str | None = Field(
        default=None,
        description="Description of the product",
    )
