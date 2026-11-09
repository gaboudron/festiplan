"""Mappings DTO ↔ domaine pour les concerts."""

from app.adapters.inbound.api.dtos import (
    ConcertCreateRequest,
    ConcertRescheduleRequest,
    ConcertResponse,
)
from app.adapters.inbound.api.mappers.common import (
    require_persisted_id,
    resolve_time_range,
    status_value,
)
from app.domain.concert.entities import Concert
from app.domain.concert.value_object import ConcertStatus
from app.domain.time_range import TimeRange


def concert_create_to_domain(dto: ConcertCreateRequest) -> Concert:
    return Concert(
        id=None,
        festival_id=dto.festival_id,
        artist_id=dto.artist_id,
        stage_id=dto.stage_id,
        time_range=TimeRange(start=dto.start_time, end=dto.end_time),
        status=ConcertStatus.SCHEDULED,
    )


def concert_reschedule_to_time_range(
    dto: ConcertRescheduleRequest,
) -> TimeRange:
    """Construit le nouveau créneau à partir du DTO."""
    return TimeRange(start=dto.start_time, end=dto.end_time)


def concert_reschedule_to_domain(
    concert: Concert, dto: ConcertRescheduleRequest
) -> Concert:
    """Applique la reprogrammation au concert.

    ``dto.stage_id`` à ``None`` conserve la scène actuelle.
    """
    concert.reschedule(
        new_time_range=concert_reschedule_to_time_range(dto),
        new_stage_id=dto.stage_id,
    )
    return concert


def concert_to_response(concert: Concert) -> ConcertResponse:
    """Mappe un concert du domaine vers le DTO de réponse."""
    start_time, end_time = resolve_time_range(concert)
    return ConcertResponse(
        id=require_persisted_id(concert.id),
        festival_id=concert.festival_id,
        artist_id=concert.artist_id,
        stage_id=concert.stage_id,
        start_time=start_time,
        end_time=end_time,
        status=status_value(concert.status),
    )
