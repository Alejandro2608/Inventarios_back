from fastapi import APIRouter, Depends
from app.infrastructure.db.database import get_db
from app.infrastructure.repositories.producto_repository import ProductoRepository
from app.infrastructure.repositories.movimiento_repository import MovimientoRepository
from app.application.use_cases.registrar_entrada_producto import RegistrarEntradaProducto
from app.application.use_cases.registrar_salida_producto import RegistrarSalidaProducto

router = APIRouter(prefix="/inventario")

@router.post("/entrada")
def registrar_entrada(data: dict, db=Depends(get_db)):
    usecase = RegistrarEntradaProducto(
        ProductoRepository(db),
        MovimientoRepository(db),
        db
    )
    usecase.execute(**data)
    return {"msg": "Entrada registrada"}

@router.post("/salida")
def registrar_salida(data: dict, db=Depends(get_db)):
    usecase = RegistrarSalidaProducto(
        ProductoRepository(db),
        MovimientoRepository(db),
        db
    )
    usecase.execute(**data)
    return {"msg": "Salida registrada"}
