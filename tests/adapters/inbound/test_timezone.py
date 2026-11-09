"""Tests de la convention timezone aux frontières et en persistance.

Convention du projet : tout datetime exposé est en UTC aware, les entrées
naïves sont interprétées comme de l'UTC, et l'ORM stocke de l'UTC naïf puis
restitue de l'UTC aware.
"""

from datetime import datetime, timedelta, timezone

from app.adapters.inbound.api.dtos import (
    ConcertRescheduleRequest,
    FestivalCreateRequest,
    IncidentCreateRequest,
)
from app.adapters.outbound.repository.models import Festival
from app.database import SessionLocal
from app.utils.datetime_helpers import ensure_utc


def test_schema_normalizes_naive_datetime_to_utc():
    festival = FestivalCreateRequest(
        name="Festiplan",
        location="Paris",
        start_date=datetime(2027, 6, 18, 18, 0),
        end_date=datetime(2027, 6, 18, 23, 0),
    )

    assert festival.start_date == datetime(2027, 6, 18, 18, 0, tzinfo=timezone.utc)
    assert festival.start_date.tzinfo is not None
    assert festival.end_date == datetime(2027, 6, 18, 23, 0, tzinfo=timezone.utc)


def test_schema_converts_offset_to_utc():
    festival = FestivalCreateRequest(
        name="Festiplan",
        location="Paris",
        start_date=datetime(2027, 6, 18, 20, 0, tzinfo=timezone(timedelta(hours=2))),
        end_date=datetime(2027, 6, 18, 21, 0, tzinfo=timezone(timedelta(hours=2))),
    )

    assert festival.start_date == datetime(2027, 6, 18, 18, 0, tzinfo=timezone.utc)
    assert festival.end_date == datetime(2027, 6, 18, 19, 0, tzinfo=timezone.utc)


def test_concert_reschedule_dto_normalizes_datetimes_to_utc():
    dto = ConcertRescheduleRequest(
        stage_id=3,
        start_time=datetime(2027, 6, 18, 20, 0, tzinfo=timezone(timedelta(hours=2))),
        end_time=datetime(2027, 6, 18, 22, 0),
    )

    assert dto.start_time == datetime(2027, 6, 18, 18, 0, tzinfo=timezone.utc)
    assert dto.end_time == datetime(2027, 6, 18, 22, 0, tzinfo=timezone.utc)


def test_incident_schema_normalizes_optional_occurred_at():
    dto = IncidentCreateRequest(
        concert_id=1,
        description="Micro défectueux",
        occurred_at=datetime(2027, 6, 18, 20, 0),
    )

    assert dto.occurred_at == datetime(2027, 6, 18, 20, 0, tzinfo=timezone.utc)

    without_date = IncidentCreateRequest(
        concert_id=1, description="Micro défectueux"
    )
    assert without_date.occurred_at is None


def test_ensure_utc_is_idempotent():
    aware = datetime(2027, 6, 18, 18, 0, tzinfo=timezone.utc)

    assert ensure_utc(aware) is aware
    assert ensure_utc(ensure_utc(datetime(2027, 6, 18, 18, 0))) == aware


def test_orm_round_trip_returns_aware_utc():
    db = SessionLocal()
    try:
        festival = Festival(
            name="Round-trip",
            location="Lyon",
            start_date=datetime(2027, 6, 18, 18, 0),
            end_date=datetime(2027, 6, 18, 23, 0),
            status="preparation",
        )
        db.add(festival)
        db.commit()
        festival_id = festival.id
    finally:
        db.close()

    db = SessionLocal()
    try:
        reloaded = db.get(Festival, festival_id)

        assert reloaded.start_date == datetime(2027, 6, 18, 18, 0, tzinfo=timezone.utc)
        assert reloaded.end_date == datetime(2027, 6, 18, 23, 0, tzinfo=timezone.utc)
        assert reloaded.start_date.tzinfo is not None
        assert reloaded.end_date.tzinfo is not None
    finally:
        if reloaded is not None:
            db.delete(reloaded)
            db.commit()
        db.close()


def test_orm_round_trip_converts_offset_to_utc():
    db = SessionLocal()
    try:
        festival = Festival(
            name="Offset round-trip",
            location="Berlin",
            start_date=datetime(2027, 6, 18, 20, 0, tzinfo=timezone(timedelta(hours=2))),
            end_date=datetime(2027, 6, 18, 22, 0, tzinfo=timezone(timedelta(hours=2))),
            status="preparation",
        )
        db.add(festival)
        db.commit()
        festival_id = festival.id
    finally:
        db.close()

    db = SessionLocal()
    try:
        reloaded = db.get(Festival, festival_id)

        assert reloaded.start_date == datetime(2027, 6, 18, 18, 0, tzinfo=timezone.utc)
        assert reloaded.end_date == datetime(2027, 6, 18, 20, 0, tzinfo=timezone.utc)
    finally:
        if reloaded is not None:
            db.delete(reloaded)
            db.commit()
        db.close()
