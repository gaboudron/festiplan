"""Port entrant pour les festivals."""

from typing import Protocol, runtime_checkable

from app.domain.festival.entities import Festival


@runtime_checkable
class FestivalInboundPort(Protocol):
    """Cas d'usage exposés à l'adaptateur entrant pour les festivals."""

    def list_festivals(self) -> list[Festival]:
        """Retourne tous les festivals."""
        ...

    def create_festival(self, festival: Festival) -> Festival:
        """Crée un festival et retourne l'entité persistée."""
        ...

    def publish_festival(self, festival_id: int) -> Festival:
        """Publie un festival et retourne l'entité mise à jour."""
        ...
