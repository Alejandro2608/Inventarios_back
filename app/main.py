from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.settings import settings
from app.infrastructure.db.database import create_db_and_tables
from app.api.v1 import inventario_routes, productos_routes, dashboard_routes
import webbrowser
import threading


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Sistema de Inventarios para Licorería LicoCastillo - Arquitectura Hexagonal"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def open_browser():
    """Abre el navegador con la documentación Swagger después de 1.5 segundos."""
    import time
    time.sleep(1.5)
    webbrowser.open("http://localhost:8000/docs")


@app.on_event("startup")
def on_startup():
    """
    Evento que se ejecuta al iniciar la aplicación.
    Inicializa la base de datos y abre el navegador automáticamente.
    """
    print(">> Inicializando sistema de inventarios...")
    create_db_and_tables()
    print(">> Base de datos inicializada")
    print(f">> {settings.app_name} v{settings.app_version} - LISTO")
    print(">> Abriendo documentación Swagger en el navegador...")

    # Abrir el navegador en un hilo separado
    threading.Thread(target=open_browser, daemon=True).start()


@app.get("/", tags=["Health"])
def root():
    """Endpoint raíz para verificar que el servidor está funcionando."""
    return {
        "mensaje": "Sistema de Inventarios LicoCastillo",
        "version": settings.app_version,
        "status": "operativo",
        "arquitectura": "Hexagonal (Puertos y Adaptadores)"
    }


@app.get("/health", tags=["Health"])
def health_check():
    """Endpoint de salud para monitoreo (RNF12)."""
    return {
        "status": "healthy",
        "database": "sqlite",
        "database_url": settings.database_url
    }


# Registrar routers de la API v1
app.include_router(productos_routes.router)
app.include_router(inventario_routes.router)
app.include_router(dashboard_routes.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Recarga automática en desarrollo
        log_level="info"
    )
