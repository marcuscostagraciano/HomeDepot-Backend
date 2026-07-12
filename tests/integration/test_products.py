"""Product CRUD tests."""


async def test_create_product(client, user_token_headers):
    resp = await client.post(
        "/v1/products/",
        json={"name": "Hammer", "brand": "Acme"},
        headers=user_token_headers,
    )
    assert resp.status_code == 200
    assert resp.json()["name"] == "Hammer"


async def test_read_products(client, user_token_headers):
    await client.post("/v1/products/", json={"name": "A"}, headers=user_token_headers)
    await client.post("/v1/products/", json={"name": "B"}, headers=user_token_headers)
    resp = await client.get("/v1/products", headers=user_token_headers)
    assert resp.status_code == 200
    assert len(resp.json()) >= 2


async def test_read_product_by_id(client, user_token_headers):
    created = await client.post(
        "/v1/products/", json={"name": "Saw"}, headers=user_token_headers
    )
    pid = created.json()["id"]
    resp = await client.get(f"/v1/products/{pid}", headers=user_token_headers)
    assert resp.status_code == 200
    assert resp.json()["name"] == "Saw"
