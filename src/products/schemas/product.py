from uuid import UUID

from core.schemas.base import BaseSchema


class Product(BaseSchema):
    brand: str | None = None
    description: str | None = None
    price: float | None = None


class ProductCreate(Product):
    name: str


class ProductRead(Product):
    id: UUID
    name: str


class ProductUpdate(Product):
    name: str | None = None
    name: str | None = None
