"""Fixtures partagées pour les tests des cas d'usage.

Les fixtures s'appuient sur les fabriques de ``factories.py`` et renvoient des
objets neufs à chaque test : un test peut donc modifier son entité sans
impacter les autres. Aucune base de données ni aucun client HTTP n'est
nécessaire ici ; les dépendances sortantes seront remplacées par des faux
adaptateurs dans les tests.
"""

import pytest

from app.domain.time_range import TimeRange
from factories import (
    DEFAULT_CONCERT_END,
    DEFAULT_CONCERT_START,
    DEFAULT_FESTIVAL_END,
    DEFAULT_FESTIVAL_START,
    make_artist,
    make_concert,
    make_festival,
    make_incident,
    make_stage,
)


@pytest.fixture
def festival_time_range() -> TimeRange:
    """Créneau par défaut du festival (trois jours en juin 2027)."""
    return TimeRange(DEFAULT_FESTIVAL_START, DEFAULT_FESTIVAL_END)


@pytest.fixture
def concert_time_range() -> TimeRange:
    """Créneau par défaut d'un concert (premier soir du festival)."""
    return TimeRange(DEFAULT_CONCERT_START, DEFAULT_CONCERT_END)


@pytest.fixture
def artist():
    """Artiste valide, sans identifiant persistant particulier."""
    return make_artist()


@pytest.fixture
def stage():
    """Scène valide rattachée au festival par défaut."""
    return make_stage()


@pytest.fixture
def festival(stage):
    """Festival en préparation contenant la scène par défaut."""
    return make_festival(stages=[stage])


@pytest.fixture
def concert(festival, artist, stage):
    """Concert programmé cohérent avec le festival, l'artiste et la scène."""
    return make_concert(
        festival_id=festival.id,
        artist_id=artist.id,
        stage_id=stage.id,
    )


@pytest.fixture
def incident(concert):
    """Incident non résolu rattaché au concert par défaut."""
    return make_incident(concert_id=concert.id)
