from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.adapters.inbound.api.dtos import (
    IncidentCreateRequest,
    IncidentResponse,
)
from app.adapters.inbound.api.mappers import (
    incident_create_to_domain,
    incident_to_response,
)
from app.database import get_db
from app.models import Concert, Incident

router = APIRouter(prefix="/incidents", tags=["incidents"])


@router.post("", response_model=IncidentResponse, status_code=201)
def create_incident(payload: IncidentCreateRequest, db: Session = Depends(get_db)):
    if db.query(Concert).filter(Concert.id == payload.concert_id).first() is None:
        raise HTTPException(status_code=404, detail="Concert introuvable")

    # Validation/normalisation du domaine à la frontière entrante.
    incident = incident_create_to_domain(payload)

    row = Incident(
        concert_id=incident.concert_id,
        description=incident.description,
        occurred_at=incident.occurred_at,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return incident_to_response(row)


@router.get("", response_model=list[IncidentResponse])
def list_incidents(concert_id: int | None = None, db: Session = Depends(get_db)):
    query = db.query(Incident)
    if concert_id is not None:
        query = query.filter(Incident.concert_id == concert_id)
    return [
        incident_to_response(incident)
        for incident in query.order_by(Incident.occurred_at.desc()).all()
    ]
