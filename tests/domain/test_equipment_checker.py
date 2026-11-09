import pytest

from app.domain.artist.entities import Artist
from app.domain.equipments import EquipmentSet
from app.domain.exceptions import EquipmentMismatchError
from app.domain.festival.entities import Stage
from app.domain.services.equipment_checker import EquipmentChecker


def _artist(required: list[str]) -> Artist:
    return Artist(
        id=1,
        name="Iron Vow",
        genre="Heavy metal",
        required_equipment=EquipmentSet.from_list(required),
    )


def _stage(available: list[str]) -> Stage:
    return Stage(
        id=1,
        festival_id=1,
        name="Mainstage",
        capacity=50000,
        available_equipment=EquipmentSet.from_list(available),
    )


def test_equipment_checker_accepts_compatible_stage():
    EquipmentChecker.check(
        artist=_artist(["large_rigging", "special_lighting"]),
        stage=_stage(["large_rigging", "special_lighting", "pyrotechnics"]),
    )


def test_equipment_checker_rejects_missing_equipment():
    with pytest.raises(EquipmentMismatchError):
        EquipmentChecker.check(
            artist=_artist(["large_rigging", "pyrotechnics"]),
            stage=_stage(["large_rigging", "special_lighting"]),
        )
