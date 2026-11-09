"""Point d'entrée public des DTO de l'adaptateur entrant.

Les DTO sont segmentés par domaine métier pour garder chaque fichier court
et faciliter la navigation. Ils portent la validation et la normalisation
UTC à la frontière HTTP, sans contenir de logique métier.
"""

from app.adapters.inbound.api.dtos.artist_dtos import (
    ArtistCreateRequest,
    ArtistResponse,
)
from app.adapters.inbound.api.dtos.concert_dtos import (
    ConcertCreateRequest,
    ConcertRescheduleRequest,
    ConcertResponse,
)
from app.adapters.inbound.api.dtos.festival_dtos import (
    FestivalCreateRequest,
    FestivalResponse,
)
from app.adapters.inbound.api.dtos.incident_dtos import (
    IncidentCreateRequest,
    IncidentResponse,
)
from app.adapters.inbound.api.dtos.stage_dtos import (
    StageCreateRequest,
    StageResponse,
)

__all__ = [
    "ArtistCreateRequest",
    "ArtistResponse",
    "ConcertCreateRequest",
    "ConcertRescheduleRequest",
    "ConcertResponse",
    "FestivalCreateRequest",
    "FestivalResponse",
    "IncidentCreateRequest",
    "IncidentResponse",
    "StageCreateRequest",
    "StageResponse",
]
