from sqlalchemy.orm import Session
from app.adapters.outbound.repository.mappers.incident_mapper import (
    IncidentMapper,
)
from app.domain.incident.entities import Incident
from app.adapters.outbound.repository.models import Incident as IncidentORM
from app.ports.outbound.repository.incident_repository_outbound_port import (
    IncidentRepositoryOutboundPort,
)


class IncidentSqlAlchemyRepository(IncidentRepositoryOutboundPort):
    def __init__(self, db: Session):
        self.db = db

    def get(self, incident_id: int) -> Incident | None:
        row = (
            self.db.query(IncidentORM)
            .filter(IncidentORM.id == incident_id)
            .first()
        )
        return IncidentMapper.to_domain(row) if row else None

    def list_all(self) -> list[Incident]:
        rows = (
            self.db.query(IncidentORM)
            .order_by(IncidentORM.occurred_at.desc())
            .all()
        )
        return [IncidentMapper.to_domain(row) for row in rows]

    def list_by_concert_id(self, concert_id: int) -> list[Incident]:
        rows = (
            self.db.query(IncidentORM)
            .filter(IncidentORM.concert_id == concert_id)
            .order_by(IncidentORM.occurred_at.desc())
            .all()
        )
        return [IncidentMapper.to_domain(row) for row in rows]

    def save(self, incident: Incident) -> Incident:
        if incident.id is not None:
            existing_orm = (
                self.db.query(IncidentORM)
                .filter(IncidentORM.id == incident.id)
                .first()
            )
            if existing_orm is not None:
                orm = IncidentMapper.to_orm(incident, existing_orm=existing_orm)
                self.db.flush()
                return IncidentMapper.to_domain(orm)

        orm = IncidentMapper.to_orm(incident)
        self.db.add(orm)
        self.db.flush()
        return IncidentMapper.to_domain(orm)

