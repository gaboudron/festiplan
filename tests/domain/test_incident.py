from datetime import datetime, timezone
import pytest
from app.domain.incident.entities import Incident
from app.domain.exceptions import InvalidIncidentMessageError

# ==========================
# Tests Incident
# ==========================

def test_incident_default_values():
    incident = Incident(
        id=6,
        concert_id= 2,
        description="Micro défectueux",
    )

    assert incident.resolved is False
    assert isinstance(incident.occurred_at, datetime)


def test_incident_normalizes_occurred_at_to_utc():
    """Vérifie que la date de survenue est normalisée en UTC aware."""
    incident = Incident(
        id=1,
        concert_id=3,
        description="Problème lumière",
        occurred_at=datetime(2027, 6, 18, 20, 0),
    )

    assert incident.occurred_at == datetime(2027, 6, 18, 20, 0, tzinfo=timezone.utc)
    assert incident.occurred_at.tzinfo is not None


def test_incident_resolved():
    """Vérifie qu'un incident soit bien résolu;"""
    incident = Incident(
        id=1,
        concert_id= 3,
        description="Problème lumière",
        resolved=False
    )

    incident.mark_resolved()

    assert incident.resolved is True


def test_incident_cannot_have_empty_description():
    """Vérifie qu'un incident n'a pas de message vide/invalide."""
    with pytest.raises(InvalidIncidentMessageError):
        Incident(id=1, concert_id=3, description="  ")
