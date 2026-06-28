from core.schemas.base import BaseCreateSchema, BaseQueryParamsSchema, BaseReadSchema


class Product(BaseCreateSchema):
    name: str
    brand: str | None = None
    description: str | None = None
    price: float | None = None


class ProductCreate(Product): ...


class ProductRead(Product, BaseReadSchema): ...


class ProductUpdate(Product): ...


class ProductQueryParams(BaseQueryParamsSchema):
    search: str | None = None
    brand: str | None = None
    min_price: float | None = None
    max_price: float | None = None
