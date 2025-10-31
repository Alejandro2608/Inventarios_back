from datetime import datetime


class Producto:
    """
    Entidad del dominio que representa un producto del inventario.

    RESPONSABILIDADES:
    - Mantener la identidad del producto (SKU único)
    - Validar reglas de negocio relacionadas con el producto
    - Encapsular los datos del producto

    REGLAS DE NEGOCIO APLICADAS:
    - RN1: SKU debe ser único (validado en el caso de uso)
    - RN2: Stock no puede ser negativo
    - RN5: Productos inactivos no se pueden mover ni vender

    PRINCIPIOS SOLID:
    - SRP: Esta clase solo se encarga de la lógica de negocio del Producto
    - OCP: Podemos extenderla sin modificarla
    """

    def __init__(
        self,
        sku: str,
        nombre: str,
        tipo_licor: str,
        presentacion: str,
        proveedor: str,
        precio_compra: float,
        precio_venta: float,
        stock: int,
        estado: str = "Activo",
        id: int | None = None,
        fecha_creacion: datetime | None = None,
        fecha_actualizacion: datetime | None = None
    ):
        """
        Constructor de la entidad Producto.

        Args:
            sku: Código SKU único del producto
            nombre: Nombre del producto
            tipo_licor: Tipo de licor (Ron, Whisky, Vodka, etc.)
            presentacion: Presentación del producto (Botella 750ml, etc.)
            proveedor: Nombre del proveedor
            precio_compra: Precio al que se compra el producto
            precio_venta: Precio al que se vende el producto
            stock: Cantidad disponible en inventario
            estado: Estado del producto (Activo/Inactivo)
            id: ID del producto (asignado por la BD)
            fecha_creacion: Fecha de creación del registro
            fecha_actualizacion: Fecha de última actualización
        """
        self.id = id
        self.sku = sku
        self.nombre = nombre
        self.tipo_licor = tipo_licor
        self.presentacion = presentacion
        self.proveedor = proveedor
        self.precio_compra = precio_compra
        self.precio_venta = precio_venta
        self.stock = stock
        self.estado = estado
        self.fecha_creacion = fecha_creacion or datetime.now()
        self.fecha_actualizacion = fecha_actualizacion or datetime.now()

    def validar_stock_no_negativo(self) -> None:
        """
        Valida la regla de negocio RN2: Stock no negativo.

        Esta validación asegura que nunca tengamos stock negativo,
        lo cual no tiene sentido en el mundo real.

        Raises:
            ValueError: Si el stock es menor que 0

        Ejemplo:
            producto.stock = -5
            producto.validar_stock_no_negativo()  # Lanza ValueError
        """
        if self.stock < 0:
            raise ValueError("El stock no puede ser negativo (RN2)")

    def validar_precios(self) -> None:
        """
        Valida que los precios sean mayores a 0.

        Los precios deben ser positivos para tener sentido comercial.

        Raises:
            ValueError: Si algún precio es inválido

        Ejemplo:
            producto.precio_compra = 0
            producto.validar_precios()  # Lanza ValueError
        """
        if self.precio_compra <= 0:
            raise ValueError("El precio de compra debe ser mayor a 0")

        if self.precio_venta <= 0:
            raise ValueError("El precio de venta debe ser mayor a 0")

    def desactivar(self) -> None:
        """
        Cambia el estado del producto a Inactivo (RN5).

        Un producto inactivo no puede ser vendido ni movido.
        Se usa en lugar de eliminar el producto para mantener
        el historial y la trazabilidad.

        Ejemplo:
            producto.desactivar()
            print(producto.estado)  # "Inactivo"
        """
        self.estado = "Inactivo"
        self.fecha_actualizacion = datetime.now()

    def activar(self) -> None:
        """
        Cambia el estado del producto a Activo.

        Reactiva un producto previamente desactivado.

        Ejemplo:
            producto.activar()
            print(producto.estado)  # "Activo"
        """
        self.estado = "Activo"
        self.fecha_actualizacion = datetime.now()

    def actualizar_stock(self, nueva_cantidad: int) -> None:
        """
        Actualiza el stock validando que no sea negativo.

        Este método encapsula la lógica de actualización de stock
        garantizando que se cumpla la regla RN2.

        Args:
            nueva_cantidad: Nueva cantidad de stock

        Raises:
            ValueError: Si la cantidad es negativa

        Ejemplo:
            producto.actualizar_stock(50)
            print(producto.stock)  # 50
        """
        self.stock = nueva_cantidad
        self.validar_stock_no_negativo()
        self.fecha_actualizacion = datetime.now()

    def esta_activo(self) -> bool:
        """
        Verifica si el producto está activo.

        Returns:
            True si el producto está activo, False en caso contrario

        Ejemplo:
            if producto.esta_activo():
                print("Puede venderse")
        """
        return self.estado == "Activo"

    def __repr__(self) -> str:
        """
        Representación en string del producto (útil para debugging).

        Returns:
            String con la representación del producto

        Ejemplo:
            print(producto)  # Producto(SKU: RON001, Nombre: Ron Viejo...)
        """
        return f"Producto(SKU: {self.sku}, Nombre: {self.nombre}, Stock: {self.stock})"
