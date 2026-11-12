from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, PlainTextResponse

from app.api.router import api_router
from app.core.config import settings
from app.core.logger import logger
from app.services.pulse_service import pulse_service

FALLBACK_HTML = """
<html>
    <body style='font-family:sans-serif;background:#0f172a;color:#f8fafc;padding:40px;'>
        <h1>⚡ DevPulse Backend is Running</h1>
        <p>Visit <a style='color:#818cf8;' href='/docs'>/docs</a> for OpenAPI documentation.</p>
    </body>
</html>
"""

TEMPLATE_PATH = Path(__file__).resolve().parent / "templates" / "dashboard.html"


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Lifespan context manager for startup and shutdown routines."""
    logger.info(
        "Starting %s v%s [%s]",
        settings.PROJECT_NAME,
        settings.VERSION,
        settings.ENVIRONMENT,
    )
    logger.info("Docs available at http://%s:%s/docs", settings.HOST, settings.PORT)
    yield
    logger.info("Shutting down %s", settings.PROJECT_NAME)


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
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Router
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def root_dashboard() -> HTMLResponse:
    """Renders the DevPulse developer dashboard at the root URL."""
    if TEMPLATE_PATH.exists():
        return HTMLResponse(content=TEMPLATE_PATH.read_text(encoding="utf-8"))
    return HTMLResponse(content=FALLBACK_HTML)


@app.get(
    "/metrics",
    response_class=PlainTextResponse,
    tags=["Observability"],
    summary="Prometheus Metrics Exporter",
    description="Exposes system performance metrics formatted for Prometheus and Grafana scrapers.",
)
async def prometheus_metrics() -> PlainTextResponse:
    """Exposes telemetry in standard Prometheus exposition format."""
    return PlainTextResponse(
        pulse_service.get_prometheus_exposition(),
        media_type="text/plain; version=0.0.4; charset=utf-8",
    )
