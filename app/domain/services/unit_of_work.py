from sqlmodel import Session


class UnitOfWork:
    """
    Servicio de infraestructura para manejar transacciones.

    RESPONSABILIDAD:
    - Garantizar atomicidad ACID de las operaciones (RNF6)
    - Simplificar manejo de commit y rollback
    - Mantener independencia del dominio (principio SRP)

    APLICADO EN:
    - RF4: Entrada de productos (stock + movimiento atómico)
    - RF5: Salida de productos (validación + stock + movimiento atómico)
    - RNF6: Transaccionalidad y consistencia

    USO:
        with UnitOfWork(db) as uow:
            # Operaciones sobre repos
            # Si hay error, hace rollback automático
            # Si todo OK, hace commit automático
    """

    def __init__(self, db: Session):
        self.db = db

    def __enter__(self):
        # SQLModel Session ya maneja transacciones internamente
        # No necesitamos begin() explícito
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            # Si hubo excepción, hacer rollback
            self.db.rollback()
        # El commit se maneja en los repositorios

    def rollback(self):
        """Rollback manual en caso de error."""
        self.db.rollback()
