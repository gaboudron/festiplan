from sqlalchemy.orm import Session

from app.models import Artist as ArtistModel
from app.domain.artist.entities import Artist
from app.adapters.out.persistence.mappers import (
    artist_to_domain,
    artist_to_model,
)


class SqlAlchemyArtistRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, artist_id: int) -> Artist | None:
        model = self.db.get(ArtistModel, artist_id)

        if model is None:
            return None

        return artist_to_domain(model)

    def get_all(self) -> list[Artist]:
        models = (
            self.db.query(ArtistModel)
            .order_by(ArtistModel.name)
            .all()
        )

        return [artist_to_domain(model) for model in models]

    def save(self, artist: Artist) -> Artist:
        model = (
            self.db.get(ArtistModel, artist.id)
            if artist.id is not None
            else None
        )

        if model is None:
            model = artist_to_model(artist)
            self.db.add(model)
        else:
            model.name = artist.name
            model.genre = artist.genre
            model.required_equipment = (
                artist_to_model(artist).required_equipment
            )

        self.db.flush()

        return artist_to_domain(model)