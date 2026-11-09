from abc import ABC, abstractmethod
from app.domain.incident.entities import Incident


class IncidentRepositoryOutboundPort(ABC):
    @abstractmethod
    def get(self, incident_id: int) -> Incident | None:
        """Récupère un incident par son identifiant."""
        pass

    @abstractmethod
    def list_all(self) -> list[Incident]:
        """Retourne l'ensemble des incidents."""
        pass

    @abstractmethod
    def list_by_concert_id(self, concert_id: int) -> list[Incident]:
        """Retourne les incidents rattachés à un concert."""
        pass

    @abstractmethod
    def save(self, incident: Incident) -> Incident:
        """Persiste (création ou mise à jour) un incident et le retourne."""
        pass

