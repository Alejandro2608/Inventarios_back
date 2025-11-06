from datetime import datetime
from app.domain.entities.movimiento_inventario import MovimientoInventario, TipoMovimiento
from app.domain.services.unit_of_work import UnitOfWork


class RegistrarSalidaProducto:
    """
    Caso de Uso: Registrar Salida de Producto (RF5).

    RESPONSABILIDAD:
    - Registrar salidas de productos del inventario
    - Decrementar stock automáticamente
    - Validar stock disponible (RN2)
    - Mantener trazabilidad con movimientos (RN6)

    REGLAS APLICADAS:
    - RN2: Stock no puede ser negativo
    - RN6: Modificación de stock solo vía movimiento
    - RF5: Registrar salida por venta, ajuste o traslado
    """

    def __init__(self, producto_repo, movimiento_repo, db):
        self.producto_repo = producto_repo
        self.movimiento_repo = movimiento_repo
        self.db = db

    def execute(self, producto_id: int, cantidad: int, motivo: str = None, bodega: str = None):
        """
        Ejecuta el registro de salida de producto.

        Args:
            producto_id: ID del producto
            cantidad: Cantidad a retirar
            motivo: Motivo de la salida (venta, ajuste, traslado)
            bodega: Bodega origen (opcional, RF9)

        Raises:
            ValueError: Si el producto no existe
            ValueError: Si no hay stock suficiente (RN2)
        """
        with UnitOfWork(self.db):
            producto = self.producto_repo.obtener_por_id(producto_id)
            if not producto:
                raise ValueError("Producto no encontrado")

            # Validar stock disponible (RN2)
            if producto.stock < cantidad:
                raise ValueError(f"Stock insuficiente. Disponible: {producto.stock}, Solicitado: {cantidad} (RN2)")

            producto.stock -= cantidad
            producto.actualizar_stock(producto.stock)  # Valida RN2

            movimiento = MovimientoInventario(
                producto_id=producto_id,
                cantidad=-cantidad,  # Negativo para salidas
                tipo=TipoMovimiento.SALIDA,
                fecha=datetime.now(),
                motivo=motivo,
                bodega=bodega
            )

            self.movimiento_repo.crear_movimiento(movimiento)
            self.producto_repo.actualizar(producto)

