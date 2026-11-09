"""Service applicatif pour les concerts."""

from app.domain.artist.entities import Artist
from app.domain.concert.entities import Concert
from app.domain.concert.events import (
    ConcertCancelledEvent,
    ConcertRescheduledEvent,
)
from app.domain.festival.entities import Festival, Stage
from app.domain.services.conflict_checker import SchedulingConflictChecker
from app.domain.services.equipment_checker import EquipmentChecker
from app.domain.services.festival_policy import FestivalPolicy
from app.domain.time_range import TimeRange
from app.ports.inbound.concert_inbound_port import ConcertInboundPort
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
from app.ports.outbound.repository.stage_repository_outbound_port import (
    StageRepositoryOutboundPort,
)
from app.ports.outbound.transaction.transaction_outbound_port import (
    TransactionOutboundPort,
)
from app.use_cases._support import (
    in_transaction,
    require_artist,
    require_concert,
    require_festival,
    require_stage,
)


class ConcertService(ConcertInboundPort):
    """Implémente ``ConcertInboundPort``.

    Orchestre les entités, ``SchedulingConflictChecker``, ``EquipmentChecker``,
    ``FestivalPolicy`` et les ports sortants. La transaction est déléguée au
    port de transaction ; les événements sont publiés après le commit.
    """

    def __init__(
        self,
        concerts: ConcertRepositoryOutboundPort,
        festivals: FestivalRepositoryOutboundPort,
        artists: ArtistRepositoryOutboundPort,
        stages: StageRepositoryOutboundPort,
        transaction: TransactionOutboundPort,
        event_bus: DomainEventBusOutboundPort,
    ) -> None:
        self._concerts = concerts
        self._festivals = festivals
        self._artists = artists
        self._stages = stages
        self._transaction = transaction
        self._event_bus = event_bus

    # ------------------------------------------------------------------
    # Lectures
    # ------------------------------------------------------------------

    def list_concerts(self, festival_id: int) -> list[Concert]:
        return [
            concert
            for concert in self._concerts.list_by_festival_id(festival_id)
            if not concert.is_cancelled
        ]

    def get_concert(self, concert_id: int) -> Concert:
        return require_concert(self._concerts, concert_id)

    def get_schedule(self, festival_id: int) -> list[Concert]:
        return self._concerts.list_by_festival_id(festival_id)

    # ------------------------------------------------------------------
    # Écritures
    # ------------------------------------------------------------------

    def create_concert(self, concert: Concert) -> Concert:
        festival = require_festival(self._festivals, concert.festival_id)
        artist = require_artist(self._artists, concert.artist_id)
        stage = require_stage(self._stages, concert.stage_id)

        self._validate(
            festival=festival,
            festival_id=concert.festival_id,
            artist=artist,
            stage=stage,
            time_range=concert.time_range,
            stage_id=concert.stage_id,
            artist_id=concert.artist_id,
        )

        return in_transaction(
            self._transaction, lambda: self._concerts.save(concert)
        )

    def reschedule_concert(
        self,
        concert_id: int,
        new_time_range: TimeRange,
        new_stage_id: int | None = None,
    ) -> Concert:
        concert = require_concert(self._concerts, concert_id)
        festival = require_festival(self._festivals, concert.festival_id)
        stage_id = new_stage_id if new_stage_id is not None else concert.stage_id
        artist = require_artist(self._artists, concert.artist_id)
        stage = require_stage(self._stages, stage_id)

        self._validate(
            festival=festival,
            festival_id=concert.festival_id,
            artist=artist,
            stage=stage,
            time_range=new_time_range,
            stage_id=stage_id,
            artist_id=concert.artist_id,
            exclude_concert_id=concert.id,
        )

        # ``None`` conserve la scène actuelle ; un identifiant la change.
        concert.reschedule(new_time_range, new_stage_id=new_stage_id)
        saved = in_transaction(
            self._transaction, lambda: self._concerts.save(concert)
        )
        self._event_bus.publish(
            ConcertRescheduledEvent(
                concert_id=saved.id if saved.id is not None else concert_id,
                festival_id=concert.festival_id,
                new_time_range=new_time_range,
            )
        )
        return saved

    def cancel_concert(self, concert_id: int) -> Concert:
        concert = require_concert(self._concerts, concert_id)
        festival = require_festival(self._festivals, concert.festival_id)
        FestivalPolicy.ensure_not_published(festival)

        concert.cancel()
        saved = in_transaction(
            self._transaction, lambda: self._concerts.save(concert)
        )
        self._event_bus.publish(
            ConcertCancelledEvent(
                concert_id=saved.id if saved.id is not None else concert_id,
                festival_id=concert.festival_id,
            )
        )
        return saved

    # ------------------------------------------------------------------
    # Validation partagée création / reprogrammation
    # ------------------------------------------------------------------

    def _validate(
        self,
        *,
        festival: Festival,
        festival_id: int,
        artist: Artist,
        stage: Stage,
        time_range: TimeRange,
        stage_id: int,
        artist_id: int,
        exclude_concert_id: int | None = None,
    ) -> None:
        FestivalPolicy.ensure_not_published(festival)
        FestivalPolicy.ensure_concert_within_dates(festival, time_range)
        FestivalPolicy.ensure_stage_belongs_to_festival(festival, stage)
        EquipmentChecker.check(artist, stage)
        SchedulingConflictChecker.check_conflicts(
            existing_concerts=self._concerts.list_by_festival_id(festival_id),
            stage_id=stage_id,
            artist_id=artist_id,
            time_range=time_range,
            exclude_concert_id=exclude_concert_id,
        )
