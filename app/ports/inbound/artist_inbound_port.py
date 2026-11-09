"""Port entrant pour les artistes."""

from abc import ABC, abstractmethod

from app.domain.artist.entities import Artist


class ArtistInboundPort(ABC):
    """Cas d'usage exposés à l'adaptateur entrant pour les artistes."""

    @abstractmethod
    def list_artists(self) -> list[Artist]:
        """Retourne tous les artistes."""
        ...

    @abstractmethod
    def create_artist(self, artist: Artist) -> Artist:
        """Crée un artiste et retourne l'entité persistée."""
        ...
