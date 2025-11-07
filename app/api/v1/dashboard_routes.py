# -*- coding: utf-8 -*-
"""
Endpoints de Dashboard - API REST

Proporciona estadísticas y resumen del sistema para la pantalla principal.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.infrastructure.db.database import get_session
from app.infrastructure.repositories.producto_repository import ProductoRepository
from app.infrastructure.repositories.movimiento_repo import MovimientoRepository
from app.infrastructure.db.models import ProductoModel
from app.application.dto.dashboard_dto import EstadisticasResponse


router = APIRouter(prefix="/api/v1/dashboard", tags=["Dashboard"])


# ============================================================================
# ENDPOINTS de Dashboard
# ============================================================================

@router.get("/estadisticas", response_model=EstadisticasResponse, summary="Estadísticas del sistema")
def obtener_estadisticas(
    stock_minimo: int = 10,
    db: Session = Depends(get_session)
):
    """
    Obtiene estadísticas generales del sistema para el dashboard.

    **Información que retorna:**
    - Total de productos registrados
    - Productos activos vs inactivos
    - Stock total en el inventario
    - Productos con stock bajo (alerta de reabastecimiento)
    - Movimientos registrados hoy
    - Valor total del inventario (suma de precio_compra * stock)

    **Parámetros:**
    - stock_minimo: Umbral para considerar stock bajo (default: 10)

    **Para qué sirve:**
    - Mostrar resumen ejecutivo en la pantalla principal
    - Identificar alertas de stock bajo (RF6, RF7)
    - Monitorear actividad diaria

    **Respuestas:**
    - 200: Estadísticas calculadas
    - 500: Error del servidor
    """
    try:
        producto_repo = ProductoRepository(db)
        movimiento_repo = MovimientoRepository(db)

        # 1. Total de productos
        todos_productos = producto_repo.listar_todos()
        total_productos = len(todos_productos)

        # 2. Productos activos vs inactivos
        productos_activos = len([p for p in todos_productos if p.estado == "Activo"])
        productos_inactivos = total_productos - productos_activos

        # 3. Stock total (suma de todas las unidades)
        stock_total = sum(p.stock for p in todos_productos)

        # 4. Productos con stock bajo (alerta)
        productos_stock_bajo = len([
            p for p in todos_productos
            if p.stock <= stock_minimo and p.estado == "Activo"
        ])

        # 5. Movimientos registrados hoy
        movimientos_hoy = movimiento_repo.contar_movimientos_hoy()

        # 6. Valor total del inventario (precio_compra * stock)
        valor_inventario = sum(
            p.precio_compra * p.stock for p in todos_productos
        )

        return EstadisticasResponse(
            total_productos=total_productos,
            productos_activos=productos_activos,
            productos_inactivos=productos_inactivos,
            stock_total=stock_total,
            productos_stock_bajo=productos_stock_bajo,
            movimientos_hoy=movimientos_hoy,
            valor_inventario=valor_inventario
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.get("/productos-stock-bajo", summary="Alertas de stock bajo (RF6, RF7)")
def obtener_productos_stock_bajo(
    stock_minimo: int = 10,
    db: Session = Depends(get_session)
):
    """
    Lista productos que necesitan reabastecimiento (stock bajo).

    **Para qué sirve:**
    - Generar alertas de reabastecimiento (RF7)
    - Identificar productos críticos
    - Planificar compras

    **Parámetros:**
    - stock_minimo: Umbral para considerar stock bajo (default: 10)

    **Respuestas:**
    - 200: Lista de productos con stock bajo
    - 500: Error del servidor
    """
    try:
        # Consulta directa para productos con stock bajo
        statement = select(ProductoModel).where(
            ProductoModel.stock <= stock_minimo,
            ProductoModel.estado == "Activo"
        ).order_by(ProductoModel.stock.asc())  # Ordenar por stock ascendente (más críticos primero)

        productos = db.exec(statement).all()

        # Convertir a formato de respuesta
        resultado = [
            {
                "id": p.id,
                "sku": p.sku,
                "nombre": p.nombre,
                "stock": p.stock,
                "tipo_licor": p.tipo_licor,
                "proveedor": p.proveedor
            }
            for p in productos
        ]

        return {
            "total_alertas": len(resultado),
            "productos": resultado
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
