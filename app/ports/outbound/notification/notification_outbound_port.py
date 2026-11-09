from abc import ABC, abstractmethod


class NotificationOutboundPort(ABC):
    @abstractmethod
    def notify_schedule_change(self, concert_id: int, message: str) -> None:
        """Notifie d'un changement d'horaire pour un concert."""
        pass

    @abstractmethod
    def notify_festival_published(self, festival_id: int, message: str) -> None:
        """Notifie de la publication de la programmation d'un festival."""
        pass

    @abstractmethod
    def notify_concert_cancelled(self, concert_id: int, message: str) -> None:
        """Notifie de l'annulation d'un concert."""
        pass

