from fastapi.testclient import TestClient


def test_health_endpoint(client: TestClient) -> None:
    """Tests the /api/v1/health endpoint."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["app_name"] == "DevPulse"
    assert "uptime_seconds" in data
    assert "version" in data


def test_root_dashboard(client: TestClient) -> None:
    """Tests the root dashboard HTML rendering."""
    response = client.get("/")
    assert response.status_code == 200
    assert "DevPulse" in response.text
