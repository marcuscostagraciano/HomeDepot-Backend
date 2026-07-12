from unittest.mock import AsyncMock
from uuid import UUID

import pytest

from core.domain.errors import NotFoundError
from shared.domain.types import AssociationIdVO
from shared.list_products.domain.schemas import (
    ListProduct,
    ListProductCreate,
    ListProductUpdate,
)
from shared.list_products.domain.use_cases import (
    add_product_to_list,
    delete_list_product,
    read_list_products,
    update_list_product,
)


@pytest.fixture
def user_id() -> UUID:
    return UUID("11111111-1111-1111-1111-111111111111")


@pytest.fixture
def list_id() -> UUID:
    return UUID("22222222-2222-2222-2222-222222222222")


@pytest.fixture
def product_id() -> UUID:
    return UUID("33333333-3333-3333-3333-333333333333")


@pytest.fixture
def list_read(list_id: UUID, user_id: UUID) -> AsyncMock:
    obj = AsyncMock()
    obj.id = list_id
    obj.created_by_id = user_id
    return obj


async def test_add_product_to_list_successful(
    user_id: UUID,
    list_id: UUID,
    product_id: UUID,
    list_read: AsyncMock,
) -> None:
    repository = AsyncMock()
    list_repository = AsyncMock()
    product_repository = AsyncMock()
    share_repository = AsyncMock()
    payload = ListProductCreate(list_id=list_id, product_id=product_id, quantity=2)

    list_repository.read.return_value = list_read
    product_repository.read.return_value = AsyncMock()
    repository.create.return_value = AsyncMock()

    result = await add_product_to_list(
        repository,
        list_repository,
        product_repository,
        share_repository,
        payload,
        user_id,
    )

    assert result is not None
    product_repository.read.assert_awaited_once_with(product_id)
    repository.create.assert_awaited_once_with(payload)


async def test_add_product_to_list_product_not_found(
    user_id: UUID,
    list_id: UUID,
    product_id: UUID,
    list_read: AsyncMock,
) -> None:
    repository = AsyncMock()
    list_repository = AsyncMock()
    product_repository = AsyncMock()
    share_repository = AsyncMock()
    payload = ListProductCreate(list_id=list_id, product_id=product_id, quantity=2)

    list_repository.read.return_value = list_read
    product_repository.read.return_value = None

    with pytest.raises(NotFoundError, match="Product"):
        await add_product_to_list(
            repository,
            list_repository,
            product_repository,
            share_repository,
            payload,
            user_id,
        )


async def test_read_list_products(
    user_id: UUID,
    list_id: UUID,
    list_read: AsyncMock,
) -> None:
    repository = AsyncMock()
    list_repository = AsyncMock()
    share_repository = AsyncMock()

    list_repository.read.return_value = list_read
    repository.read_all_by_list.return_value = []

    result = await read_list_products(
        repository, list_repository, share_repository, list_id, user_id
    )

    assert result == []
    repository.read_all_by_list.assert_awaited_once_with(list_id)


async def test_update_list_product_successful(
    user_id: UUID,
    list_id: UUID,
    product_id: UUID,
    list_read: AsyncMock,
) -> None:
    repository = AsyncMock()
    list_repository = AsyncMock()
    share_repository = AsyncMock()
    id_vo = AssociationIdVO(list_id, product_id)
    payload = ListProductUpdate(quantity=3)

    list_repository.read.return_value = list_read
    repository.update.return_value = AsyncMock()

    result = await update_list_product(
        repository, list_repository, share_repository, id_vo, payload, user_id
    )

    assert result is not None
    repository.update.assert_awaited_once_with(id_vo, payload)


async def test_update_list_product_not_found(
    user_id: UUID,
    list_id: UUID,
    product_id: UUID,
    list_read: AsyncMock,
) -> None:
    repository = AsyncMock()
    list_repository = AsyncMock()
    share_repository = AsyncMock()
    id_vo = AssociationIdVO(list_id, product_id)
    payload = ListProductUpdate(quantity=3)

    list_repository.read.return_value = list_read
    repository.update.return_value = None

    with pytest.raises(NotFoundError, match="ListProduct"):
        await update_list_product(
            repository, list_repository, share_repository, id_vo, payload, user_id
        )


async def test_delete_list_product_successful(
    user_id: UUID,
    list_id: UUID,
    product_id: UUID,
    list_read: AsyncMock,
) -> None:
    repository = AsyncMock()
    list_repository = AsyncMock()
    share_repository = AsyncMock()
    id_vo = AssociationIdVO(list_id, product_id)

    list_repository.read.return_value = list_read
    repository.delete.return_value = AsyncMock()

    result = await delete_list_product(
        repository, list_repository, share_repository, id_vo, user_id
    )

    assert result is not None
    repository.delete.assert_awaited_once_with(id_vo)


async def test_delete_list_product_not_found(
    user_id: UUID,
    list_id: UUID,
    product_id: UUID,
    list_read: AsyncMock,
) -> None:
    repository = AsyncMock()
    list_repository = AsyncMock()
    share_repository = AsyncMock()
    id_vo = AssociationIdVO(list_id, product_id)

    list_repository.read.return_value = list_read
    repository.delete.return_value = None

    with pytest.raises(NotFoundError, match="ListProduct"):
        await delete_list_product(
            repository, list_repository, share_repository, id_vo, user_id
        )
