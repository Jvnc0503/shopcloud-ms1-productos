from __future__ import annotations

from src.crud.crud_producto import create_producto
from src.schemas.producto import ProductoCreate


def test_crud_create_producto_rejects_missing_categoria(db_session):
    producto = ProductoCreate(
        nombre="Mouse",
        precio=49.99,
        stock=10,
        categoria_id=12345,
    )

    try:
        create_producto(db_session, producto)
        raised = False
    except ValueError as exc:
        raised = True
        assert str(exc) == "Categoría 12345 no encontrada"

    assert raised is True