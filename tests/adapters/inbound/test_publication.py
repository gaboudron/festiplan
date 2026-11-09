from fastapi.testclient import TestClient

# ==========================
# Tests API Publication
# ==========================

def test_publish_unknown_festival_returns_404(client: TestClient):
    """Vérifie que la publication d'un festival inexistant renvoie 404."""
    response = client.post("/festivals/999/publish")

    assert response.status_code == 404
