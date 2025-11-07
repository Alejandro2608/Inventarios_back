# -*- coding: utf-8 -*-
"""
Endpoints de Inventario (Movimientos) - API REST

Maneja las entradas y salidas de productos en el inventario.
Cada movimiento queda registrado para trazabilidad completa.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from typing import List, Optional
from app.infrastructure.db.database import get_session
from app.infrastructure.repositories.producto_repository import ProductoRepository
from app.infrastructure.repositories.movimiento_repo import MovimientoRepository
from app.application.use_cases.registrar_entrada_producto import RegistrarEntradaProducto
from app.application.use_cases.registrar_salida_producto import RegistrarSalidaProducto
from app.application.dto.movimiento_dto import (
    EntradaProductoRequest,
    SalidaProductoRequest,
    MovimientoResponse
)
from app.application.dto.pagination_dto import PaginatedResponse


router = APIRouter(prefix="/api/v1/inventario", tags=["Inventario"])


# ============================================================================
# ENDPOINTS de Movimientos
# ============================================================================

@router.post("/entrada", summary="Registrar entrada de producto (RF4)")
def registrar_entrada(
    data: EntradaProductoRequest,
    db: Session = Depends(get_session)
):
    """
    Registra una entrada de producto al inventario.

    **Qué hace:**
    1. Incrementa el stock del producto
    2. Crea un registro de movimiento para trazabilidad
    3. Guarda información del lote y proveedor

    **Reglas de Negocio:**
    - RN6: Todo cambio de stock se registra como movimiento
    - RF4: Registro de entrada con trazabilidad completa

    **Respuestas:**
    - 200: Entrada registrada exitosamente
    - 400: Producto no existe o datos inválidos
    - 500: Error del servidor
    """
    try:
        # Crear caso de uso con repositorios necesarios
        usecase = RegistrarEntradaProducto(
            ProductoRepository(db),
            MovimientoRepository(db),
            db
        )

        # Ejecutar entrada de producto
        usecase.execute(
            producto_id=data.producto_id,
            cantidad=data.cantidad,
            proveedor=data.proveedor,
            lote=data.lote,
            bodega=data.bodega
        )

        return {
            "mensaje": "Entrada registrada exitosamente",
            "producto_id": data.producto_id
        }

    except ValueError as e:
        # Error de validación (ej: producto no existe)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Error interno del servidor
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.post("/salida", summary="Registrar salida de producto (RF5)")
def registrar_salida(
    data: SalidaProductoRequest,
    db: Session = Depends(get_session)
):
    """
    Registra una salida de producto del inventario.

    **Qué hace:**
    1. Verifica que haya suficiente stock disponible
    2. Decrementa el stock del producto
    3. Crea un registro de movimiento con el motivo

    **Reglas de Negocio:**
    - RN2: Stock no puede quedar negativo (valida disponibilidad)
    - RN6: Todo cambio de stock se registra como movimiento
    - RF5: Registro de salida con motivo

    **Respuestas:**
    - 200: Salida registrada exitosamente
    - 400: Stock insuficiente, producto no existe o datos inválidos
    - 500: Error del servidor
    """
    try:
        # Crear caso de uso con repositorios necesarios
        usecase = RegistrarSalidaProducto(
            ProductoRepository(db),
            MovimientoRepository(db),
            db
        )

        # Ejecutar salida de producto
        usecase.execute(
            producto_id=data.producto_id,
            cantidad=data.cantidad,
            motivo=data.motivo,
            bodega=data.bodega
        )

        return {
            "mensaje": "Salida registrada exitosamente",
            "producto_id": data.producto_id
        }

    except ValueError as e:
        # Error de validación (ej: stock insuficiente)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Error interno del servidor
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.get("/movimientos", response_model=PaginatedResponse[MovimientoResponse], summary="Listar movimientos con paginación (RF8, RNF1)")
def listar_movimientos(
    producto_id: Optional[int] = Query(None, description="Filtrar por producto"),
    tipo: Optional[str] = Query(None, description="Filtrar por tipo (entrada/salida)"),
    bodega: Optional[str] = Query(None, description="Filtrar por bodega"),
    page: int = Query(1, ge=1, description="Número de página (1-indexed)"),
    page_size: int = Query(50, ge=1, le=100, description="Elementos por página (max: 100)"),
    db: Session = Depends(get_session)
):
    """
    Lista el historial de movimientos de inventario con PAGINACIÓN (RF8, RNF1).

    **Filtros disponibles:**
    - producto_id: Ver movimientos de un producto específico
    - tipo: Filtrar por "entrada" o "salida"
    - bodega: Filtrar por bodega

    **Paginación (RNF1):**
    - page: Página a consultar (empieza en 1)
    - page_size: Cantidad de elementos por página (máximo 100)

    **Respuesta paginada:**
    ```json
    {
        "items": [...movimientos...],
        "total": 10000,
        "page": 1,
        "page_size": 50,
        "total_pages": 200,
        "has_next": true,
        "has_prev": false
    }
    ```

    **Ordenamiento:**
    - Los movimientos se devuelven ordenados por fecha descendente (más recientes primero)

    **Para qué sirve:**
    - Ver el historial completo de entradas/salidas paginado
    - Auditar movimientos de inventario sin sobrecargar el servidor
    - Trazabilidad completa (RN6)

    **Respuestas:**
    - 200: Lista paginada de movimientos
    - 500: Error del servidor
    """
    try:
        repo = MovimientoRepository(db)

        # Obtener movimientos con filtros y paginación
        movimientos, total = repo.listar_movimientos(
            producto_id=producto_id,
            tipo=tipo,
            bodega=bodega,
            page=page,
            page_size=page_size
        )

        # Crear respuesta paginada
        return PaginatedResponse.create(
            items=movimientos,
            total=total,
            page=page,
            page_size=page_size
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.get("/movimientos/{producto_id}", response_model=List[MovimientoResponse], summary="Historial de un producto")
def obtener_movimientos_producto(
    producto_id: int,
    limit: int = Query(50, ge=1, le=200, description="Límite de resultados"),
    db: Session = Depends(get_session)
):
    """
    Obtiene el historial completo de movimientos de un producto específico.

    **Para qué sirve:**
    - Ver todas las entradas y salidas de un producto
    - Conocer el historial de lotes
    - Saber cuándo ingresó y salió stock

    **Respuestas:**
    - 200: Lista de movimientos del producto
    - 404: Producto no existe
    - 500: Error del servidor
    """
    try:
        # Verificar que el producto existe
        producto_repo = ProductoRepository(db)
        producto = producto_repo.obtener_por_id(producto_id)

        if not producto:
            raise HTTPException(
                status_code=404,
                detail=f"Producto con ID {producto_id} no encontrado"
            )

        # Obtener movimientos
        movimiento_repo = MovimientoRepository(db)
        movimientos = movimiento_repo.obtener_movimientos_por_producto(
            producto_id=producto_id,
            limit=limit
        )

        return movimientos

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
