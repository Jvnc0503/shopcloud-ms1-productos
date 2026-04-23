from sqlalchemy.orm import Session
from src.models.producto import Producto
from src.schemas.producto import ProductoCreate

def get_productos(db: Session, skip: int = 0, limit: int = 100) -> list[Producto]:
    """Obtiene una lista paginada de productos."""
    return db.query(Producto).offset(skip).limit(limit).all()

def get_producto_by_id(db: Session, producto_id: int) -> Producto | None:
    """Busca un producto específico por su ID."""
    return db.query(Producto).filter(Producto.id == producto_id).first()

def create_producto(db: Session, producto: ProductoCreate) -> Producto:
    """Inserta un nuevo producto en la base de datos."""
    db_producto = Producto(
        nombre=producto.nombre,
        precio=producto.precio,
        stock=producto.stock,
        categoria_id=producto.categoria_id
    )
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto