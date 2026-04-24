from fastapi import FastAPI
from src.database import engine, Base
from src.api.endpoints import categoria, productos

# Genera las tablas en MySQL al arrancar si no existen 
# (En producción real usarías Alembic para migraciones)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ShopCloud - MS1 Productos",
    description="API de catálogo de productos e inventario",
    version="1.0.0"
)

# Incluir los endpoints separados
app.include_router(categoria.router)
app.include_router(productos.router)

@app.get("/")
def health_check():
    """Endpoint de salud para el Load Balancer"""
    return {"status": "ok", "service": "ms1-productos"} 