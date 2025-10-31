from typing import List
from app.domain.entities.producto import Producto
from app.domain.ports.producto_repo_port import ProductoRepoPort


class ConsultarInventarioUseCase:
    """
    Caso de Uso: Consultar Inventario General (RF3).

    RESPONSABILIDAD:
    - Proporcionar acceso a la lista completa de productos
    - Permitir consultar solo productos activos (opcional)
    - Facilitar la visualización del estado del inventario

    INFORMACIÓN RETORNADA:
    - Todos los productos del inventario
    - Cantidad actual de stock
    - Estado (Activo/Inactivo)
    - Fecha de última actualización
    - Todos los demás datos del producto

    USO PRINCIPAL:
    - Dashboard de inventario (RF20)
    - Reportes de inventario (RF11)
    - Consultas generales por parte de usuarios

    PRINCIPIOS SOLID:
    - S (SRP): Solo consulta inventario
    - D (DIP): Depende de abstracción (ProductoRepoPort)
    """

    def __init__(self, repo: ProductoRepoPort):
        """
        Constructor del caso de uso.

        Args:
            repo: Repositorio de productos
        """
        self.repo = repo

    def ejecutar(self, solo_activos: bool = False) -> List[Producto]:
        """
        Ejecuta la consulta del inventario.

        FLUJO:
        1. Llamar al repositorio
        2. Obtener lista de productos (todos o solo activos)
        3. Retornar lista

        Args:
            solo_activos: Si True, retorna solo productos activos

        Returns:
            Lista de productos del inventario

        Ejemplo:
            # Consultar todos los productos
            todos = caso_uso.ejecutar()

            # Consultar solo activos
            activos = caso_uso.ejecutar(solo_activos=True)
        """
        if solo_activos:
            return self.repo.listar_activos()
        else:
            return self.repo.listar_todos()

    def buscar_por_sku(self, sku: str) -> Producto | None:
        """
        Busca un producto específico por SKU.

        UTILIDAD:
        - Búsqueda rápida de productos
        - Validación de existencia

        Args:
            sku: Código SKU del producto

        Returns:
            Producto encontrado o None

        Ejemplo:
            producto = caso_uso.buscar_por_sku("RON001")
            if producto:
                print(f"Stock: {producto.stock}")
        """
        return self.repo.buscar_por_sku(sku)

    def buscar_por_id(self, id: int) -> Producto | None:
        """
        Busca un producto específico por ID.

        Args:
            id: ID del producto

        Returns:
            Producto encontrado o None

        Ejemplo:
            producto = caso_uso.buscar_por_id(1)
        """
        return self.repo.buscar_por_id(id)
