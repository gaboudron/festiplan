"""DTO de l'adaptateur entrant pour les scènes."""

from pydantic import BaseModel, Field


class StageCreateRequest(BaseModel):
    """Payload attendu pour la création d'une scène."""

    festival_id: int
    name: str = Field(min_length=2, max_length=100)
    capacity: int = Field(gt=0)
    available_equipment: list[str] = Field(default_factory=list)


class StageResponse(BaseModel):
    """Représentation d'une scène renvoyée au client."""

    id: int
    festival_id: int
    name: str
    capacity: int
    available_equipment: list[str]
