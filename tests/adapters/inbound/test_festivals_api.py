from fastapi.testclient import TestClient

# ==========================
# Tests API Festivals
# ==========================

def test_festival_end_must_be_after_start(client: TestClient):
    """Vérifie qu'un festival dont la fin précède le début est refusé."""
    response = client.post(
        "/festivals",
        json={
            "name": "Test Festival",
            "location": "Clisson",
            "start_date": "2027-06-20T10:00:00",
            "end_date": "2027-06-19T10:00:00",
        },
    )

    assert response.status_code == 400
    assert response.json()["type"] == "BAD_REQUEST"
