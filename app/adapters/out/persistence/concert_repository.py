from sqlalchemy.orm import Session

from app.models import Concert as ConcertModel
from app.domain.concert.entities import Concert
from app.adapters.out.persistence.mappers import (
    concert_to_domain,
    concert_to_model,
)


class SqlAlchemyConcertRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, concert_id: int) -> Concert | None:
        model = self.db.get(ConcertModel, concert_id)

        if model is None:
            return None

        return concert_to_domain(model)

    def get_for_festival(self, festival_id: int) -> list[Concert]:
        models = (
            self.db.query(ConcertModel)
            .filter(ConcertModel.festival_id == festival_id)
            .order_by(ConcertModel.start_time)
            .all()
        )

        return [concert_to_domain(model) for model in models]

    def save(self, concert: Concert) -> Concert:
        model = (
            self.db.get(ConcertModel, concert.id)
            if concert.id is not None
            else None
        )

        if model is None:
            model = concert_to_model(concert)
            self.db.add(model)
        else:
            updated = concert_to_model(concert)

            model.festival_id = updated.festival_id
            model.artist_id = updated.artist_id
            model.stage_id = updated.stage_id
            model.start_time = updated.start_time
            model.end_time = updated.end_time
            model.status = updated.status

        self.db.flush()

        return concert_to_domain(model)