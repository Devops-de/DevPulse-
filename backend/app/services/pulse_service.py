import platform
import time
import uuid
from datetime import datetime, timezone
from threading import Lock
from typing import List, Optional

from app.schemas.metrics import (
    MetricSummary,
    PulseEvent,
    PulseEventCreate,
    ServiceStatus,
    SystemMetric,
)

# Optional psutil integration for real system stats
try:
    import psutil
except ImportError:
    psutil = None  # type: ignore


class PulseService:
    """Service managing system metrics and pulse event telemetry."""

    def __init__(self) -> None:
        self._lock = Lock()
        self._start_time = time.time()
        self._events: List[PulseEvent] = []
        self._seed_initial_events()

    def _seed_initial_events(self) -> None:
        """Seeds initial template events for demonstration."""
        initial_samples = [
            ("DevPulse Template Initialized", "system", "success", "Boilerplate setup completed successfully"),
            ("FastAPI Service Bootstrapped", "backend", "success", "API routers and telemetry mounted"),
            ("React Dashboard Connected", "frontend", "info", "Vite UI dev link established"),
        ]
        for title, cat, status, details in initial_samples:
            self._events.append(
                PulseEvent(
                    id=str(uuid.uuid4())[:8],
                    title=title,
                    category=cat,
                    status=status,
                    details=details,
                    timestamp=datetime.now(timezone.utc),
                )
            )

    @property
    def uptime_seconds(self) -> float:
        """Returns application uptime in seconds."""
        return round(time.time() - self._start_time, 2)

    def get_system_metrics(self) -> SystemMetric:
        """Captures current system resource utilization."""
        if psutil:
            try:
                cpu = psutil.cpu_percent(interval=None)
                mem = psutil.virtual_memory()
                disk = psutil.disk_usage("/")
                return SystemMetric(
                    cpu_percent=cpu,
                    memory_percent=mem.percent,
                    memory_used_mb=round(mem.used / (1024 * 1024), 1),
                    memory_total_mb=round(mem.total / (1024 * 1024), 1),
                    disk_percent=disk.percent,
                    platform_name=f"{platform.system()} {platform.release()}",
                )
            except Exception:
                pass

        # Fallback simulated metrics if psutil is unavailable or access restricted
        return SystemMetric(
            cpu_percent=12.5,
            memory_percent=38.2,
            memory_used_mb=6120.0,
            memory_total_mb=16000.0,
            disk_percent=45.0,
            platform_name=f"{platform.system()} {platform.release()}",
        )

    def get_services_status(self) -> List[ServiceStatus]:
        """Returns health status of dependent services."""
        return [
            ServiceStatus(name="FastAPI Core API", status="online", latency_ms=1.2),
            ServiceStatus(name="Telemetry Engine", status="online", latency_ms=0.8),
            ServiceStatus(name="Cache / In-Memory Store", status="online", latency_ms=0.3),
        ]

    def list_events(self, limit: int = 50) -> List[PulseEvent]:
        """Returns list of recent pulse events, newest first."""
        with self._lock:
            return list(reversed(self._events[-limit:]))

    def create_event(self, data: PulseEventCreate) -> PulseEvent:
        """Records a new activity pulse event."""
        event = PulseEvent(
            id=str(uuid.uuid4())[:8],
            title=data.title,
            category=data.category,
            status=data.status,
            details=data.details,
            timestamp=datetime.now(timezone.utc),
        )
        with self._lock:
            self._events.append(event)
            # Retain up to 200 events in memory
            if len(self._events) > 200:
                self._events.pop(0)
        return event

    def get_summary(self) -> MetricSummary:
        """Returns full pulse overview including system telemetry and recent events."""
        return MetricSummary(
            system=self.get_system_metrics(),
            active_services=self.get_services_status(),
            recent_events=self.list_events(limit=10),
            total_events_recorded=len(self._events),
        )


pulse_service = PulseService()
