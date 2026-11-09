from app.models import Incident as IncidentORM
from app.domain.incident.entities import Incident


class IncidentMapper:
    @staticmethod
    def to_domain(orm: IncidentORM) -> Incident:
        return Incident(
            id=orm.id,
            concert_id=orm.concert_id,
            description=orm.description,
            occurred_at=orm.occurred_at,
            resolved=orm.resolved,
        )

    @staticmethod
    def to_orm(
        entity: Incident, existing_orm: IncidentORM | None = None
    ) -> IncidentORM:
        if existing_orm is None:
            return IncidentORM(
                id=entity.id,
                concert_id=entity.concert_id,
                description=entity.description,
                occurred_at=entity.occurred_at,
                resolved=entity.resolved,
            )
        existing_orm.concert_id = entity.concert_id
        existing_orm.description = entity.description
        existing_orm.occurred_at = entity.occurred_at
        existing_orm.resolved = entity.resolved
        return existing_orm

