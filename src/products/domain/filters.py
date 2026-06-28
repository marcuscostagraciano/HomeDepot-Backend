from dataclasses import dataclass

from core.domain import BaseFilter


@dataclass(frozen=True)
class ProductFilters(BaseFilter):
    search: str | None
    brand: str | None
    min_price: float | None
    max_price: float | None
