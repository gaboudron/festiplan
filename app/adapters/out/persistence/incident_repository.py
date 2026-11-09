from sqlalchemy.orm import Session

from app.models import Incident as IncidentModel
from app.domain.incident.entities import Incident
from app.adapters.out.persistence.mappers import (
    incident_to_domain,
    incident_to_model,
)


class SqlAlchemyIncidentRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, incident_id: int) -> Incident | None:
        model = self.db.get(IncidentModel, incident_id)

        if model is None:
            return None

        return incident_to_domain(model)

    def get_for_concert(self, concert_id: int) -> list[Incident]:
        models = (
            self.db.query(IncidentModel)
            .filter(IncidentModel.concert_id == concert_id)
            .order_by(IncidentModel.occurred_at)
            .all()
        )

        return [incident_to_domain(model) for model in models]

    def save(self, incident: Incident) -> Incident:
        model = (
            self.db.get(IncidentModel, incident.id)
            if incident.id is not None
            else None
        )

        if model is None:
            model = incident_to_model(incident)
            self.db.add(model)
        else:
            updated = incident_to_model(incident)

            model.concert_id = updated.concert_id
            model.description = updated.description
            model.occurred_at = updated.occurred_at
            model.resolved = updated.resolved

        self.db.flush()

        return incident_to_domain(model)