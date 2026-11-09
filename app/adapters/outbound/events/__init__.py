"""Adaptateurs sortants pour les événements de domaine.

Fournit un bus en mémoire et les handlers qui traduisent les événements
publiés après commit en notifications via ``NotificationOutboundPort``.
Les erreurs d'un handler sont journalisées sans faire échouer l'opération
métier déjà validée.
"""

from app.adapters.outbound.events.in_memory_event_bus_adapter import (
    InMemoryEventBusAdapter,
)
from app.adapters.outbound.events.notification_handlers import (
    create_event_bus_with_notifications,
    handle_concert_cancelled,
    handle_concert_rescheduled,
    handle_festival_published,
    register_notification_handlers,
)

__all__ = [
    "InMemoryEventBusAdapter",
    "create_event_bus_with_notifications",
    "handle_concert_cancelled",
    "handle_concert_rescheduled",
    "handle_festival_published",
    "register_notification_handlers",
]
