from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.adapters.inbound.api.dtos import (
    FestivalCreateRequest,
    FestivalResponse,
)
from app.adapters.inbound.api.mappers import (
    festival_create_to_domain,
    festival_to_response,
)
from app.database import get_db
from app.services.festival_service import FestivalService
from app.services.publication_service import PublicationService

router = APIRouter(prefix="/festivals", tags=["festivals"])


@router.get("", response_model=list[FestivalResponse])
def list_festivals(db: Session = Depends(get_db)):
    return [festival_to_response(festival) for festival in FestivalService(db).list_festivals()]


@router.post("", response_model=FestivalResponse, status_code=201)
def create_festival(payload: FestivalCreateRequest, db: Session = Depends(get_db)):
    # Validation du créneau à la frontière entrante (InvalidTimeRangeError -> 400).
    festival_create_to_domain(payload)
    try:
        return festival_to_response(FestivalService(db).create_festival(payload))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.post("/{festival_id}/publish", response_model=FestivalResponse)
def publish_festival(festival_id: int, db: Session = Depends(get_db)):
    try:
        festival = PublicationService(db).publish(festival_id)
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    if festival is None:
        raise HTTPException(status_code=404, detail="Festival introuvable")
    return festival_to_response(festival)
