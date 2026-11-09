from datetime import datetime, timezone
from types import SimpleNamespace

import pytest

from app.adapters.inbound.api.dtos import (
    ArtistCreateRequest,
    ConcertCreateRequest,
    ConcertRescheduleRequest,
    FestivalCreateRequest,
    IncidentCreateRequest,
    StageCreateRequest,
)
from app.adapters.inbound.api.mappers import (
    artist_create_to_domain,
    artist_to_response,
    concert_create_to_domain,
    concert_reschedule_to_domain,
    concert_reschedule_to_time_range,
    concert_to_response,
    festival_create_to_domain,
    festival_to_response,
    incident_create_to_domain,
    incident_to_response,
    stage_create_to_domain,
    stage_to_response,
)
from app.domain.artist.entities import Artist
from app.domain.concert.value_object import ConcertStatus
from app.domain.equipments import EquipmentSet
from app.domain.exceptions import InvalidIncidentMessageError, InvalidTimeRangeError
from app.domain.festival.value_objects import FestivalStatus
from app.domain.time_range import TimeRange


START = datetime(2027, 6, 18, 18, 0)
END = datetime(2027, 6, 18, 19, 30)


# ---------------------------------------------------------------------------
# Artist
# ---------------------------------------------------------------------------

def test_artist_mapping_round_trip():
    dto = ArtistCreateRequest(
        name="Iron Vow",
        genre="Heavy metal",
        required_equipment=[" large_rigging ", "special_lighting", ""],
    )

    artist = artist_create_to_domain(dto)

    assert artist.id is None
    assert artist.name == "Iron Vow"
    assert artist.required_equipment == EquipmentSet.from_list(
        ["large_rigging", "special_lighting"]
    )

    artist.id = 7
    response = artist_to_response(artist)

    assert response.id == 7
    assert response.required_equipment == ["large_rigging", "special_lighting"]


def test_artist_to_response_requires_persisted_entity():
    artist = Artist(
        id=None,
        name="Iron Vow",
        genre="Heavy metal",
        required_equipment=EquipmentSet.from_list([]),
    )

    with pytest.raises(ValueError):
        artist_to_response(artist)


def test_artist_to_response_accepts_orm_row():
    row = SimpleNamespace(
        id=7,
        name="Iron Vow",
        genre="Heavy metal",
        required_equipment="large_rigging,special_lighting",
    )

    response = artist_to_response(row)

    assert response.required_equipment == ["large_rigging", "special_lighting"]


# ---------------------------------------------------------------------------
# Stage
# ---------------------------------------------------------------------------

def test_stage_mapping_round_trip():
    dto = StageCreateRequest(
        festival_id=1,
        name="Mainstage",
        capacity=50000,
        available_equipment=["large_rigging", "special_lighting"],
    )

    stage = stage_create_to_domain(dto)

    assert stage.id is None
    assert stage.festival_id == 1
    assert stage.available_equipment == EquipmentSet.from_list(
        ["large_rigging", "special_lighting"]
    )

    stage.id = 3
    response = stage_to_response(stage)

    assert response.id == 3
    assert response.capacity == 50000
    assert response.available_equipment == ["large_rigging", "special_lighting"]


def test_stage_to_response_accepts_orm_row():
    row = SimpleNamespace(
        id=3,
        festival_id=1,
        name="Mainstage",
        capacity=50000,
        available_equipment="large_rigging,special_lighting",
    )

    response = stage_to_response(row)

    assert response.available_equipment == ["large_rigging", "special_lighting"]


# ---------------------------------------------------------------------------
# Festival
# ---------------------------------------------------------------------------

def test_festival_mapping_round_trip():
    dto = FestivalCreateRequest(
        name="Hellforge Open Air",
        location="Clisson-sur-Rivière",
        start_date=datetime(2027, 6, 18, 10, 0),
        end_date=datetime(2027, 6, 20, 23, 59),
    )

    festival = festival_create_to_domain(dto)

    assert festival.id is None
    assert festival.status == FestivalStatus.PREPARATION
    assert festival.time_range == TimeRange(dto.start_date, dto.end_date)

    festival.id = 1
    festival.publish()
    response = festival_to_response(festival)

    assert response.id == 1
    assert response.start_date == dto.start_date
    assert response.end_date == dto.end_date
    assert response.status == "published"


def test_festival_mapping_rejects_invalid_time_range():
    dto = FestivalCreateRequest(
        name="Hellforge Open Air",
        location="Clisson-sur-Rivière",
        start_date=END,
        end_date=START,
    )

    with pytest.raises(InvalidTimeRangeError):
        festival_create_to_domain(dto)


def test_festival_to_response_accepts_orm_row():
    row = SimpleNamespace(
        id=1,
        name="Hellforge Open Air",
        location="Clisson-sur-Rivière",
        start_date=START,
        end_date=END,
        status="preparation",
    )

    response = festival_to_response(row)

    assert response.start_date == START.replace(tzinfo=timezone.utc)
    assert response.end_date == END.replace(tzinfo=timezone.utc)
    assert response.status == "preparation"


# ---------------------------------------------------------------------------
# Concert
# ---------------------------------------------------------------------------

def test_concert_create_mapping():
    dto = ConcertCreateRequest(
        festival_id=1,
        artist_id=2,
        stage_id=3,
        start_time=START,
        end_time=END,
    )

    concert = concert_create_to_domain(dto)

    assert concert.id is None
    assert concert.festival_id == 1
    assert concert.artist_id == 2
    assert concert.stage_id == 3
    assert concert.time_range == TimeRange(START, END)
    assert concert.status == ConcertStatus.SCHEDULED


def test_concert_mapping_to_response_includes_status():
    concert = concert_create_to_domain(
        ConcertCreateRequest(
            festival_id=1,
            artist_id=2,
            stage_id=3,
            start_time=START,
            end_time=END,
        )
    )
    concert.id = 9

    response = concert_to_response(concert)

    assert response.status == "scheduled"
    assert response.start_time == START.replace(tzinfo=timezone.utc)
    assert response.end_time == END.replace(tzinfo=timezone.utc)


def test_concert_to_response_accepts_orm_row():
    row = SimpleNamespace(
        id=9,
        festival_id=1,
        artist_id=2,
        stage_id=3,
        start_time=START,
        end_time=END,
        status="scheduled",
    )

    response = concert_to_response(row)

    assert response.start_time == START.replace(tzinfo=timezone.utc)
    assert response.end_time == END.replace(tzinfo=timezone.utc)
    assert response.status == "scheduled"


def test_concert_reschedule_mapping_builds_time_range():
    dto = ConcertRescheduleRequest(stage_id=99, start_time=START, end_time=END)

    time_range = concert_reschedule_to_time_range(dto)

    assert time_range == TimeRange(START, END)


def test_concert_reschedule_mapping_rejects_invalid_range():
    dto = ConcertRescheduleRequest(stage_id=3, start_time=END, end_time=START)

    with pytest.raises(InvalidTimeRangeError):
        concert_reschedule_to_time_range(dto)


def test_concert_reschedule_to_domain_updates_stage_and_time():
    concert = concert_create_to_domain(
        ConcertCreateRequest(
            festival_id=1,
            artist_id=2,
            stage_id=3,
            start_time=START,
            end_time=END,
        )
    )
    concert.id = 9
    dto = ConcertRescheduleRequest(stage_id=42, start_time=START, end_time=END)

    updated = concert_reschedule_to_domain(concert, dto)

    assert updated.stage_id == 42
    assert updated.time_range == TimeRange(START, END)


def test_concert_reschedule_stage_is_optional():
    dto = ConcertRescheduleRequest(start_time=START, end_time=END)

    assert dto.stage_id is None


def test_concert_reschedule_to_domain_keeps_stage_when_not_provided():
    concert = concert_create_to_domain(
        ConcertCreateRequest(
            festival_id=1,
            artist_id=2,
            stage_id=3,
            start_time=START,
            end_time=END,
        )
    )
    concert.id = 9
    dto = ConcertRescheduleRequest(start_time=START, end_time=END)

    updated = concert_reschedule_to_domain(concert, dto)

    assert updated.stage_id == 3
    assert updated.time_range == TimeRange(START, END)


# ---------------------------------------------------------------------------
# Incident
# ---------------------------------------------------------------------------

def test_incident_mapping_uses_domain_default_date():
    dto = IncidentCreateRequest(concert_id=1, description="Retour de son")

    incident = incident_create_to_domain(dto)

    assert incident.id is None
    assert incident.occurred_at is not None
    assert incident.resolved is False

    incident.id = 5
    response = incident_to_response(incident)

    assert response.id == 5
    assert response.concert_id == 1
    assert response.description == "Retour de son"
    assert response.resolved is False


def test_incident_mapping_keeps_explicit_date():
    occurred_at = datetime(2027, 6, 18, 20, 0)
    dto = IncidentCreateRequest(
        concert_id=1,
        description="Retour de son",
        occurred_at=occurred_at,
    )

    incident = incident_create_to_domain(dto)

    assert incident.occurred_at == occurred_at.replace(tzinfo=timezone.utc)


def test_incident_to_response_accepts_orm_row():
    row = SimpleNamespace(
        id=5,
        concert_id=1,
        description="Retour de son",
        occurred_at=START,
        resolved=False,
    )

    response = incident_to_response(row)

    assert response.occurred_at == START.replace(tzinfo=timezone.utc)


def test_incident_mapping_rejects_blank_description():
    dto = IncidentCreateRequest(concert_id=1, description="   ")

    with pytest.raises(InvalidIncidentMessageError):
        incident_create_to_domain(dto)
