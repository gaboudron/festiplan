from abc import ABC, abstractmethod
from app.domain.concert.entities import Concert


class ConcertRepositoryOutboundPort(ABC):
    @abstractmethod
    def get(self, concert_id: int) -> Concert | None:
        """Récupère un concert par son identifiant."""
        pass

    @abstractmethod
    def list_by_festival_id(self, festival_id: int) -> list[Concert]:
        """Retourne la liste des concerts d'un festival."""
        pass

    @abstractmethod
    def save(self, concert: Concert) -> Concert:
        """Persiste (création ou mise à jour) un concert et le retourne."""
        pass

