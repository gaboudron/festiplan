"""Handlers abonnés au bus d'événements traduisant les événements en notifications."""

from app.adapters.outbound.events.in_memory_event_bus_adapter import (
    InMemoryEventBusAdapter,
)
from app.domain.concert.events import (
    ConcertCancelledEvent,
    ConcertRescheduledEvent,
)
from app.domain.festival.events import FestivalPublishedEvent
from app.ports.outbound.notification.notification_outbound_port import (
    NotificationOutboundPort,
)


def handle_festival_published(
    event: FestivalPublishedEvent,
    notification_port: NotificationOutboundPort,
) -> None:
    """Traduit ``FestivalPublishedEvent`` en notification de publication."""
    message = f"Le planning du festival {event.festival_name} a été publié."
    notification_port.notify_festival_published(event.festival_id, message)


def handle_concert_rescheduled(
    event: ConcertRescheduledEvent,
    notification_port: NotificationOutboundPort,
) -> None:
    """Traduit ``ConcertRescheduledEvent`` en notification de changement d'horaire."""
    message = f"Concert déplacé au {event.new_time_range.start.isoformat()}"
    notification_port.notify_schedule_change(event.concert_id, message)


def handle_concert_cancelled(
    event: ConcertCancelledEvent,
    notification_port: NotificationOutboundPort,
) -> None:
    """Traduit ``ConcertCancelledEvent`` en notification d'annulation."""
    message = f"Le concert #{event.concert_id} a été annulé."
    notification_port.notify_concert_cancelled(event.concert_id, message)


def register_notification_handlers(
    event_bus: InMemoryEventBusAdapter,
    notification_port: NotificationOutboundPort,
) -> None:
    """Abonne les handlers de notification aux événements de domaine correspondants."""
    event_bus.subscribe(
        FestivalPublishedEvent,
        lambda event: handle_festival_published(event, notification_port),
    )
    event_bus.subscribe(
        ConcertRescheduledEvent,
        lambda event: handle_concert_rescheduled(event, notification_port),
    )
    event_bus.subscribe(
        ConcertCancelledEvent,
        lambda event: handle_concert_cancelled(event, notification_port),
    )


def create_event_bus_with_notifications(
    notification_port: NotificationOutboundPort,
    suppress_errors: bool = True,
) -> InMemoryEventBusAdapter:
    """Fabrique un bus d'événements configuré avec les handlers de notification."""
    event_bus = InMemoryEventBusAdapter(suppress_errors=suppress_errors)
    register_notification_handlers(event_bus, notification_port)
    return event_bus

