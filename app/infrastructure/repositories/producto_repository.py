from sqlmodel import Session, select
from app.domain.entities.producto import Producto
from app.domain.ports.producto_repo_port import ProductoRepoPort
from app.infrastructure.db.models import ProductoModel


class ProductoRepository(ProductoRepoPort):
    """Adaptador que implementa el puerto ProductoRepoPort usando SQLModel."""

    def __init__(self, db: Session):
        self.db = db

    def guardar(self, producto: Producto) -> Producto:
        statement = select(ProductoModel).where(ProductoModel.sku == producto.sku)
        existente = self.db.exec(statement).first()
        if existente:
            raise ValueError("El SKU ya existe (RN1)")

        model = ProductoModel(
            sku=producto.sku,
            nombre=producto.nombre,
            tipo_licor=producto.tipo_licor,
            presentacion=producto.presentacion,
            proveedor=producto.proveedor,
            precio_compra=producto.precio_compra,
            precio_venta=producto.precio_venta,
            stock=producto.stock,
            estado=producto.estado,
            fecha_creacion=producto.fecha_creacion,
            fecha_actualizacion=producto.fecha_actualizacion
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return model.to_entity()

    def actualizar(self, producto: Producto) -> Producto:
        model = self.db.get(ProductoModel, producto.id)
        if not model:
            raise ValueError("Producto no encontrado")

        model.nombre = producto.nombre
        model.tipo_licor = producto.tipo_licor
        model.presentacion = producto.presentacion
        model.proveedor = producto.proveedor
        model.precio_compra = producto.precio_compra
        model.precio_venta = producto.precio_venta
        model.stock = producto.stock
        model.estado = producto.estado
        model.fecha_actualizacion = producto.fecha_actualizacion

        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return model.to_entity()

    def obtener_por_id(self, id: int) -> Producto | None:
        model = self.db.get(ProductoModel, id)
        return model.to_entity() if model else None

    def obtener_por_sku(self, sku: str) -> Producto | None:
        statement = select(ProductoModel).where(ProductoModel.sku == sku)
        model = self.db.exec(statement).first()
        return model.to_entity() if model else None

    def listar_todos(self) -> list[Producto]:
        """Retorna todos los productos (activos e inactivos)."""
        statement = select(ProductoModel)
        models = self.db.exec(statement).all()
        return [m.to_entity() for m in models]

    def listar_activos(self) -> list[Producto]:
        """Retorna solo los productos activos."""
        statement = select(ProductoModel).where(ProductoModel.estado == "Activo")
        models = self.db.exec(statement).all()
        return [m.to_entity() for m in models]
