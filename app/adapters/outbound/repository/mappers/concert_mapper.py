from app.models import Concert as ConcertORM
from app.domain.concert.entities import Concert
from app.domain.concert.value_object import ConcertStatus
from app.domain.time_range import TimeRange


class ConcertMapper:
    @staticmethod
    def to_domain(orm: ConcertORM) -> Concert:
        return Concert(
            id=orm.id,
            festival_id=orm.festival_id,
            artist_id=orm.artist_id,
            stage_id=orm.stage_id,
            time_range=TimeRange(start=orm.start_time, end=orm.end_time),
            status=ConcertStatus(orm.status),
        )

    @staticmethod
    def to_orm(
        entity: Concert, existing_orm: ConcertORM | None = None
    ) -> ConcertORM:
        if existing_orm is None:
            return ConcertORM(
                id=entity.id,
                festival_id=entity.festival_id,
                artist_id=entity.artist_id,
                stage_id=entity.stage_id,
                start_time=entity.time_range.start,
                end_time=entity.time_range.end,
                status=entity.status.value,
            )
        existing_orm.festival_id = entity.festival_id
        existing_orm.artist_id = entity.artist_id
        existing_orm.stage_id = entity.stage_id
        existing_orm.start_time = entity.time_range.start
        existing_orm.end_time = entity.time_range.end
        existing_orm.status = entity.status.value
        return existing_orm

