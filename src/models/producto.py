from sqlalchemy import Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from src.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.categoria import Categoria

class Producto(Base):
    # Nombre exacto de la tabla en MySQL
    __tablename__ = "productos"

    # Definición de columnas
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    categoria_id: Mapped[int] = mapped_column(ForeignKey("categorias.id"), nullable=False)
    nombre: Mapped[str] = mapped_column(String(150), index=True, nullable=False)
    precio: Mapped[float] = mapped_column(Float, nullable=False)
    stock: Mapped[int] = mapped_column(Integer, default=0)
    creado_en: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Relación con la tabla categorías
    categoria: Mapped["Categoria"] = relationship(back_populates="productos")