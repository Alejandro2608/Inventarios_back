from datetime import datetime
from app.domain.entities.movimiento_inventario import MovimientoInventario, TipoMovimiento
from app.domain.services.unit_of_work import UnitOfWork


class RegistrarEntradaProducto:
    """
    Caso de Uso: Registrar Entrada de Producto (RF4).

    RESPONSABILIDAD:
    - Registrar nuevas entradas de productos al inventario
    - Incrementar stock automáticamente
    - Mantener trazabilidad con movimientos (RN6)

    REGLAS APLICADAS:
    - RN6: Modificación de stock solo vía movimiento
    - RF4: Registrar entrada con proveedor, lote y bodega
    """

    def __init__(self, producto_repo, movimiento_repo, db):
        self.producto_repo = producto_repo
        self.movimiento_repo = movimiento_repo
        self.db = db

    def execute(self, producto_id: int, cantidad: int, proveedor: str = None, lote: str = None, bodega: str = None):
        """
        Ejecuta el registro de entrada de producto.

        Args:
            producto_id: ID del producto
            cantidad: Cantidad a ingresar
            proveedor: Proveedor del producto (opcional)
            lote: Número de lote (opcional, RF21)
            bodega: Bodega destino (opcional, RF9)

        Raises:
            ValueError: Si el producto no existe
        """
        with UnitOfWork(self.db):
            producto = self.producto_repo.obtener_por_id(producto_id)
            if not producto:
                raise ValueError("Producto no encontrado")

            producto.stock += cantidad
            producto.actualizar_stock(producto.stock)  # Valida RN2

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
