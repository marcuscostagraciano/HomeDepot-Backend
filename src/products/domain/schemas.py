from dataclasses import dataclass
from uuid import UUID

from core.domain.schemas import DomainCreateSchema, DomainReadSchema, DomainSchema


@dataclass(frozen=True)
class Product(DomainSchema):
    name: str
    brand: str | None = None
    description: str | None = None


@dataclass(frozen=True)
class ProductCreate(Product, DomainCreateSchema):
    created_by_id: UUID | None = None


@dataclass(frozen=True)
class ProductRead(ProductCreate, DomainReadSchema):
    updated_by_id: UUID | None = None


@dataclass(frozen=True)
class ProductUpdate(Product): ...
