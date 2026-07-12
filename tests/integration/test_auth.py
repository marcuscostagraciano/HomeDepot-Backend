"""Authentication & token tests."""

from tests.integration.conftest import unique_email


async def test_login_successful(client):
    email = unique_email("l")
    await client.post(
        "/v1/users/",
        json={
            "first_name": "L",
            "last_name": "U",
            "email": email,
            "password": "12345678",
        },
    )
    resp = await client.post(
        "/v1/users/login",
        data={"username": email, "password": "12345678"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert data["token_type"] == "Bearer"


async def test_login_invalid_credentials(client):
    resp = await client.post(
        "/v1/users/login",
        data={"username": "no@test.com", "password": "wrong"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert resp.status_code == 401


async def test_read_me_with_token(client, user_token_headers):
    resp = await client.get("/v1/users/me", headers=user_token_headers)
    assert resp.status_code == 200
    assert resp.json()["email"] is not None


async def test_read_me_without_token(client):
    assert (await client.get("/v1/users/me")).status_code == 401
