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

    def ejecutar(self, solo_activos: bool = False) -> List[Producto]:
        """
        Retorna la lista de productos del inventario.
        Si `solo_activos` es True, solo devuelve productos activos.
        """
        if solo_activos:
            return self.repo.listar_activos()
        else:
            return self.repo.listar_todos()

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

        producto = self.repo.buscar_por_sku(sku)

        if not producto:
            # Puedes registrar log o lanzar excepción según tu dominio
            raise ValueError(f"No se encontró ningún producto con SKU '{sku}'")

        return producto
