from pydantic import BaseModel, Field, field_validator
from datetime import datetime


class ProductoCreateDTO(BaseModel):
    """
    DTO (Data Transfer Object) para crear un producto (RF1).

    �QU� ES UN DTO?
    - Objeto simple para transferir datos entre capas
    - No tiene l�gica de negocio (eso est� en la Entidad)
    - Usa Pydantic para validaci�n autom�tica

    �POR QU� USAMOS DTOs?
    1. SEPARACI�N DE RESPONSABILIDADES:
       - La Entidad tiene l�gica de negocio
       - El DTO solo valida formato de datos de entrada

    2. VALIDACI�N AUTOM�TICA:
       - Pydantic valida tipos, rangos, formatos
       - Si algo est� mal, lanza excepci�n antes de llegar al dominio

    3. DOCUMENTACI�N AUTO-GENERADA:
       - FastAPI usa estos DTOs para generar Swagger/OpenAPI
       - El frontend sabe exactamente qu� enviar

    RELACI�N CON LA ARQUITECTURA:
    - Pertenece a la capa de APLICACI�N
    - Es el contrato entre la API y los casos de uso
    """

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
        """
        Valida que el SKU no contenga espacios y lo convierte a may�sculas.

        Args:
            v: Valor del SKU

        Returns:
            SKU en may�sculas y sin espacios

        Raises:
            ValueError: Si el SKU contiene espacios
        """
        if ' ' in v:
            raise ValueError('El SKU no puede contener espacios')
        return v.upper()

    class Config:
        """
        Configuraci�n de Pydantic.

        json_schema_extra: Ejemplo que aparece en Swagger
        """
        json_schema_extra = {
            "example": {
                "sku": "RON001",
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
    """
    DTO para actualizar un producto (RF2).

    CARACTER�STICAS:
    - Todos los campos son opcionales (Optional)
    - Permite actualizaciones parciales
    - Solo se actualizan los campos enviados

    Ejemplo:
        # Actualizar solo el precio
        {
            "precio_venta": 70000.00
        }
    """

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
    """
    DTO para respuestas de la API.

    PROP�SITO:
    - Define qu� datos se env�an al cliente
    - Incluye datos calculados/generados (ID, fechas)
    - Se usa en las respuestas de todos los endpoints

    VENTAJAS:
    - El cliente sabe exactamente qu� esperar
    - FastAPI genera documentaci�n autom�tica
    - Valida que la respuesta tenga el formato correcto
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
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    class Config:
        """
        from_attributes: Permite crear DTO desde objetos Python
        (como las entidades del dominio)
        """
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "sku": "RON001",
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
