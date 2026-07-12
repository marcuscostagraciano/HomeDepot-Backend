from uuid import UUID

import pytest

from core.domain.errors import GreaterEqualError
from shared.list_products.domain.schemas import (
    ListProduct,
    ListProductCreate,
    ListProductRead,
    ListProductUpdate,
)


class TestListProduct:
    def test_valid(self) -> None:
        lp = ListProduct(
            list_id=UUID("11111111-1111-1111-1111-111111111111"),
            product_id=UUID("22222222-2222-2222-2222-222222222222"),
            quantity=2,
        )
        assert lp.quantity == 2
        assert lp.bought is False
        assert lp.notes is None

    def test_quantity_zero_raises(self) -> None:
        with pytest.raises(GreaterEqualError, match="quantity"):
            ListProduct(
                list_id=UUID("11111111-1111-1111-1111-111111111111"),
                product_id=UUID("22222222-2222-2222-2222-222222222222"),
                quantity=0,
            )

    def test_quantity_negative_raises(self) -> None:
        with pytest.raises(GreaterEqualError, match="quantity"):
            ListProduct(
                list_id=UUID("11111111-1111-1111-1111-111111111111"),
                product_id=UUID("22222222-2222-2222-2222-222222222222"),
                quantity=-1,
            )


class TestListProductCreate:
    def test_create(self) -> None:
        lp = ListProductCreate(
            list_id=UUID("11111111-1111-1111-1111-111111111111"),
            product_id=UUID("22222222-2222-2222-2222-222222222222"),
            quantity=1,
        )
        assert lp.quantity == 1


class TestListProductRead:
    def test_read(self) -> None:
        lp = ListProductRead(
            id=UUID("33333333-3333-3333-3333-333333333333"),
            created_date="2000-01-01",  # type: ignore
            updated_date=None,
            list_id=UUID("11111111-1111-1111-1111-111111111111"),
            product_id=UUID("22222222-2222-2222-2222-222222222222"),
            quantity=1,
        )
        assert lp.id == UUID("33333333-3333-3333-3333-333333333333")


class TestListProductUpdate:
    def test_all_none(self) -> None:
        update = ListProductUpdate()
        assert update.quantity is None
        assert update.bought is None
        assert update.notes is None

    def test_partial(self) -> None:
        update = ListProductUpdate(quantity=5, bought=True)
        assert update.quantity == 5
        assert update.bought is True
        assert update.notes is None
