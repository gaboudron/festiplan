from typing import Protocol

from app.domain.festival.entities import Festival


class FestivalRepositoryPort(Protocol):
    """Contrat de persistance des festivals."""

    def get_by_id(self, festival_id: int) -> Festival | None:
        ...

    def get_all(self) -> list[Festival]:
        ...

    def save(self, festival: Festival) -> Festival:
        ...