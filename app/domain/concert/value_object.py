from enum import Enum

class ConcertStatus(str, Enum):
    SCHEDULED = "scheduled"
    CANCELLED = "cancelled"