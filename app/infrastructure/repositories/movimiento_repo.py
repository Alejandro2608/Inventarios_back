from sqlmodel import Session
from app.domain.entities.movimiento_inventario import MovimientoInventario
from app.infrastructure.db.models import MovimientoInventarioModel


class MovimientoRepository:
    """
    Repositorio para gestionar movimientos de inventario.

    RESPONSABILIDAD:
    - Persistir movimientos de entrada/salida en BD
    - Implementar trazabilidad de operaciones (RF8, RF16)

    REGLAS APLICADAS:
    - RN6: Todo cambio de stock requiere movimiento
    """

    def __init__(self, db: Session):
        self.db = db

    def crear_movimiento(self, movimiento: MovimientoInventario):
        """Registra un nuevo movimiento en la base de datos."""
        model = MovimientoInventarioModel(
            producto_id=movimiento.producto_id,
            cantidad=movimiento.cantidad,
            tipo=movimiento.tipo.value,  # Convierte Enum a string
            fecha=movimiento.fecha,
            proveedor=movimiento.proveedor,
            lote=movimiento.lote,
            bodega=movimiento.bodega,
            motivo=movimiento.motivo
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return model
