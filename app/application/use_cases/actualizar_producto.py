from app.domain.entities.producto import Producto
from app.domain.ports.producto_repo_port import ProductoRepoPort


class ActualizarProductoUseCase:
    """
    Caso de Uso: Actualizar Producto (RF2).

    RESPONSABILIDAD:
    - Permitir modificar los datos de un producto existente
    - Validar reglas de negocio antes de actualizar
    - Mantener la trazabilidad (fecha de actualización)

    CAMPOS ACTUALIZABLES:
    - Nombre
    - Tipo de licor
    - Presentación
    - Proveedor
    - Precio de compra
    - Precio de venta
    - Stock
    - Estado (Activo/Inactivo - RN5)

    REGLAS DE NEGOCIO APLICADAS:
    - RN2: Stock no puede ser negativo
    - RN5: Productos inactivos no se pueden mover

    PRINCIPIOS SOLID:
    - S (SRP): Solo actualiza productos
    - D (DIP): Depende de abstracción (ProductoRepoPort)
    """

    def __init__(self, repo: ProductoRepoPort):
        """
        Constructor del caso de uso.

        Args:
            repo: Repositorio de productos
        """
        self.repo = repo

    def ejecutar(
        self,
        id: int,
        nombre: str | None = None,
        tipo_licor: str | None = None,
        presentacion: str | None = None,
        proveedor: str | None = None,
        precio_compra: float | None = None,
        precio_venta: float | None = None,
        stock: int | None = None,
        estado: str | None = None
    ) -> Producto:
        """
        Ejecuta la actualización de un producto.

        FLUJO:
        1. Buscar producto existente por ID
        2. Actualizar solo los campos que vienen con valor
        3. Validar reglas de negocio (stock, precios)
        4. Guardar cambios
        5. Retornar producto actualizado

        Args:
            id: ID del producto a actualizar
            nombre: Nuevo nombre (opcional)
            tipo_licor: Nuevo tipo de licor (opcional)
            presentacion: Nueva presentación (opcional)
            proveedor: Nuevo proveedor (opcional)
            precio_compra: Nuevo precio de compra (opcional)
            precio_venta: Nuevo precio de venta (opcional)
            stock: Nuevo stock (opcional)
            estado: Nuevo estado (opcional)

        Returns:
            Producto actualizado

        Raises:
            ValueError: Si el producto no existe
            ValueError: Si el stock es negativo
            ValueError: Si los precios no son válidos

        Ejemplo:
            producto = caso_uso.ejecutar(
                id=1,
                precio_venta=70000,
                stock=150
            )
        """
        producto = self.repo.buscar_por_id(id)
        if not producto:
            raise ValueError(f"Producto con ID {id} no encontrado")

        if nombre is not None:
            producto.nombre = nombre
        if tipo_licor is not None:
            producto.tipo_licor = tipo_licor
        if presentacion is not None:
            producto.presentacion = presentacion
        if proveedor is not None:
            producto.proveedor = proveedor
        if precio_compra is not None:
            producto.precio_compra = precio_compra
        if precio_venta is not None:
            producto.precio_venta = precio_venta
        if stock is not None:
            producto.actualizar_stock(stock)
        if estado is not None:
            if estado == "Activo":
                producto.activar()
            elif estado == "Inactivo":
                producto.desactivar()

        producto.validar_precios()

        producto_actualizado = self.repo.actualizar(producto)

        return producto_actualizado
