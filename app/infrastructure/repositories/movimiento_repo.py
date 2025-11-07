from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime
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

    def crear_movimiento(self, movimiento: MovimientoInventario, auto_commit: bool = True):
        """
        Registra un nuevo movimiento en la base de datos.

        Args:
            movimiento: Entidad de movimiento a registrar
            auto_commit: Si es True, hace commit automático.
                        Si es False, solo prepara el cambio (flush).
                        Usar False cuando se usa dentro de UnitOfWork (RNF6)
        """
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

        if auto_commit:
            self.db.commit()
            self.db.refresh(model)
        else:
            self.db.flush()  # Solo prepara, no guarda aún (para transacciones)

        return model

    def listar_movimientos(
        self,
        producto_id: Optional[int] = None,
        tipo: Optional[str] = None,
        fecha_desde: Optional[datetime] = None,
        fecha_hasta: Optional[datetime] = None,
        bodega: Optional[str] = None,
        page: int = 1,
        page_size: int = 50
    ) -> tuple[List[MovimientoInventarioModel], int]:
        """
        Lista movimientos con filtros opcionales y paginación (RNF1).

        Parámetros:
        - producto_id: Filtrar por producto específico
        - tipo: Filtrar por tipo (entrada/salida)
        - fecha_desde: Movimientos desde esta fecha
        - fecha_hasta: Movimientos hasta esta fecha
        - bodega: Filtrar por bodega
        - page: Página actual (1-indexed)
        - page_size: Elementos por página (default: 50)

        Returns:
            Tupla (movimientos, total) donde:
            - movimientos: Lista de movimientos de la página actual
            - total: Total de movimientos que cumplen los filtros
        """
        from sqlmodel import func

        # Construir query base con filtros
        statement = select(MovimientoInventarioModel)

        # Aplicar filtros
        if producto_id:
            statement = statement.where(MovimientoInventarioModel.producto_id == producto_id)
        if tipo:
            statement = statement.where(MovimientoInventarioModel.tipo == tipo)
        if fecha_desde:
            statement = statement.where(MovimientoInventarioModel.fecha >= fecha_desde)
        if fecha_hasta:
            statement = statement.where(MovimientoInventarioModel.fecha <= fecha_hasta)
        if bodega:
            statement = statement.where(MovimientoInventarioModel.bodega == bodega)

        # Contar total de resultados (sin paginación)
        count_statement = select(func.count()).select_from(MovimientoInventarioModel)
        if producto_id:
            count_statement = count_statement.where(MovimientoInventarioModel.producto_id == producto_id)
        if tipo:
            count_statement = count_statement.where(MovimientoInventarioModel.tipo == tipo)
        if fecha_desde:
            count_statement = count_statement.where(MovimientoInventarioModel.fecha >= fecha_desde)
        if fecha_hasta:
            count_statement = count_statement.where(MovimientoInventarioModel.fecha <= fecha_hasta)
        if bodega:
            count_statement = count_statement.where(MovimientoInventarioModel.bodega == bodega)

        total = self.db.exec(count_statement).one()

        # Ordenar por fecha descendente (más recientes primero)
        statement = statement.order_by(MovimientoInventarioModel.fecha.desc())

        # Aplicar paginación
        offset = (page - 1) * page_size
        statement = statement.offset(offset).limit(page_size)

        movimientos = self.db.exec(statement).all()
        return (list(movimientos), total)

    def obtener_movimientos_por_producto(self, producto_id: int, limit: int = 50) -> List[MovimientoInventarioModel]:
        """
        Obtiene el historial de movimientos de un producto especifico.
        Ordenados por fecha descendente (más recientes primero).
        """
        statement = select(MovimientoInventarioModel).where(
            MovimientoInventarioModel.producto_id == producto_id
        ).order_by(
            MovimientoInventarioModel.fecha.desc()
        ).limit(limit)

        movimientos = self.db.exec(statement).all()
        return list(movimientos)

    def contar_movimientos_hoy(self) -> int:
        """Cuenta cuántos movimientos se han registrado hoy."""
        from datetime import date
        hoy = date.today()

        statement = select(MovimientoInventarioModel).where(
            MovimientoInventarioModel.fecha >= datetime.combine(hoy, datetime.min.time())
        )

        movimientos = self.db.exec(statement).all()
        return len(movimientos)
