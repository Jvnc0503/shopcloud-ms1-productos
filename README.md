# ShopCloud - MS1 Productos

Microservicio de catalogo e inventario para ShopCloud, construido con FastAPI, SQLAlchemy y MySQL.

## Resumen

Este proyecto expone una API REST para gestionar productos. En el arranque, la aplicacion crea las tablas definidas en el modelo SQLAlchemy usando `Base.metadata.create_all(bind=engine)`.

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
│   │       └── productos.py
│   ├── crud/
│   │   └── crud_producto.py
│   ├── models/
│   │   └── producto.py
│   └── schemas/
│       └── producto.py
└── test/
```

## Caracteristicas

- API REST con FastAPI.
- Persistencia con SQLAlchemy.
- Conexion a MySQL usando `pymysql`.
- Configuracion por variables de entorno con `pydantic-settings`.
- Documentacion automatica de FastAPI en `/docs` y `/redoc`.

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

### Productos

- `GET /productos/` - Lista productos con paginacion (`skip`, `limit`).
- `POST /productos/` - Crea un producto.
- `GET /productos/{producto_id}` - Obtiene el detalle de un producto.

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

- `seed.py` esta vacio y todavia no carga datos de prueba.
- La carpeta `test/` esta vacia y no existen pruebas automatizadas.
- El modelo `Producto` referencia una tabla `categorias`, por lo que el esquema de categorias debe existir en la base de datos antes de insertar productos.

## Notas de implementacion

- `src/config.py` construye `DATABASE_URL` a partir de las variables de entorno.
- `src/database.py` crea el engine y la sesion de SQLAlchemy.
- `src/main.py` registra el router de productos y expone un endpoint de salud.

## Siguientes pasos sugeridos

1. Agregar el modelo, esquema y CRUD de categorias.
2. Crear pruebas para los endpoints principales.
3. Implementar `seed.py` con datos iniciales.
