"""Tests unitaires du conteneur d'injection de dépendances FastAPI."""

from unittest.mock import MagicMock
from sqlalchemy.orm import Session

from app.adapters.inbound.api.dependencies import (
    get_artist_repository,
    get_artist_service,
    get_concert_repository,
    get_concert_service,
    get_event_bus,
    get_festival_repository,
    get_festival_service,
    get_incident_repository,
    get_incident_service,
    get_notification_port,
    get_stage_repository,
    get_stage_service,
    get_transaction_port,
)
from app.ports.inbound.artist_inbound_port import ArtistInboundPort
from app.ports.inbound.concert_inbound_port import ConcertInboundPort
from app.ports.inbound.festival_inbound_port import FestivalInboundPort
from app.ports.inbound.incident_inbound_port import IncidentInboundPort
from app.ports.inbound.stage_inbound_port import StageInboundPort
from app.ports.outbound.events.domain_event_bus_outbound_port import (
    DomainEventBusOutboundPort,
)
from app.ports.outbound.notification.notification_outbound_port import (
    NotificationOutboundPort,
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
from app.ports.outbound.transaction.transaction_outbound_port import (
    TransactionOutboundPort,
)


def test_transaction_dependency():
    mock_db = MagicMock(spec=Session)
    adapter = get_transaction_port(mock_db)
    assert isinstance(adapter, TransactionOutboundPort)
    assert adapter.db is mock_db


def test_notification_dependency():
    adapter = get_notification_port()
    assert isinstance(adapter, NotificationOutboundPort)


def test_event_bus_dependency():
    mock_notif = MagicMock(spec=NotificationOutboundPort)
    bus = get_event_bus(mock_notif)
    assert isinstance(bus, DomainEventBusOutboundPort)


def test_repository_dependencies():
    mock_db = MagicMock(spec=Session)

    assert isinstance(get_festival_repository(mock_db), FestivalRepositoryOutboundPort)
    assert isinstance(get_stage_repository(mock_db), StageRepositoryOutboundPort)
    assert isinstance(get_artist_repository(mock_db), ArtistRepositoryOutboundPort)
    assert isinstance(get_concert_repository(mock_db), ConcertRepositoryOutboundPort)
    assert isinstance(get_incident_repository(mock_db), IncidentRepositoryOutboundPort)


def test_use_case_dependencies():
    mock_festivals = MagicMock(spec=FestivalRepositoryOutboundPort)
    mock_stages = MagicMock(spec=StageRepositoryOutboundPort)
    mock_artists = MagicMock(spec=ArtistRepositoryOutboundPort)
    mock_concerts = MagicMock(spec=ConcertRepositoryOutboundPort)
    mock_incidents = MagicMock(spec=IncidentRepositoryOutboundPort)
    mock_tx = MagicMock(spec=TransactionOutboundPort)
    mock_bus = MagicMock(spec=DomainEventBusOutboundPort)

    festival_service = get_festival_service(
        festivals=mock_festivals,
        transaction=mock_tx,
        event_bus=mock_bus,
    )
    assert isinstance(festival_service, FestivalInboundPort)

    concert_service = get_concert_service(
        concerts=mock_concerts,
        festivals=mock_festivals,
        artists=mock_artists,
        stages=mock_stages,
        transaction=mock_tx,
        event_bus=mock_bus,
    )
    assert isinstance(concert_service, ConcertInboundPort)

    stage_service = get_stage_service(
        stages=mock_stages,
        festivals=mock_festivals,
        transaction=mock_tx,
    )
    assert isinstance(stage_service, StageInboundPort)

    artist_service = get_artist_service(
        artists=mock_artists,
        transaction=mock_tx,
    )
    assert isinstance(artist_service, ArtistInboundPort)

    incident_service = get_incident_service(
        incidents=mock_incidents,
        concerts=mock_concerts,
        transaction=mock_tx,
    )
    assert isinstance(incident_service, IncidentInboundPort)

