"""Routeur FastAPI pour les scènes."""

from fastapi import APIRouter, Depends

from app.adapters.inbound.api.dependencies import get_stage_service
from app.adapters.inbound.api.dtos import StageCreateRequest, StageResponse
from app.adapters.inbound.api.mappers import (
    stage_create_to_domain,
    stage_to_response,
)
from app.ports.inbound.stage_inbound_port import StageInboundPort

router = APIRouter(prefix="/stages", tags=["stages"])


@router.get("", response_model=list[StageResponse])
def list_stages(
    festival_id: int,
    service: StageInboundPort = Depends(get_stage_service),
):
    return [stage_to_response(stage) for stage in service.list_stages(festival_id)]


@router.post("", response_model=StageResponse, status_code=201)
def create_stage(
    payload: StageCreateRequest,
    service: StageInboundPort = Depends(get_stage_service),
):
    stage = stage_create_to_domain(payload)
    created = service.create_stage(stage)
    return stage_to_response(created)
