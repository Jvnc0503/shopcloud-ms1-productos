from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from functools import lru_cache

class Settings(BaseSettings):
    """
    Clase central para la configuración del microservicio.
    Pydantic leerá automáticamente las variables de entorno o el archivo .env.
    Si falta una variable obligatoria, la aplicación no arrancará (Fail Fast).
    """
    # Configuración General
    ENVIRONMENT: str = Field(default="development", description="Entorno actual")
    DEBUG: bool = Field(default=False, description="Activa el modo debug de FastAPI y SQLAlchemy")

    # Credenciales de Base de Datos
    DATABASE_URL_VALUE: str | None = Field(default=None, validation_alias="DATABASE_URL")
    DB_HOST: str = Field(default="127.0.0.1", description="Host de la base de datos MySQL")
    DB_PORT: int = Field(default=3306, description="Puerto de MySQL")
    DB_USER: str = Field(default="root", description="Usuario de MySQL")
    DB_PASSWORD: str = Field(default="secret_password_aqui", description="Contraseña de MySQL")
    DB_NAME: str = Field(default="shopcloud_productos", description="Nombre de la base de datos")

    # Configuración para que Pydantic sepa dónde buscar el archivo .env
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        # Ignora variables extra en el .env que no estén definidas en esta clase
        extra="ignore" 
    )

    @property
    def DATABASE_URL(self) -> str:
        """
        Construye dinámicamente la cadena de conexión de SQLAlchemy.
        Usa el driver 'mysql+pymysql' que definimos en requirements.txt.
        """
        if self.DATABASE_URL_VALUE:
            return self.DATABASE_URL_VALUE
        return (
            f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )
    
@lru_cache()
def get_settings() -> Settings:
    """
    Devuelve la instancia de configuración. 
    @lru_cache asegura que Pydantic lea el archivo .env solo la primera vez.
    """
    return Settings()