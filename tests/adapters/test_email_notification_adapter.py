from unittest.mock import patch
import pytest
from app.adapters.outbound.notification.email_notification_adapter import (
    EmailNotificationAdapter,
)
from app.ports.outbound.notification.notification_outbound_port import (
    NotificationOutboundPort,
)


def test_email_notification_adapter_implements_port():
    adapter = EmailNotificationAdapter()
    assert isinstance(adapter, NotificationOutboundPort)


@patch("app.adapters.outbound.notification.email_notification_adapter.send_email")
def test_notify_schedule_change(mock_send_email):
    adapter = EmailNotificationAdapter()
    adapter.notify_schedule_change(10, "Nouvel horaire : 21h00")

    mock_send_email.assert_called_once_with(
        "production@festiplan.test",
        "Modification du concert #10",
        "Nouvel horaire : 21h00",
    )


@patch("app.adapters.outbound.notification.email_notification_adapter.send_email")
def test_notify_festival_published(mock_send_email):
    adapter = EmailNotificationAdapter()
    adapter.notify_festival_published(1, "Le festival a été publié")

    mock_send_email.assert_called_once_with(
        "production@festiplan.test",
        "Publication du festival #1",
        "Le festival a été publié",
    )


@patch("app.adapters.outbound.notification.email_notification_adapter.send_email")
def test_notify_concert_cancelled(mock_send_email):
    adapter = EmailNotificationAdapter()
    adapter.notify_concert_cancelled(5, "Le concert a été annulé")

    mock_send_email.assert_called_once_with(
        "production@festiplan.test",
        "Annulation du concert #5",
        "Le concert a été annulé",
    )

