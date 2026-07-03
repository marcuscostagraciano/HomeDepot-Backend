from dataclasses import dataclass

from core.domain.filters import BaseFilter


@dataclass(frozen=True)
class ListFilters(BaseFilter):
    name: str | None
    observation: str | None
    bought: bool | None
