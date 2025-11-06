# -*- coding: utf-8 -*-
"""
Script para inicializar la base de datos.

PROPOSITO:
- Crear el archivo de base de datos SQLite
- Crear todas las tablas segun los modelos
- Verificar que todo este correctamente configurado

USO:
    python init_db.py
"""

from app.infrastructure.db.database import create_db_and_tables
from app.config.settings import settings

if __name__ == "__main__":
    print("=" * 60)
    print("INICIALIZANDO BASE DE DATOS")
    print("=" * 60)
    print(f"Base de datos: {settings.database_url}")
    print("Creando tablas...")

    try:
        create_db_and_tables()
        print("OK - Tablas creadas exitosamente:")
        print("   - productos")
        print("   - movimientos_inventario")
        print("=" * 60)
        print("Base de datos lista para usar")
        print("=" * 60)
    except Exception as e:
        print(f"ERROR al crear la base de datos: {e}")
        import traceback
        traceback.print_exc()
