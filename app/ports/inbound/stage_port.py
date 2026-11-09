"""Port entrant pour les scènes."""

from typing import Protocol, runtime_checkable

from app.domain.festival.entities import Stage


@runtime_checkable
class StageInboundPort(Protocol):
    """Cas d'usage exposés à l'adaptateur entrant pour les scènes."""

    def list_stages(self, festival_id: int) -> list[Stage]:
        """Retourne les scènes d'un festival."""
        ...

    def create_stage(self, stage: Stage) -> Stage:
        """Crée une scène et retourne l'entité persistée."""
        ...
