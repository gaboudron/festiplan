from sqlalchemy.orm import Session

from app.models import Festival as FestivalModel
from app.domain.festival.entities import Festival
from app.adapters.out.persistence.mappers import (
    festival_to_domain,
    festival_to_model,
)


class SqlAlchemyFestivalRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, festival_id: int) -> Festival | None:
        model = self.db.get(FestivalModel, festival_id)

        if model is None:
            return None

        return festival_to_domain(model)

    def get_all(self) -> list[Festival]:
        models = (
            self.db.query(FestivalModel)
            .order_by(FestivalModel.id)
            .all()
        )

        return [festival_to_domain(model) for model in models]

    def save(self, festival: Festival) -> Festival:
        model = (
            self.db.get(FestivalModel, festival.id)
            if festival.id is not None
            else None
        )

        if model is None:
            model = festival_to_model(festival)
            self.db.add(model)
        else:
            updated = festival_to_model(festival)

            model.name = updated.name
            model.location = updated.location
            model.start_date = updated.start_date
            model.end_date = updated.end_date
            model.status = updated.status

        self.db.flush()

        return festival_to_domain(model)