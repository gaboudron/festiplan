from abc import ABC, abstractmethod
from app.domain.artist.entities import Artist


class ArtistRepositoryOutboundPort(ABC):
    @abstractmethod
    def get(self, artist_id: int) -> Artist | None:
        """Récupère un artiste par son identifiant."""
        pass

    @abstractmethod
    def list_all(self) -> list[Artist]:
        """Retourne la liste complète des artistes."""
        pass

    @abstractmethod
    def save(self, artist: Artist) -> Artist:
        """Persiste (création ou mise à jour) un artiste et le retourne."""
        pass

