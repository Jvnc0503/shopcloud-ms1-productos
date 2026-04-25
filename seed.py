"""Seed data for MS1 productos.

Genera categorias base y 20,000 productos ficticios para cumplir con el
requisito de carga masiva del proyecto.
"""

from __future__ import annotations

import random

from faker import Faker
from sqlalchemy import func

from src.config import get_settings
from src.database import Base, SessionLocal, engine
from src.models.categoria import Categoria
from src.models.producto import Producto


faker = Faker("es_ES")
settings = get_settings()


def ensure_categorias(db) -> list[Categoria]:
	categorias = db.query(Categoria).order_by(Categoria.id).all()
	if categorias:
		return categorias

	nombres = [
		"Accesorios",
		"Audio",
		"Computo",
		"Gaming",
		"Hogar",
		"Moviles",
		"Oficina",
		"Perifericos",
		"Redes",
		"Software",
	]
	categorias = [Categoria(nombre=nombre) for nombre in nombres]
	db.add_all(categorias)
	db.commit()
	for categoria in categorias:
		db.refresh(categoria)
	return categorias


def seed_productos(db, categorias: list[Categoria], total: int = 20_000) -> int:
	existentes = db.query(func.count(Producto.id)).scalar() or 0
	if existentes >= total:
		return 0

	categorias_ids = [categoria.id for categoria in categorias]
	productos: list[Producto] = []
	for _ in range(total - existentes):
		productos.append(
			Producto(
				categoria_id=random.choice(categorias_ids),
				nombre=faker.word().title(),
				precio=round(random.uniform(5, 500), 2),
				stock=random.randint(0, 300),
			)
		)

	db.add_all(productos)
	db.commit()
	return len(productos)


def main() -> None:
	Base.metadata.create_all(bind=engine)
	db = SessionLocal()
	try:
		categorias = ensure_categorias(db)
		inserted = seed_productos(db, categorias)
		print(
			f"Seed completado para {settings.DB_NAME}: "
			f"{len(categorias)} categorias, {inserted} productos nuevos"
		)
	finally:
		db.close()


if __name__ == "__main__":
	main()
