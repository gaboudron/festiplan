"""Tests unitaires de ``ArtistService``."""

import pytest


def test_list_artists_returns_repository_result(
    artist_service, artist_repository, artist
):
    artist_repository.list_all.return_value = [artist]

    assert artist_service.list_artists() == [artist]
    artist_repository.list_all.assert_called_once_with()


def test_create_artist_saves_and_commits(
    artist_service, artist_repository, transaction, artist
):
    artist_repository.save.return_value = artist

    result = artist_service.create_artist(artist)

    assert result is artist
    artist_repository.save.assert_called_once_with(artist)
    transaction.commit.assert_called_once_with()
    transaction.rollback.assert_not_called()


def test_create_artist_rolls_back_on_repository_failure(
    artist_service, artist_repository, transaction, artist
):
    artist_repository.save.side_effect = RuntimeError("base indisponible")

    with pytest.raises(RuntimeError, match="base indisponible"):
        artist_service.create_artist(artist)

    transaction.rollback.assert_called_once_with()
    transaction.commit.assert_not_called()
