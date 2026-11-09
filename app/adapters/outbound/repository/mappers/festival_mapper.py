from app.adapters.outbound.repository.mappers.stage_mapper import StageMapper
from app.adapters.outbound.repository.models import Festival as FestivalORM
from app.domain.festival.entities import Festival
from app.domain.festival.value_objects import FestivalStatus
from app.domain.time_range import TimeRange


class FestivalMapper:
    @staticmethod
    def to_domain(orm: FestivalORM) -> Festival:
        stages = (
            [StageMapper.to_domain(s) for s in orm.stages]
            if orm.stages
            else []
        )
        return Festival(
            id=orm.id,
            name=orm.name,
            location=orm.location,
            time_range=TimeRange(start=orm.start_date, end=orm.end_date),
            status=FestivalStatus(orm.status),
            stages=stages,
        )

    @staticmethod
    def to_orm(
        entity: Festival, existing_orm: FestivalORM | None = None
    ) -> FestivalORM:
        if existing_orm is None:
            return FestivalORM(
                id=entity.id,
                name=entity.name,
                location=entity.location,
                start_date=entity.time_range.start,
                end_date=entity.time_range.end,
                status=entity.status.value,
            )
        existing_orm.name = entity.name
        existing_orm.location = entity.location
        existing_orm.start_date = entity.time_range.start
        existing_orm.end_date = entity.time_range.end
        existing_orm.status = entity.status.value
        return existing_orm

