"""Adaptateurs sortants pour les événements de domaine."""

from app.adapters.outbound.events.in_memory_event_bus_adapter import (
    InMemoryEventBusAdapter,
)
from app.adapters.outbound.events.notification_handlers import (
    create_event_bus_with_notifications,
    register_notification_handlers,
)

__all__ = [
    "InMemoryEventBusAdapter",
    "create_event_bus_with_notifications",
    "register_notification_handlers",
]

