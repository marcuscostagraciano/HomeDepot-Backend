from unittest.mock import AsyncMock
from uuid import UUID

import pytest

from core.domain.errors import ForbiddenError, NotFoundError
from lists.domain.filters import ListFilters
from lists.domain.schemas import ListCreate, ListRead
from lists.domain.use_cases import create_list, delete_list, read_list, read_lists


@pytest.fixture
def user_id() -> UUID:
    return UUID("11111111-1111-1111-1111-111111111111")


@pytest.fixture
def list_id() -> UUID:
    return UUID("22222222-2222-2222-2222-222222222222")


@pytest.fixture
def list_read(list_id: UUID, user_id: UUID) -> ListRead:
    return ListRead(
        id=list_id,
        created_date="2000-01-01",  # type: ignore
        updated_date=None,
        name="My List",
        observation=None,
        bought=False,
        created_by_id=user_id,
        updated_by_id=None,
    )


async def test_create_list(
    user_id: UUID,
) -> None:
    repository = AsyncMock()
    payload = ListCreate(name="My List", observation=None)
    expected = ListRead(
        id=UUID("22222222-2222-2222-2222-222222222222"),
        created_date="2000-01-01",  # type: ignore
        updated_date=None,
        name="My List",
        observation=None,
        bought=False,
        created_by_id=user_id,
        updated_by_id=None,
    )
    repository.create.return_value = expected

    result = await create_list(repository, payload, user_id)

    assert result.name == "My List"
    assert result.created_by_id == user_id
    repository.create.assert_awaited_once()


async def test_read_list_successful(
    list_id: UUID,
    user_id: UUID,
    list_read: ListRead,
) -> None:
    repository = AsyncMock()
    share_repository = AsyncMock()
    repository.read.return_value = list_read
    share_repository.read_by_user_and_list.return_value = None  # owner, no share needed

    result = await read_list(repository, share_repository, list_id, user_id)

    assert result.id == list_id
    repository.read.assert_awaited_once_with(list_id)


async def test_read_list_not_found(
    list_id: UUID,
    user_id: UUID,
) -> None:
    repository = AsyncMock()
    share_repository = AsyncMock()
    repository.read.return_value = None

    with pytest.raises(NotFoundError, match="List"):
        await read_list(repository, share_repository, list_id, user_id)


async def test_read_list_forbidden(
    list_id: UUID,
    user_id: UUID,
) -> None:
    other_user_id = UUID("33333333-3333-3333-3333-333333333333")
    repository = AsyncMock()
    share_repository = AsyncMock()
    repository.read.return_value = ListRead(
        id=list_id,
        created_date="2000-01-01",  # type: ignore
        updated_date=None,
        name="My List",
        observation=None,
        bought=False,
        created_by_id=other_user_id,
        updated_by_id=None,
    )
    share_repository.read_by_user_and_list.return_value = None

    with pytest.raises(ForbiddenError):
        await read_list(repository, share_repository, list_id, user_id)


async def test_read_lists(
    user_id: UUID,
    list_read: ListRead,
) -> None:
    repository = AsyncMock()
    filters = AsyncMock()
    repository.read_all_accessible.return_value = [list_read]

    result = await read_lists(repository, filters, user_id)

    assert len(result) == 1
    assert result[0].name == "My List"
    repository.read_all_accessible.assert_awaited_once_with(filters, user_id)


async def test_delete_list_as_owner(
    list_id: UUID,
    user_id: UUID,
    list_read: ListRead,
) -> None:
    repository = AsyncMock()
    share_repository = AsyncMock()
    repository.read.return_value = list_read
    repository.delete.return_value = list_read

    result = await delete_list(repository, share_repository, list_id, user_id)

    assert result.id == list_id
    repository.delete.assert_awaited_once_with(list_id)


async def test_delete_list_not_owner(
    list_id: UUID,
    user_id: UUID,
) -> None:
    other_user_id = UUID("33333333-3333-3333-3333-333333333333")
    repository = AsyncMock()
    share_repository = AsyncMock()
    repository.read.return_value = ListRead(
        id=list_id,
        created_date="2000-01-01",  # type: ignore
        updated_date=None,
        name="My List",
        observation=None,
        bought=False,
        created_by_id=other_user_id,
        updated_by_id=None,
    )

    with pytest.raises(ForbiddenError):
        await delete_list(repository, share_repository, list_id, user_id)


async def test_delete_list_not_found_after_delete(
    list_id: UUID,
    user_id: UUID,
    list_read: ListRead,
) -> None:
    repository = AsyncMock()
    share_repository = AsyncMock()
    repository.read.return_value = list_read
    repository.delete.return_value = None

    with pytest.raises(NotFoundError, match="List"):
        await delete_list(repository, share_repository, list_id, user_id)
