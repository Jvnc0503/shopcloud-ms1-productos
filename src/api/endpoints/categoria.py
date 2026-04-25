from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database import get_db
from src.schemas.categoria import CategoriaCreate, CategoriaResponse, CategoriaUpdate
from src.crud import crud_categoria

router = APIRouter(prefix="/categorias", tags=["Categorías"])

@router.get("/", response_model=list[CategoriaResponse])
def listar_categorias(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Retorna el listado de categorías con paginación."""
    return crud_categoria.get_categorias(db, skip=skip, limit=limit)

@router.post("/", response_model=CategoriaResponse, status_code=status.HTTP_201_CREATED)
def crear_categoria(categoria: CategoriaCreate, db: Session = Depends(get_db)):
    """Crea una nueva categoría."""
    return crud_categoria.create_categoria(db, categoria)

@router.get("/{categoria_id}", response_model=CategoriaResponse)
def obtener_categoria(categoria_id: int, db: Session = Depends(get_db)):
    """Obtiene los detalles de una categoría. Lanza 404 si no existe."""
    db_categoria = crud_categoria.get_categoria_by_id(db, categoria_id)
    if db_categoria is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return db_categoria

@router.patch("/{categoria_id}", response_model=CategoriaResponse)
def actualizar_categoria(categoria_id: int, categoria_data: CategoriaUpdate, db: Session = Depends(get_db)):
    """Actualiza parcialmente una categoría existente. Lanza 404 si no se encuentra."""
    updated_categoria = crud_categoria.update_categoria(db, categoria_id, categoria_data)
    if updated_categoria is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return updated_categoria