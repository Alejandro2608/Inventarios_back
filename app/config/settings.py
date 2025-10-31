from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Configuraci�n de la aplicaci�n.

    RESPONSABILIDAD:
    - Centralizar todas las variables de configuraci�n
    - Leer variables de entorno desde .env
    - Proporcionar valores por defecto

    PRINCIPIOS APLICADOS:
    - RA14: Gesti�n de configuraci�n externa
    - No hardcodear valores sensibles
    - Facilitar cambio entre entornos (dev, test, prod)

    VARIABLES:
    - database_url: URL de conexi�n a la base de datos
      * SQLite para desarrollo local
      * PostgreSQL para producci�n
    """

    database_url: str = "sqlite:///inventarios.db"
    app_name: str = "Inventarios LicoCastillo"
    app_version: str = "1.0.0"

    class Config:
        """
        Configuraci�n de Pydantic Settings.

        env_file: Lee variables desde archivo .env
        """
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
