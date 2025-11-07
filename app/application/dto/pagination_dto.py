# -*- coding: utf-8 -*-
"""
DTOs para Paginación (RNF1)

Proporciona respuestas paginadas para endpoints que devuelven muchos resultados.
"""

from pydantic import BaseModel, Field
from typing import Generic, TypeVar, List
from math import ceil


T = TypeVar('T')  # Tipo genérico para los items


class PaginatedResponse(BaseModel, Generic[T]):
    """
    Respuesta paginada genérica (RNF1).

    Campos:
    - items: Lista de elementos de la página actual
    - total: Total de elementos en todas las páginas
    - page: Página actual (1-indexed)
    - page_size: Cantidad de elementos por página
    - total_pages: Total de páginas disponibles
    - has_next: Indica si hay una página siguiente
    - has_prev: Indica si hay una página anterior

    Ejemplo de uso:
        GET /api/v1/movimientos?page=2&page_size=50

        {
            "items": [...50 movimientos...],
            "total": 10000,
            "page": 2,
            "page_size": 50,
            "total_pages": 200,
            "has_next": true,
            "has_prev": true
        }
    """
    items: List[T]
    total: int = Field(..., description="Total de elementos")
    page: int = Field(..., ge=1, description="Página actual (1-indexed)")
    page_size: int = Field(..., ge=1, description="Elementos por página")
    total_pages: int = Field(..., ge=0, description="Total de páginas")
    has_next: bool = Field(..., description="¿Existe página siguiente?")
    has_prev: bool = Field(..., description="¿Existe página anterior?")

    class Config:
        json_schema_extra = {
            "example": {
                "items": ["...elementos..."],
                "total": 10000,
                "page": 2,
                "page_size": 50,
                "total_pages": 200,
                "has_next": True,
                "has_prev": True
            }
        }

    @staticmethod
    def create(items: List[T], total: int, page: int, page_size: int) -> 'PaginatedResponse[T]':
        """
        Crea una respuesta paginada calculando los metadatos automáticamente.

        Args:
            items: Lista de elementos de la página actual
            total: Total de elementos en todas las páginas
            page: Página actual (1-indexed)
            page_size: Elementos por página

        Returns:
            PaginatedResponse con todos los metadatos calculados
        """
        total_pages = ceil(total / page_size) if page_size > 0 else 0

        return PaginatedResponse(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
            has_next=page < total_pages,
            has_prev=page > 1
        )
