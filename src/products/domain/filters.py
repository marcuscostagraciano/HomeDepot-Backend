from dataclasses import dataclass

from core.domain.filters import BaseFilter


@dataclass(frozen=True)
class ProductFilters(BaseFilter):
    name: str | None
    brand: str | None
    min_price: float | None
    max_price: float | None
