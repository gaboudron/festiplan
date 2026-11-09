"""Adaptateur en mémoire pour le bus d'événements de domaine."""

from collections import defaultdict
import logging
from typing import Any, Callable, TypeVar

from app.ports.outbound.events.domain_event_bus_outbound_port import (
    DomainEventBusOutboundPort,
)

logger = logging.getLogger(__name__)

T = TypeVar("T")


class InMemoryEventBusAdapter(DomainEventBusOutboundPort):
    """Implémentation concrète en mémoire de ``DomainEventBusOutboundPort``.

    Permet d'enregistrer des handlers synchrones et de diffuser les événements
    de domaine publiés après commit par les cas d'usage.

    Par défaut, ``suppress_errors=True`` permet de protéger la transaction
    déjà validée : une erreur dans un handler secondaire (ex: panne SMTP lors
    de l'envoi d'email) est consignée dans les logs mais ne fait pas échouer
    l'opération métier principale.
    """

    def __init__(self, suppress_errors: bool = True) -> None:
        self._subscribers: dict[type, list[Callable[[Any], None]]] = defaultdict(list)
        self._suppress_errors = suppress_errors
        self._published_events: list[object] = []

    @property
    def published_events(self) -> list[object]:
        """Retourne la liste des événements publiés (utile pour l'observabilité et les tests)."""
        return list(self._published_events)

    def subscribe(self, event_type: type[T], handler: Callable[[T], None]) -> None:
        """Abonne un handler à un type d'événement de domaine spécifique."""
        self._subscribers[event_type].append(handler)

    def publish(self, event: object) -> None:
        """Diffuse un événement de domaine à tous les handlers abonnés.

        Si un handler échoue et que ``suppress_errors`` est activé, l'erreur est
        capturée et journalisée pour ne pas interrompre le flux applicatif.
        """
        self._published_events.append(event)

        for event_type, handlers in self._subscribers.items():
            if isinstance(event, event_type):
                for handler in handlers:
                    try:
                        handler(event)
                    except Exception as exc:
                        logger.error(
                            "Erreur lors de l'exécution du handler %r pour l'événement %r: %s",
                            handler,
                            event,
                            exc,
                            exc_info=True,
                        )
                        if not self._suppress_errors:
                            raise

