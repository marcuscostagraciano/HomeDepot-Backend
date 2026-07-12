from datetime import datetime
from uuid import UUID

from core.domain.schemas import DomainReadSchema
from users.domain.schemas.users import UserRead, UserUpdate


def test_user_read_from_dataclass() -> None:
    user = UserRead(
        id=UUID("11111111-1111-1111-1111-111111111111"),
        created_date=datetime(2000, 1, 1),
        updated_date=None,
        first_name="John",
        last_name="Doe",
        email="john@test.com",
        password="hashed",
    )
    assert isinstance(user, DomainReadSchema)
    assert user.email == "john@test.com"
    assert user.updated_date is None


def test_user_update_all_none() -> None:
    update = UserUpdate()
    assert update.first_name is None
    assert update.last_name is None
    assert update.email is None
    assert update.password is None


def test_user_update_partial() -> None:
    update = UserUpdate(first_name="Jane")
    assert update.first_name == "Jane"
    assert update.last_name is None
