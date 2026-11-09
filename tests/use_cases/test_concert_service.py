"""Tests unitaires de ``ConcertService``."""

from datetime import datetime, timezone

import pytest

from app.domain.concert.events import (
    ConcertCancelledEvent,
    ConcertRescheduledEvent,
)
from app.domain.concert.value_object import ConcertStatus
from app.domain.exceptions import (
    ArtistAlreadyScheduledError,
    ArtistNotFoundError,
    ConcertNotFoundError,
    ConcertOutsideFestivalDatesError,
    EquipmentMismatchError,
    FestivalAlreadyPublishedError,
    FestivalNotFoundError,
    StageDoesNotBelongToFestivalError,
    StageNotFoundError,
    StageOccupiedError,
)
from app.domain.festival.value_objects import FestivalStatus
from app.domain.time_range import TimeRange
from factories import make_artist, make_concert, make_festival, make_stage


def _wire(
    *,
    festival_repository,
    artist_repository,
    stage_repository,
    concert_repository,
    festival,
    artist,
    stage,
    existing=None,
):
    """Configure les doublures pour un scénario nominal de validation."""
    festival_repository.get.return_value = festival
    artist_repository.get.return_value = artist
    stage_repository.get.return_value = stage
    concert_repository.list_by_festival_id.return_value = (
        existing if existing is not None else []
    )
    concert_repository.save.side_effect = lambda entity: entity


def _outside_festival_range() -> TimeRange:
    return TimeRange(
        start=datetime(2027, 6, 17, 18, 0, tzinfo=timezone.utc),
        end=datetime(2027, 6, 17, 19, 0, tzinfo=timezone.utc),
    )


# ---------------------------------------------------------------------------
# Lectures
# ---------------------------------------------------------------------------


def test_list_concerts_excludes_cancelled(
    concert_service, concert_repository, concert
):
    cancelled = make_concert(id=2, status=ConcertStatus.CANCELLED)
    concert_repository.list_by_festival_id.return_value = [concert, cancelled]

    assert concert_service.list_concerts(concert.festival_id) == [concert]


def test_get_schedule_returns_all_concerts(
    concert_service, concert_repository, concert
):
    cancelled = make_concert(id=2, status=ConcertStatus.CANCELLED)
    concert_repository.list_by_festival_id.return_value = [concert, cancelled]

    assert concert_service.get_schedule(concert.festival_id) == [
        concert,
        cancelled,
    ]


def test_get_concert_requires_existing_concert(
    concert_service, concert_repository
):
    concert_repository.get.return_value = None

    with pytest.raises(ConcertNotFoundError):
        concert_service.get_concert(99)


# ---------------------------------------------------------------------------
# Création
# ---------------------------------------------------------------------------


def test_create_concert_validates_and_saves(
    concert_service, concert_repository, festival_repository,
    artist_repository, stage_repository, transaction,
    festival, artist, stage, concert,
):
    _wire(
        festival_repository=festival_repository,
        artist_repository=artist_repository,
        stage_repository=stage_repository,
        concert_repository=concert_repository,
        festival=festival,
        artist=artist,
        stage=stage,
    )

    result = concert_service.create_concert(concert)

    assert result is concert
    concert_repository.save.assert_called_once_with(concert)
    transaction.commit.assert_called_once_with()


def test_create_concert_requires_existing_festival(
    concert_service, concert_repository, festival_repository,
    artist_repository, stage_repository, transaction,
    artist, stage, concert,
):
    festival_repository.get.return_value = None
    artist_repository.get.return_value = artist
    stage_repository.get.return_value = stage

    with pytest.raises(FestivalNotFoundError):
        concert_service.create_concert(concert)

    concert_repository.save.assert_not_called()
    transaction.commit.assert_not_called()


def test_create_concert_requires_existing_artist(
    concert_service, concert_repository, festival_repository,
    artist_repository, stage_repository, festival, stage, concert,
):
    festival_repository.get.return_value = festival
    artist_repository.get.return_value = None
    stage_repository.get.return_value = stage

    with pytest.raises(ArtistNotFoundError):
        concert_service.create_concert(concert)


def test_create_concert_requires_existing_stage(
    concert_service, festival_repository, artist_repository,
    stage_repository, festival, artist, concert,
):
    festival_repository.get.return_value = festival
    artist_repository.get.return_value = artist
    stage_repository.get.return_value = None

    with pytest.raises(StageNotFoundError):
        concert_service.create_concert(concert)


def test_create_concert_rejects_published_festival(
    concert_service, concert_repository, festival_repository,
    artist_repository, stage_repository, artist, stage, concert,
):
    published = make_festival(status=FestivalStatus.PUBLISHED)
    _wire(
        festival_repository=festival_repository,
        artist_repository=artist_repository,
        stage_repository=stage_repository,
        concert_repository=concert_repository,
        festival=published,
        artist=artist,
        stage=stage,
    )

    with pytest.raises(FestivalAlreadyPublishedError):
        concert_service.create_concert(concert)


def test_create_concert_rejects_concert_outside_festival_dates(
    concert_service, concert_repository, festival_repository,
    artist_repository, stage_repository, festival, artist, stage,
):
    _wire(
        festival_repository=festival_repository,
        artist_repository=artist_repository,
        stage_repository=stage_repository,
        concert_repository=concert_repository,
        festival=festival,
        artist=artist,
        stage=stage,
    )
    out_of_range = make_concert(time_range=_outside_festival_range())

    with pytest.raises(ConcertOutsideFestivalDatesError):
        concert_service.create_concert(out_of_range)


def test_create_concert_rejects_stage_from_another_festival(
    concert_service, concert_repository, festival_repository,
    artist_repository, stage_repository, festival, artist, concert,
):
    other_stage = make_stage(festival_id=999)
    _wire(
        festival_repository=festival_repository,
        artist_repository=artist_repository,
        stage_repository=stage_repository,
        concert_repository=concert_repository,
        festival=festival,
        artist=artist,
        stage=other_stage,
    )

    with pytest.raises(StageDoesNotBelongToFestivalError):
        concert_service.create_concert(concert)


def test_create_concert_rejects_missing_equipment(
    concert_service, concert_repository, festival_repository,
    artist_repository, stage_repository, festival, stage, concert,
):
    demanding_artist = make_artist(required_equipment=["pyro"])
    _wire(
        festival_repository=festival_repository,
        artist_repository=artist_repository,
        stage_repository=stage_repository,
        concert_repository=concert_repository,
        festival=festival,
        artist=demanding_artist,
        stage=stage,
    )

    with pytest.raises(EquipmentMismatchError):
        concert_service.create_concert(concert)


def test_create_concert_rejects_occupied_stage(
    concert_service, concert_repository, festival_repository,
    artist_repository, stage_repository, festival, artist, stage,
    concert, concert_time_range,
):
    overlapping = make_concert(
        id=2, stage_id=stage.id, time_range=concert_time_range
    )
    _wire(
        festival_repository=festival_repository,
        artist_repository=artist_repository,
        stage_repository=stage_repository,
        concert_repository=concert_repository,
        festival=festival,
        artist=artist,
        stage=stage,
        existing=[overlapping],
    )

    with pytest.raises(StageOccupiedError):
        concert_service.create_concert(concert)


def test_create_concert_rejects_artist_already_scheduled(
    concert_service, concert_repository, festival_repository,
    artist_repository, stage_repository, festival, artist, stage,
    concert, concert_time_range,
):
    overlapping = make_concert(
        id=2, stage_id=999, artist_id=artist.id,
        time_range=concert_time_range,
    )
    _wire(
        festival_repository=festival_repository,
        artist_repository=artist_repository,
        stage_repository=stage_repository,
        concert_repository=concert_repository,
        festival=festival,
        artist=artist,
        stage=stage,
        existing=[overlapping],
    )

    with pytest.raises(ArtistAlreadyScheduledError):
        concert_service.create_concert(concert)


# ---------------------------------------------------------------------------
# Reprogrammation
# ---------------------------------------------------------------------------


def test_reschedule_changes_time_and_stage(
    concert_service, concert_repository, festival_repository,
    artist_repository, stage_repository, transaction, event_bus,
    festival, artist, stage, concert, concert_time_range,
):
    concert_repository.get.return_value = concert
    _wire(
        festival_repository=festival_repository,
        artist_repository=artist_repository,
        stage_repository=stage_repository,
        concert_repository=concert_repository,
        festival=festival,
        artist=artist,
        stage=stage,
    )
    new_range = TimeRange(
        start=datetime(2027, 6, 19, 18, 0, tzinfo=timezone.utc),
        end=datetime(2027, 6, 19, 19, 30, tzinfo=timezone.utc),
    )

    result = concert_service.reschedule_concert(
        concert.id, new_range, new_stage_id=42
    )

    assert result.stage_id == 42
    assert result.time_range == new_range
    transaction.commit.assert_called_once_with()
    event = event_bus.publish.call_args.args[0]
    assert isinstance(event, ConcertRescheduledEvent)
    assert event.new_time_range == new_range


def test_reschedule_without_stage_keeps_current_stage(
    concert_service, concert_repository, festival_repository,
    artist_repository, stage_repository, event_bus,
    festival, artist, stage, concert, concert_time_range,
):
    concert_repository.get.return_value = concert
    _wire(
        festival_repository=festival_repository,
        artist_repository=artist_repository,
        stage_repository=stage_repository,
        concert_repository=concert_repository,
        festival=festival,
        artist=artist,
        stage=stage,
    )
    new_range = TimeRange(
        start=datetime(2027, 6, 19, 18, 0, tzinfo=timezone.utc),
        end=datetime(2027, 6, 19, 19, 30, tzinfo=timezone.utc),
    )

    result = concert_service.reschedule_concert(concert.id, new_range)

    assert result.stage_id == stage.id
    assert isinstance(
        event_bus.publish.call_args.args[0], ConcertRescheduledEvent
    )


def test_reschedule_excludes_itself_from_conflict_check(
    concert_service, concert_repository, festival_repository,
    artist_repository, stage_repository, festival, artist, stage,
    concert, concert_time_range,
):
    concert_repository.get.return_value = concert
    _wire(
        festival_repository=festival_repository,
        artist_repository=artist_repository,
        stage_repository=stage_repository,
        concert_repository=concert_repository,
        festival=festival,
        artist=artist,
        stage=stage,
        existing=[concert],
    )
    new_range = TimeRange(
        start=datetime(2027, 6, 19, 18, 0, tzinfo=timezone.utc),
        end=datetime(2027, 6, 19, 19, 30, tzinfo=timezone.utc),
    )

    result = concert_service.reschedule_concert(concert.id, new_range)

    assert result.time_range == new_range


def test_reschedule_requires_existing_concert(
    concert_service, concert_repository, event_bus, concert_time_range
):
    concert_repository.get.return_value = None

    with pytest.raises(ConcertNotFoundError):
        concert_service.reschedule_concert(99, concert_time_range)

    event_bus.publish.assert_not_called()


def test_reschedule_rejects_published_festival(
    concert_service, concert_repository, festival_repository,
    artist_repository, stage_repository, artist, stage, concert,
    concert_time_range,
):
    concert_repository.get.return_value = concert
    published = make_festival(status=FestivalStatus.PUBLISHED)
    _wire(
        festival_repository=festival_repository,
        artist_repository=artist_repository,
        stage_repository=stage_repository,
        concert_repository=concert_repository,
        festival=published,
        artist=artist,
        stage=stage,
    )

    with pytest.raises(FestivalAlreadyPublishedError):
        concert_service.reschedule_concert(concert.id, concert_time_range)


def test_reschedule_publishes_event_after_commit(
    concert_service, concert_repository, festival_repository,
    artist_repository, stage_repository, transaction, event_bus,
    festival, artist, stage, concert, concert_time_range,
):
    concert_repository.get.return_value = concert
    _wire(
        festival_repository=festival_repository,
        artist_repository=artist_repository,
        stage_repository=stage_repository,
        concert_repository=concert_repository,
        festival=festival,
        artist=artist,
        stage=stage,
    )

    def assert_event_not_yet_published():
        assert event_bus.publish.call_count == 0

    transaction.commit.side_effect = assert_event_not_yet_published

    concert_service.reschedule_concert(concert.id, concert_time_range)

    transaction.commit.assert_called_once_with()
    event_bus.publish.assert_called_once()


# ---------------------------------------------------------------------------
# Annulation et transaction
# ---------------------------------------------------------------------------


def test_cancel_concert_cancels_and_publishes_event(
    concert_service, concert_repository, festival_repository,
    transaction, event_bus, festival, concert,
):
    concert_repository.get.return_value = concert
    concert_repository.save.side_effect = lambda entity: entity
    festival_repository.get.return_value = festival

    result = concert_service.cancel_concert(concert.id)

    assert result.is_cancelled is True
    transaction.commit.assert_called_once_with()
    event = event_bus.publish.call_args.args[0]
    assert isinstance(event, ConcertCancelledEvent)
    assert event.concert_id == concert.id


def test_cancel_concert_requires_existing_concert(
    concert_service, concert_repository, event_bus
):
    concert_repository.get.return_value = None

    with pytest.raises(ConcertNotFoundError):
        concert_service.cancel_concert(99)

    event_bus.publish.assert_not_called()


def test_repository_failure_rolls_back_without_event(
    concert_service, concert_repository, festival_repository,
    artist_repository, stage_repository, transaction, event_bus,
    festival, artist, stage, concert,
):
    _wire(
        festival_repository=festival_repository,
        artist_repository=artist_repository,
        stage_repository=stage_repository,
        concert_repository=concert_repository,
        festival=festival,
        artist=artist,
        stage=stage,
    )
    concert_repository.save.side_effect = RuntimeError("base indisponible")

    with pytest.raises(RuntimeError, match="base indisponible"):
        concert_service.create_concert(concert)

    transaction.rollback.assert_called_once_with()
    transaction.commit.assert_not_called()
    event_bus.publish.assert_not_called()
