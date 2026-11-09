"""Port entrant pour les incidents."""

from abc import ABC, abstractmethod

from app.domain.incident.entities import Incident


class IncidentInboundPort(ABC):
    """Cas d'usage exposés à l'adaptateur entrant pour les incidents."""

    @abstractmethod
    def list_incidents(self, concert_id: int | None = None) -> list[Incident]:
        """Retourne les incidents, éventuellement filtrés par concert."""
        ...

    @abstractmethod
    def declare_incident(self, incident: Incident) -> Incident:
        """Déclare un incident et retourne l'entité persistée."""
        ...

    def resolve_incident(self, incident_id: int) -> Incident:
        """Marque un incident comme résolu et retourne l'entité persistée."""
        raise NotImplementedError
