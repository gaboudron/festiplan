"""Règles d'état du festival (décision 7.B : services de domaine)."""

from app.domain.exceptions import (
    ConcertOutsideFestivalDatesError,
    FestivalAlreadyPublishedError,
    StageDoesNotBelongToFestivalError,
)
from app.domain.festival.entities import Festival, Stage
from app.domain.time_range import TimeRange


class FestivalPolicy:
    """Invariants d'état vérifiés avant toute modification du planning."""

    @staticmethod
    def ensure_not_published(festival: Festival) -> None:
        """Un planning publié n'est plus modifiable (règle R7)."""
        if festival.is_published:
            raise FestivalAlreadyPublishedError()

    @staticmethod
    def ensure_concert_within_dates(
        festival: Festival, time_range: TimeRange
    ) -> None:
        """Un concert doit rester dans les dates du festival."""
        if not festival.contains_time_range(time_range):
            raise ConcertOutsideFestivalDatesError()

    @staticmethod
    def ensure_stage_belongs_to_festival(
        festival: Festival, stage: Stage
    ) -> None:
        """La scène d'un concert doit appartenir au même festival."""
        if stage.festival_id != festival.id:
            raise StageDoesNotBelongToFestivalError()
