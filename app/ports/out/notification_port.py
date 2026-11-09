from typing import Protocol


class NotificationPort(Protocol):
    """Contrat d'envoi des notifications."""

    def send_notification(
        self,
        recipient: str,
        subject: str,
        message: str,
    ) -> None:
        ...