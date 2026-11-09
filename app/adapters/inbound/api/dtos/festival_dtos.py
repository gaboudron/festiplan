"""DTO de l'adaptateur entrant pour les festivals."""

from pydantic import BaseModel, ConfigDict, Field

from app.utils.datetime_helpers import UTCDatetime


class FestivalCreateRequest(BaseModel):
    """Payload attendu pour la création d'un festival."""

    name: str = Field(min_length=2, max_length=120)
    location: str = Field(min_length=2, max_length=120)
    start_date: UTCDatetime
    end_date: UTCDatetime


class FestivalResponse(FestivalCreateRequest):
    """Représentation d'un festival renvoyée au client."""

    id: int
    status: str
    model_config = ConfigDict(from_attributes=True)
