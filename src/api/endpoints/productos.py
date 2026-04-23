from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database import get_db
from src.schemas.producto import ProductoCreate, ProductoResponse
from src.crud import crud_producto

router = APIRouter(prefix="/productos", tags=["Productos"])

@router.get("/", response_model=list[ProductoResponse])
def listar_productos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Retorna el listado de productos con paginación."""
    return crud_producto.get_productos(db, skip=skip, limit=limit)

@router.post("/", response_model=ProductoResponse, status_code=status.HTTP_201_CREATED)
def crear_producto(producto: ProductoCreate, db: Session = Depends(get_db)):
    """Crea un nuevo producto."""
    return crud_producto.create_producto(db, producto)

@router.get("/{producto_id}", response_model=ProductoResponse)
def detalle_producto(producto_id: int, db: Session = Depends(get_db)):
    """Obtiene los detalles de un producto. Lanza 404 si no existe."""
    db_producto = crud_producto.get_producto_by_id(db, producto_id)
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_producto