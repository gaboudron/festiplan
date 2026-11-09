from unittest.mock import MagicMock
from fastapi.testclient import TestClient

from app.adapters.inbound.api.dependencies import get_concert_service
from app.domain.concert.entities import Concert
from app.domain.concert.value_object import ConcertStatus
from app.domain.time_range import TimeRange
from app.main import app
from app.ports.inbound.concert_inbound_port import ConcertInboundPort


# ==========================
# Tests API Concerts
# ==========================

def test_concert_end_must_be_after_start(client: TestClient):
    """Vérifie qu'un concert dont la fin précède le début est refusé."""
    response = client.post(
        "/concerts",
        json={
            "festival_id": 1,
            "artist_id": 1,
            "stage_id": 1,
            "start_time": "2027-06-18T15:00:00",
            "end_time": "2027-06-18T14:00:00",
        },
    )

    assert response.status_code == 400


def test_create_concert_with_unknown_festival_returns_404(client: TestClient):
    """Vérifie qu'un concert rattaché à un festival inexistant renvoie 404."""
    response = client.post(
        "/concerts",
        json={
            "festival_id": 999,
            "artist_id": 1,
            "stage_id": 1,
            "start_time": "2027-06-18T15:00:00",
            "end_time": "2027-06-18T16:00:00",
        },
    )

    assert response.status_code == 404
    assert response.json()["type"] == "NOT_FOUND"


def test_create_concert_with_dependency_override(client: TestClient):
    """Vérifie que l'injection du port entrant peut être substituée avec dependency_overrides."""
    mock_service = MagicMock(spec=ConcertInboundPort)
    from datetime import datetime
    mock_service.create_concert.return_value = Concert(
        id=42,
        festival_id=1,
        artist_id=2,
        stage_id=3,
        time_range=TimeRange(
            start=datetime(2027, 6, 18, 15, 0),
            end=datetime(2027, 6, 18, 16, 0),
        ),
        status=ConcertStatus.SCHEDULED,
    )

    app.dependency_overrides[get_concert_service] = lambda: mock_service
    try:
        response = client.post(
            "/concerts",
            json={
                "festival_id": 1,
                "artist_id": 2,
                "stage_id": 3,
                "start_time": "2027-06-18T15:00:00",
                "end_time": "2027-06-18T16:00:00",
            },
        )
        assert response.status_code == 201
        assert response.json()["id"] == 42
        mock_service.create_concert.assert_called_once()
    finally:
        app.dependency_overrides.clear()

