"""Tests unitaires de ``StageService``."""

import pytest

from app.domain.exceptions import FestivalNotFoundError


def test_list_stages_returns_repository_result(
    stage_service, stage_repository, stage
):
    stage_repository.list_by_festival_id.return_value = [stage]

    assert stage_service.list_stages(1) == [stage]
    stage_repository.list_by_festival_id.assert_called_once_with(1)


def test_create_stage_saves_and_commits(
    stage_service, stage_repository, festival_repository, transaction,
    festival, stage,
):
    festival_repository.get.return_value = festival
    stage_repository.save.return_value = stage

    result = stage_service.create_stage(stage)

    assert result is stage
    festival_repository.get.assert_called_once_with(stage.festival_id)
    stage_repository.save.assert_called_once_with(stage)
    transaction.commit.assert_called_once_with()


def test_create_stage_requires_existing_festival(
    stage_service, stage_repository, festival_repository, transaction, stage
):
    festival_repository.get.return_value = None

    with pytest.raises(FestivalNotFoundError):
        stage_service.create_stage(stage)

    stage_repository.save.assert_not_called()
    transaction.commit.assert_not_called()
