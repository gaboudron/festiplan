from typing import Protocol

from app.domain.artist.entities import Artist


class ArtistRepositoryPort(Protocol):
    """Contrat de persistance des artistes."""

    def get_by_id(self, artist_id: int) -> Artist | None:
        ...

    def get_all(self) -> list[Artist]:
        ...

    def save(self, artist: Artist) -> Artist:
        ...