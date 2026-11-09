"""Mappings DTO ↔ domaine pour les scènes."""

from app.adapters.inbound.api.dtos import StageCreateRequest, StageResponse
from app.adapters.inbound.api.mappers.common import (
    equipment_items,
    require_persisted_id,
)
from app.domain.equipments import EquipmentSet
from app.domain.festival.entities import Stage


def stage_create_to_domain(dto: StageCreateRequest) -> Stage:
    return Stage(
        id=None,
        festival_id=dto.festival_id,
        name=dto.name,
        capacity=dto.capacity,
        available_equipment=EquipmentSet.from_list(dto.available_equipment),
    )


def stage_to_response(stage: Stage) -> StageResponse:
    """Mappe une scène du domaine vers le DTO de réponse."""
    return StageResponse(
        id=require_persisted_id(stage.id),
        festival_id=stage.festival_id,
        name=stage.name,
        capacity=stage.capacity,
        available_equipment=equipment_items(stage.available_equipment),
    )
