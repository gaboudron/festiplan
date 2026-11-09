from datetime import datetime, timezone
from app.adapters.outbound.repository.mappers.artist_mapper import ArtistMapper
from app.adapters.outbound.repository.mappers.concert_mapper import ConcertMapper
from app.adapters.outbound.repository.mappers.equipment_mapper import (
    EquipmentMapper,
)
from app.adapters.outbound.repository.mappers.festival_mapper import (
    FestivalMapper,
)
from app.adapters.outbound.repository.mappers.incident_mapper import (
    IncidentMapper,
)
from app.adapters.outbound.repository.mappers.stage_mapper import StageMapper
from app.models import (
    Artist as ArtistORM,
    Concert as ConcertORM,
    Festival as FestivalORM,
    Incident as IncidentORM,
    Stage as StageORM,
)
from app.domain.artist.entities import Artist
from app.domain.concert.entities import Concert
from app.domain.concert.value_object import ConcertStatus
from app.domain.equipments import EquipmentSet
from app.domain.festival.entities import Festival, Stage
from app.domain.festival.value_objects import FestivalStatus
from app.domain.incident.entities import Incident
from app.domain.time_range import TimeRange


def test_stage_mapper():
    orm = StageORM(
        id=1,
        festival_id=10,
        name="Main Stage",
        capacity=5000,
        available_equipment="light, sound, mic",
    )
    domain = StageMapper.to_domain(orm)

    assert domain.id == 1
    assert domain.festival_id == 10
    assert domain.name == "Main Stage"
    assert domain.capacity == 5000
    assert domain.available_equipment.items == frozenset({"light", "sound", "mic"})

    # to_orm (new)
    new_orm = StageMapper.to_orm(domain)
    assert new_orm.id == 1
    assert new_orm.name == "Main Stage"
    assert "light" in new_orm.available_equipment

    # to_orm (update)
    domain.name = "Renamed Stage"
    updated_orm = StageMapper.to_orm(domain, existing_orm=orm)
    assert updated_orm.name == "Renamed Stage"
    assert updated_orm is orm


def test_festival_mapper():
    start = datetime(2026, 7, 1, 10, 0)
    end = datetime(2026, 7, 3, 23, 0)
    orm = FestivalORM(
        id=2,
        name="Summer Fest",
        location="Paris",
        start_date=start,
        end_date=end,
        status="preparation",
        stages=[
            StageORM(
                id=1,
                festival_id=2,
                name="A",
                capacity=100,
                available_equipment="sound",
            )
        ],
    )
    domain = FestivalMapper.to_domain(orm)

    assert domain.id == 2
    assert domain.name == "Summer Fest"
    assert domain.location == "Paris"
    assert domain.time_range.start == start
    assert domain.time_range.end == end
    assert domain.status == FestivalStatus.PREPARATION
    assert len(domain.stages) == 1
    assert domain.stages[0].name == "A"

    # to_orm (new)
    new_orm = FestivalMapper.to_orm(domain)
    assert new_orm.id == 2
    assert new_orm.name == "Summer Fest"
    assert new_orm.start_date == start
    assert new_orm.status == "preparation"

    # to_orm (update)
    domain.publish()
    updated_orm = FestivalMapper.to_orm(domain, existing_orm=orm)
    assert updated_orm.status == "published"
    assert updated_orm is orm


def test_artist_mapper():
    orm = ArtistORM(
        id=3,
        name="Daft Punk",
        genre="Electro",
        required_equipment="synthesizer, laser",
    )
    domain = ArtistMapper.to_domain(orm)

    assert domain.id == 3
    assert domain.name == "Daft Punk"
    assert domain.genre == "Electro"
    assert domain.required_equipment.items == frozenset({"synthesizer", "laser"})

    # to_orm
    new_orm = ArtistMapper.to_orm(domain)
    assert new_orm.id == 3
    assert new_orm.name == "Daft Punk"
    assert "synthesizer" in new_orm.required_equipment


def test_concert_mapper():
    start = datetime(2026, 7, 1, 20, 0)
    end = datetime(2026, 7, 1, 22, 0)
    orm = ConcertORM(
        id=4,
        festival_id=2,
        artist_id=3,
        stage_id=1,
        start_time=start,
        end_time=end,
        status="scheduled",
    )
    domain = ConcertMapper.to_domain(orm)

    assert domain.id == 4
    assert domain.festival_id == 2
    assert domain.artist_id == 3
    assert domain.stage_id == 1
    assert domain.time_range.start == start
    assert domain.time_range.end == end
    assert domain.status == ConcertStatus.SCHEDULED

    # to_orm
    new_orm = ConcertMapper.to_orm(domain)
    assert new_orm.id == 4
    assert new_orm.status == "scheduled"
    assert new_orm.start_time == start


def test_incident_mapper():
    now = datetime.now(timezone.utc)
    orm = IncidentORM(
        id=5,
        concert_id=4,
        description="Power outage",
        occurred_at=now,
        resolved=False,
    )
    domain = IncidentMapper.to_domain(orm)

    assert domain.id == 5
    assert domain.concert_id == 4
    assert domain.description == "Power outage"
    assert domain.occurred_at == now
    assert not domain.resolved

    # to_orm
    domain.mark_resolved()
    updated_orm = IncidentMapper.to_orm(domain, existing_orm=orm)
    assert updated_orm.resolved is True


def test_equipment_mapper():
    eq = EquipmentMapper.to_domain("light, sound, microphone")
    assert eq.items == frozenset({"light", "sound", "microphone"})

    raw = EquipmentMapper.to_orm(eq)
    assert "light" in raw
    assert "sound" in raw
    assert "microphone" in raw

    empty = EquipmentMapper.to_domain(None)
    assert len(empty.items) == 0

