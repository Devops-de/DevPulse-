from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncGenerator
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from app.api.router import api_router
from app.core.config import settings
from app.core.logger import logger


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
    description="High-performance developer telemetry & pulse monitoring API.",
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
