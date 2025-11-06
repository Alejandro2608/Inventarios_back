from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel, Field, Session, create_engine, select

app = FastAPI(title="Inventarios LicoCastillo")

# Base de datos SQLite
sqlite_url = "sqlite:///inventarios.db"
engine = create_engine(sqlite_url)

# Modelo
class Producto(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    sku: str = Field(index=True, unique=True)
    nombre: str
    precio_compra: float
    precio_venta: float
    stock: int
    estado: str = "Activo"

# Crear tablas
@app.on_event("startup")
def startup():
    SQLModel.metadata.create_all(engine)

# Endpoint para registrar producto
@app.post("/api/v1/productos")
def crear_producto(producto: Producto):
    with Session(engine) as session:
        # verificar SKU único
        existente = session.exec(select(Producto).where(Producto.sku == producto.sku)).first()
        if existente:
            raise HTTPException(status_code=409, detail="SKU ya existe")

        session.add(producto)
        session.commit()
        session.refresh(producto)
        return producto
from typing import List

@app.get("/api/v1/inventario", response_model=List[Producto])
def listar_productos():
    with Session(engine) as session:
        productos = session.exec(select(Producto)).all()
        return productos
