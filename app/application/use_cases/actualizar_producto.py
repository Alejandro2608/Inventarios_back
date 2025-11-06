from app.domain.entities.producto import Producto
from app.domain.ports.producto_repo_port import ProductoRepoPort


class ActualizarProductoUseCase:

    def __init__(self, repo: ProductoRepoPort):
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

        # Buscar producto existente
        producto = self.repo.buscar_por_id(id)
        if not producto:
            raise ValueError(f"Producto con ID {id} no encontrado")

        # Actualizar campos dinámicamente
        campos_actualizables = {
            "nombre": nombre,
            "tipo_licor": tipo_licor,
            "presentacion": presentacion,
            "proveedor": proveedor,
            "precio_compra": precio_compra,
            "precio_venta": precio_venta
        }

        for campo, valor in campos_actualizables.items():
            if valor is not None:
                setattr(producto, campo, valor)

        # Actualizar stock
        if stock is not None:
            if stock < 0:
                raise ValueError("El stock no puede ser negativo")
            producto.actualizar_stock(stock)

        # Manejo del estado
        if estado is not None:
            estado = estado.strip().capitalize()
            if estado == "Activo":
                producto.activar()
            elif estado == "Inactivo":
                producto.desactivar()
            else:
                raise ValueError("El estado debe ser 'Activo' o 'Inactivo'")

        # Validar consistencia de precios
        producto.validar_precios()

        # Persistir cambios
        producto_actualizado = self.repo.actualizar(producto)

        return producto_actualizado
