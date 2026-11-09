"""Fabriques d'entités du domaine pour les tests des cas d'usage.

Chaque fabrique construit une entité valide avec des valeurs par défaut
raisonnables, tout en laissant chaque champ surchargeable. Les tests restent
ainsi focalisés sur le comportement du cas d'usage plutôt que sur la
construction des objets du domaine.

Convention temporelle : toutes les dates par défaut sont en UTC aware,
conformément à la règle du domaine.
"""

from datetime import datetime, timezone

from app.domain.artist.entities import Artist
from app.domain.concert.entities import Concert
from app.domain.concert.value_object import ConcertStatus
from app.domain.equipments import EquipmentSet
from app.domain.festival.entities import Festival, Stage
from app.domain.festival.value_objects import FestivalStatus
from app.domain.incident.entities import Incident
from app.domain.time_range import TimeRange

__all__ = [
    "make_artist",
    "make_concert",
    "make_festival",
    "make_incident",
    "make_stage",
]

# Créneaux par défaut : un festival de trois jours et un concert le premier soir.
DEFAULT_FESTIVAL_START = datetime(2027, 6, 18, 10, 0, tzinfo=timezone.utc)
DEFAULT_FESTIVAL_END = datetime(2027, 6, 20, 23, 0, tzinfo=timezone.utc)
DEFAULT_CONCERT_START = datetime(2027, 6, 18, 18, 0, tzinfo=timezone.utc)
DEFAULT_CONCERT_END = datetime(2027, 6, 18, 19, 30, tzinfo=timezone.utc)
DEFAULT_INCIDENT_OCCURRED_AT = datetime(2027, 6, 18, 20, 0, tzinfo=timezone.utc)


def _equipment_set(items, *, default=()) -> EquipmentSet:
    """Construit un ``EquipmentSet`` à partir d'itérables ou du défaut fourni."""
    return EquipmentSet.from_list(list(default if items is None else items))


def make_artist(
    *,
    id: int | None = 1,
    name: str = "Iron Vow",
    genre: str = "Heavy metal",
    required_equipment=None,
) -> Artist:
    """Construit un artiste valide.

    ``required_equipment`` accepte une liste ou tout itérable de noms
    d'équipements ; ``None`` applique le défaut ``("large_rigging",)``.
    """
    return Artist(
        id=id,
        name=name,
        genre=genre,
        required_equipment=_equipment_set(
            required_equipment,
            default=("large_rigging",),
        ),
    )


def make_stage(
    *,
    id: int | None = 1,
    festival_id: int = 1,
    name: str = "Mainstage",
    capacity: int = 50_000,
    available_equipment=None,
) -> Stage:
    """Construit une scène valide.

    ``available_equipment`` accepte une liste ou tout itérable de noms
    d'équipements ; ``None`` applique le défaut
    ``("large_rigging", "special_lighting")``.
    """
    return Stage(
        id=id,
        festival_id=festival_id,
        name=name,
        capacity=capacity,
        available_equipment=_equipment_set(
            available_equipment,
            default=("large_rigging", "special_lighting"),
        ),
    )


def make_festival(
    *,
    id: int | None = 1,
    name: str = "Hellforge Open Air",
    location: str = "Clisson",
    time_range: TimeRange | None = None,
    status: FestivalStatus = FestivalStatus.PREPARATION,
    stages: list[Stage] | None = None,
) -> Festival:
    """Construit un festival valide.

    ``time_range`` vaut par défaut trois jours à partir du 18 juin 2027.
    ``stages`` est copié pour que l'appelant puisse réutiliser sa liste.
    """
    return Festival(
        id=id,
        name=name,
        location=location,
        time_range=time_range
        or TimeRange(DEFAULT_FESTIVAL_START, DEFAULT_FESTIVAL_END),
        status=status,
        stages=list(stages) if stages is not None else [],
    )


def make_concert(
    *,
    id: int | None = 1,
    festival_id: int = 1,
    artist_id: int = 1,
    stage_id: int = 1,
    time_range: TimeRange | None = None,
    status: ConcertStatus = ConcertStatus.SCHEDULED,
) -> Concert:
    """Construit un concert valide.

    ``time_range`` vaut par défaut le créneau du 18 juin 2027, 18h00-19h30 UTC.
    """
    return Concert(
        id=id,
        festival_id=festival_id,
        artist_id=artist_id,
        stage_id=stage_id,
        time_range=time_range or TimeRange(DEFAULT_CONCERT_START, DEFAULT_CONCERT_END),
        status=status,
    )


def make_incident(
    *,
    id: int | None = 1,
    concert_id: int = 1,
    description: str = "Retour de sonde sur la scène principale",
    occurred_at: datetime | None = None,
    resolved: bool = False,
) -> Incident:
    """Construit un incident valide.

    ``occurred_at`` vaut par défaut le 18 juin 2027 à 20h00 UTC.
    """
    return Incident(
        id=id,
        concert_id=concert_id,
        description=description,
        occurred_at=occurred_at or DEFAULT_INCIDENT_OCCURRED_AT,
        resolved=resolved,
    )
