"""Routeur FastAPI pour les festivals."""

from fastapi import APIRouter, Depends

from app.adapters.inbound.api.dependencies import get_festival_service
from app.adapters.inbound.api.dtos import (
    FestivalCreateRequest,
    FestivalResponse,
)
from app.adapters.inbound.api.mappers import (
    festival_create_to_domain,
    festival_to_response,
)
from app.ports.inbound.festival_inbound_port import FestivalInboundPort

router = APIRouter(prefix="/festivals", tags=["festivals"])


@router.get("", response_model=list[FestivalResponse])
def list_festivals(
    service: FestivalInboundPort = Depends(get_festival_service),
):
    return [
        festival_to_response(festival)
        for festival in service.list_festivals()
    ]


@router.post("", response_model=FestivalResponse, status_code=201)
def create_festival(
    payload: FestivalCreateRequest,
    service: FestivalInboundPort = Depends(get_festival_service),
):
    festival = festival_create_to_domain(payload)
    created = service.create_festival(festival)
    return festival_to_response(created)


@router.post("/{festival_id}/publish", response_model=FestivalResponse)
def publish_festival(
    festival_id: int,
    service: FestivalInboundPort = Depends(get_festival_service),
):
    published = service.publish_festival(festival_id)
    return festival_to_response(published)
