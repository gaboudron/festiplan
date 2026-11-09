"""Port entrant pour les concerts."""

from typing import Protocol, runtime_checkable

from app.domain.concert.entities import Concert
from app.domain.time_range import TimeRange


@runtime_checkable
class ConcertInboundPort(Protocol):
    """Cas d'usage exposés à l'adaptateur entrant pour les concerts."""

    def list_concerts(self, festival_id: int) -> list[Concert]:
        """Retourne les concerts non annulés d'un festival."""
        ...

    def get_concert(self, concert_id: int) -> Concert:
        """Retourne un concert ou lève ``ConcertNotFoundError``."""
        ...

    def create_concert(self, concert: Concert) -> Concert:
        """Programme un concert et retourne l'entité persistée."""
        ...

    def reschedule_concert(
        self,
        concert_id: int,
        new_time_range: TimeRange,
        new_stage_id: int | None = None,
    ) -> Concert:
        """Déplace un concert et, si fourni, le change de scène."""
        ...

    def cancel_concert(self, concert_id: int) -> Concert:
        """Annule un concert et retourne l'entité mise à jour."""
        ...

    def get_schedule(self, festival_id: int) -> list[Concert]:
        """Retourne le planning d'un festival."""
        ...
