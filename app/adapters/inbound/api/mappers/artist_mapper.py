"""Mappings DTO ↔ domaine pour les artistes."""

from typing import Any

from app.adapters.inbound.api.dtos import ArtistCreateRequest, ArtistResponse
from app.adapters.inbound.api.mappers.common import (
    equipment_items,
    require_persisted_id,
)
from app.domain.artist.entities import Artist
from app.domain.equipments import EquipmentSet


def artist_create_to_domain(dto: ArtistCreateRequest) -> Artist:
    return Artist(
        id=None,
        name=dto.name,
        genre=dto.genre,
        required_equipment=EquipmentSet.from_list(dto.required_equipment),
    )


def artist_to_response(artist: Any) -> ArtistResponse:
    """Mappe un artiste du domaine (ou une ligne ORM transitoire) vers le DTO."""
    return ArtistResponse(
        id=require_persisted_id(artist.id),
        name=artist.name,
        genre=artist.genre,
        required_equipment=equipment_items(artist.required_equipment),
    )
