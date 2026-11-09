"""Port sortant de gestion de la transaction."""

from abc import ABC, abstractmethod


class TransactionOutboundPort(ABC):
    """Port auquel les cas d'usage délèguent la transaction.

    Le cas d'usage ne commit jamais lui-même : il fournit le travail, ce port
    porte le commit (et le rollback en cas d'échec). Les événements de domaine
    sont publiés une fois la transaction validée.
    """

    @abstractmethod
    def commit(self) -> None:
        """Valide la transaction en cours."""
        ...

    @abstractmethod
    def rollback(self) -> None:
        """Annule la transaction en cours."""
        ...

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.rollback()
        return False
