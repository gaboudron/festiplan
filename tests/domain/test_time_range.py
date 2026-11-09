from datetime import datetime
import pytest
from app.domain.time_range import TimeRange
from app.domain.exceptions import InvalidTimeRangeError

# ==========================
# Tests TimeRange
# ==========================

def test_time_range_cannot_end_before_or_at_start():
    """Vérifie qu'un TimeRange ne peut pas avoir une date de fin antérieure ou égale à sa date de début."""
    with pytest.raises(InvalidTimeRangeError):
        TimeRange(
            start=datetime(2027, 6, 18, 18, 0), # year, month, day, hour, minute
            end=datetime(2027, 6, 18, 17, 0)    # debut = 18h, fin = 17h -> Erreur
        )

    with pytest.raises(InvalidTimeRangeError):
        TimeRange(
            start=datetime(2027, 6, 18, 18, 0),
            end=datetime(2027, 6, 18, 18, 0),
        )


def test_time_range_detects_overlaps():
    t1 = TimeRange(start=datetime(2027, 6, 18, 18, 0), end=datetime(2027, 6, 18, 19, 0))
    t2 = TimeRange(start=datetime(2027, 6, 18, 18, 30), end=datetime(2027, 6, 18, 19, 30))
    t3 = TimeRange(start=datetime(2027, 6, 18, 19, 0), end=datetime(2027, 6, 18, 20, 0))

    assert t1.overlaps_with(t2) is True
    assert t1.overlaps_with(t3) is False


def test_time_range_is_within_boundary():
    """Vérifie que is_within valide l'inclusion complète dans une plage parente."""
    boundary = TimeRange(start=datetime(2027, 6, 18, 10, 0), end=datetime(2027, 6, 18, 22, 0))

    inside = TimeRange(start=datetime(2027, 6, 18, 14, 0), end=datetime(2027, 6, 18, 16, 0))
    exact = TimeRange(start=datetime(2027, 6, 18, 10, 0), end=datetime(2027, 6, 18, 22, 0))
    starts_before = TimeRange(start=datetime(2027, 6, 18, 9, 0), end=datetime(2027, 6, 18, 12, 0))
    ends_after = TimeRange(start=datetime(2027, 6, 18, 20, 0), end=datetime(2027, 6, 18, 23, 0))

    assert inside.is_within(boundary) is True
    assert exact.is_within(boundary) is True
    assert starts_before.is_within(boundary) is False
    assert ends_after.is_within(boundary) is False