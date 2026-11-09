"""Tests des contrats de ports sortants (outbound).

Les ports sont des classes abstraites : une implémentation doit fournir
toutes les méthodes, sinon elle ne peut pas être instanciée.
"""

import inspect

import pytest

from app.domain.artist.entities import Artist
from app.domain.concert.entities import Concert
from app.domain.festival.entities import Festival, Stage
from app.domain.incident.entities import Incident
from app.ports.outbound.notification.notification_outbound_port import (
    NotificationOutboundPort,
)
from app.ports.outbound.transaction.transaction_outbound_port import (
    TransactionOutboundPort,
)
from app.ports.outbound.repository.artist_repository_outbound_port import (
    ArtistRepositoryOutboundPort,
)
from app.ports.outbound.repository.concert_repository_outbound_port import (
    ConcertRepositoryOutboundPort,
)
from app.ports.outbound.repository.festival_repository_outbound_port import (
    FestivalRepositoryOutboundPort,
)
from app.ports.outbound.repository.incident_repository_outbound_port import (
    IncidentRepositoryOutboundPort,
)
from app.ports.outbound.repository.stage_repository_outbound_port import (
    StageRepositoryOutboundPort,
)

# ==========================
# Implémentations factices
# ==========================


class FakeArtistRepositoryPort(ArtistRepositoryOutboundPort):
    def get(self, artist_id: int) -> Artist | None:
        return None

    def list_all(self) -> list[Artist]:
        return []

    def save(self, artist: Artist) -> Artist:
        return artist


class FakeConcertRepositoryPort(ConcertRepositoryOutboundPort):
    def get(self, concert_id: int) -> Concert | None:
        return None

    def list_by_festival_id(self, festival_id: int) -> list[Concert]:
        return []

    def save(self, concert: Concert) -> Concert:
        return concert


class FakeFestivalRepositoryPort(FestivalRepositoryOutboundPort):
    def get(self, festival_id: int) -> Festival | None:
        return None

    def list_all(self) -> list[Festival]:
        return []

    def save(self, festival: Festival) -> Festival:
        return festival


class FakeIncidentRepositoryPort(IncidentRepositoryOutboundPort):
    def get(self, incident_id: int) -> Incident | None:
        return None

    def list_all(self) -> list[Incident]:
        return []

    def list_by_concert_id(self, concert_id: int) -> list[Incident]:
        return []

    def save(self, incident: Incident) -> Incident:
        return incident


class FakeStageRepositoryPort(StageRepositoryOutboundPort):
    def get(self, stage_id: int) -> Stage | None:
        return None

    def list_by_festival_id(self, festival_id: int) -> list[Stage]:
        return []

    def save(self, stage: Stage) -> Stage:
        return stage


class FakeNotificationPort(NotificationOutboundPort):
    def notify_schedule_change(self, concert_id: int, message: str) -> None:
        pass

    def notify_festival_published(self, festival_id: int, message: str) -> None:
        pass

    def notify_concert_cancelled(self, concert_id: int, message: str) -> None:
        pass


class FakeTransactionPort(TransactionOutboundPort):
    def commit(self) -> None:
        pass

    def rollback(self) -> None:
        pass


# ==========================
# Tests
# ==========================


def test_ports_are_abstract():
    for port in (
        ArtistRepositoryOutboundPort,
        ConcertRepositoryOutboundPort,
        FestivalRepositoryOutboundPort,
        IncidentRepositoryOutboundPort,
        StageRepositoryOutboundPort,
        NotificationOutboundPort,
        TransactionOutboundPort,
    ):
        with pytest.raises(TypeError):
            port()


def test_complete_implementations_are_valid():
    assert isinstance(FakeArtistRepositoryPort(), ArtistRepositoryOutboundPort)
    assert isinstance(FakeConcertRepositoryPort(), ConcertRepositoryOutboundPort)
    assert isinstance(FakeFestivalRepositoryPort(), FestivalRepositoryOutboundPort)
    assert isinstance(FakeIncidentRepositoryPort(), IncidentRepositoryOutboundPort)
    assert isinstance(FakeStageRepositoryPort(), StageRepositoryOutboundPort)
    assert isinstance(FakeNotificationPort(), NotificationOutboundPort)
    assert isinstance(FakeTransactionPort(), TransactionOutboundPort)


def test_incomplete_implementation_cannot_be_instantiated():
    class IncompleteArtistRepositoryPort(ArtistRepositoryOutboundPort):
        def get(self, artist_id: int) -> Artist | None:
            return None

    with pytest.raises(TypeError):
        IncompleteArtistRepositoryPort()

    class IncompleteNotificationPort(NotificationOutboundPort):
        def notify_schedule_change(self, concert_id: int, message: str) -> None:
            pass

    with pytest.raises(TypeError):
        IncompleteNotificationPort()

    class IncompleteTransactionPort(TransactionOutboundPort):
        def commit(self) -> None:
            pass

    with pytest.raises(TypeError):
        IncompleteTransactionPort()


def test_repository_ports_signatures():
    get_sig = inspect.signature(ArtistRepositoryOutboundPort.get)
    assert "artist_id" in get_sig.parameters

    save_sig = inspect.signature(FestivalRepositoryOutboundPort.save)
    assert "festival" in save_sig.parameters

    concert_by_fest_sig = inspect.signature(ConcertRepositoryOutboundPort.list_by_festival_id)
    assert "festival_id" in concert_by_fest_sig.parameters

    incident_by_concert_sig = inspect.signature(IncidentRepositoryOutboundPort.list_by_concert_id)
    assert "concert_id" in incident_by_concert_sig.parameters

    stage_by_fest_sig = inspect.signature(StageRepositoryOutboundPort.list_by_festival_id)
    assert "festival_id" in stage_by_fest_sig.parameters


def test_notification_port_signatures():
    for method_name in (
        "notify_schedule_change",
        "notify_festival_published",
        "notify_concert_cancelled",
    ):
        sig = inspect.signature(getattr(NotificationOutboundPort, method_name))
        assert "message" in sig.parameters

