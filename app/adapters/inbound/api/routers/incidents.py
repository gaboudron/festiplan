"""Routeur FastAPI pour les incidents."""

from fastapi import APIRouter, Depends

from app.adapters.inbound.api.dependencies import get_incident_service
from app.adapters.inbound.api.dtos import (
    IncidentCreateRequest,
    IncidentResponse,
)
from app.adapters.inbound.api.mappers import (
    incident_create_to_domain,
    incident_to_response,
)
from app.ports.inbound.incident_inbound_port import IncidentInboundPort

router = APIRouter(prefix="/incidents", tags=["incidents"])


@router.post("", response_model=IncidentResponse, status_code=201)
def create_incident(
    payload: IncidentCreateRequest,
    service: IncidentInboundPort = Depends(get_incident_service),
):
    incident = incident_create_to_domain(payload)
    created = service.declare_incident(incident)
    return incident_to_response(created)


@router.patch("/{incident_id}/resolve", response_model=IncidentResponse)
@router.post("/{incident_id}/resolve", response_model=IncidentResponse)
def resolve_incident(
    incident_id: int,
    service: IncidentInboundPort = Depends(get_incident_service),
):
    resolved = service.resolve_incident(incident_id)
    return incident_to_response(resolved)


@router.get("", response_model=list[IncidentResponse])
def list_incidents(
    concert_id: int | None = None,
    service: IncidentInboundPort = Depends(get_incident_service),
):
    return [
        incident_to_response(incident)
        for incident in service.list_incidents(concert_id)
    ]
