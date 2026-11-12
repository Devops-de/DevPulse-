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
    assert "innerHTML" not in response.text


def test_prometheus_metrics(client: TestClient) -> None:
    """Tests the /metrics Prometheus exposition endpoint."""
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "devpulse_cpu_percent" in response.text
    assert "devpulse_memory_percent" in response.text
    assert "devpulse_uptime_seconds" in response.text
    assert "devpulse_events_total" in response.text
