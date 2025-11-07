# -*- coding: utf-8 -*-
"""
DTOs para Productos

Data Transfer Objects para crear, actualizar y consultar productos.
"""

from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional


class RegistrarProductoRequest(BaseModel):
    """
    DTO para crear un producto nuevo (RF1).
    Valida que los datos vengan correctos antes de procesarlos.
    """
    sku: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Código SKU único del producto (RN1)"
    )
    nombre: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Nombre del producto"
    )
    tipo_licor: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Tipo de licor (Ron, Whisky, Vodka, etc.)"
    )
    presentacion: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Presentación del producto (Botella 750ml, Caja x6, etc.)"
    )
    proveedor: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Nombre del proveedor"
    )
    precio_compra: float = Field(
        ...,
        gt=0,
        description="Precio de compra (debe ser mayor a 0)"
    )
    precio_venta: float = Field(
        ...,
        gt=0,
        description="Precio de venta (debe ser mayor a 0)"
    )
    stock: int = Field(
        0,
        ge=0,
        description="Stock inicial (debe ser mayor o igual a 0 - RN2)"
    )

    @field_validator('sku')
    @classmethod
    def sku_sin_espacios(cls, v: str) -> str:
        """Valida que el SKU no contenga espacios y lo convierte a mayúsculas."""
        if ' ' in v:
            raise ValueError('El SKU no puede contener espacios')
        return v.upper()

    class Config:
        json_schema_extra = {
            "example": {
                "sku": "RON-MEDELLIN-750",
                "nombre": "Ron Medellín Añejo",
                "tipo_licor": "Ron",
                "presentacion": "Botella 750ml",
                "proveedor": "Licores Nacionales S.A.",
                "precio_compra": 25000.00,
                "precio_venta": 35000.00,
                "stock": 100
            }
        }


class ActualizarProductoRequest(BaseModel):
    """
    DTO para actualizar un producto (RF2).
    Todos los campos son opcionales para permitir actualización parcial.
    """
    nombre: Optional[str] = Field(None, min_length=1, max_length=200)
    tipo_licor: Optional[str] = Field(None, min_length=1, max_length=100)
    presentacion: Optional[str] = Field(None, min_length=1, max_length=100)
    proveedor: Optional[str] = Field(None, min_length=1, max_length=200)
    precio_compra: Optional[float] = Field(None, gt=0)
    precio_venta: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    estado: Optional[str] = Field(None, pattern="^(Activo|Inactivo)$")

    class Config:
        json_schema_extra = {
            "example": {
                "precio_venta": 38000.00,
                "stock": 150,
                "estado": "Activo"
            }
        }


class ProductoResponse(BaseModel):
    """
    DTO de respuesta - convierte las entidades a JSON para devolverlas al cliente.
    """
    id: int
    sku: str
    nombre: str
    tipo_licor: str
    presentacion: str
    proveedor: str
    precio_compra: float
    precio_venta: float
    stock: int
    estado: str

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "sku": "RON-MEDELLIN-750",
                "nombre": "Ron Medellín Añejo",
                "tipo_licor": "Ron",
                "presentacion": "Botella 750ml",
                "proveedor": "Licores Nacionales S.A.",
                "precio_compra": 25000.00,
                "precio_venta": 35000.00,
                "stock": 100,
                "estado": "Activo"
            }
        }
