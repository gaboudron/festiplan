from dataclasses import dataclass, field
from datetime import datetime
from app.domain.time_range import TimeRange

@dataclass(frozen=True)
class ConcertRescheduledEvent:
    """Événement émis lorsqu'un concert a été reprogrammé."""
    concert_id    : int
    festival_id   : int
    new_time_range: TimeRange
    occurred_at   : datetime = field(default_factory=datetime.utcnow)


@dataclass(frozen=True)
class ConcertCancelledEvent:
    """Événement émis lorsqu'un concert a été annulé."""
    concert_id : int
    festival_id: int
    occurred_at: datetime = field(default_factory=datetime.utcnow)