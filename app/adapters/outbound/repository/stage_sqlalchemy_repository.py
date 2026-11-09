from sqlalchemy.orm import Session
from app.adapters.outbound.repository.mappers.stage_mapper import StageMapper
from app.domain.festival.entities import Stage
from app.adapters.outbound.repository.models import Stage as StageORM
from app.ports.outbound.repository.stage_repository_outbound_port import (
    StageRepositoryOutboundPort,
)


class StageSqlAlchemyRepository(StageRepositoryOutboundPort):
    def __init__(self, db: Session):
        self.db = db

    def get(self, stage_id: int) -> Stage | None:
        row = self.db.query(StageORM).filter(StageORM.id == stage_id).first()
        return StageMapper.to_domain(row) if row else None

    def list_by_festival_id(self, festival_id: int) -> list[Stage]:
        rows = (
            self.db.query(StageORM)
            .filter(StageORM.festival_id == festival_id)
            .order_by(StageORM.id)
            .all()
        )
        return [StageMapper.to_domain(row) for row in rows]

    def save(self, stage: Stage) -> Stage:
        if stage.id is not None:
            existing_orm = (
                self.db.query(StageORM)
                .filter(StageORM.id == stage.id)
                .first()
            )
            if existing_orm is not None:
                orm = StageMapper.to_orm(stage, existing_orm=existing_orm)
                self.db.commit()
                self.db.refresh(orm)
                return StageMapper.to_domain(orm)

        orm = StageMapper.to_orm(stage)
        self.db.add(orm)
        self.db.commit()
        self.db.refresh(orm)
        return StageMapper.to_domain(orm)

