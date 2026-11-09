"""Fixtures partagées pour les tests des cas d'usage.

Les fixtures d'entités s'appuient sur ``factories.py`` et renvoient des objets
neufs à chaque test. Les dépendances sortantes sont doublées par des
``MagicMock(spec=...)`` calés sur les ABC de ``app/ports/outbound/``
(décision 11.B) : aucune base de données ni aucun client HTTP n'est nécessaire.
"""

from unittest.mock import MagicMock

import pytest

from app.domain.time_range import TimeRange
from app.ports.outbound.events.domain_event_bus_outbound_port import (
    DomainEventBusOutboundPort,
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
from app.use_cases import (
    ArtistService,
    ConcertService,
    FestivalService,
    IncidentService,
    StageService,
)
from factories import (
    DEFAULT_CONCERT_END,
    DEFAULT_CONCERT_START,
    DEFAULT_FESTIVAL_END,
    DEFAULT_FESTIVAL_START,
    make_artist,
    make_concert,
    make_festival,
    make_incident,
    make_stage,
)


# ---------------------------------------------------------------------------
# Entités du domaine
# ---------------------------------------------------------------------------


@pytest.fixture
def festival_time_range() -> TimeRange:
    """Créneau par défaut du festival (trois jours en juin 2027)."""
    return TimeRange(DEFAULT_FESTIVAL_START, DEFAULT_FESTIVAL_END)


@pytest.fixture
def concert_time_range() -> TimeRange:
    """Créneau par défaut d'un concert (premier soir du festival)."""
    return TimeRange(DEFAULT_CONCERT_START, DEFAULT_CONCERT_END)


@pytest.fixture
def artist():
    """Artiste valide."""
    return make_artist()


@pytest.fixture
def stage():
    """Scène valide rattachée au festival par défaut."""
    return make_stage()


@pytest.fixture
def festival(stage):
    """Festival en préparation contenant la scène par défaut."""
    return make_festival(stages=[stage])


@pytest.fixture
def concert(festival, artist, stage):
    """Concert programmé cohérent avec le festival, l'artiste et la scène."""
    return make_concert(
        festival_id=festival.id,
        artist_id=artist.id,
        stage_id=stage.id,
    )


@pytest.fixture
def incident(concert):
    """Incident non résolu rattaché au concert par défaut."""
    return make_incident(concert_id=concert.id)


# ---------------------------------------------------------------------------
# Doublures des ports sortants
# ---------------------------------------------------------------------------


@pytest.fixture
def transaction() -> MagicMock:
    return MagicMock(spec=TransactionOutboundPort)


@pytest.fixture
def event_bus() -> MagicMock:
    return MagicMock(spec=DomainEventBusOutboundPort)


@pytest.fixture
def artist_repository() -> MagicMock:
    return MagicMock(spec=ArtistRepositoryOutboundPort)


@pytest.fixture
def stage_repository() -> MagicMock:
    return MagicMock(spec=StageRepositoryOutboundPort)


@pytest.fixture
def festival_repository() -> MagicMock:
    return MagicMock(spec=FestivalRepositoryOutboundPort)


@pytest.fixture
def concert_repository() -> MagicMock:
    return MagicMock(spec=ConcertRepositoryOutboundPort)


@pytest.fixture
def incident_repository() -> MagicMock:
    return MagicMock(spec=IncidentRepositoryOutboundPort)


# ---------------------------------------------------------------------------
# Services applicatifs prêts à l'emploi
# ---------------------------------------------------------------------------


@pytest.fixture
def artist_service(artist_repository, transaction) -> ArtistService:
    return ArtistService(artist_repository, transaction)


@pytest.fixture
def stage_service(stage_repository, festival_repository, transaction) -> StageService:
    return StageService(stage_repository, festival_repository, transaction)


@pytest.fixture
def festival_service(festival_repository, transaction, event_bus) -> FestivalService:
    return FestivalService(festival_repository, transaction, event_bus)


@pytest.fixture
def concert_service(
    concert_repository,
    festival_repository,
    artist_repository,
    stage_repository,
    transaction,
    event_bus,
) -> ConcertService:
    return ConcertService(
        concert_repository,
        festival_repository,
        artist_repository,
        stage_repository,
        transaction,
        event_bus,
    )


@pytest.fixture
def incident_service(
    incident_repository, concert_repository, transaction
) -> IncidentService:
    return IncidentService(incident_repository, concert_repository, transaction)
