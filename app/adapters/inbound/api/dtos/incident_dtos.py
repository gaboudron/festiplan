"""DTO de l'adaptateur entrant pour les incidents."""

from pydantic import BaseModel, ConfigDict, Field

from app.utils.datetime_helpers import UTCDatetime, UTCDatetimeOrNone


class IncidentCreateRequest(BaseModel):
    """Payload attendu pour la déclaration d'un incident."""

    concert_id: int
    description: str = Field(min_length=3, max_length=2000)
    occurred_at: UTCDatetimeOrNone = None


class IncidentResponse(BaseModel):
    """Représentation d'un incident renvoyée au client."""

    id: int
    concert_id: int
    description: str
    occurred_at: UTCDatetime
    resolved: bool
    model_config = ConfigDict(from_attributes=True)
