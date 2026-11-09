"""Port entrant pour les scènes."""

from abc import ABC, abstractmethod

from app.domain.festival.entities import Stage


class StageInboundPort(ABC):
    """Cas d'usage exposés à l'adaptateur entrant pour les scènes."""

    @abstractmethod
    def list_stages(self, festival_id: int) -> list[Stage]:
        """Retourne les scènes d'un festival."""
        ...

    @abstractmethod
    def create_stage(self, stage: Stage) -> Stage:
        """Crée une scène et retourne l'entité persistée."""
        ...
