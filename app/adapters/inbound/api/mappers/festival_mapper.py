"""Mappings DTO ↔ domaine pour les festivals."""

from app.adapters.inbound.api.dtos import (
    FestivalCreateRequest,
    FestivalResponse,
)
from app.adapters.inbound.api.mappers.common import (
    require_persisted_id,
    resolve_time_range,
    status_value,
)
from app.domain.festival.entities import Festival
from app.domain.festival.value_objects import FestivalStatus
from app.domain.time_range import TimeRange


def festival_create_to_domain(dto: FestivalCreateRequest) -> Festival:
    return Festival(
        id=None,
        name=dto.name,
        location=dto.location,
        time_range=TimeRange(start=dto.start_date, end=dto.end_date),
        status=FestivalStatus.PREPARATION,
    )


def festival_to_response(festival: Festival) -> FestivalResponse:
    """Mappe un festival du domaine vers le DTO de réponse."""
    start_date, end_date = resolve_time_range(festival)
    return FestivalResponse(
        id=require_persisted_id(festival.id),
        name=festival.name,
        location=festival.location,
        start_date=start_date,
        end_date=end_date,
        status=status_value(festival.status),
    )
