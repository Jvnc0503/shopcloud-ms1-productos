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