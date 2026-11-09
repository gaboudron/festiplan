"""Fournisseurs d'injection de dépendances pour l'API FastAPI."""

from fastapi import Depends
from sqlalchemy.orm import Session

from app.adapters.outbound.events import create_event_bus_with_notifications
from app.adapters.outbound.notification.email_notification_adapter import (
    EmailNotificationAdapter,
)
from app.adapters.outbound.repository.artist_sqlalchemy_repository import (
    ArtistSqlAlchemyRepository,
)
from app.adapters.outbound.repository.concert_sqlalchemy_repository import (
    ConcertSqlAlchemyRepository,
)
from app.adapters.outbound.repository.festival_sqlalchemy_repository import (
    FestivalSqlAlchemyRepository,
)
from app.adapters.outbound.repository.incident_sqlalchemy_repository import (
    IncidentSqlAlchemyRepository,
)
from app.adapters.outbound.repository.stage_sqlalchemy_repository import (
    StageSqlAlchemyRepository,
)
from app.adapters.outbound.transaction.transaction_sqlalchemy_adapter import (
    SqlAlchemyTransactionAdapter,
)
from app.database import get_db
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
from app.use_cases.artist_service import ArtistService
from app.use_cases.concert_service import ConcertService
from app.use_cases.festival_service import FestivalService
from app.use_cases.incident_service import IncidentService
from app.use_cases.stage_service import StageService


# ---------------------------------------------------------------------------
# Adaptateurs techniques et ports sortants transverses
# ---------------------------------------------------------------------------

def get_transaction_port(db: Session = Depends(get_db)) -> TransactionOutboundPort:
    """Fournit l'adaptateur de transaction SQLAlchemy pour la session en cours."""
    return SqlAlchemyTransactionAdapter(db)


def get_notification_port() -> NotificationOutboundPort:
    """Fournit l'adaptateur d'envoi de notifications par email."""
    return EmailNotificationAdapter()


def get_event_bus(
    notification_port: NotificationOutboundPort = Depends(get_notification_port),
) -> DomainEventBusOutboundPort:
    """Fournit le bus d'événements de domaine configuré avec les handlers de notification."""
    return create_event_bus_with_notifications(notification_port)


# ---------------------------------------------------------------------------
# Repositories sortants (persistance)
# ---------------------------------------------------------------------------

def get_festival_repository(
    db: Session = Depends(get_db),
) -> FestivalRepositoryOutboundPort:
    return FestivalSqlAlchemyRepository(db)


def get_stage_repository(
    db: Session = Depends(get_db),
) -> StageRepositoryOutboundPort:
    return StageSqlAlchemyRepository(db)


def get_artist_repository(
    db: Session = Depends(get_db),
) -> ArtistRepositoryOutboundPort:
    return ArtistSqlAlchemyRepository(db)


def get_concert_repository(
    db: Session = Depends(get_db),
) -> ConcertRepositoryOutboundPort:
    return ConcertSqlAlchemyRepository(db)


def get_incident_repository(
    db: Session = Depends(get_db),
) -> IncidentRepositoryOutboundPort:
    return IncidentSqlAlchemyRepository(db)


# ---------------------------------------------------------------------------
# Services applicatifs / Cas d'usage (Ports entrants)
# ---------------------------------------------------------------------------

def get_festival_service(
    festivals: FestivalRepositoryOutboundPort = Depends(get_festival_repository),
    transaction: TransactionOutboundPort = Depends(get_transaction_port),
    event_bus: DomainEventBusOutboundPort = Depends(get_event_bus),
) -> FestivalInboundPort:
    return FestivalService(
        festivals=festivals,
        transaction=transaction,
        event_bus=event_bus,
    )


def get_concert_service(
    concerts: ConcertRepositoryOutboundPort = Depends(get_concert_repository),
    festivals: FestivalRepositoryOutboundPort = Depends(get_festival_repository),
    artists: ArtistRepositoryOutboundPort = Depends(get_artist_repository),
    stages: StageRepositoryOutboundPort = Depends(get_stage_repository),
    transaction: TransactionOutboundPort = Depends(get_transaction_port),
    event_bus: DomainEventBusOutboundPort = Depends(get_event_bus),
) -> ConcertInboundPort:
    return ConcertService(
        concerts=concerts,
        festivals=festivals,
        artists=artists,
        stages=stages,
        transaction=transaction,
        event_bus=event_bus,
    )


def get_stage_service(
    stages: StageRepositoryOutboundPort = Depends(get_stage_repository),
    festivals: FestivalRepositoryOutboundPort = Depends(get_festival_repository),
    transaction: TransactionOutboundPort = Depends(get_transaction_port),
) -> StageInboundPort:
    return StageService(
        stages=stages,
        festivals=festivals,
        transaction=transaction,
    )


def get_artist_service(
    artists: ArtistRepositoryOutboundPort = Depends(get_artist_repository),
    transaction: TransactionOutboundPort = Depends(get_transaction_port),
) -> ArtistInboundPort:
    return ArtistService(
        artists=artists,
        transaction=transaction,
    )


def get_incident_service(
    incidents: IncidentRepositoryOutboundPort = Depends(get_incident_repository),
    concerts: ConcertRepositoryOutboundPort = Depends(get_concert_repository),
    transaction: TransactionOutboundPort = Depends(get_transaction_port),
) -> IncidentInboundPort:
    return IncidentService(
        incidents=incidents,
        concerts=concerts,
        transaction=transaction,
    )
