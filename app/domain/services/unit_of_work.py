# -*- coding: utf-8 -*-
"""
Unit of Work - Patrón para Transacciones Atómicas (RNF6)

Garantiza que múltiples operaciones se ejecuten como una unidad:
- Si todas tienen éxito → COMMIT (guardar cambios)
- Si alguna falla → ROLLBACK (revertir todo)
"""

from sqlmodel import Session


class UnitOfWork:
    """
    Servicio para manejar transacciones atómicas (RNF6).

    RESPONSABILIDAD:
    - Garantizar atomicidad ACID de las operaciones
    - Commit automático si todo sale bien
    - Rollback automático si algo falla
    - Mantener consistencia de datos

    APLICADO EN:
    - RF4: Entrada de productos (actualizar stock + crear movimiento)
    - RF5: Salida de productos (validar + actualizar stock + crear movimiento)
    - RNF6: Transaccionalidad y consistencia

    EJEMPLO DE USO:
        with UnitOfWork(db):
            # Operación 1: actualizar stock
            producto.stock += 50
            producto_repo.actualizar(producto)

            # Operación 2: crear movimiento
            movimiento_repo.crear_movimiento(movimiento)

            # Si ambas OK → commit automático ✅
            # Si alguna falla → rollback automático ✅
    """

    def __init__(self, db: Session):
        self.db = db
        self._should_commit = True

    def __enter__(self):
        """Inicia el contexto de la transacción."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Finaliza la transacción:
        - Si no hubo errores (exc_type es None) → COMMIT
        - Si hubo error → ROLLBACK
        """
        if exc_type is not None:
            # Hubo una excepción, hacer rollback
            self.db.rollback()
            return False  # Re-lanza la excepción
        else:
            # Todo salió bien, hacer commit
            if self._should_commit:
                self.db.commit()
            return True

    def commit(self):
        """Commit manual (opcional)."""
        self.db.commit()

    def rollback(self):
        """Rollback manual (opcional)."""
        self.db.rollback()
        self._should_commit = False
