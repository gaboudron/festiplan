from fastapi.testclient import TestClient

# ==========================
# Tests API Scènes
# ==========================

def test_stage_capacity_must_be_positive(client: TestClient):
    """Vérifie qu'une capacité de scène nulle ou négative est refusée."""
    response = client.post(
        "/stages",
        json={
            "festival_id": 1,
            "name": "Mainstage",
            "capacity": 0,
            "available_equipment": [],
        },
    )

    assert response.status_code == 422
