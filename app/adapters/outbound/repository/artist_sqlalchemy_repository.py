from sqlalchemy.orm import Session
from app.adapters.outbound.repository.mappers.artist_mapper import (
    ArtistMapper,
)
from app.domain.artist.entities import Artist
from app.adapters.outbound.repository.models import Artist as ArtistORM
from app.ports.outbound.repository.artist_repository_outbound_port import (
    ArtistRepositoryOutboundPort,
)


class ArtistSqlAlchemyRepository(ArtistRepositoryOutboundPort):
    def __init__(self, db: Session):
        self.db = db

    def get(self, artist_id: int) -> Artist | None:
        row = self.db.query(ArtistORM).filter(ArtistORM.id == artist_id).first()
        return ArtistMapper.to_domain(row) if row else None

    def list_all(self) -> list[Artist]:
        rows = self.db.query(ArtistORM).order_by(ArtistORM.name).all()
        return [ArtistMapper.to_domain(row) for row in rows]

    def save(self, artist: Artist) -> Artist:
        if artist.id is not None:
            existing_orm = (
                self.db.query(ArtistORM)
                .filter(ArtistORM.id == artist.id)
                .first()
            )
            if existing_orm is not None:
                orm = ArtistMapper.to_orm(artist, existing_orm=existing_orm)
                self.db.commit()
                self.db.refresh(orm)
                return ArtistMapper.to_domain(orm)

        orm = ArtistMapper.to_orm(artist)
        self.db.add(orm)
        self.db.commit()
        self.db.refresh(orm)
        return ArtistMapper.to_domain(orm)

