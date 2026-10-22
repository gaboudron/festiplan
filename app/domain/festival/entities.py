from dataclasses import dataclass, field
from app.domain.time_range import TimeRange
from app.domain.equipments import EquipmentSet
from app.domain.festival.value_objects import FestivalStatus
from app.domain.exceptions import FestivalAlreadyPublishedError

@dataclass
class Stage:
    id         : int | None
    festival_id: int
    name       : str
    capacity   : int
    available_equipment: EquipmentSet


@dataclass
class Festival:
    id        : int | None
    name      : str
    location  : str
    time_range: TimeRange
    status: FestivalStatus = FestivalStatus.PREPARATION
    stages: list[Stage]    = field(default_factory=list)


    @property
    def is_published(self) -> bool:
        return self.status == FestivalStatus.PUBLISHED


    def publish(self) -> None:
        """Fait passer le festival en statut publié."""
        self.status = FestivalStatus.PUBLISHED


    def contains_time_range(self, range: TimeRange) -> bool:
        """Vérifie qu'un créneau est inclus dans les dates du festival."""
        return range.is_within(self.time_range)
