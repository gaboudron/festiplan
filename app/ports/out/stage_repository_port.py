from typing import Protocol

from app.domain.festival.entities import Stage


class StageRepositoryPort(Protocol):
    """Contrat de persistance des scènes."""

    def get_by_id(self, stage_id: int) -> Stage | None:
        ...

    def get_for_festival(self, festival_id: int) -> list[Stage]:
        ...

    def save(self, stage: Stage) -> Stage:
        ...