from unittest.mock import AsyncMock
from uuid import UUID

import pytest

from core.domain.errors import ForbiddenError, NotFoundError
from shared.domain.types import AssociationIdVO
from shared.list_shares.domain.schemas import UserListCreate, UserListRead
from shared.list_shares.domain.use_cases import (
    read_shared_lists,
    remove_share,
    share_list,
    validate_user_access_to_list,
)


@pytest.fixture
def user_id() -> UUID:
    return UUID("11111111-1111-1111-1111-111111111111")


@pytest.fixture
def list_id() -> UUID:
    return UUID("22222222-2222-2222-2222-222222222222")


@pytest.fixture
def list_read(list_id: UUID, user_id: UUID) -> AsyncMock:
    obj = AsyncMock()
    obj.id = list_id
    obj.created_by_id = user_id
    return obj


async def test_share_list_successful(
    user_id: UUID,
    list_id: UUID,
    list_read: AsyncMock,
) -> None:
    repository = AsyncMock()
    list_repository = AsyncMock()
    user_repository = AsyncMock()
    payload = UserListCreate(
        user_id=UUID("33333333-3333-3333-3333-333333333333"), list_id=list_id
    )

    list_repository.read.return_value = list_read
    user_repository.read.return_value = AsyncMock()
    repository.read_by_user_and_list.return_value = None
    repository.create.return_value = AsyncMock()

    result = await share_list(
        repository, list_repository, user_repository, payload, user_id
    )

    assert result is not None
    list_repository.read.assert_awaited_once_with(payload.list_id)
    user_repository.read.assert_awaited_once_with(payload.user_id)
    repository.create.assert_awaited_once_with(payload)


async def test_share_list_list_not_found(
    user_id: UUID,
    list_id: UUID,
) -> None:
    repository = AsyncMock()
    list_repository = AsyncMock()
    user_repository = AsyncMock()
    payload = UserListCreate(
        user_id=UUID("33333333-3333-3333-3333-333333333333"), list_id=list_id
    )

    list_repository.read.return_value = None

    with pytest.raises(NotFoundError, match="List"):
        await share_list(repository, list_repository, user_repository, payload, user_id)


async def test_share_list_forbidden(
    user_id: UUID,
    list_id: UUID,
    list_read: AsyncMock,
) -> None:
    repository = AsyncMock()
    list_repository = AsyncMock()
    user_repository = AsyncMock()
    payload = UserListCreate(
        user_id=UUID("33333333-3333-3333-3333-333333333333"), list_id=list_id
    )

    list_read.created_by_id = UUID("99999999-9999-9999-9999-999999999999")
    list_repository.read.return_value = list_read

    with pytest.raises(ForbiddenError):
        await share_list(repository, list_repository, user_repository, payload, user_id)


async def test_share_list_user_not_found(
    user_id: UUID,
    list_id: UUID,
    list_read: AsyncMock,
) -> None:
    repository = AsyncMock()
    list_repository = AsyncMock()
    user_repository = AsyncMock()
    payload = UserListCreate(
        user_id=UUID("33333333-3333-3333-3333-333333333333"), list_id=list_id
    )

    list_repository.read.return_value = list_read
    user_repository.read.return_value = None

    with pytest.raises(NotFoundError, match="User"):
        await share_list(repository, list_repository, user_repository, payload, user_id)


async def test_share_list_already_shared(
    user_id: UUID,
    list_id: UUID,
    list_read: AsyncMock,
) -> None:
    repository = AsyncMock()
    list_repository = AsyncMock()
    user_repository = AsyncMock()
    payload = UserListCreate(
        user_id=UUID("33333333-3333-3333-3333-333333333333"), list_id=list_id
    )
    existing = AsyncMock()

    list_repository.read.return_value = list_read
    user_repository.read.return_value = AsyncMock()
    repository.read_by_user_and_list.return_value = existing

    result = await share_list(
        repository, list_repository, user_repository, payload, user_id
    )

    assert result == existing
    repository.create.assert_not_called()


async def test_read_shared_lists(user_id: UUID) -> None:
    repository = AsyncMock()
    repository.read_all_by_user.return_value = []

    result = await read_shared_lists(repository, user_id)

    assert result == []
    repository.read_all_by_user.assert_awaited_once_with(user_id)


async def test_validate_user_access_to_list_as_owner(
    list_id: UUID,
    user_id: UUID,
    list_read: AsyncMock,
) -> None:
    repository = AsyncMock()
    list_repository = AsyncMock()
    list_repository.read.return_value = list_read

    result = await validate_user_access_to_list(
        repository, list_repository, list_id, user_id
    )

    assert result == list_read
    repository.read_by_user_and_list.assert_not_called()


async def test_validate_user_access_to_list_as_shared(
    list_id: UUID,
    user_id: UUID,
    list_read: AsyncMock,
) -> None:
    repository = AsyncMock()
    list_repository = AsyncMock()
    list_read.created_by_id = UUID("99999999-9999-9999-9999-999999999999")
    list_repository.read.return_value = list_read
    repository.read_by_user_and_list.return_value = AsyncMock()

    result = await validate_user_access_to_list(
        repository, list_repository, list_id, user_id
    )

    assert result == list_read
    repository.read_by_user_and_list.assert_awaited_once_with(user_id, list_id)


async def test_validate_user_access_to_list_forbidden(
    list_id: UUID,
    user_id: UUID,
    list_read: AsyncMock,
) -> None:
    repository = AsyncMock()
    list_repository = AsyncMock()
    list_read.created_by_id = UUID("99999999-9999-9999-9999-999999999999")
    list_repository.read.return_value = list_read
    repository.read_by_user_and_list.return_value = None

    with pytest.raises(ForbiddenError):
        await validate_user_access_to_list(
            repository, list_repository, list_id, user_id
        )


async def test_remove_share_as_owner(
    user_id: UUID,
    list_id: UUID,
    list_read: AsyncMock,
) -> None:
    repository = AsyncMock()
    list_repository = AsyncMock()
    list_repository.read.return_value = list_read
    repository.read_by_user_and_list.return_value = AsyncMock()
    repository.delete.return_value = AsyncMock()
    association_id = AssociationIdVO(
        UUID("33333333-3333-3333-3333-333333333333"), list_id
    )

    result = await remove_share(repository, list_repository, user_id, association_id)

    assert result is not None
    repository.delete.assert_awaited_once_with(association_id)


async def test_remove_share_as_self(
    user_id: UUID,
    list_id: UUID,
    list_read: AsyncMock,
) -> None:
    repository = AsyncMock()
    list_repository = AsyncMock()
    list_read.created_by_id = UUID("99999999-9999-9999-9999-999999999999")
    list_repository.read.return_value = list_read
    repository.read_by_user_and_list.return_value = AsyncMock()
    repository.delete.return_value = AsyncMock()
    association_id = AssociationIdVO(user_id, list_id)

    result = await remove_share(repository, list_repository, user_id, association_id)

    assert result is not None
    repository.delete.assert_awaited_once_with(association_id)


async def test_remove_share_list_not_found(
    user_id: UUID,
    list_id: UUID,
) -> None:
    repository = AsyncMock()
    list_repository = AsyncMock()
    list_repository.read.return_value = None
    association_id = AssociationIdVO(
        UUID("33333333-3333-3333-3333-333333333333"), list_id
    )

    with pytest.raises(NotFoundError, match="List"):
        await remove_share(repository, list_repository, user_id, association_id)


async def test_remove_share_forbidden(
    user_id: UUID,
    list_id: UUID,
    list_read: AsyncMock,
) -> None:
    repository = AsyncMock()
    list_repository = AsyncMock()
    list_read.created_by_id = UUID("99999999-9999-9999-9999-999999999999")
    list_repository.read.return_value = list_read
    association_id = AssociationIdVO(
        UUID("33333333-3333-3333-3333-333333333333"), list_id
    )

    with pytest.raises(ForbiddenError):
        await remove_share(repository, list_repository, user_id, association_id)


async def test_remove_share_existing_not_found(
    user_id: UUID,
    list_id: UUID,
    list_read: AsyncMock,
) -> None:
    repository = AsyncMock()
    list_repository = AsyncMock()
    list_repository.read.return_value = list_read
    repository.read_by_user_and_list.return_value = None
    association_id = AssociationIdVO(
        UUID("33333333-3333-3333-3333-333333333333"), list_id
    )

    with pytest.raises(NotFoundError, match="ListShare"):
        await remove_share(repository, list_repository, user_id, association_id)


async def test_remove_share_delete_returns_none(
    user_id: UUID,
    list_id: UUID,
    list_read: AsyncMock,
) -> None:
    repository = AsyncMock()
    list_repository = AsyncMock()
    list_repository.read.return_value = list_read
    repository.read_by_user_and_list.return_value = AsyncMock()
    repository.delete.return_value = None
    association_id = AssociationIdVO(
        UUID("33333333-3333-3333-3333-333333333333"), list_id
    )

    with pytest.raises(NotFoundError, match="ListShare"):
        await remove_share(repository, list_repository, user_id, association_id)
