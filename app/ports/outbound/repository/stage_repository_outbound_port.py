from abc import ABC, abstractmethod
from app.domain.festival.entities import Stage


class StageRepositoryOutboundPort(ABC):
    @abstractmethod
    def get(self, stage_id: int) -> Stage | None:
        """Récupère une scène par son identifiant."""
        pass

    @abstractmethod
    def list_by_festival_id(self, festival_id: int) -> list[Stage]:
        """Retourne toutes les scènes rattachées à un festival."""
        pass

    @abstractmethod
    def save(self, stage: Stage) -> Stage:
        """Persiste (création ou mise à jour) une scène et la retourne."""
        pass

