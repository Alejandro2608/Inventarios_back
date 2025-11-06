from sqlalchemy.orm import Session
from app.domain.entities.movimiento_inventario import MovimientoInventario
from app.infrastructure.db.models import MovimientoInventarioModel

class MovimientoRepository:

    def __init__(self, db: Session):
        self.db = db

    def crear_movimiento(self, movimiento: MovimientoInventario):
        model = MovimientoInventarioModel(
            producto_id=movimiento.producto_id,
            cantidad=movimiento.cantidad,
            tipo=movimiento.tipo,
            fecha=movimiento.fecha,
            proveedor=movimiento.proveedor,
            lote=movimiento.lote,
            bodega=movimiento.bodega,
            motivo=movimiento.motivo
        )
        self.db.add(model)
