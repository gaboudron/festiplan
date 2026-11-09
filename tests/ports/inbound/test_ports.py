"""Tests des contrats de ports entrants.

Les ports sont des classes abstraites : une implémentation doit fournir
toutes les méthodes, sinon elle ne peut pas être instanciée.
"""

import inspect

import pytest

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

class FakeArtistPort(ArtistInboundPort):
    def list_artists(self) -> list[Artist]:
        return []

    def create_artist(self, artist: Artist) -> Artist:
        return artist


class FakeStagePort(StageInboundPort):
    def list_stages(self, festival_id: int) -> list[Stage]:
        return []

    def create_stage(self, stage: Stage) -> Stage:
        return stage


class FakeFestivalPort(FestivalInboundPort):
    def list_festivals(self) -> list[Festival]:
        return []

    def create_festival(self, festival: Festival) -> Festival:
        return festival

    def publish_festival(self, festival_id: int) -> Festival:
        raise NotImplementedError


class FakeConcertPort(ConcertInboundPort):
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


class FakeIncidentPort(IncidentInboundPort):
    def list_incidents(self, concert_id: int | None = None) -> list[Incident]:
        return []

    def declare_incident(self, incident: Incident) -> Incident:
        return incident


# ==========================
# Tests
# ==========================

def test_ports_are_abstract():
    for port in (
        ArtistInboundPort,
        StageInboundPort,
        FestivalInboundPort,
        ConcertInboundPort,
        IncidentInboundPort,
    ):
        with pytest.raises(TypeError):
            port()


def test_complete_implementations_are_valid():
    assert isinstance(FakeArtistPort(), ArtistInboundPort)
    assert isinstance(FakeStagePort(), StageInboundPort)
    assert isinstance(FakeFestivalPort(), FestivalInboundPort)
    assert isinstance(FakeConcertPort(), ConcertInboundPort)
    assert isinstance(FakeIncidentPort(), IncidentInboundPort)


def test_incomplete_implementation_cannot_be_instantiated():
    class IncompleteArtistPort(ArtistInboundPort):
        def list_artists(self) -> list[Artist]:
            return []

    with pytest.raises(TypeError):
        IncompleteArtistPort()


def test_reschedule_stage_is_optional():
    parameters = inspect.signature(
        ConcertInboundPort.reschedule_concert
    ).parameters

    assert parameters["new_stage_id"].default is None
