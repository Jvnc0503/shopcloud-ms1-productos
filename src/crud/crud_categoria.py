from sqlalchemy.orm import Session
from src.models.categoria import Categoria
from src.schemas.categoria import CategoriaCreate

def get_categorias(db: Session, skip: int = 0, limit: int = 100) -> list[Categoria]:
    """Obtiene una lista paginada de categorías."""
    return db.query(Categoria).offset(skip).limit(limit).all()

def get_categoria_by_id(db: Session, categoria_id: int) -> Categoria | None:
    """Busca una categoría específica por su ID."""
    return db.query(Categoria).filter(Categoria.id == categoria_id).first()

def create_categoria(db: Session, categoria: CategoriaCreate) -> Categoria:
    """Inserta una nueva categoría en la base de datos."""
    db_categoria = Categoria(nombre=categoria.nombre)
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria