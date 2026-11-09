"""Tests des contrats de ports entrants.

Les ports sont des ``Protocol`` : ces tests vérifient qu'une implémentation
exposant les bonnes méthodes est reconnue, et qu'il manque bien une méthode
sinon.
"""

from app.domain.artist.entities import Artist
from app.domain.concert.entities import Concert
from app.domain.festival.entities import Festival, Stage
from app.domain.incident.entities import Incident
from app.domain.time_range import TimeRange
from app.ports.inbound import (
    ArtistInboundPort,
    ConcertInboundPort,
    FestivalInboundPort,
    IncidentInboundPort,
    StageInboundPort,
)

# ==========================
# Implémentations factices
# ==========================

class FakeArtistPort:
    def list_artists(self) -> list[Artist]:
        return []

    def create_artist(self, artist: Artist) -> Artist:
        return artist


class FakeStagePort:
    def list_stages(self, festival_id: int) -> list[Stage]:
        return []

    def create_stage(self, stage: Stage) -> Stage:
        return stage


class FakeFestivalPort:
    def list_festivals(self) -> list[Festival]:
        return []

    def create_festival(self, festival: Festival) -> Festival:
        return festival

    def publish_festival(self, festival_id: int) -> Festival:
        raise NotImplementedError


class FakeConcertPort:
    def list_concerts(self, festival_id: int) -> list[Concert]:
        return []

    def get_concert(self, concert_id: int) -> Concert:
        raise NotImplementedError

    def create_concert(self, concert: Concert) -> Concert:
        return concert

    def reschedule_concert(
        self,
        concert_id: int,
        new_time_range: TimeRange,
        new_stage_id: int | None = None,
    ) -> Concert:
        raise NotImplementedError

    def cancel_concert(self, concert_id: int) -> Concert:
        raise NotImplementedError

    def get_schedule(self, festival_id: int) -> list[Concert]:
        return []


class FakeIncidentPort:
    def list_incidents(self, concert_id: int | None = None) -> list[Incident]:
        return []

    def declare_incident(self, incident: Incident) -> Incident:
        return incident


class IncompleteArtistPort:
    def list_artists(self) -> list[Artist]:
        return []


# ==========================
# Tests
# ==========================

def test_artist_port_contract():
    assert isinstance(FakeArtistPort(), ArtistInboundPort)
    assert not isinstance(IncompleteArtistPort(), ArtistInboundPort)


def test_stage_port_contract():
    assert isinstance(FakeStagePort(), StageInboundPort)


def test_festival_port_contract():
    assert isinstance(FakeFestivalPort(), FestivalInboundPort)


def test_concert_port_contract():
    assert isinstance(FakeConcertPort(), ConcertInboundPort)


def test_incident_port_contract():
    assert isinstance(FakeIncidentPort(), IncidentInboundPort)


def test_concert_port_exposes_reschedule_with_optional_stage():
    assert isinstance(FakeConcertPort(), ConcertInboundPort)
    # Le changement de scène est optionnel dans le contrat.
    assert "new_stage_id" in ConcertInboundPort.reschedule_concert.__annotations__
