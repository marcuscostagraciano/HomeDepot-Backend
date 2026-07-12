"""List sharing tests."""

from tests.integration.conftest import unique_email


async def test_share_list(client):
    owner_email = unique_email("o")
    shared_email = unique_email("s")

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

    lst = (
        await client.post("/v1/lists/", json={"name": "Shared"}, headers=owner_h)
    ).json()

    share_resp = await client.post(
        "/v1/list-shares/",
        json={"user_id": shared_id, "list_id": lst["id"]},
        headers=owner_h,
    )
    assert share_resp.status_code == 200

    my = await client.get("/v1/list-shares/", headers=shared_h)
    assert my.status_code == 200
    assert len(my.json()) >= 1

    read = await client.get(f"/v1/lists/{lst['id']}", headers=shared_h)
    assert read.status_code == 200

    del_resp = await client.delete(
        f"/v1/list-shares/{lst['id']}/users/{shared_id}",
        headers=owner_h,
    )
    assert del_resp.status_code == 200
