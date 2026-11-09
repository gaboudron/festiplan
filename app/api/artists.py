from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.adapters.inbound.api.dtos import ArtistCreateRequest, ArtistResponse
from app.adapters.inbound.api.mappers import (
    artist_create_to_domain,
    artist_to_response,
)
from app.database import get_db
from app.services.artist_service import ArtistService

router = APIRouter(prefix="/artists", tags=["artists"])


@router.get("", response_model=list[ArtistResponse])
def list_artists(db: Session = Depends(get_db)):
    return [artist_to_response(artist) for artist in ArtistService(db).list_artists()]


@router.post("", response_model=ArtistResponse, status_code=201)
def create_artist(payload: ArtistCreateRequest, db: Session = Depends(get_db)):
    # Validation/normalisation du domaine à la frontière entrante.
    artist_create_to_domain(payload)
    return artist_to_response(ArtistService(db).create_artist(payload))
