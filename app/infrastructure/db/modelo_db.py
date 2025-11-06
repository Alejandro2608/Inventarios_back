from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.domain.entities.movimiento_inventario import TipoMovimiento
from .database import Base

class MovimientoInventarioModel(Base):
    __tablename__ = "movimientos_inventario"

    id = Column(Integer, primary_key=True, autoincrement=True)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    tipo = Column(Enum(TipoMovimiento), nullable=False)
    fecha = Column(DateTime, nullable=False)
    proveedor = Column(String)
    lote = Column(String)
    bodega = Column(String)
    motivo = Column(String)

    producto = relationship("ProductoModel")
