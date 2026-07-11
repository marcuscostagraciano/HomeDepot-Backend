from dataclasses import dataclass
from uuid import UUID

from core.domain.errors import GreaterEqualError
from core.domain.schemas import DomainCreateSchema, DomainReadSchema, DomainSchema


@dataclass(frozen=True)
class ListProduct(DomainSchema):
    list_id: UUID
    product_id: UUID
    quantity: int
    bought: bool = False
    notes: str | None = None

    def __post_init__(self):
        if self.quantity < 1:
            raise GreaterEqualError(
                field_name="quantity",
                value=1,
            )


@dataclass(frozen=True)
class ListProductCreate(ListProduct, DomainCreateSchema): ...


@dataclass(frozen=True)
class ListProductRead(ListProduct, DomainReadSchema): ...


@dataclass(frozen=True)
class ListProductUpdate(DomainSchema):
    quantity: int | None = None
    bought: bool | None = None
    notes: str | None = None
