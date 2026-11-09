"""Tests unitaires de ``FestivalService``."""

import pytest

from app.domain.exceptions import FestivalNotFoundError
from app.domain.festival.events import FestivalPublishedEvent


def test_list_festivals_returns_repository_result(
    festival_service, festival_repository, festival
):
    festival_repository.list_all.return_value = [festival]

    assert festival_service.list_festivals() == [festival]


def test_create_festival_saves_and_commits(
    festival_service, festival_repository, transaction, festival
):
    festival_repository.save.return_value = festival

    assert festival_service.create_festival(festival) is festival
    festival_repository.save.assert_called_once_with(festival)
    transaction.commit.assert_called_once_with()


def test_publish_festival_uses_domain_method_and_publishes_event(
    festival_service, festival_repository, transaction, event_bus, festival
):
    festival_repository.get.return_value = festival
    festival_repository.save.side_effect = lambda entity: entity

    result = festival_service.publish_festival(festival.id)

    assert result.is_published is True
    festival_repository.save.assert_called_once_with(festival)
    transaction.commit.assert_called_once_with()
    event_bus.publish.assert_called_once()
    event = event_bus.publish.call_args.args[0]
    assert isinstance(event, FestivalPublishedEvent)
    assert event.festival_id == festival.id
    assert event.festival_name == festival.name


def test_publish_festival_publishes_after_commit(
    festival_service, festival_repository, transaction, event_bus, festival
):
    festival_repository.get.return_value = festival
    festival_repository.save.side_effect = lambda entity: entity

    def assert_event_not_yet_published():
        assert event_bus.publish.call_count == 0

    transaction.commit.side_effect = assert_event_not_yet_published

    festival_service.publish_festival(festival.id)

    transaction.commit.assert_called_once_with()
    event_bus.publish.assert_called_once()


def test_publish_festival_requires_existing_festival(
    festival_service, festival_repository, event_bus, transaction
):
    festival_repository.get.return_value = None

    with pytest.raises(FestivalNotFoundError):
        festival_service.publish_festival(99)

    festival_repository.save.assert_not_called()
    transaction.commit.assert_not_called()
    event_bus.publish.assert_not_called()
