from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class SystemMetric(BaseModel):
    """Real-time system telemetry schema."""
    cpu_percent: float = Field(..., description="Current CPU usage percentage")
    memory_percent: float = Field(..., description="Current RAM usage percentage")
    memory_used_mb: float = Field(..., description="Used RAM in Megabytes")
    memory_total_mb: float = Field(..., description="Total RAM in Megabytes")
    disk_percent: float = Field(..., description="Disk usage percentage")
    platform_name: str = Field(..., description="Operating system platform")


class PulseEventBase(BaseModel):
    """Base fields for an activity pulse event."""
    title: str = Field(..., description="Event title", min_length=2, max_length=100)
    category: str = Field("general", description="Event category (e.g., git, build, deployment, test)")
    status: str = Field("success", description="Status (success, warning, error, info)")
    details: Optional[str] = Field(None, description="Detailed description or payload")


class PulseEventCreate(PulseEventBase):
    """Schema for creating a pulse event."""
    pass


class PulseEvent(PulseEventBase):
    """Schema for a persisted pulse event."""
    id: str = Field(..., description="Unique event identifier")
    timestamp: datetime = Field(..., description="Event creation timestamp")


class ServiceStatus(BaseModel):
    """Status of an individual internal/external service."""
    name: str
    status: str  # online, offline, degraded
    latency_ms: float


class MetricSummary(BaseModel):
    """Comprehensive pulse metrics summary."""
    system: SystemMetric
    active_services: List[ServiceStatus]
    recent_events: List[PulseEvent]
    total_events_recorded: int
