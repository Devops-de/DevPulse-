import sys
from datetime import datetime, timezone
from fastapi import APIRouter
from app.core.config import settings
from app.schemas.health import HealthResponse
from app.services.pulse_service import pulse_service

router = APIRouter()


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Service Health Check",
    description="Returns current operational status, uptime, and system metadata.",
)
async def get_health() -> HealthResponse:
    """Returns application health status."""
    return HealthResponse(
        status="ok",
        app_name=settings.PROJECT_NAME,
        version=settings.VERSION,
        environment=settings.ENVIRONMENT,
        uptime_seconds=pulse_service.uptime_seconds,
        timestamp=datetime.now(timezone.utc),
        python_version=sys.version.split()[0],
    )
