from sqlalchemy.orm import Session
from app.adapters.outbound.repository.mappers.concert_mapper import (
    ConcertMapper,
)
from app.domain.concert.entities import Concert
from app.models import Concert as ConcertORM
from app.ports.outbound.repository.concert_repository_outbound_port import (
    ConcertRepositoryOutboundPort,
)


class ConcertSqlAlchemyRepository(ConcertRepositoryOutboundPort):
    def __init__(self, db: Session):
        self.db = db

    def get(self, concert_id: int) -> Concert | None:
        row = (
            self.db.query(ConcertORM)
            .filter(ConcertORM.id == concert_id)
            .first()
        )
        return ConcertMapper.to_domain(row) if row else None

    def list_by_festival_id(self, festival_id: int) -> list[Concert]:
        rows = (
            self.db.query(ConcertORM)
            .filter(ConcertORM.festival_id == festival_id)
            .order_by(ConcertORM.start_time)
            .all()
        )
        return [ConcertMapper.to_domain(row) for row in rows]

    def save(self, concert: Concert) -> Concert:
        if concert.id is not None:
            existing_orm = (
                self.db.query(ConcertORM)
                .filter(ConcertORM.id == concert.id)
                .first()
            )
            if existing_orm is not None:
                orm = ConcertMapper.to_orm(concert, existing_orm=existing_orm)
                self.db.commit()
                self.db.refresh(orm)
                return ConcertMapper.to_domain(orm)

        orm = ConcertMapper.to_orm(concert)
        self.db.add(orm)
        self.db.commit()
        self.db.refresh(orm)
        return ConcertMapper.to_domain(orm)

