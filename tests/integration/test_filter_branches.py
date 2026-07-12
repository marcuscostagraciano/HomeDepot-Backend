"""Tests for repository filter branches via API."""

from tests.integration.conftest import unique_email


async def _create_user_and_login(client) -> tuple[str, dict]:
    email = unique_email("f")
    await client.post(
        "/v1/users/",
        json={
            "first_name": "F",
            "last_name": "U",
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
    return email, {"Authorization": f"Bearer {token}"}


async def test_list_filters_by_name(client):
    """list_repository.py: _apply_filters name branch (line 50)."""
    _, h = await _create_user_and_login(client)
    await client.post("/v1/lists/", json={"name": "Groceries"}, headers=h)
    await client.post("/v1/lists/", json={"name": "Hardware"}, headers=h)

    resp = await client.get("/v1/lists?name=Groc", headers=h)
    assert resp.status_code == 200
    assert len(resp.json()) >= 1


async def test_list_filters_by_bought(client):
    """list_repository.py: _apply_filters bought branch (lines 56-62)."""
    _, h = await _create_user_and_login(client)
    await client.post("/v1/lists/", json={"name": "BoughtList"}, headers=h)

    resp = await client.get("/v1/lists?bought=false", headers=h)
    assert resp.status_code == 200


async def test_product_filters_by_name(client):
    """product_repository.py: _apply_filters name branch (line 47)."""
    _, h = await _create_user_and_login(client)
    await client.post("/v1/products/", json={"name": "Hammer"}, headers=h)
    await client.post("/v1/products/", json={"name": "Drill"}, headers=h)

    resp = await client.get("/v1/products?name=Ham", headers=h)
    assert resp.status_code == 200
    assert len(resp.json()) >= 1


async def test_product_filters_by_brand(client):
    """product_repository.py: _apply_filters brand branch (line 53)."""
    _, h = await _create_user_and_login(client)
    await client.post("/v1/products/", json={"name": "Saw", "brand": "Acme"}, headers=h)

    resp = await client.get("/v1/products?brand=Acme", headers=h)
    assert resp.status_code == 200
    assert len(resp.json()) >= 1


async def test_list_share_read_by_user(client):
    """list_share_repository.py: read_by_user_and_list (lines 44-46)."""
    owner_email = unique_email("o2")
    shared_email = unique_email("s2")

    # Create owner
    await client.post(
        "/v1/users/",
        json={
            "first_name": "O",
            "last_name": "U",
            "email": owner_email,
            "password": "12345678",
        },
    )
    owner_login = await client.post(
        "/v1/users/login",
        data={"username": owner_email, "password": "12345678"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    owner_h = {"Authorization": f"Bearer {owner_login.json()['access_token']}"}

    # Create shared user
    shared_resp = await client.post(
        "/v1/users/",
        json={
            "first_name": "S",
            "last_name": "U",
            "email": shared_email,
            "password": "12345678",
        },
    )
    shared_id = shared_resp.json()["id"]
    shared_login = await client.post(
        "/v1/users/login",
        data={"username": shared_email, "password": "12345678"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    shared_h = {"Authorization": f"Bearer {shared_login.json()['access_token']}"}

    # Owner creates list and shares
    lst = (
        await client.post("/v1/lists/", json={"name": "SharedFilter"}, headers=owner_h)
    ).json()
    await client.post(
        "/v1/list-shares/",
        json={"user_id": shared_id, "list_id": lst["id"]},
        headers=owner_h,
    )

    # Shared user reads shared lists
    resp = await client.get("/v1/list-shares/", headers=shared_h)
    assert resp.status_code == 200
    assert len(resp.json()) >= 1


async def test_list_product_update_bought_and_notes(client):
    """list_product_repository.py: update with bought/notes (lines 59-64, 69)."""
    _, h = await _create_user_and_login(client)
    lst = (await client.post("/v1/lists/", json={"name": "LPUpdate"}, headers=h)).json()
    prod = (await client.post("/v1/products/", json={"name": "Item"}, headers=h)).json()
    await client.post(
        f"/v1/lists/{lst['id']}/products",
        json={"product_id": prod["id"], "quantity": 1},
        headers=h,
    )

    # Update with bought and notes
    resp = await client.patch(
        f"/v1/lists/{lst['id']}/products/{prod['id']}",
        json={"bought": True, "notes": "check this"},
        headers=h,
    )
    assert resp.status_code == 200
    assert resp.json()["bought"] is True
    assert resp.json()["notes"] == "check this"
