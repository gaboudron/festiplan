"""Port entrant pour les artistes."""

from typing import Protocol, runtime_checkable

from app.domain.artist.entities import Artist


@runtime_checkable
class ArtistInboundPort(Protocol):
    """Cas d'usage exposés à l'adaptateur entrant pour les artistes."""

    def list_artists(self) -> list[Artist]:
        """Retourne tous les artistes."""
        ...

    def create_artist(self, artist: Artist) -> Artist:
        """Crée un artiste et retourne l'entité persistée."""
        ...
