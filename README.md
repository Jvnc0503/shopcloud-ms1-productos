# ShopCloud - MS1 Productos

Microservicio de catalogo e inventario para ShopCloud, construido con FastAPI, SQLAlchemy y MySQL.

## Resumen

Este proyecto expone una API REST para gestionar productos y categorias. En el arranque, la aplicacion crea las tablas definidas en el modelo SQLAlchemy usando `Base.metadata.create_all(bind=engine)`.

La suite automatizada valida el flujo principal de categorias y productos, la validacion de relaciones y la actualizacion parcial por `PATCH`.

## Estructura actual

```text
.
├── Dockerfile
├── README.md
├── requirements.txt
├── seed.py
├── src/
│   ├── config.py
│   ├── database.py
│   ├── main.py
│   ├── api/
│   │   └── endpoints/
│   │       ├── categoria.py
│   │       └── productos.py
│   ├── crud/
│   │   ├── crud_categoria.py
│   │   └── crud_producto.py
│   ├── models/
│   │   ├── categoria.py
│   │   └── producto.py
│   └── schemas/
│       ├── categoria.py
│       └── producto.py
└── test/
```

## Caracteristicas

- API REST con FastAPI.
- Persistencia con SQLAlchemy.
- Conexion a MySQL usando `pymysql`.
- Configuracion por variables de entorno con `pydantic-settings`.
- Documentacion automatica de FastAPI en `/docs` y `/redoc`.
- CRUD de categorias y productos con relaciones entre ambos modelos.

## Requisitos

- Python 3.11+ recomendado.
- MySQL 8 o compatible.
- Dependencias listadas en `requirements.txt`.

## Configuracion

1. Copia el archivo de ejemplo:

```bash
cp .env.example .env
```

2. Ajusta las variables de entorno segun tu entorno local o contenedor:

| Variable | Descripcion | Valor por defecto |
| --- | --- | --- |
| `ENVIRONMENT` | Entorno de ejecucion | `development` |
| `DEBUG` | Activa logs y consulta SQL | `True` |
| `DB_HOST` | Host de MySQL | `127.0.0.1` |
| `DB_PORT` | Puerto de MySQL | `3306` |
| `DB_USER` | Usuario de MySQL | `root` |
| `DB_PASSWORD` | Clave de MySQL | `secret_password_aqui` |
| `DB_NAME` | Nombre de la base de datos | `shopcloud_productos` |
| `DATABASE_URL` | Sobrescribe la cadena completa de conexión | _vacío_ |

## Ejecucion local

Instala dependencias:

```bash
pip install -r requirements.txt
```

Arranca la aplicacion:

```bash
uvicorn src.main:app --host 0.0.0.0 --port 8001 --reload
```

La API quedara disponible en:

- `http://localhost:8001`
- `http://localhost:8001/docs`
- `http://localhost:8001/redoc`

Ejecuta la suite de pruebas localmente:

```bash
pytest -q
```

## Flujo operativo local

1. Levanta MySQL en tu máquina o con Docker.

```bash
docker run -d --name shopcloud-mysql \
	-e MYSQL_ROOT_PASSWORD=secret_password_aqui \
	-e MYSQL_DATABASE=shopcloud_productos \
	-p 3306:3306 \
	mysql:8.0
```

2. Verifica que `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD` y `DB_NAME` coincidan con tu entorno.

3. Carga la data inicial.

```bash
python seed.py
```

El script inserta las 10 categorias base y genera 20,000 productos ficticios en lotes para reducir el tiempo de carga.

4. Arranca el servicio.

```bash
uvicorn src.main:app --host 0.0.0.0 --port 8001 --reload
```

5. Valida el contrato.

- Abre `http://localhost:8001/docs` para probar Swagger.
- Importa `openapi.yml` en Postman si prefieres colecciones externas.
- Usa `postman_collection.json` como colección de arranque.

6. Ejecuta la suite de pruebas.

```bash
pytest
```

## Integracion continua

El repositorio incluye un workflow de GitHub Actions en [.github/workflows/ci.yml](.github/workflows/ci.yml) que instala dependencias y ejecuta `pytest` en cada `push` y `pull_request`.

## Ejecucion con Docker

Construye la imagen:

```bash
docker build -t shopcloud-ms1-productos .
```

Ejecuta el contenedor:

```bash
docker run --rm -p 8001:8001 --env-file .env shopcloud-ms1-productos
```

## Endpoints

### Health check

- `GET /`

Respuesta:

```json
{ "status": "ok", "service": "ms1-productos" }
```

### Categorias

- `GET /categorias/` - Lista categorias con paginacion (`skip`, `limit`).
- `POST /categorias/` - Crea una categoria.
- `GET /categorias/{categoria_id}` - Obtiene el detalle de una categoria.
- `PATCH /categorias/{categoria_id}` - Actualiza parcialmente una categoria.

Ejemplo de payload para crear una categoria:

```json
{
	"nombre": "Perifericos"
}
```

### Productos

- `GET /productos/` - Lista productos con paginacion (`skip`, `limit`).
- `POST /productos/` - Crea un producto.
- `GET /productos/{producto_id}` - Obtiene el detalle de un producto.
- `PATCH /productos/{producto_id}` - Actualiza el stock de un producto.

Ejemplo de payload para crear un producto:

```json
{
	"nombre": "Teclado mecanico",
	"precio": 129.99,
	"stock": 15,
	"categoria_id": 1
}
```

## Estado actual del proyecto

- `seed.py` genera categorias base y productos ficticios para la carga masiva.
- La carpeta `test/` contiene pruebas automatizadas del contrato y la logica de relaciones.
- El modelo `Producto` referencia una tabla `categorias`, por lo que la base debe tener categorias creadas antes de insertar productos.
- Las listas de categorias y productos se entregan ordenadas por `id` para que la paginacion sea determinista.

## Notas de implementacion

- `src/config.py` construye `DATABASE_URL` a partir de las variables de entorno.
- `src/database.py` crea el engine y la sesion de SQLAlchemy.
- `src/main.py` registra los routers de categorias y productos, ademas del endpoint de salud.

## Siguientes pasos sugeridos

2. Sustituir `Base.metadata.create_all` por migraciones con Alembic.
