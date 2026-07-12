from unittest.mock import AsyncMock
from uuid import UUID

import pytest

from core.domain.errors import NotFoundError, RequiredFieldMissingError
from products.domain.filters import ProductFilters
from products.domain.schemas import ProductCreate, ProductRead
from products.domain.use_cases import create_product, read_product, read_products


@pytest.fixture
def user_id() -> UUID:
    return UUID("11111111-1111-1111-1111-111111111111")


@pytest.fixture
def product_id() -> UUID:
    return UUID("22222222-2222-2222-2222-222222222222")


async def test_create_product_successful(user_id: UUID) -> None:
    repository = AsyncMock()
    payload = ProductCreate(name="Hammer", brand="Acme", description=None)
    expected = ProductRead(
        id=UUID("22222222-2222-2222-2222-222222222222"),
        created_date="2000-01-01",  # type: ignore
        updated_date=None,
        name="Hammer",
        brand="Acme",
        description=None,
        created_by_id=user_id,
        updated_by_id=None,
    )
    repository.create.return_value = expected

    result = await create_product(repository, payload, user_id)

    assert result.name == "Hammer"
    repository.create.assert_awaited_once_with(payload, creator_id=user_id)


async def test_create_product_missing_name(user_id: UUID) -> None:
    repository = AsyncMock()
    payload = ProductCreate(name="", brand="Acme", description=None)

    with pytest.raises(RequiredFieldMissingError, match="name"):
        await create_product(repository, payload, user_id)

    repository.create.assert_not_called()


async def test_read_product_successful(product_id: UUID) -> None:
    repository = AsyncMock()
    expected = ProductRead(
        id=product_id,
        created_date="2000-01-01",  # type: ignore
        updated_date=None,
        name="Hammer",
        brand="Acme",
        description=None,
        created_by_id=UUID("11111111-1111-1111-1111-111111111111"),
        updated_by_id=None,
    )
    repository.read.return_value = expected

    result = await read_product(repository, product_id)

    assert result.id == product_id
    repository.read.assert_awaited_once_with(product_id)


async def test_read_product_not_found(product_id: UUID) -> None:
    repository = AsyncMock()
    repository.read.return_value = None

    with pytest.raises(NotFoundError, match="Product"):
        await read_product(repository, product_id)


async def test_read_products() -> None:
    repository = AsyncMock()
    filters = AsyncMock()
    repository.read_all.return_value = []

    result = await read_products(repository, filters)

    assert result == []
    repository.read_all.assert_awaited_once_with(filters)
