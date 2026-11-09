from fastapi.testclient import TestClient

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
