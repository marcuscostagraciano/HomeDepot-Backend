from uuid import UUID

from pydantic import Field

from core.presentation.base_presentation import BasePresentation
from core.presentation.requests import BaseRequestPresentation
from core.presentation.responses import BaseResponsePresentation


class Product(BasePresentation):
    name: str
    observation: str | None = Field(
        default=None,
        description="Observation about the Product",
    )


class ProductCreate(Product, BaseRequestPresentation): ...


class ProductReadResponsePresentation(ProductCreate, BaseResponsePresentation):
    created_by_id: UUID = Field(
        description="User id who created the Product",
    )
    updated_by_id: UUID | None = Field(
        default=None,
        description="User id who last updated the Product",
    )


class ProductUpdate(Product, BasePresentation): ...
