from pydantic import BaseModel, Field, field_validator
from datetime import datetime


class ProductoCreateDTO(BaseModel):

    sku: str = Field(
        ...,
        min_length=1,
        max_length=50,

        description="C�digo SKU �nico del producto"

    )

    nombre: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Nombre del producto"
    )

    tipo_licor: str = Field(
        ...,
        description="Tipo de licor (Ron, Whisky, Vodka, etc.)"
    )

    presentacion: str = Field(
        ...,

        description="Presentaci�n del producto (Botella 750ml, Caja x6, etc.)"

    )

    proveedor: str = Field(
        ...,
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
        ...,
        ge=0,
        description="Stock inicial (debe ser mayor o igual a 0 - RN2)"
    )

    @field_validator('sku')
    @classmethod
    def sku_sin_espacios(cls, v: str) -> str:
     
        if ' ' in v:
            raise ValueError('El SKU no puede contener espacios')
        return v.upper()

    class Config:
        json_schema_extra = {
            "example": {
                "sku": "RON001",

                "nombre": "Ron Viejo de Caldas 8 A�os",

                "nombre": "Ron Viejo de Caldas 8 A�os",

                "tipo_licor": "Ron",
                "presentacion": "Botella 750ml",
                "proveedor": "Licores Nacionales S.A.",
                "precio_compra": 45000.00,
                "precio_venta": 65000.00,
                "stock": 100
            }
        }


class ProductoUpdateDTO(BaseModel):
    
    nombre: str | None = Field(None, min_length=1, max_length=200)
    tipo_licor: str | None = None
    presentacion: str | None = None
    proveedor: str | None = None
    precio_compra: float | None = Field(None, gt=0)
    precio_venta: float | None = Field(None, gt=0)
    stock: int | None = Field(None, ge=0)
    estado: str | None = Field(None, pattern="^(Activo|Inactivo)$")

    class Config:
        json_schema_extra = {
            "example": {
                "precio_venta": 70000.00,
                "stock": 150
            }
        }


class ProductoResponseDTO(BaseModel):
 
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
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    class Config:

        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "sku": "RON001",

                "nombre": "Ron Viejo de Caldas 8 A�os",

                "nombre": "Ron Viejo de Caldas 8 A�os",

                "tipo_licor": "Ron",
                "presentacion": "Botella 750ml",
                "proveedor": "Licores Nacionales S.A.",
                "precio_compra": 45000.00,
                "precio_venta": 65000.00,
                "stock": 100,
                "estado": "Activo",
                "fecha_creacion": "2025-10-30T10:00:00",
                "fecha_actualizacion": "2025-10-30T10:00:00"
            }
        }
