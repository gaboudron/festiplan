"""Ports entrants de l'application FestiPlan.

Les ports entrants décrivent les cas d'usage que l'adaptateur entrant (HTTP)
peut appeler. Leurs implémentations vivent dans ``app/use_cases`` et
manipulent exclusivement des entités du domaine.

Convention de nommage : le fichier est le snake_case du nom de classe, comme
pour les ports sortants (``artist_inbound_port.py`` pour ``ArtistInboundPort``).
"""

from app.ports.inbound.artist_inbound_port import ArtistInboundPort
from app.ports.inbound.concert_inbound_port import ConcertInboundPort
from app.ports.inbound.festival_inbound_port import FestivalInboundPort
from app.ports.inbound.incident_inbound_port import IncidentInboundPort
from app.ports.inbound.stage_inbound_port import StageInboundPort

__all__ = [
    "ArtistInboundPort",
    "ConcertInboundPort",
    "FestivalInboundPort",
    "IncidentInboundPort",
    "StageInboundPort",
]
