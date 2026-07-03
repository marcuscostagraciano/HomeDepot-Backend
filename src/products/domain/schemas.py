from dataclasses import dataclass

from core.domain.schemas import DomainCreateSchema, DomainReadSchema, DomainSchema


@dataclass(frozen=True)
class Product(DomainSchema):
    name: str
    brand: str | None = None
    description: str | None = None
    price: float | None = None


@dataclass(frozen=True)
class ProductCreate(Product, DomainCreateSchema): ...


@dataclass(frozen=True)
class ProductRead(Product, DomainReadSchema): ...


@dataclass(frozen=True)
class ProductUpdate(Product): ...
