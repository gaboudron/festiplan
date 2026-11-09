from app.adapters.outbound.repository.mappers.equipment_mapper import (
    EquipmentMapper,
)
from app.models import Stage as StageORM
from app.domain.festival.entities import Stage


class StageMapper:
    @staticmethod
    def to_domain(orm: StageORM) -> Stage:
        return Stage(
            id=orm.id,
            festival_id=orm.festival_id,
            name=orm.name,
            capacity=orm.capacity,
            available_equipment=EquipmentMapper.to_domain(
                orm.available_equipment
            ),
        )

    @staticmethod
    def to_orm(entity: Stage, existing_orm: StageORM | None = None) -> StageORM:
        equipment_str = EquipmentMapper.to_orm(entity.available_equipment)
        if existing_orm is None:
            return StageORM(
                id=entity.id,
                festival_id=entity.festival_id,
                name=entity.name,
                capacity=entity.capacity,
                available_equipment=equipment_str,
            )
        existing_orm.festival_id = entity.festival_id
        existing_orm.name = entity.name
        existing_orm.capacity = entity.capacity
        existing_orm.available_equipment = equipment_str
        return existing_orm

