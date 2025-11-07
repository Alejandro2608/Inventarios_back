# -*- coding: utf-8 -*-
"""
Endpoints de Productos - API REST

Este archivo es un ADAPTADOR PRIMARIO en arquitectura hexagonal:
- Recibe peticiones HTTP y las traduce a operaciones de dominio
- No contiene lógica de negocio, solo coordina
- Usa casos de uso (application layer) para ejecutar operaciones
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from typing import List
from app.infrastructure.db.database import get_session
from app.infrastructure.repositories.producto_repository import ProductoRepository
from app.application.use_cases.registrar_producto import RegistrarProductoUseCase
from app.application.use_cases.actualizar_producto import ActualizarProductoUseCase
from app.application.use_cases.consultar_inventario import ConsultarInventarioUseCase
from app.application.dto.producto_dto import (
    RegistrarProductoRequest,
    ActualizarProductoRequest,
    ProductoResponse
)
from app.application.dto.pagination_dto import PaginatedResponse


router = APIRouter(prefix="/api/v1/productos", tags=["Productos"])


# ============================================================================
# ENDPOINTS (Adaptadores Primarios)
# Traducen HTTP → Dominio → HTTP
# ============================================================================

@router.post("/", response_model=ProductoResponse, status_code=201, summary="Registrar nuevo producto (RF1)")
def registrar_producto(
    data: RegistrarProductoRequest,
    db: Session = Depends(get_session)
):
    """
    Crea un nuevo producto en el inventario.

    **Reglas de Negocio:**
    - RN1: El SKU debe ser único (no puede repetirse)
    - RN2: El stock no puede ser negativo
    - El precio de venta debe ser mayor o igual al precio de compra

    **Respuestas:**
    - 201: Producto creado exitosamente
    - 400: Datos inválidos o SKU duplicado
    - 500: Error del servidor
    """
    try:
        # 1. Crear repositorio y caso de uso (inyección de dependencias)
        repo = ProductoRepository(db)
        usecase = RegistrarProductoUseCase(repo)

        # 2. Ejecutar caso de uso (aquí está la lógica de negocio)
        producto = usecase.ejecutar(
            sku=data.sku,
            nombre=data.nombre,
            tipo_licor=data.tipo_licor,
            presentacion=data.presentacion,
            proveedor=data.proveedor,
            precio_compra=data.precio_compra,
            precio_venta=data.precio_venta,
            stock=data.stock
        )

        # 3. Devolver producto creado
        return producto

    except ValueError as e:
        # Error de validación de negocio (ej: SKU duplicado)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Error interno del servidor
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.get("/", response_model=PaginatedResponse[ProductoResponse], summary="Listar productos con paginación (RF3, RNF1)")
def listar_productos(
    solo_activos: bool = False,
    page: int = Query(1, ge=1, description="Número de página (1-indexed)"),
    page_size: int = Query(50, ge=1, le=100, description="Elementos por página (max: 100)"),
    db: Session = Depends(get_session)
):
    """
    Lista todos los productos del inventario con PAGINACIÓN (RF3, RNF1).

    **Parámetros:**
    - solo_activos: Si es true, solo muestra productos con estado "Activo"

    **Paginación (RNF1):**
    - page: Página a consultar (empieza en 1)
    - page_size: Cantidad de elementos por página (máximo 100)

    **Respuesta paginada:**
    ```json
    {
        "items": [...productos...],
        "total": 50,
        "page": 1,
        "page_size": 50,
        "total_pages": 1,
        "has_next": false,
        "has_prev": false
    }
    ```

    **Respuestas:**
    - 200: Lista paginada de productos
    - 500: Error del servidor
    """
    try:
        repo = ProductoRepository(db)
        usecase = ConsultarInventarioUseCase(repo)

        # Obtener lista de productos paginada
        productos, total = usecase.ejecutar(
            solo_activos=solo_activos,
            page=page,
            page_size=page_size
        )

        # Crear respuesta paginada
        return PaginatedResponse.create(
            items=productos,
            total=total,
            page=page,
            page_size=page_size
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.get("/{producto_id}", response_model=ProductoResponse, summary="Obtener producto por ID")
def obtener_producto(
    producto_id: int,
    db: Session = Depends(get_session)
):
    """
    Busca un producto específico por su ID.

    **Respuestas:**
    - 200: Producto encontrado
    - 404: Producto no existe
    - 500: Error del servidor
    """
    try:
        repo = ProductoRepository(db)
        producto = repo.obtener_por_id(producto_id)

        if not producto:
            raise HTTPException(status_code=404, detail=f"Producto con ID {producto_id} no encontrado")

        return producto

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.get("/sku/{sku}", response_model=ProductoResponse, summary="Buscar producto por SKU")
def buscar_por_sku(
    sku: str,
    db: Session = Depends(get_session)
):
    """
    Busca un producto por su código SKU único.

    **RN1:** Solo puede existir un producto con cada SKU

    **Respuestas:**
    - 200: Producto encontrado
    - 404: SKU no existe
    - 500: Error del servidor
    """
    try:
        repo = ProductoRepository(db)
        usecase = ConsultarInventarioUseCase(repo)

        producto = usecase.obtener_por_sku(sku)

        return producto

    except ValueError as e:
        # No se encontró el producto
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.put("/{producto_id}", response_model=ProductoResponse, summary="Actualizar producto (RF2)")
def actualizar_producto(
    producto_id: int,
    data: ActualizarProductoRequest,
    db: Session = Depends(get_session)
):
    """
    Actualiza la información de un producto existente.

    **Características:**
    - Actualización parcial: solo envía los campos que quieres cambiar
    - Valida reglas de negocio antes de guardar

    **Reglas de Negocio:**
    - RN2: Stock no puede ser negativo
    - RN5: Estados válidos (Activo/Inactivo)
    - Precio de venta >= precio de compra

    **Respuestas:**
    - 200: Producto actualizado
    - 400: Datos inválidos
    - 404: Producto no existe
    - 500: Error del servidor
    """
    try:
        repo = ProductoRepository(db)
        usecase = ActualizarProductoUseCase(repo)

        # Ejecutar actualización
        producto = usecase.ejecutar(
            id=producto_id,
            nombre=data.nombre,
            tipo_licor=data.tipo_licor,
            presentacion=data.presentacion,
            proveedor=data.proveedor,
            precio_compra=data.precio_compra,
            precio_venta=data.precio_venta,
            stock=data.stock,
            estado=data.estado
        )

        return producto

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.delete("/{producto_id}", status_code=204, summary="Eliminar producto")
def eliminar_producto(
    producto_id: int,
    db: Session = Depends(get_session)
):
    """
    Elimina un producto del inventario.

    **NOTA:** En producción se recomienda usar eliminación lógica
    (cambiar estado a "Inactivo") en lugar de borrar físicamente.

    **Respuestas:**
    - 204: Producto eliminado (sin contenido)
    - 404: Producto no existe
    - 500: Error del servidor
    """
    try:
        repo = ProductoRepository(db)

        eliminado = repo.eliminar(producto_id)

        if not eliminado:
            raise HTTPException(status_code=404, detail=f"Producto con ID {producto_id} no encontrado")

        return None  # 204 No Content

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
