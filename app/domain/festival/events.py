from dataclasses import dataclass, field
from datetime import datetime

@dataclass(frozen=True)
class FestivalPublishedEvent:
    """Événement déclenché lorsque le festival est rendu public."""
    festival_id  : int
    festival_name: str
    occurred_at  : datetime = field(default_factory=datetime.utcnow)

@dataclass(frozen=True)
class FestivalCancelledEvent:
    """Événement déclenché lorsque le festival est annulé."""
    festival_id  : int
    festival_name: str
    occurred_at  : datetime = field(default_factory=datetime.utcnow)
    