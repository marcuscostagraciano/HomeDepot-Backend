from dataclasses import dataclass

from .enums import SortFieldEnum, SortOrderEnum
from .errors import GreaterEqualError, OutsideLimitError


@dataclass(frozen=True)
class BaseFilter:
    page: int
    limit: int
    sort: SortFieldEnum
    order: SortOrderEnum

    def __post_init__(self):
        if self.page < 1:
            raise GreaterEqualError("page", 1)

        if not 1 <= self.limit <= 100:
            raise OutsideLimitError("limit", 1, 100)
