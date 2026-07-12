from uuid import UUID

from shared.list_shares.domain.schemas import UserList, UserListCreate, UserListRead


class TestUserList:
    def test_valid(self) -> None:
        ul = UserList(
            user_id=UUID("11111111-1111-1111-1111-111111111111"),
            list_id=UUID("22222222-2222-2222-2222-222222222222"),
        )
        assert ul.user_id == UUID("11111111-1111-1111-1111-111111111111")
        assert ul.list_id == UUID("22222222-2222-2222-2222-222222222222")


class TestUserListCreate:
    def test_create(self) -> None:
        ul = UserListCreate(
            user_id=UUID("11111111-1111-1111-1111-111111111111"),
            list_id=UUID("22222222-2222-2222-2222-222222222222"),
        )
        assert ul.user_id == UUID("11111111-1111-1111-1111-111111111111")


class TestUserListRead:
    def test_read(self) -> None:
        ul = UserListRead(
            id=UUID("33333333-3333-3333-3333-333333333333"),
            created_date="2000-01-01",  # type: ignore
            updated_date=None,
            user_id=UUID("11111111-1111-1111-1111-111111111111"),
            list_id=UUID("22222222-2222-2222-2222-222222222222"),
        )
        assert ul.id == UUID("33333333-3333-3333-3333-333333333333")
