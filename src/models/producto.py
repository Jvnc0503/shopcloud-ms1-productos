from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.database import Base

class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=False)
    nombre = Column(String(150), index=True, nullable=False)
    precio = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    creado_en = Column(DateTime(timezone=True), server_default=func.now())

    # Relación con la tabla categorías (asumiendo que crearás models/categoria.py)
    categoria = relationship("Categoria", back_populates="productos")