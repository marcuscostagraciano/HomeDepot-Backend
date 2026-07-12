"""List CRUD tests."""


async def test_create_list(client, user_token_headers):
    resp = await client.post(
        "/v1/lists/",
        json={"name": "Grocery", "observation": "Weekly"},
        headers=user_token_headers,
    )
    assert resp.status_code == 200
    assert resp.json()["name"] == "Grocery"


async def test_read_lists(client, user_token_headers):
    await client.post("/v1/lists/", json={"name": "A"}, headers=user_token_headers)
    await client.post("/v1/lists/", json={"name": "B"}, headers=user_token_headers)
    resp = await client.get("/v1/lists", headers=user_token_headers)
    assert resp.status_code == 200
    assert len(resp.json()) >= 2


async def test_read_list_by_id(client, user_token_headers):
    created = await client.post(
        "/v1/lists/", json={"name": "Mine"}, headers=user_token_headers
    )
    list_id = created.json()["id"]
    resp = await client.get(f"/v1/lists/{list_id}", headers=user_token_headers)
    assert resp.status_code == 200
    assert resp.json()["name"] == "Mine"


async def test_delete_list(client, user_token_headers):
    created = await client.post(
        "/v1/lists/", json={"name": "Del"}, headers=user_token_headers
    )
    list_id = created.json()["id"]
    resp = await client.delete(f"/v1/lists/{list_id}", headers=user_token_headers)
    assert resp.status_code == 200
