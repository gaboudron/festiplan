from app.domain.concert.entities import Concert
from app.domain.time_range import TimeRange
from app.domain.exceptions import StageOccupiedError, ArtistAlreadyScheduledError

class SchedulingConflictChecker:
    @staticmethod
    def check_conflicts(
        existing_concerts: list[Concert],
        stage_id: int,
        artist_id: int,
        time_range: TimeRange,
        exclude_concert_id: int | None = None,
    ) -> None:
        for concert in existing_concerts:
            if exclude_concert_id is not None and concert.id == exclude_concert_id:
                continue
            if concert.is_cancelled:
                continue

            if time_range.overlaps_with(concert.time_range):
                if concert.stage_id == stage_id:
                    raise StageOccupiedError()
                if concert.artist_id == artist_id:
                    raise ArtistAlreadyScheduledError()
