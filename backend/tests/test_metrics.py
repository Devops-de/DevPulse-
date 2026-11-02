from fastapi.testclient import TestClient


def test_pulse_summary(client: TestClient) -> None:
    """Tests the /api/v1/metrics/pulse endpoint."""
    response = client.get("/api/v1/metrics/pulse")
    assert response.status_code == 200
    data = response.json()
    assert "system" in data
    assert "active_services" in data
    assert "recent_events" in data
    assert "total_events_recorded" in data
    assert data["system"]["cpu_percent"] >= 0


def test_system_metrics(client: TestClient) -> None:
    """Tests the /api/v1/metrics/system endpoint."""
    response = client.get("/api/v1/metrics/system")
    assert response.status_code == 200
    data = response.json()
    assert "cpu_percent" in data
    assert "memory_percent" in data
    assert "disk_percent" in data


def test_create_and_list_events(client: TestClient) -> None:
    """Tests creating and querying pulse events."""
    payload = {
        "title": "Automated Unit Test Event",
        "category": "test",
        "status": "info",
        "details": "Integration run verification",
    }
    post_res = client.post("/api/v1/metrics/events", json=payload)
    assert post_res.status_code == 201
    created = post_res.json()
    assert created["title"] == payload["title"]
    assert "id" in created
    assert "timestamp" in created

    # Verify event appears in list
    list_res = client.get("/api/v1/metrics/events?limit=10")
    assert list_res.status_code == 200
    events = list_res.json()
    assert any(e["id"] == created["id"] for e in events)
