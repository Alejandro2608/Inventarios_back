from abc import ABC, abstractmethod
from typing import List
from app.domain.entities.producto import Producto


class ProductoRepoPort(ABC):
    """
    Puerto (Interface) que define las operaciones de persistencia.

    Este es un PUERTO SECUNDARIO (salida) de la arquitectura hexagonal.

    ¿QUÉ ES UN PUERTO?
    - Es una interfaz (contrato) que define operaciones
    - Define QUÉ se necesita hacer, NO CÓMO hacerlo
    - Pertenece a la capa de DOMINIO

    ¿POR QUÉ USAMOS PUERTOS?
    1. INVERSIÓN DE DEPENDENCIAS (SOLID - Principio D):
       - El dominio define lo que necesita
       - La infraestructura lo implementa
       - El dominio NO depende de la infraestructura

    2. FLEXIBILIDAD:
       - Podemos tener múltiples implementaciones:
         * ProductoRepoSQL (SQLite/PostgreSQL)
         * ProductoRepoMongo (MongoDB)
         * ProductoRepoMemory (para pruebas)
       - Cambiar de BD no afecta al dominio

    3. TESTABILIDAD:
       - Podemos crear mocks fácilmente
       - No necesitamos BD real para probar el dominio

    RELACIÓN CON EL PATRÓN ADAPTER:
    - Este puerto es la interfaz que los adaptadores deben implementar
    - Los adaptadores "adaptan" tecnologías externas a este contrato
    """

    @abstractmethod
    def guardar(self, producto: Producto) -> Producto:
        """
        Guarda un producto nuevo en el repositorio.

        RESPONSABILIDAD:
        - Persistir un producto nuevo
        - Asignar un ID único
        - Validar que el SKU no exista (RN1)

        Args:
            producto: Entidad Producto a guardar

        Returns:
            Producto guardado con su ID asignado

        Raises:
            ValueError: Si el SKU ya existe (RN1)

        Ejemplo:
            producto = Producto(sku="RON001", ...)
            producto_guardado = repo.guardar(producto)
            print(producto_guardado.id)  # 1
        """
        pass

    @abstractmethod
    def actualizar(self, producto: Producto) -> Producto:
        """
        Actualiza un producto existente.

        RESPONSABILIDAD:
        - Modificar los datos de un producto existente
        - Actualizar la fecha de modificación

        Args:
            producto: Entidad Producto con los datos actualizados

        Returns:
            Producto actualizado

        Raises:
            ValueError: Si el producto no existe

        Ejemplo:
            producto.precio_venta = 70000
            repo.actualizar(producto)
        """
        pass

    @abstractmethod
    def buscar_por_id(self, id: int) -> Producto | None:
        """
        Busca un producto por su ID.

        Args:
            id: ID del producto

        Returns:
            Producto encontrado o None si no existe

        Ejemplo:
            producto = repo.buscar_por_id(1)
            if producto:
                print(producto.nombre)
        """
        pass

    @abstractmethod
    def buscar_por_sku(self, sku: str) -> Producto | None:
        """
        Busca un producto por su SKU.

        IMPORTANCIA:
        - Usado para validar RN1 (SKU único)
        - Evita duplicados en el inventario

        Args:
            sku: Código SKU del producto

        Returns:
            Producto encontrado o None si no existe

        Ejemplo:
            producto = repo.buscar_por_sku("RON001")
            if producto:
                print("SKU ya existe")
        """
        pass

    @abstractmethod
    def listar_todos(self) -> List[Producto]:
        """
        Lista todos los productos del inventario (RF3).

        RESPONSABILIDAD:
        - Retornar todos los productos (activos e inactivos)
        - Útil para consultas generales de inventario

        Returns:
            Lista de todos los productos

        Ejemplo:
            productos = repo.listar_todos()
            for p in productos:
                print(f"{p.sku}: {p.stock} unidades")
        """
        pass

    @abstractmethod
    def listar_activos(self) -> List[Producto]:
        """
        Lista solo los productos activos.

        RESPONSABILIDAD:
        - Retornar solo productos con estado "Activo"
        - Usado para mostrar productos disponibles para la venta

        REGLA DE NEGOCIO:
        - RN5: Solo productos activos pueden venderse

        Returns:
            Lista de productos con estado "Activo"

        Ejemplo:
            productos_activos = repo.listar_activos()
            # Solo productos que pueden venderse
        """
        pass
