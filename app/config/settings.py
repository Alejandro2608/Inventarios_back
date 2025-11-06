# -*- coding: utf-8 -*-
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Configuracion de la aplicacion.

    RESPONSABILIDAD:
    - Centralizar todas las variables de configuracion
    - Leer variables de entorno desde .env
    - Proporcionar valores por defecto

    PRINCIPIOS APLICADOS:
    - RA14: Gestion de configuracion externa
    - No hardcodear valores sensibles
    - Facilitar cambio entre entornos (dev, test, prod)

    VARIABLES:
    - database_url: URL de conexion a la base de datos
      * SQLite para desarrollo local
      * PostgreSQL para produccion
    """

    database_url: str = "sqlite:///inventarios.db"
    app_name: str = "Inventarios LicoCastillo"
    app_version: str = "1.0.0"

    class Config:
        """
        Configuracion de Pydantic Settings.

        env_file: Lee variables desde archivo .env
        """
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
