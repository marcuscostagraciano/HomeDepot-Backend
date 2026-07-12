"""User registration & validation tests."""

from tests.integration.conftest import unique_email


async def test_create_user(client):
    email = unique_email("j")
    resp = await client.post(
        "/v1/users/",
        json={
            "first_name": "John",
            "last_name": "Doe",
            "email": email,
            "password": "12345678",
        },
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["email"] == email
    assert "id" in data


async def test_create_user_duplicate_email(client):
    email = unique_email("j2")
    payload = {
        "first_name": "Jane",
        "last_name": "Doe",
        "email": email,
        "password": "12345678",
    }
    assert (await client.post("/v1/users/", json=payload)).status_code == 200
    assert (await client.post("/v1/users/", json=payload)).status_code == 409


async def test_create_user_short_password(client):
    resp = await client.post(
        "/v1/users/",
        json={
            "first_name": "J",
            "last_name": "D",
            "email": unique_email("s"),
            "password": "123",
        },
    )
    assert resp.status_code == 422
