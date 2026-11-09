"""Tests unitaires de ``FestivalPolicy`` (règles d'état du domaine)."""

from datetime import datetime, timezone

import pytest

from app.domain.equipments import EquipmentSet
from app.domain.exceptions import (
    ConcertOutsideFestivalDatesError,
    FestivalAlreadyPublishedError,
    StageDoesNotBelongToFestivalError,
)
from app.domain.festival.entities import Festival, Stage
from app.domain.festival.value_objects import FestivalStatus
from app.domain.services.festival_policy import FestivalPolicy
from app.domain.time_range import TimeRange

FESTIVAL_RANGE = TimeRange(
    start=datetime(2027, 6, 18, 10, 0, tzinfo=timezone.utc),
    end=datetime(2027, 6, 20, 23, 0, tzinfo=timezone.utc),
)


def _festival(status=FestivalStatus.PREPARATION) -> Festival:
    return Festival(
        id=1,
        name="Hellforge Open Air",
        location="Clisson",
        time_range=FESTIVAL_RANGE,
        status=status,
    )


def _stage(festival_id: int = 1) -> Stage:
    return Stage(
        id=1,
        festival_id=festival_id,
        name="Mainstage",
        capacity=50_000,
        available_equipment=EquipmentSet.from_list(["large_rigging"]),
    )


def test_ensure_not_published_accepts_preparation():
    FestivalPolicy.ensure_not_published(_festival())


def test_ensure_not_published_rejects_published():
    with pytest.raises(FestivalAlreadyPublishedError):
        FestivalPolicy.ensure_not_published(
            _festival(status=FestivalStatus.PUBLISHED)
        )


def test_ensure_concert_within_dates_accepts_included_range():
    concert_range = TimeRange(
        start=datetime(2027, 6, 18, 18, 0, tzinfo=timezone.utc),
        end=datetime(2027, 6, 18, 19, 30, tzinfo=timezone.utc),
    )
    FestivalPolicy.ensure_concert_within_dates(_festival(), concert_range)


def test_ensure_concert_within_dates_rejects_outside_range():
    outside = TimeRange(
        start=datetime(2027, 6, 17, 18, 0, tzinfo=timezone.utc),
        end=datetime(2027, 6, 17, 19, 0, tzinfo=timezone.utc),
    )
    with pytest.raises(ConcertOutsideFestivalDatesError):
        FestivalPolicy.ensure_concert_within_dates(_festival(), outside)


def test_ensure_stage_belongs_accepts_matching_festival():
    FestivalPolicy.ensure_stage_belongs_to_festival(_festival(), _stage())


def test_ensure_stage_belongs_rejects_other_festival():
    with pytest.raises(StageDoesNotBelongToFestivalError):
        FestivalPolicy.ensure_stage_belongs_to_festival(
            _festival(), _stage(festival_id=999)
        )
