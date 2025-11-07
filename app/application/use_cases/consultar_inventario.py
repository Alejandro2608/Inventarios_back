from typing import List, Optional
from app.domain.entities.producto import Producto
from app.domain.ports.producto_repo_port import ProductoRepoPort


class ConsultarInventarioUseCase:
    """
    Caso de Uso: Consultar Inventario General (RF3)
    - Permite listar productos o consultar por SKU específico.
    """

    def __init__(self, repo: ProductoRepoPort):
        self.repo = repo

    def ejecutar(self, solo_activos: bool = False, page: int = 1, page_size: int = 50) -> tuple[List[Producto], int]:
        """
        Retorna la lista de productos del inventario con paginación (RNF1).

        Args:
            solo_activos: Si es True, solo devuelve productos activos
            page: Página actual (1-indexed)
            page_size: Elementos por página

        Returns:
            Tupla (productos, total) donde:
            - productos: Lista de productos de la página actual
            - total: Total de productos
        """
        if solo_activos:
            return self.repo.listar_todos(page=page, page_size=page_size, estado="Activo")
        else:
            return self.repo.listar_todos(page=page, page_size=page_size)

    def obtener_por_sku(self, sku: str) -> Optional[Producto]:
        """
        Consulta un producto específico usando su SKU.

        Args:
            sku (str): Código SKU único del producto.

        Returns:
            Producto encontrado o None si no existe.
        """
        if not sku or not sku.strip():
            raise ValueError("El SKU no puede estar vacío")

        producto = self.repo.obtener_por_sku(sku)

        if not producto:
            # Puedes registrar log o lanzar excepción según tu dominio
            raise ValueError(f"No se encontró ningún producto con SKU '{sku}'")

        return producto
