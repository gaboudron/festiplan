"""DTO de l'adaptateur entrant pour les artistes."""

from pydantic import BaseModel, Field


class ArtistCreateRequest(BaseModel):
    """Payload attendu pour la création d'un artiste."""

    name: str = Field(min_length=2, max_length=120)
    genre: str = Field(min_length=2, max_length=80)
    required_equipment: list[str] = Field(default_factory=list)


class ArtistResponse(BaseModel):
    """Représentation d'un artiste renvoyé au client."""

    id: int
    name: str
    genre: str
    required_equipment: list[str]
