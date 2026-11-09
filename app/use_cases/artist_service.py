"""Service applicatif pour les artistes."""

from app.domain.artist.entities import Artist
from app.ports.inbound.artist_inbound_port import ArtistInboundPort
from app.ports.outbound.repository.artist_repository_outbound_port import (
    ArtistRepositoryOutboundPort,
)
from app.ports.outbound.transaction.transaction_outbound_port import (
    TransactionOutboundPort,
)
from app.use_cases._support import in_transaction


class ArtistService(ArtistInboundPort):
    """Implémente ``ArtistInboundPort`` en orchestrant repository et transaction."""

    def __init__(
        self,
        artists: ArtistRepositoryOutboundPort,
        transaction: TransactionOutboundPort,
    ) -> None:
        self._artists = artists
        self._transaction = transaction

    def list_artists(self) -> list[Artist]:
        return self._artists.list_all()

    def create_artist(self, artist: Artist) -> Artist:
        return in_transaction(
            self._transaction, lambda: self._artists.save(artist)
        )
