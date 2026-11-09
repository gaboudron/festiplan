from sqlalchemy.orm import Session
from app.adapters.outbound.repository.mappers.festival_mapper import (
    FestivalMapper,
)
from app.domain.festival.entities import Festival
from app.models import Festival as FestivalORM
from app.ports.outbound.repository.festival_repository_outbound_port import (
    FestivalRepositoryOutboundPort,
)


class FestivalSqlAlchemyRepository(FestivalRepositoryOutboundPort):
    def __init__(self, db: Session):
        self.db = db

    def get(self, festival_id: int) -> Festival | None:
        row = (
            self.db.query(FestivalORM)
            .filter(FestivalORM.id == festival_id)
            .first()
        )
        return FestivalMapper.to_domain(row) if row else None

    def list_all(self) -> list[Festival]:
        rows = self.db.query(FestivalORM).order_by(FestivalORM.id).all()
        return [FestivalMapper.to_domain(row) for row in rows]

    def save(self, festival: Festival) -> Festival:
        if festival.id is not None:
            existing_orm = (
                self.db.query(FestivalORM)
                .filter(FestivalORM.id == festival.id)
                .first()
            )
            if existing_orm is not None:
                orm = FestivalMapper.to_orm(festival, existing_orm=existing_orm)
                self.db.commit()
                self.db.refresh(orm)
                return FestivalMapper.to_domain(orm)

        orm = FestivalMapper.to_orm(festival)
        self.db.add(orm)
        self.db.commit()
        self.db.refresh(orm)
        return FestivalMapper.to_domain(orm)

