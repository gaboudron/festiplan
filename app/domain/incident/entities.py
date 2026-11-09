from dataclasses import dataclass, field
from datetime import datetime
from app.domain.exceptions import InvalidIncidentMessageError
from app.utils.datetime_helpers import ensure_utc, utc_now

@dataclass
class Incident:
    id: int | None
    concert_id: int
    description: str
    occurred_at: datetime = field(default_factory=utc_now)
    resolved: bool = False


    def __post_init__(self):
        # Convention du domaine : la date de survenue est en UTC aware.
        self.occurred_at = ensure_utc(self.occurred_at)
        # La description ne doit pas être vide
        if not self.description.strip():
            raise InvalidIncidentMessageError()


    def mark_resolved(self) -> None:
        self.resolved = True