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


    def reschedule(self, new_time_range: TimeRange, new_stage_id: int | None = None) -> None:
        """Reprogramme le concert à un nouvel horaire et, si fourni, sur une nouvelle scène."""
        self.time_range = new_time_range
        if new_stage_id is not None:
            self.stage_id = new_stage_id


    def cancel(self) -> None:
        """Annule le concert."""
        self.status = ConcertStatus.CANCELLED


    @property
    def is_cancelled(self) -> bool:
        return self.status == ConcertStatus.CANCELLED
