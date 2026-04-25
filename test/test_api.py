from __future__ import annotations


def test_create_producto_requires_existing_categoria(client):
    response = client.post(
        "/productos/",
        json={
            "nombre": "Teclado mecanico",
            "precio": 129.99,
            "stock": 15,
            "categoria_id": 999,
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Categoría 999 no encontrada"


def test_list_endpoints_are_paged_and_ordered(client):
    categoria_1 = client.post("/categorias/", json={"nombre": "Perifericos"})
    categoria_2 = client.post("/categorias/", json={"nombre": "Audio"})
    assert categoria_1.status_code == 201
    assert categoria_2.status_code == 201

    producto_1 = client.post(
        "/productos/",
        json={
            "nombre": "Teclado mecanico",
            "precio": 129.99,
            "stock": 15,
            "categoria_id": categoria_1.json()["id"],
        },
    )
    producto_2 = client.post(
        "/productos/",
        json={
            "nombre": "Auriculares",
            "precio": 89.99,
            "stock": 8,
            "categoria_id": categoria_2.json()["id"],
        },
    )
    assert producto_1.status_code == 201
    assert producto_2.status_code == 201

    categorias = client.get("/categorias/?skip=1&limit=1")
    assert categorias.status_code == 200
    assert [item["id"] for item in categorias.json()] == [categoria_2.json()["id"]]

    productos = client.get("/productos/?skip=1&limit=1")
    assert productos.status_code == 200
    assert [item["id"] for item in productos.json()] == [producto_2.json()["id"]]


def test_missing_resources_return_404(client):
    categoria_get = client.get("/categorias/9999")
    assert categoria_get.status_code == 404
    assert categoria_get.json()["detail"] == "Categoría no encontrada"

    categoria_patch = client.patch("/categorias/9999", json={"nombre": "Nueva"})
    assert categoria_patch.status_code == 404
    assert categoria_patch.json()["detail"] == "Categoría no encontrada"

    producto_get = client.get("/productos/9999")
    assert producto_get.status_code == 404
    assert producto_get.json()["detail"] == "Producto no encontrado"

    producto_patch = client.patch("/productos/9999", json={"stock": 1})
    assert producto_patch.status_code == 404
    assert producto_patch.json()["detail"] == "Producto no encontrado"


def test_categoria_and_producto_patch_flow(client):
    categoria = client.post("/categorias/", json={"nombre": "Perifericos"})
    assert categoria.status_code == 201
    categoria_id = categoria.json()["id"]

    producto = client.post(
        "/productos/",
        json={
            "nombre": "Teclado mecanico",
            "precio": 129.99,
            "stock": 15,
            "categoria_id": categoria_id,
        },
    )
    assert producto.status_code == 201
    producto_id = producto.json()["id"]

    categoria_patch = client.patch(
        f"/categorias/{categoria_id}",
        json={"nombre": "Accesorios de PC"},
    )
    assert categoria_patch.status_code == 200
    assert categoria_patch.json()["nombre"] == "Accesorios de PC"

    producto_patch = client.patch(
        f"/productos/{producto_id}",
        json={"stock": 42},
    )
    assert producto_patch.status_code == 200
    assert producto_patch.json()["stock"] == 42
    assert producto_patch.json()["categoria_id"] == categoria_id

    producto_get = client.get(f"/productos/{producto_id}")
    assert producto_get.status_code == 200
    assert producto_get.json()["stock"] == 42

    categoria_get = client.get(f"/categorias/{categoria_id}")
    assert categoria_get.status_code == 200
    assert categoria_get.json()["nombre"] == "Accesorios de PC"