from datetime import datetime
from app.domain.entities.movimiento_inventario import MovimientoInventario, TipoMovimiento
from app.application.services.unit_of_work import UnitOfWork


class RegistrarEntradaProducto:
    """
    Caso de Uso: Registrar Entrada de Producto (RF4)
    """

    def __init__(self, producto_repo, movimiento_repo, db):
        self.producto_repo = producto_repo
        self.movimiento_repo = movimiento_repo
        self.db = db

    def execute(self, producto_id, cantidad, proveedor, lote, bodega):
        with UnitOfWork(self.db):
            producto = self.producto_repo.obtener_por_id(producto_id)
            if not producto:
                raise Exception("Producto no encontrado")

            producto.stock += cantidad

            movimiento = MovimientoInventario(
                producto_id=producto_id,
                cantidad=cantidad,
                tipo=TipoMovimiento.ENTRADA,
                fecha=datetime.now(),
                proveedor=proveedor,
                lote=lote,
                bodega=bodega
            )

            self.movimiento_repo.crear_movimiento(movimiento)
            self.producto_repo.actualizar(producto)
