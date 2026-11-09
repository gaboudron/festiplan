from typing import Protocol

from app.domain.concert.entities import Concert


class ConcertRepositoryPort(Protocol):
    """Contrat de persistance des concerts."""

    def get_by_id(self, concert_id: int) -> Concert | None:
        ...

    def get_for_festival(self, festival_id: int) -> list[Concert]:
        ...

    def save(self, concert: Concert) -> Concert:
        ...