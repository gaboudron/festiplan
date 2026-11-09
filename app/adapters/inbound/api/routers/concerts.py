"""Routeur FastAPI pour les concerts."""

from fastapi import APIRouter, Depends

from app.adapters.inbound.api.dependencies import get_concert_service
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
from app.ports.inbound.concert_inbound_port import ConcertInboundPort

router = APIRouter(prefix="/concerts", tags=["concerts"])


@router.get("", response_model=list[ConcertResponse])
def list_concerts(
    festival_id: int,
    service: ConcertInboundPort = Depends(get_concert_service),
):
    return [
        concert_to_response(concert)
        for concert in service.list_concerts(festival_id)
    ]


@router.get("/{concert_id}", response_model=ConcertResponse)
def get_concert(
    concert_id: int,
    service: ConcertInboundPort = Depends(get_concert_service),
):
    return concert_to_response(service.get_concert(concert_id))


@router.post("", response_model=ConcertResponse, status_code=201)
def create_concert(
    payload: ConcertCreateRequest,
    service: ConcertInboundPort = Depends(get_concert_service),
):
    concert = concert_create_to_domain(payload)
    created = service.create_concert(concert)
    return concert_to_response(created)


@router.patch("/{concert_id}/reschedule", response_model=ConcertResponse)
def reschedule_concert(
    concert_id: int,
    payload: ConcertRescheduleRequest,
    service: ConcertInboundPort = Depends(get_concert_service),
):
    new_time_range = concert_reschedule_to_time_range(payload)
    rescheduled = service.reschedule_concert(
        concert_id=concert_id,
        new_time_range=new_time_range,
        new_stage_id=payload.stage_id,
    )
    return concert_to_response(rescheduled)


@router.post("/{concert_id}/cancel", response_model=ConcertResponse)
def cancel_concert(
    concert_id: int,
    service: ConcertInboundPort = Depends(get_concert_service),
):
    cancelled = service.cancel_concert(concert_id)
    return concert_to_response(cancelled)


@router.get("/schedule/{festival_id}", response_model=list[ConcertResponse])
def get_schedule(
    festival_id: int,
    service: ConcertInboundPort = Depends(get_concert_service),
):
    return [
        concert_to_response(concert)
        for concert in service.get_schedule(festival_id)
    ]
