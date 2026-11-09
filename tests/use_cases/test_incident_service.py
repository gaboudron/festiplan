"""Tests unitaires de ``IncidentService``."""

import pytest

from app.domain.exceptions import ConcertNotFoundError


def test_list_incidents_without_filter(
    incident_service, incident_repository, incident
):
    incident_repository.list_all.return_value = [incident]

    assert incident_service.list_incidents() == [incident]
    incident_repository.list_all.assert_called_once_with()
    incident_repository.list_by_concert_id.assert_not_called()


def test_list_incidents_filtered_by_concert(
    incident_service, incident_repository, incident
):
    incident_repository.list_by_concert_id.return_value = [incident]

    assert incident_service.list_incidents(concert_id=incident.concert_id) == [
        incident
    ]
    incident_repository.list_by_concert_id.assert_called_once_with(
        incident.concert_id
    )
    incident_repository.list_all.assert_not_called()


def test_declare_incident_saves_and_commits(
    incident_service, incident_repository, concert_repository, transaction,
    concert, incident,
):
    concert_repository.get.return_value = concert
    incident_repository.save.return_value = incident

    result = incident_service.declare_incident(incident)

    assert result is incident
    concert_repository.get.assert_called_once_with(incident.concert_id)
    incident_repository.save.assert_called_once_with(incident)
    transaction.commit.assert_called_once_with()


def test_declare_incident_requires_existing_concert(
    incident_service, incident_repository, concert_repository, transaction,
    incident,
):
    concert_repository.get.return_value = None

    with pytest.raises(ConcertNotFoundError):
        incident_service.declare_incident(incident)

    incident_repository.save.assert_not_called()
    transaction.commit.assert_not_called()


def test_resolve_incident_marks_resolved_and_saves(
    incident_service, incident_repository, transaction, incident,
):
    incident.resolved = False
    incident_repository.get.return_value = incident
    incident_repository.save.return_value = incident

    result = incident_service.resolve_incident(incident.id)

    assert result.resolved is True
    incident_repository.get.assert_called_once_with(incident.id)
    incident_repository.save.assert_called_once_with(incident)
    transaction.commit.assert_called_once_with()
