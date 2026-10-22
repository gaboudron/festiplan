from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Incident:
    id: int | None
    concert_id: int
    description: str
    occurred_at: datetime = field(default_factory=datetime.utcnow)
    resolved: bool = False


    def mark_resolved(self) -> None:
        self.resolved = True