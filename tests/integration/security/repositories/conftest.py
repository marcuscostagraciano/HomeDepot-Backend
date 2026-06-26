import pytest


@pytest.fixture
async def persisted_user(
    db_session,
    password_hasher,
):
    user = User(
        name="Test",
        email="Test@test.com",
        password=password_hasher.hash("123456"),
    )

    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    return user


@pytest.fixture
def auth_repository(
    db_session,
    password_hasher,
):
    return AuthRepository(
        session=db_session,
        password_hasher=password_hasher,
    )
