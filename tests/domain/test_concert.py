from datetime import datetime
import pytest
from app.domain.concert.entities import Concert
from app.domain.concert.value_object import ConcertStatus
from app.domain.time_range import TimeRange

# ==========================
# Tests Concert
# ==========================

@pytest.fixture
def initial_time_range() -> TimeRange:
    return TimeRange(
        start=datetime(2027, 6, 18, 18, 0),
        end=datetime(2027, 6, 18, 19, 30),
    )


def test_concert_initial_state(initial_time_range: TimeRange):
    """Vérifie l'état initial d'un concert à sa création."""
    concert = Concert(
        id=1,
        festival_id=1,
        artist_id=2,
        stage_id=3,
        time_range=initial_time_range,
    )

    assert concert.status == ConcertStatus.SCHEDULED
    assert concert.is_cancelled is False
    assert concert.time_range == initial_time_range


def test_concert_reschedule(initial_time_range: TimeRange):
    """Vérifie la reprogrammation d'un concert avec un nouveau créneau."""
    concert = Concert(
        id=1,
        festival_id=1,
        artist_id=2,
        stage_id=3,
        time_range=initial_time_range,
    )

    new_time_range = TimeRange(
        start=datetime(2027, 6, 18, 20, 0),
        end=datetime(2027, 6, 18, 21, 30),
    )

    concert.reschedule(new_time_range)

    assert concert.time_range == new_time_range
    assert concert.status == ConcertStatus.SCHEDULED


def test_concert_reschedule_can_change_stage(initial_time_range: TimeRange):
    """Vérifie que la reprogrammation peut aussi changer la scène."""
    concert = Concert(
        id=1,
        festival_id=1,
        artist_id=2,
        stage_id=3,
        time_range=initial_time_range,
    )

    new_time_range = TimeRange(
        start=datetime(2027, 6, 18, 20, 0),
        end=datetime(2027, 6, 18, 21, 30),
    )

    concert.reschedule(new_time_range, new_stage_id=4)

    assert concert.time_range == new_time_range
    assert concert.stage_id == 4


def test_concert_reschedule_keeps_stage_when_not_provided(initial_time_range: TimeRange):
    """Vérifie que la scène est conservée si elle n'est pas fournie."""
    concert = Concert(
        id=1,
        festival_id=1,
        artist_id=2,
        stage_id=3,
        time_range=initial_time_range,
    )

    concert.reschedule(
        TimeRange(
            start=datetime(2027, 6, 18, 20, 0),
            end=datetime(2027, 6, 18, 21, 30),
        )
    )

    assert concert.stage_id == 3


def test_concert_cancel(initial_time_range: TimeRange):
    """Vérifie l'annulation d'un concert."""
    concert = Concert(
        id=1,
        festival_id=1,
        artist_id=2,
        stage_id=3,
        time_range=initial_time_range,
    )

    concert.cancel()

    assert concert.status == ConcertStatus.CANCELLED
    assert concert.is_cancelled is True

