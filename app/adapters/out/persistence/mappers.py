from datetime import timezone

from app.models import (
    Artist as ArtistModel,
    Concert as ConcertModel,
    Festival as FestivalModel,
    Incident as IncidentModel,
    Stage as StageModel,
)

from app.domain.artist.entities import Artist
from app.domain.concert.entities import Concert
from app.domain.concert.value_object import ConcertStatus
from app.domain.festival.entities import Festival, Stage
from app.domain.festival.value_objects import FestivalStatus
from app.domain.incident.entities import Incident
from app.domain.time_range import TimeRange
from app.domain.equipments import EquipmentSet


# --------------------------------------------------
# Gestion des équipements
# --------------------------------------------------

def equipment_to_db(equipment: EquipmentSet) -> str:
    """Convertit un EquipmentSet en texte pour la base."""
    return ",".join(equipment.to_list())


def equipment_from_db(value: str | None) -> EquipmentSet:
    """Convertit le texte de la base en EquipmentSet."""
    if not value:
        return EquipmentSet.from_list([])

    return EquipmentSet.from_list(value.split(","))


# --------------------------------------------------
# Gestion des dates
# --------------------------------------------------

def datetime_to_db(value):
    """Convertit une date avec fuseau en UTC sans fuseau."""
    if value.tzinfo is None:
        return value

    return value.astimezone(timezone.utc).replace(tzinfo=None)


def datetime_from_db(value):
    """Interprète une date SQL sans fuseau comme une date UTC."""
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)

    return value.astimezone(timezone.utc)


# --------------------------------------------------
# Artist
# --------------------------------------------------

def artist_to_domain(model: ArtistModel) -> Artist:
    return Artist(
        id=model.id,
        name=model.name,
        genre=model.genre,
        required_equipment=equipment_from_db(model.required_equipment),
    )


def artist_to_model(entity: Artist) -> ArtistModel:
    return ArtistModel(
        id=entity.id,
        name=entity.name,
        genre=entity.genre,
        required_equipment=equipment_to_db(entity.required_equipment),
    )


# --------------------------------------------------
# Stage
# --------------------------------------------------

def stage_to_domain(model: StageModel) -> Stage:
    return Stage(
        id=model.id,
        festival_id=model.festival_id,
        name=model.name,
        capacity=model.capacity,
        available_equipment=equipment_from_db(model.available_equipment),
    )


def stage_to_model(entity: Stage) -> StageModel:
    return StageModel(
        id=entity.id,
        festival_id=entity.festival_id,
        name=entity.name,
        capacity=entity.capacity,
        available_equipment=equipment_to_db(entity.available_equipment),
    )


# --------------------------------------------------
# Concert
# --------------------------------------------------

def concert_to_domain(model: ConcertModel) -> Concert:
    return Concert(
        id=model.id,
        festival_id=model.festival_id,
        artist_id=model.artist_id,
        stage_id=model.stage_id,
        time_range=TimeRange(
            start=datetime_from_db(model.start_time),
            end=datetime_from_db(model.end_time),
        ),
        status=ConcertStatus(model.status),
    )


def concert_to_model(entity: Concert) -> ConcertModel:
    return ConcertModel(
        id=entity.id,
        festival_id=entity.festival_id,
        artist_id=entity.artist_id,
        stage_id=entity.stage_id,
        start_time=datetime_to_db(entity.time_range.start),
        end_time=datetime_to_db(entity.time_range.end),
        status=entity.status.value,
    )


# --------------------------------------------------
# Festival
# --------------------------------------------------

def festival_to_domain(model: FestivalModel) -> Festival:
    return Festival(
        id=model.id,
        name=model.name,
        location=model.location,
        time_range=TimeRange(
            start=datetime_from_db(model.start_date),
            end=datetime_from_db(model.end_date),
        ),
        status=FestivalStatus(model.status),
        stages=[stage_to_domain(stage) for stage in model.stages],
    )


def festival_to_model(entity: Festival) -> FestivalModel:
    return FestivalModel(
        id=entity.id,
        name=entity.name,
        location=entity.location,
        start_date=datetime_to_db(entity.time_range.start),
        end_date=datetime_to_db(entity.time_range.end),
        status=entity.status.value,
        stages=[stage_to_model(stage) for stage in entity.stages],
    )


# --------------------------------------------------
# Incident
# --------------------------------------------------

def incident_to_domain(model: IncidentModel) -> Incident:
    return Incident(
        id=model.id,
        concert_id=model.concert_id,
        description=model.description,
        occurred_at=datetime_from_db(model.occurred_at),
        resolved=model.resolved,
    )


def incident_to_model(entity: Incident) -> IncidentModel:
    return IncidentModel(
        id=entity.id,
        concert_id=entity.concert_id,
        description=entity.description,
        occurred_at=datetime_to_db(entity.occurred_at),
        resolved=entity.resolved,
    )
