from sqlalchemy.orm import Session

class UnitOfWork:
    """
    Servicio de infraestructura para manejar transacciones.

    RESPONSABILIDAD:
    - Garantizar atomicidad ACID de las operaciones
    - Simplificar manejo de commit y rollback
    - Mantener independencia del dominio (principio SRP)
    """

    def __init__(self, db: Session):
        self.db = db

    def __enter__(self):
        self.transaction = self.db.begin()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.transaction.rollback()
        else:
            self.transaction.commit()

    def rollback(self):
        self.transaction.rollback()
