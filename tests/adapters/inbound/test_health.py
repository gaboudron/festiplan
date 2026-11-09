from fastapi.testclient import TestClient

# ==========================
# Tests API Santé
# ==========================

def test_health_endpoint(client: TestClient):
    """Vérifie que l'endpoint de santé répond correctement."""
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
