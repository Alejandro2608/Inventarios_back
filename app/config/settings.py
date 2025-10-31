from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Configuración de la aplicación.

    RESPONSABILIDAD:
    - Centralizar todas las variables de configuración
    - Leer variables de entorno desde .env
    - Proporcionar valores por defecto

    PRINCIPIOS APLICADOS:
    - RA14: Gestión de configuración externa
    - No hardcodear valores sensibles
    - Facilitar cambio entre entornos (dev, test, prod)

    VARIABLES:
    - database_url: URL de conexión a la base de datos
      * SQLite para desarrollo local
      * PostgreSQL para producción
    """

    database_url: str = "sqlite:///inventarios.db"
    app_name: str = "Inventarios LicoCastillo"
    app_version: str = "1.0.0"

    class Config:
        """
        Configuración de Pydantic Settings.

        env_file: Lee variables desde archivo .env
        """
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
