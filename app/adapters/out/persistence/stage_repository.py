from sqlalchemy.orm import Session

from app.models import Stage as StageModel
from app.domain.festival.entities import Stage
from app.adapters.out.persistence.mappers import (
    stage_to_domain,
    stage_to_model,
)


class SqlAlchemyStageRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, stage_id: int) -> Stage | None:
        model = self.db.get(StageModel, stage_id)

        if model is None:
            return None

        return stage_to_domain(model)

    def get_for_festival(self, festival_id: int) -> list[Stage]:
        models = (
            self.db.query(StageModel)
            .filter(StageModel.festival_id == festival_id)
            .order_by(StageModel.id)
            .all()
        )

        return [stage_to_domain(model) for model in models]

    def save(self, stage: Stage) -> Stage:
        model = (
            self.db.get(StageModel, stage.id)
            if stage.id is not None
            else None
        )

        if model is None:
            model = stage_to_model(stage)
            self.db.add(model)
        else:
            updated = stage_to_model(stage)

            model.festival_id = updated.festival_id
            model.name = updated.name
            model.capacity = updated.capacity
            model.available_equipment = updated.available_equipment

        self.db.flush()

        return stage_to_domain(model)