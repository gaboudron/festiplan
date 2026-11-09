from datetime import datetime, timezone
import pytest
from app.database import SessionLocal
from app.adapters.outbound.repository.festival_sqlalchemy_repository import (
    FestivalSqlAlchemyRepository,
)
from app.adapters.outbound.repository.stage_sqlalchemy_repository import (
    StageSqlAlchemyRepository,
)
from app.adapters.outbound.repository.artist_sqlalchemy_repository import (
    ArtistSqlAlchemyRepository,
)
from app.adapters.outbound.repository.concert_sqlalchemy_repository import (
    ConcertSqlAlchemyRepository,
)
from app.adapters.outbound.repository.incident_sqlalchemy_repository import (
    IncidentSqlAlchemyRepository,
)
from app.domain.festival.entities import Festival, Stage
from app.domain.festival.value_objects import FestivalStatus
from app.domain.artist.entities import Artist
from app.domain.concert.entities import Concert
from app.domain.incident.entities import Incident
from app.domain.time_range import TimeRange
from app.domain.equipments import EquipmentSet


@pytest.fixture
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_festival_repository_crud(db_session):
    repo = FestivalSqlAlchemyRepository(db_session)
    festival = Festival(
        id=None,
        name="Hellfest",
        location="Clisson",
        time_range=TimeRange(
            start=datetime(2027, 6, 18, 10, 0),
            end=datetime(2027, 6, 20, 23, 0),
        ),
        status=FestivalStatus.PREPARATION,
    )

    saved = repo.save(festival)
    assert saved.id is not None
    assert saved.name == "Hellfest"

    fetched = repo.get(saved.id)
    assert fetched is not None
    assert fetched.id == saved.id
    assert fetched.name == "Hellfest"
    assert fetched.status == FestivalStatus.PREPARATION

    # Update
    fetched.publish()
    updated = repo.save(fetched)
    assert updated.status == FestivalStatus.PUBLISHED

    # List all
    all_festivals = repo.list_all()
    assert any(f.id == saved.id for f in all_festivals)


def test_stage_repository_crud(db_session):
    fest_repo = FestivalSqlAlchemyRepository(db_session)
    festival = fest_repo.save(
        Festival(
            id=None,
            name="ElectroBeach",
            location="Barcarès",
            time_range=TimeRange(
                start=datetime(2027, 7, 10, 10, 0),
                end=datetime(2027, 7, 12, 23, 0),
            ),
        )
    )

    stage_repo = StageSqlAlchemyRepository(db_session)
    stage = Stage(
        id=None,
        festival_id=festival.id,
        name="Main Stage",
        capacity=20000,
        available_equipment=EquipmentSet.from_list(["laser", "sound"]),
    )

    saved = stage_repo.save(stage)
    assert saved.id is not None
    assert saved.name == "Main Stage"

    stages = stage_repo.list_by_festival_id(festival.id)
    assert len(stages) == 1
    assert stages[0].name == "Main Stage"
    assert "laser" in stages[0].available_equipment.items


def test_artist_repository_crud(db_session):
    repo = ArtistSqlAlchemyRepository(db_session)
    artist = Artist(
        id=None,
        name="Justice",
        genre="Electro",
        required_equipment=EquipmentSet.from_list(["sound", "cross"]),
    )

    saved = repo.save(artist)
    assert saved.id is not None
    assert saved.name == "Justice"

    fetched = repo.get(saved.id)
    assert fetched is not None
    assert fetched.genre == "Electro"

    all_artists = repo.list_all()
    assert any(a.name == "Justice" for a in all_artists)


def test_concert_repository_crud(db_session):
    fest_repo = FestivalSqlAlchemyRepository(db_session)
    stage_repo = StageSqlAlchemyRepository(db_session)
    artist_repo = ArtistSqlAlchemyRepository(db_session)
    concert_repo = ConcertSqlAlchemyRepository(db_session)

    festival = fest_repo.save(
        Festival(
            id=None,
            name="Rock en Seine",
            location="Saint-Cloud",
            time_range=TimeRange(
                start=datetime(2027, 8, 20, 10, 0),
                end=datetime(2027, 8, 22, 23, 0),
            ),
        )
    )
    stage = stage_repo.save(
        Stage(
            id=None,
            festival_id=festival.id,
            name="Scène Cascade",
            capacity=15000,
            available_equipment=EquipmentSet.from_list(["sound"]),
        )
    )
    artist = artist_repo.save(
        Artist(
            id=None,
            name="Arctic Monkeys",
            genre="Indie Rock",
            required_equipment=EquipmentSet.from_list(["sound"]),
        )
    )

    concert = Concert(
        id=None,
        festival_id=festival.id,
        artist_id=artist.id,
        stage_id=stage.id,
        time_range=TimeRange(
            start=datetime(2027, 8, 20, 20, 0),
            end=datetime(2027, 8, 20, 21, 30),
        ),
    )

    saved = concert_repo.save(concert)
    assert saved.id is not None

    concerts = concert_repo.list_by_festival_id(festival.id)
    assert len(concerts) == 1
    assert concerts[0].id == saved.id

    # Reschedule
    saved.reschedule(
        TimeRange(
            start=datetime(2027, 8, 20, 21, 0),
            end=datetime(2027, 8, 20, 22, 30),
        )
    )
    updated = concert_repo.save(saved)
    assert updated.time_range.start == datetime(2027, 8, 20, 21, 0)

    # Cancel
    updated.cancel()
    cancelled = concert_repo.save(updated)
    assert cancelled.is_cancelled


def test_incident_repository_crud(db_session):
    fest_repo = FestivalSqlAlchemyRepository(db_session)
    stage_repo = StageSqlAlchemyRepository(db_session)
    artist_repo = ArtistSqlAlchemyRepository(db_session)
    concert_repo = ConcertSqlAlchemyRepository(db_session)
    incident_repo = IncidentSqlAlchemyRepository(db_session)

    festival = fest_repo.save(
        Festival(
            id=None,
            name="Fest X",
            location="Lyon",
            time_range=TimeRange(
                start=datetime(2027, 9, 1, 10, 0),
                end=datetime(2027, 9, 2, 23, 0),
            ),
        )
    )
    stage = stage_repo.save(
        Stage(
            id=None,
            festival_id=festival.id,
            name="Scène 1",
            capacity=5000,
            available_equipment=EquipmentSet.from_list([]),
        )
    )
    artist = artist_repo.save(
        Artist(
            id=None,
            name="Phoenix",
            genre="Pop",
            required_equipment=EquipmentSet.from_list([]),
        )
    )
    concert = concert_repo.save(
        Concert(
            id=None,
            festival_id=festival.id,
            artist_id=artist.id,
            stage_id=stage.id,
            time_range=TimeRange(
                start=datetime(2027, 9, 1, 20, 0),
                end=datetime(2027, 9, 1, 21, 0),
            ),
        )
    )

    incident = Incident(
        id=None,
        concert_id=concert.id,
        description="Microphone defect",
        occurred_at=datetime.now(timezone.utc),
    )

    saved = incident_repo.save(incident)
    assert saved.id is not None
    assert saved.description == "Microphone defect"
    assert not saved.resolved

    by_concert = incident_repo.list_by_concert_id(concert.id)
    assert len(by_concert) == 1

    saved.mark_resolved()
    updated = incident_repo.save(saved)
    assert updated.resolved is True

