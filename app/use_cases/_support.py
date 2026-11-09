"""Helpers partagés par les services applicatifs.

Ici vivent les deux mécanismes transverses :

- la délégation de la transaction au port sortant (décision 5.A) ;
- la résolution des entités liées, avec les exceptions ``*NotFoundError`` du
  domaine plutôt que des ``ValueError``.
"""

from typing import Callable, TypeVar

from app.domain.artist.entities import Artist
from app.domain.concert.entities import Concert
from app.domain.exceptions import (
    ArtistNotFoundError,
    ConcertNotFoundError,
    FestivalNotFoundError,
    StageNotFoundError,
)
from app.domain.festival.entities import Festival, Stage
from app.ports.outbound.repository.artist_repository_outbound_port import (
    ArtistRepositoryOutboundPort,
)
from app.ports.outbound.repository.concert_repository_outbound_port import (
    ConcertRepositoryOutboundPort,
)
from app.ports.outbound.repository.festival_repository_outbound_port import (
    FestivalRepositoryOutboundPort,
)
from app.ports.outbound.repository.stage_repository_outbound_port import (
    StageRepositoryOutboundPort,
)
from app.ports.outbound.transaction.transaction_outbound_port import (
    TransactionOutboundPort,
)

T = TypeVar("T")


def in_transaction(
    transaction: TransactionOutboundPort, operation: Callable[[], T]
) -> T:
    """Exécute ``operation`` et délègue commit/rollback au port de transaction.

    Le cas d'usage ne porte pas la transaction : il fournit le travail, le port
    valide ou annule. Les événements de domaine sont publiés **après** cet appel.
    """
    try:
        result = operation()
    except Exception:
        transaction.rollback()
        raise
    transaction.commit()
    return result


def require_festival(
    repository: FestivalRepositoryOutboundPort, festival_id: int
) -> Festival:
    entity = repository.get(festival_id)
    if entity is None:
        raise FestivalNotFoundError(festival_id)
    return entity


def require_artist(
    repository: ArtistRepositoryOutboundPort, artist_id: int
) -> Artist:
    entity = repository.get(artist_id)
    if entity is None:
        raise ArtistNotFoundError(artist_id)
    return entity


def require_stage(
    repository: StageRepositoryOutboundPort, stage_id: int
) -> Stage:
    entity = repository.get(stage_id)
    if entity is None:
        raise StageNotFoundError(stage_id)
    return entity


def require_concert(
    repository: ConcertRepositoryOutboundPort, concert_id: int
) -> Concert:
    entity = repository.get(concert_id)
    if entity is None:
        raise ConcertNotFoundError(concert_id)
    return entity
