# -*- coding: utf-8 -*-
"""
DTOs para Dashboard

Data Transfer Objects para estadísticas y resúmenes del sistema.
"""

from pydantic import BaseModel


class EstadisticasResponse(BaseModel):
    """
    DTO con estadísticas generales del sistema.
    Usado para mostrar el resumen en el dashboard principal.

    Incluye:
    - Total de productos (activos e inactivos)
    - Stock total del inventario
    - Productos con stock bajo (alertas)
    - Movimientos registrados hoy
    - Valor total del inventario
    """
    total_productos: int
    productos_activos: int
    productos_inactivos: int
    stock_total: int
    productos_stock_bajo: int
    movimientos_hoy: int
    valor_inventario: float

    class Config:
        json_schema_extra = {
            "example": {
                "total_productos": 50,
                "productos_activos": 45,
                "productos_inactivos": 5,
                "stock_total": 2500,
                "productos_stock_bajo": 8,
                "movimientos_hoy": 15,
                "valor_inventario": 125000000.0
            }
        }


class ProductoStockBajoResponse(BaseModel):
    """
    DTO para productos con stock bajo (alertas de reabastecimiento).
    Usado en el endpoint de alertas RF6 y RF7.
    """
    id: int
    sku: str
    nombre: str
    stock: int
    tipo_licor: str
    proveedor: str

    class Config:
        json_schema_extra = {
            "example": {
                "id": 5,
                "sku": "RON-VIEJO-750",
                "nombre": "Ron Viejo de Caldas",
                "stock": 3,
                "tipo_licor": "Ron",
                "proveedor": "Licores de Caldas"
            }
        }


class AlertasStockBajoResponse(BaseModel):
    """
    DTO de respuesta completa para el endpoint de alertas de stock bajo.
    Incluye el total de alertas y la lista de productos.
    """
    total_alertas: int
    productos: list[ProductoStockBajoResponse]

    class Config:
        json_schema_extra = {
            "example": {
                "total_alertas": 3,
                "productos": [
                    {
                        "id": 5,
                        "sku": "RON-VIEJO-750",
                        "nombre": "Ron Viejo de Caldas",
                        "stock": 3,
                        "tipo_licor": "Ron",
                        "proveedor": "Licores de Caldas"
                    }
                ]
            }
        }
