from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncGenerator
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, PlainTextResponse

from app.api.router import api_router
from app.core.config import settings
from app.core.logger import logger
from app.services.pulse_service import pulse_service


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Lifespan context manager for startup and shutdown routines."""
    logger.info(f"Starting {settings.PROJECT_NAME} v{settings.VERSION} [{settings.ENVIRONMENT}]")
    logger.info(f"Docs available at http://{settings.HOST}:{settings.PORT}/docs")
    yield
    logger.info(f"Shutting down {settings.PROJECT_NAME}")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="High-performance developer telemetry & cloud observability API.",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# Configure CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS if isinstance(settings.CORS_ORIGINS, list) else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Router
app.include_router(api_router, prefix=settings.API_V1_STR)

# Root dashboard template loader
TEMPLATE_PATH = Path(__file__).resolve().parent / "templates" / "dashboard.html"


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def root_dashboard() -> HTMLResponse:
    """Renders the DevPulse developer dashboard at the root URL."""
    if TEMPLATE_PATH.exists():
        return HTMLResponse(content=TEMPLATE_PATH.read_text(encoding="utf-8"))
    return HTMLResponse(
        content="""
        <html>
            <body style='font-family:sans-serif;background:#0f172a;color:#f8fafc;padding:40px;'>
                <h1>⚡ DevPulse Backend is Running</h1>
                <p>Visit <a style='color:#818cf8;' href='/docs'>/docs</a> for the OpenAPI documentation.</p>
            </body>
        </html>
        """
    )


@app.get(
    "/metrics",
    response_class=PlainTextResponse,
    tags=["Observability"],
    summary="Prometheus Metrics Exporter",
    description="Exposes system performance metrics formatted for Prometheus and Grafana scrapers.",
)
async def prometheus_metrics() -> PlainTextResponse:
    """Exposes telemetry in standard Prometheus exposition format."""
    sys_metric = pulse_service.get_system_metrics()
    summary = pulse_service.get_summary()
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
        f"devpulse_uptime_seconds {pulse_service.uptime_seconds}",
        "# HELP devpulse_events_total Total developer pulse events recorded",
        "# TYPE devpulse_events_total counter",
        f"devpulse_events_total {summary.total_events_recorded}",
    ]
    return PlainTextResponse(
        "\n".join(lines) + "\n",
        media_type="text/plain; version=0.0.4; charset=utf-8",
    )
