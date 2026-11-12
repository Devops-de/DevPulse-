from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

PulseEventStatus = Literal["success", "warning", "error", "info"]
ServiceState = Literal["online", "offline", "degraded"]


class SystemMetric(BaseModel):
    """Real-time system telemetry schema."""

    cpu_percent: float = Field(..., ge=0.0, le=100.0, description="Current CPU usage percentage")
    memory_percent: float = Field(..., ge=0.0, le=100.0, description="Current RAM usage percentage")
    memory_used_mb: float = Field(..., ge=0.0, description="Used RAM in Megabytes")
    memory_total_mb: float = Field(..., ge=0.0, description="Total RAM in Megabytes")
    disk_percent: float = Field(..., ge=0.0, le=100.0, description="Disk usage percentage")
    platform_name: str = Field(..., description="Operating system platform")


class PulseEventBase(BaseModel):
    """Base fields for an activity pulse event."""

    title: str = Field(..., description="Event title", min_length=2, max_length=100)
    category: str = Field(
        "general",
        min_length=1,
        max_length=50,
        description="Event category (e.g., git, build, deployment, test)",
    )
    status: PulseEventStatus = Field(
        "success",
        description="Status (success, warning, error, info)",
    )
    details: str | None = Field(
        None,
        max_length=500,
        description="Detailed description or payload",
    )


class PulseEventCreate(PulseEventBase):
    """Schema for creating a pulse event."""


class PulseEvent(PulseEventBase):
    """Schema for a persisted pulse event."""

    id: str = Field(..., description="Unique event identifier")
    timestamp: datetime = Field(..., description="Event creation timestamp")


class ServiceStatus(BaseModel):
    """Status of an individual internal/external service."""

    name: str
    status: ServiceState
    latency_ms: float = Field(..., ge=0.0)


class MetricSummary(BaseModel):
    """Comprehensive pulse metrics summary."""

    system: SystemMetric
    active_services: list[ServiceStatus]
    recent_events: list[PulseEvent]
    total_events_recorded: int = Field(..., ge=0)
