from app.ports.outbound.notification.notification_outbound_port import (
    NotificationOutboundPort,
)
from app.utils.email_sender import send_email


class EmailNotificationAdapter(NotificationOutboundPort):
    def __init__(self, default_recipient: str = "production@festiplan.test"):
        self.default_recipient = default_recipient

    def notify_schedule_change(self, concert_id: int, message: str) -> None:
        subject = f"Modification du concert #{concert_id}"
        send_email(self.default_recipient, subject, message)

    def notify_festival_published(self, festival_id: int, message: str) -> None:
        subject = f"Publication du festival #{festival_id}"
        send_email(self.default_recipient, subject, message)

    def notify_concert_cancelled(self, concert_id: int, message: str) -> None:
        subject = f"Annulation du concert #{concert_id}"
        send_email(self.default_recipient, subject, message)

