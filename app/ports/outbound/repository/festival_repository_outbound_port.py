from abc import ABC, abstractmethod
from app.domain.festival.entities import Festival


class FestivalRepositoryOutboundPort(ABC):
    @abstractmethod
    def get(self, festival_id: int) -> Festival | None:
        """Récupère un festival par son identifiant."""
        pass

    @abstractmethod
    def list_all(self) -> list[Festival]:
        """Retourne l'ensemble des festivals."""
        pass

    @abstractmethod
    def save(self, festival: Festival) -> Festival:
        """Persiste (création ou mise à jour) un festival et le retourne avec son identifiant."""
        pass

