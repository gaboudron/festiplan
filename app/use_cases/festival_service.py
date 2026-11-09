"""Service applicatif pour les festivals."""

from app.domain.festival.entities import Festival
from app.domain.festival.events import FestivalPublishedEvent
from app.ports.inbound.festival_inbound_port import FestivalInboundPort
from app.ports.outbound.events.domain_event_bus_outbound_port import (
    DomainEventBusOutboundPort,
)
from app.ports.outbound.repository.festival_repository_outbound_port import (
    FestivalRepositoryOutboundPort,
)
from app.ports.outbound.transaction.transaction_outbound_port import (
    TransactionOutboundPort,
)
from app.use_cases._support import in_transaction, require_festival


class FestivalService(FestivalInboundPort):
    """Implémente ``FestivalInboundPort``."""

    def __init__(
        self,
        festivals: FestivalRepositoryOutboundPort,
        transaction: TransactionOutboundPort,
        event_bus: DomainEventBusOutboundPort,
    ) -> None:
        self._festivals = festivals
        self._transaction = transaction
        self._event_bus = event_bus

    def list_festivals(self) -> list[Festival]:
        return self._festivals.list_all()

    def create_festival(self, festival: Festival) -> Festival:
        return in_transaction(
            self._transaction, lambda: self._festivals.save(festival)
        )

    def publish_festival(self, festival_id: int) -> Festival:
        festival = require_festival(self._festivals, festival_id)
        festival.publish()
        saved = in_transaction(
            self._transaction, lambda: self._festivals.save(festival)
        )
        # Décision 6.A : l'événement est publié après le commit.
        self._event_bus.publish(
            FestivalPublishedEvent(
                festival_id=saved.id if saved.id is not None else festival_id,
                festival_name=saved.name,
            )
        )
        return saved
