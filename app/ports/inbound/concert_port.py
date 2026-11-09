"""Port entrant pour les concerts."""

from abc import ABC, abstractmethod

from app.domain.concert.entities import Concert
from app.domain.time_range import TimeRange


class ConcertInboundPort(ABC):
    """Cas d'usage exposés à l'adaptateur entrant pour les concerts."""

    @abstractmethod
    def list_concerts(self, festival_id: int) -> list[Concert]:
        """Retourne les concerts non annulés d'un festival."""
        ...

    @abstractmethod
    def get_concert(self, concert_id: int) -> Concert:
        """Retourne un concert ou lève ``ConcertNotFoundError``."""
        ...

    @abstractmethod
    def create_concert(self, concert: Concert) -> Concert:
        """Programme un concert et retourne l'entité persistée."""
        ...

    @abstractmethod
    def reschedule_concert(
        self,
        concert_id: int,
        new_time_range: TimeRange,
        new_stage_id: int | None = None,
    ) -> Concert:
        """Déplace un concert et, si fourni, le change de scène.

        ``new_stage_id`` à ``None`` conserve la scène actuelle.
        """
        ...

    @abstractmethod
    def cancel_concert(self, concert_id: int) -> Concert:
        """Annule un concert et retourne l'entité mise à jour."""
        ...

    @abstractmethod
    def get_schedule(self, festival_id: int) -> list[Concert]:
        """Retourne le planning d'un festival."""
        ...
