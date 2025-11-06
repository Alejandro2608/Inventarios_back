# -*- coding: utf-8 -*-
from sqlmodel import create_engine, Session, SQLModel
from app.config.settings import settings


engine = create_engine(
    settings.database_url,
    echo=True
)


def create_db_and_tables():
    """
    Crea todas las tablas en la base de datos.

    RESPONSABILIDAD:
    - Inicializar el esquema de la base de datos
    - Crear tablas basadas en los modelos SQLModel

    CUANDO SE EJECUTA:
    - Al iniciar la aplicacion (evento startup de FastAPI)
    - Solo crea tablas si no existen

    Ejemplo:
        create_db_and_tables()  # Crea tabla 'productos' si no existe
    """
    from app.infrastructure.db.models import ProductoModel, MovimientoInventarioModel
    SQLModel.metadata.create_all(engine)


def get_session():
    """
    Generador de sesiones de base de datos.

    RESPONSABILIDAD:
    - Proporcionar una sesion de BD por request
    - Garantizar que la sesion se cierre correctamente

    USO EN FASTAPI:
    - Se usa con Depends() para inyeccion de dependencias
    - Cada endpoint recibe su propia sesion

    PATRON:
    - Context Manager (with statement)
    - Garantiza limpieza de recursos

    Ejemplo:
        @app.get("/productos")
        def listar(session: Session = Depends(get_session)):
            productos = session.exec(select(Producto)).all()
            return productos
    """
    with Session(engine) as session:
        yield session
