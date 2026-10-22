from datetime import datetime
import pytest
from app.domain.time_range import TimeRange
from app.domain.exceptions import InvalidTimeRangeError

# ==========================
# Tests TimeRange
# ==========================

def test_time_range_cannot_end_before_start():
    """Vérifie qu'un TimeRange ne peut pas avoir une date de fin antérieur à sa date de début."""
    with pytest.raises(InvalidTimeRangeError):
        TimeRange(
            start=datetime(2027, 6, 18, 18, 0), # year, month, day, hour, minute
            end=datetime(2027, 6, 18, 17, 0)    # debut = 18h, fin = 17h -> Erreur
        )


def test_time_range_detects_overlaps():
    t1 = TimeRange(start=datetime(2027, 6, 18, 18, 0), end=datetime(2027, 6, 18, 19, 0))
    t2 = TimeRange(start=datetime(2027, 6, 18, 18, 30), end=datetime(2027, 6, 18, 19, 30))
    t3 = TimeRange(start=datetime(2027, 6, 18, 19, 0), end=datetime(2027, 6, 18, 20, 0))

    assert t1.overlaps_with(t2) == True
    assert t1.overlaps_with(t3) == False