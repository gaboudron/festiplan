from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.adapters.inbound.api.dtos import StageCreateRequest, StageResponse
from app.adapters.inbound.api.mappers import (
    stage_create_to_domain,
    stage_to_response,
)
from app.database import get_db
from app.services.stage_service import StageService

router = APIRouter(prefix="/stages", tags=["stages"])


@router.get("", response_model=list[StageResponse])
def list_stages(festival_id: int, db: Session = Depends(get_db)):
    return [stage_to_response(stage) for stage in StageService(db).list_stages(festival_id)]


@router.post("", response_model=StageResponse, status_code=201)
def create_stage(payload: StageCreateRequest, db: Session = Depends(get_db)):
    # Validation/normalisation du domaine à la frontière entrante.
    stage_create_to_domain(payload)
    try:
        return stage_to_response(StageService(db).create_stage(payload))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
