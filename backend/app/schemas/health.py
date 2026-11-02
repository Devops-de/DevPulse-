from datetime import datetime
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Schema for health status endpoint."""
    status: str = Field(..., description="Overall service status, e.g., 'ok' or 'degraded'")
    app_name: str = Field(..., description="Application name")
    version: str = Field(..., description="Application release version")
    environment: str = Field(..., description="Active environment name")
    uptime_seconds: float = Field(..., description="Application uptime in seconds")
    timestamp: datetime = Field(..., description="Current server timestamp")
    python_version: str = Field(..., description="Python runtime version")
