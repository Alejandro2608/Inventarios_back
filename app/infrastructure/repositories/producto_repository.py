from sqlmodel import Session, select
from typing import Optional
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

    def actualizar(self, producto: Producto, auto_commit: bool = True) -> Producto:
        """
        Actualiza un producto existente.

        Args:
            producto: Entidad del producto con los nuevos valores
            auto_commit: Si es True, hace commit automático.
                        Si es False, solo prepara el cambio (flush).
                        Usar False cuando se usa dentro de UnitOfWork (RNF6)
        """
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

        if auto_commit:
            self.db.commit()
            self.db.refresh(model)
        else:
            self.db.flush()  # Solo prepara, no guarda aún (para transacciones)

        return model.to_entity()

    def obtener_por_id(self, id: int) -> Producto | None:
        model = self.db.get(ProductoModel, id)
        return model.to_entity() if model else None

    def obtener_por_sku(self, sku: str) -> Producto | None:
        statement = select(ProductoModel).where(ProductoModel.sku == sku)
        model = self.db.exec(statement).first()
        return model.to_entity() if model else None

    def listar_todos(self, page: int = 1, page_size: int = 50, estado: Optional[str] = None) -> tuple[list[Producto], int]:
        """
        Retorna todos los productos con paginación (RNF1).

        Args:
            page: Página actual (1-indexed)
            page_size: Elementos por página
            estado: Filtrar por estado ("Activo", "Inactivo") o None para todos

        Returns:
            Tupla (productos, total) donde:
            - productos: Lista de productos de la página actual
            - total: Total de productos que cumplen los filtros
        """
        from sqlmodel import func

        # Query base
        statement = select(ProductoModel)
        count_statement = select(func.count()).select_from(ProductoModel)

        # Aplicar filtro de estado si se especifica
        if estado:
            statement = statement.where(ProductoModel.estado == estado)
            count_statement = count_statement.where(ProductoModel.estado == estado)

        # Contar total
        total = self.db.exec(count_statement).one()

        # Aplicar paginación
        offset = (page - 1) * page_size
        statement = statement.offset(offset).limit(page_size)

        models = self.db.exec(statement).all()
        productos = [m.to_entity() for m in models]

        return (productos, total)

    def listar_activos(self) -> list[Producto]:
        """Retorna solo los productos activos."""
        statement = select(ProductoModel).where(ProductoModel.estado == "Activo")
        models = self.db.exec(statement).all()
        return [m.to_entity() for m in models]

    def eliminar(self, id: int) -> bool:
        """Elimina un producto por ID. Devuelve True si fue eliminado."""
        model = self.db.get(ProductoModel, id)
        if not model:
            return False
        self.db.delete(model)
        self.db.commit()
        return True

    def existe(self, sku: str) -> bool:
        """Verifica si existe un producto con el SKU dado."""
        statement = select(ProductoModel).where(ProductoModel.sku == sku)
        model = self.db.exec(statement).first()
        return model is not None
