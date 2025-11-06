from app.domain.ports.producto_repo_port import ProductoRepoPort
from app.domain.entities.producto import Producto


class RegistrarProductoUseCase:
    """
    Caso de Uso: Registrar Producto (RF1).
    (docstring resumido)
    """

    def __init__(self, repo: ProductoRepoPort):
        self.repo = repo

    def ejecutar(
        self,
        sku: str,
        nombre: str,
        tipo_licor: str,
        presentacion: str,
        proveedor: str,
        precio_compra: float,
        precio_venta: float,
        stock: int
    ) -> Producto:
        """
        Ejecuta el caso de uso de registrar un producto.

        Reglas aplicadas (ejemplo):
         - RN1: SKU único -> si ya existe, ValueError
         - RN2: precio_venta >= precio_compra -> si no, ValueError
         - RNx: stock >= 0
        """

        # Validaciones básicas de entrada
        if not sku or not sku.strip():
            raise ValueError("SKU inválido.")
        if not nombre or not nombre.strip():
            raise ValueError("Nombre inválido.")
        if precio_compra is None or precio_compra < 0:
            raise ValueError("Precio de compra inválido.")
        if precio_venta is None or precio_venta < 0:
            raise ValueError("Precio de venta inválido.")
        if precio_venta < precio_compra:
            raise ValueError("El precio de venta no puede ser menor que el precio de compra.")
        if stock is None or stock < 0:
            raise ValueError("Stock inválido; debe ser >= 0.")

        # RN1: verificar SKU único usando el puerto
        existente = self.repo.buscar_por_sku(sku)
        if existente is not None:
            raise ValueError(f"SKU '{sku}' ya existe.")

        # Crear la entidad Producto (ajusta la firma si tu entidad difiere)
        producto = Producto(
            sku=sku,
            nombre=nombre,
            tipo_licor=tipo_licor,
            presentacion=presentacion,
            proveedor=proveedor,
            precio_compra=precio_compra,
            precio_venta=precio_venta,
            stock=stock,
        )

        # Persistir usando el repositorio (puerto)
        producto_guardado = self.repo.guardar(producto)

        return producto_guardado
