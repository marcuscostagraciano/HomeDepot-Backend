"""List-Product association tests."""


async def test_add_product_to_list(client, user_token_headers):
    h = user_token_headers
    lst = (await client.post("/v1/lists/", json={"name": "S"}, headers=h)).json()
    prod = (await client.post("/v1/products/", json={"name": "Milk"}, headers=h)).json()

    resp = await client.post(
        f"/v1/lists/{lst['id']}/products",
        json={"product_id": prod["id"], "quantity": 2},
        headers=h,
    )
    assert resp.status_code == 200
    assert resp.json()["quantity"] == 2


async def test_read_list_products(client, user_token_headers):
    h = user_token_headers
    lst = (await client.post("/v1/lists/", json={"name": "S2"}, headers=h)).json()
    p1 = (await client.post("/v1/products/", json={"name": "P1"}, headers=h)).json()
    p2 = (await client.post("/v1/products/", json={"name": "P2"}, headers=h)).json()
    await client.post(
        f"/v1/lists/{lst['id']}/products",
        json={"product_id": p1["id"], "quantity": 1},
        headers=h,
    )
    await client.post(
        f"/v1/lists/{lst['id']}/products",
        json={"product_id": p2["id"], "quantity": 2},
        headers=h,
    )

    resp = await client.get(f"/v1/lists/{lst['id']}/products", headers=h)
    assert resp.status_code == 200
    assert len(resp.json()) == 2


async def test_update_list_product(client, user_token_headers):
    h = user_token_headers
    lst = (await client.post("/v1/lists/", json={"name": "U"}, headers=h)).json()
    prod = (await client.post("/v1/products/", json={"name": "Upd"}, headers=h)).json()
    await client.post(
        f"/v1/lists/{lst['id']}/products",
        json={"product_id": prod["id"], "quantity": 1},
        headers=h,
    )

    resp = await client.patch(
        f"/v1/lists/{lst['id']}/products/{prod['id']}",
        json={"quantity": 5},
        headers=h,
    )
    assert resp.status_code == 200
    assert resp.json()["quantity"] == 5


async def test_delete_list_product(client, user_token_headers):
    h = user_token_headers
    lst = (await client.post("/v1/lists/", json={"name": "D"}, headers=h)).json()
    prod = (await client.post("/v1/products/", json={"name": "Del"}, headers=h)).json()
    await client.post(
        f"/v1/lists/{lst['id']}/products",
        json={"product_id": prod["id"], "quantity": 1},
        headers=h,
    )

    resp = await client.delete(
        f"/v1/lists/{lst['id']}/products/{prod['id']}", headers=h
    )
    assert resp.status_code == 200
