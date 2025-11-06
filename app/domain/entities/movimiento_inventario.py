from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class TipoMovimiento(Enum):
    ENTRADA = "entrada"
    SALIDA = "salida"

@dataclass
class MovimientoInventario:
    producto_id: int
    cantidad: int
    tipo: TipoMovimiento
    fecha: datetime
    proveedor: str = None
    lote: str = None
    bodega: str = None
    motivo: str = None
