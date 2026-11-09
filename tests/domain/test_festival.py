from datetime import datetime
import pytest
from app.domain.festival.entities import Festival, Stage
from app.domain.festival.value_objects import FestivalStatus
from app.domain.time_range import TimeRange
from app.domain.equipments import EquipmentSet

# ==========================
# Tests Festival & Stage
# ==========================

@pytest.fixture
def festival_time_range() -> TimeRange:
    return TimeRange(
        start=datetime(2027, 6, 18, 14, 0),
        end=datetime(2027, 6, 20, 23, 0),
    )


def test_festival_default_state(festival_time_range: TimeRange):
    """Vérifie l'état initial par défaut d'un festival."""
    festival = Festival(
        id=1,
        name="Hellfest 2027",
        location="Clisson",
        time_range=festival_time_range,
    )

    assert festival.status == FestivalStatus.PREPARATION
    assert festival.is_published is False
    assert festival.stages == []


def test_festival_publish(festival_time_range: TimeRange):
    """Vérifie la publication du festival."""
    festival = Festival(
        id=1,
        name="Hellfest 2027",
        location="Clisson",
        time_range=festival_time_range,
    )

    festival.publish()

    assert festival.status == FestivalStatus.PUBLISHED
    assert festival.is_published is True


def test_festival_cancel(festival_time_range: TimeRange):
    """Vérifie l'annulation d'un festival."""
    festival = Festival(
        id=1,
        name="Hellfest 2027",
        location="Clisson",
        time_range=festival_time_range,
    )

    festival.cancel()

    assert festival.status == FestivalStatus.CANCELLED
    assert festival.is_cancelled is True



def test_festival_contains_time_range(festival_time_range: TimeRange):
    """Vérifie si un créneau est inclus ou non dans les dates du festival."""
    festival = Festival(
        id=1,
        name="Hellfest 2027",
        location="Clisson",
        time_range=festival_time_range,
    )

    # Créneau entièrement inclus dans le festival
    valid_range = TimeRange(
        start=datetime(2027, 6, 18, 18, 0),
        end=datetime(2027, 6, 18, 20, 0),
    )
    assert festival.contains_time_range(valid_range) is True

    # Créneau démarrant avant le début du festival
    range_starts_before = TimeRange(
        start=datetime(2027, 6, 18, 10, 0),
        end=datetime(2027, 6, 18, 16, 0),
    )
    assert festival.contains_time_range(range_starts_before) is False

    # Créneau se terminant après la fin du festival
    range_ends_after = TimeRange(
        start=datetime(2027, 6, 20, 20, 0),
        end=datetime(2027, 6, 21, 2, 0),
    )
    assert festival.contains_time_range(range_ends_after) is False


def test_stage_creation():
    """Vérifie la création d'une scène avec ses équipements."""
    equipments = EquipmentSet.from_list(["sound_system", "lights"])
    stage = Stage(
        id=1,
        festival_id=1,
        name="Mainstage 01",
        capacity=50000,
        available_equipment=equipments,
    )

    assert stage.name == "Mainstage 01"
    assert stage.capacity == 50000
    assert "lights" in stage.available_equipment.items
