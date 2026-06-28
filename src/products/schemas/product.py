from core.schemas.base import BaseCreateSchema, BaseQueryParamsSchema, BaseReadSchema


class Product(BaseCreateSchema):
    brand: str | None = None
    description: str | None = None
    price: float | None = None


class ProductCreate(Product):
    name: str


class ProductRead(Product, BaseReadSchema):
    name: str


class ProductUpdate(Product):
    name: str | None = None
