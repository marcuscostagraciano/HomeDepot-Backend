"""Targeted tests for remaining uncovered lines."""

from uuid import UUID

from core.config.settings import Settings
from db.db import create_db_and_tables
from lists.domain.filters import ListFilters
from lists.repositories.list_repository import ListRepository
from products.domain.filters import ProductFilters
from products.repositories.product_repository import ProductRepository
from shared.domain.types import AssociationIdVO
from shared.list_products.domain.schemas import ListProductUpdate
from shared.list_products.repositories.list_product_repository import (
    ListProductRepository,
)
from shared.list_shares.repositories.list_share_repository import ListShareRepository
from users.adapters.jwt_service import JWTService, get_jwt_service
from users.repositories.user_repository import UserRepository, get_user_repository


async def test_get_user_repository_function(db_session):
    """user_repository.py: get_user_repository (line 58)."""
    repo = get_user_repository(db_session)
    assert isinstance(repo, UserRepository)


async def test_get_user_by_email_not_found(db_session):
    """user_repository.py: get_user_by_email None branch (line 35)."""
    repo = UserRepository(db_session)
    assert await repo.get_user_by_email("nonexistent@test.com") is None


async def test_check_email_exists_false(db_session):
    """user_repository.py: check_email_exists (lines 42-43)."""
    repo = UserRepository(db_session)
    assert await repo.check_email_exists("missing@test.com") is False


async def test_dependencies_user_not_found(client):
    """dependencies.py: user not found (lines 36-42)."""
    jwt_service = JWTService(Settings())
    token = jwt_service.generate({"email": "ghost@test.com"}).access_token
    resp = await client.get(
        "/v1/users/me", headers={"Authorization": f"Bearer {token}"}
    )
    assert resp.status_code == 401


async def test_dependencies_missing_email_in_token(client):
    """dependencies.py: email missing from payload (line 29)."""
    jwt_service = JWTService(Settings())
    token = jwt_service.generate({"sub": "no-email"}).access_token
    resp = await client.get(
        "/v1/users/me", headers={"Authorization": f"Bearer {token}"}
    )
    assert resp.status_code == 401


def test_get_jwt_service():
    """jwt_service.py: get_jwt_service factory."""
    svc = get_jwt_service()
    assert svc is not None


async def test_create_db_and_tables():
    """db.py: create_db_and_tables (lines 13-14)."""
    await create_db_and_tables()


async def test_list_repository_read_all_empty(db_session):
    """list_repository.py: read_all with no lists (line 50)."""
    repo = ListRepository(db_session)
    filters = ListFilters(
        page=1,
        limit=20,
        name=None,
        observation=None,
        bought=None,
        sort="id",
        order="asc",
    )  # type: ignore
    assert await repo.read_all(filters) == []


async def test_list_repository_read_all_accessible_empty(db_session):
    """list_repository.py: read_all_accessible (lines 96, 99, 102, 105)."""
    repo = ListRepository(db_session)
    uid = UUID("11111111-1111-1111-1111-111111111111")
    filters = ListFilters(
        page=1,
        limit=20,
        name=None,
        observation=None,
        bought=None,
        sort="id",
        order="asc",
    )  # type: ignore
    assert await repo.read_all_accessible(filters, uid) == []


async def test_product_repository_read_all_empty(db_session):
    """product_repository.py: read_all with no products (lines 47, 53, 56, 59)."""
    repo = ProductRepository(db_session)
    filters = ProductFilters(
        page=1,
        limit=20,
        name=None,
        brand=None,
        min_price=None,
        max_price=None,
        sort="id",
        order="asc",
    )  # type: ignore
    assert await repo.read_all(filters) == []


async def test_list_share_repository_read_not_found(db_session):
    """list_share_repository.py: read not found (lines 31-32)."""
    repo = ListShareRepository(db_session)
    z = UUID("00000000-0000-0000-0000-000000000000")
    assert await repo.read(AssociationIdVO(z, z)) is None


async def test_list_share_repository_delete_not_found(db_session):
    """list_share_repository.py: delete not found (line 52)."""
    repo = ListShareRepository(db_session)
    z = UUID("00000000-0000-0000-0000-000000000000")
    assert await repo.delete(AssociationIdVO(z, z)) is None


async def test_list_product_repository_read_not_found(db_session):
    """list_product_repository.py: read not found (lines 33-34)."""
    repo = ListProductRepository(db_session)
    z = UUID("00000000-0000-0000-0000-000000000000")
    assert await repo.read(AssociationIdVO(z, z)) is None


async def test_list_product_repository_update_not_found(db_session):
    """list_product_repository.py: update not found (line 40)."""
    repo = ListProductRepository(db_session)
    z = UUID("00000000-0000-0000-0000-000000000000")
    assert (
        await repo.update(AssociationIdVO(z, z), ListProductUpdate(quantity=5)) is None
    )


async def test_list_product_repository_delete_not_found(db_session):
    """list_product_repository.py: delete not found (line 48)."""
    repo = ListProductRepository(db_session)
    z = UUID("00000000-0000-0000-0000-000000000000")
    assert await repo.delete(AssociationIdVO(z, z)) is None
