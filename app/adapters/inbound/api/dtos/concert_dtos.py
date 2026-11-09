"""DTO de l'adaptateur entrant pour les concerts."""

from pydantic import BaseModel, ConfigDict

from app.utils.datetime_helpers import UTCDatetime


class ConcertCreateRequest(BaseModel):
    """Payload attendu pour la création d'un concert."""

    festival_id: int
    artist_id: int
    stage_id: int
    start_time: UTCDatetime
    end_time: UTCDatetime


class ConcertRescheduleRequest(BaseModel):
    """Payload attendu pour le déplacement d'un concert.

    ``stage_id`` est optionnel : ``None`` conserve la scène actuelle.
    """

    stage_id: int | None = None
    start_time: UTCDatetime
    end_time: UTCDatetime


class ConcertResponse(BaseModel):
    """Représentation d'un concert renvoyée au client."""

    id: int
    festival_id: int
    artist_id: int
    stage_id: int
    start_time: UTCDatetime
    end_time: UTCDatetime
    status: str
    model_config = ConfigDict(from_attributes=True)
