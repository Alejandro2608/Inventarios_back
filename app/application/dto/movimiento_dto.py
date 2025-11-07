# -*- coding: utf-8 -*-
"""
DTOs para Movimientos de Inventario

Data Transfer Objects para registrar entradas, salidas y consultar movimientos.
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class EntradaProductoRequest(BaseModel):
    """
    DTO para registrar entrada de producto (RF4).
    Una entrada incrementa el stock del producto.
    """
    producto_id: int = Field(..., description="ID del producto a ingresar")
    cantidad: int = Field(..., gt=0, description="Cantidad a ingresar (mayor a 0)")
    proveedor: str | None = Field(None, description="Nombre del proveedor")
    lote: str | None = Field(None, description="Número de lote (opcional)")
    bodega: str | None = Field(None, description="Bodega donde se ingresa")

    class Config:
        json_schema_extra = {
            "example": {
                "producto_id": 1,
                "cantidad": 50,
                "proveedor": "Licores Nacionales S.A.",
                "lote": "LT-2024-001",
                "bodega": "Bodega Principal"
            }
        }


class SalidaProductoRequest(BaseModel):
    """
    DTO para registrar salida de producto (RF5).
    Una salida decrementa el stock del producto.
    """
    producto_id: int = Field(..., description="ID del producto a retirar")
    cantidad: int = Field(..., gt=0, description="Cantidad a retirar (mayor a 0)")
    motivo: str | None = Field(None, description="Motivo de la salida (venta, pérdida, etc.)")
    bodega: str | None = Field(None, description="Bodega de donde sale")

    class Config:
        json_schema_extra = {
            "example": {
                "producto_id": 1,
                "cantidad": 10,
                "motivo": "Venta al cliente",
                "bodega": "Bodega Principal"
            }
        }


class MovimientoResponse(BaseModel):
    """
    DTO de respuesta para movimientos de inventario.
    Representa un movimiento (entrada o salida) registrado en el sistema.
    """
    id: int
    producto_id: int
    cantidad: int
    tipo: str
    fecha: datetime
    proveedor: Optional[str] = None
    lote: Optional[str] = None
    bodega: Optional[str] = None
    motivo: Optional[str] = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "producto_id": 1,
                "cantidad": 50,
                "tipo": "entrada",
                "fecha": "2025-11-06T10:30:00",
                "proveedor": "Licores Nacionales S.A.",
                "lote": "LT-2024-001",
                "bodega": "Bodega Principal",
                "motivo": None
            }
        }
