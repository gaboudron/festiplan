"""Port entrant pour les incidents."""

from typing import Protocol, runtime_checkable

from app.domain.incident.entities import Incident


@runtime_checkable
class IncidentInboundPort(Protocol):
    """Cas d'usage exposés à l'adaptateur entrant pour les incidents."""

    def list_incidents(self, concert_id: int | None = None) -> list[Incident]:
        """Retourne les incidents, éventuellement filtrés par concert."""
        ...

    def declare_incident(self, incident: Incident) -> Incident:
        """Déclare un incident et retourne l'entité persistée."""
        ...
