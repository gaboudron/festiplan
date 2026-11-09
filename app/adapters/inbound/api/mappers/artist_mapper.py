"""Mappings DTO ↔ domaine pour les artistes."""

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


def artist_to_response(artist: Artist) -> ArtistResponse:
    """Mappe un artiste du domaine vers le DTO de réponse."""
    return ArtistResponse(
        id=require_persisted_id(artist.id),
        name=artist.name,
        genre=artist.genre,
        required_equipment=equipment_items(artist.required_equipment),
    )
