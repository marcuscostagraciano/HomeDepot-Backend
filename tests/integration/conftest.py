from typing import AsyncGenerator
from uuid import uuid4

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from core.models.base import BaseModel
from db.db import get_async_session
from main import app

TEST_DB_URL = "sqlite+aiosqlite://"


def unique_email(prefix: str = "u") -> str:
    return f"{prefix}{uuid4().hex[:8]}@test.com"


@pytest_asyncio.fixture(scope="function")
async def db_sessionmaker() -> async_sessionmaker[AsyncSession]:
    """Create engine + tables, return a sessionmaker for the test."""
    test_engine = create_async_engine(TEST_DB_URL, echo=False)
    maker = async_sessionmaker(test_engine, expire_on_commit=False)

    async with test_engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)

    yield maker

    async with test_engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)

    await test_engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def db_session(
    db_sessionmaker: async_sessionmaker[AsyncSession],
) -> AsyncGenerator[AsyncSession, None]:
    """Provide a session for direct DB access in tests."""
    async with db_sessionmaker() as session:
        yield session


@pytest_asyncio.fixture(scope="function")
async def client(
    db_sessionmaker: async_sessionmaker[AsyncSession],
) -> AsyncGenerator[AsyncClient, None]:
    """Override DB dependency to create a fresh session per request."""

    async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
        async with db_sessionmaker() as session:
            yield session

    app.dependency_overrides[get_async_session] = override_get_async_session

    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url="http://test", follow_redirects=True
    ) as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest_asyncio.fixture(scope="function")
async def user_token_headers(
    client: AsyncClient,
) -> dict[str, str]:
    """Create a user, login, return Authorization headers."""
    email = unique_email("u")
    await client.post(
        "/v1/users/",
        json={
            "first_name": "Test",
            "last_name": "User",
            "email": email,
            "password": "12345678",
        },
    )
    login = await client.post(
        "/v1/users/login",
        data={"username": email, "password": "12345678"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    token = login.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="function")
def anyio_backend():
    return "asyncio"
