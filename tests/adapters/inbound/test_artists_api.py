from fastapi.testclient import TestClient

# ==========================
# Tests API Artistes
# ==========================

def test_artist_name_must_be_a_string(client: TestClient):
    """Vérifie qu'un nom d'artiste non textuel est refusé par la validation."""
    response = client.post(
        "/artists",
        json={
            "name": 123,
            "genre": "Metal",
            "required_equipment": [],
        },
    )

    assert response.status_code == 422
