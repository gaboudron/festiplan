from app.adapters.outbound.repository.mappers.equipment_mapper import (
    EquipmentMapper,
)
from app.models import Artist as ArtistORM
from app.domain.artist.entities import Artist


class ArtistMapper:
    @staticmethod
    def to_domain(orm: ArtistORM) -> Artist:
        return Artist(
            id=orm.id,
            name=orm.name,
            genre=orm.genre,
            required_equipment=EquipmentMapper.to_domain(
                orm.required_equipment
            ),
        )

    @staticmethod
    def to_orm(
        entity: Artist, existing_orm: ArtistORM | None = None
    ) -> ArtistORM:
        equipment_str = EquipmentMapper.to_orm(entity.required_equipment)
        if existing_orm is None:
            return ArtistORM(
                id=entity.id,
                name=entity.name,
                genre=entity.genre,
                required_equipment=equipment_str,
            )
        existing_orm.name = entity.name
        existing_orm.genre = entity.genre
        existing_orm.required_equipment = equipment_str
        return existing_orm

