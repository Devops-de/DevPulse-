from app.core.config import Settings
from app.schemas.metrics import PulseEventCreate
from app.services.pulse_service import PulseService
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
    assert 0.0 <= data["system"]["cpu_percent"] <= 100.0
    assert 0.0 <= data["system"]["memory_percent"] <= 100.0
    assert 0.0 <= data["system"]["disk_percent"] <= 100.0


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

    # Verify event appears first in list (newest-first ordering)
    list_res = client.get("/api/v1/metrics/events?limit=10")
    assert list_res.status_code == 200
    events = list_res.json()
    assert events[0]["id"] == created["id"]


def test_create_event_validation_errors(client: TestClient) -> None:
    """Tests schema validation rejects malformed or invalid event payloads."""
    # Title shorter than min_length=2
    short_title_res = client.post(
        "/api/v1/metrics/events",
        json={"title": "A", "category": "test", "status": "info"},
    )
    assert short_title_res.status_code == 422

    # Invalid literal status
    bad_status_res = client.post(
        "/api/v1/metrics/events",
        json={"title": "Valid Title", "category": "test", "status": "unknown_status"},
    )
    assert bad_status_res.status_code == 422

    # Out-of-range query limit
    bad_limit_res = client.get("/api/v1/metrics/events?limit=500")
    assert bad_limit_res.status_code == 422


def test_pulse_service_ring_buffer_and_monotonic_counter() -> None:
    """Tests bounded event retention and monotonic cumulative counter."""
    service = PulseService(max_events=5)
    # 3 seeded initially
    assert service.get_summary().total_events_recorded == 3

    for idx in range(4):
        service.create_event(
            PulseEventCreate(
                title=f"Event #{idx}",
                category="test",
                status="success",
            )
        )

    # Bounded to max_events=5, while total_events_recorded tracks cumulative 7
    retained = service.list_events(limit=50)
    assert len(retained) == 5
    assert retained[0].title == "Event #3"
    assert service.get_summary().total_events_recorded == 7
    assert service._clamp_percent(125.4) == 100.0
    assert service._clamp_percent(-5.0) == 0.0


def test_settings_cors_origins_parsing() -> None:
    """Tests CORS origin parsing from comma-separated and JSON strings."""
    csv_settings = Settings.model_validate(
        {"CORS_ORIGINS": "http://localhost:3000, http://localhost:5173"}
    )
    assert csv_settings.CORS_ORIGINS == ["http://localhost:3000", "http://localhost:5173"]

    json_settings = Settings.model_validate({"CORS_ORIGINS": '["https://example.com"]'})
    assert json_settings.CORS_ORIGINS == ["https://example.com"]
