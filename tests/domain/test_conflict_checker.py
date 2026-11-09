from datetime import datetime
import pytest
from app.domain.concert.entities import Concert
from app.domain.time_range import TimeRange
from app.domain.services.conflict_checker import SchedulingConflictChecker
from app.domain.exceptions import StageOccupiedError, ArtistAlreadyScheduledError

# ==========================
# Tests Conflit Checker
# ==========================

def test_conflict_on_same_stage():
    """
    Vérifie les conflits sur un même stage.
    Même stage, même horaire mais artistes différents.
    """
    existing_concerts = [
        Concert(
            id=15,
            festival_id=1,
            artist_id=7,
            stage_id=3,
            time_range=TimeRange(start=datetime(2027, 6, 18, 18, 0), end=datetime(2027, 6, 18, 19, 0))
        )
    ]
    concert_to_check = Concert(
        id=9,
        festival_id=1,
        artist_id=2,
        stage_id=3,
        time_range=TimeRange(start=datetime(2027, 6, 18, 18, 0), end=datetime(2027, 6, 18, 19, 0))
    )

    checker = SchedulingConflictChecker()

    with pytest.raises(StageOccupiedError):
        checker.check_conflicts(
            existing_concerts=existing_concerts,
            stage_id=concert_to_check.stage_id,
            artist_id=concert_to_check.artist_id,
            time_range=concert_to_check.time_range
        )


def test_conflict_on_same_artist():
    """
    Vérifie les conflits pour même artiste.
    Même artiste, même horaire, mais stages différents
    """
    existing_concerts = [
        Concert(
            id=15,
            festival_id=1,
            artist_id=7,
            stage_id=3,
            time_range=TimeRange(start=datetime(2027, 6, 18, 18, 0), end=datetime(2027, 6, 18, 19, 0))
        )
    ]
    concert_to_check = Concert(
        id=9,
        festival_id=1,
        artist_id=7,
        stage_id=4,
        time_range=TimeRange(start=datetime(2027, 6, 18, 18, 0), end=datetime(2027, 6, 18, 19, 0))
    )

    checker = SchedulingConflictChecker()

    with pytest.raises(ArtistAlreadyScheduledError):
        checker.check_conflicts(
            existing_concerts=existing_concerts,
            stage_id=concert_to_check.stage_id,
            artist_id=concert_to_check.artist_id,
            time_range=concert_to_check.time_range
        )


def test_cancelled_concert_is_ignored_for_conflicts():
    """Vérifie qu'un concert annulé ne génère pas de conflit d'horaire."""
    cancelled_concert = Concert(
        id=15,
        festival_id=1,
        artist_id=7,
        stage_id=3,
        time_range=TimeRange(start=datetime(2027, 6, 18, 18, 0), end=datetime(2027, 6, 18, 19, 0)),
    )
    cancelled_concert.cancel()

    checker = SchedulingConflictChecker()

    # Même scène et même heure, mais le premier concert est annulé -> pas d'erreur levée
    checker.check_conflicts(
        existing_concerts=[cancelled_concert],
        stage_id=3,
        artist_id=99,
        time_range=TimeRange(start=datetime(2027, 6, 18, 18, 0), end=datetime(2027, 6, 18, 19, 0)),
    )


def test_no_conflict_when_different_stages_and_artists():
    """Vérifie qu'aucune erreur n'est levée si les scènes et artistes sont distincts."""
    existing_concert = Concert(
        id=1,
        festival_id=1,
        artist_id=1,
        stage_id=1,
        time_range=TimeRange(start=datetime(2027, 6, 18, 18, 0), end=datetime(2027, 6, 18, 19, 0)),
    )

    checker = SchedulingConflictChecker()
    checker.check_conflicts(
        existing_concerts=[existing_concert],
        stage_id=2,
        artist_id=2,
        time_range=TimeRange(start=datetime(2027, 6, 18, 18, 0), end=datetime(2027, 6, 18, 19, 0)),
    )

