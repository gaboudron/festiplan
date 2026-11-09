"""Service applicatif pour les incidents."""

from app.domain.incident.entities import Incident
from app.ports.inbound.incident_inbound_port import IncidentInboundPort
from app.ports.outbound.repository.concert_repository_outbound_port import (
    ConcertRepositoryOutboundPort,
)
from app.ports.outbound.repository.incident_repository_outbound_port import (
    IncidentRepositoryOutboundPort,
)
from app.ports.outbound.transaction.transaction_outbound_port import (
    TransactionOutboundPort,
)
from app.use_cases._support import in_transaction, require_concert


class IncidentService(IncidentInboundPort):
    """Implémente ``IncidentInboundPort``."""

    def __init__(
        self,
        incidents: IncidentRepositoryOutboundPort,
        concerts: ConcertRepositoryOutboundPort,
        transaction: TransactionOutboundPort,
    ) -> None:
        self._incidents = incidents
        self._concerts = concerts
        self._transaction = transaction

    def list_incidents(self, concert_id: int | None = None) -> list[Incident]:
        if concert_id is None:
            return self._incidents.list_all()
        return self._incidents.list_by_concert_id(concert_id)

    def declare_incident(self, incident: Incident) -> Incident:
        # Un incident ne peut concerner qu'un concert existant.
        require_concert(self._concerts, incident.concert_id)
        return in_transaction(
            self._transaction, lambda: self._incidents.save(incident)
        )
