from sqlalchemy.orm import Session
from app.domain.entities.producto import Producto
from app.domain.ports.producto_repo_port import ProductoRepoPort
from app.infrastructure.db.models import ProductoModel


class ProductoRepository(ProductoRepoPort):
    """Adaptador que implementa el puerto ProductoRepoPort usando SQLAlchemy."""

    def __init__(self, db: Session):
        self.db = db

    def guardar(self, producto: Producto) -> Producto:
        existente = self.db.query(ProductoModel).filter_by(sku=producto.sku).first()
        if existente:
            raise ValueError("El SKU ya existe")

        model = ProductoModel(**producto.__dict__)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return model.to_entity()

    def actualizar(self, producto: Producto) -> Producto:
        model = self.db.query(ProductoModel).filter_by(id=producto.id).first()
        if not model:
            raise ValueError("Producto no encontrado")

        for key, value in producto.__dict__.items():
            setattr(model, key, value)

        self.db.commit()
        self.db.refresh(model)
        return model.to_entity()

    def obtener_por_id(self, id: int) -> Producto | None:
        model = self.db.query(ProductoModel).filter_by(id=id).first()
        return model.to_entity() if model else None

    def obtener_por_sku(self, sku: str) -> Producto | None:
        model = self.db.query(ProductoModel).filter_by(sku=sku).first()
        return model.to_entity() if model else None

    def listar_todos(self) -> list[Producto]:
        """Retorna todos los productos (activos e inactivos)."""
        models = self.db.query(ProductoModel).all()
        return [m.to_entity() for m in models]

    def listar_activos(self) -> list[Producto]:
        """Retorna solo los productos activos."""
        models = self.db.query(ProductoModel).filter_by(activo=True).all()
        return [m.to_entity() for m in models]
