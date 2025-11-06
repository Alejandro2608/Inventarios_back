from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from pydantic import BaseModel
from app.infrastructure.db.database import get_session
from app.infrastructure.repositories.producto_repository import ProductoRepository
from app.infrastructure.repositories.movimiento_repo import MovimientoRepository
from app.application.use_cases.registrar_entrada_producto import RegistrarEntradaProducto
from app.application.use_cases.registrar_salida_producto import RegistrarSalidaProducto

router = APIRouter(prefix="/api/v1/inventario", tags=["Inventario"])


class EntradaProductoRequest(BaseModel):
    """DTO para registrar entrada de producto (RF4)."""
    producto_id: int
    cantidad: int
    proveedor: str | None = None
    lote: str | None = None
    bodega: str | None = None


class SalidaProductoRequest(BaseModel):
    """DTO para registrar salida de producto (RF5)."""
    producto_id: int
    cantidad: int
    motivo: str | None = None
    bodega: str | None = None


@router.post("/entrada", summary="Registrar entrada de producto (RF4)")
def registrar_entrada(data: EntradaProductoRequest, db: Session = Depends(get_session)):
    """
    Registra una entrada de producto al inventario.

    Incrementa el stock del producto y crea un registro de movimiento.

    Reglas aplicadas:
    - RN6: Modificación de stock solo vía movimiento
    - RF4: Registro de entrada con trazabilidad
    """
    try:
        usecase = RegistrarEntradaProducto(
            ProductoRepository(db),
            MovimientoRepository(db),
            db
        )
        usecase.execute(
            producto_id=data.producto_id,
            cantidad=data.cantidad,
            proveedor=data.proveedor,
            lote=data.lote,
            bodega=data.bodega
        )
        return {"mensaje": "Entrada registrada exitosamente", "producto_id": data.producto_id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.post("/salida", summary="Registrar salida de producto (RF5)")
def registrar_salida(data: SalidaProductoRequest, db: Session = Depends(get_session)):
    """
    Registra una salida de producto del inventario.

    Decrementa el stock del producto y crea un registro de movimiento.

    Reglas aplicadas:
    - RN2: Stock no puede ser negativo (valida disponibilidad)
    - RN6: Modificación de stock solo vía movimiento
    - RF5: Registro de salida con motivo
    """
    try:
        usecase = RegistrarSalidaProducto(
            ProductoRepository(db),
            MovimientoRepository(db),
            db
        )
        usecase.execute(
            producto_id=data.producto_id,
            cantidad=data.cantidad,
            motivo=data.motivo,
            bodega=data.bodega
        )
        return {"mensaje": "Salida registrada exitosamente", "producto_id": data.producto_id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
