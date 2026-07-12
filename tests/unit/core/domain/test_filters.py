import pytest

from core.domain.enums import SortFieldEnum, SortOrderEnum
from core.domain.errors import GreaterEqualError, OutsideLimitError
from core.domain.filters import BaseFilter
from lists.domain.filters import ListFilters


def test_base_filter_accepts_valid_values() -> None:
    filters = BaseFilter(
        page=1,
        limit=20,
        sort=SortFieldEnum.ID,
        order=SortOrderEnum.ASC,
    )

    assert filters.page == 1
    assert filters.limit == 20


@pytest.mark.parametrize(
    "page,limit,expected_exception",
    [
        (0, 20, GreaterEqualError),
        (1, 0, OutsideLimitError),
        (1, 101, OutsideLimitError),
    ],
)
def test_base_filter_raises_for_invalid_pagination(
    page: int,
    limit: int,
    expected_exception: type[Exception],
) -> None:
    with pytest.raises(expected_exception):
        BaseFilter(
            page=page,
            limit=limit,
            sort=SortFieldEnum.ID,
            order=SortOrderEnum.ASC,
        )


def test_list_filters_accepts_valid_values() -> None:
    filters = ListFilters(
        page=1,
        limit=20,
        sort=SortFieldEnum.ID,
        order=SortOrderEnum.ASC,
        name=None,
        observation=None,
        bought=None,
    )

    assert filters.page == 1
    assert filters.limit == 20
    assert filters.name is None
