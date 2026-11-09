from dataclasses import dataclass
from app.domain.time_range import TimeRange
from app.domain.concert.value_object import ConcertStatus

@dataclass
class Concert: 
    id: int | None
    festival_id: int
    artist_id: int
    stage_id: int
    time_range: TimeRange
    status: ConcertStatus = ConcertStatus.SCHEDULED


    def reschedule(self, new_time_range: TimeRange) -> None:
        """Reprogramme le concert à un nouvel horaire."""
        self.time_range = new_time_range


    def cancel(self) -> None:
        """Annule le concert."""
        self.status = ConcertStatus.CANCELLED


    @property
    def is_cancelled(self) -> bool:
        return self.status == ConcertStatus.CANCELLED
