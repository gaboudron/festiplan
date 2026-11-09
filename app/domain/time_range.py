from dataclasses import dataclass
from datetime import datetime
from app.domain.exceptions import InvalidTimeRangeError
from app.utils.datetime_helpers import ensure_utc

@dataclass(frozen=True)
class TimeRange:
    start: datetime
    end: datetime

    def __post_init__(self):
        # Convention du domaine : tous les créneaux sont en UTC aware.
        object.__setattr__(self, "start", ensure_utc(self.start))
        object.__setattr__(self, "end", ensure_utc(self.end))
        if self.end <= self.start:
            raise InvalidTimeRangeError()


    def overlaps_with(self, other: "TimeRange") -> bool:
        """Vérifie si deux créneaux temporels se chevauchent."""
        return self.start < other.end and self.end > other.start


    def is_within(self, boundary: "TimeRange") -> bool:
        """Vérifie que ce créneau est entièrement inclus dans un créneau parent (ex: le festival)."""
        return self.start >= boundary.start and self.end <= boundary.end
