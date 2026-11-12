import os
import platform
import time
import uuid
from collections import deque
from datetime import UTC, datetime
from threading import Lock

from app.core.logger import logger
from app.schemas.metrics import (
    MetricSummary,
    PulseEvent,
    PulseEventCreate,
    PulseEventStatus,
    ServiceStatus,
    SystemMetric,
)

# Optional psutil integration for real system stats
try:
    import psutil
except ImportError:
    psutil = None  # type: ignore

MAX_RETAINED_EVENTS = 200


class PulseService:
    """Service managing system metrics and pulse event telemetry."""

    def __init__(self, max_events: int = MAX_RETAINED_EVENTS) -> None:
        self._lock = Lock()
        self._start_time = time.time()
        self._events: deque[PulseEvent] = deque(maxlen=max_events)
        self._total_events_count: int = 0
        self._seed_initial_events()

    def _seed_initial_events(self) -> None:
        """Seeds initial template events for demonstration."""
        initial_samples: list[tuple[str, str, PulseEventStatus, str]] = [
            (
                "DevPulse Template Initialized",
                "system",
                "success",
                "Boilerplate setup completed successfully",
            ),
            (
                "FastAPI Service Bootstrapped",
                "backend",
                "success",
                "API routers and telemetry mounted",
            ),
            (
                "React Dashboard Connected",
                "frontend",
                "info",
                "Vite UI dev link established",
            ),
        ]
        for title, category, status, details in initial_samples:
            self._events.append(
                PulseEvent(
                    id=str(uuid.uuid4())[:8],
                    title=title,
                    category=category,
                    status=status,
                    details=details,
                    timestamp=datetime.now(UTC),
                )
            )
            self._total_events_count += 1

    @property
    def uptime_seconds(self) -> float:
        """Returns application uptime in seconds."""
        return round(time.time() - self._start_time, 2)

    @staticmethod
    def _clamp_percent(value: float) -> float:
        """Clamps percentage readings within valid [0.0, 100.0] bounds."""
        return round(min(max(float(value), 0.0), 100.0), 1)

    def get_system_metrics(self) -> SystemMetric:
        """Captures current system resource utilization."""
        platform_label = f"{platform.system()} {platform.release()}"
        if psutil is not None:
            try:
                cpu = self._clamp_percent(psutil.cpu_percent(interval=None))
                mem = psutil.virtual_memory()
                root_path = os.path.abspath(os.sep)
                disk = psutil.disk_usage(root_path)
                return SystemMetric(
                    cpu_percent=cpu,
                    memory_percent=self._clamp_percent(mem.percent),
                    memory_used_mb=round(mem.used / (1024 * 1024), 1),
                    memory_total_mb=round(mem.total / (1024 * 1024), 1),
                    disk_percent=self._clamp_percent(disk.percent),
                    platform_name=platform_label,
                )
            except Exception as exc:
                logger.warning("Failed to sample live psutil metrics, using fallback: %s", exc)

        # Fallback simulated metrics if psutil is unavailable or access restricted
        return SystemMetric(
            cpu_percent=12.5,
            memory_percent=38.2,
            memory_used_mb=6120.0,
            memory_total_mb=16000.0,
            disk_percent=45.0,
            platform_name=platform_label,
        )

    def get_services_status(self) -> list[ServiceStatus]:
        """Returns health status of dependent services."""
        return [
            ServiceStatus(name="FastAPI Core API", status="online", latency_ms=1.2),
            ServiceStatus(name="Telemetry Engine", status="online", latency_ms=0.8),
            ServiceStatus(name="Cache / In-Memory Store", status="online", latency_ms=0.3),
        ]

    def list_events(self, limit: int = 50) -> list[PulseEvent]:
        """Returns list of recent pulse events, newest first."""
        if limit <= 0:
            return []
        with self._lock:
            events_snapshot = list(self._events)
        return list(reversed(events_snapshot[-limit:]))

    def create_event(self, data: PulseEventCreate) -> PulseEvent:
        """Records a new activity pulse event."""
        event = PulseEvent(
            id=str(uuid.uuid4())[:8],
            title=data.title,
            category=data.category,
            status=data.status,
            details=data.details,
            timestamp=datetime.now(UTC),
        )
        with self._lock:
            self._events.append(event)
            self._total_events_count += 1
        return event

    def get_summary(self) -> MetricSummary:
        """Returns full pulse overview including system telemetry and recent events."""
        with self._lock:
            events_snapshot = list(self._events)
            total_recorded = self._total_events_count

        return MetricSummary(
            system=self.get_system_metrics(),
            active_services=self.get_services_status(),
            recent_events=list(reversed(events_snapshot[-10:])),
            total_events_recorded=total_recorded,
        )

    def get_prometheus_exposition(self) -> str:
        """Formats current telemetry into Prometheus RFC 0.0.4 text exposition format."""
        sys_metric = self.get_system_metrics()
        with self._lock:
            total_recorded = self._total_events_count

        lines = [
            "# HELP devpulse_cpu_percent Current CPU utilization percentage",
            "# TYPE devpulse_cpu_percent gauge",
            f"devpulse_cpu_percent {sys_metric.cpu_percent}",
            "# HELP devpulse_memory_percent Current RAM utilization percentage",
            "# TYPE devpulse_memory_percent gauge",
            f"devpulse_memory_percent {sys_metric.memory_percent}",
            "# HELP devpulse_memory_used_mb Used RAM in Megabytes",
            "# TYPE devpulse_memory_used_mb gauge",
            f"devpulse_memory_used_mb {sys_metric.memory_used_mb}",
            "# HELP devpulse_disk_percent Disk utilization percentage",
            "# TYPE devpulse_disk_percent gauge",
            f"devpulse_disk_percent {sys_metric.disk_percent}",
            "# HELP devpulse_uptime_seconds Application uptime in seconds",
            "# TYPE devpulse_uptime_seconds counter",
            f"devpulse_uptime_seconds {self.uptime_seconds}",
            "# HELP devpulse_events_total Total developer pulse events recorded",
            "# TYPE devpulse_events_total counter",
            f"devpulse_events_total {total_recorded}",
        ]
        return "\n".join(lines) + "\n"


pulse_service = PulseService()
