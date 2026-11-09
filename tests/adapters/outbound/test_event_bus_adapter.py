from datetime import datetime, timezone
from unittest.mock import MagicMock

import pytest

from app.adapters.outbound.events import (
    InMemoryEventBusAdapter,
    create_event_bus_with_notifications,
    register_notification_handlers,
)
from app.domain.concert.events import (
    ConcertCancelledEvent,
    ConcertRescheduledEvent,
)
from app.domain.festival.events import FestivalPublishedEvent
from app.domain.time_range import TimeRange
from app.ports.outbound.events.domain_event_bus_outbound_port import (
    DomainEventBusOutboundPort,
)
from app.ports.outbound.notification.notification_outbound_port import (
    NotificationOutboundPort,
)


def test_in_memory_event_bus_implements_port():
    bus = InMemoryEventBusAdapter()
    assert isinstance(bus, DomainEventBusOutboundPort)


def test_publish_notifies_subscribed_handlers():
    bus = InMemoryEventBusAdapter()
    received = []

    bus.subscribe(FestivalPublishedEvent, lambda event: received.append(event))

    event = FestivalPublishedEvent(festival_id=1, festival_name="Hellfest")
    bus.publish(event)

    assert len(received) == 1
    assert received[0] is event
    assert bus.published_events == [event]


def test_multiple_subscribers_on_same_event():
    bus = InMemoryEventBusAdapter()
    calls = []

    bus.subscribe(FestivalPublishedEvent, lambda e: calls.append("handler_1"))
    bus.subscribe(FestivalPublishedEvent, lambda e: calls.append("handler_2"))

    bus.publish(FestivalPublishedEvent(festival_id=1, festival_name="Hellfest"))

    assert calls == ["handler_1", "handler_2"]


def test_publish_unsubscribed_event_does_not_fail():
    bus = InMemoryEventBusAdapter()
    event = FestivalPublishedEvent(festival_id=1, festival_name="Hellfest")

    # Aucun handler abonné, l'appel ne doit pas lever d'erreur
    bus.publish(event)
    assert bus.published_events == [event]


def test_handler_error_suppressed_by_default(caplog):
    bus = InMemoryEventBusAdapter(suppress_errors=True)

    def failing_handler(e):
        raise RuntimeError("Erreur réseau inattendue")

    bus.subscribe(FestivalPublishedEvent, failing_handler)

    # Ne doit pas lever d'exception
    bus.publish(FestivalPublishedEvent(festival_id=1, festival_name="Hellfest"))
    assert "Erreur réseau inattendue" in caplog.text


def test_handler_error_raised_when_suppress_errors_disabled():
    bus = InMemoryEventBusAdapter(suppress_errors=False)

    def failing_handler(e):
        raise RuntimeError("Erreur réseau inattendue")

    bus.subscribe(FestivalPublishedEvent, failing_handler)

    with pytest.raises(RuntimeError, match="Erreur réseau inattendue"):
        bus.publish(FestivalPublishedEvent(festival_id=1, festival_name="Hellfest"))


def test_notification_handlers_translation():
    mock_notification = MagicMock(spec=NotificationOutboundPort)
    bus = InMemoryEventBusAdapter()
    register_notification_handlers(bus, mock_notification)

    # 1. Festival publié
    pub_event = FestivalPublishedEvent(festival_id=42, festival_name="ElectroBeach")
    bus.publish(pub_event)
    mock_notification.notify_festival_published.assert_called_once_with(
        42, "Le planning du festival ElectroBeach a été publié."
    )

    # 2. Concert reprogrammé
    resched_event = ConcertRescheduledEvent(
        concert_id=7,
        festival_id=42,
        new_time_range=TimeRange(
            start=datetime(2027, 7, 10, 20, 0, tzinfo=timezone.utc),
            end=datetime(2027, 7, 10, 21, 30, tzinfo=timezone.utc),
        ),
    )
    bus.publish(resched_event)
    mock_notification.notify_schedule_change.assert_called_once_with(
        7,
        f"Concert déplacé au {resched_event.new_time_range.start.isoformat()}",
    )

    # 3. Concert annulé
    cancel_event = ConcertCancelledEvent(concert_id=7, festival_id=42)
    bus.publish(cancel_event)
    mock_notification.notify_concert_cancelled.assert_called_once_with(
        7, "Le concert #7 a été annulé."
    )


def test_create_event_bus_with_notifications_factory():
    mock_notification = MagicMock(spec=NotificationOutboundPort)
    bus = create_event_bus_with_notifications(mock_notification)

    assert isinstance(bus, InMemoryEventBusAdapter)

    bus.publish(FestivalPublishedEvent(festival_id=99, festival_name="Download"))
    mock_notification.notify_festival_published.assert_called_once_with(
        99, "Le planning du festival Download a été publié."
    )

