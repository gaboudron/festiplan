from typing import Protocol

from app.domain.incident.entities import Incident


class IncidentRepositoryPort(Protocol):
    """Contrat de persistance des incidents."""

    def get_by_id(self, incident_id: int) -> Incident | None:
        ...

    def get_for_concert(self, concert_id: int) -> list[Incident]:
        ...

    def save(self, incident: Incident) -> Incident:
        ...