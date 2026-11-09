"""Port sortant de publication des événements de domaine."""

from abc import ABC, abstractmethod


class DomainEventBusOutboundPort(ABC):
    """Bus auquel les cas d'usage publient leurs événements après commit.

    Les handlers (notifications, outbox, retry...) sont abonnés côté adaptateur
    et seront câblés avec l'injection de dépendances.
    """

    @abstractmethod
    def publish(self, event: object) -> None:
        """Diffuse un événement de domaine aux handlers abonnés."""
        ...
