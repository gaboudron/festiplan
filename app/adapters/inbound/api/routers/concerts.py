from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.adapters.inbound.api.dtos import (
    ConcertCreateRequest,
    ConcertRescheduleRequest,
    ConcertResponse,
)
from app.adapters.inbound.api.mappers import (
    concert_create_to_domain,
    concert_reschedule_to_time_range,
    concert_to_response,
)
from app.database import get_db
from app.models import Concert
from app.services.scheduling_service import SchedulingService

router = APIRouter(prefix="/concerts", tags=["concerts"])


@router.get("", response_model=list[ConcertResponse])
def list_concerts(festival_id: int, db: Session = Depends(get_db)):
    return [
        concert_to_response(concert)
        for concert in SchedulingService(db).list_concerts(festival_id)
    ]


@router.get("/{concert_id}", response_model=ConcertResponse)
def get_concert(concert_id: int, db: Session = Depends(get_db)):
    # Accès direct à SQLAlchemy depuis le contrôleur : défaut architectural.
    concert = db.query(Concert).filter(Concert.id == concert_id).first()
    if concert is None:
        raise HTTPException(status_code=404, detail="Concert introuvable")
    return concert_to_response(concert)


@router.post("", response_model=ConcertResponse, status_code=201)
def create_concert(payload: ConcertCreateRequest, db: Session = Depends(get_db)):
    # Validation du créneau à la frontière entrante (InvalidTimeRangeError -> 400).
    concert_create_to_domain(payload)
    try:
        return concert_to_response(SchedulingService(db).create_concert(payload))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.patch("/{concert_id}/reschedule", response_model=ConcertResponse)
def reschedule_concert(
    concert_id: int,
    payload: ConcertRescheduleRequest,
    db: Session = Depends(get_db),
):
    # Validation du nouveau créneau à la frontière entrante.
    concert_reschedule_to_time_range(payload)

    try:
        concert = SchedulingService(db).reschedule_concert(concert_id, payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    # Le service retourne None quand le concert n'existe pas : pas besoin
    # d'une lecture SQLAlchemy supplémentaire dans le routeur.
    if concert is None:
        raise HTTPException(status_code=404, detail="Concert introuvable")
    return concert_to_response(concert)


@router.post("/{concert_id}/cancel", response_model=ConcertResponse)
def cancel_concert(concert_id: int, db: Session = Depends(get_db)):
    concert = SchedulingService(db).cancel_concert(concert_id)
    if concert is None:
        raise HTTPException(status_code=404, detail="Concert introuvable")
    return concert_to_response(concert)


@router.get("/schedule/{festival_id}", response_model=list[ConcertResponse])
def get_schedule(festival_id: int, db: Session = Depends(get_db)):
    return [
        concert_to_response(concert)
        for concert in SchedulingService(db).get_schedule(festival_id)
    ]
