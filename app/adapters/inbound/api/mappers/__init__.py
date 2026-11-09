"""Point d'entrée public des mappings DTO ↔ domaine.

Les implémentations sont segmentées par domaine métier pour garder chaque
fichier court et faciliter la navigation. Les mappers ne manipulent que des
entités du domaine : la compatibilité transitoire avec les lignes ORM a été
retirée, ``common.py`` ne contient plus que des helpers de présentation.
"""

from app.adapters.inbound.api.mappers.artist_mapper import (
    artist_create_to_domain,
    artist_to_response,
)
from app.adapters.inbound.api.mappers.common import (
    equipment_items,
    require_persisted_id,
    resolve_time_range,
    status_value,
)
from app.adapters.inbound.api.mappers.concert_mapper import (
    concert_create_to_domain,
    concert_reschedule_to_domain,
    concert_reschedule_to_time_range,
    concert_to_response,
)
from app.adapters.inbound.api.mappers.festival_mapper import (
    festival_create_to_domain,
    festival_to_response,
)
from app.adapters.inbound.api.mappers.incident_mapper import (
    incident_create_to_domain,
    incident_to_response,
)
from app.adapters.inbound.api.mappers.stage_mapper import (
    stage_create_to_domain,
    stage_to_response,
)

__all__ = [
    "artist_create_to_domain",
    "artist_to_response",
    "concert_create_to_domain",
    "concert_reschedule_to_domain",
    "concert_reschedule_to_time_range",
    "concert_to_response",
    "equipment_items",
    "festival_create_to_domain",
    "festival_to_response",
    "incident_create_to_domain",
    "incident_to_response",
    "require_persisted_id",
    "resolve_time_range",
    "stage_create_to_domain",
    "stage_to_response",
    "status_value",
]
