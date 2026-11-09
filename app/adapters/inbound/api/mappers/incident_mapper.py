"""Mappings DTO ↔ domaine pour les incidents."""

from app.adapters.inbound.api.dtos import (
    IncidentCreateRequest,
    IncidentResponse,
)
from app.adapters.inbound.api.mappers.common import require_persisted_id
from app.domain.incident.entities import Incident


def incident_create_to_domain(dto: IncidentCreateRequest) -> Incident:
    if dto.occurred_at is None:
        return Incident(
            id=None,
            concert_id=dto.concert_id,
            description=dto.description,
        )
    return Incident(
        id=None,
        concert_id=dto.concert_id,
        description=dto.description,
        occurred_at=dto.occurred_at,
    )


def incident_to_response(incident: Incident) -> IncidentResponse:
    """Mappe un incident du domaine vers le DTO de réponse."""
    return IncidentResponse(
        id=require_persisted_id(incident.id),
        concert_id=incident.concert_id,
        description=incident.description,
        occurred_at=incident.occurred_at,
        resolved=incident.resolved,
    )
