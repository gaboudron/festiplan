"""Routeur FastAPI pour les artistes."""

from fastapi import APIRouter, Depends

from app.adapters.inbound.api.dependencies import get_artist_service
from app.adapters.inbound.api.dtos import ArtistCreateRequest, ArtistResponse
from app.adapters.inbound.api.mappers import (
    artist_create_to_domain,
    artist_to_response,
)
from app.ports.inbound.artist_inbound_port import ArtistInboundPort

router = APIRouter(prefix="/artists", tags=["artists"])


@router.get("", response_model=list[ArtistResponse])
def list_artists(
    service: ArtistInboundPort = Depends(get_artist_service),
):
    return [artist_to_response(artist) for artist in service.list_artists()]


@router.post("", response_model=ArtistResponse, status_code=201)
def create_artist(
    payload: ArtistCreateRequest,
    service: ArtistInboundPort = Depends(get_artist_service),
):
    artist = artist_create_to_domain(payload)
    created = service.create_artist(artist)
    return artist_to_response(created)
