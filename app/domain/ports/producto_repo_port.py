from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.producto import Producto


class ProductoRepoPort(ABC):
    """
    Puerto de repositorio para la entidad Producto.
    Define las operaciones que cualquier adaptador de persistencia
    (por ejemplo, PostgreSQL, MongoDB, etc.) debe implementar.
    """

    # Crear producto
    @abstractmethod
    def guardar(self, producto: Producto) -> Producto:
        """Guarda un nuevo producto en el repositorio."""
        pass

    # Actualizar producto existente
    @abstractmethod
    def actualizar(self, producto: Producto) -> Producto:
        """Actualiza un producto existente."""
        pass

    # Obtener producto por ID
    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[Producto]:
        """Devuelve un producto según su ID, o None si no existe."""
        pass

    # Obtener producto por SKU
    @abstractmethod
    def obtener_por_sku(self, sku: str) -> Optional[Producto]:
        """Devuelve un producto según su SKU, o None si no existe."""
        pass

    # Listar todos los productos
    @abstractmethod
    def listar_todos(self) -> List[Producto]:
        """Lista todos los productos registrados."""
        pass

    # Listar solo productos activos
    @abstractmethod
    def listar_activos(self) -> List[Producto]:
        """Lista únicamente los productos con estado 'Activo'."""
        pass

    # eliminar producto
    @abstractmethod
    def eliminar(self, id: int) -> bool:
        """Elimina un producto por ID. Devuelve True si fue eliminado."""
        pass

    # verificar existencia (útil para validaciones)
    @abstractmethod
    def existe(self, sku: str) -> bool:
        """Verifica si existe un producto con el SKU dado."""
        pass
