"""Port entrant pour les festivals."""

from abc import ABC, abstractmethod

from app.domain.festival.entities import Festival


class FestivalInboundPort(ABC):
    """Cas d'usage exposés à l'adaptateur entrant pour les festivals."""

    @abstractmethod
    def list_festivals(self) -> list[Festival]:
        """Retourne tous les festivals."""
        ...

    @abstractmethod
    def create_festival(self, festival: Festival) -> Festival:
        """Crée un festival et retourne l'entité persistée."""
        ...

    @abstractmethod
    def publish_festival(self, festival_id: int) -> Festival:
        """Publie un festival et retourne l'entité mise à jour."""
        ...
