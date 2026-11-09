from dataclasses import dataclass, field
from datetime import datetime, timezone
from app.domain.exceptions import InvalidIncidentMessageError

@dataclass
class Incident:
    id: int | None
    concert_id: int
    description: str
    occurred_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    resolved: bool = False


    def __post_init__(self):
        # La description ne doit pas être vide
        if not self.description.strip():
            raise InvalidIncidentMessageError()


    def mark_resolved(self) -> None:
        self.resolved = True