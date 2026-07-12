"""Final targeted tests to push coverage past 95%."""

from uuid import UUID

from users.domain.schemas import UserCreate
from users.repositories.user_repository import UserRepository


async def test_user_repository_get_user_by_email_found(db_session):
    """user_repository.py: get_user_by_email found path (line 35)."""
    repo = UserRepository(db_session)
    payload = UserCreate(
        first_name="Test",
        last_name="User",
        email="found@test.com",
        password="12345678",
    )
    created = await repo.create(payload)
    found = await repo.get_user_by_email("found@test.com")
    assert found is not None
    assert found.id == created.id


async def test_user_repository_delete_not_found(db_session):
    """user_repository.py: delete not found path."""
    repo = UserRepository(db_session)
    result = await repo.delete(UUID("00000000-0000-0000-0000-000000000000"))
    assert result is None


async def test_user_repository_read_not_found(db_session):
    """user_repository.py: read not found path."""
    repo = UserRepository(db_session)
    result = await repo.read(UUID("00000000-0000-0000-0000-000000000000"))
    assert result is None
