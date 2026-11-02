from typing import List
from fastapi import APIRouter, Query, status
from app.schemas.metrics import (
    MetricSummary,
    PulseEvent,
    PulseEventCreate,
    SystemMetric,
)
from app.services.pulse_service import pulse_service

router = APIRouter()


@router.get(
    "/pulse",
    response_model=MetricSummary,
    summary="Get Pulse Overview",
    description="Retrieves a complete snapshot of system metrics, service status, and recent activity.",
)
async def get_pulse_summary() -> MetricSummary:
    """Returns aggregated system metrics and recent events."""
    return pulse_service.get_summary()


@router.get(
    "/system",
    response_model=SystemMetric,
    summary="Get System Telemetry",
    description="Retrieves real-time CPU, RAM, and storage utilization.",
)
async def get_system_metrics() -> SystemMetric:
    """Returns real-time hardware telemetry."""
    return pulse_service.get_system_metrics()


@router.get(
    "/events",
    response_model=List[PulseEvent],
    summary="List Activity Events",
    description="Retrieves recent activity events recorded in DevPulse.",
)
async def list_events(
    limit: int = Query(50, ge=1, le=200, description="Max number of events to return"),
) -> List[PulseEvent]:
    """Returns recorded activity events."""
    return pulse_service.list_events(limit=limit)


@router.post(
    "/events",
    response_model=PulseEvent,
    status_code=status.HTTP_201_CREATED,
    summary="Record Pulse Event",
    description="Records a new activity event or developer log item.",
)
async def create_event(event_in: PulseEventCreate) -> PulseEvent:
    """Creates a new pulse event."""
    return pulse_service.create_event(event_in)
